from rest_framework import serializers

class TransactionSummarySerializer(serializers.Serializer):
    """
    Serializer untuk ringkasan transaksi.
    
    Digunakan untuk menampilkan total pemasukan, pengeluaran, dan saldo
    dalam format yang konsisten.
    
    Attributes:
        income (decimal): Total pemasukan
        expense (decimal): Total pengeluaran
        balance (decimal): Selisih antara pemasukan dan pengeluaran
    """
    income = serializers.DecimalField(max_digits=15, decimal_places=2)
    expense = serializers.DecimalField(max_digits=15, decimal_places=2)
    balance = serializers.DecimalField(max_digits=15, decimal_places=2)


class MonthlyReportSerializer(TransactionSummarySerializer):
    """
    Serializer untuk data laporan bulanan.
    
    Digunakan untuk menampilkan ringkasan transaksi bulanan dengan
    total pemasukan, pengeluaran, dan saldo.
    
    Attributes:
        month (int): Bulan (1-12)
        year (int): Tahun
        income (decimal): Total pemasukan pada bulan tersebut
        expense (decimal): Total pengeluaran pada bulan tersebut
        balance (decimal): Selisih antara pemasukan dan pengeluaran (income - expense)
    """
    
    month = serializers.IntegerField()
    year = serializers.IntegerField()

class CategorySummarySerializer(serializers.Serializer):
    """
    Serializer untuk data ringkasan kategori.
    
    Digunakan untuk menampilkan jumlah dan persentase transaksi per kategori.
    
    Attributes:
        id (int): ID kategori
        name (str): Nama kategori
        icon (str): Ikon kategori
        color (str): Warna kategori
        amount (decimal): Total jumlah transaksi dalam kategori
        percentage (float): Persentase dari total transaksi
    """
    
    id = serializers.IntegerField(source='category__id')
    name = serializers.CharField(source='category__name')
    icon = serializers.CharField(source='category__icon', allow_null=True)
    color = serializers.CharField(source='category__color', allow_null=True)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    percentage = serializers.FloatField()