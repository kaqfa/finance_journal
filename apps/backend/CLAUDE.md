# WealthWise Backend - Django REST API

## 🎯 App Purpose
Backend API untuk WealthWise platform yang menyediakan RESTful endpoints untuk manajemen keuangan pribadi, investasi, dan trading. Built dengan Django REST Framework dengan dokumentasi OpenAPI lengkap.

## 🏗️ Tech Stack
- **Framework**: Django 4.1.13 + Django REST Framework 3.14.0
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Authentication**: JWT dengan djangorestframework-simplejwt
- **API Documentation**: Swagger/OpenAPI dengan drf-yasg
- **CORS**: django-cors-headers untuk frontend integration
- **Testing**: Django Test Framework dengan coverage

## 🗂️ Django Apps Structure
```
be/
├── wealthwise/           # Django project settings
├── master/               # User management & core models  
├── api/                  # API layer dengan versioning
│   ├── v1/auth/         # Authentication endpoints
│   ├── v1/finance/      # Finance module APIs
│   └── v1/invest/       # Investment module APIs
├── finance/              # Finance models & business logic
├── invest/               # Investment models & business logic  
├── journal/              # Journal/blog functionality
└── trading/              # Trading functionality (planned)
```

## 🧪 Testing Strategy
- **Unit Tests**: Models, serializers, utility functions
- **Integration Tests**: API endpoints dengan authentication
- **Coverage**: Target minimum 80% code coverage
- **Test Data**: Fixtures untuk consistent test data
- **Run Tests**: `python manage.py test` atau `pytest`

## 📋 Current Tasks
<!-- UPDATED: 2025-06-14 -->
### ✅ Completed
- [x] Complete authentication system dengan JWT - **2025-06-13**
- [x] Finance module API endpoints (CRUD) - **2025-06-12** 
- [x] OpenAPI documentation dengan Swagger UI - **2025-06-11**
- [x] CORS configuration untuk frontend - **2025-06-10**

### 🚧 In Progress - Investment Module API Completion
- [ ] **Serializers Enhancement**
  - [ ] Complete InvestmentPortfolioSerializer with performance calculations
  - [ ] Add InvestmentTransactionSerializer validation and processing
  - [ ] Implement InvestmentHoldingSerializer with automatic calculations
  
- [ ] **ViewSet Implementation**
  - [ ] Add portfolio performance custom actions and analytics
  - [ ] Implement asset allocation endpoints with rebalancing
  - [ ] Add portfolio optimization and rebalancing suggestions
  
- [ ] **Asset Management**
  - [ ] Asset price update endpoints with external data integration
  - [ ] Asset search optimization with filtering and pagination
  - [ ] Historical price data endpoints for charting

### 📋 Next Priorities - API Enhancements & Testing
- [ ] **Filtering & Pagination**
  - [ ] Advanced filtering for investment transactions (date, type, asset)
  - [ ] Date range filtering for all modules with timezone support
  - [ ] Custom pagination for large datasets optimization
  
- [ ] **Performance Optimization**
  - [ ] Database query optimization using select_related/prefetch_related
  - [ ] Response caching for static data (assets, categories)
  - [ ] Bulk operations for data import functionality

- [ ] **Testing Requirements**
  - [ ] Investment module unit tests (target: 90% coverage)
  - [ ] API integration tests with authentication scenarios
  - [ ] Performance testing for large datasets and complex queries
  
- [ ] **Documentation**
  - [ ] Update OpenAPI schema for investment endpoints
  - [ ] Add API usage examples and integration guides
  - [ ] Document authentication flows and error handling

## 🚀 API Endpoints Status

### ✅ Production Ready
**Authentication (`/api/v1/auth/`)**
- `POST /login/` - User login dengan JWT
- `POST /register/` - User registration
- `POST /logout/` - User logout
- `POST /token/refresh/` - JWT token refresh
- `GET /profile/` - Get user profile
- `PUT /profile/` - Update user profile

**Finance Module (`/api/v1/finance/`)**
- `GET|POST /wallets/` - Wallet management
- `GET|PUT|DELETE /wallets/{id}/` - Individual wallet operations
- `GET|POST /transactions/` - Transaction management  
- `GET|PUT|DELETE /transactions/{id}/` - Individual transaction operations
- `GET|POST /categories/` - Category management
- `GET /tags/` - Tag listing
- `GET|POST /transfers/` - Inter-wallet transfers

### 🚧 In Development
**Investment Module (`/api/v1/invest/`)**
- `GET|POST /assets/` - Asset management - **80% Complete**
- `GET|POST /portfolios/` - Portfolio management - **60% Complete**
- `GET|POST /holdings/` - Holdings tracking - **40% Complete**
- `GET|POST /transactions/` - Investment transactions - **30% Complete**

### 📋 Planned
- `GET /analytics/` - Financial analytics endpoints
- `GET /reports/` - Report generation
- `POST /import/` - Data import functionality
- `GET /export/` - Data export functionality

## 🔍 Key Files to Watch
- `wealthwise/settings.py` - Django configuration & environment variables
- `api/v1/*/views.py` - API endpoint implementations
- `*/models.py` - Database models dan business logic
- `*/serializers.py` - API serialization logic  
- `*/tests.py` - Test cases untuk setiap module
- `requirements.txt` - Python dependencies

## 📊 Database Schema

### Core Models
- **User** (Django default) - Extended dengan profile fields
- **Wallet** - User wallets dengan different types
- **Transaction** - Financial transactions dengan categories
- **Category** - Transaction categorization
- **Tag** - Transaction tagging system
- **Transfer** - Inter-wallet transfers

### Investment Models  
- **Asset** - Investment assets (stocks, crypto, etc.)
- **Portfolio** - Investment portfolios
- **Holding** - Current positions
- **InvestmentTransaction** - Buy/sell/dividend transactions

## 🛠️ Development Commands
```bash
# Virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Database operations
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

# Development server
python manage.py runserver

# Testing
python manage.py test
python manage.py test --coverage

# Create superuser
python manage.py createsuperuser

# Shell access
python manage.py shell
```

## 🔧 Configuration

### Environment Variables
```bash
# .env file (create from .env.example)
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Production settings  
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgres://user:pass@host:port/dbname
```

### Key Settings
- **CORS_ALLOWED_ORIGINS**: Configured untuk frontend development
- **JWT Settings**: Token expiration dan refresh configuration
- **DRF Settings**: Pagination, permissions, authentication classes
- **Swagger Settings**: API documentation customization

## 🐛 Known Issues & Solutions
- **CSRF Issues**: Solved dengan proper CORS configuration
- **JWT Token Refresh**: Implemented automatic refresh mechanism
- **File Upload**: Planned untuk user avatars dan document attachments
- **Database Queries**: Need optimization untuk complex analytics queries

## 🔒 Security Considerations
- **JWT Tokens**: Secure token handling dengan automatic refresh
- **CORS Policy**: Properly configured untuk production deployment
- **Input Validation**: DRF serializers handle input validation
- **SQL Injection**: Protected dengan Django ORM
- **Rate Limiting**: Planned implementation dengan django-ratelimit

## 📈 Performance Optimization
- **Database Indexing**: Added pada frequently queried fields
- **Query Optimization**: Using select_related dan prefetch_related
- **Caching Strategy**: Planned dengan Redis untuk session management
- **API Response Time**: Target <200ms untuk most endpoints

## 🧪 Testing Guidelines
```python
# Test structure example
class WalletAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(...)
        self.client.force_authenticate(user=self.user)
    
    def test_create_wallet(self):
        # Test wallet creation
        pass
    
    def test_wallet_balance_calculation(self):
        # Test business logic
        pass
```

## 🚀 Deployment Notes
- **Production Database**: PostgreSQL recommended
- **Static Files**: Configured untuk production serving
- **Environment Variables**: Use environment-specific settings
- **Docker**: Dockerfile ready untuk containerized deployment
- **CI/CD**: GitHub Actions configuration planned

---

*Module Owner: Backend Team*
*Last Updated: 2025-06-14*
*API Documentation: http://localhost:8000/api/docs/*