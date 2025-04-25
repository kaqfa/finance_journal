from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('income', 'Pemasukan'),
        ('expense', 'Pengeluaran'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES)
    icon = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'name']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Wallet(models.Model):
    WALLET_TYPE_CHOICES = [
        ('cash', 'Cash'),
        ('bank', 'Bank Account'),
        ('ewallet', 'E-Wallet'),
        ('credit', 'Credit Card'),
        ('other', 'Lainnya'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    name = models.CharField(max_length=100)
    wallet_type = models.CharField(max_length=10, choices=WALLET_TYPE_CHOICES, default='bank')
    currency = models.CharField(max_length=5, default='IDR')
    initial_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_wallet_type_display()})"
    
    def update_balance(self):
        """Update current_balance based on all transactions"""
        from decimal import Decimal
        
        # Get initial balance
        balance = self.initial_balance
        
        # Add all income transactions
        income = self.transactions.filter(type='income').aggregate(
            total=models.Sum('amount'))['total'] or Decimal('0')
        balance += income
        
        # Subtract all expense transactions
        expenses = self.transactions.filter(type='expense').aggregate(
            total=models.Sum('amount'))['total'] or Decimal('0')
        balance -= expenses
        
        # Handle transfers
        incoming = Transfer.objects.filter(to_wallet=self).aggregate(
            total=models.Sum('amount'))['total'] or Decimal('0')
        outgoing = Transfer.objects.filter(from_wallet=self).aggregate(
            total=models.Sum('amount'))['total'] or Decimal('0')
        outgoing_fees = Transfer.objects.filter(from_wallet=self).aggregate(
            total=models.Sum('fee'))['total'] or Decimal('0')
        
        balance += incoming - outgoing - outgoing_fees
        
        # Update current balance
        self.current_balance = balance
        self.save(update_fields=['current_balance', 'updated_at'])


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    transaction_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.amount} ({self.wallet.name})"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Update wallet balance after saving
        self.wallet.update_balance()
        
        # If this is a transfer transaction, make sure the transfer record exists
        if is_new and self.type == 'transfer':
            # Check if this transaction is already linked to a transfer
            if not hasattr(self, 'transfer'):
                # The related Transfer object will be created in the Transfer's save method
                pass


class Transfer(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='transfer')
    from_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='outgoing_transfers')
    to_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='incoming_transfers')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    fee = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Transfer: {self.amount} from {self.from_wallet.name} to {self.to_wallet.name}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        # If this is a new transfer, create the main transaction if it doesn't exist
        if is_new and not hasattr(self, 'transaction'):
            self.transaction = Transaction.objects.create(
                user=self.from_wallet.user,
                wallet=self.from_wallet,
                amount=self.amount + self.fee,
                type='transfer',
                description=f"Transfer to {self.to_wallet.name}",
                transaction_date=timezone.now().date()
            )
        
        super().save(*args, **kwargs)
        
        # Update balances for both wallets
        self.from_wallet.update_balance()
        self.to_wallet.update_balance()


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'name']
    
    def __str__(self):
        return self.name


class TransactionTag(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='transaction_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='transaction_tags')
    
    class Meta:
        unique_together = ['transaction', 'tag']
    
    def __str__(self):
        return f"{self.transaction} - {self.tag}"