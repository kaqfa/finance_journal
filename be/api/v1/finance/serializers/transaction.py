from rest_framework import serializers
from finance.models import Transaction, Tag, TransactionTag  # tambahkan TransactionTag di sini
from .tag import TransactionTagSerializer

class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Transaction (Transaksi Keuangan).
    
    Transaksi merepresentasikan pergerakan uang, bisa berupa pemasukan (income),
    pengeluaran (expense), atau transfer antar wallet.
    
    Attributes:
        wallet (int): ID wallet terkait
        wallet_name (str): Nama wallet (read-only)
        category (int): ID kategori transaksi
        category_name (str): Nama kategori (read-only)
        amount (decimal): Jumlah transaksi
        type (str): Tipe transaksi ('income', 'expense', 'transfer')
        description (str): Deskripsi transaksi (opsional)
        transaction_date (date): Tanggal transaksi
        created_at (datetime): Waktu pembuatan (read-only)
        updated_at (datetime): Waktu update terakhir (read-only)
        tags (list): Daftar tag terkait (read-only)
        tag_ids (list): Daftar ID tag untuk ditambahkan (write-only)
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    wallet_name = serializers.CharField(source='wallet.name', read_only=True)
    tags = TransactionTagSerializer(source='transaction_tags', many=True, read_only=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'wallet_name', 'category', 'category_name', 
                  'amount', 'type', 'description', 'transaction_date', 
                  'created_at', 'updated_at', 'tags', 'tag_ids']
        read_only_fields = ['created_at', 'updated_at', 'user']

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        user = self.context['request'].user
        validated_data['user'] = user
        
        transaction = super().create(validated_data)
        
        # Add tags
        for tag_id in tag_ids:
            try:
                tag = Tag.objects.get(id=tag_id, user=user)
                TransactionTag.objects.create(transaction=transaction, tag=tag)
            except Tag.DoesNotExist:
                pass
                
        return transaction
    
    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)
        transaction = super().update(instance, validated_data)
        
        # Update tags only if provided
        if tag_ids is not None:
            user = self.context['request'].user
            
            # Clear existing tags
            TransactionTag.objects.filter(transaction=transaction).delete()
            
            # Add new tags
            for tag_id in tag_ids:
                try:
                    tag = Tag.objects.get(id=tag_id, user=user)
                    TransactionTag.objects.create(transaction=transaction, tag=tag)
                except Tag.DoesNotExist:
                    pass
                    
        return transaction


class TransactionListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer untuk model Transaction dalam format list.
    
    Digunakan untuk menampilkan daftar transaksi dengan informasi minimal
    yang diperlukan untuk list view.
    """
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    wallet_name = serializers.CharField(source='wallet.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'wallet_name', 'category_name', 'amount', 
                  'type', 'transaction_date', 'description']