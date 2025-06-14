# WealthWise Frontend - Next.js Application

## Project Overview
WealthWise frontend is a modern React application built with Next.js 14, TypeScript, and Tailwind CSS. It provides a responsive interface for personal finance and investment tracking.

## Tech Stack (ACTUAL)
- **Framework**: Next.js 15 with App Router ✅
- **Language**: TypeScript ✅
- **Styling**: Tailwind CSS + HeroUI (NOT shadcn/ui) ✅
- **State Management**: AuthContext ✅ (need to add Zustand)
- **Data Fetching**: Basic fetch (need TanStack Query)
- **Forms**: Basic forms (need React Hook Form + Zod)
- **Charts**: Not implemented (need Recharts)
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

## Implementation Status (UPDATED)
- ✅ **Project Setup**: Next.js 15 with TypeScript complete
- ✅ **Authentication**: Login page + AuthContext working
- ✅ **Routing**: Dashboard structure exists
- 🚧 **Finance Module**: Pages exist but empty
- 📋 **Investment Module**: Not started
- 🚧 **UI Components**: Basic HeroUI setup, need more components
- 🚧 **Dashboard**: Empty page, needs implementation

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
- **Colors**: HeroUI color system with light/dark mode support
- **Typography**: Consistent font scale and weights
- **Spacing**: Tailwind spacing scale (4px increments)
- **Components**: HeroUI as base, customized for WealthWise branding

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

## Current Priorities (UPDATED)
1. **Finance Module Implementation**: Build wallet and transaction pages (backend ready)
2. **Dashboard Enhancement**: Create overview with financial widgets
3. **State Management**: Implement Zustand stores for proper state handling
4. **Component Library**: Build reusable components with HeroUI
5. **Investment Module**: Implement after finance module is complete

## Notes for Claude Code
- **Current Tasks**: Check `TODO.md` for detailed development priorities and task list
- **Component Map**: See `COMPONENT_MAP.md` for component architecture and what needs to be built
- **Development Guide**: Check `DEVELOPMENT.md` for coding standards and patterns
- **API Reference**: Check `API_REFERENCE.md` for all available backend endpoints and usage examples
- **Complete API Schema**: See `docs/openapi.json` for full OpenAPI specification
- Focus on TypeScript type safety throughout
- Use HeroUI components for consistent UI
- Implement proper loading and error states
- Follow mobile-first responsive design
- Prioritize Finance module first (backend is production-ready)
- Use existing AuthContext patterns for consistency
- Build reusable components following the component map

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

### Base Components (HeroUI)
- Button, Input, Card, Dropdown, Avatar
- Navbar, Spinner, Switch, Link, Divider
- Code, Kbd, Snippet (specialized components)
- Need to add: Table, Form, Dialog components

### Custom Components to Build
- `WalletCard`: Display wallet info with balance
- `TransactionItem`: List item for transactions
- `PortfolioCard`: Portfolio overview card
- `AssetSearchCombobox`: Searchable asset selector
- `DateRangePicker`: Date range selection
- `CurrencyInput`: Formatted currency input
- `PerformanceMetric`: Display P&L with colors

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

### Phase 1: Foundation (Week 1-2)
- Next.js project setup with TypeScript
- Authentication flow implementation
- Basic layout and navigation
- API client setup with axios

### Phase 2: Finance Module (Week 3-4)
- Wallet management pages
- Transaction CRUD functionality
- Category and tag management
- Basic reporting and charts

### Phase 3: Dashboard (Week 5)
- Overview dashboard with widgets
- Financial summary cards
- Recent transactions display
- Quick action buttons

### Phase 4: Investment Module (Week 6-8)
- Portfolio management
- Asset browser and search
- Investment transaction recording
- Holdings display with P&L

### Phase 5: Enhancement (Week 9-10)
- Advanced charts and analytics
- Mobile optimization
- Performance improvements
- Testing and bug fixes