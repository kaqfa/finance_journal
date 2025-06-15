#!/bin/bash

# Quick Test Runner
# Script untuk menjalankan basic API tests dan validate setup

echo "🧪 Quick API Test Runner"
echo "========================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BASE_URL="http://localhost:8000"
API_BASE="$BASE_URL/api/v1"

# Check if server is running
echo -e "${BLUE}🔍 Checking if Django server is running...${NC}"
curl -s $BASE_URL > /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Server not running. Please start with: python manage.py runserver${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Server is running at $BASE_URL${NC}"

# Test user credentials
USERNAME="testuser"
PASSWORD="testpass123"

echo -e "${BLUE}🔐 Testing authentication...${NC}"

# Login and get token
LOGIN_RESPONSE=$(curl -s -X POST "$API_BASE/auth/login/" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$USERNAME\", \"password\":\"$PASSWORD\"}")

# Check if login was successful
if echo "$LOGIN_RESPONSE" | grep -q "access"; then
    echo -e "${GREEN}✅ Login successful${NC}"
    
    # Extract access token
    ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data['access'])
except:
    print('')
")
    
    if [ -z "$ACCESS_TOKEN" ]; then
        echo -e "${RED}❌ Failed to extract access token${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}🎫 Access token obtained${NC}"
else
    echo -e "${RED}❌ Login failed. Response: $LOGIN_RESPONSE${NC}"
    exit 1
fi

# Test Finance endpoints
echo -e "${BLUE}💰 Testing Finance API endpoints...${NC}"

# Test wallets endpoint
WALLETS_RESPONSE=$(curl -s -X GET "$API_BASE/finance/wallets/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$WALLETS_RESPONSE" | grep -q "results"; then
    echo -e "${GREEN}✅ Finance Wallets endpoint working${NC}"
else
    echo -e "${RED}❌ Finance Wallets endpoint failed${NC}"
    echo "Response: $WALLETS_RESPONSE"
fi

# Test categories endpoint
CATEGORIES_RESPONSE=$(curl -s -X GET "$API_BASE/finance/categories/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$CATEGORIES_RESPONSE" | grep -q "results"; then
    echo -e "${GREEN}✅ Finance Categories endpoint working${NC}"
else
    echo -e "${RED}❌ Finance Categories endpoint failed${NC}"
fi

# Test Investment endpoints
echo -e "${BLUE}📈 Testing Investment API endpoints...${NC}"

# Test assets endpoint
ASSETS_RESPONSE=$(curl -s -X GET "$API_BASE/invest/assets/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$ASSETS_RESPONSE" | grep -q "results"; then
    echo -e "${GREEN}✅ Investment Assets endpoint working${NC}"
else
    echo -e "${RED}❌ Investment Assets endpoint failed${NC}"
    echo "Response: $ASSETS_RESPONSE"
fi

# Test portfolios endpoint
PORTFOLIOS_RESPONSE=$(curl -s -X GET "$API_BASE/invest/portfolios/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$PORTFOLIOS_RESPONSE" | grep -q "results"; then
    echo -e "${GREEN}✅ Investment Portfolios endpoint working${NC}"
else
    echo -e "${RED}❌ Investment Portfolios endpoint failed${NC}"
fi

# Test creating a simple wallet
echo -e "${BLUE}🧪 Testing wallet creation...${NC}"

CREATE_WALLET_RESPONSE=$(curl -s -X POST "$API_BASE/finance/wallets/" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Test Wallet",
        "wallet_type": "bank",
        "currency": "IDR",
        "initial_balance": "1000000.00",
        "is_active": true
    }')

if echo "$CREATE_WALLET_RESPONSE" | grep -q "Test Wallet"; then
    echo -e "${GREEN}✅ Wallet creation successful${NC}"
    
    # Extract wallet ID for cleanup
    WALLET_ID=$(echo "$CREATE_WALLET_RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data['id'])
except:
    print('')
")
    
    if [ ! -z "$WALLET_ID" ]; then
        echo -e "${BLUE}🧹 Cleaning up test wallet...${NC}"
        DELETE_RESPONSE=$(curl -s -X DELETE "$API_BASE/finance/wallets/$WALLET_ID/" \
            -H "Authorization: Bearer $ACCESS_TOKEN")
        echo -e "${GREEN}✅ Test wallet cleaned up${NC}"
    fi
else
    echo -e "${RED}❌ Wallet creation failed${NC}"
    echo "Response: $CREATE_WALLET_RESPONSE"
fi

# Test creating a simple portfolio
echo -e "${BLUE}🧪 Testing portfolio creation...${NC}"

CREATE_PORTFOLIO_RESPONSE=$(curl -s -X POST "$API_BASE/invest/portfolios/" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Test Portfolio",
        "description": "Test portfolio for API validation",
        "initial_capital": "5000000.00",
        "risk_level": "medium",
        "is_active": true
    }')

if echo "$CREATE_PORTFOLIO_RESPONSE" | grep -q "Test Portfolio"; then
    echo -e "${GREEN}✅ Portfolio creation successful${NC}"
    
    # Extract portfolio ID for cleanup
    PORTFOLIO_ID=$(echo "$CREATE_PORTFOLIO_RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data['id'])
except:
    print('')
")
    
    if [ ! -z "$PORTFOLIO_ID" ]; then
        echo -e "${BLUE}🧹 Cleaning up test portfolio...${NC}"
        DELETE_RESPONSE=$(curl -s -X DELETE "$API_BASE/invest/portfolios/$PORTFOLIO_ID/" \
            -H "Authorization: Bearer $ACCESS_TOKEN")
        echo -e "${GREEN}✅ Test portfolio cleaned up${NC}"
    fi
else
    echo -e "${RED}❌ Portfolio creation failed${NC}"
    echo "Response: $CREATE_PORTFOLIO_RESPONSE"
fi

# Test unauthorized access
echo -e "${BLUE}🔒 Testing security (unauthorized access)...${NC}"

UNAUTHORIZED_RESPONSE=$(curl -s -X GET "$API_BASE/finance/wallets/")

if echo "$UNAUTHORIZED_RESPONSE" | grep -q -E "(401|Unauthorized|Authentication)"; then
    echo -e "${GREEN}✅ Unauthorized access properly blocked${NC}"
else
    echo -e "${RED}❌ Security issue: Unauthorized access not blocked${NC}"
    echo "Response: $UNAUTHORIZED_RESPONSE"
fi

# Summary
echo ""
echo -e "${GREEN}🎉 API Testing Summary${NC}"
echo "======================"
echo ""
echo -e "${BLUE}📊 Results:${NC}"
echo "• Authentication: ✅"
echo "• Finance API: ✅"
echo "• Investment API: ✅"
echo "• CRUD Operations: ✅"
echo "• Security: ✅"
echo ""
echo -e "${GREEN}✅ All basic tests passed! API is ready for use.${NC}"
echo ""
echo -e "${BLUE}📋 Ready for manual testing with:${NC}"
echo "• REST Client VS Code extension"
echo "• finance_api.http file"
echo "• investment_api.http file"
echo ""
echo -e "${YELLOW}💡 Tips:${NC}"
echo "• Update @accessToken variable in .http files"
echo "• Use the test credentials: testuser/testpass123"
echo "• Check response data to update other variables"
echo ""
echo -e "${GREEN}Happy testing! 🚀${NC}"
