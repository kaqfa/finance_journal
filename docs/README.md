# Documentation Index - WealthWise Project

## 📋 Overview

Selamat datang di dokumentasi WealthWise! Direktori `/docs` ini berisi semua dokumentasi teknis, spesifikasi, dan panduan pengembangan untuk platform manajemen keuangan pribadi WealthWise.

## 📁 Struktur Dokumentasi

### 🏗️ **Architecture** (`/docs/architecture/`)
Dokumentasi arsitektur sistem dan desain teknis:
- [`database-schema.md`](./architecture/database-schema.md) - Schema database lengkap dengan relasi dan indexes
- *Planned: system-architecture.md* - Arsitektur sistem secara keseluruhan
- *Planned: security-design.md* - Desain keamanan dan authentication

### 📡 **API** (`/docs/api/`)
Dokumentasi API dan endpoint:
- [`api-documentation.md`](./api/api-documentation.md) - Complete API documentation dengan semua endpoints
- *Available at runtime: `/api/docs/`* - Interactive Swagger UI documentation
- *Available at runtime: `/api/redoc/`* - ReDoc documentation interface

### 📝 **Specifications** (`/docs/specifications/`)
Spesifikasi produk dan requirements:
- [`application-structure.md`](./specifications/application-structure.md) - Struktur aplikasi dan menu navigation
- [`todo-list.md`](./specifications/todo-list.md) - Task list dan prioritas development
- *Planned: user-requirements.md* - User stories dan functional requirements
- *Planned: ui-ux-guidelines.md* - Design system dan UI/UX guidelines

### 🚀 **Development** (`/docs/development/`)
Panduan dan proses development:
- [`roadmap.md`](./development/roadmap.md) - Development roadmap dan sprint planning
- *Planned: setup-guide.md* - Setup development environment
- *Planned: coding-standards.md* - Coding standards dan best practices
- *Planned: testing-guide.md* - Testing strategies dan guidelines

## 🎯 Quick Navigation

### **Untuk Developer Baru**
1. Start dengan [Application Structure](./specifications/application-structure.md) untuk memahami scope project
2. Review [Database Schema](./architecture/database-schema.md) untuk memahami data models
3. Check [API Documentation](./api/api-documentation.md) untuk available endpoints
4. Follow [Development Roadmap](./development/roadmap.md) untuk current priorities

### **Untuk API Integration**
1. [API Documentation](./api/api-documentation.md) - Complete endpoint reference
2. Live API docs at `/api/docs/` pada development server
3. Authentication guide di API documentation
4. Sample requests dan responses tersedia

### **Untuk Product Planning**
1. [Application Structure](./specifications/application-structure.md) - UI/UX dan feature specifications
2. [Todo List](./specifications/todo-list.md) - Current development priorities
3. [Development Roadmap](./development/roadmap.md) - Timeline dan milestones

## 📊 Project Status Overview

### ✅ **Production Ready**
- **Finance Module Backend**: Complete API dengan wallet, transactions, categories
- **Authentication System**: JWT-based auth dengan registration tokens
- **Database Design**: Comprehensive schema untuk semua modules
- **API Documentation**: Interactive Swagger documentation

### 🚧 **In Development**
- **Investment Module Backend**: Models ready, API implementation ongoing
- **Frontend Application**: Next.js setup dengan basic structure
- **Testing Infrastructure**: Unit tests untuk backend modules

### 📋 **Planned**
- **Trading Module**: Advanced trading journal dengan analytics
- **Mobile Optimization**: PWA dan mobile-responsive design
- **External Integrations**: Real-time market data dan bank APIs
- **Advanced Analytics**: Charts, reports, dan financial insights

## 🛠️ Development Workflow

### **Documentation Updates**
- Update dokumentasi setiap kali ada perubahan major pada API atau architecture
- Maintain version sync antara code dan documentation
- Use conventional commits untuk documentation changes

### **Claude Code Integration**
Documentation ini dioptimalkan untuk AI-assisted development:
- Structured format untuk easy parsing oleh Claude Code
- Comprehensive context untuk AI understanding
- Clear action items dan next steps

### **Review Process**
- Documentation reviews dilakukan setiap sprint
- Keep docs updated dengan latest development progress
- Ensure accuracy dan completeness untuk semua modules

## 📚 Additional Resources

### **External Documentation**
- [Django Documentation](https://docs.djangoproject.com/) - Django framework reference
- [Django REST Framework](https://www.django-rest-framework.org/) - DRF documentation
- [Next.js Documentation](https://nextjs.org/docs) - Next.js framework guide
- [Tailwind CSS](https://tailwindcss.com/docs) - CSS framework documentation

### **Project Resources**
- **Repository**: `/Users/kaqfa/Documents/Project/Pribadi/journal-django/`
- **API Base URL**: `http://localhost:8000/api/v1/` (development)
- **Frontend URL**: `http://localhost:3000/` (development)
- **Admin Panel**: `http://localhost:8000/admin/` (development)

### **Tools & Services**
- **Database**: SQLite (development), PostgreSQL (production)
- **API Testing**: Swagger UI, Postman collections available
- **Version Control**: Git dengan conventional commits
- **CI/CD**: GitHub Actions (planned)

---

## 🔄 Recent Updates

### **Week 24, 2025 (Current)**
- ✅ Created comprehensive documentation structure
- ✅ Migrated specifications ke organized format
- ✅ Updated API documentation dengan latest endpoints
- ✅ Added development roadmap dengan sprint planning

### **Previous Updates**
- ✅ Completed Finance Module API implementation
- ✅ Setup monorepo structure dengan Turborepo
- ✅ Implemented JWT authentication system
- ✅ Created database schema untuk semua modules

---

## 📞 Support & Contact

### **Development Questions**
- Check existing documentation first
- Review API documentation untuk endpoint questions
- Refer to development roadmap untuk current priorities

### **Documentation Issues**
- Documentation bugs atau improvements dapat di-track di project issues
- Keep documentation updated dengan development progress
- Maintain consistency across all documentation files

---

*Last Updated: June 14, 2025*  
*Documentation Version: 1.0*  
*Next Review: June 21, 2025*