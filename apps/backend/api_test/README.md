# API Testing Guide - Journal Invest

Panduan lengkap untuk testing API menggunakan REST Client VS Code extension.

## 📋 Prerequisites

1. **Install REST Client Extension**
   ```
   Name: REST Client
   Publisher: Humao
   VS Code Extension ID: humao.rest-client
   ```

2. **Setup Development Server**
   ```bash
   # Di terminal, navigate ke directory backend
   cd /Users/kaqfa/Documents/Project/Pribadi/journal-django/be
   
   # Jalankan development server
   python manage.py runserver
   
   # Server akan berjalan di http://localhost:8000
   ```

3. **Prepare Test Database**
   ```bash
   # Run migrations jika belum
   python manage.py migrate
   
   # Create superuser untuk testing (optional)
   python manage.py createsuperuser
   ```

## 🗂️ File Structure

```
be/api_test/
├── environment.http          # Environment variables
├── finance_api.http          # Finance module tests
├── investment_api.http       # Investment module tests
└── README.md                # This guide
```

## 🚀 Quick Start

### 1. Setup Environment Variables

1. Buka file `environment.http`
2. Update `@baseUrl` jika perlu (default: http://localhost:8000)
3. Variables lain akan diupdate setelah testing

### 2. Testing Finance Module

1. Buka file `finance_api.http`
2. **Start dengan Authentication:**
   - Run "Register User" request
   - Run "Login User" request
   - Copy `access_token` dari response
   - Update `@accessToken` variable di file

3. **Test Core Features:**
   ```
   Authentication → Wallets → Categories → Transactions → Analytics
   ```

4. **Update Variables:**
   - Setelah create wallet, copy ID dan update `@testWalletId`
   - Setelah create category, copy ID dan update `@testCategoryId`
   - Dan seterusnya...

### 3. Testing Investment Module

1. Buka file `investment_api.http`
2. **Start dengan Authentication** (sama seperti Finance)
3. **Test Core Features:**
   ```
   Authentication → Assets → Portfolios → Transactions → Holdings → Analytics
   ```

4. **Update Variables** sesuai response yang didapat

## 🎯 Testing Workflow

### Phase 1: Basic CRUD Operations
```
1. Authentication (register/login)
2. Create master data (assets, categories, wallets)
3. Create main entities (portfolios, transactions)
4. Test read operations (list, detail)
5. Test update operations
6. Test delete operations
```

### Phase 2: Business Logic Testing
```
1. Test holdings auto-calculation
2. Test portfolio performance metrics
3. Test transaction validations
4. Test user isolation
5. Test data consistency
```

### Phase 3: Advanced Features
```
1. Test analytics endpoints
2. Test bulk operations
3. Test export features
4. Test complex filtering
5. Test pagination
```

### Phase 4: Error Handling
```
1. Test invalid data inputs
2. Test unauthorized access
3. Test edge cases
4. Test error responses
```

## 📝 How to Run Tests

### Method 1: Individual Requests
1. Klik pada request yang ingin dijalankan
2. Click "Send Request" yang muncul di atas request
3. Lihat response di panel sebelah kanan
4. Copy data yang diperlukan untuk update variables

### Method 2: Keyboard Shortcuts
- `Ctrl+Alt+R` (Windows/Linux) atau `Cmd+Alt+R` (Mac)
- Position cursor di dalam request block
- Press shortcut to send

### Method 3: Command Palette
1. `Ctrl+Shift+P` → "REST Client: Send Request"
2. Pilih request dari list

## 🔧 Variable Management

### Dynamic Variables
Update setelah mendapat response:

```http
# Setelah create wallet, response akan berisi:
{
  "id": 1,
  "name": "BCA Savings",
  ...
}

# Update variable:
@testWalletId = 1
```

### Environment-Specific Variables
```http
# Development
@baseUrl = http://localhost:8000

# Production (contoh)
@baseUrl = https://api.journalinvest.com

# Staging (contoh)
@baseUrl = https://staging-api.journalinvest.com
```

## 📊 Response Analysis

### Success Responses
- **200 OK**: Successful GET/PUT requests
- **201 Created**: Successful POST requests
- **204 No Content**: Successful DELETE requests

### Error Responses
- **400 Bad Request**: Validation errors
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### Key Data to Extract
1. **IDs**: For updating variables
2. **Calculated Fields**: Verify business logic
3. **Timestamps**: Check data consistency
4. **Validation Errors**: Understand constraints

## 🧪 Testing Scenarios

### Finance Module Scenarios
```
✅ Wallet Management
- Create different wallet types (bank, ewallet, cash, credit)
- Test balance calculations
- Test wallet status (active/inactive)

✅ Transaction Management
- Create income/expense/transfer transactions
- Test category assignment
- Test tag functionality
- Verify balance updates

✅ Analytics
- Test summary calculations
- Test monthly reports
- Test category breakdown
- Test filtering and search
```

### Investment Module Scenarios
```
✅ Asset Management
- Create different asset types (stock, crypto, bond, reit)
- Test price history
- Test asset search

✅ Portfolio Management
- Create portfolios with different risk levels
- Test allocation tracking
- Test performance calculation

✅ Transaction Management
- Test buy/sell/dividend transactions
- Verify holdings auto-calculation
- Test bulk import functionality

✅ Holdings & Analytics
- Test portfolio valuation
- Test diversification analysis
- Test performance metrics
```

## 🔍 Debugging Tips

### Common Issues & Solutions

1. **401 Unauthorized**
   ```
   Problem: Token expired atau tidak valid
   Solution: Run login request lagi, update @accessToken
   ```

2. **400 Bad Request**
   ```
   Problem: Data validation error
   Solution: Check request body, lihat error details di response
   ```

3. **404 Not Found**
   ```
   Problem: Wrong endpoint atau ID tidak ada
   Solution: Verify endpoint URL dan pastikan ID valid
   ```

4. **Variable Not Found**
   ```
   Problem: Variable belum di-set atau typo
   Solution: Update variable di header file atau fix typo
   ```

### Response Headers to Check
- `Content-Type`: Should be `application/json`
- `Authorization`: Verify token format
- `X-Request-ID`: For debugging server logs

### Request Body Validation
```json
// ✅ Good Request
{
  "name": "Test Wallet",
  "wallet_type": "bank",
  "currency": "IDR",
  "initial_balance": "1000000.00"
}

// ❌ Bad Request
{
  "name": "",                    // Empty required field
  "wallet_type": "invalid",      // Invalid choice
  "currency": "INVALID",         // Invalid currency
  "initial_balance": "abc"       // Invalid number
}
```

## 📈 Performance Testing

### Load Testing with REST Client
```http
### Test dengan multiple requests
GET {{apiBase}}/finance/transactions/?page_size=100
Authorization: Bearer {{accessToken}}

### Test complex filtering
GET {{apiBase}}/invest/transactions/?portfolio={{testPortfolioId}}&start_date=2023-01-01&end_date=2025-12-31&transaction_type=buy&min_amount=1000000&ordering=-transaction_date
Authorization: Bearer {{accessToken}}

### Test bulk operations
POST {{apiBase}}/invest/transactions/bulk_create/
Authorization: Bearer {{accessToken}}
Content-Type: application/json

{
  "transactions": [
    // Array of 50+ transactions
  ]
}
```

### Metrics to Monitor
- Response time (aim for < 200ms for simple requests)
- Memory usage (check Django debug toolbar)
- Database queries (should be minimal with proper optimization)

## 🛡️ Security Testing

### Authentication Tests
```http
### Test without token
GET {{apiBase}}/finance/wallets/
# Should return 401

### Test with invalid token
GET {{apiBase}}/finance/wallets/
Authorization: Bearer invalid_token_here
# Should return 401

### Test with expired token
GET {{apiBase}}/finance/wallets/
Authorization: Bearer {{expiredToken}}
# Should return 401
```

### Data Isolation Tests
```http
### Test user can't access other user's data
GET {{apiBase}}/finance/wallets/{{otherUserWalletId}}/
Authorization: Bearer {{accessToken}}
# Should return 404 atau 403

### Test user can't modify other user's data
PUT {{apiBase}}/invest/portfolios/{{otherUserPortfolioId}}/
Authorization: Bearer {{accessToken}}
# Should return 404 atau 403
```

### Input Validation Tests
```http
### SQL Injection Test
GET {{apiBase}}/finance/transactions/?search='; DROP TABLE finance_transaction; --
Authorization: Bearer {{accessToken}}
# Should return safe response, not execute SQL

### XSS Test
POST {{apiBase}}/finance/categories/
Authorization: Bearer {{accessToken}}
Content-Type: application/json

{
  "name": "<script>alert('xss')</script>",
  "type": "expense"
}
# Should sanitize input
```

## 📋 Test Checklist

### ✅ Finance Module Checklist
- [ ] User registration & login
- [ ] Create wallets (all types)
- [ ] Create categories (income/expense)
- [ ] Create tags
- [ ] Create transactions (income/expense)
- [ ] Create transfers between wallets
- [ ] Test wallet balance calculations
- [ ] Test transaction summary
- [ ] Test monthly reports
- [ ] Test filtering & search
- [ ] Test pagination
- [ ] Test error scenarios

### ✅ Investment Module Checklist
- [ ] Create assets (all types)
- [ ] Add asset price data
- [ ] Create portfolios (different risk levels)
- [ ] Create buy transactions
- [ ] Verify holdings auto-creation
- [ ] Create sell transactions
- [ ] Create dividend transactions
- [ ] Test portfolio performance
- [ ] Test asset allocation
- [ ] Test rebalancing recommendations
- [ ] Test analytics endpoints
- [ ] Test bulk operations
- [ ] Test export functionality
- [ ] Test error scenarios

### ✅ Security Checklist
- [ ] Authentication required for all endpoints
- [ ] User data isolation
- [ ] Input validation
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] Rate limiting (if implemented)
- [ ] CORS headers (if needed)

## 🚨 Troubleshooting

### Server Not Starting
```bash
# Check if port is already in use
lsof -i :8000

# Kill existing process if needed
kill -9 <PID>

# Check for migration issues
python manage.py showmigrations
python manage.py migrate
```

### Database Issues
```bash
# Reset database (development only!)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser

# Check model consistency
python manage.py check
```

### API Not Responding
```bash
# Check Django logs
# Look for errors in terminal where runserver is running

# Test basic connectivity
curl http://localhost:8000/api/v1/auth/login/

# Check if URL patterns are correct
python manage.py show_urls
```

### Import Errors
```bash
# Check if all dependencies are installed
pip install -r requirements.txt

# Check for syntax errors
python manage.py check --deploy
```

## 📖 Best Practices

### 1. Test Organization
- Group related tests together
- Use descriptive test names
- Add comments for complex scenarios
- Organize by user workflow

### 2. Data Management
- Use realistic test data
- Clean up after destructive tests
- Keep test data consistent
- Document data dependencies

### 3. Error Handling
- Test both success and failure cases
- Verify error messages are helpful
- Test edge cases and boundary conditions
- Document expected error responses

### 4. Performance
- Test with realistic data volumes
- Monitor response times
- Test pagination with large datasets
- Verify database query efficiency

### 5. Security
- Always test authentication
- Verify user data isolation
- Test input validation thoroughly
- Check for common vulnerabilities

## 🎯 Quick Test Commands

```bash
# Start testing session
cd /Users/kaqfa/Documents/Project/Pribadi/journal-django/be
python manage.py runserver

# In VS Code:
# 1. Open finance_api.http or investment_api.http
# 2. Start with authentication requests
# 3. Update variables as you go
# 4. Follow the testing workflow
```

## 📞 Support

Jika ada masalah atau pertanyaan:
1. Check Django server logs untuk error details
2. Verify variable values di REST Client
3. Check network tab di browser dev tools
4. Review API documentation di Swagger (if available)
5. Test dengan simple curl commands untuk isolate issues

Happy testing! 🚀
