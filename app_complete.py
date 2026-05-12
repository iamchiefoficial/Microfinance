from flask import Flask, session, redirect, url_for, request, flash, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, gettext as _
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import json
import pandas as pd
from io import BytesIO
from flask import send_file
from collections import defaultdict

# SMS Configuration - AfricasTalking
import africastalking

# Initialize AfricasTalking (use sandbox for testing)
username = 'sandbox'  # Use 'sandbox' for testing, or your username for live
api_key = 'YOUR_API_KEY'  # Get from https://account.africastalking.com
africastalking.initialize(username, api_key)
sms = africastalking.SMS

app = Flask(__name__)
app.secret_key = 'orethan_secret_key_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///microfinance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'orethan-microfinance-secret-key-2024'
CORS(app)
jwt = JWTManager(app)

# Upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'id_cards'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'business_licenses'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'collateral'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'income_proof'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'other'), exist_ok=True)

db = SQLAlchemy(app)

# Language configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'sw']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

babel = Babel(app)

# Language selector function
def get_locale():
    # Check if language is in session
    if 'language' in session:
        return session['language']
    # Default to English
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

babel.init_app(app, locale_selector=get_locale)

# Add custom template filter for number formatting
@app.template_filter('format_number')
def format_number(value):
    """Format number with commas"""
    try:
        if value is None:
            return "0"
        return f"{int(value):,}" if value == int(value) else f"{value:,.2f}"
    except (ValueError, TypeError):
        return str(value)

@app.template_filter('format_currency')
def format_currency(value):
    """Format currency in Tanzania Shillings"""
    try:
        if value is None:
            return "Tsh 0"
        formatted = f"{value:,.2f}" if isinstance(value, float) and value % 1 != 0 else f"{int(value):,}"
        return f"Tsh {formatted}"
    except (ValueError, TypeError):
        return "Tsh 0"

# Language switcher route
@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'sw']:
        session['language'] = lang
        flash(_('Language changed to {}'.format('English' if lang == 'en' else 'Kiswahili')), 'success')
    return redirect(request.referrer or url_for('dashboard'))

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100))
    full_name = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='client')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Activity Log Model
class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    username = db.Column(db.String(100))
    user_role = db.Column(db.String(50))
    action = db.Column(db.String(100))
    entity_type = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    status = db.Column(db.String(20), default='SUCCESS')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id], backref='activities')

def log_activity(user_id, action, entity_type=None, entity_id=None, details=None, status='SUCCESS'):
    """Log user activity"""
    try:
        from flask import request
        user = User.query.get(user_id) if user_id else None
        
        log = ActivityLog(
            user_id=user_id,
            username=user.username if user else 'System',
            user_role=user.role if user else 'System',
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            ip_address=request.remote_addr if request else None,
            user_agent=str(request.headers.get('User-Agent'))[:500] if request else None,
            status=status,
            created_at=datetime.now()
        )
        db.session.add(log)
        db.session.commit()
        return True
    except Exception as e:
        print(f'Logging error: {e}')
        return False

# Individual Loan Model
class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String(200))
    status = db.Column(db.String(50), default='pending')
    current_stage = db.Column(db.String(50), default='loan_officer')
    term_months = db.Column(db.Integer, default=12)
    monthly_payment = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    client = db.relationship('User', foreign_keys=[client_id], backref='loans')
    
    def get_current_stage_name(self):
        stages = {
            'loan_officer': 'Loan Officer Review',
            'loan_manager': 'Loan Manager Review',
            'managing_director': 'Managing Director Review',
            'general_director': 'General Director Review',
            'completed': 'Approved - Ready for Disbursement'
        }
        return stages.get(self.current_stage, 'Unknown Stage')

# Repayment Model
class Repayment(db.Model):
    __tablename__ = 'repayments'
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)
    amount_paid = db.Column(db.Float, default=0)
    status = db.Column(db.String(50), default='pending')  # pending, paid, overdue, partial
    payment_date = db.Column(db.DateTime, nullable=True)
    late_fee = db.Column(db.Float, default=0)
    days_overdue = db.Column(db.Integer, default=0)
    penalty_rate = db.Column(db.Float, default=0)  # 5% per month late fee
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    loan = db.relationship('Loan', foreign_keys=[loan_id], backref='repayments')
    client = db.relationship('User', foreign_keys=[client_id], backref='repayments')
    
    def calculate_late_fee(self):
        if self.status == 'pending' and self.due_date < datetime.now():
            days = (datetime.now() - self.due_date).days
            self.days_overdue = days
            self.late_fee = self.amount_due * (self.penalty_rate / 100) * (days // 30)
            return self.late_fee
        return 0
    
    def mark_as_paid(self, amount, payment_date=None):
        self.amount_paid = amount
        self.payment_date = payment_date or datetime.now()
        if self.amount_paid >= self.amount_due:
            self.status = 'paid'
        else:
            self.status = 'partial'
        self.updated_at = datetime.now()
        return self.status

def generate_repayment_schedule(loan):
    """Generate repayment schedule for a loan"""
    try:
        # Delete existing repayments if any
        Repayment.query.filter_by(loan_id=loan.id).delete()
        
        monthly_payment = loan.monthly_payment
        months = loan.term_months
        start_date = loan.created_at or datetime.now()
        
        for i in range(1, months + 1):
            due_date = start_date.replace(day=1) + timedelta(days=32*i)
            due_date = due_date.replace(day=min(due_date.day, 28))
            
            # Calculate penalty rate (higher for later payments)
            penalty_rate = 5  # 5% per month late fee
            
            repayment = Repayment(
                loan_id=loan.id,
                client_id=loan.client_id,
                due_date=due_date,
                amount_due=monthly_payment,
                amount_paid=0,
                status='pending',
                penalty_rate=penalty_rate,
                created_at=datetime.now()
            )
            db.session.add(repayment)
        
        db.session.commit()
        return True
    except Exception as e:
        print(f'Error generating schedule: {e}')
        return False

# Group Loan Model
class GroupLoan(db.Model):
    __tablename__ = 'group_loans'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Applicant Information
    applicant_full_name = db.Column(db.String(200), nullable=False)
    applicant_national_id = db.Column(db.String(50), nullable=False)
    applicant_dob = db.Column(db.Date, nullable=True)
    applicant_gender = db.Column(db.String(10), nullable=True)
    applicant_marital_status = db.Column(db.String(20), nullable=True)
    applicant_phone = db.Column(db.String(20), nullable=True)
    applicant_address = db.Column(db.Text, nullable=True)
    applicant_occupation = db.Column(db.String(100), nullable=True)
    monthly_income = db.Column(db.Float, nullable=True)
    bank_account = db.Column(db.String(50), nullable=True)
    
    # Group Information
    group_name = db.Column(db.String(200), nullable=True)
    group_chairperson = db.Column(db.String(200), nullable=False)
    group_registration_number = db.Column(db.String(50), nullable=True)
    male_members = db.Column(db.Integer, default=0)
    female_members = db.Column(db.Integer, default=0)
    group_meeting_day = db.Column(db.String(20), nullable=True)
    group_meeting_time = db.Column(db.String(20), nullable=True)
    group_meeting_place = db.Column(db.String(200), nullable=True)
    
    # Project Information
    project_type = db.Column(db.String(100), nullable=True)
    project_description = db.Column(db.Text, nullable=True)
    project_experience = db.Column(db.String(20), nullable=True)
    project_location = db.Column(db.String(200), nullable=True)
    monthly_revenue = db.Column(db.Float, nullable=True)
    monthly_expenses = db.Column(db.Float, nullable=True)
    
    # Loan Details
    loan_amount = db.Column(db.Float, nullable=False)
    loan_purpose = db.Column(db.String(200), nullable=True)
    repayment_period = db.Column(db.Integer, nullable=False)
    interest_rate = db.Column(db.Float, default=15.0)
    monthly_installment = db.Column(db.Float, nullable=True)
    
    # Guarantor 1 Information
    guarantor1_name = db.Column(db.String(200), nullable=True)
    guarantor1_national_id = db.Column(db.String(50), nullable=True)
    guarantor1_phone = db.Column(db.String(20), nullable=True)
    guarantor1_address = db.Column(db.Text, nullable=True)
    guarantor1_occupation = db.Column(db.String(100), nullable=True)
    guarantor1_relationship = db.Column(db.String(50), nullable=True)
    
    # Guarantor 2 Information
    guarantor2_name = db.Column(db.String(200), nullable=True)
    guarantor2_national_id = db.Column(db.String(50), nullable=True)
    guarantor2_phone = db.Column(db.String(20), nullable=True)
    guarantor2_address = db.Column(db.Text, nullable=True)
    guarantor2_occupation = db.Column(db.String(100), nullable=True)
    guarantor2_relationship = db.Column(db.String(50), nullable=True)
    
    # Collateral Information (JSON)
    collateral_info = db.Column(db.Text, nullable=True)
    
    # Signatures
    applicant_signature = db.Column(db.Text, nullable=True)
    applicant_date = db.Column(db.Date, nullable=True)
    chairperson_signature = db.Column(db.Text, nullable=True)
    chairperson_date = db.Column(db.Date, nullable=True)
    
    # Workflow Fields
    status = db.Column(db.String(50), default='pending')
    current_stage = db.Column(db.String(50), default='loan_officer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Approval Fields
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

# Payment/Banking Model
class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))  # M-Pesa, Tigo Pesa, Airtel Money, NMB, CRDB
    payment_type = db.Column(db.String(50))    # Loan Repayment, Disbursement, Fee
    transaction_id = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(20))
    account_number = db.Column(db.String(50))
    bank_name = db.Column(db.String(50))       # NMB, CRDB, etc.
    status = db.Column(db.String(50), default='pending')  # pending, completed, failed
    reference_number = db.Column(db.String(100))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Relationships
    loan = db.relationship('Loan', foreign_keys=[loan_id], backref='payments')
    client = db.relationship('User', foreign_keys=[client_id], backref='payments')

# Disbursement Model
class Disbursement(db.Model):
    __tablename__ = 'disbursements'
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50))  # M-Pesa, Bank Transfer, Cash
    phone_number = db.Column(db.String(20))
    bank_name = db.Column(db.String(50))
    account_number = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    disbursement_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')
    confirmed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    loan = db.relationship('Loan', foreign_keys=[loan_id])
    client = db.relationship('User', foreign_keys=[client_id])

# Document Model
class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=True)
    document_type = db.Column(db.String(100))  # ID Card, Business License, etc.
    document_name = db.Column(db.String(200))
    filename = db.Column(db.String(500))
    file_path = db.Column(db.String(1000))
    file_size = db.Column(db.Integer)  # in bytes
    mime_type = db.Column(db.String(100))
    status = db.Column(db.String(50), default='pending')  # pending, verified, rejected
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='documents')
    loan = db.relationship('Loan', foreign_keys=[loan_id], backref='documents')
    verifier = db.relationship('User', foreign_keys=[verified_by])

# SMS Functions
def send_sms(phone_number, message):
    """
    Send SMS using AfricasTalking
    """
    try:
        # Format phone number (remove any spaces, ensure Tanzania format)
        if phone_number:
            # Remove any non-digit characters
            phone_number = ''.join(filter(str.isdigit, phone_number))
            
            # Add country code if not present
            if phone_number.startswith('0'):
                phone_number = '255' + phone_number[1:]
            elif not phone_number.startswith('255'):
                phone_number = '255' + phone_number
            
            # Send SMS
            response = sms.send(message, [phone_number])
            print(f"SMS sent to {phone_number}: {response}")
            return True
        return False
    except Exception as e:
        print(f"SMS error: {e}")
        return False

def send_loan_approval_sms(client, loan):
    """
    Send SMS when loan is approved
    """
    if not client.phone:
        print(f"No phone number for {client.username}")
        return False
    
    # Format amount with commas
    formatted_amount = f"{int(loan.amount):,}" if loan.amount == int(loan.amount) else f"{loan.amount:,.2f}"
    
    message = f"""ORETHAN MICROFINANCE: CONGRATULATIONS {client.full_name or client.username}!

Your loan of Tsh {formatted_amount} has been APPROVED! 
Loan ID: #{loan.id}
Amount: Tsh {formatted_amount}
Term: {loan.term_months} months

Our disbursement team will contact you within 24 hours.
Thank you for choosing Orethan Microfinance!"""
    
    return send_sms(client.phone, message)

def send_disbursement_sms(client, loan, method):
    """
    Send SMS when loan is disbursed
    """
    if not client.phone:
        print(f"No phone number for {client.username}")
        return False
    
    # Format amount with commas
    formatted_amount = f"{int(loan.amount):,}" if loan.amount == int(loan.amount) else f"{loan.amount:,.2f}"
    formatted_payment = f"{int(loan.monthly_payment):,}" if loan.monthly_payment == int(loan.monthly_payment) else f"{loan.monthly_payment:,.2f}"
    
    message = f"""ORETHAN MICROFINANCE: DISBURSEMENT CONFIRMATION

Dear {client.full_name or client.username},
Your loan of Tsh {formatted_amount} has been DISBURSED via {method}!
Loan ID: #{loan.id}
Monthly Payment: Tsh {formatted_payment}
First payment due in 30 days.

Thank you for banking with Orethan!"""
    
    return send_sms(client.phone, message)

def send_payment_reminder_sms(client, loan, days_overdue=0):
    """
    Send SMS reminder for upcoming or overdue payment
    """
    if not client.phone:
        return False
    
    if days_overdue > 0:
        message = f"""ORETHAN MICROFINANCE: PAYMENT REMINDER

Dear {client.full_name or client.username},
Your loan payment of Tsh {loan.monthly_payment:,.2f} is {days_overdue} days OVERDUE.
Loan ID: #{loan.id}
Please make payment immediately to avoid penalties.

Contact us at (+255) 769 337 774"""
    else:
        message = f"""ORETHAN MICROFINANCE: PAYMENT REMINDER

Dear {client.full_name or client.username},
Your monthly payment of Tsh {loan.monthly_payment:,.2f} is due in 5 days.
Loan ID: #{loan.id}

Please ensure sufficient funds in your account.
Thank you for your cooperation!"""
    
    return send_sms(client.phone, message)

# Document Helper Functions
import os
from werkzeug.utils import secure_filename
from flask import send_file

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_document_category(document_type):
    categories = {
        'ID Card': 'id_cards',
        'Passport': 'id_cards',
        'Voter ID': 'id_cards',
        'Business License': 'business_licenses',
        'Collateral': 'collateral',
        'Proof of Income': 'income_proof',
        'Other': 'other'
    }
    return categories.get(document_type, 'other')

# Routes
@app.route('/')
def index():
    return render_template("front_page.html")
    return render_template("front_page.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            # Log successful login
            log_activity(user.id, 'LOGIN', 'USER', user.id, f'User {user.username} logged in', 'SUCCESS')
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Welcome {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Log failed login
            log_activity(None, 'LOGIN_FAILED', 'USER', None, f'Failed login attempt for username: {username}', 'FAILED')
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return render_template("front_page.html")
    user = db.session.get(User, session['user_id'])
    if user:
        flash(_('Welcome back, {}!').format(user.username), 'success')
        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user.role == 'client':
            return redirect(url_for('client_dashboard'))
        else:
            return redirect(url_for('staff_dashboard'))
    else:
        session.clear()
        return redirect(url_for('login'))

@app.route('/client_dashboard')
def client_dashboard():
    if 'user_id' not in session:
        return render_template("front_page.html")
    user = db.session.get(User, session['user_id'])
    loans = Loan.query.filter_by(client_id=user.id).all()
    group_loans = GroupLoan.query.filter_by(client_id=user.id).all()
    total_loans = len(loans) + len(group_loans)
    active_loans = len([l for l in loans if l.status == 'active']) + len([gl for gl in group_loans if gl.status == 'active'])
    completed_loans = len([l for l in loans if l.status == 'completed']) + len([gl for gl in group_loans if gl.status == 'completed'])
    
    return render_template('client_dashboard.html', user=user, loans=loans, group_loans=group_loans, 
                         total_loans=total_loans, active_loans=active_loans, completed_loans=completed_loans)

@app.route('/staff_dashboard')
def staff_dashboard():
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    if not user or user.role == 'client':
        flash('Access denied!', 'danger')
        return render_template("front_page.html")
    
    # Different views based on role
    if user.role == 'loan_officer':
        pending_loans = Loan.query.filter_by(current_stage='loan_officer', status='pending').all()
        approved_loans = []
        all_clients = []
        
    elif user.role == 'loan_manager':
        pending_loans = Loan.query.filter_by(current_stage='loan_manager', status='pending').all()
        approved_loans = []
        all_clients = []
        
    elif user.role == 'managing_director':
        pending_loans = Loan.query.filter_by(current_stage='managing_director', status='pending').all()
        approved_loans = []
        all_clients = []
        
    elif user.role == 'general_director':
        # General Director sees ALL pending loans at their stage
        pending_loans = Loan.query.filter_by(current_stage='general_director', status='pending').all()
        # Also show all clients for reference
        all_clients = User.query.filter_by(role='client').all()
        # Show all loans for overview
        approved_loans = Loan.query.filter_by(status='approved').all()
        
    else:  # admin
        pending_loans = Loan.query.filter_by(current_stage='general_director', status='pending').all()
        all_clients = User.query.filter_by(role='client').all()
        approved_loans = Loan.query.filter_by(status='approved').all()
    
    total_clients = User.query.filter_by(role='client').count()
    total_loans = Loan.query.count()
    pending_for_me = len(pending_loans)
    
    return render_template('staff_dashboard.html',
                         user=user,
                         total_clients=total_clients,
                         total_loans=total_loans,
                         pending_for_me=pending_for_me,
                         pending_loans=pending_loans,
                         approved_loans=approved_loans,
                         all_clients=all_clients if 'all_clients' in locals() else [])

@app.route('/approve_loan/<int:loan_id>', methods=['POST'])
def approve_loan(loan_id):
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    loan = Loan.query.get_or_404(loan_id)
    
    # Simple approval logic
    if user.role == 'loan_officer' and loan.current_stage == 'loan_officer':
        loan.current_stage = 'loan_manager'
        log_activity(user.id, 'APPROVE', 'LOAN', loan.id, f'Loan #{loan.id} approved by {user.role} at stage {loan.current_stage}', 'SUCCESS')
        flash(f'✅ Loan #{loan.id} approved by {user.role}. Moving to Loan Manager.', 'success')
    elif user.role == 'loan_manager' and loan.current_stage == 'loan_manager':
        loan.current_stage = 'managing_director'
        log_activity(user.id, 'APPROVE', 'LOAN', loan.id, f'Loan #{loan.id} approved by {user.role} at stage {loan.current_stage}', 'SUCCESS')
        flash(f'✅ Loan #{loan.id} approved by {user.role}. Moving to Managing Director.', 'success')
    elif user.role == 'managing_director' and loan.current_stage == 'managing_director':
        loan.current_stage = 'general_director'
        log_activity(user.id, 'APPROVE', 'LOAN', loan.id, f'Loan #{loan.id} approved by {user.role} at stage {loan.current_stage}', 'SUCCESS')
        flash(f'✅ Loan #{loan.id} approved by {user.role}. Moving to General Director.', 'success')
    elif user.role == 'general_director' and loan.current_stage == 'general_director':
        loan.status = 'approved'
        loan.current_stage = 'completed'
        db.session.commit()
        
        # Generate repayment schedule
        generate_repayment_schedule(loan)
        
        # Send SMS notification to client
        send_loan_approval_sms(loan.client, loan)
        
        log_activity(user.id, 'APPROVE', 'LOAN', loan.id, f'Loan #{loan.id} fully approved by {user.role}. Repayment schedule generated.', 'SUCCESS')
        flash(f'🎉 Loan #{loan.id} has been FULLY APPROVED! Repayment schedule generated. Client notified via SMS.', 'success')
    else:
        log_activity(user.id, 'APPROVE_FAILED', 'LOAN', loan.id, f'Failed approval attempt by {user.role} at stage {loan.current_stage}', 'FAILED')
        flash(f'⚠️ You cannot approve this loan at the current stage.', 'warning')
        return redirect(url_for('staff_dashboard'))
    
    db.session.commit()
    return redirect(url_for('staff_dashboard'))

@app.route('/reject_loan/<int:loan_id>', methods=['POST'])
def reject_loan(loan_id):
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    loan = Loan.query.get_or_404(loan_id)
    
    # Simple rejection logic - move back one stage
    if user.role == 'loan_manager' and loan.current_stage == 'loan_manager':
        loan.current_stage = 'loan_officer'
        flash(f'🔄 Loan #{loan.id} sent back to Loan Officer by {user.role}.', 'warning')
    elif user.role == 'managing_director' and loan.current_stage == 'managing_director':
        loan.current_stage = 'loan_manager'
        flash(f'🔄 Loan #{loan.id} sent back to Loan Manager by {user.role}.', 'warning')
    elif user.role == 'general_director' and loan.current_stage == 'general_director':
        loan.current_stage = 'managing_director'
        flash(f'🔄 Loan #{loan.id} sent back to Managing Director by {user.role}.', 'warning')
    elif user.role == 'loan_officer' and loan.current_stage == 'loan_officer':
        loan.status = 'rejected'
        flash(f'❌ Loan #{loan.id} has been REJECTED by Loan Officer.', 'danger')
    else:
        flash(f'⚠️ You cannot reject this loan.', 'warning')
        return redirect(url_for('staff_dashboard'))
    
    db.session.commit()
    return redirect(url_for('staff_dashboard'))

@app.route('/client_loan_history/<int:client_id>')
def client_loan_history(client_id):
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    
    # Only General Director, Admin, or client themselves can view
    if user.role not in ['general_director', 'admin'] and user.id != client_id:
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    client = User.query.get_or_404(client_id)
    loans = Loan.query.filter_by(client_id=client_id).order_by(Loan.created_at.desc()).all()
    
    return render_template('client_loan_history.html', client=client, loans=loans, viewer=user)

def get_analytics_data():
    """Get REAL analytics data from database"""
    from collections import defaultdict
    from sqlalchemy import func
    
    # Get real data for last 6 months
    months = []
    approval_counts = []
    pending_counts = []
    revenue_data = []
    client_counts = []
    
    for i in range(5, -1, -1):
        month_date = datetime.now().replace(day=1) - timedelta(days=30*i)
        month_name = month_date.strftime('%b %Y')
        months.append(month_name)
        
        # Start and end of month
        start_of_month = month_date.replace(day=1, hour=0, minute=0, second=0)
        if i == 0:
            end_of_month = datetime.now()
        else:
            next_month = month_date.replace(day=28) + timedelta(days=4)
            end_of_month = next_month.replace(day=1, hour=23, minute=59, second=59)
        
        # Count approved loans in this month (REAL DATA)
        approved_count = Loan.query.filter(
            Loan.status == 'approved',
            Loan.updated_at >= start_of_month,
            Loan.updated_at <= end_of_month
        ).count()
        
        # Count pending loans in this month (REAL DATA)
        pending_count = Loan.query.filter(
            Loan.status == 'pending',
            Loan.created_at >= start_of_month,
            Loan.created_at <= end_of_month
        ).count()
        
        # Calculate revenue from payments (REAL DATA)
        revenue = db.session.query(func.sum(Payment.amount)).filter(
            Payment.payment_date >= start_of_month,
            Payment.payment_date <= end_of_month,
            Payment.status == 'completed'
        ).scalar() or 0
        
        # New clients registered (REAL DATA)
        new_clients = User.query.filter(
            User.role == 'client',
            User.created_at >= start_of_month,
            User.created_at <= end_of_month
        ).count()
        
        approval_counts.append(approved_count)
        pending_counts.append(pending_count)
        revenue_data.append(float(revenue))
        client_counts.append(new_clients)
    
    # Loan type distribution (REAL DATA)
    individual_loans = Loan.query.filter(Loan.purpose.notin_(['Group Loan', 'Business', 'Emergency'])).count()
    group_loans = Loan.query.filter_by(purpose='Group Loan').count()
    business_loans = Loan.query.filter_by(purpose='Business').count()
    emergency_loans = Loan.query.filter_by(purpose='Emergency').count()
    
    # Calculate totals
    total_approved = sum(approval_counts)
    total_pending = sum(pending_counts)
    total_revenue = sum(revenue_data)
    
    return {
        'approval_labels': months,
        'approval_data': approval_counts,
        'pending_data': pending_counts,
        'revenue_labels': months,
        'revenue_data': revenue_data,
        'client_labels': months,
        'client_data': client_counts,
        'loan_type_data': [individual_loans, group_loans, business_loans, emergency_loans],
        'total_approved': total_approved,
        'total_pending': total_pending,
        'total_revenue': total_revenue
    }

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    if not user or user.role != 'admin':
        flash('Access denied! Admin only.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Statistics
    total_users = User.query.count()
    total_clients = User.query.filter_by(role='client').count()
    total_staff = User.query.filter(User.role != 'client').count()
    total_loans = Loan.query.count()
    pending_loans = Loan.query.filter_by(status='pending').count()
    approved_loans = Loan.query.filter_by(status='approved').count()
    rejected_loans = Loan.query.filter_by(status='rejected').count()
    
    # Calculate total disbursed amount
    total_disbursed_amount = db.session.query(db.func.sum(Loan.amount)).filter(Loan.status == 'approved').scalar() or 0
    
    # Recent activity
    recent_loans = Loan.query.order_by(Loan.created_at.desc()).limit(10).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    # Loans by stage
    loans_by_stage = {
        'loan_officer': Loan.query.filter_by(current_stage='loan_officer', status='pending').count(),
        'loan_manager': Loan.query.filter_by(current_stage='loan_manager', status='pending').count(),
        'managing_director': Loan.query.filter_by(current_stage='managing_director', status='pending').count(),
        'general_director': Loan.query.filter_by(current_stage='general_director', status='pending').count(),
        'completed': Loan.query.filter_by(current_stage='completed').count()
    }
    
    analytics = get_analytics_data()
    
    return render_template('admin_dashboard.html',
                         user=user,
                         total_users=total_users,
                         total_clients=total_clients,
                         total_staff=total_staff,
                         total_loans=total_loans,
                         total_disbursed_amount=total_disbursed_amount,
                         pending_loans=pending_loans,
                         approved_loans=approved_loans,
                         rejected_loans=rejected_loans,
                         recent_loans=recent_loans,
                         recent_users=recent_users,
                         loans_by_stage=loans_by_stage,
                         approval_labels=analytics['approval_labels'],
                         approval_data=analytics['approval_data'],
                         pending_data=analytics['pending_data'],
                         revenue_labels=analytics['revenue_labels'],
                         revenue_data=analytics['revenue_data'],
                         client_labels=analytics['client_labels'],
                         client_data=analytics['client_data'],
                         loan_type_data=analytics['loan_type_data'])

@app.route('/admin/users')

def admin_users():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    admin_user = db.session.get(User, session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied! Admin only.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get ONLY clients (role = 'client')
    all_clients = User.query.filter_by(role='client').order_by(User.created_at.desc()).all()
    
    return render_template('admin_users.html', users=all_clients)

@app.route('/admin/loans')
def admin_loans():
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    if not user or user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    all_loans = Loan.query.order_by(Loan.created_at.desc()).all()
    return render_template('admin_loans.html', loans=all_loans)

@app.route('/admin/approve_loan/<int:loan_id>', methods=['POST'])
def admin_approve_loan(loan_id):
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    admin_user = db.session.get(User, session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    loan = Loan.query.get_or_404(loan_id)
    loan.status = 'approved'
    loan.current_stage = 'completed'
    db.session.commit()
    
    flash(f'✅ Loan #{loan.id} approved by Administrator!', 'success')
    return redirect(url_for('admin_loans'))

@app.route('/admin/reject_loan/<int:loan_id>', methods=['POST'])
def admin_reject_loan(loan_id):
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    admin_user = db.session.get(User, session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    loan = Loan.query.get_or_404(loan_id)
    loan.status = 'rejected'
    db.session.commit()
    
    flash(f'❌ Loan #{loan.id} rejected by Administrator!', 'danger')

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    admin_user = db.session.get(User, session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    user_to_delete = User.query.get_or_404(user_id)
    
    if user_to_delete.role == 'admin':
        flash('Cannot delete the main admin user!', 'danger')
    elif user_to_delete.role == 'client':
        # First delete all loans associated with this client
        loans = Loan.query.filter_by(client_id=user_to_delete.id).all()
        for loan in loans:
            # Delete associated repayments
            Repayment.query.filter_by(loan_id=loan.id).delete()
            # Delete associated payments
            Payment.query.filter_by(loan_id=loan.id).delete()
            # Delete the loan
            db.session.delete(loan)
        
        # Delete user activities
        ActivityLog.query.filter_by(user_id=user_to_delete.id).delete()
        
        # Finally delete the user
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f' User {user_to_delete.username} and all related data deleted successfully!', 'success')
    else:
        # For staff, just delete the user (they shouldn't have loans)
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f' Staff {user_to_delete.username} deleted successfully!', 'success')
    
    return redirect(url_for('admin_users'))

@app.route('/apply_loan', methods=['POST'])
def apply_loan():
    if 'user_id' not in session:
        return render_template("front_page.html")
    user = db.session.get(User, session['user_id'])
    
    new_loan = Loan(
        client_id=user.id,
        amount=float(request.form.get('amount')),
        purpose=request.form.get('purpose'),
        term_months=int(request.form.get('term_months')),
        monthly_payment=float(request.form.get('amount')) / int(request.form.get('term_months')),
        status='pending',
        current_stage='loan_officer'
    )
    db.session.add(new_loan)
    db.session.commit()
    flash('Individual loan application submitted!', 'success')
    return redirect(url_for('client_dashboard'))

@app.route('/submit_individual_loan', methods=['POST'])
def submit_individual_loan():
    if 'user_id' not in session:
        return render_template("front_page.html")
    user = db.session.get(User, session['user_id'])
    
    new_loan = Loan(
        client_id=user.id,
        amount=float(request.form.get('amount')),
        purpose=request.form.get('purpose'),
        term_months=int(request.form.get('term_months')),
        monthly_payment=float(request.form.get('amount')) / int(request.form.get('term_months')),
        status='pending',
        current_stage='loan_officer'
    )
    db.session.add(new_loan)
    db.session.commit()
    flash('Individual loan application submitted successfully!', 'success')
    return redirect(url_for('client_dashboard'))

@app.route('/individual_loan_form')
def individual_loan_form():
    if 'user_id' not in session:
        return render_template("front_page.html")
    user = db.session.get(User, session['user_id'])
    return render_template('individual_loan_form.html', user=user)

@app.route('/group_loan_form')
def group_loan_form():
    if 'user_id' not in session:
        return render_template("front_page.html")
    user = db.session.get(User, session['user_id'])
    return render_template('group_loan_form.html', user=user)

@app.route('/apply_group_loan')
def apply_group_loan():
    if 'user_id' not in session:
        return render_template("front_page.html")
    user = db.session.get(User, session['user_id'])
    if not user or user.role != 'client':
        flash('Only clients can apply for group loans!', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('group_loan_form.html')

@app.route('/group_loan_form_new', methods=['GET'])
def group_loan_form_new():
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    if not user or user.role != 'client':
        flash('Only clients can apply for group loans!', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('group_loan_form.html')

@app.route('/submit_group_loan_new', methods=['POST'])
def submit_group_loan_new():
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    
    applicant_name = request.form.get('applicant_full_name')
    loan_amount = request.form.get('loan_amount')
    
    flash(f'✅ Group loan application submitted for {applicant_name} - Amount: Tsh {loan_amount}', 'success')
    return redirect(url_for('client_dashboard'))

@app.route('/submit_group_loan', methods=['POST'])
def submit_group_loan():
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    
    try:
        # Create a regular loan (since GroupLoan table might not exist)
        new_loan = Loan(
            client_id=user.id,
            amount=float(request.form.get('loan_amount')),
            purpose=request.form.get('loan_purpose') or 'Group Loan',
            term_months=int(request.form.get('repayment_period')) if request.form.get('repayment_period') else 12,
            monthly_payment=float(request.form.get('loan_amount')) / int(request.form.get('repayment_period')) if request.form.get('repayment_period') else 0,
            status='pending',
            current_stage='loan_officer'
        )
        
        db.session.add(new_loan)
        db.session.commit()
        
        # Store additional group info in session or separate table
        flash(f'✅ Group loan application submitted successfully! Amount: Tsh {float(request.form.get("loan_amount")):,.2f}', 'success')
        return redirect(url_for('client_dashboard'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error: {str(e)}', 'danger')
        return redirect(url_for('group_loan_form_new'))

@app.route('/approve_group_loan/<int:group_loan_id>', methods=['POST'])
def approve_group_loan(group_loan_id):
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    group_loan = GroupLoan.query.get_or_404(group_loan_id)
    
    if user.role == 'loan_officer' and group_loan.current_stage == 'loan_officer':
        group_loan.loan_officer_approved = True
        group_loan.loan_officer_id = user.id
        group_loan.loan_officer_approved_at = datetime.now()
        group_loan.current_stage = 'loan_manager'
        flash(f'Group loan #{group_loan.id} approved by Loan Officer. Moving to Loan Manager.', 'success')
        
    elif user.role == 'loan_manager' and group_loan.current_stage == 'loan_manager':
        group_loan.loan_manager_approved = True
        group_loan.loan_manager_id = user.id
        group_loan.loan_manager_approved_at = datetime.now()
        group_loan.current_stage = 'managing_director'
        flash(f'Group loan #{group_loan.id} approved by Loan Manager. Moving to Managing Director.', 'success')
        
    elif user.role == 'managing_director' and group_loan.current_stage == 'managing_director':
        group_loan.managing_director_approved = True
        group_loan.managing_director_id = user.id
        group_loan.managing_director_approved_at = datetime.now()
        group_loan.current_stage = 'general_director'
        flash(f'Group loan #{group_loan.id} approved by Managing Director. Moving to General Director.', 'success')
        
    elif user.role == 'general_director' and group_loan.current_stage == 'general_director':
        group_loan.general_director_approved = True
        group_loan.general_director_id = user.id
        group_loan.general_director_approved_at = datetime.now()
        group_loan.status = 'approved'
        group_loan.current_stage = 'completed'
        flash(f'Group loan #{group_loan.id} has been FULLY APPROVED! Ready for disbursement.', 'success')
        
    else:
        flash('You cannot approve this group loan at the current stage.', 'warning')
        return redirect(url_for('staff_dashboard'))
    
    db.session.commit()
    return redirect(url_for('staff_dashboard'))

@app.route('/reject_group_loan/<int:group_loan_id>', methods=['POST'])
def reject_group_loan(group_loan_id):
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    group_loan = GroupLoan.query.get_or_404(group_loan_id)
    rejection_reason = request.form.get('rejection_reason', 'No reason provided')
    
    if user.role == 'loan_officer' and group_loan.current_stage == 'loan_officer':
        group_loan.status = 'rejected'
        group_loan.rejection_reason = f"Rejected by Loan Officer: {rejection_reason}"
        group_loan.rejected_by = user.id
        group_loan.rejected_at = datetime.now()
        flash(f'Group loan #{group_loan.id} rejected by Loan Officer.', 'danger')
        
    elif user.role == 'loan_manager' and group_loan.current_stage == 'loan_manager':
        group_loan.current_stage = 'loan_officer'
        group_loan.loan_officer_approved = False
        group_loan.loan_officer_id = None
        group_loan.loan_officer_approved_at = None
        group_loan.rejection_reason = f"Sent back by Loan Manager: {rejection_reason}"
        flash(f'Group loan #{group_loan.id} sent back to Loan Officer.', 'warning')
        
    elif user.role == 'managing_director' and group_loan.current_stage == 'managing_director':
        group_loan.current_stage = 'loan_manager'
        group_loan.loan_manager_approved = False
        group_loan.loan_manager_id = None
        group_loan.loan_manager_approved_at = None
        group_loan.rejection_reason = f"Sent back by Managing Director: {rejection_reason}"
        flash(f'Group loan #{group_loan.id} sent back to Loan Manager.', 'warning')
        
    elif user.role == 'general_director' and group_loan.current_stage == 'general_director':
        group_loan.current_stage = 'managing_director'
        group_loan.managing_director_approved = False
        group_loan.managing_director_id = None
        group_loan.managing_director_approved_at = None
        group_loan.rejection_reason = f"Sent back by General Director: {rejection_reason}"
        flash(f'Group loan #{group_loan.id} sent back to Managing Director.', 'warning')
        
    else:
        flash('You cannot reject this group loan.', 'danger')
        return redirect(url_for('staff_dashboard'))
    
    db.session.commit()
    return redirect(url_for('staff_dashboard'))

@app.route('/send_payment_reminder/<int:loan_id>', methods=['POST'])
def send_payment_reminder(loan_id):
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    if user.role not in ['loan_officer', 'admin']:
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    loan = Loan.query.get_or_404(loan_id)
    
    if loan.status != 'approved':
        flash('Loan must be approved to send reminders!', 'danger')
        return redirect(url_for('staff_dashboard'))
    
    days_overdue = int(request.form.get('days_overdue', 0))
    send_payment_reminder_sms(loan.client, loan, days_overdue)
    
    flash(f'✅ Payment reminder SMS sent to {loan.client.phone}', 'success')
    return redirect(url_for('staff_dashboard'))

@app.route('/test_sms')
def test_sms():
    # Test sending SMS to yourself
    phone = '0712345678'  # Test phone number
    message = 'Test SMS from Orethan Microfinance - SMS system is working!'
    result = send_sms(phone, message)
    return f"SMS sent: {result}"

@app.route('/upload_document', methods=['GET', 'POST'])
def upload_document():
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    
    if request.method == 'POST':
        document_type = request.form.get('document_type')
        loan_id = request.form.get('loan_id')
        
        if 'file' not in request.files:
            flash('No file selected!', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected!', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            category = get_document_category(document_type)
            
            # Create unique filename
            import uuid
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            
            # Save file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], category, unique_filename)
            file.save(file_path)
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Create document record
            document = Document(
                user_id=user.id,
                loan_id=int(loan_id) if loan_id else None,
                document_type=document_type,
                document_name=filename,
                filename=unique_filename,
                file_path=file_path,
                file_size=file_size,
                mime_type=file.content_type,
                status='pending',
                uploaded_at=datetime.now()
            )
            
            db.session.add(document)
            db.session.commit()
            
            flash(f'✅ Document "{filename}" uploaded successfully!', 'success')
            return redirect(url_for('view_my_documents'))
        else:
            flash('File type not allowed! Allowed: PNG, JPG, PDF, DOC', 'danger')
    
    # GET request - show upload form
    loans = Loan.query.filter_by(client_id=user.id).all()
    return render_template('upload_document.html', user=user, loans=loans)

@app.route('/my_documents')
def view_my_documents():
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    documents = Document.query.filter_by(user_id=user.id).order_by(Document.uploaded_at.desc()).all()
    
    return render_template('my_documents.html', user=user, documents=documents)

@app.route('/admin/documents')
def admin_documents():
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    if user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    documents = Document.query.order_by(Document.uploaded_at.desc()).all()
    return render_template('admin_documents.html', user=user, documents=documents)

@app.route('/verify_document/<int:doc_id>', methods=['POST'])
def verify_document(doc_id):
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    admin = db.session.get(User, session['user_id'])
    if admin.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    document = Document.query.get_or_404(doc_id)
    status = request.form.get('status')
    notes = request.form.get('notes', '')
    
    document.status = status
    document.verified_by = admin.id
    document.verified_at = datetime.now()
    document.notes = notes
    
    db.session.commit()
    
    flash(f'✅ Document "{document.document_name}" marked as {status}!', 'success')
    return redirect(url_for('admin_documents'))

@app.route('/download_document/<int:doc_id>')
def download_document(doc_id):
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    document = Document.query.get_or_404(doc_id)
    
    # Check permission (owner or admin can download)
    if user.id != document.user_id and user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    return send_file(
        document.file_path,
        as_attachment=True,
        download_name=document.document_name,
        mimetype=document.mime_type
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        existing = User.query.filter_by(username=username).first()
        if existing:
            flash('Username exists!', 'danger')
            return render_template('register.html')
        
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            role='client',
            full_name=request.form.get('full_name', ''),
            email=request.form.get('email', ''),
            phone=request.form.get('phone', '')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return render_template("front_page.html")
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template("front_page.html")


# Create staff accounts
def create_staff():
    with app.app_context():
        staff_list = [
            ('Admin', 'admin123', 'admin'),
            ('Loan Officer', 'mf@123', 'loan_officer'),
            ('Loan Manager', 'mf@123', 'loan_manager'),
            ('Managing Director', 'mf@123', 'managing_director'),
            ('General Director', 'mf@123', 'general_director'),
        ]
        for username, password, role in staff_list:
            if not User.query.filter_by(username=username).first():
                user = User(username=username, password=generate_password_hash(password), role=role)
                db.session.add(user)
        db.session.commit()



# Payment Routes
@app.route('/make_payment/<int:loan_id>', methods=['GET', 'POST'])
def make_payment(loan_id):
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    loan = Loan.query.get_or_404(loan_id)
    
    # Check if loan belongs to the logged-in user
    if loan.client_id != user.id:
        flash('Unauthorized! This loan does not belong to you.', 'danger')
        return redirect(url_for('client_dashboard'))
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        amount = float(request.form.get('amount'))
        phone_number = request.form.get('phone_number')
        account_number = request.form.get('account_number')
        bank_name = request.form.get('bank_name')
        
        # Generate transaction ID
        import uuid
        transaction_id = f"{payment_method.upper()}{uuid.uuid4().hex[:10].upper()}"
        
        # Create payment record (if you have Payment model)
        # For now, just show success message
        flash(f'✅ Payment of Tsh {amount:,.2f} received via {payment_method}! Transaction ID: {transaction_id}', 'success')
        return redirect(url_for('client_dashboard'))
    
    return render_template('make_payment.html', loan=loan, user=user)

@app.route('/payment_history')
def payment_history():
    if 'user_id' not in session:
        return render_template("front_page.html")
    
    user = db.session.get(User, session['user_id'])
    # Get payments for the user (if you have Payment model)
    payments = []  # Replace with actual query when Payment model exists
    
    return render_template('payment_history.html', user=user, payments=payments)



@app.route('/admin/staff')

def admin_staff():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    admin_user = db.session.get(User, session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied! Admin only.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get all staff users (all roles except 'client')
    staff_list = User.query.filter(User.role != 'client').order_by(User.created_at.desc()).all()
    
    return render_template('admin_staff.html', staff_list=staff_list)

@app.route('/admin/add_staff', methods=['POST'])
def admin_add_staff():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    admin_user = db.session.get(User, session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    username = request.form.get('username')
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    role = request.form.get('role')
    password = request.form.get('password')
    
    # Check if username exists
    if User.query.filter_by(username=username).first():
        flash('Username already exists!', 'danger')
        return redirect(url_for('admin_staff'))
    
    # Create new staff user
    new_staff = User(
        username=username,
        full_name=full_name,
        email=email,
        phone=phone,
        role=role,
        password=generate_password_hash(password),
        created_at=datetime.now()
    )
    
    db.session.add(new_staff)
    db.session.commit()
    
    flash(f'✅ Staff member {username} added successfully!', 'success')
    return redirect(url_for('admin_staff'))

@app.route('/admin/delete_staff/<int:user_id>', methods=['POST'])
def admin_delete_staff(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    admin_user = db.session.get(User, session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    staff_to_delete = User.query.get_or_404(user_id)
    
    if staff_to_delete.role == 'admin':
        flash('Cannot delete the main admin user!', 'danger')
    else:
        # Check if staff has any approved loans
        if staff_to_delete.role in ['loan_officer', 'loan_manager', 'managing_director', 'general_director']:
            # Delete activity logs for this staff
            ActivityLog.query.filter_by(user_id=staff_to_delete.id).delete()
        
        db.session.delete(staff_to_delete)
        db.session.commit()
        flash(f'✅ Staff {staff_to_delete.username} deleted successfully!', 'success')
    
    return redirect(url_for('admin_staff'))

@app.route('/admin/reset_staff_password/<int:user_id>', methods=['POST'])
def admin_reset_staff_password(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    admin_user = db.session.get(User, session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    staff = User.query.get_or_404(user_id)
    new_password = request.form.get('password', 'mf@123')
    staff.password = generate_password_hash(new_password)
    db.session.commit()
    
    flash(f'✅ Password reset for {staff.username} successfully!', 'success')
    return redirect(url_for('admin_staff'))

@app.route('/repayment_schedule/<int:loan_id>')
def repayment_schedule(loan_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    loan = Loan.query.get_or_404(loan_id)
    
    # Check permission
    if user.id != loan.client_id and user.role not in ['admin', 'loan_officer']:
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    repayments = Repayment.query.filter_by(loan_id=loan_id).order_by(Repayment.due_date).all()
    
    # Update overdue status
    for repayment in repayments:
        if repayment.status == 'pending' and repayment.due_date < datetime.now():
            repayment.status = 'overdue'
            repayment.calculate_late_fee()
    db.session.commit()
    
    total_due = sum(r.amount_due for r in repayments)
    total_paid = sum(r.amount_paid for r in repayments)
    remaining_balance = total_due - total_paid
    payments_made = len([r for r in repayments if r.status == 'paid'])
    
    return render_template('repayment_schedule.html', 
                         loan=loan, 
                         repayments=repayments,
                         total_due=total_due,
                         total_paid=total_paid,
                         remaining_balance=remaining_balance,
                         payments_made=payments_made)

@app.route('/make_scheduled_payment/<int:loan_id>/<int:repayment_id>')
def make_scheduled_payment(loan_id, repayment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    loan = Loan.query.get_or_404(loan_id)
    repayment = Repayment.query.get_or_404(repayment_id)
    
    if user.id != loan.client_id:
        flash('Unauthorized!', 'danger')
        return redirect(url_for('dashboard'))
    
    amount = float(request.args.get('amount', repayment.amount_due))
    
    # Process payment
    repayment.mark_as_paid(amount)
    
    # Add to payment history
    payment = Payment(
        loan_id=loan.id,
        client_id=user.id,
        amount=amount,
        payment_method='Scheduled Payment',
        payment_type='Loan Repayment',
        transaction_id=f'SCHED-{loan.id}-{repayment.id}',
        status='completed',
        payment_date=datetime.now()
    )
    db.session.add(payment)
    db.session.commit()
    
    flash(f'✅ Payment of Tsh {amount:,.2f} received for repayment #{repayment.id}!', 'success')
    return redirect(url_for('repayment_schedule', loan_id=loan.id))

def check_overdue_payments():
    """Check for overdue payments and update status"""
    with app.app_context():
        overdue_repayments = Repayment.query.filter(
            Repayment.status == 'pending',
            Repayment.due_date < datetime.now()
        ).all()
        
        for repayment in overdue_repayments:
            repayment.status = 'overdue'
            late_fee = repayment.calculate_late_fee()
            repayment.late_fee = late_fee
            db.session.commit()
            
            # Send notification for overdue payment
            client = repayment.client
            if client.phone:
                message = f"ORETHAN: Payment of Tsh {repayment.amount_due:,.2f} is OVERDUE! Late fee: Tsh {late_fee:,.2f}. Please pay immediately."
                send_sms(client.phone, message)
        
        return len(overdue_repayments)

@app.route('/financial_reports')
def financial_reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if user.role != 'admin':
        flash('Access denied! Admin only.', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('financial_reports.html', user=user)

@app.route('/api/report/<report_type>')
def api_report(report_type):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = db.session.get(User, session['user_id'])
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    
    try:
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        pass
    
    if report_type == 'loan_summary':
        return loan_summary_report(start_date, end_date)
    elif report_type == 'payment_report':
        return payment_report(start_date, end_date)
    elif report_type == 'client_report':
        return client_report(start_date, end_date)
    elif report_type == 'portfolio_report':
        return portfolio_report(start_date, end_date)
    else:
        return jsonify({'error': 'Invalid report type'}), 400

def loan_summary_report(start_date, end_date):
    query = Loan.query
    if start_date:
        query = query.filter(Loan.created_at >= start_date)
    if end_date:
        query = query.filter(Loan.created_at <= end_date)
    
    loans = query.all()
    
    total_loans = len(loans)
    total_amount = sum(l.amount for l in loans)
    approved_loans = len([l for l in loans if l.status == 'approved'])
    disbursed_loans = len([l for l in loans if l.status == 'disbursed'])
    rejected_loans = len([l for l in loans if l.status == 'rejected'])
    
    # Prepare table data
    columns = ['Loan ID', 'Client Name', 'Amount', 'Purpose', 'Status', 'Stage', 'Application Date']
    rows = []
    for loan in loans:
        rows.append([
            loan.id,
            loan.client.full_name or loan.client.username,
            f"Tsh {loan.amount:,.2f}",
            loan.purpose,
            loan.status.upper(),
            loan.current_stage.replace('_', ' ').title(),
            loan.created_at.strftime('%Y-%m-%d')
        ])
    
    return jsonify({
        'total_loans': total_loans,
        'total_disbursed': total_amount,
        'total_repaid': 0,
        'outstanding_balance': total_amount,
        'columns': columns,
        'rows': rows
    })

def payment_report(start_date, end_date):
    query = Payment.query
    if start_date:
        query = query.filter(Payment.payment_date >= start_date)
    if end_date:
        query = query.filter(Payment.payment_date <= end_date)
    
    payments = query.all()
    
    total_payments = len(payments)
    total_amount = sum(p.amount for p in payments)
    
    columns = ['Payment ID', 'Loan ID', 'Client', 'Amount', 'Method', 'Date', 'Status']
    rows = []
    for payment in payments:
        rows.append([
            payment.id,
            payment.loan_id,
            payment.client.full_name or payment.client.username,
            f"Tsh {payment.amount:,.2f}",
            payment.payment_method,
            payment.payment_date.strftime('%Y-%m-%d') if payment.payment_date else 'N/A',
            payment.status.upper()
        ])
    
    return jsonify({
        'total_loans': total_payments,
        'total_disbursed': total_amount,
        'total_repaid': total_amount,
        'outstanding_balance': 0,
        'columns': columns,
        'rows': rows
    })

def client_report(start_date, end_date):
    query = User.query.filter_by(role='client')
    if start_date:
        query = query.filter(User.created_at >= start_date)
    if end_date:
        query = query.filter(User.created_at <= end_date)
    
    clients = query.all()
    
    total_clients = len(clients)
    total_loans = sum(len(c.loans) for c in clients)
    
    columns = ['Client ID', 'Full Name', 'Username', 'Email', 'Phone', 'Registered', 'Total Loans']
    rows = []
    for client in clients:
        rows.append([
            client.id,
            client.full_name or 'N/A',
            client.username,
            client.email or 'N/A',
            client.phone or 'N/A',
            client.created_at.strftime('%Y-%m-%d') if client.created_at else 'N/A',
            len(client.loans)
        ])
    
    return jsonify({
        'total_loans': total_clients,
        'total_disbursed': total_loans,
        'total_repaid': 0,
        'outstanding_balance': 0,
        'columns': columns,
        'rows': rows
    })

def portfolio_report(start_date, end_date):
    # Get loans by stage
    stage_counts = {
        'loan_officer': Loan.query.filter_by(current_stage='loan_officer').count(),
        'loan_manager': Loan.query.filter_by(current_stage='loan_manager').count(),
        'managing_director': Loan.query.filter_by(current_stage='managing_director').count(),
        'general_director': Loan.query.filter_by(current_stage='general_director').count(),
        'completed': Loan.query.filter_by(current_stage='completed').count()
    }
    
    columns = ['Stage', 'Number of Loans', 'Percentage']
    total = sum(stage_counts.values())
    rows = []
    for stage, count in stage_counts.items():
        percentage = (count / total * 100) if total > 0 else 0
        rows.append([
            stage.replace('_', ' ').title(),
            count,
            f"{percentage:.1f}%"
        ])
    
    return jsonify({
        'total_loans': total,
        'total_disbursed': 0,
        'total_repaid': 0,
        'outstanding_balance': 0,
        'columns': columns,
        'rows': rows
    })

@app.route('/export_report/<report_type>')
def export_report(report_type):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    
    # Get report data
    if report_type == 'loan_summary':
        data = loan_summary_report_data(start_date, end_date)
        filename = f'loan_summary_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
    elif report_type == 'payment_report':
        data = payment_report_data(start_date, end_date)
        filename = f'payment_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
    elif report_type == 'client_report':
        data = client_report_data(start_date, end_date)
        filename = f'client_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
    elif report_type == 'portfolio_report':
        data = portfolio_report_data()
        filename = f'portfolio_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
    else:
        flash('Invalid report type', 'danger')
        return redirect(url_for('financial_reports'))
    
    # Create Excel file
    df = pd.DataFrame(data['rows'], columns=data['columns'])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Report', index=False)
    
    output.seek(0)
    return send_file(output, download_name=filename, as_attachment=True)

def loan_summary_report_data(start_date, end_date):
    query = Loan.query
    if start_date:
        query = query.filter(Loan.created_at >= start_date)
    if end_date:
        query = query.filter(Loan.created_at <= end_date)
    
    loans = query.all()
    rows = []
    for loan in loans:
        rows.append([
            loan.id,
            loan.client.full_name or loan.client.username,
            loan.amount,
            loan.purpose,
            loan.status.upper(),
            loan.current_stage,
            loan.created_at.strftime('%Y-%m-%d')
        ])
    return {'columns': ['Loan ID', 'Client Name', 'Amount', 'Purpose', 'Status', 'Stage', 'Application Date'], 'rows': rows}

def payment_report_data(start_date, end_date):
    query = Payment.query
    if start_date:
        query = query.filter(Payment.payment_date >= start_date)
    if end_date:
        query = query.filter(Payment.payment_date <= end_date)
    
    payments = query.all()
    rows = []
    for payment in payments:
        rows.append([
            payment.id,
            payment.loan_id,
            payment.client.full_name or payment.client.username,
            payment.amount,
            payment.payment_method,
            payment.payment_date.strftime('%Y-%m-%d') if payment.payment_date else 'N/A',
            payment.status
        ])
    return {'columns': ['Payment ID', 'Loan ID', 'Client', 'Amount', 'Method', 'Date', 'Status'], 'rows': rows}

def client_report_data(start_date, end_date):
    query = User.query.filter_by(role='client')
    if start_date:
        query = query.filter(User.created_at >= start_date)
    if end_date:
        query = query.filter(User.created_at <= end_date)
    
    clients = query.all()
    rows = []
    for client in clients:
        rows.append([
            client.id,
            client.full_name or 'N/A',
            client.username,
            client.email or 'N/A',
            client.phone or 'N/A',
            client.created_at.strftime('%Y-%m-%d') if client.created_at else 'N/A',
            len(client.loans)
        ])
    return {'columns': ['Client ID', 'Full Name', 'Username', 'Email', 'Phone', 'Registered', 'Total Loans'], 'rows': rows}

def portfolio_report_data():
    stage_counts = {
        'Loan Officer': Loan.query.filter_by(current_stage='loan_officer').count(),
        'Loan Manager': Loan.query.filter_by(current_stage='loan_manager').count(),
        'Managing Director': Loan.query.filter_by(current_stage='managing_director').count(),
        'General Director': Loan.query.filter_by(current_stage='general_director').count(),
        'Completed': Loan.query.filter_by(current_stage='completed').count()
    }
    total = sum(stage_counts.values())
    rows = []
    for stage, count in stage_counts.items():
        percentage = (count / total * 100) if total > 0 else 0
        rows.append([stage, count, f"{percentage:.1f}%"])
    return {'columns': ['Stage', 'Number of Loans', 'Percentage'], 'rows': rows}

@app.route('/activity_logs')
def activity_logs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if user.role != 'admin':
        flash('Access denied! Admin only.', 'danger')
        return redirect(url_for('dashboard'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    # Summary stats
    total_logs = ActivityLog.query.count()
    unique_users = db.session.query(db.func.count(db.distinct(ActivityLog.user_id))).scalar() or 0
    login_count = ActivityLog.query.filter_by(action='LOGIN').count()
    approval_count = ActivityLog.query.filter_by(action='APPROVE').count()
    
    return render_template('activity_logs.html', 
                         logs=logs.items,
                         page=page,
                         total_pages=logs.pages,
                         total_logs=total_logs,
                         unique_users=unique_users,
                         login_count=login_count,
                         approval_count=approval_count)

from mpesa_api import mpesa

# ==================== MOBILE API ROUTES ====================

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route('/api/login', methods=['POST'])
def api_login():
    """Mobile app login"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            # Create access token
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(days=30)
            )
            
            return jsonify({
                'success': True,
                'token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'email': user.email,
                    'phone': user.phone,
                    'role': user.role
                }
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/my_loans', methods=['GET'])
@jwt_required()
def api_my_loans():
    """Get user's loans"""
    try:
        user_id = get_jwt_identity()
        loans = Loan.query.filter_by(client_id=user_id).order_by(Loan.created_at.desc()).all()
        
        loan_list = []
        for loan in loans:
            loan_list.append({
                'id': loan.id,
                'amount': loan.amount,
                'amount_formatted': f'Tsh {loan.amount:,.2f}',
                'purpose': loan.purpose,
                'status': loan.status,
                'current_stage': loan.current_stage,
                'stage_name': loan.get_current_stage_name() if hasattr(loan, 'get_current_stage_name') else loan.current_stage,
                'term_months': loan.term_months,
                'monthly_payment': loan.monthly_payment,
                'monthly_payment_formatted': f'Tsh {loan.monthly_payment:,.2f}',
                'created_at': loan.created_at.strftime('%Y-%m-%d %H:%M:%S') if loan.created_at else None
            })
        
        return jsonify({'success': True, 'loans': loan_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/apply_loan', methods=['POST'])
@jwt_required()
def api_apply_loan():
    """Apply for individual loan"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        amount = float(data.get('amount'))
        purpose = data.get('purpose')
        term_months = int(data.get('term_months', 12))
        monthly_payment = amount / term_months
        
        new_loan = Loan(
            client_id=user_id,
            amount=amount,
            purpose=purpose,
            term_months=term_months,
            monthly_payment=monthly_payment,
            status='pending',
            current_stage='loan_officer',
            created_at=datetime.now()
        )
        
        db.session.add(new_loan)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Loan application submitted',
            'loan_id': new_loan.id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def api_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'phone': user.phone,
                'role': user.role,
                'joined_date': user.created_at.strftime('%Y-%m-%d') if user.created_at else None
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/dashboard_stats', methods=['GET'])
@jwt_required()
def api_dashboard_stats():
    """Get dashboard statistics"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if user.role == 'client':
            loans = Loan.query.filter_by(client_id=user.id).all()
            total_loans = len(loans)
            active_loans = len([l for l in loans if l.status == 'approved'])
            completed_loans = len([l for l in loans if l.status == 'completed'])
            pending_loans = len([l for l in loans if l.status == 'pending'])
            
            return jsonify({
                'success': True,
                'stats': {
                    'total_loans': total_loans,
                    'active_loans': active_loans,
                    'completed_loans': completed_loans,
                    'pending_loans': pending_loans
                }
            }), 200
        else:
            # Staff stats
            total_clients = User.query.filter_by(role='client').count()
            total_loans = Loan.query.count()
            pending_approvals = Loan.query.filter_by(status='pending').count()
            
            return jsonify({
                'success': True,
                'stats': {
                    'total_clients': total_clients,
                    'total_loans': total_loans,
                    'pending_approvals': pending_approvals
                }
            }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/mpesa_payment/<int:loan_id>', methods=['POST'])
def mpesa_payment(loan_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    loan = Loan.query.get_or_404(loan_id)
    
    if loan.client_id != user.id:
        flash('Unauthorized!', 'danger')
        return redirect(url_for('dashboard'))
    
    phone_number = request.form.get('phone_number')
    amount = float(request.form.get('amount'))
    
    # Call M-Pesa API
    response = mpesa.stk_push(
        phone_number=phone_number,
        amount=amount,
        account_reference=f'LOAN{loan.id}',
        transaction_desc=f'Loan repayment {loan.id}'
    )
    
    if response.get('ResponseCode') == '0':
        # Save transaction
        checkout_id = response.get('CheckoutRequestID')
        
        transaction = Payment(
            loan_id=loan.id,
            client_id=user.id,
            amount=amount,
            payment_method='M-Pesa',
            payment_type='Loan Repayment',
            transaction_id=checkout_id,
            phone_number=phone_number,
            status='pending',
            reference_number=checkout_id,
            payment_date=datetime.now()
        )
        db.session.add(transaction)
        db.session.commit()
        
        flash(f'✅ M-Pesa payment initiated! Check your phone to complete payment.', 'success')
    else:
        flash(f'❌ Payment failed: {response.get("ResponseDescription", "Unknown error")}', 'danger')
    
    return redirect(url_for('repayment_schedule', loan_id=loan_id))

@app.route('/mpesa_callback', methods=['POST'])
def mpesa_callback():
    """M-Pesa callback URL for payment confirmation"""
    try:
        data = request.get_json()
        if data:
            # Extract transaction details
            result_code = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
            checkout_id = data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
            callback_metadata = data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {})
            
            # Find transaction
            transaction = Payment.query.filter_by(transaction_id=checkout_id).first()
            
            if transaction:
                if result_code == '0':
                    # Successful payment
                    amount = callback_metadata.get('Item', [{}])[0].get('Value', 0)
                    mpesa_receipt = callback_metadata.get('Item', [{}])[1].get('Value', '')
                    
                    transaction.status = 'completed'
                    transaction.transaction_id = mpesa_receipt
                    transaction.amount = amount
                else:
                    transaction.status = 'failed'
                
                db.session.commit()
                
                # Update loan repayment schedule
                if transaction.status == 'completed':
                    repayment = Repayment.query.filter_by(loan_id=transaction.loan_id, status='pending').first()
                    if repayment:
                        repayment.mark_as_paid(transaction.amount)
                        db.session.commit()
        
        return {'ResultCode': 0, 'ResultDesc': 'Success'}
    except Exception as e:
        return {'ResultCode': 1, 'ResultDesc': str(e)}

@app.route('/api/realtime_stats')
def realtime_stats():
    """Get real-time statistics for dashboard"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    from sqlalchemy import func
    
    # Get real-time counts
    total_loans = Loan.query.count()
    pending_loans = Loan.query.filter_by(status='pending').count()
    approved_loans = Loan.query.filter_by(status='approved').count()
    rejected_loans = Loan.query.filter_by(status='rejected').count()
    total_clients = User.query.filter_by(role='client').count()
    
    # Get real-time revenue
    total_revenue = db.session.query(func.sum(Payment.amount)).filter(
        Payment.status == 'completed'
    ).scalar() or 0
    
    # Get today's activity
    today = datetime.now().replace(hour=0, minute=0, second=0)
    today_loans = Loan.query.filter(Loan.created_at >= today).count()
    today_payments = Payment.query.filter(Payment.payment_date >= today).count()
    
    return jsonify({
        'success': True,
        'stats': {
            'total_loans': total_loans,
            'pending_loans': pending_loans,
            'approved_loans': approved_loans,
            'rejected_loans': rejected_loans,
            'total_clients': total_clients,
            'total_revenue': float(total_revenue),
            'today_loans': today_loans,
            'today_payments': today_payments
        },
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_staff()
    print("✅ Orethan Microfinance Platform running at http://127.0.0.1:5000")
    print("🏦 Complete Group Loan System Ready!")
    print("👤 Staff Login: mf@123")
    app.run(debug=True, host='127.0.0.1', port=5000)
