# WealthWise API Reference for Frontend Development

## Base Configuration
- **Base URL**: `http://127.0.0.1:8000/api/v1`
- **Authentication**: Bearer JWT token in Authorization header
- **Content-Type**: `application/json`
- **Full API Docs**: Available at `http://127.0.0.1:8000/api/docs/`

## Authentication Endpoints

### Login
```typescript
POST /auth/login/
Request: {
  username: string;
  password: string;
}
Response: {
  access: string;
  refresh: string;
  user: {
    id: string;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
  }
}
```

### Logout
```typescript
POST /auth/logout/
Request: {
  refresh: string;
}
```

### Profile
```typescript
GET /auth/profile/
Response: User

PUT /auth/profile/
Request: Partial<User>
Response: User
```

### Token Refresh
```typescript
POST /auth/token/refresh/
Request: {
  refresh: string;
}
Response: {
  access: string;
}
```

---

## Finance Module Endpoints (✅ Production Ready)

### Wallets
```typescript
// List wallets
GET /finance/wallets/
Query: {
  page?: number;
  page_size?: number;
  search?: string;
  ordering?: string;
}
Response: PaginatedResponse<WalletList[]>

// Create wallet
POST /finance/wallets/
Request: {
  name: string;
  wallet_type: 'cash' | 'bank' | 'ewallet' | 'credit' | 'other';
  currency: string;
  initial_balance: string;
  is_active?: boolean;
}
Response: Wallet

// Get wallet detail
GET /finance/wallets/{id}/
Response: Wallet

// Get choices on wallet
GET /finance/wallets/choices/
Response: JSON

// Update wallet
PUT /finance/wallets/{id}/
Request: Partial<Wallet>
Response: Wallet

// Delete wallet
DELETE /finance/wallets/{id}/

// Recalculate wallet balance
POST /finance/wallets/{id}/recalculate/
Response: Wallet
```

### Transactions
```typescript
// List transactions
GET /finance/transactions/
Query: {
  page?: number;
  page_size?: number;
  search?: string;
  ordering?: string;
  wallet?: number;
  category?: number;
  type?: 'income' | 'expense' | 'transfer';
  start_date?: string;
  end_date?: string;
}
Response: PaginatedResponse<TransactionList[]>

// Create transaction
POST /finance/transactions/
Request: {
  wallet: number;
  amount: string;
  type: 'income' | 'expense' | 'transfer';
  category?: number;
  description?: string;
  transaction_date: string; // YYYY-MM-DD
  tag_ids?: number[];
}
Response: Transaction

// Get transaction detail
GET /finance/transactions/{id}/
Response: Transaction

// Update transaction
PUT /finance/transactions/{id}/
Request: Partial<Transaction>
Response: Transaction

// Delete transaction
DELETE /finance/transactions/{id}/

// Transaction summary
GET /finance/transactions/summary/
Query: {
  wallet?: number;
  start_date?: string;
  end_date?: string;
}
Response: {
  total_income: string;
  total_expense: string;
  net_balance: string;
}

// Transactions by category
GET /finance/transactions/by_category/
Query: {
  type?: 'income' | 'expense';
  wallet?: number;
  start_date?: string;
  end_date?: string;
}
Response: CategorySummary[]

// Monthly report
GET /finance/transactions/monthly_report/
Query: {
  year?: number;
  wallet?: number;
}
Response: MonthlyReport[]
```

### Categories
```typescript
// List categories
GET /finance/categories/
Response: PaginatedResponse<Category[]>

// Create category
POST /finance/categories/
Request: {
  name: string;
  type: 'income' | 'expense';
  icon?: string;
  color?: string;
}
Response: Category

// Get category detail
GET /finance/categories/{id}/
Response: Category

// Update category
PUT /finance/categories/{id}/
Request: Partial<Category>
Response: Category

// Delete category
DELETE /finance/categories/{id}/

// Income categories only
GET /finance/categories/income/
Response: PaginatedResponse<Category[]>

// Expense categories only
GET /finance/categories/expense/
Response: PaginatedResponse<Category[]>
```

### Tags
```typescript
// List tags
GET /finance/tags/
Response: PaginatedResponse<Tag[]>

// Create tag
POST /finance/tags/
Request: {
  name: string;
}
Response: Tag

// Get tag detail
GET /finance/tags/{id}/
Response: Tag

// Update tag
PUT /finance/tags/{id}/
Request: Partial<Tag>
Response: Tag

// Delete tag
DELETE /finance/tags/{id}/

// Get transactions for tag
GET /finance/tags/{id}/transactions/
Response: PaginatedResponse<Transaction[]>
```

### Transfers
```typescript
// List transfers
GET /finance/transfers/
Response: PaginatedResponse<Transfer[]>

// Create transfer
POST /finance/transfers/
Request: {
  from_wallet: number;
  to_wallet: number;
  amount: string;
  fee?: string;
  description?: string;
}
Response: Transfer

// Get transfer detail
GET /finance/transfers/{id}/
Response: Transfer

// Update transfer
PUT /finance/transfers/{id}/
Request: Partial<Transfer>
Response: Transfer

// Delete transfer
DELETE /finance/transfers/{id}/
```

---

## Investment Module Endpoints (🚧 In Development)

### Assets
```typescript
// List assets
GET /invest/assets/
Query: {
  search?: string;
  type?: 'stock' | 'crypto' | 'bond' | 'reit' | 'mutual_fund';
  exchange?: string;
  sector?: string;
}
Response: PaginatedResponse<AssetList[]>

// Get asset detail
GET /invest/assets/{id}/
Response: Asset

// Asset search (for autocomplete)
GET /invest/assets/search/
Query: {
  q: string;
  limit?: number;
}
Response: AssetSearch[]

// Asset price history
GET /invest/assets/{id}/prices/
Query: {
  days?: number;
  interval?: 'daily' | 'weekly' | 'monthly';
}
Response: AssetPrice[]
```

### Investment Portfolios
```typescript
// List portfolios
GET /invest/portfolios/
Response: PaginatedResponse<InvestmentPortfolioList[]>

// Create portfolio
POST /invest/portfolios/
Request: {
  name: string;
  description?: string;
  initial_capital: string;
  risk_level: 'low' | 'medium' | 'high';
  target_allocation?: object;
}
Response: InvestmentPortfolio

// Get portfolio detail
GET /invest/portfolios/{id}/
Response: InvestmentPortfolio

// Portfolio performance
GET /invest/portfolios/{id}/performance/
Query: {
  period?: '1M' | '3M' | '6M' | '1Y' | 'YTD' | 'ALL';
}
Response: PortfolioPerformance

// Portfolio allocation
GET /invest/portfolios/{id}/allocation/
Response: AllocationBreakdown
```

### Investment Transactions
```typescript
// List investment transactions
GET /invest/transactions/
Query: {
  portfolio?: string;
  asset?: string;
  transaction_type?: 'buy' | 'sell' | 'dividend' | 'split' | 'bonus';
  start_date?: string;
  end_date?: string;
}
Response: PaginatedResponse<InvestmentTransactionList[]>

// Create investment transaction
POST /invest/transactions/
Request: {
  portfolio_id: string;
  asset_id: string;
  transaction_type: 'buy' | 'sell' | 'dividend' | 'split' | 'bonus';
  quantity: string;
  price: string;
  transaction_date: string;
  fees?: string;
  notes?: string;
}
Response: InvestmentTransaction
```

### Holdings
```typescript
// List holdings
GET /invest/holdings/
Query: {
  portfolio?: string;
  asset?: string;
}
Response: PaginatedResponse<InvestmentHoldingList[]>

// Holdings analytics
GET /invest/holdings/analytics/
Response: HoldingsAnalytics

// Holdings by portfolio
GET /invest/holdings/by_portfolio/
Response: PortfolioHoldings[]

// Holdings performance
GET /invest/holdings/performance/
Query: {
  period?: '1M' | '3M' | '6M' | '1Y' | 'ALL';
}
Response: HoldingsPerformance

// Refresh holdings with current prices
POST /invest/holdings/refresh/
Request: {
  portfolio_ids?: string[];
  force_update?: boolean;
}
Response: RefreshResult
```

---

## TypeScript Types

### Common Types
```typescript
interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  phone?: string;
  date_joined: string;
}
```

### Finance Types
```typescript
interface Wallet {
  id: number;
  name: string;
  wallet_type: 'cash' | 'bank' | 'ewallet' | 'credit' | 'other';
  currency: string;
  initial_balance: string;
  current_balance: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface WalletList {
  id: number;
  name: string;
  wallet_type: 'cash' | 'bank' | 'ewallet' | 'credit' | 'other';
  currency: string;
  current_balance: string;
  is_active: boolean;
}

interface Transaction {
  id: number;
  wallet: number;
  wallet_name: string;
  category?: number;
  category_name: string;
  amount: string;
  type: 'income' | 'expense' | 'transfer';
  description?: string;
  transaction_date: string;
  created_at: string;
  updated_at: string;
  tag_ids: number[];
}

interface TransactionList {
  id: number;
  wallet_name: string;
  category_name: string;
  amount: string;
  type: 'income' | 'expense' | 'transfer';
  transaction_date: string;
  description?: string;
}

interface Category {
  id: number;
  name: string;
  type: 'income' | 'expense';
  icon?: string;
  color?: string;
  created_at: string;
  updated_at: string;
}

interface Tag {
  id: number;
  name: string;
  created_at: string;
}

interface Transfer {
  id: number;
  from_wallet: number;
  from_wallet_name: string;
  to_wallet: number;
  to_wallet_name: string;
  amount: string;
  fee: string;
  transaction_date: string;
  created_at: string;
  updated_at: string;
}
```

### Investment Types
```typescript
interface Asset {
  id: string;
  symbol: string;
  name: string;
  type: 'stock' | 'crypto' | 'bond' | 'reit' | 'mutual_fund';
  exchange?: string;
  sector?: string;
  currency: string;
  is_active: boolean;
  latest_price?: string;
  price_change_24h?: string;
}

interface InvestmentPortfolio {
  id: string;
  name: string;
  description?: string;
  initial_capital: string;
  risk_level: 'low' | 'medium' | 'high';
  is_active: boolean;
  created_at: string;
  total_value?: string;
  total_pnl?: string;
  total_pnl_percentage?: string;
}

interface InvestmentTransaction {
  id: string;
  portfolio_id: string;
  portfolio_name: string;
  asset: Asset;
  asset_id: string;
  transaction_type: 'buy' | 'sell' | 'dividend' | 'split' | 'bonus';
  quantity: string;
  price: string;
  total_amount: string;
  fees: string;
  transaction_date: string;
  notes?: string;
  created_at: string;
}

interface InvestmentHolding {
  id: string;
  portfolio_name: string;
  asset_symbol: string;
  asset_name: string;
  quantity: string;
  average_price: string;
  current_price: string;
  current_value: string;
  unrealized_pnl: string;
  unrealized_pnl_percentage: string;
  last_updated: string;
}
```

---

## Error Handling

### Standard Error Responses
```typescript
interface APIError {
  error?: string;
  detail?: string;
  non_field_errors?: string[];
  [field: string]: string[] | string | undefined;
}

// Common HTTP Status Codes
// 200 - Success
// 201 - Created
// 400 - Bad Request (validation errors)
// 401 - Unauthorized (auth required)
// 403 - Forbidden (permission denied)
// 404 - Not Found
// 500 - Internal Server Error
```

---

## Usage Examples

### Authentication Flow
```typescript
// Login
const loginResponse = await fetch('/api/v1/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'user@example.com',
    password: 'password123'
  })
});

const { access, refresh, user } = await loginResponse.json();

// Use access token for API calls
const apiResponse = await fetch('/api/v1/finance/wallets/', {
  headers: {
    'Authorization': `Bearer ${access}`,
    'Content-Type': 'application/json'
  }
});
```

### Creating a Transaction
```typescript
const transaction = await fetch('/api/v1/finance/transactions/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    wallet: 1,
    amount: "150000.00",
    type: "expense",
    category: 5,
    description: "Weekly groceries",
    transaction_date: "2025-06-01",
    tag_ids: [1, 3]
  })
});
```

---

## Notes for Claude Code
- All endpoints require Bearer token except auth endpoints
- Use proper TypeScript types for all API calls
- Implement proper error handling for all requests
- Finance module is production-ready, Investment module is in development
- Base URL should be configurable via environment variables
- Always include proper loading and error states in components