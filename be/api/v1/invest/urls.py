from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssetViewSet,
    InvestmentPortfolioViewSet,
    InvestmentTransactionViewSet,
    InvestmentHoldingViewSet
)

"""
Investment API Endpoints

Dokumentasi ini menjelaskan endpoint-endpoint API untuk modul investment (portfolio tracking)
dari aplikasi Journal Invest.

Endpoint yang tersedia:

- /assets/ - Master data asset investasi (stocks, crypto, bonds, REITs, mutual funds)
- /portfolios/ - Manajemen portfolio investasi dengan target allocation
- /transactions/ - Manajemen transaksi investasi (buy/sell/dividend/split/bonus)
- /holdings/ - View holdings saat ini dengan performance metrics

## Asset Endpoints:
- GET /assets/ - List semua asset dengan filtering
- GET /assets/{id}/ - Detail asset dengan price history
- GET /assets/search/ - Pencarian asset untuk autocomplete
- GET /assets/{id}/prices/ - Price history asset
- POST /assets/{id}/add_price/ - Add price data (admin only)
- GET /assets/by_type/ - Asset grouped by type
- GET /assets/statistics/ - Asset statistics

## Portfolio Endpoints:
- GET /portfolios/ - List portfolio user dengan metrics
- POST /portfolios/ - Create portfolio baru
- GET /portfolios/{id}/ - Detail portfolio dengan holdings
- PUT /portfolios/{id}/ - Update portfolio
- DELETE /portfolios/{id}/ - Delete portfolio
- GET /portfolios/{id}/performance/ - Performance analysis
- GET /portfolios/{id}/allocation/ - Asset allocation breakdown
- POST /portfolios/{id}/rebalance/ - Rebalancing recommendations
- GET /portfolios/overview/ - Overview semua portfolio

## Transaction Endpoints:
- GET /transactions/ - List transaksi dengan filtering
- POST /transactions/ - Create transaksi baru (auto-update holdings)
- GET /transactions/{id}/ - Detail transaksi
- PUT /transactions/{id}/ - Update transaksi
- DELETE /transactions/{id}/ - Delete transaksi
- GET /transactions/summary/ - Transaction summary
- GET /transactions/by_asset/ - Transactions grouped by asset
- GET /transactions/monthly_report/ - Monthly transaction report
- POST /transactions/bulk_create/ - Bulk import transactions
- GET /transactions/export/ - Export to CSV

## Holdings Endpoints (Read-Only):
- GET /holdings/ - List current holdings dengan metrics
- GET /holdings/{id}/ - Detail holding dengan analytics
- GET /holdings/by_portfolio/ - Holdings grouped by portfolio
- POST /holdings/refresh/ - Refresh dengan current prices
- GET /holdings/analytics/ - Investment analytics overview
- GET /holdings/diversification/ - Diversification analysis
- GET /holdings/performance/ - Performance analysis

Semua endpoint mendukung pagination, searching, dan ordering.
Filter parameters tersedia untuk setiap endpoint sesuai kebutuhan.
"""

# Membuat router untuk API
router = DefaultRouter()
router.register(r'assets', AssetViewSet, basename='asset')
router.register(r'portfolios', InvestmentPortfolioViewSet, basename='portfolio')
router.register(r'transactions', InvestmentTransactionViewSet, basename='transaction')
router.register(r'holdings', InvestmentHoldingViewSet, basename='holding')

urlpatterns = [
    path('', include(router.urls)),
]
