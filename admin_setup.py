#!/usr/bin/env python3
"""
Admin Setup Script for Microfinance Platform
Run this script to create initial admin and staff accounts for production deployment
"""

from app import app, db, User
from werkzeug.security import generate_password_hash

def create_admin_accounts():
    """Create initial admin and staff accounts"""
    with app.app_context():
        # Check if admin already exists
        if User.query.filter_by(role='admin').first():
            print("Admin account already exists. Skipping setup.")
            return
        
        # Create System Administrator
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            full_name='System Administrator',
            email='admin@company.com',
            national_id='ADMIN001',
            occupation='Administrator',
            monthly_income=0,
            role='admin'
        )
        db.session.add(admin)
        
        print("Created System Administrator account:")
        print("  Username: admin")
        print("  Password: admin123")
        print("  Email: admin@company.com")
        print("\nIMPORTANT: Change these credentials after first login!")
        
        db.session.commit()
        print("\nAdmin account created successfully!")

if __name__ == '__main__':
    create_admin_accounts()
