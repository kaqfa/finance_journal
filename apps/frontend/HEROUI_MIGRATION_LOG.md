# HeroUI to shadcn/ui Migration Log

## REDESIGN-001: Dependencies Removed

### Removed HeroUI Dependencies (2025-06-14)

#### Main HeroUI Packages:
- @heroui/avatar: ^2.2.15
- @heroui/button: 2.2.17  
- @heroui/card: 2.2.16
- @heroui/chip: ^2.2.17
- @heroui/code: 2.2.12
- @heroui/divider: ^2.2.13
- @heroui/dropdown: ^2.3.19
- @heroui/input: 2.4.17
- @heroui/kbd: 2.2.13
- @heroui/link: 2.2.14
- @heroui/listbox: 2.3.16
- @heroui/modal: ^2.2.18
- @heroui/navbar: 2.2.15
- @heroui/select: ^2.4.21
- @heroui/snippet: 2.2.18
- @heroui/spinner: ^2.2.16
- @heroui/switch: 2.2.15
- @heroui/system: 2.4.13
- @heroui/theme: 2.4.13

#### Related Dependencies Removed:
- @react-aria/ssr: 3.9.7
- @react-aria/visually-hidden: 3.8.21
- framer-motion: 11.13.1 (used by HeroUI)
- tailwind-variants: 0.3.0 (HeroUI styling system)
- @react-types/shared: 3.25.0 (React Aria types)

#### Preserved Dependencies:
- axios: ^1.9.0 (HTTP client)
- clsx: 2.1.1 (class name utility - will be useful for shadcn)
- intl-messageformat: ^10.5.0 (internationalization)
- next: 15.0.4 (framework)
- next-themes: ^0.4.4 (theme management)
- react: 18.3.1 (core)
- react-dom: 18.3.1 (core)

## Files Requiring Migration

### Component Files with HeroUI Imports:
1. `./types/heroui.d.ts` - Type definitions
2. `./app/(auth)/register/page.tsx` - Registration page
3. `./app/(auth)/forget-password/page.tsx` - Password reset page
4. `./app/(auth)/login/page.tsx` - Login page
5. `./app/(dashboard)/dashboard/page.tsx` - Dashboard page
6. `./app/(dashboard)/finance/wallets/page.tsx` - Wallets page
7. `./app/providers.tsx` - App providers
8. `./components/ui/spinner.tsx` - Spinner component
9. `./components/navbar.tsx` - Navigation bar
10. `./components/auth/AuthLayout.tsx` - Auth layout
11. `./components/layout/DashboardLayout.tsx` - Dashboard layout
12. `./components/counter.tsx` - Counter component
13. `./components/theme-switch.tsx` - Theme switcher
14. `./components/finance/WalletCard.tsx` - Wallet card
15. `./components/finance/WalletForm.tsx` - Wallet form

### Configuration Files to Update:
- `tailwind.config.js` - Remove HeroUI theme, add shadcn config
- Component imports throughout the application

## Next Steps
1. Install shadcn/ui dependencies (REDESIGN-002)
2. Initialize shadcn/ui CLI (REDESIGN-003)  
3. Install core components (REDESIGN-004)
4. Update Tailwind config (REDESIGN-005)
5. Create component mapping (REDESIGN-006)
6. Begin component migration (REDESIGN-007+)

## Migration Status
- ✅ REDESIGN-001: Dependencies removed
- ⏳ Next: Install shadcn/ui requirements