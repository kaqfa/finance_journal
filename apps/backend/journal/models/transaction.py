from django.db import models
from django.utils.timezone import now  # Import timezone.now
from journal.models.master import Asset, Sekuritas

class Account(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    sekuritas = models.ForeignKey(Sekuritas, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Account {self.id} - User {self.user}"


class Portfolio(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class TopupWithdraw(models.Model):
    TOPUP = 'topup'
    WITHDRAW = 'withdraw'
    TYPE_CHOICES = [
        (TOPUP, 'Topup'),
        (WITHDRAW, 'Withdraw'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.IntegerField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TOPUP)
    trans_date = models.DateTimeField(default=now)  # Use timezone.now

    def __str__(self):
        return f"{self.type.capitalize()} - {self.amount}"


class Investment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    avg_price = models.IntegerField(default=0)
    goal_desc = models.TextField(null=True, blank=True)
    strategy = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Investment in {self.asset.name}"


class Trading(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    tp_plan = models.IntegerField(default=0)
    cl_plan = models.IntegerField(default=0)
    realized_pl = models.IntegerField(default=0)
    reasons = models.CharField(max_length=255, null=True, blank=True)
    strategy = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Trading {self.asset.name}"


class Transaction(models.Model):
    BUY = 'buy'
    SELL = 'sell'
    DEVIDEN = 'deviden'
    TRANSACTION_TYPE_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
        (DEVIDEN, 'Deviden'),
    ]

    trading = models.ForeignKey(Trading, null=True, blank=True, on_delete=models.CASCADE)
    investment = models.ForeignKey(Investment, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    transaction_date = models.DateTimeField(default=now)  # Use timezone.now
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.quantity}"