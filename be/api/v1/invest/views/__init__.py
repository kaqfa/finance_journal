# Investment Module Views
# Modern investment portfolio views

from .asset import AssetViewSet
from .portfolio import InvestmentPortfolioViewSet
from .transaction import InvestmentTransactionViewSet
from .holding import InvestmentHoldingViewSet

__all__ = [
    'AssetViewSet',
    'InvestmentPortfolioViewSet', 
    'InvestmentTransactionViewSet',
    'InvestmentHoldingViewSet',
]
