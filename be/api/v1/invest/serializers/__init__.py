# Investment Module Serializers
# Professional investment tracking serializers

from .asset import (
    AssetSerializer,
    AssetListSerializer,
    AssetSearchSerializer,
    AssetPriceSerializer
)

from .portfolio import (
    InvestmentPortfolioSerializer,
    InvestmentPortfolioListSerializer,
    InvestmentHoldingSerializer,
    PortfolioAllocationSerializer,
    PortfolioPerformanceSerializer
)

from .transaction import (
    InvestmentTransactionSerializer,
    InvestmentTransactionListSerializer,
    TransactionSummarySerializer,
    TransactionsByAssetSerializer
)

from .holding import (
    InvestmentHoldingListSerializer,
    InvestmentHoldingDetailSerializer,
    HoldingRefreshSerializer,
    InvestmentAnalyticsSerializer,
    DiversificationAnalysisSerializer,
    PerformanceAnalysisSerializer
)

__all__ = [
    # Asset serializers
    'AssetSerializer',
    'AssetListSerializer', 
    'AssetSearchSerializer',
    'AssetPriceSerializer',
    
    # Portfolio serializers
    'InvestmentPortfolioSerializer',
    'InvestmentPortfolioListSerializer',
    'InvestmentHoldingSerializer',
    'PortfolioAllocationSerializer',
    'PortfolioPerformanceSerializer',
    
    # Transaction serializers
    'InvestmentTransactionSerializer',
    'InvestmentTransactionListSerializer',
    'TransactionSummarySerializer',
    'TransactionsByAssetSerializer',
    
    # Holding & Analytics serializers
    'InvestmentHoldingListSerializer',
    'InvestmentHoldingDetailSerializer',
    'HoldingRefreshSerializer',
    'InvestmentAnalyticsSerializer',
    'DiversificationAnalysisSerializer',
    'PerformanceAnalysisSerializer',
]
