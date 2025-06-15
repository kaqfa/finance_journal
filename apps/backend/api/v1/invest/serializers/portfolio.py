from rest_framework import serializers
from invest.models import InvestmentPortfolio, InvestmentHolding
from .asset import AssetListSerializer
from decimal import Decimal


class InvestmentHoldingSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model InvestmentHolding.
    
    Menampilkan informasi kepemilikan asset dalam portfolio dengan
    perhitungan profit/loss dan persentase allocation.
    """
    asset = AssetListSerializer(read_only=True)
    unrealized_pnl_percentage = serializers.SerializerMethodField()
    allocation_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = InvestmentHolding
        fields = ['id', 'asset', 'quantity', 'average_price', 'total_cost',
                  'current_price', 'current_value', 'unrealized_pnl', 
                  'unrealized_pnl_percentage', 'allocation_percentage', 'last_updated']
        read_only_fields = ['id', 'user', 'portfolio', 'last_updated']
    
    def get_unrealized_pnl_percentage(self, obj):
        """Menghitung persentase unrealized P&L"""
        if obj.total_cost > 0:
            return round((obj.unrealized_pnl / obj.total_cost) * 100, 2)
        return 0
    
    def get_allocation_percentage(self, obj):
        """Menghitung persentase alokasi dalam portfolio"""
        portfolio = obj.portfolio
        total_portfolio_value = sum(
            holding.current_value for holding in portfolio.holdings.all()
        )
        if total_portfolio_value > 0:
            return round((obj.current_value / total_portfolio_value) * 100, 2)
        return 0


class InvestmentPortfolioListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer untuk model InvestmentPortfolio dalam format list.
    
    Digunakan untuk menampilkan daftar portfolio dengan informasi minimal
    yang diperlukan untuk list view.
    """
    total_value = serializers.SerializerMethodField()
    total_pnl = serializers.SerializerMethodField()
    total_pnl_percentage = serializers.SerializerMethodField()
    holdings_count = serializers.SerializerMethodField()
    
    class Meta:
        model = InvestmentPortfolio
        fields = ['id', 'name', 'description', 'initial_capital', 'risk_level',
                  'total_value', 'total_pnl', 'total_pnl_percentage', 
                  'holdings_count', 'is_active', 'created_at']
    
    def get_total_value(self, obj):
        """Menghitung total nilai portfolio saat ini"""
        return sum(holding.current_value for holding in obj.holdings.all())
    
    def get_total_pnl(self, obj):
        """Menghitung total profit/loss portfolio"""
        total_cost = sum(holding.total_cost for holding in obj.holdings.all())
        current_value = self.get_total_value(obj)
        return current_value - total_cost
    
    def get_total_pnl_percentage(self, obj):
        """Menghitung persentase profit/loss portfolio"""
        total_cost = sum(holding.total_cost for holding in obj.holdings.all())
        if total_cost > 0:
            pnl = self.get_total_pnl(obj)
            return round((pnl / total_cost) * 100, 2)
        return 0
    
    def get_holdings_count(self, obj):
        """Menghitung jumlah holdings dalam portfolio"""
        return obj.holdings.count()


class InvestmentPortfolioSerializer(serializers.ModelSerializer):
    """
    Full serializer untuk model InvestmentPortfolio.
    
    Portfolio merepresentasikan kumpulan investasi user dengan strategi
    dan alokasi target tertentu.
    
    Attributes:
        name (str): Nama portfolio
        description (str): Deskripsi portfolio
        initial_capital (decimal): Modal awal portfolio
        target_allocation (json): Target alokasi aset {"stocks": 70, "bonds": 20, "crypto": 10}
        risk_level (str): Tingkat risiko ('low', 'medium', 'high')
        is_active (bool): Status aktif portfolio
        created_at (datetime): Waktu pembuatan (read-only)
        updated_at (datetime): Waktu update terakhir (read-only)
    """
    holdings = InvestmentHoldingSerializer(many=True, read_only=True)
    total_value = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    total_pnl = serializers.SerializerMethodField()
    total_pnl_percentage = serializers.SerializerMethodField()
    actual_allocation = serializers.SerializerMethodField()
    performance_metrics = serializers.SerializerMethodField()
    
    class Meta:
        model = InvestmentPortfolio
        fields = ['id', 'name', 'description', 'initial_capital', 'target_allocation',
                  'risk_level', 'is_active', 'created_at', 'updated_at', 'holdings',
                  'total_value', 'total_cost', 'total_pnl', 'total_pnl_percentage',
                  'actual_allocation', 'performance_metrics']
        read_only_fields = ['created_at', 'updated_at', 'user']
    
    def create(self, validated_data):
        """Override create untuk mengset user dari request"""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
    def get_total_value(self, obj):
        """Menghitung total nilai portfolio saat ini"""
        return sum(holding.current_value for holding in obj.holdings.all())
    
    def get_total_cost(self, obj):
        """Menghitung total cost basis portfolio"""
        return sum(holding.total_cost for holding in obj.holdings.all())
    
    def get_total_pnl(self, obj):
        """Menghitung total profit/loss portfolio"""
        return self.get_total_value(obj) - self.get_total_cost(obj)
    
    def get_total_pnl_percentage(self, obj):
        """Menghitung persentase profit/loss portfolio"""
        total_cost = self.get_total_cost(obj)
        if total_cost > 0:
            pnl = self.get_total_pnl(obj)
            return round((pnl / total_cost) * 100, 2)
        return 0
    
    def get_actual_allocation(self, obj):
        """Menghitung alokasi aktual berdasarkan asset type"""
        total_value = self.get_total_value(obj)
        if total_value <= 0:
            return {}
        
        allocation = {}
        for holding in obj.holdings.all():
            asset_type = holding.asset.type
            if asset_type not in allocation:
                allocation[asset_type] = 0
            allocation[asset_type] += holding.current_value
        
        # Convert to percentage
        for asset_type in allocation:
            allocation[asset_type] = round((allocation[asset_type] / total_value) * 100, 2)
        
        return allocation
    
    def get_performance_metrics(self, obj):
        """Menghitung berbagai metrics performa portfolio"""
        holdings = obj.holdings.all()
        if not holdings:
            return {}
        
        total_value = self.get_total_value(obj)
        total_cost = self.get_total_cost(obj)
        
        winning_positions = sum(1 for h in holdings if h.unrealized_pnl > 0)
        losing_positions = sum(1 for h in holdings if h.unrealized_pnl < 0)
        total_positions = len(holdings)
        
        return {
            'total_positions': total_positions,
            'winning_positions': winning_positions,
            'losing_positions': losing_positions,
            'win_rate': round((winning_positions / total_positions) * 100, 2) if total_positions > 0 else 0,
            'largest_holding': max(holdings, key=lambda h: h.current_value).asset.symbol if holdings else None,
            'best_performer': max(holdings, key=lambda h: h.unrealized_pnl).asset.symbol if holdings else None,
            'worst_performer': min(holdings, key=lambda h: h.unrealized_pnl).asset.symbol if holdings else None,
        }


class PortfolioAllocationSerializer(serializers.Serializer):
    """
    Serializer untuk analisis alokasi portfolio.
    
    Menampilkan breakdown alokasi asset berdasarkan berbagai dimensi
    seperti asset type, sector, geographic, dll.
    """
    by_asset_type = serializers.DictField()
    by_sector = serializers.DictField()
    by_currency = serializers.DictField()
    top_holdings = serializers.ListField()
    diversification_score = serializers.FloatField()
    
    class Meta:
        fields = ['by_asset_type', 'by_sector', 'by_currency', 
                  'top_holdings', 'diversification_score']


class PortfolioPerformanceSerializer(serializers.Serializer):
    """
    Serializer untuk metrics performa portfolio.
    
    Menampilkan berbagai metrics seperti ROI, Sharpe ratio, volatility, dll.
    """
    total_return = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_return_percentage = serializers.FloatField()
    annualized_return = serializers.FloatField()
    volatility = serializers.FloatField()
    sharpe_ratio = serializers.FloatField()
    max_drawdown = serializers.FloatField()
    best_day = serializers.FloatField()
    worst_day = serializers.FloatField()
    
    class Meta:
        fields = ['total_return', 'total_return_percentage', 'annualized_return',
                  'volatility', 'sharpe_ratio', 'max_drawdown', 'best_day', 'worst_day']
