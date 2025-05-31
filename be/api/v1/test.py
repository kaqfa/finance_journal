from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal

from finance.models import Category, Wallet, Transaction, Transfer, Tag, TransactionTag


class FinanceApiTestCase(APITestCase):
    def setUp(self):
        # Membuat user untuk testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Membuat token untuk user
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        
        # Set token di header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Membuat data test
        self.create_test_data()
        
    def create_test_data(self):
        # Membuat kategori
        self.income_category = Category.objects.create(
            user=self.user,
            name="Salary",
            type="income"
        )
        
        self.expense_category = Category.objects.create(
            user=self.user,
            name="Food",
            type="expense",
            icon="🍔",
            color="#FF5733"
        )
        
        # Membuat wallet
        self.wallet = Wallet.objects.create(
            user=self.user,
            name="Bank BCA",
            wallet_type="bank",
            initial_balance=Decimal("1000000"),
            currency="IDR"
        )
        
        # Membuat tag
        self.tag = Tag.objects.create(
            user=self.user,
            name="Important"
        )
        
        # Membuat transaction
        self.transaction = Transaction.objects.create(
            user=self.user,
            wallet=self.wallet,
            category=self.income_category,
            amount=Decimal("5000000"),
            type="income",
            description="Monthly salary",
            transaction_date="2025-05-01"
        )
        
        # Membuat wallet ke-2 untuk testing transfer
        self.wallet2 = Wallet.objects.create(
            user=self.user,
            name="E-Wallet",
            wallet_type="ewallet",
            initial_balance=Decimal("100000"),
            currency="IDR"
        )


class CategoryApiTests(FinanceApiTestCase):
    def test_list_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_create_category(self):
        url = reverse('category-list')
        data = {
            'name': 'Transportation',
            'type': 'expense',
            'icon': '🚗',
            'color': '#3498DB'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Transportation')
        self.assertEqual(response.data['type'], 'expense')
        
        # Verifikasi bahwa kategori dibuat di database
        self.assertTrue(Category.objects.filter(name='Transportation').exists())
    
    def test_get_expense_categories(self):
        url = reverse('category-expense')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Food')
    
    def test_get_income_categories(self):
        url = reverse('category-income')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Salary')


class WalletApiTests(FinanceApiTestCase):
    def test_list_wallets(self):
        url = reverse('wallet-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_create_wallet(self):
        url = reverse('wallet-list')
        data = {
            'name': 'Cash',
            'wallet_type': 'cash',
            'initial_balance': '500000',
            'currency': 'IDR'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Cash')
        self.assertEqual(response.data['wallet_type'], 'cash')
        self.assertEqual(response.data['initial_balance'], '500000.00')
        self.assertEqual(response.data['current_balance'], '500000.00')
        
        # Verifikasi bahwa wallet dibuat di database
        self.assertTrue(Wallet.objects.filter(name='Cash').exists())
    
    def test_recalculate_wallet_balance(self):
        # Tambahkan transaksi pengeluaran
        Transaction.objects.create(
            user=self.user,
            wallet=self.wallet,
            category=self.expense_category,
            amount=Decimal("200000"),
            type="expense",
            description="Grocery shopping",
            transaction_date="2025-05-02"
        )
        
        # Recalculate balance
        url = reverse('wallet-recalculate', args=[self.wallet.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Expected balance = initial (1,000,000) + income (5,000,000) - expense (200,000)
        self.assertEqual(response.data['current_balance'], '5800000.00')


class TransactionApiTests(FinanceApiTestCase):
    def test_list_transactions(self):
        url = reverse('transaction-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_transaction(self):
        url = reverse('transaction-list')
        data = {
            'wallet': self.wallet.id,
            'category': self.expense_category.id,
            'amount': '150000',
            'type': 'expense',
            'description': 'Restaurant bill',
            'transaction_date': '2025-05-03'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['amount'], '150000.00')
        self.assertEqual(response.data['type'], 'expense')
        
        # Verifikasi bahwa transaksi dibuat di database
        self.assertTrue(Transaction.objects.filter(description='Restaurant bill').exists())
        
        # Verifikasi bahwa saldo wallet terupdate
        self.wallet.refresh_from_db()
        # Expected = initial (1,000,000) + income (5,000,000) - expense (150,000)
        self.assertEqual(self.wallet.current_balance, Decimal('5850000.00'))
    
    def test_create_transaction_with_tags(self):
        url = reverse('transaction-list')
        data = {
            'wallet': self.wallet.id,
            'category': self.expense_category.id,
            'amount': '75000',
            'type': 'expense',
            'description': 'Coffee shop',
            'transaction_date': '2025-05-03',
            'tag_ids': [self.tag.id]
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifikasi bahwa transaksi memiliki tag
        transaction = Transaction.objects.get(description='Coffee shop')
        self.assertEqual(transaction.transaction_tags.count(), 1)
        self.assertEqual(transaction.transaction_tags.first().tag.name, 'Important')
    
    def test_get_transaction_summary(self):
        # Tambahkan transaksi expense
        Transaction.objects.create(
            user=self.user,
            wallet=self.wallet,
            category=self.expense_category,
            amount=Decimal("300000"),
            type="expense",
            description="Utilities",
            transaction_date="2025-05-04"
        )
        
        url = reverse('transaction-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['income'], '5000000.00')
        self.assertEqual(response.data['expense'], '300000.00')
        self.assertEqual(response.data['balance'], '4700000.00')
    
    def test_get_transactions_by_category(self):
        # Tambahkan beberapa transaksi dengan kategori yang sama
        for i in range(3):
            Transaction.objects.create(
                user=self.user,
                wallet=self.wallet,
                category=self.expense_category,
                amount=Decimal("100000"),
                type="expense",
                description=f"Food expense {i+1}",
                transaction_date=f"2025-05-{i+5}"
            )
        
        url = reverse('transaction-by-category')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Hanya 1 kategori expense
        self.assertEqual(response.data[0]['name'], 'Food')
        self.assertEqual(response.data[0]['amount'], '300000.00')
        self.assertEqual(response.data[0]['percentage'], 100.0)
    
    def test_get_monthly_report(self):
        # Tambahkan transaksi di bulan yang berbeda
        Transaction.objects.create(
            user=self.user,
            wallet=self.wallet,
            category=self.expense_category,
            amount=Decimal("400000"),
            type="expense",
            description="Shopping",
            transaction_date="2025-06-01"  # Bulan 6
        )
        
        url = reverse('transaction-monthly-report')
        response = self.client.get(url, {'year': '2025'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 12)  # 12 bulan
        
        # Check bulan 5 (May)
        may_data = next(item for item in response.data if item['month'] == 5)
        self.assertEqual(may_data['income'], '5000000.00')
        self.assertEqual(may_data['expense'], '0.00')
        self.assertEqual(may_data['balance'], '5000000.00')
        
        # Check bulan 6 (Jun)
        june_data = next(item for item in response.data if item['month'] == 6)
        self.assertEqual(june_data['income'], '0.00')
        self.assertEqual(june_data['expense'], '400000.00')
        self.assertEqual(june_data['balance'], '-400000.00')


class TransferApiTests(FinanceApiTestCase):
    def test_create_transfer(self):
        url = reverse('transfer-list')
        data = {
            'from_wallet': self.wallet.id,
            'to_wallet': self.wallet2.id,
            'amount': '500000',
            'fee': '5000',
            'description': 'Transfer to e-wallet'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifikasi bahwa transfer dibuat di database
        self.assertTrue(Transfer.objects.filter(amount=Decimal('500000')).exists())
        
        # Verifikasi bahwa saldo wallet terupdate
        self.wallet.refresh_from_db()
        self.wallet2.refresh_from_db()
        
        # Wallet 1: initial (1,000,000) + income (5,000,000) - transfer (500,000) - fee (5,000)
        self.assertEqual(self.wallet.current_balance, Decimal('5495000.00'))
        
        # Wallet 2: initial (100,000) + transfer (500,000)
        self.assertEqual(self.wallet2.current_balance, Decimal('600000.00'))


class TagApiTests(FinanceApiTestCase):
    def test_list_tags(self):
        url = reverse('tag-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Important')
    
    def test_create_tag(self):
        url = reverse('tag-list')
        data = {'name': 'Business'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Business')
        
        # Verifikasi bahwa tag dibuat di database
        self.assertTrue(Tag.objects.filter(name='Business').exists())
    
    def test_get_transactions_for_tag(self):
        # Tambahkan tag ke transaksi
        TransactionTag.objects.create(
            transaction=self.transaction,
            tag=self.tag
        )
        
        url = reverse('tag-transactions', args=[self.tag.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['description'], 'Monthly salary')


class PermissionTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'pass')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'pass')
        
        self.wallet_user1 = Wallet.objects.create(
            user=self.user1,
            name="User1 Wallet",
            wallet_type="bank"
        )
        
    def test_user_cannot_access_others_wallet(self):
        """Test IsOwner permission - user2 tidak bisa akses wallet user1"""
        self.client.force_authenticate(user=self.user2)
        
        # Try to access user1's wallet
        response = self.client.get(f'/api/v1/finance/wallets/{self.wallet_user1.id}/')
        
        # Should be 404 (karena get_queryset filter) atau 403 (kalau IsOwner kick in)
        self.assertIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN])