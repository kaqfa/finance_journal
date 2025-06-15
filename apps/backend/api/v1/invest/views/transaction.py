from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from invest.models import InvestmentTransaction, InvestmentPortfolio, Asset
from ..serializers import (
    InvestmentTransactionSerializer,
    InvestmentTransactionListSerializer,
    TransactionSummarySerializer,
    TransactionsByAssetSerializer
)
from api.utils.permissions import IsOwner
from api.utils.mixins import ChoicesMixin


class InvestmentTransactionViewSet(ChoicesMixin, viewsets.ModelViewSet):
    """
    Investment Transaction Management.
    
    Transaction merepresentasikan aktivitas jual/beli asset dalam portfolio
    investasi seperti buy, sell, dividend, stock split, bonus shares.
    
    Features:
    - CRUD operations untuk transaksi investasi
    - Auto-update holdings setelah transaksi
    - Transaction summary dan analytics
    - Grouping berdasarkan asset, portfolio, periode
    - Import/export capabilities
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['asset__symbol', 'asset__name', 'portfolio__name', 'broker', 'notes']
    ordering_fields = ['transaction_date', 'total_amount', 'created_at']
    ordering = ['-transaction_date']
    
    choices_config = {
        'transaction_types': {
            'choices': InvestmentTransaction.TRANSACTION_TYPE_CHOICES,
            'description': 'Tipe-tipe transaksi investasi yang tersedia'
        }
    }
    
    def get_serializer_class(self):
        """Menggunakan serializer yang berbeda untuk list dan detail view"""
        if self.action == 'list':
            return InvestmentTransactionListSerializer
        return InvestmentTransactionSerializer
    
    def get_queryset(self):
        """
        Filter queryset untuk hanya menampilkan transaksi milik user saat ini
        dengan berbagai opsi filtering.
        
        Query Parameters:
        - portfolio: Filter berdasarkan portfolio ID
        - asset: Filter berdasarkan asset ID
        - transaction_type: Filter berdasarkan tipe transaksi
        - start_date: Tanggal mulai filter
        - end_date: Tanggal akhir filter
        - min_amount: Minimum total amount
        - max_amount: Maximum total amount
        - broker: Filter berdasarkan broker
        """
        queryset = InvestmentTransaction.objects.filter(user=self.request.user)
        
        # Filter by portfolio
        portfolio_id = self.request.query_params.get('portfolio')
        if portfolio_id:
            queryset = queryset.filter(portfolio_id=portfolio_id)
        
        # Filter by asset
        asset_id = self.request.query_params.get('asset')
        if asset_id:
            queryset = queryset.filter(asset_id=asset_id)
        
        # Filter by transaction type
        transaction_type = self.request.query_params.get('transaction_type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(transaction_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(transaction_date__lte=end_date)
        
        # Filter by amount range
        min_amount = self.request.query_params.get('min_amount')
        max_amount = self.request.query_params.get('max_amount')
        
        if min_amount:
            queryset = queryset.filter(total_amount__gte=min_amount)
        if max_amount:
            queryset = queryset.filter(total_amount__lte=max_amount)
        
        # Filter by broker
        broker = self.request.query_params.get('broker')
        if broker:
            queryset = queryset.filter(broker__icontains=broker)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Mendapatkan ringkasan transaksi investasi.
        
        Query Parameters:
        - portfolio: Filter berdasarkan portfolio ID (optional)
        - start_date: Tanggal mulai filter (optional)
        - end_date: Tanggal akhir filter (optional)
        
        Returns summary statistik transaksi dalam periode tertentu.
        """
        queryset = self.get_queryset()
        
        # Apply additional filters
        portfolio_id = request.query_params.get('portfolio')
        if portfolio_id:
            queryset = queryset.filter(portfolio_id=portfolio_id)
        
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(transaction_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(transaction_date__lte=end_date)
        
        # Calculate summary statistics
        total_transactions = queryset.count()
        
        # Group by transaction type
        buy_transactions = queryset.filter(transaction_type='buy')
        sell_transactions = queryset.filter(transaction_type='sell')
        dividend_transactions = queryset.filter(transaction_type='dividend')
        
        total_buy_amount = buy_transactions.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        total_sell_amount = sell_transactions.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        total_dividend = dividend_transactions.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        total_fees = queryset.aggregate(
            total=Sum('fees')
        )['total'] or 0
        
        net_investment = total_buy_amount - total_sell_amount
        
        # Most traded asset
        most_traded = queryset.values('asset__symbol', 'asset__name').annotate(
            transaction_count=Count('id'),
            total_volume=Sum('total_amount')
        ).order_by('-transaction_count').first()
        
        most_traded_asset = None
        if most_traded:
            most_traded_asset = f"{most_traded['asset__symbol']} - {most_traded['asset__name']}"
        
        # Transaction frequency by month
        transaction_frequency = {}
        for transaction in queryset:
            month_key = transaction.transaction_date.strftime('%Y-%m')
            if month_key not in transaction_frequency:
                transaction_frequency[month_key] = 0
            transaction_frequency[month_key] += 1
        
        summary_data = {
            'total_transactions': total_transactions,
            'total_buy_amount': total_buy_amount,
            'total_sell_amount': total_sell_amount,
            'total_dividend': total_dividend,
            'total_fees': total_fees,
            'net_investment': net_investment,
            'most_traded_asset': most_traded_asset,
            'transaction_frequency': transaction_frequency,
            'period': {
                'start_date': start_date,
                'end_date': end_date,
                'portfolio_id': portfolio_id
            },
            'generated_at': timezone.now()
        }
        
        return Response(summary_data)
    
    @action(detail=False, methods=['get'])
    def by_asset(self, request):
        """
        Mendapatkan transaksi yang dikelompokkan berdasarkan asset.
        
        Query Parameters sama dengan endpoint utama.
        
        Returns total transaksi, volume, dan P&L per asset.
        """
        queryset = self.get_queryset()
        
        # Group transactions by asset
        asset_groups = {}
        
        for transaction in queryset:
            asset_id = str(transaction.asset.id)
            
            if asset_id not in asset_groups:
                asset_groups[asset_id] = {
                    'asset': transaction.asset,
                    'transactions': [],
                    'transaction_count': 0,
                    'total_quantity_bought': 0,
                    'total_quantity_sold': 0,
                    'total_buy_amount': 0,
                    'total_sell_amount': 0,
                    'total_dividend': 0
                }
            
            group = asset_groups[asset_id]
            group['transactions'].append(transaction)
            group['transaction_count'] += 1
            
            if transaction.transaction_type == 'buy':
                group['total_quantity_bought'] += transaction.quantity
                group['total_buy_amount'] += transaction.total_amount
            elif transaction.transaction_type == 'sell':
                group['total_quantity_sold'] += transaction.quantity
                group['total_sell_amount'] += transaction.total_amount
            elif transaction.transaction_type == 'dividend':
                group['total_dividend'] += transaction.total_amount
        
        # Calculate additional metrics for each asset
        results = []
        
        for asset_id, group in asset_groups.items():
            # Calculate realized P&L
            realized_pnl = group['total_sell_amount'] - (
                group['total_quantity_sold'] * 
                (group['total_buy_amount'] / group['total_quantity_bought'] if group['total_quantity_bought'] > 0 else 0)
            )
            
            # Get current holding
            current_holding = group['total_quantity_bought'] - group['total_quantity_sold']
            
            from ..serializers import AssetListSerializer
            
            result = {
                'asset': AssetListSerializer(group['asset']).data,
                'transaction_count': group['transaction_count'],
                'total_quantity_bought': group['total_quantity_bought'],
                'total_quantity_sold': group['total_quantity_sold'],
                'total_buy_amount': group['total_buy_amount'],
                'total_sell_amount': group['total_sell_amount'],
                'total_dividend': group['total_dividend'],
                'realized_pnl': realized_pnl,
                'current_holding': current_holding
            }
            
            results.append(result)
        
        # Sort by total buy amount
        results.sort(key=lambda x: x['total_buy_amount'], reverse=True)
        
        return Response({
            'asset_groups': results,
            'total_assets': len(results),
            'generated_at': timezone.now()
        })
    
    @action(detail=False, methods=['get'])
    def monthly_report(self, request):
        """
        Mendapatkan laporan transaksi bulanan.
        
        Query Parameters:
        - year: Tahun untuk laporan (default: tahun saat ini)
        - portfolio: Portfolio ID (optional)
        
        Returns breakdown transaksi per bulan dalam tahun tertentu.
        """
        year = int(request.query_params.get('year', timezone.now().year))
        portfolio_id = request.query_params.get('portfolio')
        
        queryset = self.get_queryset().filter(
            transaction_date__year=year
        )
        
        if portfolio_id:
            queryset = queryset.filter(portfolio_id=portfolio_id)
        
        # Group by month
        monthly_data = {}
        
        for month in range(1, 13):
            month_transactions = queryset.filter(transaction_date__month=month)
            
            total_buy = month_transactions.filter(
                transaction_type='buy'
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            
            total_sell = month_transactions.filter(
                transaction_type='sell'
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            
            total_dividend = month_transactions.filter(
                transaction_type='dividend'
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            
            monthly_data[f"{year}-{month:02d}"] = {
                'month': f"{year}-{month:02d}",
                'total_transactions': month_transactions.count(),
                'total_buy_amount': total_buy,
                'total_sell_amount': total_sell,
                'total_dividend': total_dividend,
                'net_investment': total_buy - total_sell,
                'most_traded_asset': None
            }
            
            # Get most traded asset for the month
            most_traded = month_transactions.values(
                'asset__symbol', 'asset__name'
            ).annotate(
                count=Count('id')
            ).order_by('-count').first()
            
            if most_traded:
                monthly_data[f"{year}-{month:02d}"]['most_traded_asset'] = (
                    f"{most_traded['asset__symbol']} - {most_traded['asset__name']}"
                )
        
        # Calculate year totals
        year_totals = {
            'year': year,
            'total_transactions': queryset.count(),
            'total_buy_amount': queryset.filter(
                transaction_type='buy'
            ).aggregate(total=Sum('total_amount'))['total'] or 0,
            'total_sell_amount': queryset.filter(
                transaction_type='sell'
            ).aggregate(total=Sum('total_amount'))['total'] or 0,
            'total_dividend': queryset.filter(
                transaction_type='dividend'
            ).aggregate(total=Sum('total_amount'))['total'] or 0,
        }
        
        year_totals['net_investment'] = (
            year_totals['total_buy_amount'] - year_totals['total_sell_amount']
        )
        
        return Response({
            'year_totals': year_totals,
            'monthly_data': monthly_data,
            'portfolio_id': portfolio_id,
            'generated_at': timezone.now()
        })
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """
        Membuat multiple transaksi sekaligus (bulk import).
        
        Request Body:
        - transactions: List of transaction data
        - validate_only: Boolean untuk validasi saja tanpa create (default: false)
        
        Useful untuk import dari CSV/Excel atau synchronization dengan broker.
        """
        transactions_data = request.data.get('transactions', [])
        validate_only = request.data.get('validate_only', False)
        
        if not transactions_data:
            return Response({
                'error': 'Transactions data is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate all transactions first
        serializers = []
        errors = []
        
        for i, transaction_data in enumerate(transactions_data):
            serializer = InvestmentTransactionSerializer(
                data=transaction_data,
                context={'request': request}
            )
            
            if serializer.is_valid():
                serializers.append(serializer)
            else:
                errors.append({
                    'index': i,
                    'data': transaction_data,
                    'errors': serializer.errors
                })
        
        if errors:
            return Response({
                'error': 'Validation failed for some transactions',
                'failed_transactions': errors,
                'successful_count': len(serializers),
                'failed_count': len(errors)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if validate_only:
            return Response({
                'message': 'All transactions are valid',
                'transaction_count': len(serializers)
            })
        
        # Create all transactions
        created_transactions = []
        
        for serializer in serializers:
            transaction = serializer.save()
            created_transactions.append(transaction)
        
        # Serialize created transactions for response
        response_serializer = InvestmentTransactionListSerializer(
            created_transactions, many=True
        )
        
        return Response({
            'message': f'Successfully created {len(created_transactions)} transactions',
            'transactions': response_serializer.data,
            'created_count': len(created_transactions)
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def export(self, request):
        """
        Export transaksi ke format CSV.
        
        Query Parameters sama dengan filtering utama.
        
        Returns CSV data untuk download.
        """
        queryset = self.get_queryset()
        
        # Prepare CSV data
        csv_data = []
        csv_headers = [
            'Date', 'Portfolio', 'Asset Symbol', 'Asset Name', 'Type',
            'Quantity', 'Price', 'Total Amount', 'Fees', 'Broker', 'Notes'
        ]
        
        for transaction in queryset:
            csv_data.append([
                transaction.transaction_date.strftime('%Y-%m-%d'),
                transaction.portfolio.name,
                transaction.asset.symbol,
                transaction.asset.name,
                transaction.transaction_type,
                str(transaction.quantity),
                str(transaction.price),
                str(transaction.total_amount),
                str(transaction.fees),
                transaction.broker or '',
                transaction.notes or ''
            ])
        
        return Response({
            'headers': csv_headers,
            'data': csv_data,
            'total_records': len(csv_data),
            'generated_at': timezone.now(),
            'filename': f'investment_transactions_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv'
        })
