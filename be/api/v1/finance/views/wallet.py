from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from finance.models import Wallet
from ..serializers import WalletSerializer, WalletListSerializer


class WalletViewSet(viewsets.ModelViewSet):
    """
    manajemen wallet (dompet/rekening).
    
    Wallet merepresentasikan tempat penyimpanan uang seperti rekening bank,
    e-wallet, uang tunai, kartu kredit, dll. Saldo wallet diupdate otomatis
    berdasarkan transaksi yang terjadi.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'current_balance', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        """
        Menggunakan serializer yang berbeda untuk list dan detail view.
        """
        if self.action == 'list':
            return WalletListSerializer
        return WalletSerializer

    def get_queryset(self):
        """
        Filter queryset untuk hanya menampilkan wallet milik user saat ini
        dengan opsi filter tambahan berdasarkan query parameter.
        """
        queryset = Wallet.objects.filter(user=self.request.user)
        
        # Filter by is_active if specified
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        # Filter by wallet_type if specified
        wallet_type = self.request.query_params.get('wallet_type')
        if wallet_type:
            queryset = queryset.filter(wallet_type=wallet_type)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def recalculate(self, request, pk=None):
        """
        Menghitung ulang saldo wallet berdasarkan transaksi yang ada.
        
        Endpoint ini berguna jika saldo wallet perlu disesuaikan kembali
        dengan transaksi yang ada di database.
        
        Returns:
            Wallet dengan saldo yang sudah diupdate
        """
        wallet = self.get_object()
        wallet.update_balance()
        serializer = self.get_serializer(wallet)
        return Response(serializer.data)