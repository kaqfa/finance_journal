# WealthWise Frontend - Next.js Application

## Project Overview
WealthWise frontend is a modern React application built with Next.js 14, TypeScript, and Tailwind CSS. It provides a responsive interface for personal finance and investment tracking.

## Tech Stack (UPDATED)
- **Framework**: Next.js 15 with App Router ✅
- **Language**: TypeScript ✅
- **Styling**: Tailwind CSS + shadcn/ui ✅ (migrated from HeroUI)
- **UI Components**: shadcn/ui (Radix UI primitives) ✅
- **Charts**: Recharts ✅
- **State Management**: AuthContext ✅ (need to add Zustand)
- **Data Fetching**: Basic fetch (need TanStack Query)
- **Forms**: React Hook Form + Zod ✅ (implemented in WalletForm)
- **HTTP Client**: Axios ✅

## Project Structure
```
fe/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/            # Authentication pages
│   │   ├── dashboard/         # Main dashboard
│   │   ├── finance/           # Finance module pages
│   │   ├── invest/            # Investment module pages
│   │   ├── layout.tsx         # Root layout
│   │   └── page.tsx           # Home page
│   ├── components/            # Reusable components
│   │   ├── ui/               # shadcn/ui components
│   │   ├── forms/            # Form components
│   │   ├── charts/           # Chart components
│   │   └── layout/           # Layout components
│   ├── lib/                  # Utilities and configurations
│   │   ├── api.ts            # API client configuration
│   │   ├── auth.ts           # Authentication utilities
│   │   ├── utils.ts          # General utilities
│   │   └── types.ts          # TypeScript type definitions
│   ├── hooks/                # Custom React hooks
│   ├── store/                # Zustand state management
│   └── styles/               # Global styles
├── public/                   # Static assets
├── package.json
├── next.config.js
├── tailwind.config.js
└── tsconfig.json
```

## Implementation Status (UPDATED - 2025-06-15)
- ✅ **Project Setup**: Next.js 15 with TypeScript complete
- ✅ **Authentication**: Login page + AuthContext working
- ✅ **Routing**: Dashboard structure complete with modern layout
- ✅ **UI Migration**: Complete migration from HeroUI to shadcn/ui
- ✅ **Dashboard**: Modern dashboard with academy-style layout
- ✅ **Finance Module**: Wallet and transaction management with modern UI
- ✅ **Layout Components**: Sidebar, header, navigation complete
- ✅ **Chart Components**: Recharts integration with expense breakdown
- ✅ **Transaction Module**: Complete CRUD implementation
- ✅ **Page Structure**: All navigation items have proper pages
- 📋 **Investment Module**: Not started (building in progress pages created)
- 🚧 **Categories/Tags Management**: Need dedicated management pages

## API Integration
- **Base URL**: `https://jurnal.fahrifirdaus.cloud/api/v1/`
- **Authentication**: JWT with automatic token refresh
- **Error Handling**: Global error handling with user-friendly messages
- **Loading States**: Consistent loading indicators across the app

## Key Features to Implement

### Authentication Flow
- Login/register pages with validation
- JWT token management with auto-refresh
- Protected routes and auth guards
- User profile management

### Finance Module
- **Wallet Management**: Create, edit, view wallets with balance display
- **Transaction Management**: Add/edit transactions with category and tag selection
- **Categories & Tags**: Manage transaction categories and tags
- **Transfers**: Inter-wallet transfer functionality
- **Reports**: Monthly reports, expense analysis, charts

### Investment Module
- **Portfolio Management**: Create and manage investment portfolios
- **Asset Browser**: Search and browse available assets
- **Transaction Recording**: Buy/sell/dividend transaction forms
- **Holdings View**: Current positions with P&L display
- **Performance Analytics**: Charts and metrics for portfolio performance

### Dashboard
- **Overview Cards**: Total balance, portfolio value, recent transactions
- **Charts**: Financial trends, portfolio allocation, performance
- **Quick Actions**: Add transaction, transfer money, buy/sell assets
- **Notifications**: Alerts for dividends, price targets, etc.

## Component Architecture

### Layout Components
- `RootLayout`: Main app layout with navigation
- `AuthLayout`: Layout for authentication pages
- `DashboardLayout`: Layout for authenticated pages with sidebar

### Form Components
- `TransactionForm`: Add/edit financial transactions
- `WalletForm`: Create/edit wallets
- `PortfolioForm`: Create/edit investment portfolios
- `AssetSearchForm`: Search and select assets

### Chart Components
- `BalanceChart`: Wallet balance over time
- `ExpenseChart`: Expense breakdown by category
- `PortfolioChart`: Portfolio allocation and performance
- `AssetPriceChart`: Asset price history

## State Management

### Auth Store
```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
}
```

### Finance Store
```typescript
interface FinanceState {
  wallets: Wallet[];
  transactions: Transaction[];
  categories: Category[];
  tags: Tag[];
  // Actions for CRUD operations
}
```

### Investment Store
```typescript
interface InvestmentState {
  portfolios: Portfolio[];
  holdings: Holding[];
  assets: Asset[];
  // Actions for CRUD operations
}
```

## Styling Guidelines

### Design System
- **Colors**: shadcn/ui color system with light/dark mode support
- **Typography**: Modern font scale with tracking-tight headings
- **Spacing**: Academy-style spacing (space-y-6, generous padding)
- **Components**: shadcn/ui as base, following modern dashboard patterns
- **Layout**: Clean, spacious design inspired by shadcnuikit.com/dashboard/academy

### Responsive Design
- **Mobile First**: Design for mobile, enhance for desktop
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)
- **Navigation**: Collapsible sidebar on mobile, persistent on desktop
- **Tables**: Responsive table layouts with horizontal scroll

## Development Guidelines

### Code Standards
- Use TypeScript for all files
- Follow React best practices and hooks patterns
- Implement proper error boundaries
- Use semantic HTML and accessibility features
- Consistent naming conventions

### Performance
- Implement proper loading states
- Use React Query for server state management
- Optimize images and assets
- Implement proper SEO meta tags

### Testing
- Unit tests for utility functions
- Integration tests for API calls
- E2E tests for critical user flows

## Environment Variables
```env
NEXT_PUBLIC_API_URL=https://jurnal.fahrifirdaus.cloud/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret
```

## Development Workflow

### Getting Started
```bash
npm install
npm run dev
```

### Common Tasks
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm run lint`: Run ESLint
- `npm run type-check`: TypeScript type checking

## Integration with Backend

### API Client Setup
- Axios instance with base configuration
- Request/response interceptors for auth
- Automatic token refresh handling
- Error handling and retry logic

### Type Safety
- Generate TypeScript types from OpenAPI schema
- Use proper typing for all API responses
- Implement runtime validation with Zod

## 📋 Current Tasks & Priorities
<!-- AUTO-UPDATED: 2025-06-15 -->

### ✅ COMPLETED TASKS

#### **UI Migration & Dashboard Redesign (Week 24-25)**
- [x] **REDESIGN-001**: Remove HeroUI dependencies from package.json - **Completed** (2025-06-15)
- [x] **REDESIGN-002**: Install shadcn/ui requirements - **Completed** (2025-06-15)
- [x] **DASHBOARD-001**: Study shadcnuikit.com/dashboard design patterns - **Completed** (2025-06-15)
- [x] **DASHBOARD-002**: Install additional shadcn components - **Completed** (2025-06-15)
- [x] **DASHBOARD-003**: Create modern sidebar navigation - **Completed** (2025-06-15)
- [x] **DASHBOARD-004**: Create top header with user menu - **Completed** (2025-06-15)
- [x] **DASHBOARD-005**: Redesign main dashboard layout - **Completed** (2025-06-15)
- [x] **DASHBOARD-006**: Create dashboard cards and metrics - **Completed** (2025-06-15)
- [x] **DASHBOARD-007**: Migrate finance pages to new design - **Completed** (2025-06-15)
- [x] **DASHBOARD-008**: Update to academy-style layout - **Completed** (2025-06-15)

#### **Finance Module Foundation**
- [x] Wallet management page with modern shadcn/ui design - **Completed** (2025-06-15)
- [x] WalletCard component with dropdown actions - **Completed** (2025-06-15)
- [x] WalletForm with Dialog and validation - **Completed** (2025-06-15)
- [x] Finance overview page with quick actions - **Completed** (2025-06-15)
- [x] Integration with backend wallet API - **Completed** (2025-06-15)

#### **Dashboard Components**
- [x] OverviewCards with financial metrics - **Completed** (2025-06-15)
- [x] RecentTransactions component - **Completed** (2025-06-15)
- [x] ExpenseChart with Recharts - **Completed** (2025-06-15)
- [x] MetricCard with trend indicators - **Completed** (2025-06-15)
- [x] Responsive grid layout (academy-style) - **Completed** (2025-06-15)

#### **Layout & Navigation**
- [x] Modern sidebar with navigation sections - **Completed** (2025-06-15)
- [x] Mobile sidebar with sheet component - **Completed** (2025-06-15)
- [x] Clean header (removed notifications/search) - **Completed** (2025-06-15)
- [x] Page-level padding system - **Completed** (2025-06-15)
- [x] Consistent typography and spacing - **Completed** (2025-06-15)

#### **Transaction Module Implementation (Week 25)**
- [x] `/finance/transactions` - Transaction list page with shadcn/ui design - **Completed** (2025-06-15)
- [x] `/finance/transactions/new` - Add transaction form with category/tag selection - **Completed** (2025-06-15)
- [x] `/finance/transactions/[id]/edit` - Edit transaction form - **Completed** (2025-06-15)
- [x] Transaction search & filter components (real-time search, type filtering) - **Completed** (2025-06-15)
- [x] TransactionCard component with modern card design - **Completed** (2025-06-15)
- [x] Form validation and error handling with defensive programming - **Completed** (2025-06-15)
- [x] Category and tag selection with type filtering - **Completed** (2025-06-15)
- [x] Complete CRUD operations for transactions - **Completed** (2025-06-15)

#### **UX Improvements & Page Structure**
- [x] BuildingInProgress component for unimplemented features - **Completed** (2025-06-15)
- [x] Building in progress pages for all navigation items - **Completed** (2025-06-15)
- [x] Professional placeholder pages with expected completion dates - **Completed** (2025-06-15)
- [x] Consistent navigation and back button functionality - **Completed** (2025-06-15)

### ✅ COMPLETED TASKS - Transaction Module (Week 26)

#### **Transaction Module Implementation** ✅ COMPLETED
- [x] Complete Transaction CRUD with modern shadcn/ui design - **Completed** (2025-06-15)
- [x] Transaction list page with real-time search and filtering - **Completed** (2025-06-15) 
- [x] Transaction form with category/tag selection and validation - **Completed** (2025-06-15)
- [x] Transaction edit functionality with prefilled forms - **Completed** (2025-06-15)
- [x] Transaction delete with confirmation dialogs - **Completed** (2025-06-15)
- [x] Advanced filtering (type, category, date range) - **Completed** (2025-06-15)

#### **Error Handling & Code Quality** ✅ COMPLETED
- [x] Comprehensive array safety guards (Array.isArray) - **Completed** (2025-06-15)
- [x] Select component value validation (empty string → "none") - **Completed** (2025-06-15)
- [x] Defensive programming patterns throughout forms - **Completed** (2025-06-15)

### ✅ COMPLETED TASKS - Categories & Tags Module (Week 27)

#### **Categories & Tags Management** ✅ COMPLETED
- [x] `/finance/categories` - Complete category management with CRUD operations - **Completed** (2025-06-15)
- [x] CategoryForm component with icon/color selection - **Completed** (2025-06-15)
- [x] `/finance/tags` - Complete tag management with search functionality - **Completed** (2025-06-15)
- [x] TagForm component with validation and preview - **Completed** (2025-06-15)
- [x] Modern UI with income/expense separation for categories - **Completed** (2025-06-15)
- [x] Tag statistics dashboard with usage metrics - **Completed** (2025-06-15)

### 🚧 CURRENT TASKS - Wallet Enhancement & Investment

#### **Wallet Enhancement (Medium Priority)**
- [ ] `/finance/wallets/[id]` - Wallet detail view with transaction history
- [ ] Wallet transaction history component
- [ ] Wallet balance chart over time

### 🎯 Dashboard Enhancement (Week 3-4)

#### **Dashboard Enhancement (Low Priority)**
- [ ] Real data integration for overview cards
- [ ] Monthly spending trend chart
- [ ] Interactive chart legends
- [ ] Quick action improvements

### 🔧 State Management & Architecture

#### **Zustand Stores**
- [ ] Finance store (wallets, transactions, categories, tags)
- [ ] Auth store improvement with persistent token management
- [ ] UI state store (loading states, errors, modal management)

#### **API Integration Enhancement**
- [ ] Enhanced axios interceptors with better error handling
- [ ] Standardized loading states across all components
- [ ] Retry logic for failed requests
- [ ] Optimistic updates for better UX

### 🧩 Component Architecture

#### **Component Development**
- [ ] TransactionList component with sorting and filtering
- [ ] CategorySelector component with search functionality
- [ ] DateRangePicker component for filtering
- [ ] TransactionForm with real-time validation
- [ ] TransferForm for inter-wallet transfers
- [ ] CurrencyInput component with proper formatting

### 📱 Mobile Optimization
- [ ] Responsive layouts for all pages (mobile-first approach)
- [ ] Touch-friendly interactions and button sizing
- [ ] Mobile navigation improvements with collapsible sidebar
- [ ] Swipe gestures for transaction actions

### 💼 Investment Module (Week 5-6) - After Finance Completion

#### **Portfolio Management**
- [ ] Portfolio list and detail pages with performance metrics
- [ ] Add/edit portfolio forms with risk level selection
- [ ] Portfolio performance display with charts and analytics

#### **Asset Management**
- [ ] Asset browser and search with filtering by type/sector
- [ ] Asset detail pages with price history and charts
- [ ] Asset selection components for transaction forms

### 🎯 CURRENT SPRINT PRIORITIES
1. **Transaction Module** - Complete transaction CRUD with modern UI
2. **Categories & Tags** - Management pages for transaction organization
3. **Real Data Integration** - Connect dashboard to actual API data
4. **Mobile Optimization** - Test and refine responsive design
5. **Investment Module** - Start portfolio management features

### 📈 PROGRESS METRICS (UPDATED: 2025-06-15)
- **UI Migration**: 100% Complete ✅
- **Dashboard Redesign**: 100% Complete ✅
- **Finance Module**: 100% Complete ✅ (Wallets ✅, Transactions ✅, Categories ✅, Tags ✅)
- **Transaction Module**: 100% Complete ✅ (Full CRUD with modern UI)
- **Categories & Tags**: 100% Complete ✅ (Complete management interface)
- **Layout & Navigation**: 100% Complete ✅
- **Component Library**: 95% Complete ✅ (Core components ✅, Forms ✅, Charts ✅)
- **Page Structure**: 100% Complete ✅ (All navigation items have pages)
- **Error Handling**: 100% Complete ✅ (Defensive programming implemented)
- **Monorepo Infrastructure**: 100% Complete ✅ (Turbo config fixed)

### 🎨 DESIGN ACHIEVEMENTS
- ✅ Modern academy-style layout with generous spacing
- ✅ Complete shadcn/ui migration (removed all HeroUI dependencies)
- ✅ Responsive grid system following modern patterns
- ✅ Clean header design (removed clutter)
- ✅ Professional card-based UI with hover effects
- ✅ Consistent typography and color system

## Notes for Claude Code
- **Current Tasks**: See "📋 Current Tasks & Priorities" section above for detailed task breakdown
- **Component Map**: See `COMPONENT_MAP.md` for component architecture and what needs to be built
- **Development Guide**: Check `DEVELOPMENT.md` for coding standards and patterns
- **API Reference**: Check `API_REFERENCE.md` for all available backend endpoints and usage examples
- **Complete API Schema**: See `docs/openapi.json` for full OpenAPI specification
- Focus on TypeScript type safety throughout
- Use shadcn/ui components for consistent modern UI
- Follow academy-style design patterns for spacing and layout
- Implement proper loading and error states
- Follow mobile-first responsive design
- Prioritize Transaction module completion
- Use existing AuthContext patterns for consistency
- Build reusable components following established patterns

## Backend API Reference
The backend API is fully documented at `https://jurnal.fahrifirdaus.cloud/api/docs/`

### Authentication Endpoints
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/token/refresh/` - Refresh JWT token
- `GET /api/v1/auth/profile/` - Get user profile
- `PUT /api/v1/auth/profile/` - Update user profile

### Finance Module Endpoints (✅ Production Ready)
- `GET /api/v1/finance/wallets/` - List wallets
- `POST /api/v1/finance/wallets/` - Create wallet
- `GET /api/v1/finance/wallets/{id}/` - Get wallet details
- `GET /api/v1/finance/transactions/` - List transactions
- `POST /api/v1/finance/transactions/` - Create transaction
- `GET /api/v1/finance/categories/` - List categories
- `GET /api/v1/finance/tags/` - List tags
- `GET /api/v1/finance/transfers/` - List transfers
- `POST /api/v1/finance/transfers/` - Create transfer

### Investment Module Endpoints (🚧 In Development)
- `GET /api/v1/invest/assets/` - List assets
- `GET /api/v1/invest/portfolios/` - List portfolios
- `POST /api/v1/invest/portfolios/` - Create portfolio
- `GET /api/v1/invest/holdings/` - List holdings
- `GET /api/v1/invest/transactions/` - List investment transactions
- `POST /api/v1/invest/transactions/` - Create investment transaction

## Type Definitions from Backend

### Core Types
```typescript
export interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  phone?: string;
  date_joined: string;
}

export interface Wallet {
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

export interface Transaction {
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

export interface Category {
  id: number;
  name: string;
  type: 'income' | 'expense';
  icon?: string;
  color?: string;
  created_at: string;
  updated_at: string;
}

export interface Tag {
  id: number;
  name: string;
  created_at: string;
}

export interface Asset {
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

export interface InvestmentPortfolio {
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

export interface InvestmentHolding {
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

## UI Components Structure

### Base Components (shadcn/ui) ✅
- Button, Input, Card, Avatar, Badge ✅
- Dialog, Select, Switch, Label ✅
- Alert, Dropdown Menu ✅
- Sidebar, Sheet (mobile) ✅
- Need to add: Table, Form, Combobox components

### Custom Components Status
- ✅ `WalletCard`: Modern card with dropdown actions
- ✅ `WalletForm`: Dialog form with validation
- ✅ `MetricCard`: Dashboard metrics with trends
- ✅ `RecentTransactions`: Transaction list component
- ✅ `ExpenseChart`: Pie chart with Recharts
- ✅ `Sidebar`: Navigation with sections
- ✅ `Header`: Clean header with user menu
- [ ] `TransactionItem`: List item for transactions
- [ ] `TransactionForm`: Add/edit transaction form
- [ ] `CategorySelector`: Category selection component
- [ ] `DateRangePicker`: Date range selection
- [ ] `CurrencyInput`: Formatted currency input

## Routing Structure
```
/                           # Landing/home page
/(auth)/
  ├── login                 # Login page
  ├── register              # Registration page
  └── forgot-password       # Password reset
/dashboard                  # Main dashboard
/finance/
  ├── wallets              # Wallet management
  ├── transactions         # Transaction list/add
  ├── categories           # Category management
  ├── tags                 # Tag management
  └── reports              # Financial reports
/invest/
  ├── portfolios           # Portfolio management
  ├── assets               # Asset browser
  ├── transactions         # Investment transactions
  └── analytics            # Investment analytics
/settings/
  ├── profile              # User profile
  └── preferences          # App preferences
```

## Development Phases

### ✅ COMPLETED PHASES

#### Phase 1: Foundation ✅
- ✅ Next.js project setup with TypeScript
- ✅ Authentication flow implementation
- ✅ Modern layout and navigation (shadcn/ui)
- ✅ API client setup with axios

#### Phase 2: UI Migration & Dashboard ✅
- ✅ Complete HeroUI to shadcn/ui migration
- ✅ Modern dashboard with academy-style layout
- ✅ Wallet management with modern UI
- ✅ Chart integration with Recharts
- ✅ Responsive design implementation

### 🚧 CURRENT PHASE

#### Phase 3: Transaction Module (In Progress)
- [ ] Transaction CRUD functionality
- [ ] Advanced filtering and search
- [ ] Category and tag management
- [ ] Real-time data integration

### 📋 UPCOMING PHASES

#### Phase 4: Investment Module
- [ ] Portfolio management
- [ ] Asset browser and search
- [ ] Investment transaction recording
- [ ] Holdings display with P&L

#### Phase 5: Enhancement
- [ ] Advanced analytics
- [ ] Performance optimizations
- [ ] Comprehensive testing
- [ ] Production deployment