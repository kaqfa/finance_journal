from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response

from finance.models import Transfer
from ..serializers import TransferSerializer, TransferCreateSerializer


class TransferViewSet(viewsets.ModelViewSet):
    """
    manajemen transfer antar wallet.
    
    Transfer merepresentasikan perpindahan uang dari satu wallet ke wallet lain.
    Saat dibuat, transfer otomatis membuat transaksi tipe 'transfer' di wallet sumber
    dan mengupdate saldo kedua wallet (sumber dan tujuan).
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Menggunakan serializer yang berbeda untuk create/update dan retrieve/list.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return TransferCreateSerializer
        return TransferSerializer

    def get_queryset(self):
        """
        Filter queryset untuk hanya menampilkan transfer antara wallet milik user saat ini.
        """
        user = self.request.user
        return Transfer.objects.filter(from_wallet__user=user)
    
    def create(self, request, *args, **kwargs):
        """
        Membuat transfer baru antara wallet.
        
        Melakukan validasi bahwa kedua wallet (sumber dan tujuan) dimiliki oleh
        user yang sama. Juga membuat transaksi tipe 'transfer' secara otomatis
        yang akan terlihat di riwayat transaksi wallet sumber.
        
        Request Body:
            from_wallet (int): ID wallet sumber
            to_wallet (int): ID wallet tujuan
            amount (decimal): Jumlah transfer
            fee (decimal): Biaya transfer (opsional)
            description (str): Deskripsi transfer (opsional)
            
        Returns:
            Transfer yang berhasil dibuat
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        from_wallet = serializer.validated_data['from_wallet']
        to_wallet = serializer.validated_data['to_wallet']
        
        # Check if user owns both wallets
        if from_wallet.user != user or to_wallet.user != user:
            return Response(
                {"detail": "You can only transfer between your own wallets."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create the transfer object
        transfer = serializer.save()
        
        # Use TransferSerializer for response
        response_serializer = TransferSerializer(transfer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)