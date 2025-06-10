#!/bin/bash

# Migration Script untuk Registration Token System
echo "🚀 Creating migrations for Registration Token System"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run from Django project root."
    exit 1
fi

echo "📦 Creating migrations for master app..."

# Create migrations
python manage.py makemigrations master --name="add_registration_token_system"

if [ $? -eq 0 ]; then
    echo "✅ Migrations created successfully"
else
    echo "❌ Failed to create migrations"
    exit 1
fi

echo ""
echo "📊 Migration Summary:"
echo "- Added RegToken model with validation logic"
echo "- Added reg_token field to User model"
echo "- Updated admin interface for token management"
echo "- Enhanced authentication with token validation"
echo ""
echo "🔄 Next steps:"
echo "1. Run: python manage.py migrate"
echo "2. Create superuser if needed: python manage.py createsuperuser"
echo "3. Access admin panel to create registration tokens"
echo "4. Test registration with token validation"
echo ""
echo "📝 Admin Panel Usage:"
echo "- Go to http://localhost:8000/admin/"
echo "- Navigate to 'Registration Tokens'"
echo "- Create new tokens with unique codes"
echo "- Monitor token usage and manage users"
