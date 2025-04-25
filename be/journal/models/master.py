from django.db import models

class Sekuritas(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Sector(models.Model):
    STOCK = 'stock'
    BONDS = 'bonds'
    CRYPTO = 'crypto'
    OTHER = 'other'
    TYPE_CHOICES = [
        (STOCK, 'Stock'),
        (BONDS, 'Bonds'),
        (CRYPTO, 'Crypto'),
        (OTHER, 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=STOCK)

    def __str__(self):
        return self.name
    

class Asset(models.Model):
    STOCK = 'stock'
    CRYPTO = 'crypto'
    BONDS = 'bonds'
    ASSET_TYPE_CHOICES = [
        (STOCK, 'Stock'),
        (CRYPTO, 'Crypto'),
        (BONDS, 'Bonds'),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    endpoint_url = models.URLField(null=True, blank=True)
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPE_CHOICES, default=STOCK)
    sector = models.ForeignKey(Sector, on_delete=models.RESTRICT)
    description = models.TextField(null=True, blank=True)
    last_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_update = models.DateTimeField(auto_now=True)
    price_check = models.BooleanField(default=False)
    dividend_check = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    
class Dividend(models.Model):
    INTERIM = 'interim'
    FINAL = 'final'
    TYPE_CHOICES = [
        (INTERIM, 'Interim'),
        (FINAL, 'Final'),
    ]

    PREDICT = 'predict'
    SCHEDULED = 'scheduled'
    FIX = 'fix'
    STATUS_CHOICES = [
        (PREDICT, 'Predict'),
        (SCHEDULED, 'Scheduled'),
        (FIX, 'Fix'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=FINAL)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PREDICT)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.amount}"
