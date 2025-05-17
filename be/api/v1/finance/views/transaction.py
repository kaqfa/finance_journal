from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from django.db.models.functions import ExtractMonth, ExtractYear
from decimal import Decimal
from datetime import datetime

from finance.models import Transaction, Tag
from ..serializers import (
    TransactionSerializer, 
    TransactionListSerializer, 
    CategorySummarySerializer, 
    MonthlyReportSerializer,
    TransactionSummarySerializer
)

class TransactionViewSet(viewsets.ModelViewSet):
    """
    manajemen transaksi keuangan.
    
    Transaksi merepresentasikan pergerakan uang, bisa berupa pemasukan (income),
    pengeluaran (expense), atau transfer antar wallet. Ketika transaksi dibuat,
    diupdate, atau dihapus, saldo wallet terkait akan diupdate secara otomatis.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'wallet__name', 'category__name']
    ordering_fields = ['transaction_date', 'amount', 'created_at']
    ordering = ['-transaction_date']

    def get_serializer_class(self):
        """
        Menggunakan serializer yang berbeda untuk list dan detail view.
        """
        if self.action == 'list':
            return TransactionListSerializer
        return TransactionSerializer

    def get_queryset(self):
        """
        Filter queryset untuk hanya menampilkan transaksi milik user saat ini
        dengan berbagai opsi filter tambahan berdasarkan query parameter.
        """
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Filter by wallet if specified
        wallet_id = self.request.query_params.get('wallet')
        if wallet_id:
            queryset = queryset.filter(wallet_id=wallet_id)
        
        # Filter by type if specified
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(type=transaction_type)
        
        # Filter by category if specified
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by tag if specified
        tag_id = self.request.query_params.get('tag')
        if tag_id:
            queryset = queryset.filter(transaction_tags__tag_id=tag_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(transaction_date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(transaction_date__lte=end_date)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Mendapatkan ringkasan transaksi (total pemasukan, pengeluaran, dan saldo).
        
        Query Parameters:
            wallet (int): ID wallet (opsional)
            start_date (date): Tanggal mulai filter (opsional)
            end_date (date): Tanggal akhir filter (opsional)
            
        Returns:
            dict: Ringkasan transaksi berisi income, expense, dan balance
        """
        wallet_id = request.query_params.get('wallet')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = Transaction.objects.filter(user=request.user)
        
        # Apply filters if specified
        if wallet_id:
            queryset = queryset.filter(wallet_id=wallet_id)
        
        if start_date:
            queryset = queryset.filter(transaction_date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(transaction_date__lte=end_date)
        
        # Calculate totals
        income = queryset.filter(type='income').aggregate(total=Sum('amount'))['total'] or Decimal('0')
        expense = queryset.filter(type='expense').aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        data = {
            'income': income,
            'expense': expense,
            'balance': income - expense
        }
        
        serializer = TransactionSummarySerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Mendapatkan transaksi dikelompokkan berdasarkan kategori dengan jumlah total
        dan persentase.
        
        Query Parameters:
            type (str): Tipe transaksi ('income' atau 'expense', default: 'expense')
            wallet (int): ID wallet (opsional)
            start_date (date): Tanggal mulai filter (opsional)
            end_date (date): Tanggal akhir filter (opsional)
            
        Returns:
            list: Daftar kategori dengan jumlah dan persentase transaksi
        """
        transaction_type = request.query_params.get('type', 'expense')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        wallet_id = request.query_params.get('wallet')
        
        # Start with base queryset
        queryset = Transaction.objects.filter(
            user=request.user,
            type=transaction_type
        )
        
        # Apply filters
        if start_date:
            queryset = queryset.filter(transaction_date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(transaction_date__lte=end_date)
        
        if wallet_id:
            queryset = queryset.filter(wallet_id=wallet_id)
        
        # Get total amount for percentage calculation
        total_amount = queryset.aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        # Group by category
        categories = queryset.values(
            'category__id', 
            'category__name',
            'category__icon',
            'category__color'
        ).annotate(
            amount=Sum('amount')
        ).order_by('-amount')
        
        # Calculate percentage for each category
        for category in categories:
            percentage = (category['amount'] / total_amount * 100) if total_amount > 0 else 0
            category['percentage'] = round(percentage, 2)
        
        serializer = CategorySummarySerializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def monthly_report(self, request):
        """
        Mendapatkan laporan bulanan untuk pemasukan dan pengeluaran.
        
        Laporan ini menampilkan total pemasukan, pengeluaran, dan saldo untuk
        setiap bulan dalam tahun yang ditentukan.
        
        Query Parameters:
            year (int): Tahun untuk laporan (default: tahun saat ini)
            wallet (int): ID wallet (opsional)
            
        Returns:
            list: Daftar data bulanan dengan income, expense, dan balance
        """
        year = request.query_params.get('year')
        wallet_id = request.query_params.get('wallet')
        
        # If no year specified, use current year
        if not year:
            year = datetime.now().year
        
        # Start with base queryset
        queryset = Transaction.objects.filter(
            user=request.user,
            transaction_date__year=year
        )
        
        # Apply wallet filter if specified
        if wallet_id:
            queryset = queryset.filter(wallet_id=wallet_id)
        
        # Annotate month and year
        queryset = queryset.annotate(
            month=ExtractMonth('transaction_date'),
            year=ExtractYear('transaction_date')
        )
        
        # Get monthly income
        income_by_month = queryset.filter(
            type='income'
        ).values(
            'month', 'year'
        ).annotate(
            total=Sum('amount')
        ).order_by('year', 'month')
        
        # Get monthly expense
        expense_by_month = queryset.filter(
            type='expense'
        ).values(
            'month', 'year'
        ).annotate(
            total=Sum('amount')
        ).order_by('year', 'month')
        
        # Prepare results
        months_data = {}
        
        # Initialize with zeros for all months
        for month in range(1, 13):
            months_data[month] = {
                'month': month,
                'year': int(year),
                'income': Decimal('0'),
                'expense': Decimal('0'),
                'balance': Decimal('0')
            }
        
        # Fill in actual data
        for item in income_by_month:
            month = item['month']
            months_data[month]['income'] = item['total']
            months_data[month]['balance'] = months_data[month]['income'] - months_data[month]['expense']
            
        for item in expense_by_month:
            month = item['month']
            months_data[month]['expense'] = item['total']
            months_data[month]['balance'] = months_data[month]['income'] - months_data[month]['expense']
        
        # Convert to list
        result = list(months_data.values())
        
        serializer = MonthlyReportSerializer(result, many=True)
        return Response(serializer.data)