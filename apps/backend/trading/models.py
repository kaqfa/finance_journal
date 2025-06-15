# ========================================
# trading/models.py - Trading Journal
# ========================================

from master.models import User
from invest.models import Asset

import uuid
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class TradingAccount(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('stock', 'Stock Trading'),
        ('crypto', 'Cryptocurrency'),
        ('forex', 'Forex'),
        ('futures', 'Futures'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_accounts')
    account_name = models.CharField(max_length=255)
    broker = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    initial_balance = models.DecimalField(max_digits=15, decimal_places=2)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2)
    available_margin = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    max_daily_loss = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    max_position_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # percentage
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'trading_accounts'
    def __str__(self):
        return f"{self.user.full_name} - {self.account_name}"


class TradingStrategy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_strategies')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    rules = models.TextField(blank=True)
    risk_reward_ratio = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    win_rate_target = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    timeframe = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'trading_strategies'

    def __str__(self):
        return self.name


class Trade(models.Model):
    SIDE_CHOICES = [
        ('long', 'Long'),
        ('short', 'Short'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ]
    
    MARKET_CONDITION_CHOICES = [
        ('trending', 'Trending'),
        ('ranging', 'Ranging'),
        ('volatile', 'Volatile'),
        ('news_driven', 'News Driven'),
    ]
    
    EMOTIONAL_STATE_CHOICES = [
        ('confident', 'Confident'),
        ('fearful', 'Fearful'),
        ('greedy', 'Greedy'),
        ('neutral', 'Neutral'),
        ('fomo', 'FOMO'),
        ('revenge', 'Revenge Trading'),
    ]
    
    QUALITY_CHOICES = [
        ('A', 'Excellent'),
        ('B', 'Good'),
        ('C', 'Average'),
        ('D', 'Poor'),
    ]
    
    EXECUTION_QUALITY_CHOICES = [
        ('perfect', 'Perfect'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades')
    trading_account = models.ForeignKey(TradingAccount, on_delete=models.CASCADE, related_name='trades')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='trades')
    strategy = models.ForeignKey(TradingStrategy, on_delete=models.CASCADE, related_name='trades', blank=True, null=True)
    
    # Trade Planning
    planned_entry = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    planned_target = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    planned_stop_loss = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    planned_quantity = models.DecimalField(max_digits=18, decimal_places=8, blank=True, null=True)
    planned_risk_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    
    # Trade Execution
    side = models.CharField(max_length=10, choices=SIDE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    total_quantity = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    average_entry_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    average_exit_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_fees = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Trade Results
    realized_pnl = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pnl_percentage = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    holding_time = models.DurationField(blank=True, null=True)
    
    # Analysis & Notes
    market_condition = models.CharField(max_length=20, choices=MARKET_CONDITION_CHOICES, blank=True)
    emotional_state = models.CharField(max_length=20, choices=EMOTIONAL_STATE_CHOICES, blank=True)
    setup_quality = models.CharField(max_length=1, choices=QUALITY_CHOICES, blank=True)
    execution_quality = models.CharField(max_length=10, choices=EXECUTION_QUALITY_CHOICES, blank=True)
    notes = models.TextField(blank=True)
    screenshot_urls = models.TextField(blank=True, default='[]') 
    
    # Timestamps
    planned_at = models.DateTimeField(blank=True, null=True)
    entered_at = models.DateTimeField(blank=True, null=True)
    exited_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'trades'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'entered_at']),
            models.Index(fields=['trading_account', 'status']),
            models.Index(fields=['strategy', 'status']),
        ]

    def __str__(self):
        return f"{self.side} {self.asset.symbol} - {self.status}"


class TradeExecution(models.Model):
    EXECUTION_TYPE_CHOICES = [
        ('entry', 'Entry'),
        ('exit', 'Exit'),
        ('partial_exit', 'Partial Exit'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='executions')
    execution_type = models.CharField(max_length=15, choices=EXECUTION_TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    fees = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    executed_at = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'trade_executions'

    def __str__(self):
        return f"{self.execution_type} - {self.quantity} @ {self.price}"


class TradingPerformance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_performances')
    trading_account = models.ForeignKey(TradingAccount, on_delete=models.CASCADE, related_name='performances')
    date = models.DateField()
    
    # Daily metrics
    starting_balance = models.DecimalField(max_digits=15, decimal_places=2)
    ending_balance = models.DecimalField(max_digits=15, decimal_places=2)
    daily_pnl = models.DecimalField(max_digits=15, decimal_places=2)
    daily_pnl_percentage = models.DecimalField(max_digits=8, decimal_places=4)
    
    # Trade statistics
    total_trades = models.IntegerField(default=0)
    winning_trades = models.IntegerField(default=0)
    losing_trades = models.IntegerField(default=0)
    win_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Risk metrics
    max_drawdown = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    max_risk_per_trade = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'trading_performance'
        unique_together = ['user', 'trading_account', 'date']
        indexes = [
            models.Index(fields=['user', 'trading_account', 'date']),
        ]

    def __str__(self):
        return f"{self.trading_account.account_name} - {self.date}"
