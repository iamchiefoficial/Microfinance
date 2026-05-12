from flask import Flask, request, jsonify, session, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'microfinance_platform_2025_secure_key'

# MySQL Database Configuration
# Try common MySQL passwords - update if needed
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/microfinance_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    national_id = db.Column(db.String(50), unique=True, nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    monthly_income = db.Column(db.Float, nullable=False)
    role = db.Column(db.String(50), nullable=False, default='client')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='pending')
    current_stage = db.Column(db.String(50), default='loan_officer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    client = db.relationship('User', backref='loans')

class LoanApproval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    approver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stage = db.Column(db.String(50), nullable=False)
    decision = db.Column(db.String(20), nullable=False)  # 'approved' or 'rejected'
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    loan = db.relationship('Loan', backref='approvals')
    approver = db.relationship('User', backref='loan_decisions')

# Production system - no demo data
# Staff accounts should be created through admin interface or direct database insertion

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return render_template('login.html', message='Username and password are required', message_type='error-msg')
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', message='Invalid username or password', message_type='error-msg')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.form
    required_fields = ['fullName', 'email', 'nationalId', 'occupation', 'monthlyIncome', 'username', 'password']
    for field in required_fields:
        if not data.get(field, '').strip():
            return render_template('register.html', message=f'{field} is required', message_type='error-msg')
    
    if data.get('password') != data.get('confirmPassword'):
        return render_template('register.html', message='Passwords do not match', message_type='error-msg')
    
    if User.query.filter_by(username=data['username']).first():
        return render_template('register.html', message='Username already exists', message_type='error-msg')
    
    if User.query.filter_by(email=data['email']).first():
        return render_template('register.html', message='Email already registered', message_type='error-msg')
    
    if User.query.filter_by(national_id=data['nationalId']).first():
        return render_template('register.html', message='National ID already registered', message_type='error-msg')
    
    try:
        new_user = User(
            username=data['username'].strip(),
            password_hash=generate_password_hash(data['password']),
            full_name=data['fullName'].strip(),
            email=data['email'].strip(),
            national_id=data['nationalId'].strip(),
            occupation=data['occupation'].strip(),
            monthly_income=float(data['monthlyIncome']),
            role='client'
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return render_template('register.html', message='Registration successful! You can now login.', message_type='success-msg')
    
    except Exception as e:
        db.session.rollback()
        return render_template('register.html', message='Registration failed. Please try again.', message_type='error-msg')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required_fields = ['fullName', 'email', 'nationalId', 'occupation', 'monthlyIncome', 'username', 'password']
    for field in required_fields:
        if not data.get(field, '').strip():
            return jsonify({'success': False, 'message': f'{field} is required'})
    
    if data.get('password') != data.get('confirmPassword'):
        return jsonify({'success': False, 'message': 'Passwords do not match'})
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'success': False, 'message': 'Username already exists'})
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'message': 'Email already registered'})
    
    if User.query.filter_by(national_id=data['nationalId']).first():
        return jsonify({'success': False, 'message': 'National ID already registered'})
    
    try:
        new_user = User(
            username=data['username'].strip(),
            password_hash=generate_password_hash(data['password']),
            full_name=data['fullName'].strip(),
            email=data['email'].strip(),
            national_id=data['nationalId'].strip(),
            occupation=data['occupation'].strip(),
            monthly_income=float(data['monthlyIncome']),
            role='client'
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Registration failed. Please try again.'})

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))
    
    # DEBUG: Print the role to see what it actually is
    print(f"User role is: '{user.role}' (type: {type(user.role)})")
    
    total_clients = User.query.filter_by(role='client').count()
    
    # Role mapping that works with numbers OR strings
    role_mapping = {
        # String keys
        'admin': 'System Administrator',
        'general_director': 'General Director',
        'managing_director': 'Managing Director',
        'loan_manager': 'Loan Manager',
        'loan_officer': 'Loan Officer',
        'client': 'Client',
        # Number keys (if needed)
        1: 'System Administrator',
        2: 'General Director',
        3: 'Managing Director',
        4: 'Loan Manager',
        5: 'Loan Officer',
        6: 'Client'
    }
    
    # Handle both string and numeric roles
    role_name = role_mapping.get(user.role, f'Unknown Role: {user.role}')
    
    # Calculate dashboard statistics
    stats = {
        'total_clients': total_clients,
        'total_loans': Loan.query.count() if hasattr(Loan, 'query') else 0,
        'active_loans': Loan.query.filter_by(status='active').count() if hasattr(Loan, 'query') else 0,
        'total_revenue': db.session.query(db.func.sum(Loan.amount)).scalar() or 0 if hasattr(Loan, 'query') else 0
    }
    
    pending_loans = Loan.query.filter_by(status='pending').all() if hasattr(Loan, 'query') else []
    
    recent_clients = User.query.filter_by(role='client').order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                        user=user, 
                        role_name=role_name,
                        stats=stats,
                        recent_clients=recent_clients,
                        pending_loans=pending_loans)

    if user.role == 'admin':
        stats = [
            {'icon': 'fas fa-users', 'label': 'Total Clients', 'value': total_clients},
            {'icon': 'fas fa-user-tie', 'label': 'Staff Members', 'value': User.query.filter(User.role != 'client').count()},
            {'icon': 'fas fa-money-bill-wave', 'label': 'Total Monthly Income', 'value': "${:,.0f}".format(db.session.query(db.func.sum(User.monthly_income)).filter_by(role='client').scalar() or 0)}
        ]
    elif user.role == 'general_director':
        stats = [
            {'icon': 'fas fa-chart-line', 'label': 'Active Clients', 'value': total_clients},
            {'icon': 'fas fa-chart-bar', 'label': 'Avg Client Income', 'value': "${:,.0f}".format(db.session.query(db.func.avg(User.monthly_income)).filter_by(role='client').scalar() or 0)},
            {'icon': 'fas fa-hand-holding-usd', 'label': 'Loan Portfolio', 'value': "${:,.0f}".format(25000000)}
        ]
    elif user.role == 'managing_director':
        stats = [
            {'icon': 'fas fa-clock', 'label': 'Pending Approvals', 'value': 12},
            {'icon': 'fas fa-percent', 'label': 'Repayment Rate', 'value': '94.5%'},
            {'icon': 'fas fa-building', 'label': 'Active Branches', 'value': 3}
        ]
    elif user.role == 'loan_manager':
        stats = [
            {'icon': 'fas fa-file-alt', 'label': 'Pending Applications', 'value': 8},
            {'icon': 'fas fa-check-circle', 'label': 'Active Loans', 'value': 45},
            {'icon': 'fas fa-users', 'label': 'Total Borrowers', 'value': total_clients}
        ]
    elif user.role == 'loan_officer':
        stats = [
            {'icon': 'fas fa-calendar-day', 'label': "Today's Visits", 'value': 5},
            {'icon': 'fas fa-user-friends', 'label': 'Field Clients', 'value': 23},
            {'icon': 'fas fa-handshake', 'label': 'Active Assignments', 'value': 12}
        ]
    else:  # client
        stats = [
            {'icon': 'fas fa-wallet', 'label': 'Monthly Income', 'value': "${:,.0f}".format(user.monthly_income)},
            {'icon': 'fas fa-gem', 'label': 'Loan Eligibility', 'value': "${:,.0f}".format(user.monthly_income * 5)},
            {'icon': 'fas fa-chart-simple', 'label': 'Credit Score', 'value': 'Excellent'}
        ]
    
    # Get pending loans for staff - proper stage progression
    pending_loans = []
    if user.role in ['loan_officer', 'loan_manager', 'general_director', 'managing_director']:
        stage_mapping = {
            'loan_officer': 'loan_officer',
            'loan_manager': 'loan_manager',
            'general_director': 'general_director',
            'managing_director': 'managing_director'
        }
        
        # Only show loans at current user's stage
        pending_loans = Loan.query.filter_by(
            current_stage=stage_mapping[user.role],
            status='pending'
        ).all()
    
    # Define stage order globally
stage_order = ['loan_officer', 'loan_manager', 'general_director', 'managing_director']

# Get all loans for visibility (staff can see all loans in their department)
    all_visible_loans = []
    if user.role in ['loan_officer', 'loan_manager', 'general_director', 'managing_director']:
        # Staff can see all loans up to their current stage
        current_stage_index = stage_order.index(user.role) if user.role in stage_order else -1
        
        if current_stage_index >= 0:
            # Show all loans up to current stage
            for i in range(current_stage_index + 1):
                stage_loans = Loan.query.filter_by(current_stage=stage_order[i]).all()
                all_visible_loans.extend(stage_loans)
    
    return render_template('dashboard.html', 
                        user=user, 
                        role_name=role_name,
                        stats=stats,
                        recent_clients=recent_clients,
                        pending_loans=pending_loans)

@app.route('/loan/apply', methods=['POST'])
def apply_loan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if user.role != 'client':
        return redirect(url_for('dashboard'))
    
    amount = request.form.get('amount')
    purpose = request.form.get('purpose')
    
    if not amount or not purpose:
        return render_template('dashboard.html', 
                           user=user, 
                           role_name='Client',
                           stats=[
                               {'icon': 'fas fa-wallet', 'label': 'Monthly Income', 'value': "${:,.0f}".format(user.monthly_income)},
                               {'icon': 'fas fa-gem', 'label': 'Loan Eligibility', 'value': "${:,.0f}".format(user.monthly_income * 5)},
                               {'icon': 'fas fa-chart-simple', 'label': 'Credit Score', 'value': 'Excellent'}
                           ],
                           recent_clients=[],
                           pending_loans=[],
                           loan_message='Please fill in all fields',
                           loan_message_type='error-msg')
    
    loan = Loan(
        client_id=user.id,
        amount=float(amount),
        purpose=purpose.strip(),
        status='pending',
        current_stage='loan_officer'
    )
    
    db.session.add(loan)
    db.session.commit()
    
    return render_template('dashboard.html', 
                       user=user, 
                       role_name='Client',
                       stats=[
                           {'icon': 'fas fa-wallet', 'label': 'Monthly Income', 'value': "${:,.0f}".format(user.monthly_income)},
                           {'icon': 'fas fa-gem', 'label': 'Loan Eligibility', 'value': "${:,.0f}".format(user.monthly_income * 5)},
                           {'icon': 'fas fa-chart-simple', 'label': 'Credit Score', 'value': 'Excellent'}
                       ],
                       recent_clients=[],
                       pending_loans=[],
                       loan_message='Loan application submitted successfully!',
                       loan_message_type='success-msg')

@app.route('/api/loan/pending', methods=['GET'])
def get_pending_loans():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    user = User.query.get(session['user_id'])
    if user.role not in ['loan_officer', 'loan_manager', 'general_director', 'managing_director']:
        return jsonify({'success': False, 'message': 'Access denied'})
    
    stage_mapping = {
        'loan_officer': 'loan_officer',
        'loan_manager': 'loan_manager',
        'general_director': 'general_director',
        'managing_director': 'managing_director'
    }
    
    loans = Loan.query.filter_by(
        current_stage=stage_mapping[user.role],
        status='pending'
    ).all()
    
    loans_data = []
    for loan in loans:
        loans_data.append({
            'id': loan.id,
            'client_name': loan.client.full_name,
            'amount': loan.amount,
            'purpose': loan.purpose,
            'created_at': loan.created_at.isoformat()
        })
    
    return jsonify({'success': True, 'loans': loans_data})

@app.route('/loan/approve', methods=['POST'])
def approve_loan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if user.role not in ['loan_officer', 'loan_manager', 'general_director', 'managing_director']:
        return redirect(url_for('dashboard'))
    
    loan_id = request.form.get('loan_id')
    decision = request.form.get('decision')  # 'approved' or 'rejected'
    comments = request.form.get('comments', '')
    reason = request.form.get('reason', '')
    
    if not loan_id or decision not in ['approved', 'rejected']:
        return redirect(url_for('dashboard'))
    
    loan = Loan.query.get(loan_id)
    if not loan:
        return redirect(url_for('dashboard'))
    
    # Ensure loan is at current user's stage
    if loan.current_stage != user.role:
        return redirect(url_for('dashboard'))
    
    # Stage progression order
    stage_order = ['loan_officer', 'loan_manager', 'general_director', 'managing_director']
    current_stage_index = stage_order.index(loan.current_stage)
    
    if decision == 'approved':
        # Move to next stage if not final
        if current_stage_index < len(stage_order) - 1:
            loan.current_stage = stage_order[current_stage_index + 1]
            loan.status = 'pending'  # Still pending until final approval
            message = f"Loan approved by {user.role} and forwarded to {stage_order[current_stage_index + 1]}"
        else:
            # Final approval
            loan.status = 'approved'
            # Create disbursement transaction
            transaction = Transaction(
                loan_id=loan.id,
                amount=loan.amount,
                transaction_type='disbursement',
                balance_after=loan.amount,
                notes=f"Final approval by {user.role}. {comments}"
            )
            db.session.add(transaction)
            message = f"Loan finally approved by {user.role}. {comments}"
    
    elif decision == 'rejected':
        loan.status = 'rejected'
        # Create rejection transaction
        transaction = Transaction(
            loan_id=loan.id,
            amount=0,
            transaction_type='rejection',
            balance_after=loan.amount,
            notes=f"Rejected by {user.role}. Reason: {reason}. {comments}"
        )
        db.session.add(transaction)
        message = f"Loan rejected by {user.role}. Reason: {reason}. {comments}"
    
    # Update loan metadata
    loan.updated_at = datetime.utcnow()
    loan.approved_by = user.role  # Track who approved/rejected
    
    db.session.commit()
    
    # Flash message for user
    flash(message)
    
    return redirect(url_for('dashboard'))
    
    approval = LoanApproval(
        loan_id=loan_id,
        approver_id=user.id,
        stage=user.role,
        decision=decision,
        comments=comments
    )
    db.session.add(approval)
    
    if decision == 'approved':
        stage_order = ['loan_officer', 'loan_manager', 'general_director', 'managing_director']
        current_index = stage_order.index(loan.current_stage)
        
        if current_index < len(stage_order) - 1:
            loan.current_stage = stage_order[current_index + 1]
        else:
            loan.status = 'approved'
    else:
        stage_order = ['loan_officer', 'loan_manager', 'general_director', 'managing_director']
        current_index = stage_order.index(loan.current_stage)
        
        if current_index > 0:
            loan.current_stage = stage_order[current_index - 1]
        else:
            loan.status = 'rejected'
    
    loan.updated_at = datetime.utcnow()
    db.session.commit()
    
    return redirect(url_for('dashboard'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

from waitress import serve

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Database connection error: {e}")
            print("Please ensure MySQL is running and database 'microfinance_db' exists.")
            print("Run: mysql -u root -p < database_setup.sql")
    
    serve(app, host="0.0.0.0", port=9000)
