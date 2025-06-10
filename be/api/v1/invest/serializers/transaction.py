from rest_framework import serializers
from invest.models import InvestmentTransaction, InvestmentPortfolio, Asset
from .asset import AssetListSerializer
from .portfolio import InvestmentPortfolioListSerializer
from decimal import Decimal


class InvestmentTransactionListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer untuk model InvestmentTransaction dalam format list.
    
    Digunakan untuk menampilkan daftar transaksi dengan informasi minimal
    yang diperlukan untuk list view.
    """
    portfolio_name = serializers.CharField(source='portfolio.name', read_only=True)
    asset_symbol = serializers.CharField(source='asset.symbol', read_only=True)
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    
    class Meta:
        model = InvestmentTransaction
        fields = ['id', 'transaction_type', 'portfolio_name', 'asset_symbol', 
                  'asset_name', 'quantity', 'price', 'total_amount', 
                  'transaction_date', 'created_at']


class InvestmentTransactionSerializer(serializers.ModelSerializer):
    """
    Full serializer untuk model InvestmentTransaction.
    
    Transaction merepresentasikan aktivitas jual/beli asset dalam portfolio
    investasi seperti buy, sell, dividend, stock split, bonus shares.
    
    Attributes:
        portfolio (uuid): ID portfolio tujuan transaksi
        asset (uuid): ID asset yang ditransaksikan
        transaction_type (str): Tipe transaksi ('buy', 'sell', 'dividend', 'split', 'bonus')
        quantity (decimal): Jumlah unit asset
        price (decimal): Harga per unit
        total_amount (decimal): Total nilai transaksi (otomatis dihitung)
        fees (decimal): Biaya transaksi (broker fee, tax, dll)
        transaction_date (date): Tanggal transaksi
        broker (str): Nama broker/platform trading
        notes (str): Catatan tambahan
        created_at (datetime): Waktu pembuatan (read-only)
    """
    portfolio_name = serializers.CharField(source='portfolio.name', read_only=True)
    asset = AssetListSerializer(read_only=True)
    asset_id = serializers.UUIDField(write_only=True)
    portfolio_id = serializers.UUIDField(write_only=True)
    net_amount = serializers.SerializerMethodField()
    impact_to_portfolio = serializers.SerializerMethodField()
    
    class Meta:
        model = InvestmentTransaction
        fields = ['id', 'portfolio_id', 'portfolio_name', 'asset', 'asset_id', 
                  'transaction_type', 'quantity', 'price', 'total_amount', 'fees',
                  'net_amount', 'transaction_date', 'broker', 'notes', 'created_at',
                  'impact_to_portfolio']
        read_only_fields = ['created_at', 'user', 'total_amount']
    
    def validate(self, data):
        """Validasi data transaksi"""
        user = self.context['request'].user
        
        # Validasi portfolio ownership
        try:
            portfolio = InvestmentPortfolio.objects.get(
                id=data['portfolio_id'], 
                user=user
            )
            data['portfolio'] = portfolio
        except InvestmentPortfolio.DoesNotExist:
            raise serializers.ValidationError("Portfolio not found or you don't have access")
        
        # Validasi asset exists
        try:
            asset = Asset.objects.get(id=data['asset_id'])
            data['asset'] = asset
        except Asset.DoesNotExist:
            raise serializers.ValidationError("Asset not found")
        
        # Validasi quantity untuk sell transaction
        if data['transaction_type'] == 'sell':
            current_holding = portfolio.holdings.filter(asset=asset).first()
            if not current_holding or current_holding.quantity < data['quantity']:
                raise serializers.ValidationError(
                    f"Insufficient {asset.symbol} balance. Available: {current_holding.quantity if current_holding else 0}"
                )
        
        # Auto-calculate total_amount
        data['total_amount'] = data['quantity'] * data['price']
        
        return data
    
    def create(self, validated_data):
        """Override create untuk mengset user dan update holdings"""
        user = self.context['request'].user
        validated_data['user'] = user
        
        # Remove portfolio_id dan asset_id dari validated_data
        portfolio = validated_data.pop('portfolio')
        asset = validated_data.pop('asset')
        validated_data.pop('portfolio_id', None)
        validated_data.pop('asset_id', None)
        
        validated_data['portfolio'] = portfolio
        validated_data['asset'] = asset
        
        transaction = super().create(validated_data)
        
        # Update holdings setelah transaksi dibuat
        self._update_holdings(transaction)
        
        return transaction
    
    def _update_holdings(self, transaction):
        """Update holdings berdasarkan transaksi"""
        from invest.models import InvestmentHolding
        
        holding, created = InvestmentHolding.objects.get_or_create(
            user=transaction.user,
            portfolio=transaction.portfolio,
            asset=transaction.asset,
            defaults={
                'quantity': 0,
                'average_price': 0,
                'total_cost': 0,
            }
        )
        
        if transaction.transaction_type == 'buy':
            # Calculate new average price
            old_total_cost = holding.quantity * holding.average_price
            new_total_cost = old_total_cost + transaction.total_amount + transaction.fees
            new_quantity = holding.quantity + transaction.quantity
            
            holding.quantity = new_quantity
            holding.average_price = new_total_cost / new_quantity if new_quantity > 0 else 0
            holding.total_cost = new_total_cost
            
        elif transaction.transaction_type == 'sell':
            # Reduce quantity
            holding.quantity -= transaction.quantity
            holding.total_cost = holding.quantity * holding.average_price
            
            # Delete holding if quantity becomes 0
            if holding.quantity <= 0:
                holding.delete()
                return
        
        elif transaction.transaction_type == 'dividend':
            # Dividend doesn't affect quantity atau average price
            pass
        
        elif transaction.transaction_type in ['split', 'bonus']:
            # Stock split atau bonus shares increases quantity
            split_ratio = transaction.quantity  # Menggunakan quantity sebagai ratio
            holding.quantity *= split_ratio
            holding.average_price /= split_ratio  # Average price adjusted
        
        holding.save()
    
    def get_net_amount(self, obj):
        """Menghitung net amount setelah fees"""
        if obj.transaction_type == 'buy':
            return obj.total_amount + obj.fees
        elif obj.transaction_type == 'sell':
            return obj.total_amount - obj.fees
        return obj.total_amount
    
    def get_impact_to_portfolio(self, obj):
        """Menghitung dampak transaksi terhadap portfolio"""
        net_amount = self.get_net_amount(obj)
        portfolio_value = sum(h.current_value for h in obj.portfolio.holdings.all())
        
        if portfolio_value > 0:
            impact_percentage = (net_amount / portfolio_value) * 100
            return {
                'net_amount': net_amount,
                'impact_percentage': round(impact_percentage, 2),
                'transaction_type': obj.transaction_type
            }
        return None


class TransactionSummarySerializer(serializers.Serializer):
    """
    Serializer untuk ringkasan transaksi investasi.
    
    Menampilkan summary statistik transaksi dalam periode tertentu.
    """
    total_transactions = serializers.IntegerField()
    total_buy_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_sell_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_dividend = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_fees = serializers.DecimalField(max_digits=15, decimal_places=2)
    net_investment = serializers.DecimalField(max_digits=15, decimal_places=2)
    most_traded_asset = serializers.CharField()
    transaction_frequency = serializers.DictField()
    
    class Meta:
        fields = ['total_transactions', 'total_buy_amount', 'total_sell_amount',
                  'total_dividend', 'total_fees', 'net_investment', 'most_traded_asset',
                  'transaction_frequency']


class TransactionsByAssetSerializer(serializers.Serializer):
    """
    Serializer untuk transaksi yang dikelompokkan berdasarkan asset.
    
    Menampilkan total transaksi, volume, dan P&L per asset.
    """
    asset = AssetListSerializer()
    transaction_count = serializers.IntegerField()
    total_quantity_bought = serializers.DecimalField(max_digits=18, decimal_places=8)
    total_quantity_sold = serializers.DecimalField(max_digits=18, decimal_places=8)
    total_buy_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_sell_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    realized_pnl = serializers.DecimalField(max_digits=15, decimal_places=2)
    current_holding = serializers.DecimalField(max_digits=18, decimal_places=8)
    
    class Meta:
        fields = ['asset', 'transaction_count', 'total_quantity_bought', 
                  'total_quantity_sold', 'total_buy_amount', 'total_sell_amount',
                  'realized_pnl', 'current_holding']
