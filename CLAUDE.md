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

### 🎯 Next Sprint Week 25 - Frontend Implementation
- [ ] FRONTEND-001: Implement finance module pages (wallets, transactions) - **High Priority**
- [ ] FRONTEND-002: Build dashboard with financial overview widgets - **High Priority**
- [ ] FRONTEND-003: Add Zustand state management - **Medium Priority**
- [ ] FRONTEND-004: Create reusable form components with validation - **Medium Priority**
- [ ] BACKEND-005: Complete investment module API endpoints - **Medium Priority**

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
- **Styling**: Tailwind CSS + HeroUI components
- **State Management**: React Context (AuthContext)
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