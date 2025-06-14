# Component Architecture Map - WealthWise Frontend

## Existing Components

### ✅ Implemented
- **Login Page** (`app/(auth)/login/page.tsx`)
  - Uses HeroUI Input, Button, Link, Divider
  - AuthContext integration
  - Form validation and error handling

- **Root Layout** (`app/layout.tsx`)
  - HeroUI providers setup
  - Theme provider integration

- **Auth Context** (`contexts/AuthContext.tsx`)
  - JWT token management
  - User state management
  - Login/logout functionality

### 🚧 Empty Pages (Need Implementation)
- **Dashboard** (`app/(dashboard)/dashboard/page.tsx`)
- **Finance** (`app/(dashboard)/finance/page.tsx`)
- **Journal** (`app/(dashboard)/journal/page.tsx`)

## Components to Build

### Layout Components
- [ ] **DashboardLayout** - Main layout with sidebar navigation
- [ ] **Sidebar** - Navigation with HeroUI components
- [ ] **Header** - Top navigation with user menu
- [ ] **Breadcrumb** - Page navigation indicator

### Finance Components
- [ ] **WalletCard** - Display wallet info with balance
- [ ] **WalletList** - Grid of wallet cards
- [ ] **WalletForm** - Create/edit wallet form
- [ ] **TransactionList** - Table/list of transactions
- [ ] **TransactionForm** - Add/edit transaction form
- [ ] **TransactionItem** - Single transaction display
- [ ] **CategorySelector** - Dropdown for categories
- [ ] **TagSelector** - Multi-select for tags

### Dashboard Components
- [ ] **OverviewCard** - Summary cards for dashboard
- [ ] **RecentTransactions** - Latest transactions widget
- [ ] **BalanceChart** - Chart showing balance over time
- [ ] **ExpenseChart** - Category breakdown chart
- [ ] **QuickActions** - Floating action buttons

### Form Components
- [ ] **CurrencyInput** - Formatted money input
- [ ] **DatePicker** - Date selection component
- [ ] **SearchInput** - Search with suggestions
- [ ] **FilterDropdown** - Advanced filtering options

### UI Components (Using HeroUI)
- [ ] **LoadingSpinner** - Loading states
- [ ] **ErrorBoundary** - Error handling
- [ ] **EmptyState** - No data placeholder
- [ ] **ConfirmDialog** - Confirmation modals

## HeroUI Components in Use
```tsx
// Current imports from existing code
import { Input } from "@heroui/input";
import { Button } from "@heroui/button";
import { Link } from "@heroui/link";
import { Divider } from "@heroui/divider";

// Available HeroUI components to use
import { Card, CardBody, CardHeader } from "@heroui/card";
import { Dropdown, DropdownTrigger, DropdownMenu, DropdownItem } from "@heroui/dropdown";
import { Avatar } from "@heroui/avatar";
import { Spinner } from "@heroui/spinner";
import { Switch } from "@heroui/switch";
import { Navbar, NavbarBrand, NavbarContent, NavbarItem } from "@heroui/navbar";
```

## File Structure to Create
```
components/
├── layout/
│   ├── DashboardLayout.tsx
│   ├── Sidebar.tsx
│   └── Header.tsx
├── finance/
│   ├── WalletCard.tsx
│   ├── WalletForm.tsx
│   ├── TransactionList.tsx
│   └── TransactionForm.tsx
├── dashboard/
│   ├── OverviewCard.tsx
│   ├── RecentTransactions.tsx
│   └── Charts/
├── ui/
│   ├── LoadingSpinner.tsx
│   ├── ErrorBoundary.tsx
│   └── EmptyState.tsx
└── forms/
    ├── CurrencyInput.tsx
    ├── DatePicker.tsx
    └── SearchInput.tsx
```

## State Management Architecture
```tsx
// Zustand stores to create
stores/
├── authStore.ts        # User authentication state
├── financeStore.ts     # Wallets, transactions, categories
├── uiStore.ts         # Loading, errors, modals
└── index.ts           # Store exports
```

## API Integration Pattern
```tsx
// Pattern for component data fetching
const WalletList = () => {
  const { wallets, loading, error } = useFinanceStore();
  
  useEffect(() => {
    financeStore.fetchWallets();
  }, []);
  
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorState error={error} />;
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {wallets.map(wallet => (
        <WalletCard key={wallet.id} wallet={wallet} />
      ))}
    </div>
  );
};
```