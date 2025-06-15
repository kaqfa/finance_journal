from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from decimal import Decimal

from invest.models import InvestmentPortfolio, InvestmentHolding, Asset
from ..serializers import (
    InvestmentPortfolioSerializer,
    InvestmentPortfolioListSerializer,
    PortfolioAllocationSerializer,
    PortfolioPerformanceSerializer,
    InvestmentHoldingSerializer
)
from api.utils.permissions import IsOwner
from api.utils.mixins import ChoicesMixin


class InvestmentPortfolioViewSet(ChoicesMixin, viewsets.ModelViewSet):
    """
    Investment Portfolio Management.
    
    Portfolio merepresentasikan kumpulan investasi user dengan strategi
    dan alokasi target tertentu. Setiap portfolio bisa berisi multiple holdings
    dari berbagai asset types.
    
    Features:
    - CRUD operations untuk portfolio
    - Portfolio performance metrics
    - Asset allocation analysis
    - Rebalancing recommendations
    - Holdings management
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'initial_capital']
    ordering = ['-created_at']
    
    choices_config = {
        'risk_levels': {
            'choices': InvestmentPortfolio.RISK_LEVEL_CHOICES,
            'description': 'Level risiko portfolio yang tersedia'
        }
    }
    
    def get_serializer_class(self):
        """Menggunakan serializer yang berbeda untuk list dan detail view"""
        if self.action == 'list':
            return InvestmentPortfolioListSerializer
        return InvestmentPortfolioSerializer
    
    def get_queryset(self):
        """
        Filter queryset untuk hanya menampilkan portfolio milik user saat ini
        dengan opsi filter tambahan.
        
        Query Parameters:
        - is_active: Filter berdasarkan status aktif (true/false)
        - risk_level: Filter berdasarkan risk level
        - min_value: Minimum total value portfolio
        - max_value: Maximum total value portfolio
        """
        queryset = InvestmentPortfolio.objects.filter(user=self.request.user)
        
        # Filter by is_active
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        # Filter by risk_level
        risk_level = self.request.query_params.get('risk_level')
        if risk_level:
            queryset = queryset.filter(risk_level=risk_level)
        
        # Filter by portfolio value range
        min_value = self.request.query_params.get('min_value')
        max_value = self.request.query_params.get('max_value')
        
        if min_value or max_value:
            # Calculate portfolio values for filtering
            portfolio_ids = []
            for portfolio in queryset:
                total_value = sum(h.current_value for h in portfolio.holdings.all())
                
                include_portfolio = True
                if min_value and total_value < Decimal(min_value):
                    include_portfolio = False
                if max_value and total_value > Decimal(max_value):
                    include_portfolio = False
                
                if include_portfolio:
                    portfolio_ids.append(portfolio.id)
            
            queryset = queryset.filter(id__in=portfolio_ids)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        """
        Mendapatkan detailed performance metrics untuk portfolio.
        
        Query Parameters:
        - period: Period analisis ('1M', '3M', '6M', '1Y', 'YTD', 'ALL')
        
        Returns comprehensive performance analysis including:
        - Total return, ROI, annualized return
        - Risk metrics (volatility, Sharpe ratio, max drawdown)
        - Benchmark comparison
        - Performance attribution
        """
        portfolio = self.get_object()
        period = request.query_params.get('period', '1Y')
        
        # Calculate basic metrics
        holdings = portfolio.holdings.all()
        total_cost = sum(h.total_cost for h in holdings)
        total_value = sum(h.current_value for h in holdings)
        total_pnl = total_value - total_cost
        
        if total_cost > 0:
            total_return_pct = (total_pnl / total_cost) * 100
        else:
            total_return_pct = 0
        
        # Get transaction history for period analysis
        end_date = timezone.now().date()
        if period == '1M':
            start_date = end_date - timezone.timedelta(days=30)
        elif period == '3M':
            start_date = end_date - timezone.timedelta(days=90)
        elif period == '6M':
            start_date = end_date - timezone.timedelta(days=180)
        elif period == '1Y':
            start_date = end_date - timezone.timedelta(days=365)
        elif period == 'YTD':
            start_date = timezone.datetime(end_date.year, 1, 1).date()
        else:  # ALL
            start_date = portfolio.created_at.date()
        
        # Calculate period-specific metrics
        period_transactions = portfolio.transactions.filter(
            transaction_date__gte=start_date,
            transaction_date__lte=end_date
        )
        
        period_investment = sum(
            t.total_amount for t in period_transactions.filter(transaction_type='buy')
        )
        period_withdrawal = sum(
            t.total_amount for t in period_transactions.filter(transaction_type='sell')
        )
        
        # Calculate annualized return
        holding_period_days = (end_date - start_date).days
        if holding_period_days > 0 and total_cost > 0:
            annualized_return = ((total_value / total_cost) ** (365 / holding_period_days) - 1) * 100
        else:
            annualized_return = 0
        
        # Calculate volatility (simplified version)
        # In real implementation, you'd use daily portfolio values
        volatility = 0  # Placeholder
        
        # Calculate Sharpe ratio (simplified)
        risk_free_rate = 6.0  # Assume 6% risk-free rate
        if volatility > 0:
            sharpe_ratio = (annualized_return - risk_free_rate) / volatility
        else:
            sharpe_ratio = 0
        
        # Best and worst performing holdings
        best_performer = None
        worst_performer = None
        
        if holdings:
            best_holding = max(holdings, key=lambda h: (h.unrealized_pnl / h.total_cost) if h.total_cost > 0 else 0)
            worst_holding = min(holdings, key=lambda h: (h.unrealized_pnl / h.total_cost) if h.total_cost > 0 else 0)
            
            best_performer = {
                'symbol': best_holding.asset.symbol,
                'name': best_holding.asset.name,
                'return_percentage': round((best_holding.unrealized_pnl / best_holding.total_cost) * 100, 2) if best_holding.total_cost > 0 else 0
            }
            
            worst_performer = {
                'symbol': worst_holding.asset.symbol,
                'name': worst_holding.asset.name,
                'return_percentage': round((worst_holding.unrealized_pnl / worst_holding.total_cost) * 100, 2) if worst_holding.total_cost > 0 else 0
            }
        
        performance_data = {
            'period': period,
            'total_value': total_value,
            'total_cost': total_cost,
            'total_return': total_pnl,
            'total_return_percentage': round(total_return_pct, 2),
            'annualized_return': round(annualized_return, 2),
            'volatility': round(volatility, 2),
            'sharpe_ratio': round(sharpe_ratio, 2),
            'max_drawdown': 0,  # Placeholder
            'best_day': 0,  # Placeholder
            'worst_day': 0,  # Placeholder
            'period_investment': period_investment,
            'period_withdrawal': period_withdrawal,
            'best_performer': best_performer,
            'worst_performer': worst_performer,
            'holdings_count': holdings.count(),
            'generated_at': timezone.now()
        }
        
        return Response(performance_data)
    
    @action(detail=True, methods=['get'])
    def allocation(self, request, pk=None):
        """
        Mendapatkan detailed asset allocation breakdown untuk portfolio.
        
        Returns allocation analysis berdasarkan:
        - Asset type (stocks, bonds, crypto, dll)
        - Sector (technology, healthcare, dll)
        - Currency
        - Geographic region
        - Market cap size
        """
        portfolio = self.get_object()
        holdings = portfolio.holdings.all()
        
        if not holdings:
            return Response({
                'message': 'Portfolio tidak memiliki holdings',
                'allocations': {}
            })
        
        total_value = sum(h.current_value for h in holdings)
        
        # Allocation by asset type
        by_asset_type = {}
        for holding in holdings:
            asset_type = holding.asset.type
            if asset_type not in by_asset_type:
                by_asset_type[asset_type] = {
                    'value': 0,
                    'percentage': 0,
                    'holdings_count': 0
                }
            by_asset_type[asset_type]['value'] += holding.current_value
            by_asset_type[asset_type]['holdings_count'] += 1
        
        # Calculate percentages
        for asset_type in by_asset_type:
            by_asset_type[asset_type]['percentage'] = round(
                (by_asset_type[asset_type]['value'] / total_value) * 100, 2
            ) if total_value > 0 else 0
        
        # Allocation by sector
        by_sector = {}
        for holding in holdings:
            sector = holding.asset.sector or 'Other'
            if sector not in by_sector:
                by_sector[sector] = {
                    'value': 0,
                    'percentage': 0,
                    'holdings_count': 0
                }
            by_sector[sector]['value'] += holding.current_value
            by_sector[sector]['holdings_count'] += 1
        
        # Calculate sector percentages
        for sector in by_sector:
            by_sector[sector]['percentage'] = round(
                (by_sector[sector]['value'] / total_value) * 100, 2
            ) if total_value > 0 else 0
        
        # Allocation by currency
        by_currency = {}
        for holding in holdings:
            currency = holding.asset.currency
            if currency not in by_currency:
                by_currency[currency] = {
                    'value': 0,
                    'percentage': 0,
                    'holdings_count': 0
                }
            by_currency[currency]['value'] += holding.current_value
            by_currency[currency]['holdings_count'] += 1
        
        # Calculate currency percentages
        for currency in by_currency:
            by_currency[currency]['percentage'] = round(
                (by_currency[currency]['value'] / total_value) * 100, 2
            ) if total_value > 0 else 0
        
        # Top holdings
        top_holdings = sorted(holdings, key=lambda h: h.current_value, reverse=True)[:10]
        top_holdings_data = []
        
        for holding in top_holdings:
            percentage = round((holding.current_value / total_value) * 100, 2) if total_value > 0 else 0
            top_holdings_data.append({
                'symbol': holding.asset.symbol,
                'name': holding.asset.name,
                'value': holding.current_value,
                'percentage': percentage
            })
        
        # Calculate diversification score (simplified Herfindahl index)
        holdings_percentages = [
            (h.current_value / total_value) for h in holdings if total_value > 0
        ]
        herfindahl_index = sum(p ** 2 for p in holdings_percentages)
        diversification_score = round((1 - herfindahl_index) * 100, 2)
        
        allocation_data = {
            'total_value': total_value,
            'holdings_count': holdings.count(),
            'by_asset_type': by_asset_type,
            'by_sector': by_sector,
            'by_currency': by_currency,
            'top_holdings': top_holdings_data,
            'diversification_score': diversification_score,
            'target_allocation': portfolio.target_allocation or {},
            'generated_at': timezone.now()
        }
        
        return Response(allocation_data)
    
    @action(detail=True, methods=['post'])
    def rebalance(self, request, pk=None):
        """
        Memberikan rekomendasi rebalancing untuk portfolio.
        
        Request Body:
        - target_allocation: Dict dengan target allocation baru (optional)
        - max_deviation: Maximum deviation yang diizinkan (default: 5%)
        
        Returns rekomendasi buy/sell untuk mencapai target allocation.
        """
        portfolio = self.get_object()
        target_allocation = request.data.get('target_allocation', portfolio.target_allocation)
        max_deviation = float(request.data.get('max_deviation', 5.0))
        
        if not target_allocation:
            return Response({
                'error': 'Target allocation diperlukan untuk rebalancing'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        holdings = portfolio.holdings.all()
        total_value = sum(h.current_value for h in holdings)
        
        if total_value <= 0:
            return Response({
                'error': 'Portfolio tidak memiliki nilai untuk direbalance'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate current allocation
        current_allocation = {}
        for holding in holdings:
            asset_type = holding.asset.type
            if asset_type not in current_allocation:
                current_allocation[asset_type] = 0
            current_allocation[asset_type] += (holding.current_value / total_value) * 100
        
        # Find deviations
        recommendations = []
        
        for asset_type, target_percentage in target_allocation.items():
            current_percentage = current_allocation.get(asset_type, 0)
            deviation = current_percentage - target_percentage
            
            if abs(deviation) > max_deviation:
                target_value = (target_percentage / 100) * total_value
                current_value = (current_percentage / 100) * total_value
                adjustment_amount = target_value - current_value
                
                action = 'sell' if adjustment_amount < 0 else 'buy'
                
                recommendations.append({
                    'asset_type': asset_type,
                    'current_percentage': round(current_percentage, 2),
                    'target_percentage': target_percentage,
                    'deviation': round(deviation, 2),
                    'action': action,
                    'amount': abs(adjustment_amount),
                    'priority': 'high' if abs(deviation) > max_deviation * 2 else 'medium'
                })
        
        # Sort by deviation magnitude
        recommendations.sort(key=lambda x: abs(x['deviation']), reverse=True)
        
        rebalance_data = {
            'portfolio': portfolio.name,
            'total_value': total_value,
            'current_allocation': current_allocation,
            'target_allocation': target_allocation,
            'max_deviation': max_deviation,
            'recommendations': recommendations,
            'total_adjustments': len(recommendations),
            'generated_at': timezone.now()
        }
        
        return Response(rebalance_data)
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """
        Mendapatkan overview semua portfolio user.
        
        Returns ringkasan portfolio dengan metrics utama.
        """
        portfolios = self.get_queryset()
        
        total_portfolios = portfolios.count()
        active_portfolios = portfolios.filter(is_active=True).count()
        
        # Calculate totals across all portfolios
        total_value = 0
        total_cost = 0
        total_holdings = 0
        
        portfolio_summaries = []
        
        for portfolio in portfolios:
            holdings = portfolio.holdings.all()
            portfolio_value = sum(h.current_value for h in holdings)
            portfolio_cost = sum(h.total_cost for h in holdings)
            portfolio_pnl = portfolio_value - portfolio_cost
            
            total_value += portfolio_value
            total_cost += portfolio_cost
            total_holdings += holdings.count()
            
            portfolio_summaries.append({
                'id': str(portfolio.id),
                'name': portfolio.name,
                'value': portfolio_value,
                'cost': portfolio_cost,
                'pnl': portfolio_pnl,
                'pnl_percentage': round((portfolio_pnl / portfolio_cost) * 100, 2) if portfolio_cost > 0 else 0,
                'holdings_count': holdings.count(),
                'risk_level': portfolio.risk_level,
                'is_active': portfolio.is_active
            })
        
        # Sort by value
        portfolio_summaries.sort(key=lambda x: x['value'], reverse=True)
        
        total_pnl = total_value - total_cost
        
        overview_data = {
            'total_portfolios': total_portfolios,
            'active_portfolios': active_portfolios,
            'total_value': total_value,
            'total_cost': total_cost,
            'total_pnl': total_pnl,
            'total_pnl_percentage': round((total_pnl / total_cost) * 100, 2) if total_cost > 0 else 0,
            'total_holdings': total_holdings,
            'portfolios': portfolio_summaries,
            'best_performing': portfolio_summaries[0] if portfolio_summaries else None,
            'generated_at': timezone.now()
        }
        
        return Response(overview_data)
