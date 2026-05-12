<<<<<<< HEAD
# Microfinance Platform

A professional microfinance management system with role-based access control and complete loan workflow.

## Features

- **User Authentication**: Secure login and registration system
- **Role-Based Dashboard**: Different views for different user roles
- **Client Management**: Complete client registration and profile management
- **Loan Workflow**: Multi-stage approval system with audit trail
- **MySQL Database**: Production-ready database backend
- **Modern UI**: Responsive design with beautiful styling

## User Roles

1. **System Administrator**
   - System administration
   - User management
   - Complete system oversight

2. **General Director**
   - High-level oversight
   - Client analytics
   - Portfolio management

3. **Managing Director**
   - Final loan approvals
   - Strategic oversight
   - Branch management

4. **Loan Manager**
   - Loan application processing
   - Team supervision
   - Portfolio monitoring

5. **Loan Officer**
   - Field client management
   - Daily visit tracking
   - Client assignments

6. **Client**
   - Self-registration
   - Personal dashboard
   - Loan applications
   - Profile management

## Installation

1. Install MySQL Server and create database:
```bash
mysql -u root -p < database_setup.sql
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create initial admin account:
```bash
python admin_setup.py
```

4. Run the application:
```bash
python app.py
```

## Production Deployment

### Initial Setup
1. Run database setup script to create tables
2. Run admin_setup.py to create first administrator account
3. Change default admin password after first login
4. Create staff accounts through admin interface

### Security Notes
- Change default passwords immediately after first login
- Use strong passwords for production accounts
- Configure MySQL with proper user permissions
- Disable debug mode in production (already configured)
- Use HTTPS in production environment

3. Open your browser and navigate to `http://localhost:5000`

## Technology Stack

- **Backend**: Flask with SQLAlchemy
- **Frontend**: HTML5, CSS3 (pure server-side rendering - no JavaScript)
- **Database**: MySQL with PyMySQL
- **Styling**: Custom CSS with Font Awesome icons

## API Endpoints

- `GET /api/session` - Check authentication status
- `POST /api/login` - User login
- `POST /api/register` - New client registration
- `GET /api/dashboard` - Role-based dashboard data
- `POST /api/logout` - User logout

## File Structure

```
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── static/
│   └── index.html     # Frontend application
└── microfinance.db         # SQLite database (auto-created)
```

The application automatically creates demo data on first run, including sample users and clients for testing purposes.
=======
# Microfinance
>>>>>>> f73f048ae9981a3a6bfcf3eb56584dcb65f5c691
