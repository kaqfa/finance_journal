from rest_framework import serializers
from finance.models import Tag, Transaction, TransactionTag

class TagSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Tag.
    
    Tag digunakan untuk memberikan label tambahan pada transaksi dan membantu 
    pengelompokan transaksi berdasarkan tujuan atau konteks tertentu.
    
    Attributes:
        name (str): Nama tag
        created_at (datetime): Waktu pembuatan (read-only)
    """
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['created_at', 'user']

    def create(self, validated_data):
        # Mengambil user dari request
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class TransactionTagSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model TransactionTag (relasi Transaksi-Tag).
    
    Merepresentasikan relasi many-to-many antara Transaction dan Tag.
    
    Attributes:
        tag (int): ID tag
        tag_name (str): Nama tag (read-only)
    """
    tag_name = serializers.CharField(source='tag.name', read_only=True)
    
    class Meta:
        model = TransactionTag
        fields = ['id', 'tag', 'tag_name']