# Database Schema Documentation - WealthWise

## Database Schema Overview

WealthWise menggunakan PostgreSQL sebagai database utama dengan struktur yang mendukung 4 modul utama:
- **Authentication & User Management**
- **Finance Module** 
- **Investment Module**
- **Trading Module** (planned)

## Core Tables

### Authentication & User Management

#### `auth_user` (Django Default User Extended)
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| username | VARCHAR(150) | Unique username |
| email | VARCHAR(254) | User email |
| first_name | VARCHAR(150) | First name |
| last_name | VARCHAR(150) | Last name |
| password | VARCHAR(128) | Hashed password |
| is_active | BOOLEAN | Account status |
| date_joined | TIMESTAMP | Registration date |

---

## Finance Module Tables

### `finance_wallet`
Represents user's financial accounts (bank accounts, e-wallets, cash, etc.)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique wallet ID |
| user_id | UUID | FOREIGN KEY → auth_user.id | Wallet owner |
| name | VARCHAR(100) | NOT NULL | Wallet name |
| wallet_type | VARCHAR(10) | NOT NULL | Type: cash, bank, ewallet, credit, other |
| currency | VARCHAR(5) | DEFAULT 'IDR' | Currency code |
| initial_balance | DECIMAL(10,5) | DEFAULT 0 | Starting balance |
| current_balance | DECIMAL(10,5) | DEFAULT 0 | Current balance (auto-calculated) |
| is_active | BOOLEAN | DEFAULT TRUE | Wallet status |
| created_at | TIMESTAMP | AUTO | Creation timestamp |
| updated_at | TIMESTAMP | AUTO | Last update timestamp |

**Indexes:**
- `UNIQUE(user_id, name)` - User cannot have duplicate wallet names
- `INDEX(user_id)` - Fast user wallet lookup

### `finance_category`
Transaction categories for income/expense classification

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique category ID |
| user_id | UUID | FOREIGN KEY → auth_user.id | Category owner |
| name | VARCHAR(100) | NOT NULL | Category name |
| type | VARCHAR(10) | NOT NULL | Type: income, expense |
| icon | VARCHAR(50) | NULL | Icon identifier |
| color | VARCHAR(20) | NULL | Color code |
| created_at | TIMESTAMP | AUTO | Creation timestamp |
| updated_at | TIMESTAMP | AUTO | Last update timestamp |

**Indexes:**
- `UNIQUE(user_id, name)` - User cannot have duplicate category names
- `INDEX(user_id, type)` - Fast category filtering

### `finance_tag`
Flexible tagging system for transactions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique tag ID |
| user_id | UUID | FOREIGN KEY → auth_user.id | Tag owner |
| name | VARCHAR(50) | NOT NULL | Tag name |
| created_at | TIMESTAMP | AUTO | Creation timestamp |

**Indexes:**
- `UNIQUE(user_id, name)` - User cannot have duplicate tag names

### `finance_transaction`
Financial transactions (income, expense, transfer)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique transaction ID |
| user_id | UUID | FOREIGN KEY → auth_user.id | Transaction owner |
| wallet_id | INTEGER | FOREIGN KEY → finance_wallet.id | Associated wallet |
| category_id | INTEGER | FOREIGN KEY → finance_category.id, NULL | Transaction category |
| amount | DECIMAL(10,5) | NOT NULL | Transaction amount |
| type | VARCHAR(10) | NOT NULL | Type: income, expense, transfer |
| description | TEXT | NULL | Transaction description |
| transaction_date | DATE | NOT NULL | Transaction date |
| created_at | TIMESTAMP | AUTO | Creation timestamp |
| updated_at | TIMESTAMP | AUTO | Last update timestamp |

**Indexes:**
- `INDEX(user_id, transaction_date)` - Fast date-based queries
- `INDEX(wallet_id)` - Fast wallet transaction lookup
- `INDEX(category_id)` - Fast category filtering

### `finance_transactiontag` (Many-to-Many)
Links transactions to tags

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique link ID |
| transaction_id | INTEGER | FOREIGN KEY → finance_transaction.id | Transaction reference |
| tag_id | INTEGER | FOREIGN KEY → finance_tag.id | Tag reference |

**Indexes:**
- `UNIQUE(transaction_id, tag_id)` - Prevent duplicate tag assignments

### `finance_transfer`
Transfer details between wallets

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique transfer ID |
| transaction_id | INTEGER | FOREIGN KEY → finance_transaction.id | Base transaction |
| from_wallet_id | INTEGER | FOREIGN KEY → finance_wallet.id | Source wallet |
| to_wallet_id | INTEGER | FOREIGN KEY → finance_wallet.id | Destination wallet |
| amount | DECIMAL(10,5) | NOT NULL | Transfer amount |
| fee | DECIMAL(10,5) | DEFAULT 0 | Transfer fee |
| created_at | TIMESTAMP | AUTO | Creation timestamp |
| updated_at | TIMESTAMP | AUTO | Last update timestamp |

---

## Investment Module Tables

### `invest_asset`
Master data for investment assets (stocks, crypto, bonds, etc.)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique asset ID |
| symbol | VARCHAR(20) | NOT NULL, UNIQUE | Asset symbol (e.g., BBRI, BTC) |
| name | VARCHAR(255) | NOT NULL | Asset full name |
| type | VARCHAR(20) | NOT NULL | Type: stock, crypto, bond, reit, mutual_fund |
| exchange | VARCHAR(50) | NULL | Exchange name |
| sector | VARCHAR(100) | NULL | Business sector |
| currency | VARCHAR(3) | DEFAULT 'IDR' | Trading currency |
| is_active | BOOLEAN | DEFAULT TRUE | Asset status |
| created_at | TIMESTAMP | AUTO | Creation timestamp |

**Indexes:**
- `UNIQUE(symbol)` - Prevent duplicate symbols
- `INDEX(type)` - Fast type filtering
- `INDEX(exchange)` - Fast exchange filtering

### `invest_assetprice`
Historical price data for assets

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique price record ID |
| asset_id | UUID | FOREIGN KEY → invest_asset.id | Asset reference |
| price | DECIMAL(10,5) | NOT NULL | Asset price |
| volume | DECIMAL(15,5) | NULL | Trading volume |
| market_cap | DECIMAL(20,5) | NULL | Market capitalization |
| timestamp | TIMESTAMP | NOT NULL | Price timestamp |
| source | VARCHAR(50) | NULL | Data source |

**Indexes:**
- `INDEX(asset_id, timestamp DESC)` - Fast price history queries
- `UNIQUE(asset_id, timestamp, source)` - Prevent duplicate price records

### `invest_portfolio`
Investment portfolios

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique portfolio ID |
| user_id | UUID | FOREIGN KEY → auth_user.id | Portfolio owner |
| name | VARCHAR(255) | NOT NULL | Portfolio name |
| description | TEXT | NULL | Portfolio description |
| initial_capital | DECIMAL(15,5) | DEFAULT 0 | Initial investment |
| target_allocation | JSONB | NULL | Target asset allocation |
| risk_level | VARCHAR(10) | DEFAULT 'medium' | Risk level: low, medium, high |
| is_active | BOOLEAN | DEFAULT TRUE | Portfolio status |
| created_at | TIMESTAMP | AUTO | Creation timestamp |
| updated_at | TIMESTAMP | AUTO | Last update timestamp |

**Indexes:**
- `INDEX(user_id)` - Fast user portfolio lookup
- `INDEX(user_id, is_active)` - Fast active portfolio filtering

### `invest_transaction`
Investment transactions (buy, sell, dividend, etc.)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique transaction ID |
| portfolio_id | UUID | FOREIGN KEY → invest_portfolio.id | Portfolio reference |
| asset_id | UUID | FOREIGN KEY → invest_asset.id | Asset reference |
| transaction_type | VARCHAR(20) | NOT NULL | Type: buy, sell, dividend, split, bonus |
| quantity | DECIMAL(15,8) | NOT NULL | Number of shares/units |
| price | DECIMAL(10,5) | NOT NULL | Price per unit |
| fees | DECIMAL(10,5) | DEFAULT 0 | Transaction fees |
| transaction_date | DATE | NOT NULL | Transaction date |
| broker | VARCHAR(100) | NULL | Broker name |
| notes | TEXT | NULL | Transaction notes |
| created_at | TIMESTAMP | AUTO | Creation timestamp |

**Indexes:**
- `INDEX(portfolio_id, transaction_date DESC)` - Fast portfolio transaction history
- `INDEX(asset_id)` - Fast asset transaction lookup

### `invest_holding`
Current asset holdings in portfolios (auto-calculated)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique holding ID |
| portfolio_id | UUID | FOREIGN KEY → invest_portfolio.id | Portfolio reference |
| asset_id | UUID | FOREIGN KEY → invest_asset.id | Asset reference |
| quantity | DECIMAL(15,8) | NOT NULL | Current quantity owned |
| average_price | DECIMAL(10,5) | NOT NULL | Average purchase price |
| total_cost | DECIMAL(15,5) | NOT NULL | Total amount invested |
| current_price | DECIMAL(10,5) | NULL | Latest market price |
| current_value | DECIMAL(15,5) | NULL | Current market value |
| unrealized_pnl | DECIMAL(15,5) | NULL | Unrealized profit/loss |
| last_updated | TIMESTAMP | AUTO | Last price update |

**Indexes:**
- `UNIQUE(portfolio_id, asset_id)` - One holding per asset per portfolio
- `INDEX(portfolio_id)` - Fast portfolio holdings lookup

---

## Database Relationships

### Finance Module Relationships
```
auth_user (1) ←→ (M) finance_wallet
auth_user (1) ←→ (M) finance_category
auth_user (1) ←→ (M) finance_tag
auth_user (1) ←→ (M) finance_transaction

finance_wallet (1) ←→ (M) finance_transaction
finance_category (1) ←→ (M) finance_transaction
finance_transaction (M) ←→ (M) finance_tag [through finance_transactiontag]
finance_transaction (1) ←→ (1) finance_transfer
```

### Investment Module Relationships
```
auth_user (1) ←→ (M) invest_portfolio
invest_asset (1) ←→ (M) invest_assetprice
invest_asset (1) ←→ (M) invest_transaction
invest_asset (1) ←→ (M) invest_holding

invest_portfolio (1) ←→ (M) invest_transaction
invest_portfolio (1) ←→ (M) invest_holding
```

---

## Database Triggers & Constraints

### Finance Module Triggers
1. **Wallet Balance Update**: Automatically update `finance_wallet.current_balance` when transactions are added/modified/deleted
2. **Transfer Validation**: Ensure `from_wallet` and `to_wallet` belong to same user
3. **Transaction Type Validation**: Ensure transaction type matches category type

### Investment Module Triggers
1. **Holdings Calculation**: Automatically update `invest_holding` when `invest_transaction` changes
2. **Portfolio Metrics**: Update portfolio total value and P&L when holdings change
3. **Price Update**: Update holding current values when asset prices change

---

## Performance Optimization

### Indexing Strategy
- **Heavy Read Operations**: All user-scoped queries have user_id indexes
- **Date Range Queries**: Composite indexes on (user_id, date) fields
- **Category/Type Filtering**: Indexes on frequently filtered enum fields
- **Foreign Key Performance**: All foreign keys have corresponding indexes

### Partitioning (Future)
- **Transaction Tables**: Partition by date (monthly) for large datasets
- **Price History**: Partition by asset type and date range
- **Audit Logs**: Time-based partitioning for historical data

### Query Optimization
- **Eager Loading**: Use select_related/prefetch_related for related objects
- **Aggregate Queries**: Use database aggregation for summary statistics
- **Cached Calculations**: Store frequently calculated values (balances, totals)

---

## Data Migration Strategy

### Phase 1: Core Setup
1. Create base user and finance tables
2. Migrate existing financial data (if any)
3. Setup initial categories and default data

### Phase 2: Investment Setup
1. Create investment module tables
2. Import asset master data
3. Setup price history collection

### Phase 3: Advanced Features
1. Add trading module tables
2. Implement real-time price updates
3. Add analytics and reporting tables

---

## Backup & Recovery

### Backup Strategy
- **Daily Backups**: Automated daily database backups
- **Transaction Logs**: Continuous transaction log backups
- **Point-in-Time Recovery**: 30-day point-in-time recovery capability

### Data Retention
- **Transaction Data**: Permanent retention
- **Price History**: 5-year rolling window
- **Audit Logs**: 2-year retention
- **User Sessions**: 30-day retention

---

*Last Updated: 2025-06-14*
*Database Version: PostgreSQL 13+*
