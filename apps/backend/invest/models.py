# ========================================
# invest/models.py - Investment Tracker
# ========================================

import uuid
from django.db import models
from django.utils import timezone
from master.models import User



class Asset(models.Model):
    TYPE_CHOICES = [
        ('stock', 'Stock'),
        ('crypto', 'Cryptocurrency'),
        ('bond', 'Bond'),
        ('reit', 'REIT'),
        ('mutual_fund', 'Mutual Fund'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    symbol = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    exchange = models.CharField(max_length=50, blank=True)
    sector = models.CharField(max_length=100, blank=True)
    currency = models.CharField(max_length=3, default='IDR')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'assets'

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class InvestmentPortfolio(models.Model):
    RISK_LEVEL_CHOICES = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investment_portfolios')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    initial_capital = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    target_allocation = models.JSONField(blank=True, null=True)  # {"stocks": 70, "bonds": 20, "crypto": 10}
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'investment_portfolios'

    def __str__(self):
        return f"{self.user.full_name} - {self.name}"


class InvestmentTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('dividend', 'Dividend'),
        ('split', 'Stock Split'),
        ('bonus', 'Bonus Shares'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investment_transactions')
    portfolio = models.ForeignKey(InvestmentPortfolio, on_delete=models.CASCADE, related_name='transactions')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='investment_transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    fees = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    transaction_date = models.DateField()
    broker = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'investment_transactions'
        indexes = [
            models.Index(fields=['user', 'transaction_date']),
            models.Index(fields=['portfolio', 'transaction_date']),
            models.Index(fields=['asset', 'transaction_date']),
        ]

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} {self.asset.symbol}"


class InvestmentHolding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investment_holdings')
    portfolio = models.ForeignKey(InvestmentPortfolio, on_delete=models.CASCADE, related_name='holdings')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='holdings')
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    average_price = models.DecimalField(max_digits=15, decimal_places=2)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2)
    current_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    unrealized_pnl = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'investment_holdings'
        unique_together = ['user', 'portfolio', 'asset']

    def __str__(self):
        return f"{self.asset.symbol} - {self.quantity}"


class AssetPrice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=15, decimal_places=2)
    volume = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    timestamp = models.DateTimeField()
    source = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'asset_prices'
        indexes = [
            models.Index(fields=['asset', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.asset.symbol} - {self.price} at {self.timestamp}"
