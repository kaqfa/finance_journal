# API Documentation - WealthWise (Updated Structure)

## Overview

**WealthWise** sekarang terdiri dari **4 modul utama** dengan API yang terstruktur modular:

1. **Master** - User management dan data master umum
2. **Finance** - Personal finance tracking ✅ **Production Ready**
3. **Invest** - Modern investment portfolio tracking 🚧 **In Development**
4. **Trading** - Advanced trading journal dengan analytics 🚧 **In Development**
5. ~~**Journal**~~ - ⚠️ **DEPRECATED** (reference only)

## API Base URL

All API endpoints are prefixed with `/api/v1/`

## Authentication

All endpoints require JWT authentication except explicitly mentioned otherwise.

---

## 🔐 Authentication Endpoints

| Method | Endpoint | Description | Status |
|--------|----------|-------------|---------|
| POST | `/api/v1/auth/register/` | Register new user | ✅ |
| POST | `/api/v1/auth/login/` | User login (JWT) | ✅ |
| POST | `/api/v1/auth/logout/` | User logout | ✅ |
| POST | `/api/v1/auth/token/refresh/` | Refresh JWT token | ✅ |
| POST | `/api/v1/auth/token/verify/` | Verify JWT token | ✅ |
| GET | `/api/v1/auth/profile/` | Get user profile | ✅ |
| PUT | `/api/v1/auth/profile/` | Update user profile | ✅ |
| POST | `/api/v1/auth/password/reset/` | Reset password | ✅ |
| PUT | `/api/v1/auth/password/change/` | Change password | ✅ |

---

## 💰 Finance Module Endpoints ✅ **Production Ready**

### Wallet Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/finance/wallets/` | List all user wallets |
| POST | `/api/v1/finance/wallets/` | Create new wallet |
| GET | `/api/v1/finance/wallets/{id}/` | Get wallet details |
| PUT | `/api/v1/finance/wallets/{id}/` | Update wallet |
| DELETE | `/api/v1/finance/wallets/{id}/` | Delete wallet |
| POST | `/api/v1/finance/wallets/{id}/recalculate/` | Recalculate wallet balance |

### Transaction Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/finance/transactions/` | List all transactions with filtering |
| POST | `/api/v1/finance/transactions/` | Create new transaction |
| GET | `/api/v1/finance/transactions/{id}/` | Get transaction details |
| PUT | `/api/v1/finance/transactions/{id}/` | Update transaction |
| DELETE | `/api/v1/finance/transactions/{id}/` | Delete transaction |
| GET | `/api/v1/finance/transactions/summary/` | Get transaction summary |
| GET | `/api/v1/finance/transactions/by_category/` | Get transactions grouped by category |
| GET | `/api/v1/finance/transactions/monthly_report/` | Get monthly financial report |

### Category Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/finance/categories/` | List all categories |
| POST | `/api/v1/finance/categories/` | Create new category |
| GET | `/api/v1/finance/categories/{id}/` | Get category details |
| PUT | `/api/v1/finance/categories/{id}/` | Update category |
| DELETE | `/api/v1/finance/categories/{id}/` | Delete category |
| GET | `/api/v1/finance/categories/income/` | Get income categories only |
| GET | `/api/v1/finance/categories/expense/` | Get expense categories only |

### Tag Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/finance/tags/` | List all tags |
| POST | `/api/v1/finance/tags/` | Create new tag |
| GET | `/api/v1/finance/tags/{id}/` | Get tag details |
| PUT | `/api/v1/finance/tags/{id}/` | Update tag |
| DELETE | `/api/v1/finance/tags/{id}/` | Delete tag |
| GET | `/api/v1/finance/tags/{id}/transactions/` | Get transactions for specific tag |

### Transfer Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/finance/transfers/` | List all transfers |
| POST | `/api/v1/finance/transfers/` | Create new transfer between wallets |
| GET | `/api/v1/finance/transfers/{id}/` | Get transfer details |
| PUT | `/api/v1/finance/transfers/{id}/` | Update transfer |
| DELETE | `/api/v1/finance/transfers/{id}/` | Delete transfer |

---

## 📈 Investment Module Endpoints 🚧 **In Development**

### Asset Management (Read-only initially)
| Method | Endpoint | Description | Status |
|--------|----------|-------------|---------|
| GET | `/api/v1/investments/assets/` | List all available assets | 📋 |
| GET | `/api/v1/investments/assets/{id}/` | Get asset details | 📋 |
| GET | `/api/v1/investments/assets/{id}/prices/` | Get asset price history | 📋 |
| GET | `/api/v1/investments/assets/search/` | Search assets by symbol/name | 📋 |

### Investment Portfolio Management
| Method | Endpoint | Description | Status |
|--------|----------|-------------|---------|
| GET | `/api/v1/investments/portfolios/` | List user investment portfolios | 📋 |
| POST | `/api/v1/investments/portfolios/` | Create new investment portfolio | 📋 |
| GET | `/api/v1/investments/portfolios/{id}/` | Get portfolio details with holdings | 📋 |
| PUT | `/api/v1/investments/portfolios/{id}/` | Update portfolio | 📋 |
| DELETE | `/api/v1/investments/portfolios/{id}/` | Delete portfolio | 📋 |
| GET | `/api/v1/investments/portfolios/{id}/performance/` | Get portfolio performance metrics | 📋 |
| GET | `/api/v1/investments/portfolios/{id}/allocation/` | Get asset allocation breakdown | 📋 |

### Investment Transaction Management
| Method | Endpoint | Description | Status |
|--------|----------|-------------|---------|
| GET | `/api/v1/investments/transactions/` | List investment transactions | 📋 |
| POST | `/api/v1/investments/transactions/` | Create new investment transaction | 📋 |
| GET | `/api/v1/investments/transactions/{id}/` | Get transaction details | 📋 |
| PUT | `/api/v1/investments/transactions/{id}/` | Update transaction | 📋 |
| DELETE | `/api/v1/investments/transactions/{id}/` | Delete transaction | 📋 |

### Holdings Management
| Method | Endpoint | Description | Status |
|--------|----------|-------------|---------|
| GET | `/api/v1/investments/holdings/` | List current holdings | 📋 |
| GET | `/api/v1/investments/holdings/{id}/` | Get holding details | 📋 |
| POST | `/api/v1/investments/holdings/refresh/` | Refresh holding values with current prices | 📋 |

---

## 📈 Trading Module Endpoints 🚧 **In Development**

### Trading Account Management
| Method | Endpoint | Description | Status |
|--------|----------|-------------|---------|
| GET | `/api/v1/trading/accounts/` | List trading accounts | 📋 |
| POST | `/api/v1/trading/accounts/` | Create new trading account | 📋 |
| GET | `/api/v1/trading/accounts/{id}/` | Get account details | 📋 |
| PUT | `/api/v1/trading/accounts/{id}/` | Update account | 📋 |
| DELETE | `/api/v1/trading/accounts/{id}/` | Delete account | 📋 |

### Trade Management
| Method | Endpoint | Description | Status |
|--------|----------|-------------|---------|
| GET | `/api/v1/trading/trades/` | List trades with advanced filtering | 📋 |
| POST | `/api/v1/trading/trades/` | Create new trade | 📋 |
| GET | `/api/v1/trading/trades/{id}/` | Get trade details | 📋 |
| PUT | `/api/v1/trading/trades/{id}/` | Update trade | 📋 |
| DELETE | `/api/v1/trading/trades/{id}/` | Delete trade | 📋 |

---

## 📊 Sample API Responses

### Finance Transaction List
```json
{
  "count": 25,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "wallet_name": "BCA Savings",
      "category_name": "Groceries",
      "amount": "150000.00",
      "type": "expense",
      "transaction_date": "2025-06-01",
      "description": "Weekly grocery shopping"
    }
  ]
}
```

### Investment Portfolio Detail
```json
{
  "id": "uuid-string",
  "name": "Growth Portfolio",
  "description": "Long-term growth focused portfolio",
  "initial_capital": "10000000.00",
  "current_value": "12500000.00",
  "total_return": "2500000.00",
  "total_return_percentage": "25.00",
  "risk_level": "medium",
  "holdings": [
    {
      "asset": {
        "symbol": "BBRI",
        "name": "Bank Rakyat Indonesia Tbk",
        "type": "stock"
      },
      "quantity": "1000.00000000",
      "average_price": "4500.00",
      "current_price": "4750.00",
      "unrealized_pnl": "250000.00"
    }
  ]
}
```

---

## 🔧 Development Status & Roadmap

### Current Implementation Status

#### ✅ **Completed (Production Ready)**
- **Master Module**: Custom User model dengan UUID
- **Finance Module**: Complete API dengan semua fitur
- **Authentication**: JWT dengan token blacklisting
- **API Documentation**: Swagger/OpenAPI integration

#### 🚧 **In Progress**
- **Investment Module**: Model design completed, API development ongoing
- **Database Migrations**: Implementing UUID migration strategy
- **Testing Suite**: Unit tests untuk Finance module

#### 📋 **Planned (Next Sprint)**
- **Investment API**: Complete CRUD operations
- **Asset Price Integration**: Real-time price feeds
- **Frontend Setup**: Next.js project initialization
- **CI/CD Pipeline**: GitHub Actions setup

---

## 🎯 Summary

Struktur API baru ini memberikan:

✅ **Modular Architecture** - Setiap module independen dengan API yang jelas  
✅ **Production Ready Finance** - Finance module siap untuk deployment  
✅ **Scalable Design** - Architecture yang bisa berkembang sesuai kebutuhan  
✅ **Modern Standards** - JWT auth, REST best practices, OpenAPI documentation  
✅ **Developer Friendly** - Comprehensive documentation dan testing tools  

**Next Steps:**
1. Selesaikan Investment Module API development
2. Implement comprehensive testing suite
3. Setup CI/CD pipeline untuk automated deployment
4. Begin frontend development dengan Finance module sebagai MVP
