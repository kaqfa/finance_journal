from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from finance.models import Category, Tag, Transaction
from ..serializers import CategorySerializer, TagSerializer, TransactionListSerializer
from api.utils.permissions import IsOwner
from api.utils.mixins import ChoicesMixin

class CategoryViewSet(ChoicesMixin, viewsets.ModelViewSet):
    """
    manajemen kategori transaksi keuangan.
    
    Kategori digunakan untuk mengklasifikasikan transaksi keuangan sebagai 
    pemasukan (income) atau pengeluaran (expense).
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'type', 'created_at']
    ordering = ['type', 'name']
    choices_config = {
        'category_types': {
            'choices': Category.CATEGORY_TYPE_CHOICES,
            'description': 'Tipe-tipe kategori yang tersedia'
        }
    }

    def get_swagger_auto_schema(self):
        return super().get_swagger_auto_schema()

    def get_queryset(self):
        """
        Filter queryset untuk hanya menampilkan kategori milik user saat ini.
        """
        return Category.objects.filter(user=self.request.user)
    
    
    @action(detail=False, methods=['get'])
    def income(self, request):
        """
        Mendapatkan daftar kategori pemasukan (income) saja.
        
        Returns:
            List kategori dengan tipe 'income'
        """
        categories = Category.objects.filter(user=request.user, type='income')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expense(self, request):
        """
        Mendapatkan daftar kategori pengeluaran (expense) saja.
        
        Returns:
            List kategori dengan tipe 'expense'
        """
        categories = Category.objects.filter(user=request.user, type='expense')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """
    manajemen tag transaksi.
    
    Tag adalah label tambahan yang bisa diterapkan pada transaksi untuk
    membantu mengorganisasi dan mengkategorikan transaksi melebihi yang
    bisa dilakukan dengan kategori standar. Transaksi bisa memiliki
    beberapa tag.
    
    """
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        """
        Filter queryset untuk hanya menampilkan tag milik user saat ini.
        """
        return Tag.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        """
        Mendapatkan semua transaksi yang memiliki tag tertentu.
        
        Returns:
            List transaksi yang memiliki tag ini
        """
        tag = self.get_object()
        transactions = Transaction.objects.filter(
            transaction_tags__tag=tag
        )
        
        serializer = TransactionListSerializer(transactions, many=True)
        return Response(serializer.data)