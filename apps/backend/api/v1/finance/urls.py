from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    WalletViewSet,
    TransactionViewSet,
    TransferViewSet,
    TagViewSet
)

"""
Finance API Endpoints

Dokumentasi ini menjelaskan endpoint-endpoint API untuk modul finance (manajemen keuangan)
dari aplikasi Journal Invest.

Endpoint yang tersedia:

- /categories/ - Manajemen kategori pemasukan dan pengeluaran
- /wallets/ - Manajemen dompet/rekening/wallet
- /transactions/ - Manajemen transaksi keuangan (pemasukan/pengeluaran)
- /transfers/ - Manajemen transfer antar wallet
- /tags/ - Manajemen tag untuk transaksi

Semua endpoint mendukung operasi CRUD standar (Create, Read, Update, Delete).
Beberapa endpoint juga memiliki actions tambahan, seperti:
- /categories/income/ - Mendapatkan kategori pemasukan saja
- /categories/expense/ - Mendapatkan kategori pengeluaran saja
- /wallets/{id}/recalculate/ - Menghitung ulang saldo wallet
- /transactions/summary/ - Mendapatkan ringkasan transaksi
- /transactions/by-category/ - Mendapatkan transaksi dikelompokkan per kategori
- /transactions/monthly-report/ - Mendapatkan laporan bulanan
- /tags/{id}/transactions/ - Mendapatkan transaksi dengan tag tertentu
"""

# Membuat router untuk API
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'wallets', WalletViewSet, basename='wallet')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'transfers', TransferViewSet, basename='transfer')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
]