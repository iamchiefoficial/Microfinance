# Production-Ready Microfinance Platform
from flask import Flask, request, render_template_string, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from datetime import datetime, timedelta
import decimal

app = Flask(__name__)
app.config['SECRET_KEY'] = 'microfinance_platform_2025_secure_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/microfinance_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    national_id = db.Column(db.String(50), unique=True, nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    monthly_income = db.Column(db.Numeric(12,2), nullable=False)
    role = db.Column(db.String(50), default='client')
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

# Loan Model
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Numeric(12,2), nullable=False)
    purpose = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='pending')
    current_stage = db.Column(db.String(50), default='loan_officer')
    interest_rate = db.Column(db.Numeric(5,2), default=15.00)
    term_months = db.Column(db.Integer, default=12)
    monthly_payment = db.Column(db.Numeric(12,2))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    client = db.relationship('User', backref='loans')

# Loan Approval Model
class LoanApproval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    approver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stage = db.Column(db.String(50), nullable=False)
    decision = db.Column(db.String(20), nullable=False)
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    loan = db.relationship('Loan', backref='approvals')
    approver = db.relationship('User', backref='loan_decisions')

# Transaction Model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    amount = db.Column(db.Numeric(12,2), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # payment, disbursement
    payment_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    balance_after = db.Column(db.Numeric(12,2))
    notes = db.Column(db.Text)
    
    loan = db.relationship('Loan', backref='transactions')

# Create database tables
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Database error: {e}")

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
        
        user = User.query.filter_by(username=username, is_active=True).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        
        return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Login Failed - Microfinance</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px; background: #f0f0f0;">
    <div style="max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h1 style="color: #dc3545;">Login Failed</h1>
        <p>Invalid username or password</p>
        <a href="/login" style="display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">Try Again</a>
    </div>
</body>
</html>
        ''')
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Login - Microfinance Platform</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #0b2b26 0%, #1a4a3f 100%); min-height: 100vh;">
    <div style="max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h1 style="color: #1e3e38; font-size: 24px;">🏦 Microfinance Platform</h1>
        <h2 style="color: #5e8b80;">Login</h2>
        <form method="post">
            <input type="text" name="username" placeholder="Username" required style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="password" name="password" placeholder="Password" required style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <button type="submit" style="width: 100%; padding: 12px; background: #1d6f5e; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">Login</button>
        </form>
        <p style="margin-top: 20px;"><a href="/register" style="color: #1d6f5e;">Create Account</a></p>
    </div>
</body>
</html>
    ''')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        national_id = request.form.get('national_id')
        occupation = request.form.get('occupation')
        monthly_income = request.form.get('monthly_income')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        if User.query.filter_by(username=username).first():
            return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Registration Failed</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px;">
    <div style="max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h1 style="color: #dc3545;">Registration Failed</h1>
        <p>Username already exists!</p>
        <a href="/register" style="display: inline-block; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px;">Try Again</a>
    </div>
</body>
</html>
            ''')
        
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            email=email,
            national_id=national_id,
            occupation=occupation,
            monthly_income=float(monthly_income),
            phone=phone,
            address=address,
            role='client'
        )
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Register - Microfinance Platform</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #0b2b26 0%, #1a4a3f 100%); min-height: 100vh;">
    <div style="max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h1 style="color: #1e3e38; font-size: 24px;">🏦 Microfinance Platform</h1>
        <h2 style="color: #5e8b80;">Create Account</h2>
        <form method="post">
            <input type="text" name="full_name" placeholder="Full Name" required style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="email" name="email" placeholder="Email" required style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="text" name="national_id" placeholder="National ID" required style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="text" name="occupation" placeholder="Occupation" required style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="number" name="monthly_income" placeholder="Monthly Income" required style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="text" name="phone" placeholder="Phone Number" style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <textarea name="address" placeholder="Address" style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px; height: 60px;"></textarea><br>
            <input type="text" name="username" placeholder="Username" required style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="password" name="password" placeholder="Password" required style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <button type="submit" style="width: 100%; padding: 12px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">Create Account</button>
        </form>
        <p style="margin-top: 20px;"><a href="/login" style="color: #1d6f5e;">Back to Login</a></p>
    </div>
</body>
</html>
    ''')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    # Calculate real statistics
    total_clients = User.query.filter_by(role='client', is_active=True).count()
    total_loans = Loan.query.count()
    pending_loans = Loan.query.filter_by(status='pending').count()
    approved_loans = Loan.query.filter_by(status='approved').count()
    total_loan_amount = db.session.query(db.func.sum(Loan.amount)).filter_by(status='approved').scalar() or 0
    total_revenue = db.session.query(db.func.sum(Transaction.amount)).filter_by(transaction_type='payment').scalar() or 0
    
    # Get recent data
    recent_clients = User.query.filter_by(role='client', is_active=True).order_by(User.created_at.desc()).limit(5).all()
    recent_loans = Loan.query.order_by(Loan.created_at.desc()).limit(5).all()
    
    # Get pending loans for staff
    pending_loan_list = []
    if user.role in ['loan_officer', 'loan_manager', 'general_director', 'managing_director']:
        stage_mapping = {
            'loan_officer': 'loan_officer',
            'loan_manager': 'loan_manager',
            'general_director': 'general_director',
            'managing_director': 'managing_director'
        }
        pending_loan_list = Loan.query.filter_by(
            current_stage=stage_mapping[user.role],
            status='pending'
        ).all()
    
    return render_template_string(f'''
<!DOCTYPE html>
<html>
<head><title>Dashboard - Microfinance Platform</title></head>
<body style="font-family: Arial; padding: 20px; background: #f5f5f5; min-height: 100vh;">
    <div style="max-width: 1400px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <!-- Header -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 2px solid #e0e0e0; padding-bottom: 20px;">
            <div>
                <h1 style="color: #1e3e38; margin: 0;">🏦 Microfinance Platform</h1>
                <h2 style="color: #5e8b80; margin: 5px 0;">Welcome, {user.full_name}!</h2>
                <p style="margin: 5px 0;"><strong>Role:</strong> {user.role.title()}</p>
                <p style="margin: 5px 0;"><strong>Email:</strong> {user.email}</p>
            </div>
            <div style="text-align: right;">
                <form method="post" action="/logout" style="margin: 0;">
                    <button type="submit" style="padding: 10px 20px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer;">Logout</button>
                </form>
            </div>
        </div>
        
        <!-- Statistics Cards -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h3 style="margin: 0; font-size: 16px;">Total Clients</h3>
                <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">{total_clients}</p>
                <p style="margin: 0; font-size: 14px;">Active borrowers</p>
            </div>
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h3 style="margin: 0; font-size: 16px;">Total Loans</h3>
                <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">{total_loans}</p>
                <p style="margin: 0; font-size: 14px;">All applications</p>
            </div>
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h3 style="margin: 0; font-size: 16px;">Pending Loans</h3>
                <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">{pending_loans}</p>
                <p style="margin: 0; font-size: 14px;">Awaiting approval</p>
            </div>
            <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h3 style="margin: 0; font-size: 16px;">Portfolio Value</h3>
                <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">${total_loan_amount:,.0f}</p>
                <p style="margin: 0; font-size: 14px;">Total approved</p>
            </div>
            <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h3 style="margin: 0; font-size: 16px;">Revenue</h3>
                <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">${total_revenue:,.0f}</p>
                <p style="margin: 0; font-size: 14px;">Total payments</p>
            </div>
        </div>
        
        <!-- Main Content Area -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
            <!-- Recent Clients -->
            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px;">
                <h3 style="color: #1e3e38; margin-bottom: 20px;">Recent Clients</h3>
                <div style="max-height: 300px; overflow-y: auto;">
                    {"".join([f"<div style='background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px; border-left: 4px solid #1d6f5e;'><div style='font-weight: bold;'>{client.full_name}</div><div style='color: #666; font-size: 14px;'>{client.occupation}</div><div style='color: #1d6f5e; font-weight: bold;'>${client.monthly_income:,.0f}/month</div><div style='color: #999; font-size: 12px;'>Joined: {client.created_at.strftime('%Y-%m-%d')}</div></div>" for client in recent_clients]) if recent_clients else "<p style='color: #666; text-align: center; padding: 40px;'>No clients registered yet</p>"}
                </div>
            </div>
            
            <!-- Recent Loans -->
            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px;">
                <h3 style="color: #1e3e38; margin-bottom: 20px;">Recent Loans</h3>
                <div style="max-height: 300px; overflow-y: auto;">
                    {"".join([f"<div style='background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px; border-left: 4px solid {'#28a745' if loan.status == 'approved' else '#ffc107' if loan.status == 'pending' else '#dc3545'};'><div style='font-weight: bold;'>{loan.client.full_name}</div><div style='color: #666; font-size: 14px;'>{loan.purpose}</div><div style='color: #1d6f5e; font-weight: bold;'>${loan.amount:,.0f}</div><div style='color: {'#28a745' if loan.status == 'approved' else '#ffc107' if loan.status == 'pending' else '#dc3545'}; font-weight: bold; text-transform: uppercase;'>{loan.status}</div></div>" for loan in recent_loans]) if recent_loans else "<p style='color: #666; text-align: center; padding: 40px;'>No loans yet</p>"}
                </div>
            </div>
        </div>
        
        <!-- Pending Loans for Staff -->
        {"<div style='margin-top: 30px; background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 4px solid #ffc107;'><h3 style='color: #856404; margin-bottom: 20px;'>Pending Loans for Your Review</h3><div style='display: grid; gap: 15px;'>" if pending_loan_list else ""}
        {"".join([f"<div style='background: white; padding: 20px; border-radius: 8px; border: 1px solid #ffc107;'><div style='display: flex; justify-content: space-between; align-items: start;'><div><h4 style='margin: 0 0 10px 0; color: #1e3e38;'>{loan.client.full_name}</h4><p style='margin: 5px 0;'><strong>Amount:</strong> ${loan.amount:,.0f}</p><p style='margin: 5px 0;'><strong>Purpose:</strong> {loan.purpose}</p><p style='margin: 5px 0;'><strong>Applied:</strong> {loan.created_at.strftime('%Y-%m-%d')}</p><p style='margin: 5px 0;'><strong>Client Income:</strong> ${loan.client.monthly_income:,.0f}/month</p></div><div><form method='post' action='/approve_loan' style='margin: 0;'><input type='hidden' name='loan_id' value='{loan.id}'><button type='submit' name='decision' value='approved' style='padding: 8px 16px; background: #28a745; color: white; border: none; border-radius: 5px; margin-bottom: 5px; width: 100%; cursor: pointer;'>Approve</button><button type='submit' name='decision' value='rejected' style='padding: 8px 16px; background: #dc3545; color: white; border: none; border-radius: 5px; width: 100%; cursor: pointer;'>Reject</button></form></div></div></div>" for loan in pending_loan_list]) if pending_loan_list else ""}
        {"</div></div>" if pending_loan_list else ""}
        
        <!-- Client Loan Application -->
        {"<div style='margin-top: 30px; background: #e3f2fd; padding: 25px; border-radius: 10px; border-left: 4px solid #2196f3;'><h3 style='color: #1565c0; margin-bottom: 20px;'>Apply for Loan</h3><form method='post' action='/apply_loan' style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px;'><input type='number' name='amount' placeholder='Loan Amount' required style='padding: 10px; border: 1px solid #ddd; border-radius: 5px;'><input type='text' name='purpose' placeholder='Purpose' required style='padding: 10px; border: 1px solid #ddd; border-radius: 5px;'><input type='number' name='term_months' placeholder='Term (months)' value='12' style='padding: 10px; border: 1px solid #ddd; border-radius: 5px;'><input type='number' name='interest_rate' placeholder='Interest Rate (%)' value='15' step='0.1' style='padding: 10px; border: 1px solid #ddd; border-radius: 5px;'><button type='submit' style='grid-column: 1 / -1; padding: 12px; background: #2196f3; color: white; border: none; border-radius: 5px; cursor: pointer;'>Submit Application</button></form></div>" if user.role == 'client' else ""}
        
    </div>
</body>
</html>
    ''')

@app.route('/apply_loan', methods=['POST'])
def apply_loan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if user.role != 'client':
        return redirect(url_for('dashboard'))
    
    amount = request.form.get('amount')
    purpose = request.form.get('purpose')
    term_months = request.form.get('term_months', 12)
    interest_rate = request.form.get('interest_rate', 15)
    
    # Calculate monthly payment
    principal = float(amount)
    rate = float(interest_rate) / 100 / 12
    term = int(term_months)
    monthly_payment = principal * (rate * (1 + rate)**term) / ((1 + rate)**term - 1)
    
    loan = Loan(
        client_id=user.id,
        amount=principal,
        purpose=purpose,
        status='pending',
        current_stage='loan_officer',
        term_months=term,
        interest_rate=float(interest_rate),
        monthly_payment=monthly_payment
    )
    db.session.add(loan)
    db.session.commit()
    
    return redirect(url_for('dashboard'))

@app.route('/approve_loan', methods=['POST'])
def approve_loan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if user.role not in ['loan_officer', 'loan_manager', 'general_director', 'managing_director']:
        return redirect(url_for('dashboard'))
    
    loan_id = request.form.get('loan_id')
    decision = request.form.get('decision')
    
    loan = Loan.query.get(loan_id)
    if not loan:
        return redirect(url_for('dashboard'))
    
    # Create approval record
    approval = LoanApproval(
        loan_id=loan_id,
        approver_id=user.id,
        stage=user.role,
        decision=decision
    )
    db.session.add(approval)
    
    # Update loan status
    if decision == 'approved':
        stage_order = ['loan_officer', 'loan_manager', 'general_director', 'managing_director']
        current_index = stage_order.index(loan.current_stage)
        
        if current_index < len(stage_order) - 1:
            loan.current_stage = stage_order[current_index + 1]
        else:
            loan.status = 'approved'
            # Create disbursement transaction
            transaction = Transaction(
                loan_id=loan_id,
                amount=loan.amount,
                transaction_type='disbursement',
                balance_after=loan.amount
            )
            db.session.add(transaction)
    else:
        loan.status = 'rejected'
    
    loan.updated_at = datetime.utcnow()
    db.session.commit()
    
    return redirect(url_for('dashboard'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("🚀 Starting Production Microfinance Platform...")
    print("🌐 Access at: http://127.0.0.1:5000")
    print("✅ Features: Complete Client Management, Loan Workflow, Real Analytics")
    print("💼 Professional Banking System Ready!")
    app.run(host='127.0.0.1', port=5000, debug=False)
