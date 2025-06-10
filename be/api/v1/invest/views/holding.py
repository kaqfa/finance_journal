from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from decimal import Decimal

from invest.models import InvestmentHolding, Asset, AssetPrice
from ..serializers import (
    InvestmentHoldingListSerializer,
    InvestmentHoldingDetailSerializer,
    HoldingRefreshSerializer,
    InvestmentAnalyticsSerializer,
    DiversificationAnalysisSerializer,
    PerformanceAnalysisSerializer
)
from api.utils.permissions import IsOwner
from api.utils.mixins import ChoicesMixin


class InvestmentHoldingViewSet(ChoicesMixin, viewsets.ReadOnlyModelViewSet):
    """
    Investment Holdings Management (Read-Only).
    
    Holdings merepresentasikan kepemilikan asset saat ini dalam portfolio.
    Holdings diupdate otomatis berdasarkan transaksi dan tidak bisa dimodifikasi manual.
    
    Features:
    - View current holdings dengan performance metrics
    - Holdings grouped by portfolio
    - Refresh holdings dengan current prices
    - Analytics dan diversification analysis
    - Performance attribution
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['asset__symbol', 'asset__name', 'portfolio__name']
    ordering_fields = ['current_value', 'unrealized_pnl', 'last_updated']
    ordering = ['-current_value']
    
    def get_serializer_class(self):
        """Menggunakan serializer yang berbeda untuk list dan detail view"""
        if self.action == 'list':
            return InvestmentHoldingListSerializer
        return InvestmentHoldingDetailSerializer
    
    def get_queryset(self):
        """
        Filter queryset untuk hanya menampilkan holdings milik user saat ini.
        
        Query Parameters:
        - portfolio: Filter berdasarkan portfolio ID
        - asset_type: Filter berdasarkan asset type
        - min_value: Minimum current value
        - max_value: Maximum current value
        - profitable_only: Hanya holdings yang profitable (true/false)
        """
        queryset = InvestmentHolding.objects.filter(
            user=self.request.user,
            quantity__gt=0  # Only show holdings with positive quantity
        )
        
        # Filter by portfolio
        portfolio_id = self.request.query_params.get('portfolio')
        if portfolio_id:
            queryset = queryset.filter(portfolio_id=portfolio_id)
        
        # Filter by asset type
        asset_type = self.request.query_params.get('asset_type')
        if asset_type:
            queryset = queryset.filter(asset__type=asset_type)
        
        # Filter by value range
        min_value = self.request.query_params.get('min_value')
        max_value = self.request.query_params.get('max_value')
        
        if min_value:
            queryset = queryset.filter(current_value__gte=min_value)
        if max_value:
            queryset = queryset.filter(current_value__lte=max_value)
        
        # Filter profitable only
        profitable_only = self.request.query_params.get('profitable_only')
        if profitable_only and profitable_only.lower() == 'true':
            queryset = queryset.filter(unrealized_pnl__gt=0)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_portfolio(self, request):
        """
        Mendapatkan holdings yang dikelompokkan berdasarkan portfolio.
        
        Returns holdings grouped by portfolio dengan summary metrics.
        """
        queryset = self.get_queryset()
        
        # Group by portfolio
        portfolio_groups = {}
        
        for holding in queryset:
            portfolio_id = str(holding.portfolio.id)
            
            if portfolio_id not in portfolio_groups:
                portfolio_groups[portfolio_id] = {
                    'portfolio': holding.portfolio,
                    'holdings': [],
                    'total_value': 0,
                    'total_cost': 0,
                    'total_pnl': 0,
                    'holdings_count': 0
                }
            
            group = portfolio_groups[portfolio_id]
            group['holdings'].append(holding)
            group['total_value'] += holding.current_value
            group['total_cost'] += holding.total_cost
            group['total_pnl'] += holding.unrealized_pnl
            group['holdings_count'] += 1
        
        # Prepare response data
        results = []
        
        for portfolio_id, group in portfolio_groups.items():
            from ..serializers import InvestmentPortfolioListSerializer
            
            # Calculate portfolio metrics
            total_pnl_percentage = 0
            if group['total_cost'] > 0:
                total_pnl_percentage = (group['total_pnl'] / group['total_cost']) * 100
            
            # Get top performing holding
            best_holding = max(group['holdings'], key=lambda h: h.unrealized_pnl) if group['holdings'] else None
            worst_holding = min(group['holdings'], key=lambda h: h.unrealized_pnl) if group['holdings'] else None
            
            result = {
                'portfolio': InvestmentPortfolioListSerializer(group['portfolio']).data,
                'holdings_count': group['holdings_count'],
                'total_value': group['total_value'],
                'total_cost': group['total_cost'],
                'total_pnl': group['total_pnl'],
                'total_pnl_percentage': round(total_pnl_percentage, 2),
                'best_performer': {
                    'symbol': best_holding.asset.symbol,
                    'pnl': best_holding.unrealized_pnl
                } if best_holding else None,
                'worst_performer': {
                    'symbol': worst_holding.asset.symbol,
                    'pnl': worst_holding.unrealized_pnl
                } if worst_holding else None,
                'holdings': InvestmentHoldingListSerializer(group['holdings'], many=True).data
            }
            
            results.append(result)
        
        # Sort by total value
        results.sort(key=lambda x: x['total_value'], reverse=True)
        
        return Response({
            'portfolio_groups': results,
            'total_portfolios': len(results),
            'generated_at': timezone.now()
        })
    
    @action(detail=False, methods=['post'])
    def refresh(self, request):
        """
        Refresh holdings dengan current prices dari market data.
        
        Request Body:
        - portfolio_ids: List of portfolio IDs to refresh (optional, default: all)
        - force_update: Force update even if recently updated (default: false)
        
        Updates current_price, current_value, dan unrealized_pnl untuk holdings.
        """
        portfolio_ids = request.data.get('portfolio_ids', [])
        force_update = request.data.get('force_update', False)
        
        queryset = self.get_queryset()
        
        if portfolio_ids:
            queryset = queryset.filter(portfolio_id__in=portfolio_ids)
        
        # Filter holdings that need update
        if not force_update:
            # Only update holdings that haven't been updated in the last hour
            one_hour_ago = timezone.now() - timezone.timedelta(hours=1)
            queryset = queryset.filter(last_updated__lt=one_hour_ago)
        
        holdings_updated = 0
        total_value_before = sum(h.current_value for h in queryset)
        
        for holding in queryset:
            # Get latest price for the asset
            latest_price = holding.asset.prices.order_by('-timestamp').first()
            
            if latest_price:
                old_value = holding.current_value
                
                # Update current price and calculate new values
                holding.current_price = latest_price.price
                holding.current_value = holding.quantity * holding.current_price
                holding.unrealized_pnl = holding.current_value - holding.total_cost
                holding.last_updated = timezone.now()
                
                holding.save()
                holdings_updated += 1
        
        # Calculate totals after update
        refreshed_holdings = self.get_queryset()
        if portfolio_ids:
            refreshed_holdings = refreshed_holdings.filter(portfolio_id__in=portfolio_ids)
        
        total_value_after = sum(h.current_value for h in refreshed_holdings)
        value_change = total_value_after - total_value_before
        value_change_percentage = 0
        
        if total_value_before > 0:
            value_change_percentage = (value_change / total_value_before) * 100
        
        refresh_data = {
            'holdings_updated': holdings_updated,
            'total_value_before': total_value_before,
            'total_value_after': total_value_after,
            'value_change': value_change,
            'value_change_percentage': round(value_change_percentage, 2),
            'last_refresh': timezone.now()
        }
        
        return Response(refresh_data)
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """
        Mendapatkan comprehensive analytics untuk semua holdings user.
        
        Returns overview analytics termasuk allocation, performance, top performers, dll.
        """
        queryset = self.get_queryset()
        
        if not queryset.exists():
            return Response({
                'message': 'No holdings found',
                'analytics': {}
            })
        
        # Calculate basic metrics
        total_portfolios = queryset.values('portfolio').distinct().count()
        total_value = sum(h.current_value for h in queryset)
        total_cost = sum(h.total_cost for h in queryset)
        total_pnl = total_value - total_cost
        total_pnl_percentage = (total_pnl / total_cost) * 100 if total_cost > 0 else 0
        
        # Top performers
        top_performers = sorted(queryset, key=lambda h: h.unrealized_pnl, reverse=True)[:5]
        top_performers_data = []
        
        for holding in top_performers:
            pnl_percentage = (holding.unrealized_pnl / holding.total_cost) * 100 if holding.total_cost > 0 else 0
            top_performers_data.append({
                'symbol': holding.asset.symbol,
                'name': holding.asset.name,
                'pnl': holding.unrealized_pnl,
                'pnl_percentage': round(pnl_percentage, 2),
                'portfolio': holding.portfolio.name
            })
        
        # Worst performers
        worst_performers = sorted(queryset, key=lambda h: h.unrealized_pnl)[:5]
        worst_performers_data = []
        
        for holding in worst_performers:
            pnl_percentage = (holding.unrealized_pnl / holding.total_cost) * 100 if holding.total_cost > 0 else 0
            worst_performers_data.append({
                'symbol': holding.asset.symbol,
                'name': holding.asset.name,
                'pnl': holding.unrealized_pnl,
                'pnl_percentage': round(pnl_percentage, 2),
                'portfolio': holding.portfolio.name
            })
        
        # Allocation by asset type
        allocation_by_type = {}
        for holding in queryset:
            asset_type = holding.asset.type
            if asset_type not in allocation_by_type:
                allocation_by_type[asset_type] = 0
            allocation_by_type[asset_type] += holding.current_value
        
        # Convert to percentages
        for asset_type in allocation_by_type:
            allocation_by_type[asset_type] = round(
                (allocation_by_type[asset_type] / total_value) * 100, 2
            ) if total_value > 0 else 0
        
        # Allocation by sector
        allocation_by_sector = {}
        for holding in queryset:
            sector = holding.asset.sector or 'Other'
            if sector not in allocation_by_sector:
                allocation_by_sector[sector] = 0
            allocation_by_sector[sector] += holding.current_value
        
        # Convert to percentages
        for sector in allocation_by_sector:
            allocation_by_sector[sector] = round(
                (allocation_by_sector[sector] / total_value) * 100, 2
            ) if total_value > 0 else 0
        
        # Monthly performance (simplified)
        monthly_performance = []
        current_month = timezone.now().replace(day=1)
        
        for i in range(12):
            month = current_month - timezone.timedelta(days=30 * i)
            # In real implementation, you'd track historical portfolio values
            monthly_performance.append({
                'month': month.strftime('%Y-%m'),
                'value': total_value,  # Placeholder
                'return_percentage': 0  # Placeholder
            })
        
        analytics_data = {
            'total_portfolios': total_portfolios,
            'total_value': total_value,
            'total_cost': total_cost,
            'total_pnl': total_pnl,
            'total_pnl_percentage': round(total_pnl_percentage, 2),
            'top_performers': top_performers_data,
            'worst_performers': worst_performers_data,
            'allocation_by_type': allocation_by_type,
            'allocation_by_sector': allocation_by_sector,
            'monthly_performance': monthly_performance,
            'generated_at': timezone.now()
        }
        
        return Response(analytics_data)
    
    @action(detail=False, methods=['get'])
    def diversification(self, request):
        """
        Mendapatkan analisis diversifikasi portfolio.
        
        Returns metrics diversifikasi dan rekomendasi untuk improvement.
        """
        queryset = self.get_queryset()
        
        if not queryset.exists():
            return Response({
                'message': 'No holdings found for diversification analysis',
                'diversification': {}
            })
        
        total_value = sum(h.current_value for h in queryset)
        
        # Calculate Herfindahl-Hirschman Index for concentration
        holdings_weights = [(h.current_value / total_value) for h in queryset if total_value > 0]
        hhi = sum(w ** 2 for w in holdings_weights)
        diversification_score = round((1 - hhi) * 100, 2)
        concentration_risk = round(hhi * 100, 2)
        
        # Sector diversification
        sector_diversification = {}
        for holding in queryset:
            sector = holding.asset.sector or 'Other'
            if sector not in sector_diversification:
                sector_diversification[sector] = 0
            sector_diversification[sector] += holding.current_value
        
        # Convert to percentages and find concentration
        max_sector_allocation = 0
        for sector in sector_diversification:
            percentage = (sector_diversification[sector] / total_value) * 100 if total_value > 0 else 0
            sector_diversification[sector] = round(percentage, 2)
            max_sector_allocation = max(max_sector_allocation, percentage)
        
        # Asset type diversification
        asset_type_diversification = {}
        for holding in queryset:
            asset_type = holding.asset.type
            if asset_type not in asset_type_diversification:
                asset_type_diversification[asset_type] = 0
            asset_type_diversification[asset_type] += holding.current_value
        
        # Convert to percentages
        for asset_type in asset_type_diversification:
            percentage = (asset_type_diversification[asset_type] / total_value) * 100 if total_value > 0 else 0
            asset_type_diversification[asset_type] = round(percentage, 2)
        
        # Geographic diversification (simplified by currency)
        geographic_diversification = {}
        for holding in queryset:
            currency = holding.asset.currency
            if currency not in geographic_diversification:
                geographic_diversification[currency] = 0
            geographic_diversification[currency] += holding.current_value
        
        # Convert to percentages
        for currency in geographic_diversification:
            percentage = (geographic_diversification[currency] / total_value) * 100 if total_value > 0 else 0
            geographic_diversification[currency] = round(percentage, 2)
        
        # Rebalancing recommendations
        recommendations = []
        
        # Check for over-concentration
        largest_holding = max(queryset, key=lambda h: h.current_value) if queryset else None
        if largest_holding:
            largest_percentage = (largest_holding.current_value / total_value) * 100 if total_value > 0 else 0
            if largest_percentage > 20:  # If single holding > 20%
                recommendations.append({
                    'type': 'reduce_concentration',
                    'message': f'Consider reducing {largest_holding.asset.symbol} position ({largest_percentage:.1f}% of portfolio)',
                    'priority': 'high' if largest_percentage > 30 else 'medium'
                })
        
        # Check sector concentration
        if max_sector_allocation > 40:
            recommendations.append({
                'type': 'sector_diversification',
                'message': f'Consider diversifying across sectors (max sector allocation: {max_sector_allocation:.1f}%)',
                'priority': 'medium'
            })
        
        # Check number of holdings
        if len(queryset) < 5:
            recommendations.append({
                'type': 'add_holdings',
                'message': 'Consider adding more holdings to improve diversification',
                'priority': 'medium'
            })
        elif len(queryset) > 50:
            recommendations.append({
                'type': 'reduce_holdings',
                'message': 'Consider consolidating positions for better management',
                'priority': 'low'
            })
        
        # Correlation matrix (simplified placeholder)
        correlation_matrix = {}
        symbols = [h.asset.symbol for h in queryset]
        for symbol1 in symbols:
            correlation_matrix[symbol1] = {}
            for symbol2 in symbols:
                # In real implementation, calculate actual correlation
                correlation_matrix[symbol1][symbol2] = 0.5 if symbol1 != symbol2 else 1.0
        
        diversification_data = {
            'diversification_score': diversification_score,
            'concentration_risk': concentration_risk,
            'sector_diversification': sector_diversification,
            'geographic_diversification': geographic_diversification,
            'asset_type_diversification': asset_type_diversification,
            'correlation_matrix': correlation_matrix,
            'rebalancing_recommendations': recommendations,
            'metrics': {
                'total_holdings': len(queryset),
                'hhi_index': round(hhi, 4),
                'largest_holding_percentage': round((largest_holding.current_value / total_value) * 100, 2) if largest_holding else 0,
                'top_5_concentration': round(sum(
                    (h.current_value / total_value) * 100 
                    for h in sorted(queryset, key=lambda x: x.current_value, reverse=True)[:5]
                ), 2) if total_value > 0 else 0
            },
            'generated_at': timezone.now()
        }
        
        return Response(diversification_data)
    
    @action(detail=False, methods=['get'])
    def performance(self, request):
        """
        Mendapatkan detailed performance analysis untuk holdings.
        
        Query Parameters:
        - period: Period analisis ('1M', '3M', '6M', '1Y', 'ALL')
        
        Returns comprehensive performance metrics.
        """
        queryset = self.get_queryset()
        period = request.query_params.get('period', '1Y')
        
        if not queryset.exists():
            return Response({
                'message': 'No holdings found for performance analysis',
                'performance': {}
            })
        
        # Calculate basic performance metrics
        total_value = sum(h.current_value for h in queryset)
        total_cost = sum(h.total_cost for h in queryset)
        total_return = total_value - total_cost
        total_return_percentage = (total_return / total_cost) * 100 if total_cost > 0 else 0
        
        # Calculate win rate
        winning_positions = sum(1 for h in queryset if h.unrealized_pnl > 0)
        total_positions = len(queryset)
        win_rate = (winning_positions / total_positions) * 100 if total_positions > 0 else 0
        
        # Calculate profit factor
        total_gains = sum(h.unrealized_pnl for h in queryset if h.unrealized_pnl > 0)
        total_losses = abs(sum(h.unrealized_pnl for h in queryset if h.unrealized_pnl < 0))
        profit_factor = total_gains / total_losses if total_losses > 0 else float('inf')
        
        # Simplified metrics (in real implementation, use historical data)
        annualized_return = total_return_percentage  # Placeholder
        volatility = 15.0  # Placeholder
        risk_free_rate = 6.0  # Assume 6% risk-free rate
        
        sharpe_ratio = (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
        sortino_ratio = annualized_return / volatility if volatility > 0 else 0  # Placeholder
        max_drawdown = 10.0  # Placeholder
        calmar_ratio = annualized_return / max_drawdown if max_drawdown > 0 else 0
        alpha = 2.0  # Placeholder
        beta = 1.0  # Placeholder
        
        performance_data = {
            'total_return': total_return,
            'total_return_percentage': round(total_return_percentage, 2),
            'annualized_return': round(annualized_return, 2),
            'volatility': round(volatility, 2),
            'sharpe_ratio': round(sharpe_ratio, 2),
            'sortino_ratio': round(sortino_ratio, 2),
            'max_drawdown': round(max_drawdown, 2),
            'calmar_ratio': round(calmar_ratio, 2),
            'alpha': round(alpha, 2),
            'beta': round(beta, 2),
            'win_rate': round(win_rate, 2),
            'profit_factor': round(profit_factor, 2) if profit_factor != float('inf') else 'N/A',
            'period': period,
            'generated_at': timezone.now()
        }
        
        return Response(performance_data)
