"""
Basic tests untuk Investment Module API

Test coverage untuk endpoint utama dan business logic.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date

from invest.models import Asset, InvestmentPortfolio, InvestmentTransaction, InvestmentHolding

User = get_user_model()


class InvestmentAPITestCase(APITestCase):
    """Base test case untuk Investment API"""
    
    def setUp(self):
        """Setup test data"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test asset
        self.asset = Asset.objects.create(
            symbol='BBRI',
            name='Bank Rakyat Indonesia Tbk',
            type='stock',
            exchange='IDX',
            sector='Banking',
            currency='IDR'
        )
        
        # Create test portfolio
        self.portfolio = InvestmentPortfolio.objects.create(
            user=self.user,
            name='Test Portfolio',
            description='Portfolio untuk testing',
            initial_capital=Decimal('10000000.00'),
            risk_level='medium'
        )
        
        # Authenticate user
        self.client.force_authenticate(user=self.user)


class AssetAPITest(InvestmentAPITestCase):
    """Test untuk Asset API endpoints"""
    
    def test_list_assets(self):
        """Test list assets endpoint"""
        url = reverse('asset-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['symbol'], 'BBRI')
    
    def test_asset_detail(self):
        """Test asset detail endpoint"""
        url = reverse('asset-detail', kwargs={'pk': self.asset.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['symbol'], 'BBRI')
        self.assertEqual(response.data['name'], 'Bank Rakyat Indonesia Tbk')
    
    def test_search_assets(self):
        """Test asset search endpoint"""
        url = reverse('asset-search')
        response = self.client.get(url, {'q': 'BBRI'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['symbol'], 'BBRI')


class PortfolioAPITest(InvestmentAPITestCase):
    """Test untuk Portfolio API endpoints"""
    
    def test_list_portfolios(self):
        """Test list portfolios endpoint"""
        url = reverse('portfolio-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Portfolio')
    
    def test_create_portfolio(self):
        """Test create portfolio endpoint"""
        url = reverse('portfolio-list')
        data = {
            'name': 'New Portfolio',
            'description': 'Portfolio baru untuk testing',
            'initial_capital': '5000000.00',
            'risk_level': 'high',
            'target_allocation': {
                'stocks': 80,
                'bonds': 20
            }
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Portfolio')
        self.assertEqual(response.data['risk_level'], 'high')
    
    def test_portfolio_detail(self):
        """Test portfolio detail endpoint"""
        url = reverse('portfolio-detail', kwargs={'pk': self.portfolio.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Portfolio')
    
    def test_portfolio_performance(self):
        """Test portfolio performance endpoint"""
        url = reverse('portfolio-performance', kwargs={'pk': self.portfolio.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_value', response.data)
        self.assertIn('total_cost', response.data)
        self.assertIn('total_return', response.data)  # Changed from 'total_pnl'
        self.assertIn('total_return_percentage', response.data)
        self.assertIn('period', response.data)


class TransactionAPITest(InvestmentAPITestCase):
    """Test untuk Transaction API endpoints"""
    
    def test_create_buy_transaction(self):
        """Test create buy transaction"""
        url = reverse('transaction-list')
        data = {
            'portfolio_id': str(self.portfolio.id),
            'asset_id': str(self.asset.id),
            'transaction_type': 'buy',
            'quantity': '100.00000000',
            'price': '4500.00',
            'fees': '17000.00',
            'transaction_date': '2025-06-01',
            'broker': 'Test Broker',
            'notes': 'Test buy transaction'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['transaction_type'], 'buy')
        self.assertEqual(Decimal(response.data['total_amount']), Decimal('450000.00'))
        
        # Check if holding was created
        holding = InvestmentHolding.objects.filter(
            user=self.user,
            portfolio=self.portfolio,
            asset=self.asset
        ).first()
        
        self.assertIsNotNone(holding)
        self.assertEqual(holding.quantity, Decimal('100.00000000'))
    
    def test_create_sell_transaction(self):
        """Test create sell transaction"""
        # First create a holding
        InvestmentHolding.objects.create(
            user=self.user,
            portfolio=self.portfolio,
            asset=self.asset,
            quantity=Decimal('200.00000000'),
            average_price=Decimal('4000.00'),
            total_cost=Decimal('800000.00')
        )
        
        url = reverse('transaction-list')
        data = {
            'portfolio_id': str(self.portfolio.id),
            'asset_id': str(self.asset.id),
            'transaction_type': 'sell',
            'quantity': '50.00000000',
            'price': '4800.00',
            'fees': '12000.00',
            'transaction_date': '2025-06-02',
            'broker': 'Test Broker'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['transaction_type'], 'sell')
        
        # Check if holding was updated
        holding = InvestmentHolding.objects.get(
            user=self.user,
            portfolio=self.portfolio,
            asset=self.asset
        )
        
        self.assertEqual(holding.quantity, Decimal('150.00000000'))
    
    def test_transaction_summary(self):
        """Test transaction summary endpoint"""
        # Create some test transactions first
        InvestmentTransaction.objects.create(
            user=self.user,
            portfolio=self.portfolio,
            asset=self.asset,
            transaction_type='buy',
            quantity=Decimal('100.00000000'),
            price=Decimal('4500.00'),
            total_amount=Decimal('450000.00'),
            fees=Decimal('17000.00'),
            transaction_date=date.today()
        )
        
        url = reverse('transaction-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_transactions', response.data)
        self.assertIn('total_buy_amount', response.data)
        self.assertEqual(response.data['total_transactions'], 1)


class HoldingAPITest(InvestmentAPITestCase):
    """Test untuk Holding API endpoints"""
    
    def setUp(self):
        super().setUp()
        # Create test holding
        self.holding = InvestmentHolding.objects.create(
            user=self.user,
            portfolio=self.portfolio,
            asset=self.asset,
            quantity=Decimal('100.00000000'),
            average_price=Decimal('4500.00'),
            total_cost=Decimal('450000.00'),
            current_price=Decimal('4750.00'),
            current_value=Decimal('475000.00'),
            unrealized_pnl=Decimal('25000.00')
        )
    
    def test_list_holdings(self):
        """Test list holdings endpoint"""
        url = reverse('holding-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['asset_symbol'], 'BBRI')
    
    def test_holding_detail(self):
        """Test holding detail endpoint"""
        url = reverse('holding-detail', kwargs={'pk': self.holding.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['asset']['symbol'], 'BBRI')
        self.assertEqual(Decimal(response.data['unrealized_pnl']), Decimal('25000.00'))
    
    def test_holdings_by_portfolio(self):
        """Test holdings by portfolio endpoint"""
        url = reverse('holding-by-portfolio')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['portfolio_groups']), 1)
        self.assertEqual(response.data['portfolio_groups'][0]['holdings_count'], 1)
    
    def test_holdings_analytics(self):
        """Test holdings analytics endpoint"""
        url = reverse('holding-analytics')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_value', response.data)
        self.assertIn('allocation_by_type', response.data)
    
    def test_holdings_refresh(self):
        """Test holdings refresh endpoint"""
        url = reverse('holding-refresh')
        data = {
            'portfolio_ids': [str(self.portfolio.id)],
            'force_update': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('holdings_updated', response.data)


class BusinessLogicTest(InvestmentAPITestCase):
    """Test untuk business logic dan validations"""
    
    def test_insufficient_balance_sell(self):
        """Test sell transaction dengan insufficient balance"""
        url = reverse('transaction-list')
        data = {
            'portfolio_id': str(self.portfolio.id),
            'asset_id': str(self.asset.id),
            'transaction_type': 'sell',
            'quantity': '100.00000000',  # Tidak ada holding
            'price': '4500.00',
            'transaction_date': '2025-06-01'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Insufficient', str(response.data))
    
    def test_portfolio_ownership(self):
        """Test portfolio ownership validation"""
        # Create another user's portfolio
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        other_portfolio = InvestmentPortfolio.objects.create(
            user=other_user,
            name='Other Portfolio',
            initial_capital=Decimal('1000000.00')
        )
        
        url = reverse('transaction-list')
        data = {
            'portfolio_id': str(other_portfolio.id),
            'asset_id': str(self.asset.id),
            'transaction_type': 'buy',
            'quantity': '100.00000000',
            'price': '4500.00',
            'transaction_date': '2025-06-01'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("don't have access", str(response.data))
    
    def test_holding_auto_calculation(self):
        """Test auto calculation of holdings dari transaksi"""
        # Create buy transaction
        url = reverse('transaction-list')
        buy_data = {
            'portfolio_id': str(self.portfolio.id),
            'asset_id': str(self.asset.id),
            'transaction_type': 'buy',
            'quantity': '100.00000000',
            'price': '4500.00',
            'fees': '17000.00',
            'transaction_date': '2025-06-01'
        }
        response = self.client.post(url, buy_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check initial holding
        holding = InvestmentHolding.objects.get(
            user=self.user,
            portfolio=self.portfolio,
            asset=self.asset
        )
        
        self.assertEqual(holding.quantity, Decimal('100.00000000'))
        self.assertEqual(holding.total_cost, Decimal('467000.00'))  # 450000 + 17000 fees
        
        # Create another buy transaction
        buy_data2 = {
            'portfolio_id': str(self.portfolio.id),
            'asset_id': str(self.asset.id),
            'transaction_type': 'buy',
            'quantity': '50.00000000',
            'price': '4800.00',
            'fees': '12000.00',
            'transaction_date': '2025-06-02'
        }
        response = self.client.post(url, buy_data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check updated holding
        holding.refresh_from_db()
        
        self.assertEqual(holding.quantity, Decimal('150.00000000'))
        # Total cost = 467000 + 240000 + 12000 = 719000
        self.assertEqual(holding.total_cost, Decimal('719000.00'))
        # Average price = 719000 / 150 = 4793.33
        self.assertAlmostEqual(
            float(holding.average_price), 
            4793.33, 
            places=2
        )


class PermissionTest(InvestmentAPITestCase):
    """Test untuk permissions dan security"""
    
    def test_unauthenticated_access(self):
        """Test access tanpa authentication"""
        self.client.force_authenticate(user=None)
        
        url = reverse('portfolio-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_isolation(self):
        """Test user hanya bisa akses data miliknya"""
        # Create another user dengan data
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        
        other_portfolio = InvestmentPortfolio.objects.create(
            user=other_user,
            name='Other Portfolio',
            initial_capital=Decimal('1000000.00')
        )
        
        # Test bahwa user tidak bisa lihat portfolio user lain
        url = reverse('portfolio-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Hanya portfolio sendiri
        self.assertEqual(response.data['results'][0]['name'], 'Test Portfolio')
