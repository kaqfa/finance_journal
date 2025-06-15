# Shared Types Package - @wealthwise/shared-types

## 🎯 Package Purpose
Centralized TypeScript type definitions untuk seluruh WealthWise monorepo. Package ini menyediakan type safety dan consistency across frontend, backend API responses, dan shared utilities.

## 🏗️ Tech Stack
- **Language**: TypeScript 5.3+
- **Build Tool**: TypeScript Compiler (tsc)
- **Package Manager**: npm (monorepo workspace)
- **Distribution**: CommonJS modules dengan type definitions

## 📁 Type Categories

### Core Types
- **User & Authentication**: User profiles, login responses, JWT tokens
- **Finance Module**: Wallets, transactions, categories, tags, transfers
- **Investment Module**: Assets, portfolios, holdings, investment transactions
- **API Responses**: Paginated responses, error handling types
- **Form Data**: Input validation dan form submission types

### Utility Types
- **Enums**: WalletType, TransactionType, AssetType, RiskLevel
- **API Types**: LoginResponse, RefreshTokenResponse, PaginatedResponse
- **Union Types**: Type-safe unions untuk different entity states

## 📋 Current Tasks
<!-- UPDATED: 2025-06-14 -->
### ✅ Completed
- [x] Initial type definitions dari frontend code - **2025-06-14**
- [x] Package setup dengan TypeScript build - **2025-06-14**
- [x] Core finance dan investment types - **2025-06-14**

### 🚧 In Progress
- [ ] Add validation schemas dengan Zod integration - **Not Started**
- [ ] API error handling types - **Not Started**
- [ ] Form validation types - **Not Started**

### 📋 Next Priorities
- [ ] Runtime type validation dengan Zod
- [ ] API response type guards
- [ ] Generic utility types untuk better DX
- [ ] Documentation generation dari types
- [ ] Version management strategy

## 🔧 Usage Examples

### Import dalam Frontend
```typescript
import { 
  Wallet, 
  Transaction, 
  CreateWalletData,
  PaginatedResponse 
} from '@wealthwise/shared-types';

// Type-safe API responses
const wallets: PaginatedResponse<Wallet> = await fetchWallets();

// Form data validation
const walletData: CreateWalletData = {
  name: 'Main Wallet',
  wallet_type: 'bank',
  currency: 'IDR',
  initial_balance: '1000000'
};
```

### Integration dengan API Client
```typescript
import { LoginResponse, User } from '@wealthwise/shared-types';

const loginUser = async (credentials: LoginData): Promise<LoginResponse> => {
  const response = await api.post('/auth/login/', credentials);
  return response.data; // Type-safe response
};
```

## 📊 Type Structure

### Finance Types Hierarchy
```typescript
// Base wallet type
interface Wallet extends BaseEntity {
  wallet_type: WalletType;
  current_balance: string; // Decimal as string
}

// Create/Update variants
interface CreateWalletData extends Omit<Wallet, 'id' | 'created_at' | 'updated_at'> {
  initial_balance: string;
}
```

### Investment Types Hierarchy
```typescript
// Asset management
interface Asset {
  id: string;
  symbol: string;
  type: AssetType;
  latest_price?: string;
}

// Portfolio tracking
interface InvestmentHolding {
  asset_symbol: string;
  quantity: string;
  unrealized_pnl: string;
  unrealized_pnl_percentage: string;
}
```

## 🛠️ Development Commands
```bash
# Build types
npm run build

# Type checking
npm run typecheck

# Clean build artifacts
npm run clean

# Watch mode untuk development
npm run build -- --watch
```

## 🔍 Key Files
- `src/index.ts` - Main export file dengan all type definitions
- `package.json` - Package configuration dan build scripts
- `tsconfig.json` - TypeScript compilation settings
- `dist/` - Compiled JavaScript dan type definitions (generated)

## 📈 Best Practices

### Type Naming Conventions
- **Interfaces**: PascalCase (e.g., `Wallet`, `Transaction`)
- **Union Types**: PascalCase dengan descriptive names (e.g., `WalletType`)
- **Generic Types**: Single letter atau descriptive (e.g., `T`, `ResponseData`)
- **Form Data**: Prefix dengan `Create` atau `Update` (e.g., `CreateWalletData`)

### Type Organization
- **Group related types**: Keep wallet-related types together
- **Use utility types**: Leverage TypeScript utility types seperti `Omit`, `Pick`
- **Avoid any**: Always provide specific types, avoid `any` usage
- **Optional fields**: Use `?` untuk optional properties, document when field is optional

### Version Management
- **Semantic Versioning**: Follow semver untuk breaking changes
- **Backward Compatibility**: Maintain compatibility dengan existing consumers
- **Deprecation Strategy**: Mark deprecated types dan provide migration path
- **Change Documentation**: Document type changes dalam CHANGELOG

## 🔗 Integration Points

### Frontend Integration
- Next.js frontend menggunakan types untuk API responses
- Form validation dengan type-safe data structures
- Component props typing dengan shared interfaces

### Backend Coordination
- Types harus match dengan Django API responses
- Serializer output format alignment
- Database model field mapping

### Future Integrations
- Mobile app akan menggunakan same types
- Testing utilities dengan type-safe mocks
- API documentation generation dari types

## 🚀 Planned Features

### Zod Integration
```typescript
import { z } from 'zod';

export const WalletSchema = z.object({
  name: z.string().min(1).max(100),
  wallet_type: z.enum(['cash', 'bank', 'ewallet', 'credit', 'other']),
  currency: z.string().length(3),
  initial_balance: z.string().regex(/^\d+(\.\d{2})?$/)
});

export type CreateWalletData = z.infer<typeof WalletSchema>;
```

### Type Guards
```typescript
export function isWallet(obj: unknown): obj is Wallet {
  return typeof obj === 'object' && 
         obj !== null && 
         'id' in obj && 
         'wallet_type' in obj;
}
```

### Generic API Types
```typescript
export interface APIResponse<T> {
  data: T;
  message: string;
  status: 'success' | 'error';
}

export interface APIError {
  field?: string;
  message: string;
  code: string;
}
```

## 🐛 Known Issues
- **Decimal Handling**: All monetary values sebagai string untuk precision
- **Date Formatting**: ISO string format consistency
- **Optional Fields**: Some API responses have conditional fields
- **Nested Objects**: Complex nested structures need better typing

## ⚠️ Important Notes
- **Breaking Changes**: Coordinate dengan all consumers sebelum breaking changes
- **Testing**: Types changes require testing di consuming applications
- **Documentation**: Keep type documentation up to date
- **Performance**: Large type files dapat impact TypeScript compile time

---

*Package Maintainer: Frontend Team*
*Last Updated: 2025-06-14*  
*Consumers: Frontend App, Future Mobile App*