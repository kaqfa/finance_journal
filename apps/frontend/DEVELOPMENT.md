# Development Guidelines - WealthWise Frontend

## Tech Stack (ACTUAL)
- **Framework**: Next.js 15 with App Router
- **UI Library**: HeroUI (NOT shadcn/ui)
- **State**: AuthContext (need to add Zustand)
- **HTTP Client**: Axios (basic setup exists)
- **Forms**: Need React Hook Form + Zod
- **Charts**: Need Recharts
- **Styling**: Tailwind CSS

## Existing Components & Structure
```
app/
├── (auth)/login/              # ✅ Login page implemented
├── (dashboard)/
│   ├── dashboard/             # 🚧 Empty page
│   ├── finance/               # 🚧 Empty page  
│   └── journal/               # 🚧 Empty page
└── layout.tsx                 # ✅ Root layout

lib/api/                       # ✅ Basic API setup
├── auth.ts                    # Auth API calls
├── finance.ts                 # Finance API calls
└── index.ts                   # API exports

contexts/AuthContext.tsx       # ✅ Auth management
components/                    # 🚧 Need more components
```

## Development Workflow
1. **Pages**: Create in `/app/(dashboard)/`
2. **Components**: Add to `/components/`
3. **API**: Update in `/lib/api/`
4. **Types**: Add to `/types/`
5. **State**: Use Zustand stores

## Styling Guidelines
- **Use HeroUI components as base**
- **Tailwind for custom styling**
- **Mobile-first approach**
- **Dark/light mode support with next-themes**

## API Integration
- Base URL: `https://jurnal.fahrifirdaus.cloud/api/v1`
- Auth: JWT tokens managed by AuthContext
- Error handling: Global error boundaries needed

## Component Patterns
```tsx
// HeroUI Button example
import { Button } from "@heroui/button";

<Button color="primary" variant="solid">
  Save
</Button>

// HeroUI Card example
import { Card, CardBody, CardHeader } from "@heroui/card";

<Card>
  <CardHeader>Title</CardHeader>
  <CardBody>Content</CardBody>
</Card>
```

## Next Steps
1. Install missing dependencies (Zustand, React Hook Form, Recharts)
2. Create reusable components
3. Implement Finance module pages
4. Add proper state management