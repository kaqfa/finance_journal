# Component Architecture Map - WealthWise Frontend

## 🚨 MIGRATION STATUS: HeroUI → shadcn/ui

**Current Status**: Active migration in progress (REDESIGN-001 ✅, REDESIGN-002 ✅)
- HeroUI dependencies **removed** from package.json
- shadcn/ui core requirements **installed**
- Components below need **updating** to use shadcn/ui instead of HeroUI

## Existing Components

### ✅ Implemented (⚠️ NEEDS MIGRATION)
- **Login Page** (`app/(auth)/login/page.tsx`)
  - ❌ Currently uses HeroUI Input, Button, Link, Divider
  - 🔄 **Needs migration** to shadcn/ui components
  - AuthContext integration ✅
  - Form validation and error handling ✅

- **Root Layout** (`app/layout.tsx`)
  - ❌ Currently has HeroUI providers setup
  - 🔄 **Needs migration** to shadcn/ui theme provider
  - Theme provider integration concept ✅

- **Auth Context** (`contexts/AuthContext.tsx`)
  - ✅ JWT token management (no UI changes needed)
  - ✅ User state management (independent of UI library)
  - ✅ Login/logout functionality (no UI changes needed)

### 🚧 Empty Pages (Need Implementation with shadcn/ui)
- **Dashboard** (`app/(dashboard)/dashboard/page.tsx`)
- **Finance** (`app/(dashboard)/finance/page.tsx`)
- **Journal** (`app/(dashboard)/journal/page.tsx`)

## Components to Build (Using shadcn/ui)

### Layout Components
- [ ] **DashboardLayout** - Main layout with sidebar navigation (shadcn/ui sidebar pattern)
- [ ] **Sidebar** - Navigation with shadcn/ui navigation components
- [ ] **Header** - Top navigation with user menu dropdown
- [ ] **Breadcrumb** - Page navigation indicator using shadcn/ui breadcrumb

### Finance Components
- [ ] **WalletCard** - Display wallet info with balance (shadcn/ui card)
- [ ] **WalletList** - Grid of wallet cards with responsive layout
- [ ] **WalletForm** - Create/edit wallet form (shadcn/ui form + input)
- [ ] **TransactionList** - Table/list using shadcn/ui table component
- [ ] **TransactionForm** - Add/edit transaction form with validation
- [ ] **TransactionItem** - Single transaction display component
- [ ] **CategorySelector** - Dropdown using shadcn/ui select
- [ ] **TagSelector** - Multi-select using shadcn/ui multi-select

### Dashboard Components
- [ ] **OverviewCard** - Summary cards using shadcn/ui card
- [ ] **RecentTransactions** - Latest transactions widget
- [ ] **BalanceChart** - Chart integration with Recharts
- [ ] **ExpenseChart** - Category breakdown pie chart
- [ ] **QuickActions** - Action buttons with shadcn/ui button

### Form Components
- [ ] **CurrencyInput** - Formatted money input (custom shadcn/ui input)
- [ ] **DatePicker** - Date selection using shadcn/ui date picker
- [ ] **SearchInput** - Search with suggestions (shadcn/ui command)
- [ ] **FilterDropdown** - Advanced filtering (shadcn/ui popover + form)

### UI Components (Using shadcn/ui)
- [ ] **LoadingSpinner** - Loading states (shadcn/ui spinner)
- [ ] **ErrorBoundary** - Error handling with shadcn/ui alert
- [ ] **EmptyState** - No data placeholder with shadcn/ui empty state
- [ ] **ConfirmDialog** - Confirmation modals (shadcn/ui dialog)

## 📋 Component Migration Mapping

### Core UI Components
| HeroUI Component | shadcn/ui Replacement | Status | Notes |
|------------------|------------------------|---------|-------|
| `@heroui/button` | `@/components/ui/button` | ✅ Installed | Direct replacement available |
| `@heroui/input` | `@/components/ui/input` | ✅ Installed | Similar API, form integration |
| `@heroui/card` | `@/components/ui/card` | ✅ Installed | CardHeader, CardContent, CardFooter |
| `@heroui/divider` | `@/components/ui/separator` | ✅ Installed | Same functionality, different name |
| `@heroui/spinner` | `@/components/ui/spinner` | ✅ Updated | Custom implementation with Lucide icon |
| `@heroui/switch` | `@/components/ui/switch` | ✅ Installed | Direct replacement |
| `@heroui/avatar` | `@/components/ui/avatar` | ✅ Installed | AvatarImage + AvatarFallback pattern |
| `@heroui/dropdown` | `@/components/ui/dropdown-menu` | ✅ Installed | More comprehensive menu system |
| `@heroui/modal` | `@/components/ui/dialog` | ✅ Installed | DialogContent, DialogHeader, etc. |
| `@heroui/select` | `@/components/ui/select` | ✅ Installed | SelectTrigger, SelectContent, SelectItem |
| `@heroui/navbar` | `@/components/ui/navigation-menu` | ✅ Installed | More flexible navigation system |
| `@heroui/link` | Next.js `Link` + styling | 🔄 Manual | Use Next.js Link with shadcn button styles |
| `@heroui/chip` | `@/components/ui/badge` | ✅ Installed | Similar functionality for labels/tags |

### Forms & Data Display
| HeroUI Component | shadcn/ui Replacement | Status | Notes |
|------------------|------------------------|---------|-------|
| Form validation | `@/components/ui/form` | ✅ Installed | React Hook Form integration |
| Form labels | `@/components/ui/label` | ✅ Installed | Improved accessibility |
| Data tables | `@/components/ui/table` | ✅ Installed | Comprehensive table components |

### Import Mapping Examples
```tsx
// ❌ OLD: HeroUI imports (to be replaced)
import { Input } from "@heroui/input";
import { Button } from "@heroui/button";
import { Link } from "@heroui/link";
import { Divider } from "@heroui/divider";
import { Card, CardBody, CardHeader } from "@heroui/card";
import { Dropdown, DropdownTrigger, DropdownMenu, DropdownItem } from "@heroui/dropdown";
import { Avatar } from "@heroui/avatar";
import { Spinner } from "@heroui/spinner";
import { Switch } from "@heroui/switch";
import { Modal, ModalContent, ModalHeader, ModalBody, ModalFooter } from "@heroui/modal";

// ✅ NEW: shadcn/ui imports (to replace HeroUI)
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Link from "next/link"; // Use Next.js Link with shadcn button styles
import { Separator } from "@/components/ui/separator";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Spinner } from "@/components/ui/spinner";
import { Switch } from "@/components/ui/switch";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { NavigationMenu, NavigationMenuContent, NavigationMenuItem, NavigationMenuLink, NavigationMenuList, NavigationMenuTrigger } from "@/components/ui/navigation-menu";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
```

## File Structure to Create (shadcn/ui Based)
```
components/
├── ui/                      # shadcn/ui base components (auto-generated)
│   ├── button.tsx
│   ├── input.tsx
│   ├── card.tsx
│   ├── select.tsx
│   ├── form.tsx
│   ├── table.tsx
│   ├── dialog.tsx
│   └── ... (other shadcn/ui components)
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

## 🔄 Migration Strategy

### Phase 1: Foundation (✅ Completed)
1. ✅ Remove HeroUI dependencies
2. ✅ Install shadcn/ui core requirements
3. ✅ Initialize shadcn/ui CLI
4. ✅ Install core components
5. ✅ Update Tailwind configuration

### Phase 2: Component Migration (🚧 In Progress)
**Priority Order:**
1. **UI Primitives** (button, spinner) - Start here
2. **Authentication Components** - Login/register forms
3. **Navigation Components** - Header, sidebar, navigation
4. **Layout Components** - Dashboard layout, auth layout
5. **Form Components** - Wallet forms, transaction forms
6. **Data Display** - Cards, tables, lists

### Phase 3: Testing & Cleanup
1. Test all migrated components
2. Remove unused HeroUI type definitions
3. Update documentation
4. Performance optimization

## 🛠️ Migration Guidelines

### 1. Button Migration Example
```tsx
// ❌ Before (HeroUI)
import { Button } from "@heroui/button";
<Button color="primary" variant="solid" onPress={handleClick}>
  Save Changes
</Button>

// ✅ After (shadcn/ui)
import { Button } from "@/components/ui/button";
<Button variant="default" onClick={handleClick}>
  Save Changes
</Button>
```

### 2. Card Migration Example  
```tsx
// ❌ Before (HeroUI)
import { Card, CardBody, CardHeader } from "@heroui/card";
<Card>
  <CardHeader>Title</CardHeader>
  <CardBody>Content</CardBody>
</Card>

// ✅ After (shadcn/ui)
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>Content</CardContent>
</Card>
```

### 3. Form Migration Example
```tsx
// ❌ Before (HeroUI)
import { Input } from "@heroui/input";
<Input 
  label="Email" 
  type="email" 
  isInvalid={!!error}
  errorMessage={error}
/>

// ✅ After (shadcn/ui)
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input 
    id="email"
    type="email" 
    className={error ? "border-destructive" : ""}
  />
  {error && <p className="text-destructive text-sm">{error}</p>}
</div>
```

## API Integration Pattern
```tsx
// Pattern for component data fetching (unchanged)
const WalletList = () => {
  const { wallets, loading, error } = useFinanceStore();
  
  useEffect(() => {
    financeStore.fetchWallets();
  }, []);
  
  if (loading) return <Spinner label="Loading wallets..." />;
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