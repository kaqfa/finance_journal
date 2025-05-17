from rest_framework import serializers
from finance.models import Transfer

class TransferSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Transfer (Transfer antar Wallet).
    
    Transfer merepresentasikan perpindahan dana dari satu wallet ke wallet lain.
    
    Attributes:
        from_wallet (int): ID wallet sumber
        from_wallet_name (str): Nama wallet sumber (read-only)
        to_wallet (int): ID wallet tujuan
        to_wallet_name (str): Nama wallet tujuan (read-only)
        amount (decimal): Jumlah transfer
        fee (decimal): Biaya transfer (opsional)
        transaction (int): ID transaksi terkait (read-only, dibuat otomatis)
        transaction_date (date): Tanggal transaksi (read-only, dari transaksi terkait)
        created_at (datetime): Waktu pembuatan (read-only)
        updated_at (datetime): Waktu update terakhir (read-only)
    """
    from_wallet_name = serializers.CharField(source='from_wallet.name', read_only=True)
    to_wallet_name = serializers.CharField(source='to_wallet.name', read_only=True)
    transaction_date = serializers.DateField(source='transaction.transaction_date', read_only=True)
    
    class Meta:
        model = Transfer
        fields = ['id', 'from_wallet', 'from_wallet_name', 'to_wallet', 
                  'to_wallet_name', 'amount', 'fee', 'transaction', 
                  'transaction_date', 'created_at', 'updated_at']
        read_only_fields = ['transaction', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Transfer akan membuat transaction secara otomatis
        return super().create(validated_data)


class TransferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer untuk pembuatan Transfer baru dengan opsi deskripsi.
    
    Attributes:
        from_wallet (int): ID wallet sumber
        to_wallet (int): ID wallet tujuan
        amount (decimal): Jumlah transfer
        fee (decimal): Biaya transfer (opsional)
        description (str): Deskripsi transfer (opsional)
    """
    description = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Transfer
        fields = ['from_wallet', 'to_wallet', 'amount', 'fee', 'description']

    def create(self, validated_data):
        description = validated_data.pop('description', f"Transfer to {validated_data['to_wallet'].name}")
        
        # Create transfer record which will automatically create the transaction
        transfer = Transfer.objects.create(
            from_wallet=validated_data['from_wallet'],
            to_wallet=validated_data['to_wallet'],
            amount=validated_data['amount'],
            fee=validated_data.get('fee', 0)
        )
        
        # Update the transaction description if provided
        if description:
            transfer.transaction.description = description
            transfer.transaction.save()
            
        return transfer