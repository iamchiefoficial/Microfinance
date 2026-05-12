# Fixed Microfinance Platform with Proper Loan Approval Workflow
from flask import Flask, request, jsonify, session, render_template_string, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import pymysql
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'microfinance_platform_2025_secure_key'

# MySQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/microfinance_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    national_id = db.Column(db.String(50), unique=True, nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    monthly_income = db.Column(db.Numeric(12,2), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    role = db.Column(db.String(50), default='client')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Loan Model
class Loan(db.Model):
    __tablename__ = 'loans'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String(200))
    status = db.Column(db.String(50), default='pending')  # pending, approved, rejected, disbursed
    current_stage = db.Column(db.String(50), default='loan_officer')  # loan_officer, loan_manager, managing_director, general_director, completed
    interest_rate = db.Column(db.Float, default=10.0)
    term_months = db.Column(db.Integer, nullable=False)
    monthly_payment = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Approval tracking
    loan_officer_approved = db.Column(db.Boolean, default=False)
    loan_officer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    loan_officer_approved_at = db.Column(db.DateTime, nullable=True)
    
    loan_manager_approved = db.Column(db.Boolean, default=False)
    loan_manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    loan_manager_approved_at = db.Column(db.DateTime, nullable=True)
    
    managing_director_approved = db.Column(db.Boolean, default=False)
    managing_director_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    managing_director_approved_at = db.Column(db.DateTime, nullable=True)
    
    general_director_approved = db.Column(db.Boolean, default=False)
    general_director_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    general_director_approved_at = db.Column(db.DateTime, nullable=True)
    
    rejection_reason = db.Column(db.Text, nullable=True)
    rejected_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    rejected_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    client = db.relationship('User', foreign_keys=[client_id], backref='loans')
    loan_officer = db.relationship('User', foreign_keys=[loan_officer_id])
    loan_manager = db.relationship('User', foreign_keys=[loan_manager_id])
    managing_director = db.relationship('User', foreign_keys=[managing_director_id])
    general_director = db.relationship('User', foreign_keys=[general_director_id])
    rejected_by_user = db.relationship('User', foreign_keys=[rejected_by])
    
    def get_current_stage_name(self):
        stages = {
            'loan_officer': 'Loan Officer Review',
            'loan_manager': 'Loan Manager Review',
            'managing_director': 'Managing Director Review',
            'general_director': 'General Director Review',
            'completed': 'Approved - Ready for Disbursement'
        }
        return stages.get(self.current_stage, 'Unknown Stage')
    
    def get_next_stage(self):
        stages_order = ['loan_officer', 'loan_manager', 'managing_director', 'general_director', 'completed']
        current_index = stages_order.index(self.current_stage) if self.current_stage in stages_order else 0
        return stages_order[current_index + 1] if current_index + 1 < len(stages_order) else 'completed'
    
    def can_approve(self, user_role):
        approval_map = {
            'loan_officer': self.current_stage == 'loan_officer' and not self.loan_officer_approved,
            'loan_manager': self.current_stage == 'loan_manager' and not self.loan_manager_approved,
            'managing_director': self.current_stage == 'managing_director' and not self.managing_director_approved,
            'general_director': self.current_stage == 'general_director' and not self.general_director_approved
        }
        return approval_map.get(user_role, False)

# Group Loan Model
class GroupLoan(db.Model):
    __tablename__ = 'group_loans'
    
    id = db.Column(db.Integer, primary_key=True)
    # Section 1: Applicant Info
    applicant_full_name = db.Column(db.String(200), nullable=False)
    applicant_known_name = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    id_type = db.Column(db.String(50))
    id_number = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    phone = db.Column(db.String(20))
    marital_status = db.Column(db.String(50))
    residence_area = db.Column(db.String(200))
    residence_since = db.Column(db.String(50))
    residence_ownership = db.Column(db.String(50))
    spouse_full_name = db.Column(db.String(200))
    spouse_known_name = db.Column(db.String(100))
    spouse_birth_date = db.Column(db.Date)
    dependents_count = db.Column(db.Integer)
    spouse_phone = db.Column(db.String(20))
    
    # Section 2: Group Info
    group_chairperson = db.Column(db.String(200))
    group_secretary = db.Column(db.String(200))
    group_address = db.Column(db.String(500))
    group_reg_number = db.Column(db.String(100))
    region = db.Column(db.String(100))
    district = db.Column(db.String(100))
    ward = db.Column(db.String(100))
    village = db.Column(db.String(100))
    male_members = db.Column(db.Integer, default=0)
    female_members = db.Column(db.Integer, default=0)
    registration_date = db.Column(db.Date)
    group_phone1 = db.Column(db.String(20))
    group_phone2 = db.Column(db.String(20))
    
    # Section 3: Project Info
    project_name = db.Column(db.String(200))
    project_type = db.Column(db.String(200))
    project_location = db.Column(db.String(500))
    project_ward = db.Column(db.String(100))
    project_district = db.Column(db.String(100))
    monthly_income = db.Column(db.Float)
    monthly_expenses = db.Column(db.Float)
    project_start_date = db.Column(db.Date)
    
    # Section 4: Loan Details
    loan_amount = db.Column(db.Float, nullable=False)
    repayment_period = db.Column(db.Integer)  # in months
    affordable_repayment = db.Column(db.Float)
    loan_purpose = db.Column(db.Text)
    group_existing_debt = db.Column(db.Float, default=0)
    previous_loan = db.Column(db.Boolean, default=False)
    income_source = db.Column(db.String(200))
    
    # Section 5: Guarantor 1 (Chairperson)
    guarantor1_full_name = db.Column(db.String(200))
    guarantor1_residence = db.Column(db.String(500))
    guarantor1_house_number = db.Column(db.String(50))
    guarantor1_rent_status = db.Column(db.String(50))
    guarantor1_occupation = db.Column(db.String(200))
    guarantor1_office_location = db.Column(db.String(500))
    guarantor1_company = db.Column(db.String(200))
    guarantor1_phone = db.Column(db.String(20))
    
    # Section 6: Guarantor 2 (Spouse/Relative)
    guarantor2_full_name = db.Column(db.String(200))
    guarantor2_residence = db.Column(db.String(500))
    guarantor2_house_number = db.Column(db.String(50))
    guarantor2_rent_status = db.Column(db.String(50))
    guarantor2_occupation = db.Column(db.String(200))
    guarantor2_office_location = db.Column(db.String(500))
    guarantor2_company = db.Column(db.String(200))
    guarantor2_phone = db.Column(db.String(20))
    guarantor2_relationship = db.Column(db.String(50))
    
    # Collateral Info (JSON field for multiple collaterals)
    collateral_info = db.Column(db.Text)  # Store as JSON string
    
    # Signatures and declarations
    applicant_signature = db.Column(db.String(500))  # Store signature path or base64
    applicant_date = db.Column(db.Date)
    applicant_thumbprint = db.Column(db.String(500))
    
    guarantor1_signature = db.Column(db.String(500))
    guarantor1_thumbprint = db.Column(db.String(500))
    
    guarantor2_signature = db.Column(db.String(500))
    guarantor2_thumbprint = db.Column(db.String(500))
    guarantor2_relationship_declared = db.Column(db.String(100))
    
    # Workflow fields
    status = db.Column(db.String(50), default='pending')
    current_stage = db.Column(db.String(50), default='loan_officer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Approval tracking
    loan_officer_approved = db.Column(db.Boolean, default=False)
    loan_officer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    loan_officer_approved_at = db.Column(db.DateTime)
    
    loan_manager_approved = db.Column(db.Boolean, default=False)
    loan_manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    loan_manager_approved_at = db.Column(db.DateTime)
    
    managing_director_approved = db.Column(db.Boolean, default=False)
    managing_director_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    managing_director_approved_at = db.Column(db.DateTime)
    
    general_director_approved = db.Column(db.Boolean, default=False)
    general_director_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    general_director_approved_at = db.Column(db.DateTime)
    
    # Rejection tracking
    rejection_reason = db.Column(db.Text, nullable=True)
    rejected_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    rejected_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    client = db.relationship('User', foreign_keys=[client_id], backref='group_loans')
    loan_officer = db.relationship('User', foreign_keys=[loan_officer_id])
    loan_manager = db.relationship('User', foreign_keys=[loan_manager_id])
    managing_director = db.relationship('User', foreign_keys=[managing_director_id])
    general_director = db.relationship('User', foreign_keys=[general_director_id])
    rejected_by_user = db.relationship('User', foreign_keys=[rejected_by])
    
    def get_current_stage_name(self):
        stages = {
            'loan_officer': 'Loan Officer Review',
            'loan_manager': 'Loan Manager Review',
            'managing_director': 'Managing Director Review',
            'general_director': 'General Director Review',
            'completed': 'Approved - Ready for Disbursement'
        }
        return stages.get(self.current_stage, 'Unknown Stage')
    
    def get_next_stage(self):
        stages_order = ['loan_officer', 'loan_manager', 'managing_director', 'general_director', 'completed']
        current_index = stages_order.index(self.current_stage) if self.current_stage in stages_order else 0
        return stages_order[current_index + 1] if current_index + 1 < len(stages_order) else 'completed'
    
    def can_approve(self, user_role):
        approval_map = {
            'loan_officer': self.current_stage == 'loan_officer' and not self.loan_officer_approved,
            'loan_manager': self.current_stage == 'loan_manager' and not self.loan_manager_approved,
            'managing_director': self.current_stage == 'managing_director' and not self.managing_director_approved,
            'general_director': self.current_stage == 'general_director' and not self.general_director_approved
        }
        return approval_map.get(user_role, False)

# Transaction Model
class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    amount = db.Column(db.Numeric(12,2), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    balance_after = db.Column(db.Numeric(12,2))
    notes = db.Column(db.Text)
    
    loan = db.relationship('Loan', backref='transactions')

# Create staff accounts
def create_staff_accounts():
    try:
        staff_accounts = [
            ('System Administrator', 'admin@microfinance.com', 'ADMIN001', 'Administrator', 'admin'),
            ('General Director', 'director@microfinance.com', 'DIR001', 'General Director', 'general_director'),
            ('Managing Director', 'md@microfinance.com', 'MD001', 'Managing Director', 'managing_director'),
            ('Loan Manager', 'lm@microfinance.com', 'LM001', 'Loan Manager', 'loan_manager'),
            ('Loan Officer', 'lo@microfinance.com', 'LO001', 'Loan Officer', 'loan_officer')
        ]
        
        password_hash = generate_password_hash('mf@123')
        
        for username, email, national_id, occupation, role in staff_accounts:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                user = User(
                    username=username,
                    password_hash=password_hash,
                    full_name=username,
                    email=email,
                    national_id=national_id,
                    occupation=occupation,
                    monthly_income=5000.0,
                    role=role
                )
                db.session.add(user)
                print(f"✅ Created staff account: {username}")
        
        db.session.commit()
        print("✅ Staff accounts created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating staff accounts: {e}")

# Define stage order globally
stage_order = ['loan_officer', 'loan_manager', 'general_director', 'managing_director']

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f"\n=== LOGIN ATTEMPT ===")
        print(f"Username: '{username}'")
        print(f"Password: '{password}'")
        
        try:
            # Find user by username (this was the bug - it was checking session instead)
            user = User.query.filter_by(username=username).first()
            
            if user:
                print(f"✅ User found in database!")
                print(f"  - Username: {user.username}")
                print(f"  - Role: {user.role}")
                print(f"  - Password hash: {user.password_hash[:20]}...")
                
                # Check password
                password_valid = check_password_hash(user.password_hash, password)
                print(f"  - Password valid: {password_valid}")
                
                if password_valid:
                    session['user_id'] = user.id
                    session['username'] = user.username
                    session['role'] = user.role
                    print(f"✅ Login successful! Redirecting to dashboard...")
                    flash(f'Welcome {user.username}!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    print(f"❌ Password invalid for user: {username}")
            else:
                print(f"❌ User '{username}' NOT found in database!")
                # List all users for debugging
                all_users = User.query.all()
                print(f"Available users: {[u.username for u in all_users]}")
            
            flash('Invalid username or password!', 'danger')
        except Exception as e:
            print(f"Login error: {e}")
            flash('Login error occurred')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Role is automatically set to 'client'
        role = 'client'
        
        # Validation
        errors = []
        
        if not username:
            errors.append('Username is required')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters')
            
        if not email:
            errors.append('Email is required')
        elif '@' not in email:
            errors.append('Invalid email address')
            
        if not full_name:
            errors.append('Full name is required')
            
        if not phone:
            errors.append('Phone number is required')
            
        if not password:
            errors.append('Password is required')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters')
            
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            errors.append('Username already exists. Please choose another')
        
        # If errors, show them and return to form with data
        if errors:
            for error in errors:
                flash(error, 'danger')
            # Return with form data preserved via request.form
            return render_template('register.html'), 400
        
        # Create new user with additional fields
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            phone=phone,
            address=address,
            password_hash=generate_password_hash(password),
            role=role,
            monthly_income=5000.0,  # Default income
            national_id=f"ID{username.upper()}",  # Generate default ID
            occupation=role.replace('_', ' ').title(),  # Default occupation
            created_at=datetime.utcnow()
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('✅ Registration successful! Please login with your credentials.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration error: {str(e)}', 'danger')
            return render_template('register.html'), 500
    
    # GET request - show empty form
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if not user:
        return redirect(url_for('login'))
    
    # Redirect based on user role
    if user.role == 'client':
        return redirect(url_for('client_dashboard'))
    else:
        return redirect(url_for('staff_dashboard'))

@app.route('/client_dashboard')
def client_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if not user or user.role != 'client':
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))
    
    # Get client-specific data
    loans = Loan.query.filter_by(client_id=user.id).order_by(Loan.created_at.desc()).all()
    group_loans = GroupLoan.query.filter_by(client_id=user.id).order_by(GroupLoan.created_at.desc()).all()
    
    # Calculate client statistics
    total_individual_loans = len(loans)
    total_group_loans = len(group_loans)
    total_loans = total_individual_loans + total_group_loans
    active_loans = len([l for l in loans if l.status == 'active']) + len([gl for gl in group_loans if gl.status == 'active'])
    completed_loans = len([l for l in loans if l.status == 'completed']) + len([gl for gl in group_loans if gl.status == 'completed'])
    
    return render_template('client_dashboard.html', 
                         user=user,
                         loans=loans,
                         group_loans=group_loans,
                         total_individual_loans=total_individual_loans,
                         total_group_loans=total_group_loans,
                         total_loans=total_loans,
                         active_loans=active_loans,
                         completed_loans=completed_loans)

@app.route('/staff_dashboard')
def staff_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if not user or user.role == 'client':
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))
    
    # Debug: Print to terminal
    print(f"\n=== STAFF DASHBOARD ===")
    print(f"Logged in as: {user.username} (Role: {user.role})")
    
    # Get all loans that need approval based on role
    if user.role == 'loan_officer':
        # Get individual loans at loan_officer stage
        pending_loans = Loan.query.filter(
            Loan.current_stage == 'loan_officer',
            Loan.loan_officer_approved == False,
            Loan.status == 'pending'
        ).all()
        # Get group loans at loan_officer stage
        pending_group_loans = GroupLoan.query.filter(
            GroupLoan.current_stage == 'loan_officer',
            GroupLoan.loan_officer_approved == False,
            GroupLoan.status == 'pending'
        ).all()
        print(f"Found {len(pending_loans)} individual loans and {len(pending_group_loans)} group loans pending for Loan Officer")
        
    elif user.role == 'loan_manager':
        # Get individual loans at loan_manager stage
        pending_loans = Loan.query.filter(
            Loan.current_stage == 'loan_manager',
            Loan.loan_manager_approved == False,
            Loan.status == 'pending'
        ).all()
        # Get group loans at loan_manager stage
        pending_group_loans = GroupLoan.query.filter(
            GroupLoan.current_stage == 'loan_manager',
            GroupLoan.loan_manager_approved == False,
            GroupLoan.status == 'pending'
        ).all()
        print(f"Found {len(pending_loans)} individual loans and {len(pending_group_loans)} group loans pending for Loan Manager")
        
    elif user.role == 'managing_director':
        # Get individual loans at managing_director stage
        pending_loans = Loan.query.filter(
            Loan.current_stage == 'managing_director',
            Loan.managing_director_approved == False,
            Loan.status == 'pending'
        ).all()
        # Get group loans at managing_director stage
        pending_group_loans = GroupLoan.query.filter(
            GroupLoan.current_stage == 'managing_director',
            GroupLoan.managing_director_approved == False,
            GroupLoan.status == 'pending'
        ).all()
        print(f"Found {len(pending_loans)} individual loans and {len(pending_group_loans)} group loans pending for Managing Director")
        
    elif user.role == 'general_director':
        # Get individual loans at general_director stage
        pending_loans = Loan.query.filter(
            Loan.current_stage == 'general_director',
            Loan.general_director_approved == False,
            Loan.status == 'pending'
        ).all()
        # Get group loans at general_director stage
        pending_group_loans = GroupLoan.query.filter(
            GroupLoan.current_stage == 'general_director',
            GroupLoan.general_director_approved == False,
            GroupLoan.status == 'pending'
        ).all()
        print(f"Found {len(pending_loans)} individual loans and {len(pending_group_loans)} group loans pending for General Director")
        
    else:
        pending_loans = []
        pending_group_loans = []
        print(f"No specific pending loans for role: {user.role}")
    
    # Print each pending loan for debugging
    for loan in pending_loans:
        print(f"  - Individual Loan #{loan.id}: Amount=${loan.amount}, Stage={loan.current_stage}, Client={loan.client.username}")
    for group_loan in pending_group_loans:
        print(f"  - Group Loan #{group_loan.id}: Amount=${group_loan.loan_amount}, Stage={group_loan.current_stage}, Applicant={group_loan.applicant_full_name}")
    
    all_clients = User.query.filter_by(role='client').all()
    total_clients = len(all_clients)
    total_loans = Loan.query.count() + GroupLoan.query.count()
    pending_for_me = len(pending_loans) + len(pending_group_loans)
    
    return render_template('staff_dashboard.html',
                         user=user,
                         total_clients=total_clients,
                         total_loans=total_loans,
                         pending_for_me=pending_for_me,
                         pending_loans=pending_loans,
                         pending_group_loans=pending_group_loans,
                         all_clients=all_clients)

@app.route('/apply_loan', methods=['POST'])
def apply_loan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if not user or user.role != 'client':
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))
    
    amount = float(request.form.get('amount'))
    purpose = request.form.get('purpose')
    term_months = int(request.form.get('term_months'))
    
    # Calculate interest rate (example: 10% per year)
    interest_rate = 10.0
    monthly_payment = (amount * (interest_rate/100) / 12 * term_months + amount) / term_months
    
    new_loan = Loan(
        client_id=user.id,
        amount=amount,
        purpose=purpose,
        term_months=term_months,
        interest_rate=interest_rate,
        monthly_payment=monthly_payment,
        status='pending',
        created_at=datetime.now()
    )
    
    db.session.add(new_loan)
    db.session.commit()
    
    flash('Loan application submitted successfully!', 'success')
    return redirect(url_for('client_dashboard'))

@app.route('/apply_group_loan')
def apply_group_loan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if not user or user.role != 'client':
        flash('Only clients can apply for group loans!', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('group_loan_form.html')

@app.route('/submit_group_loan', methods=['POST'])
def submit_group_loan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if not user or user.role != 'client':
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))
    
    try:
        # Collect collateral info
        collateral_types = request.form.getlist('collateral_type[]')
        collateral_reg_nos = request.form.getlist('collateral_reg_no[]')
        collateral_values = request.form.getlist('collateral_value[]')
        collateral_current_values = request.form.getlist('collateral_current_value[]')
        collateral_ages = request.form.getlist('collateral_age[]')
        collateral_owners = request.form.getlist('collateral_owner[]')
        collateral_colors = request.form.getlist('collateral_color[]')
        collateral_locations = request.form.getlist('collateral_location[]')
        
        # Build collateral JSON
        collateral_list = []
        for i in range(len(collateral_types)):
            if collateral_types[i].strip():  # Only add if there's data
                collateral_list.append({
                    'type': collateral_types[i],
                    'reg_no': collateral_reg_nos[i],
                    'value': float(collateral_values[i]) if collateral_values[i] else 0,
                    'current_value': float(collateral_current_values[i]) if collateral_current_values[i] else 0,
                    'age': int(collateral_ages[i]) if collateral_ages[i] else 0,
                    'owner': collateral_owners[i],
                    'color': collateral_colors[i],
                    'location': collateral_locations[i]
                })
        
        # Create new group loan
        new_group_loan = GroupLoan(
            # Section 1: Applicant Info
            applicant_full_name=request.form.get('applicant_full_name'),
            applicant_known_name=request.form.get('applicant_known_name'),
            gender=request.form.get('gender'),
            id_type=request.form.get('id_type'),
            id_number=request.form.get('id_number'),
            birth_date=datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date() if request.form.get('birth_date') else None,
            phone=request.form.get('phone'),
            marital_status=request.form.get('marital_status'),
            residence_area=request.form.get('residence_area'),
            residence_since=request.form.get('residence_since'),
            residence_ownership=request.form.get('residence_ownership'),
            spouse_full_name=request.form.get('spouse_full_name'),
            spouse_known_name=request.form.get('spouse_known_name'),
            spouse_birth_date=datetime.strptime(request.form.get('spouse_birth_date'), '%Y-%m-%d').date() if request.form.get('spouse_birth_date') else None,
            dependents_count=int(request.form.get('dependents_count')) if request.form.get('dependents_count') else 0,
            spouse_phone=request.form.get('spouse_phone'),
            
            # Section 2: Group Info
            group_chairperson=request.form.get('group_chairperson'),
            group_secretary=request.form.get('group_secretary'),
            group_address=request.form.get('group_address'),
            group_reg_number=request.form.get('group_reg_number'),
            region=request.form.get('region'),
            district=request.form.get('district'),
            ward=request.form.get('ward'),
            village=request.form.get('village'),
            male_members=int(request.form.get('male_members')) if request.form.get('male_members') else 0,
            female_members=int(request.form.get('female_members')) if request.form.get('female_members') else 0,
            registration_date=datetime.strptime(request.form.get('registration_date'), '%Y-%m-%d').date() if request.form.get('registration_date') else None,
            group_phone1=request.form.get('group_phone1'),
            group_phone2=request.form.get('group_phone2'),
            
            # Section 3: Project Info
            project_name=request.form.get('project_name'),
            project_type=request.form.get('project_type'),
            project_location=request.form.get('project_location'),
            project_ward=request.form.get('project_ward'),
            project_district=request.form.get('project_district'),
            monthly_income=float(request.form.get('monthly_income')) if request.form.get('monthly_income') else 0,
            monthly_expenses=float(request.form.get('monthly_expenses')) if request.form.get('monthly_expenses') else 0,
            project_start_date=datetime.strptime(request.form.get('project_start_date'), '%Y-%m-%d').date() if request.form.get('project_start_date') else None,
            
            # Section 4: Loan Details
            loan_amount=float(request.form.get('loan_amount')),
            repayment_period=int(request.form.get('repayment_period')) if request.form.get('repayment_period') else 0,
            affordable_repayment=float(request.form.get('affordable_repayment')) if request.form.get('affordable_repayment') else 0,
            loan_purpose=request.form.get('loan_purpose'),
            group_existing_debt=float(request.form.get('group_existing_debt')) if request.form.get('group_existing_debt') else 0,
            previous_loan=request.form.get('previous_loan') == 'true',
            income_source=request.form.get('income_source'),
            
            # Section 5: Guarantor 1
            guarantor1_full_name=request.form.get('guarantor1_full_name'),
            guarantor1_residence=request.form.get('guarantor1_residence'),
            guarantor1_house_number=request.form.get('guarantor1_house_number'),
            guarantor1_rent_status=request.form.get('guarantor1_rent_status'),
            guarantor1_occupation=request.form.get('guarantor1_occupation'),
            guarantor1_office_location=request.form.get('guarantor1_office_location'),
            guarantor1_company=request.form.get('guarantor1_company'),
            guarantor1_phone=request.form.get('guarantor1_phone'),
            
            # Section 6: Guarantor 2
            guarantor2_full_name=request.form.get('guarantor2_full_name'),
            guarantor2_residence=request.form.get('guarantor2_residence'),
            guarantor2_house_number=request.form.get('guarantor2_house_number'),
            guarantor2_rent_status=request.form.get('guarantor2_rent_status'),
            guarantor2_occupation=request.form.get('guarantor2_occupation'),
            guarantor2_office_location=request.form.get('guarantor2_office_location'),
            guarantor2_company=request.form.get('guarantor2_company'),
            guarantor2_phone=request.form.get('guarantor2_phone'),
            guarantor2_relationship=request.form.get('guarantor2_relationship'),
            
            # Collateral Info
            collateral_info=json.dumps(collateral_list),
            
            # Signatures and declarations
            applicant_signature=request.form.get('applicant_signature'),
            applicant_date=datetime.strptime(request.form.get('applicant_date'), '%Y-%m-%d').date() if request.form.get('applicant_date') else None,
            applicant_thumbprint=request.form.get('applicant_thumbprint'),
            guarantor1_signature=request.form.get('guarantor1_signature'),
            guarantor1_thumbprint=request.form.get('guarantor1_thumbprint'),
            guarantor2_signature=request.form.get('guarantor2_signature'),
            guarantor2_thumbprint=request.form.get('guarantor2_thumbprint'),
            guarantor2_relationship_declared=request.form.get('guarantor2_declaration_relationship'),
            
            # Workflow fields
            client_id=user.id,
            status='pending',
            current_stage='loan_officer'
        )
        
        db.session.add(new_group_loan)
        db.session.commit()
        
        flash('🎉 Group loan application submitted successfully! Your application is now under review.', 'success')
        return redirect(url_for('client_dashboard'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error submitting group loan application: {str(e)}', 'danger')
        return redirect(url_for('apply_group_loan'))

@app.route('/approve_loan/<int:loan_id>', methods=['POST'])
def approve_loan(loan_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    loan = Loan.query.get_or_404(loan_id)
    
    # Check if user can approve based on role and current stage
    if user.role == 'loan_officer' and loan.current_stage == 'loan_officer' and not loan.loan_officer_approved:
        loan.loan_officer_approved = True
        loan.loan_officer_id = user.id
        loan.loan_officer_approved_at = datetime.now()
        loan.current_stage = 'loan_manager'
        flash(f'✅ Loan #{loan.id} approved by Loan Officer. Moving to Loan Manager for review.', 'success')
        
    elif user.role == 'loan_manager' and loan.current_stage == 'loan_manager' and not loan.loan_manager_approved:
        loan.loan_manager_approved = True
        loan.loan_manager_id = user.id
        loan.loan_manager_approved_at = datetime.now()
        loan.current_stage = 'managing_director'
        flash(f'✅ Loan #{loan.id} approved by Loan Manager. Moving to Managing Director for final review.', 'success')
        
    elif user.role == 'managing_director' and loan.current_stage == 'managing_director' and not loan.managing_director_approved:
        loan.managing_director_approved = True
        loan.managing_director_id = user.id
        loan.managing_director_approved_at = datetime.now()
        loan.current_stage = 'general_director'
        flash(f'✅ Loan #{loan.id} approved by Managing Director. Moving to General Director for disbursement.', 'success')
        
    elif user.role == 'general_director' and loan.current_stage == 'general_director' and not loan.general_director_approved:
        loan.general_director_approved = True
        loan.general_director_id = user.id
        loan.general_director_approved_at = datetime.now()
        loan.status = 'approved'
        loan.current_stage = 'completed'
        flash(f'🎉 Loan #{loan.id} has been FULLY APPROVED! Ready for disbursement.', 'success')
        
    else:
        flash(f'⚠️ You cannot approve this loan at the current stage.', 'warning')
        return redirect(url_for('staff_dashboard'))
    
    db.session.commit()
    return redirect(url_for('staff_dashboard'))

@app.route('/reject_loan/<int:loan_id>', methods=['POST'])
def reject_loan(loan_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    loan = Loan.query.get_or_404(loan_id)
    rejection_reason = request.form.get('rejection_reason', 'No reason provided')
    
    # Determine which stage is rejecting
    current_stage = loan.current_stage
    
    if current_stage == 'loan_officer' and user.role == 'loan_officer':
        loan.status = 'rejected'
        loan.rejection_reason = f"Rejected by Loan Officer: {rejection_reason}"
        loan.rejected_by = user.id
        loan.rejected_at = datetime.now()
        flash(f'❌ Loan #{loan.id} rejected by Loan Officer.', 'danger')
        
    elif current_stage == 'loan_manager' and user.role == 'loan_manager':
        # Move back to loan officer
        loan.current_stage = 'loan_officer'
        loan.loan_officer_approved = False
        loan.loan_officer_id = None
        loan.loan_officer_approved_at = None
        loan.rejection_reason = f"Sent back by Loan Manager: {rejection_reason}"
        flash(f'🔄 Loan #{loan.id} sent back to Loan Officer for revision.', 'warning')
        
    elif current_stage == 'managing_director' and user.role == 'managing_director':
        # Move back to loan manager
        loan.current_stage = 'loan_manager'
        loan.loan_manager_approved = False
        loan.loan_manager_id = None
        loan.loan_manager_approved_at = None
        loan.rejection_reason = f"Sent back by Managing Director: {rejection_reason}"
        flash(f'🔄 Loan #{loan.id} sent back to Loan Manager for revision.', 'warning')
        
    elif current_stage == 'general_director' and user.role == 'general_director':
        # Move back to managing director
        loan.current_stage = 'managing_director'
        loan.managing_director_approved = False
        loan.managing_director_id = None
        loan.managing_director_approved_at = None
        loan.rejection_reason = f"Sent back by General Director: {rejection_reason}"
        flash(f'🔄 Loan #{loan.id} sent back to Managing Director for review.', 'warning')
        
    else:
        flash(f'⚠️ You cannot reject this loan.', 'danger')
        return redirect(url_for('staff_dashboard'))
    
    db.session.commit()
    return redirect(url_for('staff_dashboard'))

@app.route('/approve_group_loan/<int:group_loan_id>', methods=['POST'])
def approve_group_loan(group_loan_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    group_loan = GroupLoan.query.get_or_404(group_loan_id)
    
    # Check if user can approve based on role and current stage
    if user.role == 'loan_officer' and group_loan.current_stage == 'loan_officer' and not group_loan.loan_officer_approved:
        group_loan.loan_officer_approved = True
        group_loan.loan_officer_id = user.id
        group_loan.loan_officer_approved_at = datetime.now()
        group_loan.current_stage = 'loan_manager'
        flash(f'✅ Group Loan #{group_loan.id} approved by Loan Officer. Moving to Loan Manager for review.', 'success')
        
    elif user.role == 'loan_manager' and group_loan.current_stage == 'loan_manager' and not group_loan.loan_manager_approved:
        group_loan.loan_manager_approved = True
        group_loan.loan_manager_id = user.id
        group_loan.loan_manager_approved_at = datetime.now()
        group_loan.current_stage = 'managing_director'
        flash(f'✅ Group Loan #{group_loan.id} approved by Loan Manager. Moving to Managing Director for final review.', 'success')
        
    elif user.role == 'managing_director' and group_loan.current_stage == 'managing_director' and not group_loan.managing_director_approved:
        group_loan.managing_director_approved = True
        group_loan.managing_director_id = user.id
        group_loan.managing_director_approved_at = datetime.now()
        group_loan.current_stage = 'general_director'
        flash(f'✅ Group Loan #{group_loan.id} approved by Managing Director. Moving to General Director for disbursement.', 'success')
        
    elif user.role == 'general_director' and group_loan.current_stage == 'general_director' and not group_loan.general_director_approved:
        group_loan.general_director_approved = True
        group_loan.general_director_id = user.id
        group_loan.general_director_approved_at = datetime.now()
        group_loan.status = 'approved'
        group_loan.current_stage = 'completed'
        flash(f'🎉 Group Loan #{group_loan.id} has been FULLY APPROVED! Ready for disbursement.', 'success')
        
    else:
        flash(f'⚠️ You cannot approve this group loan at the current stage.', 'warning')
        return redirect(url_for('staff_dashboard'))
    
    db.session.commit()
    return redirect(url_for('staff_dashboard'))

@app.route('/reject_group_loan/<int:group_loan_id>', methods=['POST'])
def reject_group_loan(group_loan_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    group_loan = GroupLoan.query.get_or_404(group_loan_id)
    rejection_reason = request.form.get('rejection_reason', 'No reason provided')
    
    # Determine which stage is rejecting
    current_stage = group_loan.current_stage
    
    if current_stage == 'loan_officer' and user.role == 'loan_officer':
        group_loan.status = 'rejected'
        group_loan.rejection_reason = f"Rejected by Loan Officer: {rejection_reason}"
        group_loan.rejected_by = user.id
        group_loan.rejected_at = datetime.now()
        flash(f'❌ Group Loan #{group_loan.id} rejected by Loan Officer.', 'danger')
        
    elif current_stage == 'loan_manager' and user.role == 'loan_manager':
        # Move back to loan officer
        group_loan.current_stage = 'loan_officer'
        group_loan.loan_officer_approved = False
        group_loan.loan_officer_id = None
        group_loan.loan_officer_approved_at = None
        group_loan.rejection_reason = f"Sent back by Loan Manager: {rejection_reason}"
        flash(f'🔄 Group Loan #{group_loan.id} sent back to Loan Officer for revision.', 'warning')
        
    elif current_stage == 'managing_director' and user.role == 'managing_director':
        # Move back to loan manager
        group_loan.current_stage = 'loan_manager'
        group_loan.loan_manager_approved = False
        group_loan.loan_manager_id = None
        group_loan.loan_manager_approved_at = None
        group_loan.rejection_reason = f"Sent back by Managing Director: {rejection_reason}"
        flash(f'🔄 Group Loan #{group_loan.id} sent back to Loan Manager for revision.', 'warning')
        
    elif current_stage == 'general_director' and user.role == 'general_director':
        # Move back to managing director
        group_loan.current_stage = 'managing_director'
        group_loan.managing_director_approved = False
        group_loan.managing_director_id = None
        group_loan.managing_director_approved_at = None
        group_loan.rejection_reason = f"Sent back by General Director: {rejection_reason}"
        flash(f'🔄 Group Loan #{group_loan.id} sent back to Managing Director for review.', 'warning')
        
    else:
        flash(f'⚠️ You cannot reject this group loan.', 'danger')
        return redirect(url_for('staff_dashboard'))
    
    db.session.commit()
    return redirect(url_for('staff_dashboard'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

from waitress import serve

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
            create_staff_accounts()
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            print("💡 Make sure MySQL is running and database 'microfinance_db' exists.")
            print("🔑 Staff Password: mf@123")
    
    print("🚀 Starting Fixed Workflow Microfinance Platform...")
    print("🌐 Access at: http://127.0.0.1:9000")
    print("✅ Features: Waitress Server, Proper Loan Approval Workflow")
    print("💼 Production-Ready Banking System")
    serve(app, host="0.0.0.0", port=9000)
