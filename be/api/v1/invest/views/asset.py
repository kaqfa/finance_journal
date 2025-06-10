from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg, Max, Min
from django.utils import timezone
from datetime import timedelta

from invest.models import Asset, AssetPrice
from ..serializers import (
    AssetSerializer,
    AssetListSerializer, 
    AssetSearchSerializer,
    AssetPriceSerializer
)
from api.utils.permissions import IsOwner
from api.utils.mixins import ChoicesMixin


class AssetViewSet(ChoicesMixin, viewsets.ModelViewSet):
    """
    Asset Management (Master Data Aset Investasi).
    
    Asset merepresentasikan instrumen investasi seperti saham, crypto, bond, REIT, 
    mutual fund yang bisa dibeli/dijual dalam portfolio investment.
    
    Endpoint ini menyediakan:
    - CRUD operations untuk asset (admin only untuk create/update/delete)
    - Search asset berdasarkan symbol/name
    - Filter berdasarkan type, exchange, sector
    - Price history untuk setiap asset
    - Analytics dan statistics
    """
    queryset = Asset.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['symbol', 'name', 'sector']
    ordering_fields = ['symbol', 'name', 'created_at']
    ordering = ['symbol']
    
    choices_config = {
        'asset_types': {
            'choices': Asset.TYPE_CHOICES,
            'description': 'Tipe-tipe asset yang tersedia untuk investasi'
        }
    }
    
    def get_serializer_class(self):
        """Menggunakan serializer yang berbeda untuk berbagai actions"""
        if self.action == 'list':
            return AssetListSerializer
        elif self.action == 'search':
            return AssetSearchSerializer
        return AssetSerializer
    
    def get_queryset(self):
        """
        Filter queryset berdasarkan query parameters.
        
        Query Parameters:
        - type: Filter berdasarkan asset type
        - exchange: Filter berdasarkan exchange
        - sector: Filter berdasarkan sector
        - currency: Filter berdasarkan currency
        """
        queryset = Asset.objects.filter(is_active=True)
        
        # Filter by type
        asset_type = self.request.query_params.get('type')
        if asset_type:
            queryset = queryset.filter(type=asset_type)
        
        # Filter by exchange
        exchange = self.request.query_params.get('exchange')
        if exchange:
            queryset = queryset.filter(exchange__icontains=exchange)
        
        # Filter by sector
        sector = self.request.query_params.get('sector')
        if sector:
            queryset = queryset.filter(sector__icontains=sector)
        
        # Filter by currency
        currency = self.request.query_params.get('currency')
        if currency:
            queryset = queryset.filter(currency=currency)
        
        return queryset
    
    def get_permissions(self):
        """
        Override permissions untuk read-only access untuk regular users.
        Admin/staff bisa melakukan create/update/delete.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Endpoint khusus untuk pencarian asset yang cepat.
        
        Query Parameters:
        - q: Search term untuk symbol atau name
        - limit: Maksimal jumlah results (default: 10)
        
        Returns minimal asset info untuk autocomplete/dropdown.
        """
        query = request.query_params.get('q', '')
        limit = int(request.query_params.get('limit', 10))
        
        if not query:
            return Response([])
        
        queryset = self.get_queryset().filter(
            Q(symbol__icontains=query) | Q(name__icontains=query)
        )[:limit]
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def prices(self, request, pk=None):
        """
        Mendapatkan price history untuk asset tertentu.
        
        Query Parameters:
        - days: Jumlah hari ke belakang (default: 30)
        - interval: Interval data ('daily', 'weekly', 'monthly')
        """
        asset = self.get_object()
        days = int(request.query_params.get('days', 30))
        interval = request.query_params.get('interval', 'daily')
        
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        prices = asset.prices.filter(
            timestamp__gte=start_date,
            timestamp__lte=end_date
        ).order_by('-timestamp')
        
        # Group by interval if needed
        if interval == 'weekly':
            # Get one price per week (latest price of each week)
            prices = prices.extra(
                select={'week': "strftime('%Y-%W', timestamp)"}
            ).values('week').annotate(
                latest_timestamp=Max('timestamp')
            ).values_list('latest_timestamp', flat=True)
            prices = asset.prices.filter(timestamp__in=prices).order_by('-timestamp')
        
        elif interval == 'monthly':
            # Get one price per month (latest price of each month)
            prices = prices.extra(
                select={'month': "strftime('%Y-%m', timestamp)"}
            ).values('month').annotate(
                latest_timestamp=Max('timestamp')
            ).values_list('latest_timestamp', flat=True)
            prices = asset.prices.filter(timestamp__in=prices).order_by('-timestamp')
        
        serializer = AssetPriceSerializer(prices, many=True)
        return Response({
            'asset': AssetListSerializer(asset).data,
            'price_history': serializer.data,
            'period': f"{days} days",
            'interval': interval
        })
    
    @action(detail=True, methods=['post'])
    def add_price(self, request, pk=None):
        """
        Menambahkan data harga untuk asset (admin/system only).
        
        Request Body:
        - price: Harga asset
        - volume: Volume trading (optional)
        - market_cap: Market capitalization (optional)
        - timestamp: Timestamp harga (optional, default: now)
        - source: Sumber data (optional)
        """
        if not request.user.is_staff:
            return Response(
                {"error": "Only admin can add price data"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        asset = self.get_object()
        
        price_data = {
            'asset': asset.id,
            'price': request.data.get('price'),
            'volume': request.data.get('volume'),
            'market_cap': request.data.get('market_cap'),
            'timestamp': request.data.get('timestamp', timezone.now()),
            'source': request.data.get('source', 'manual')
        }
        
        serializer = AssetPriceSerializer(data=price_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """
        Mendapatkan asset yang dikelompokkan berdasarkan type.
        
        Returns:
        Dict dengan key = asset type, value = list of assets
        """
        asset_types = {}
        
        for asset_type, display_name in Asset.TYPE_CHOICES:
            assets = self.get_queryset().filter(type=asset_type)
            serializer = AssetListSerializer(assets, many=True)
            asset_types[asset_type] = {
                'display_name': display_name,
                'count': assets.count(),
                'assets': serializer.data
            }
        
        return Response(asset_types)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Mendapatkan statistics umum tentang asset.
        
        Returns berbagai metrics seperti total assets, breakdown by type, dll.
        """
        queryset = self.get_queryset()
        
        # Basic counts
        total_assets = queryset.count()
        type_breakdown = {}
        
        for asset_type, display_name in Asset.TYPE_CHOICES:
            count = queryset.filter(type=asset_type).count()
            type_breakdown[asset_type] = {
                'display_name': display_name,
                'count': count,
                'percentage': round((count / total_assets) * 100, 2) if total_assets > 0 else 0
            }
        
        # Exchange breakdown
        exchange_breakdown = queryset.values('exchange').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Sector breakdown
        sector_breakdown = queryset.exclude(
            sector__isnull=True
        ).exclude(
            sector=''
        ).values('sector').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Recent additions
        last_30_days = timezone.now() - timedelta(days=30)
        recent_additions = queryset.filter(
            created_at__gte=last_30_days
        ).count()
        
        return Response({
            'total_assets': total_assets,
            'type_breakdown': type_breakdown,
            'exchange_breakdown': list(exchange_breakdown),
            'sector_breakdown': list(sector_breakdown),
            'recent_additions': recent_additions,
            'most_popular_sectors': list(sector_breakdown[:5]),
            'generated_at': timezone.now()
        })
