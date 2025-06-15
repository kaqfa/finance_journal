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
<!-- AUTO-UPDATED: 2025-06-15 -->
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

### 🎯 Sprint Week 25 - Frontend Redesign (HeroUI → shadcn/ui) ✅ COMPLETED
**STRATEGIC PIVOT**: Complete redesign of frontend component library

#### Phase 1: Foundation Setup ✅ COMPLETED
- [x] REDESIGN-001: Remove HeroUI dependencies from package.json - **Completed** (2025-06-15)
- [x] REDESIGN-002: Install shadcn/ui requirements - **Completed** (2025-06-15)
- [x] REDESIGN-003: Initialize shadcn/ui with CLI - **Completed** (2025-06-15)
- [x] REDESIGN-004: Install core shadcn components - **Completed** (2025-06-15)
- [x] REDESIGN-005: Update tailwind.config.js - **Completed** (2025-06-15)
- [x] REDESIGN-006: Create component mapping documentation - **Completed** (2025-06-15)

#### Phase 2: Component Migration ✅ COMPLETED
- [x] REDESIGN-007: Migrate UI primitives (button, spinner) - **Completed** (2025-06-15)
- [x] REDESIGN-008: Migrate authentication components - **Completed** (2025-06-15)
- [x] REDESIGN-009: Setup form handling (react-hook-form + zod) - **Completed** (2025-06-15)
- [x] REDESIGN-010: Migrate navigation components - **Completed** (2025-06-15)
- [x] REDESIGN-011: Update theme system for shadcn - **Completed** (2025-06-15)
- [x] REDESIGN-012: Migrate remaining components - **Completed** (2025-06-15)

#### Phase 3: Dashboard Enhancement ✅ COMPLETED
- [x] DASHBOARD-001: Study shadcnuikit.com/dashboard patterns - **Completed** (2025-06-15)
- [x] DASHBOARD-002: Create modern sidebar navigation - **Completed** (2025-06-15)
- [x] DASHBOARD-003: Create clean header design - **Completed** (2025-06-15)
- [x] DASHBOARD-004: Implement academy-style layout - **Completed** (2025-06-15)
- [x] DASHBOARD-005: Build dashboard components - **Completed** (2025-06-15)
- [x] DASHBOARD-006: Migrate finance pages - **Completed** (2025-06-15)

### 📈 Progress Metrics
- **Phase 1 (Foundation)**: 6/6 (100%) ✅
- **Phase 2 (Migration)**: 6/6 (100%) ✅
- **Phase 3 (Dashboard)**: 6/6 (100%) ✅
- **Overall Sprint**: 18/18 (100%) ✅ **FULLY COMPLETED**

### 🎯 Sprint Week 26 - Transaction Module Implementation ✅ COMPLETED
**STRATEGIC ACHIEVEMENT**: Complete transaction management functionality

#### Transaction CRUD (High Priority) ✅ COMPLETED
- [x] TRANSACTION-001: Create transaction list page with filtering - **Completed** (2025-06-15)
- [x] TRANSACTION-002: Build transaction form with validation - **Completed** (2025-06-15)
- [x] TRANSACTION-003: Implement category/tag selection - **Completed** (2025-06-15)
- [x] TRANSACTION-004: Add transaction search functionality - **Completed** (2025-06-15)
- [x] TRANSACTION-005: Create transaction edit/delete actions - **Completed** (2025-06-15)

#### Error Handling & Code Quality ✅ COMPLETED
- [x] DEFENSIVE-001: Comprehensive array safety guards (Array.isArray) - **Completed** (2025-06-15)
- [x] DEFENSIVE-002: Select component value validation (empty string → "none") - **Completed** (2025-06-15)
- [x] DEFENSIVE-003: Defensive programming patterns throughout forms - **Completed** (2025-06-15)

#### Categories & Tags Management (Medium Priority) 🚧 IN PROGRESS
- [ ] CATEGORY-001: Build category management page
- [ ] CATEGORY-002: Create category form with icons/colors
- [ ] TAG-001: Build tag management interface
- [ ] TAG-002: Implement tag multi-select components

### 📈 Progress Metrics
- **Transaction CRUD**: 5/5 (100%) ✅
- **Error Handling**: 3/3 (100%) ✅ 
- **Categories/Tags**: 0/4 (0%) 🚧
- **Overall Sprint**: 8/12 (67%) 🚧 **IN PROGRESS**

### 🎯 Current Sprint Week 27 - Categories & Investment Foundation
**CURRENT FOCUS**: Complete categories/tags management and start investment module

#### Categories & Tags Management (High Priority)
- [ ] CATEGORY-001: Build category management page
- [ ] CATEGORY-002: Create category form with icons/colors
- [ ] TAG-001: Build tag management interface
- [ ] TAG-002: Implement tag multi-select components

#### Investment Module Foundation (Medium Priority)
- [ ] INVESTMENT-001: Portfolio management interface
- [ ] INVESTMENT-002: Asset browser and search
- [ ] INVESTMENT-003: Investment transaction forms
- [ ] INVESTMENT-004: Holdings display with P&L

### 🔄 Future Sprint Candidates
- [ ] ANALYTICS-003: Advanced financial charts and insights
- [ ] MOBILE-004: Mobile app optimization
- [ ] DEPLOY-005: CI/CD pipeline with GitHub Actions
- [ ] TESTING-006: Comprehensive test coverage

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

## 📋 Todo List Management System

### 🔄 **3-Layer Todo System**

1. **🤖 Session TodoRead/TodoWrite** (Real-time tracking)
   - Purpose: Current session work tracking, temporary
   - Usage: `TodoRead` and `TodoWrite` tools in Claude Code
   - Scope: Active development tasks only
   - Lifetime: Session-based, not persistent

2. **📁 App-Specific CLAUDE.md** (Technical implementation)
   - Purpose: Detailed technical tasks and implementation details
   - Files: `apps/frontend/CLAUDE.md`, `apps/backend/CLAUDE.md`
   - Scope: Component-level, API-level, technical architecture
   - Lifetime: Persistent, version controlled

3. **🏠 Root CLAUDE.md** (Strategic overview)
   - Purpose: Sprint goals, high-level progress, project roadmap
   - File: `/CLAUDE.md` (this file)
   - Scope: Project-wide goals, sprint planning, major milestones
   - Lifetime: Persistent, strategic planning

### ✅ **Synchronization Rules**

#### **When completing tasks:**
1. Mark as completed in Session TodoWrite
2. Update relevant app-specific CLAUDE.md with completion date
3. Update root CLAUDE.md sprint progress
4. Commit all CLAUDE.md changes with progress update

#### **Before starting new sprints:**
1. Check all 3 layers for consistency
2. Remove duplicate/redundant todos across files
3. Ensure sprint goals align with app-specific tasks
4. Archive completed sprints to maintain clean tracking

#### **Daily sync checklist:**
- [ ] `TodoRead` matches current work
- [ ] App CLAUDE.md reflects technical progress  
- [ ] Root CLAUDE.md shows sprint status
- [ ] No duplicate tasks across layers
- [ ] Completed tasks marked with dates

### 🧹 **Cleanup Guidelines**

#### **Remove redundant todos when:**
- Same task exists in multiple files with different wording
- Completed tasks are still marked as pending elsewhere
- Technical tasks are duplicated in strategic overview
- Sprint goals overlap with detailed implementation tasks

#### **Keep separate todos when:**
- Different scope (strategic vs technical vs implementation)
- Different timeline (current sprint vs future planning)
- Different responsibility (frontend vs backend vs fullstack)
- Different granularity (epic vs story vs task)

### 📊 **Progress Tracking Protocol**

```markdown
# Example sync after completing work:

1. Session: Mark dashboard-008 as completed
2. Frontend CLAUDE.md: [x] Dashboard layout migration - Completed (2025-06-15)
3. Root CLAUDE.md: [x] DASHBOARD-006: Migrate finance pages - Completed (2025-06-15)
4. Commit: "docs: sync todo completion across all layers"
```

**🎯 Goal**: Maintain single source of truth while supporting different levels of detail and planning horizons.

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

*Last Updated: 2025-06-15*
*Claude Code Integration: Optimized for AI-assisted development*
*Todo Management: 3-layer system with sync protocol*