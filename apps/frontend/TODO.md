# WealthWise Frontend - Todo List

## Current Status
- ✅ Next.js 15 setup with TypeScript
- ✅ HeroUI component library
- ✅ Auth flow (login page + AuthContext)
- ✅ Basic routing structure
- 🚧 Content pages need implementation

## Immediate Tasks (Week 1-2)

### Finance Module Implementation
- [ ] **Wallet Management**
  - [ ] `/finance/wallets` - List page with HeroUI cards
  - [ ] `/finance/wallets/new` - Create wallet form
  - [ ] `/finance/wallets/[id]` - Wallet detail + transactions
  - [ ] `/finance/wallets/[id]/edit` - Edit wallet form
  
- [ ] **Transaction Management**
  - [ ] `/finance/transactions` - List with filtering
  - [ ] `/finance/transactions/new` - Add transaction form
  - [ ] `/finance/transactions/[id]/edit` - Edit transaction
  - [ ] Transaction search & filter components
  
- [ ] **Categories & Tags**
  - [ ] `/finance/categories` - Category management
  - [ ] `/finance/tags` - Tag management
  - [ ] Category/tag selection components

### Dashboard Enhancement (Week 3-4)
- [ ] **Overview Cards**
  - [ ] Total balance card
  - [ ] Monthly income/expense cards
  - [ ] Recent transactions widget
  
- [ ] **Charts & Analytics**
  - [ ] Monthly spending chart (Recharts)
  - [ ] Category breakdown pie chart
  - [ ] Income vs expense trend

### State Management
- [ ] **Zustand Stores**
  - [ ] Finance store (wallets, transactions, categories)
  - [ ] Auth store improvement
  - [ ] UI state store (loading, errors)
  
- [ ] **API Integration**
  - [ ] Enhanced axios interceptors
  - [ ] Error handling improvement
  - [ ] Loading states standardization

## Component Architecture
- [ ] **Reusable Components**
  - [ ] WalletCard component
  - [ ] TransactionList component
  - [ ] CategorySelector component
  - [ ] DateRangePicker component
  
- [ ] **Form Components**
  - [ ] WalletForm (create/edit)
  - [ ] TransactionForm (create/edit)
  - [ ] TransferForm (between wallets)

## Mobile Optimization
- [ ] Responsive layouts for all pages
- [ ] Touch-friendly interactions
- [ ] Mobile navigation improvements

## Investment Module (Week 5-6)
- [ ] **Portfolio Management**
  - [ ] Portfolio list and detail pages
  - [ ] Add/edit portfolio forms
  - [ ] Portfolio performance display
  
- [ ] **Asset Management**
  - [ ] Asset browser and search
  - [ ] Asset detail pages
  - [ ] Asset selection components

## Notes for Claude Code
- Use HeroUI components consistently
- Follow existing auth patterns
- Mobile-first responsive design
- Focus on Finance module first (backend is ready)