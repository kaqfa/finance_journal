from rest_framework import serializers
from invest.models import Asset, AssetPrice
from datetime import datetime, timedelta
from django.utils import timezone


class AssetPriceSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model AssetPrice.
    
    Menangani data harga asset dengan informasi volume dan market cap.
    """
    formatted_timestamp = serializers.SerializerMethodField()
    
    class Meta:
        model = AssetPrice
        fields = ['id', 'price', 'volume', 'market_cap', 'timestamp', 
                  'formatted_timestamp', 'source']
        
    def get_formatted_timestamp(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')


class AssetListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer untuk model Asset dalam format list.
    
    Digunakan untuk menampilkan daftar asset dengan informasi minimal
    yang diperlukan untuk list view dan dropdowns.
    """
    latest_price = serializers.SerializerMethodField()
    price_change_24h = serializers.SerializerMethodField()
    
    class Meta:
        model = Asset
        fields = ['id', 'symbol', 'name', 'type', 'exchange', 'sector', 
                  'currency', 'latest_price', 'price_change_24h', 'is_active']
    
    def get_latest_price(self, obj):
        """Mendapatkan harga terbaru asset"""
        latest_price = obj.prices.order_by('-timestamp').first()
        return latest_price.price if latest_price else 0
    
    def get_price_change_24h(self, obj):
        """Menghitung perubahan harga 24 jam terakhir"""
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        
        latest_price = obj.prices.filter(
            timestamp__gte=yesterday
        ).order_by('-timestamp').first()
        
        previous_price = obj.prices.filter(
            timestamp__lt=yesterday
        ).order_by('-timestamp').first()
        
        if latest_price and previous_price:
            change = ((latest_price.price - previous_price.price) / previous_price.price) * 100
            return round(change, 2)
        return 0


class AssetSerializer(serializers.ModelSerializer):
    """
    Full serializer untuk model Asset (Master Data Aset Investasi).
    
    Asset merepresentasikan instrumen investasi seperti saham, crypto, bond, dll.
    yang bisa dibeli/dijual dalam portfolio investment.
    
    Attributes:
        symbol (str): Simbol/kode asset (BBRI, BTC, dll)
        name (str): Nama lengkap asset  
        type (str): Tipe asset ('stock', 'crypto', 'bond', 'reit', 'mutual_fund')
        exchange (str): Bursa tempat trading asset
        sector (str): Sektor industri asset
        currency (str): Mata uang asset (default: 'IDR')
        is_active (bool): Status aktif asset
        created_at (datetime): Waktu pembuatan (read-only)
    """
    price_history = AssetPriceSerializer(source='prices', many=True, read_only=True)
    latest_price = serializers.SerializerMethodField()
    price_change_24h = serializers.SerializerMethodField()
    total_holders = serializers.SerializerMethodField()
    
    class Meta:
        model = Asset
        fields = ['id', 'symbol', 'name', 'type', 'exchange', 'sector', 
                  'currency', 'is_active', 'created_at', 'latest_price', 
                  'price_change_24h', 'total_holders', 'price_history']
        read_only_fields = ['created_at', 'id']
    
    def get_latest_price(self, obj):
        """Mendapatkan harga terbaru asset"""
        latest_price = obj.prices.order_by('-timestamp').first()
        return latest_price.price if latest_price else 0
    
    def get_price_change_24h(self, obj):
        """Menghitung perubahan harga 24 jam terakhir"""
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        
        latest_price = obj.prices.filter(
            timestamp__gte=yesterday
        ).order_by('-timestamp').first()
        
        previous_price = obj.prices.filter(
            timestamp__lt=yesterday
        ).order_by('-timestamp').first()
        
        if latest_price and previous_price:
            change = ((latest_price.price - previous_price.price) / previous_price.price) * 100
            return round(change, 2)
        return 0
    
    def get_total_holders(self, obj):
        """Menghitung total holders yang memiliki asset ini"""
        return obj.holdings.filter(quantity__gt=0).count()


class AssetSearchSerializer(serializers.ModelSerializer):
    """
    Minimal serializer untuk pencarian asset.
    
    Digunakan untuk endpoint search dengan response cepat.
    """
    latest_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Asset
        fields = ['id', 'symbol', 'name', 'type', 'latest_price']
    
    def get_latest_price(self, obj):
        latest_price = obj.prices.order_by('-timestamp').first()
        return latest_price.price if latest_price else 0
