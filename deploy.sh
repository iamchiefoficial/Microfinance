#!/bin/bash
# Microfinance Platform Deployment Script

echo "🚀 Starting Microfinance Platform Deployment..."

# Check if MySQL is running
if ! pgrep -x "mysqld" > /dev/null; then
    echo "❌ MySQL is not running. Please start MySQL service first."
    exit 1
fi

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Setup database
echo "🗄️ Setting up MySQL database..."
mysql -u root -p < database_setup.sql

# Create admin account
echo "👤 Creating admin account..."
python admin_setup.py

# Start the application
echo "🌐 Starting Microfinance Platform..."
echo "📍 Access your application at: http://localhost:5000"
echo "🔐 Admin credentials will be shown after setup completion"
echo ""
echo "✅ Deployment complete!"
echo "📝️  System Features:"
echo "   - Pure server-side rendering (no JavaScript)"
echo "   - MySQL database backend"
echo "   - Role-based access control"
echo "   - Complete loan approval workflow"
echo "   - Production-ready security"
echo ""
echo "📝️  Don't forget to:"
echo "   - Change default admin password"
echo "   - Configure proper environment variables"
echo "   - Set up HTTPS in production"
echo "   - Configure firewall rules"

# Start Flask application
python app.py
