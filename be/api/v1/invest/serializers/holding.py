from rest_framework import serializers
from invest.models import InvestmentHolding
from .asset import AssetListSerializer
from .portfolio import InvestmentPortfolioListSerializer
from decimal import Decimal


class InvestmentHoldingListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer untuk model InvestmentHolding dalam format list.
    
    Digunakan untuk menampilkan daftar holdings dengan informasi minimal.
    """
    asset_symbol = serializers.CharField(source='asset.symbol', read_only=True)
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    portfolio_name = serializers.CharField(source='portfolio.name', read_only=True)
    unrealized_pnl_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = InvestmentHolding
        fields = ['id', 'portfolio_name', 'asset_symbol', 'asset_name', 
                  'quantity', 'average_price', 'current_price', 'current_value',
                  'unrealized_pnl', 'unrealized_pnl_percentage', 'last_updated']
    
    def get_unrealized_pnl_percentage(self, obj):
        """Menghitung persentase unrealized P&L"""
        if obj.total_cost > 0:
            return round((obj.unrealized_pnl / obj.total_cost) * 100, 2)
        return 0


class InvestmentHoldingDetailSerializer(serializers.ModelSerializer):
    """
    Detail serializer untuk model InvestmentHolding.
    
    Menampilkan informasi lengkap holding dengan analytics dan metrics.
    """
    asset = AssetListSerializer(read_only=True)
    portfolio = InvestmentPortfolioListSerializer(read_only=True)
    unrealized_pnl_percentage = serializers.SerializerMethodField()
    allocation_percentage = serializers.SerializerMethodField()
    performance_metrics = serializers.SerializerMethodField()
    risk_metrics = serializers.SerializerMethodField()
    
    class Meta:
        model = InvestmentHolding
        fields = ['id', 'portfolio', 'asset', 'quantity', 'average_price', 
                  'total_cost', 'current_price', 'current_value', 'unrealized_pnl',
                  'unrealized_pnl_percentage', 'allocation_percentage', 'last_updated',
                  'performance_metrics', 'risk_metrics']
    
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
    
    def get_performance_metrics(self, obj):
        """Menghitung metrics performa holding"""
        # Get all transactions for this holding
        transactions = obj.asset.investment_transactions.filter(
            portfolio=obj.portfolio,
            user=obj.user
        ).order_by('transaction_date')
        
        if not transactions.exists():
            return {}
        
        first_transaction = transactions.first()
        last_transaction = transactions.last()
        
        # Calculate holding period
        holding_period = (last_transaction.transaction_date - first_transaction.transaction_date).days
        
        # Calculate annualized return
        total_return = self.get_unrealized_pnl_percentage(obj)
        if holding_period > 0:
            annualized_return = ((1 + total_return/100) ** (365/holding_period) - 1) * 100
        else:
            annualized_return = total_return
        
        return {
            'holding_period_days': holding_period,
            'annualized_return': round(annualized_return, 2),
            'total_transactions': transactions.count(),
            'first_purchase_date': first_transaction.transaction_date,
            'average_purchase_price': obj.average_price,
            'current_vs_average_price': round(((obj.current_price - obj.average_price) / obj.average_price) * 100, 2) if obj.average_price > 0 else 0
        }
    
    def get_risk_metrics(self, obj):
        """Menghitung metrics risiko holding"""
        # Get recent price history for volatility calculation
        recent_prices = obj.asset.prices.order_by('-timestamp')[:30]
        
        if recent_prices.count() < 2:
            return {}
        
        # Calculate daily returns for volatility
        daily_returns = []
        prices = [float(p.price) for p in recent_prices]
        
        for i in range(1, len(prices)):
            daily_return = (prices[i] - prices[i-1]) / prices[i-1]
            daily_returns.append(daily_return)
        
        if daily_returns:
            # Calculate volatility (standard deviation of returns)
            avg_return = sum(daily_returns) / len(daily_returns)
            variance = sum((r - avg_return) ** 2 for r in daily_returns) / len(daily_returns)
            volatility = (variance ** 0.5) * (252 ** 0.5) * 100  # Annualized volatility
            
            # Calculate max drawdown
            peak = prices[0]
            max_drawdown = 0
            for price in prices:
                if price > peak:
                    peak = price
                drawdown = (peak - price) / peak
                max_drawdown = max(max_drawdown, drawdown)
            
            return {
                'volatility': round(volatility, 2),
                'max_drawdown': round(max_drawdown * 100, 2),
                'price_range_30d': {
                    'high': max(prices),
                    'low': min(prices),
                    'range_percentage': round(((max(prices) - min(prices)) / min(prices)) * 100, 2)
                }
            }
        
        return {}


class HoldingRefreshSerializer(serializers.Serializer):
    """
    Serializer untuk refresh holdings dengan current prices.
    
    Digunakan untuk update nilai holdings dengan harga terbaru.
    """
    holdings_updated = serializers.IntegerField()
    total_value_before = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_value_after = serializers.DecimalField(max_digits=15, decimal_places=2)
    value_change = serializers.DecimalField(max_digits=15, decimal_places=2)
    value_change_percentage = serializers.FloatField()
    last_refresh = serializers.DateTimeField()
    
    class Meta:
        fields = ['holdings_updated', 'total_value_before', 'total_value_after',
                  'value_change', 'value_change_percentage', 'last_refresh']


class InvestmentAnalyticsSerializer(serializers.Serializer):
    """
    Serializer untuk analytics investasi secara keseluruhan.
    
    Menampilkan overview analytics untuk semua investment user.
    """
    total_portfolios = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_cost = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_pnl = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_pnl_percentage = serializers.FloatField()
    top_performers = serializers.ListField()
    worst_performers = serializers.ListField()
    allocation_by_type = serializers.DictField()
    allocation_by_sector = serializers.DictField()
    monthly_performance = serializers.ListField()
    
    class Meta:
        fields = ['total_portfolios', 'total_value', 'total_cost', 'total_pnl',
                  'total_pnl_percentage', 'top_performers', 'worst_performers',
                  'allocation_by_type', 'allocation_by_sector', 'monthly_performance']


class DiversificationAnalysisSerializer(serializers.Serializer):
    """
    Serializer untuk analisis diversifikasi portfolio.
    
    Menampilkan metrics diversifikasi dan rekomendasi rebalancing.
    """
    diversification_score = serializers.FloatField()
    concentration_risk = serializers.FloatField()
    sector_diversification = serializers.DictField()
    geographic_diversification = serializers.DictField()
    asset_type_diversification = serializers.DictField()
    correlation_matrix = serializers.DictField()
    rebalancing_recommendations = serializers.ListField()
    
    class Meta:
        fields = ['diversification_score', 'concentration_risk', 'sector_diversification',
                  'geographic_diversification', 'asset_type_diversification', 
                  'correlation_matrix', 'rebalancing_recommendations']


class PerformanceAnalysisSerializer(serializers.Serializer):
    """
    Serializer untuk analisis performa investasi mendalam.
    
    Menampilkan berbagai metrics performa seperti Sharpe ratio, alpha, beta, dll.
    """
    total_return = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_return_percentage = serializers.FloatField()
    annualized_return = serializers.FloatField()
    volatility = serializers.FloatField()
    sharpe_ratio = serializers.FloatField()
    sortino_ratio = serializers.FloatField()
    max_drawdown = serializers.FloatField()
    calmar_ratio = serializers.FloatField()
    alpha = serializers.FloatField()
    beta = serializers.FloatField()
    win_rate = serializers.FloatField()
    profit_factor = serializers.FloatField()
    
    class Meta:
        fields = ['total_return', 'total_return_percentage', 'annualized_return',
                  'volatility', 'sharpe_ratio', 'sortino_ratio', 'max_drawdown',
                  'calmar_ratio', 'alpha', 'beta', 'win_rate', 'profit_factor']
