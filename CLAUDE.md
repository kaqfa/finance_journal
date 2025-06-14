# WealthWise Monorepo - Personal Finance Management Platform

## 🎯 Project Mission
WealthWise adalah platform manajemen keuangan pribadi yang memungkinkan pengguna untuk melacak keuangan, investasi, dan trading dalam satu aplikasi terintegrasi. Platform ini menyediakan dashboard komprehensif untuk analisis keuangan, portfolio tracking, dan perencanaan finansial.

## 🏗️ Architecture
```
wealthwise-monorepo/
├── apps/              # Applications 
│   ├── backend/       # Django REST API
│   └── frontend/      # Next.js Web App
├── packages/          # Shared libraries and components
│   ├── shared-types/  # TypeScript type definitions
│   ├── ui-components/ # Reusable UI components
│   └── eslint-config/ # Shared ESLint rules
├── tools/             # Build tools and utilities
├── docs/              # Documentation
└── .claude/           # Claude Code configurations
```

## 🛠️ Development Commands
- `npm run dev` - Start both backend and frontend development servers
- `npm run build` - Build all packages using Turborepo
- `npm run test` - Run all tests across monorepo
- `npm run lint` - Lint all code with shared ESLint config
- `npm run typecheck` - TypeScript checking for all packages
- `npm run dev:frontend` - Start only frontend dev server
- `npm run dev:backend` - Start only backend dev server
- `make setup` - Complete environment setup
- `make docker-dev` - Start development with Docker
- `make clean` - Clean all build artifacts

## 📋 Current Sprint Goals
<!-- AUTO-UPDATED: 2025-06-14 -->
### 🎯 Sprint Week 24 - Monorepo Modernization ✅ COMPLETED
- [x] Implement modern monorepo structure with Turborepo - **Completed** (2025-06-14)
- [x] Add shared packages for types and configurations - **Completed** (2025-06-14) 
- [x] Setup unified development scripts and Docker support - **Completed** (2025-06-14)
- [x] Migrate to apps/ directory structure - **Completed** (2025-06-14)
- [x] Create comprehensive CLAUDE.md documentation - **Completed** (2025-06-14)
- [x] Setup custom Claude commands for monorepo management - **Completed** (2025-06-14)

### 📈 Progress Metrics
- Completed: 6/6 (100%)
- Sprint Status: ✅ **FULLY COMPLETED**

### 🎯 Current Sprint Week 25 - Frontend Redesign (HeroUI → shadcn/ui)
**STRATEGIC PIVOT**: Complete redesign of frontend component library

#### Phase 1: Foundation Setup (High Priority)
- [ ] REDESIGN-001: Remove HeroUI dependencies from package.json - **High Priority**
- [ ] REDESIGN-002: Install shadcn/ui requirements - **High Priority**
- [ ] REDESIGN-003: Initialize shadcn/ui with CLI - **High Priority**
- [ ] REDESIGN-004: Install core shadcn components - **High Priority**
- [ ] REDESIGN-005: Update tailwind.config.js - **High Priority**
- [ ] REDESIGN-006: Create component mapping documentation - **High Priority**

#### Phase 2: Component Migration (Medium Priority)
- [ ] REDESIGN-007: Migrate UI primitives (button, spinner) - **Medium Priority**
- [ ] REDESIGN-008: Migrate authentication components - **Medium Priority**
- [ ] REDESIGN-009: Setup form handling (react-hook-form + zod) - **Medium Priority**
- [ ] REDESIGN-010: Migrate navigation components - **Medium Priority**
- [ ] REDESIGN-011: Update theme system for shadcn - **Medium Priority**
- [ ] REDESIGN-012: Migrate remaining components - **Medium Priority**

#### Phase 3: Testing & Documentation (Low Priority)
- [ ] REDESIGN-013: Test all components (responsive + dark mode) - **Low Priority**
- [ ] REDESIGN-014: Update documentation and tech stack - **Low Priority**
- [ ] REDESIGN-015: Create reusable form components - **Low Priority**
- [ ] REDESIGN-016: Final optimization and testing - **Low Priority**

### 🔄 Future Sprint Candidates
- [ ] UI-006: Create shared component library (@wealthwise/ui-components)
- [ ] API-007: Implement comprehensive API testing suite
- [ ] DEPLOY-008: Setup CI/CD pipeline with GitHub Actions
- [ ] ANALYTICS-009: Add charts and financial analytics
- [ ] MOBILE-010: Responsive design optimization

## 🎨 Code Style Guidelines
- **TypeScript First**: Use TypeScript for all new code across frontend and shared packages
- **Django Standards**: Follow Django best practices for backend development
- **Shared ESLint**: Use `@wealthwise/eslint-config` for consistent code style
- **Conventional Commits**: Use conventional commit format for all commits
- **Testing Required**: Write tests for all business logic and API endpoints
- **Type Safety**: Leverage shared types from `@wealthwise/shared-types`

## 🔄 Workflow Rules
- **Feature Branches**: Create feature branches for new development
- **Pre-commit Checks**: Always run tests and linting before committing
- **Documentation Updates**: Update relevant CLAUDE.md when adding new conventions
- **Monorepo Commands**: Use unified commands from root package.json
- **Progress Tracking**: Update sprint progress after completing major tasks
- **Code Review**: Use meaningful commit messages with `/commit-with-context`

## 🤖 AI Development Notes
- **Always run linting**: Execute `npm run lint` after code changes
- **Type checking**: Run `npm run typecheck` for TypeScript validation
- **Complex decisions**: Use "think hard" mode for architectural decisions
- **Feature planning**: Create plan documents for major features before implementation
- **Progress updates**: Update this CLAUDE.md after completing significant tasks
- **Context switching**: Use separate Claude sessions for different apps when needed
- **Docker development**: Use `make docker-dev` for consistent development environment

## 🏗️ Tech Stack Overview

### Backend (Django)
- **Framework**: Django 4.1.13 + Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: JWT with djangorestframework-simplejwt
- **API Documentation**: Swagger/OpenAPI with drf-yasg
- **Testing**: Django Test Framework + pytest

### Frontend (Next.js)
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui components (migrating from HeroUI)
- **UI Components**: shadcn/ui (built on Radix UI primitives)
- **Form Handling**: React Hook Form + Zod validation
- **State Management**: React Context (AuthContext) → planned Zustand migration
- **HTTP Client**: Axios with interceptors
- **Testing**: Jest + React Testing Library (planned)

### Shared Packages
- **Types**: Centralized TypeScript definitions
- **UI Components**: Reusable React components (planned)
- **ESLint Config**: Shared linting rules
- **Build Tools**: Turborepo for optimized builds

## 🚀 Development Environment

### Quick Start
```bash
# Clone and setup
git clone <repo-url>
cd wealthwise-monorepo

# Install dependencies and setup environment
make setup

# Start development servers
npm run dev
# OR with Docker
make docker-dev
```

### Environment Variables
```bash
# Backend (.env)
DEBUG=1
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## 📊 Module Status

### ✅ Production Ready
- **Authentication System**: Login, registration, JWT token management
- **Finance Module**: Wallet management, transactions, categories, transfers
- **Backend API**: Comprehensive REST API with OpenAPI documentation

### 🚧 In Development  
- **Frontend Implementation**: Dashboard and finance pages (structure exists)
- **Investment Module**: Backend models ready, frontend not implemented
- **Shared Components**: Basic structure created, needs implementation

### 📋 Planned
- **Mobile App**: React Native app (removed Flutter version)
- **Advanced Analytics**: Charts and financial insights
- **Trading Module**: Integration with trading APIs
- **Real-time Updates**: WebSocket for live data

## 🔍 Key Development Areas

### Current Priorities
1. **Complete Frontend Finance Module**: Implement wallet and transaction UIs
2. **Shared Component Library**: Build reusable UI components
3. **Investment Module Frontend**: Create portfolio management interface
4. **Testing Infrastructure**: Add comprehensive test coverage
5. **CI/CD Pipeline**: Automated testing and deployment

### Technical Debt
- Remove unused mobile Flutter code (in progress)
- Standardize error handling across frontend
- Add comprehensive API testing
- Implement proper logging and monitoring
- Optimize database queries for better performance

## 🤝 Team Workflow

### Daily Development
- Start with `/update-progress` command to sync current status
- Use focused Claude sessions for specific modules
- Update CLAUDE.md files when adding new patterns or conventions
- Run full test suite before major commits
- Use meaningful commit messages following conventional commits

### Code Review Process
- All changes require tests for business logic
- Frontend changes must maintain type safety
- Backend changes require API documentation updates
- Shared package changes need version bumps
- Performance impact consideration for database changes

---

*Last Updated: 2025-06-14*
*Claude Code Integration: Optimized for AI-assisted development*