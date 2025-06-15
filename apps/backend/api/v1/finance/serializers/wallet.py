from rest_framework import serializers
from finance.models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Wallet (Dompet/Rekening Keuangan).
    
    Wallet merepresentasikan wadah/tempat penyimpanan uang seperti rekening bank,
    e-wallet, cash, kartu kredit, dll.
    
    Attributes:
        name (str): Nama wallet
        wallet_type (str): Tipe wallet ('cash', 'bank', 'ewallet', 'credit', 'other')
        currency (str): Mata uang wallet (default: 'IDR')
        initial_balance (decimal): Saldo awal wallet
        current_balance (decimal): Saldo terkini wallet (read-only, diupdate otomatis)
        is_active (bool): Status aktif wallet
        created_at (datetime): Waktu pembuatan (read-only)
        updated_at (datetime): Waktu update terakhir (read-only)
    """
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'wallet_type', 'currency', 'initial_balance', 
                  'current_balance', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'current_balance', 'user']

    def create(self, validated_data):
        # Mengambil user dari request
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class WalletListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer untuk model Wallet dalam format list.
    
    Digunakan untuk menampilkan daftar wallet dengan informasi minimal
    yang diperlukan untuk list view.
    """
    
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'wallet_type', 'currency', 'current_balance', 'is_active']