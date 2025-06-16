# WealthWise API Reference

## 🔗 Base Information
- **Base URL**: `http://localhost:8000/api/v1/`
- **Authentication**: JWT Bearer Token
- **Format**: JSON

## 🔐 Authentication

### Headers
```
Authorization: Bearer <your_access_token>
Content-Type: application/json
```

### Endpoints
- `POST /auth/login/` - User login
- `POST /auth/register/` - User registration  
- `POST /auth/logout/` - User logout
- `POST /auth/token/refresh/` - Refresh access token
- `GET /auth/profile/` - Get user profile
- `PUT /auth/profile/` - Update user profile

## 💰 Finance Module

### Wallets

#### **GET /finance/wallets/**
List all user wallets with pagination.

**Query Parameters:**
- `page` (int): Page number
- `page_size` (int): Results per page
- `search` (string): Search term
- `ordering` (string): Sort field

**Response:**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/v1/finance/wallets/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Main Wallet",
      "wallet_type": "bank",
      "currency": "IDR",
      "initial_balance": "1000000.00",
      "current_balance": "1250000.00",
      "is_active": true,
      "created_at": "2025-01-01T10:00:00Z",
      "updated_at": "2025-01-01T10:00:00Z"
    }
  ]
}
```

#### **POST /finance/wallets/**
Create a new wallet.

**Request Body:**
```json
{
  "name": "Wallet Name",
  "wallet_type": "bank", // "cash", "bank", "ewallet", "credit", "other"
  "currency": "IDR",
  "initial_balance": "1000000.00",
  "is_active": true
}
```

#### **GET /finance/wallets/{id}/**
Get wallet details by ID.

#### **PUT /finance/wallets/{id}/**
Update wallet. **Note: initial_balance is read-only after creation**.

**Request Body:**
```json
{
  "name": "Updated Name",
  "wallet_type": "bank",
  "currency": "IDR",
  "is_active": true
}
```

#### **DELETE /finance/wallets/{id}/**
Delete wallet.

#### **GET /finance/wallets/choices/**
Get available wallet choices/options for forms.

**Query Parameters:**
- `search` (string): Search term
- `ordering` (string): Sort field  
- `page`, `page_size`: Pagination

**Response:**
```json
{
  "wallet_types": [
    {"key": "cash", "label": "Cash"},
    {"key": "bank", "label": "Bank Account"},
    {"key": "ewallet", "label": "E-Wallet"},
    {"key": "credit", "label": "Credit Card"},
    {"key": "other", "label": "Other"}
  ],
  "currencies": [
    {"key": "IDR", "label": "Indonesian Rupiah"},
    {"key": "USD", "label": "US Dollar"}
  ]
}
```

### Transactions

#### **GET /finance/transactions/**
List transactions with pagination.

**Query Parameters:**
- `page`, `page_size`, `search`, `ordering`
- `wallet` (int): Filter by wallet ID

**Response:**
```json
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "wallet": 1,
      "wallet_name": "Main Wallet",
      "category": 5,
      "category_name": "Food",
      "amount": "50000.00",
      "type": "expense", // "income", "expense", "transfer"
      "description": "Lunch",
      "transaction_date": "2025-01-01",
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z",
      "tags": [
        {"id": 1, "name": "daily"}
      ],
      "tag_ids": [1]
    }
  ]
}
```

#### **POST /finance/transactions/**
Create new transaction.

**Request Body:**
```json
{
  "wallet": 1,
  "category": 5, // optional
  "amount": "50000.00",
  "type": "expense",
  "description": "Transaction description",
  "transaction_date": "2025-01-01",
  "tag_ids": [1, 2] // optional
}
```

#### **GET /finance/transactions/{id}/**
Get transaction details.

#### **PUT /finance/transactions/{id}/**
Update transaction.

#### **DELETE /finance/transactions/{id}/**
Delete transaction.

#### **GET /finance/transactions/choices/**
Get available transaction choices/options for forms.

**Response:**
```json
{
  "transaction_types": [
    {"key": "income", "label": "Income"},
    {"key": "expense", "label": "Expense"},
    {"key": "transfer", "label": "Transfer"}
  ],
  "wallets": [
    {"id": 1, "name": "Main Wallet", "wallet_type": "bank"}
  ],
  "categories": [
    {"id": 1, "name": "Food", "type": "expense"}
  ],
  "tags": [
    {"id": 1, "name": "daily"}
  ]
}
```

### Special Transaction Endpoints

#### **GET /finance/transactions/summary/**
Get transaction summary (total income, expense, balance).

**Query Parameters:**
- `wallet` (int): Filter by wallet
- `start_date` (date): Start date filter
- `end_date` (date): End date filter

#### **GET /finance/transactions/by_category/**
Get transactions grouped by category with totals and percentages.

**Query Parameters:**
- `type` (string): "income" or "expense" (default: "expense")
- `wallet` (int): Filter by wallet
- `start_date` (date): Start date filter
- `end_date` (date): End date filter

#### **GET /finance/transactions/monthly_report/**
Get monthly report for income and expenses.

**Query Parameters:**
- `year` (int): Year for report (default: current year)
- `wallet` (int): Filter by wallet

### Categories

#### **GET /finance/categories/**
List all categories with pagination.

**Response:**
```json
{
  "count": 20,
  "results": [
    {
      "id": 1,
      "name": "Food",
      "type": "expense", // "income" or "expense"
      "icon": "🍔", // optional
      "color": "#ff5555", // optional
      "created_at": "2025-01-01T10:00:00Z",
      "updated_at": "2025-01-01T10:00:00Z"
    }
  ]
}
```

#### **POST /finance/categories/**
Create new category.

**Request Body:**
```json
{
  "name": "Category Name",
  "type": "expense",
  "icon": "🍔", // optional
  "color": "#ff5555" // optional
}
```

#### **GET /finance/categories/income/**
Get income categories only.

#### **GET /finance/categories/expense/**
Get expense categories only.

#### **PUT /finance/categories/{id}/**
Update category.

#### **DELETE /finance/categories/{id}/**
Delete category.

#### **GET /finance/categories/choices/**
Get available category choices/options for forms.

**Response:**
```json
{
  "category_types": [
    {"key": "income", "label": "Income"},
    {"key": "expense", "label": "Expense"}
  ],
  "icons": [
    {"key": "🍔", "label": "Food"},
    {"key": "🏠", "label": "Home"},
    {"key": "🚗", "label": "Transport"}
  ],
  "colors": [
    {"key": "#ff5555", "label": "Red"},
    {"key": "#55ff55", "label": "Green"},
    {"key": "#5555ff", "label": "Blue"}
  ]
}
```

### Tags

#### **GET /finance/tags/**
List all tags with pagination.

**Response:**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "name": "daily",
      "created_at": "2025-01-01T10:00:00Z"
    }
  ]
}
```

#### **POST /finance/tags/**
Create new tag.

**Request Body:**
```json
{
  "name": "tag-name"
}
```

#### **PUT /finance/tags/{id}/**
Update tag.

#### **DELETE /finance/tags/{id}/**
Delete tag.

#### **GET /finance/tags/{id}/transactions/**
Get all transactions with specific tag.

### Transfers

#### **GET /finance/transfers/**
List transfers with pagination.

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "from_wallet": 1,
      "from_wallet_name": "Main Wallet",
      "to_wallet": 2,
      "to_wallet_name": "Savings",
      "amount": "100000.00",
      "fee": "0.00",
      "transaction": 15, // auto-created transaction ID
      "transaction_date": "2025-01-01",
      "created_at": "2025-01-01T15:00:00Z",
      "updated_at": "2025-01-01T15:00:00Z"
    }
  ]
}
```

#### **POST /finance/transfers/**
Create new transfer between wallets.

**Request Body:**
```json
{
  "from_wallet": 1,
  "to_wallet": 2,
  "amount": "100000.00",
  "fee": "0.00", // optional
  "description": "Transfer description" // optional
}
```

## 📊 Investment Module

### Assets

#### **GET /invest/assets/**
List available assets for investment.

#### **GET /invest/assets/{id}/**
Get asset details including latest price.

### Portfolios

#### **GET /invest/portfolios/**
List investment portfolios.

#### **POST /invest/portfolios/**
Create new portfolio.

#### **GET /invest/portfolios/{id}/**
Get portfolio details with holdings and performance.

### Investment Transactions

#### **GET /invest/transactions/**
List investment transactions (buy, sell, dividend).

#### **POST /invest/transactions/**
Create investment transaction.

### Holdings

#### **GET /invest/holdings/**
List current holdings with P&L calculations.

### Choices Endpoints

#### **GET /invest/assets/choices/**
Get available asset choices for forms.

#### **GET /invest/portfolios/choices/**
Get available portfolio choices for forms.

#### **GET /invest/transactions/choices/**
Get available investment transaction choices for forms.

#### **GET /invest/holdings/choices/**
Get available holding choices for forms.

## 🎯 Data Schema Summary

### Key Field Notes:

#### Wallet Schema:
- `initial_balance`: **Read-only after creation** - cannot be updated via PUT/PATCH
- `current_balance`: **Always read-only** - calculated automatically
- `wallet_type`: Enum of "cash", "bank", "ewallet", "credit", "other"

#### Transaction Schema:
- `wallet_name`, `category_name`: **Read-only** - populated automatically
- `tag_ids`: Array of tag IDs for assignment
- `tags`: **Read-only** - populated automatically with full tag objects
- `type`: Enum of "income", "expense", "transfer"

#### Category Schema:
- `type`: Must be "income" or "expense"
- `icon`: Optional emoji or icon identifier
- `color`: Optional hex color code

## 🔄 Pagination Pattern

All list endpoints use consistent pagination:

```json
{
  "count": 100,           // Total items
  "next": "url",          // Next page URL or null
  "previous": "url",      // Previous page URL or null  
  "results": []           // Array of items
}
```

## ⚠️ Error Responses

```json
{
  "error": "Error message",
  "details": {
    "field_name": ["Field error message"]
  }
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `500`: Internal Server Error

---

*Last Updated: 2025-06-16*
*Generated from OpenAPI documentation at http://localhost:8000/api/v1/docs/*

## 📝 Update Notes

**2025-06-16**: Added missing `/choices` endpoints for all modules:
- `/finance/wallets/choices/` - Get wallet type and currency options
- `/finance/transactions/choices/` - Get transaction types, wallets, categories, tags
- `/finance/categories/choices/` - Get category types, icons, colors
- Investment module choices endpoints documented
- Created custom command `/update-api-docs` for automated updates