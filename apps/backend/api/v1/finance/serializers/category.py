from rest_framework import serializers
from finance.models import Category

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Category (Kategori Transaksi).
    
    Kategori digunakan untuk mengklasifikasikan transaksi keuangan menjadi
    kategori pemasukan (income) dan pengeluaran (expense).
    
    Attributes:
        name (str): Nama kategori
        type (str): Tipe kategori ('income' atau 'expense')
        icon (str): Emoji atau ikon untuk kategori (opsional)
        color (str): Kode warna hex untuk kategori (opsional)
        created_at (datetime): Waktu pembuatan (read-only)
        updated_at (datetime): Waktu update terakhir (read-only)
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'icon', 'color', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'user']

    def create(self, validated_data):
        # Mengambil user dari request
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)