#!/bin/bash

# Quick API Testing Script
# Script untuk setup dan testing dasar API

echo "🚀 Journal Invest API Testing Setup"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo -e "${RED}❌ Error: manage.py not found. Please run this script from the Django project root directory.${NC}"
    exit 1
fi

echo -e "${BLUE}📁 Current directory: $(pwd)${NC}"

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠️  Warning: No virtual environment detected. Consider activating your venv.${NC}"
fi

# Check if Django is installed
python -c "import django" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Django not found. Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

echo -e "${GREEN}✅ Dependencies check complete${NC}"

# Run migrations
echo -e "${BLUE}📦 Running database migrations...${NC}"
python manage.py migrate

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Migrations completed successfully${NC}"
else
    echo -e "${RED}❌ Migration failed${NC}"
    exit 1
fi

# Check if superuser exists
echo -e "${BLUE}👤 Checking for superuser...${NC}"
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if User.objects.filter(is_superuser=True).exists():
    print('Superuser already exists')
    exit(0)
else:
    print('No superuser found')
    exit(1)
" 2>/dev/null

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}📝 Creating superuser for testing...${NC}"
    echo "Please create a superuser account (optional, for admin access):"
    python manage.py createsuperuser --noinput --username admin --email admin@test.com 2>/dev/null || true
fi

# Create test data
echo -e "${BLUE}🗃️  Creating test data...${NC}"
python manage.py shell << EOF
from django.contrib.auth import get_user_model
from invest.models import Asset
from finance.models import Category

User = get_user_model()

# Create test user if not exists
test_user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
)
if created:
    test_user.set_password('testpass123')
    test_user.save()
    print(f"✅ Created test user: {test_user.username}")
else:
    print(f"ℹ️  Test user already exists: {test_user.username}")

# Create sample assets
assets_data = [
    {'symbol': 'BBRI', 'name': 'Bank Rakyat Indonesia Tbk', 'type': 'stock', 'exchange': 'IDX', 'sector': 'Banking', 'currency': 'IDR'},
    {'symbol': 'BBCA', 'name': 'Bank Central Asia Tbk', 'type': 'stock', 'exchange': 'IDX', 'sector': 'Banking', 'currency': 'IDR'},
    {'symbol': 'BTC', 'name': 'Bitcoin', 'type': 'crypto', 'exchange': 'Binance', 'sector': 'Cryptocurrency', 'currency': 'USD'},
    {'symbol': 'ETH', 'name': 'Ethereum', 'type': 'crypto', 'exchange': 'Binance', 'sector': 'Cryptocurrency', 'currency': 'USD'},
]

for asset_data in assets_data:
    asset, created = Asset.objects.get_or_create(
        symbol=asset_data['symbol'],
        defaults=asset_data
    )
    if created:
        print(f"✅ Created asset: {asset.symbol}")
    else:
        print(f"ℹ️  Asset already exists: {asset.symbol}")

# Create sample categories for test user
categories_data = [
    {'name': 'Salary', 'type': 'income', 'icon': 'work', 'color': '#4CAF50'},
    {'name': 'Food & Dining', 'type': 'expense', 'icon': 'restaurant', 'color': '#FF9800'},
    {'name': 'Transportation', 'type': 'expense', 'icon': 'directions_car', 'color': '#2196F3'},
    {'name': 'Shopping', 'type': 'expense', 'icon': 'shopping_cart', 'color': '#E91E63'},
    {'name': 'Investment Income', 'type': 'income', 'icon': 'trending_up', 'color': '#8BC34A'},
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        user=test_user,
        name=cat_data['name'],
        defaults=cat_data
    )
    if created:
        print(f"✅ Created category: {category.name}")
    else:
        print(f"ℹ️  Category already exists: {category.name}")

print("🎉 Test data setup complete!")
EOF

echo -e "${GREEN}✅ Test data created successfully${NC}"

# Check server status
echo -e "${BLUE}🌐 Checking server status...${NC}"
python manage.py check

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Django project check passed${NC}"
else
    echo -e "${RED}❌ Django project check failed${NC}"
    exit 1
fi

# Display testing instructions
echo ""
echo -e "${GREEN}🎉 Setup Complete! Ready for API Testing${NC}"
echo "=========================================="
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Start the development server:"
echo "   ${YELLOW}python manage.py runserver${NC}"
echo ""
echo "2. Open VS Code and install REST Client extension if not installed:"
echo "   ${YELLOW}Name: REST Client (by Humao)${NC}"
echo ""
echo "3. Open the API test files:"
echo "   ${YELLOW}📁 api_test/finance_api.http${NC}"
echo "   ${YELLOW}📁 api_test/investment_api.http${NC}"
echo ""
echo "4. Start testing with authentication:"
echo "   - Register user (or use existing testuser/testpass123)"
echo "   - Login to get access token"
echo "   - Update @accessToken variable in test files"
echo ""
echo -e "${BLUE}📊 Available Test Endpoints:${NC}"
echo "• Finance API: http://localhost:8000/api/v1/finance/"
echo "• Investment API: http://localhost:8000/api/v1/invest/"
echo "• Auth API: http://localhost:8000/api/v1/auth/"
echo "• Admin Panel: http://localhost:8000/admin/"
echo "• API Docs: http://localhost:8000/api/docs/ (if configured)"
echo ""
echo -e "${BLUE}🔐 Test Credentials:${NC}"
echo "• Username: testuser"
echo "• Password: testpass123"
echo "• Email: test@example.com"
echo ""
echo -e "${GREEN}Happy Testing! 🚀${NC}"
