# Professional Microfinance Platform with Real Functionality
from flask import Flask, request, render_template_string, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from datetime import datetime, timedelta

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
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Loan Model
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Numeric(12,2), nullable=False)
    purpose = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='pending')
    current_stage = db.Column(db.String(50), default='loan_officer')
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
        
        user = User.query.filter_by(username=username).first()
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
        <h1>Login Failed</h1>
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
        <h1 style="color: #1e3e38;">🏦 Microfinance Platform</h1>
        <h2>Login</h2>
        <form method="post">
            <input type="text" name="username" placeholder="Username" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="password" name="password" placeholder="Password" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <button type="submit" style="width: 100%; padding: 10px; background: #1d6f5e; color: white; border: none; border-radius: 5px; cursor: pointer;">Login</button>
        </form>
        <p><a href="/register">Create Account</a></p>
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
        
        if User.query.filter_by(username=username).first():
            return "Username already exists!"
        
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            email=email,
            national_id=national_id,
            occupation=occupation,
            monthly_income=float(monthly_income),
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
        <h1 style="color: #1e3e38;">🏦 Microfinance Platform</h1>
        <h2>Create Account</h2>
        <form method="post">
            <input type="text" name="full_name" placeholder="Full Name" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="email" name="email" placeholder="Email" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="text" name="national_id" placeholder="National ID" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="text" name="occupation" placeholder="Occupation" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="number" name="monthly_income" placeholder="Monthly Income" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="text" name="username" placeholder="Username" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="password" name="password" placeholder="Password" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <button type="submit" style="width: 100%; padding: 10px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer;">Create Account</button>
        </form>
        <p><a href="/login">Back to Login</a></p>
    </div>
</body>
</html>
    ''')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    # Calculate statistics
    total_clients = User.query.filter_by(role='client').count()
    total_loans = Loan.query.count()
    pending_loans = Loan.query.filter_by(status='pending').count()
    approved_loans = Loan.query.filter_by(status='approved').count()
    total_loan_amount = db.session.query(db.func.sum(Loan.amount)).filter_by(status='approved').scalar() or 0
    
    # Get recent data
    recent_clients = User.query.filter_by(role='client').order_by(User.created_at.desc()).limit(5).all()
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
<body style="font-family: Arial; padding: 20px; background: #f0f0f0; min-height: 100vh;">
    <div style="max-width: 1200px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 2px solid #e0e0e0; padding-bottom: 20px;">
            <div>
                <h1 style="color: #1e3e38; margin: 0;">🏦 Microfinance Platform</h1>
                <h2 style="color: #5e8b80; margin: 5px 0;">Welcome, {user.full_name}!</h2>
                <p style="margin: 5px 0;"><strong>Role:</strong> {user.role.title()}</p>
                <p style="margin: 5px 0;"><strong>Email:</strong> {user.email}</p>
            </div>
            <form method="post" action="/logout" style="margin: 0;">
                <button type="submit" style="padding: 10px 20px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer;">Logout</button>
            </form>
        </div>
        
        <!-- Statistics Cards -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px;">
            <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; border-left: 4px solid #28a745;">
                <h3 style="margin: 0; color: #155724;">Total Clients</h3>
                <p style="font-size: 24px; font-weight: bold; margin: 10px 0;">{total_clients}</p>
            </div>
            <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; border-left: 4px solid #2196f3;">
                <h3 style="margin: 0; color: #0d47a1;">Total Loans</h3>
                <p style="font-size: 24px; font-weight: bold; margin: 10px 0;">{total_loans}</p>
            </div>
            <div style="background: #fff3e0; padding: 20px; border-radius: 8px; border-left: 4px solid #ff9800;">
                <h3 style="margin: 0; color: #e65100;">Pending Loans</h3>
                <p style="font-size: 24px; font-weight: bold; margin: 10px 0;">{pending_loans}</p>
            </div>
            <div style="background: #fce4ec; padding: 20px; border-radius: 8px; border-left: 4px solid #e91e63;">
                <h3 style="margin: 0; color: #880e4f;">Approved Loans</h3>
                <p style="font-size: 24px; font-weight: bold; margin: 10px 0;">{approved_loans}</p>
            </div>
        </div>
        
        <!-- Recent Clients -->
        <div style="margin-bottom: 30px;">
            <h3>Recent Clients</h3>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
                {"".join([f"<div style='padding: 10px; border-bottom: 1px solid #e0e0e0;'><strong>{client.full_name}</strong> - {client.occupation} - Income: ${client.monthly_income:,.0f}</div>" for client in recent_clients]) if recent_clients else "<p>No clients registered yet</p>"}
            </div>
        </div>
        
        <!-- Pending Loans for Staff -->
        {"<div style='margin-bottom: 30px;'><h3>Pending Loans for Your Review</h3>" if pending_loan_list else ""}
        {"".join([f"<div style='background: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #ffc107;'><strong>{loan.client.full_name}</strong><br>Amount: ${loan.amount:,.0f}<br>Purpose: {loan.purpose}<br>Applied: {loan.created_at.strftime('%Y-%m-%d')}<br><form method='post' action='/approve_loan' style='margin-top: 10px;'><input type='hidden' name='loan_id' value='{loan.id}'><button type='submit' name='decision' value='approved' style='padding: 5px 10px; background: #28a745; color: white; border: none; border-radius: 3px; margin-right: 5px;'>Approve</button><button type='submit' name='decision' value='rejected' style='padding: 5px 10px; background: #dc3545; color: white; border: none; border-radius: 3px;'>Reject</button></form></div>" for loan in pending_loan_list]) if pending_loan_list else ""}
        {"</div>" if pending_loan_list else ""}
        
        <!-- Client Loan Application -->
        {"<div style='margin-bottom: 30px;'><h3>Apply for Loan</h3><form method='post' action='/apply_loan'><input type='number' name='amount' placeholder='Loan Amount' required style='width: 200px; padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 5px;'><input type='text' name='purpose' placeholder='Purpose' required style='width: 300px; padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 5px;'><button type='submit' style='padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;'>Apply</button></form></div>" if user.role == 'client' else ""}
        
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
    
    loan = Loan(
        client_id=user.id,
        amount=float(amount),
        purpose=purpose,
        status='pending',
        current_stage='loan_officer'
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
    print("🚀 Starting Professional Microfinance Platform...")
    print("🌐 Access at: http://127.0.0.1:5000")
    print("✅ Features: Real Client Management, Loan Workflow, Staff Dashboard")
    app.run(host='127.0.0.1', port=5000, debug=False)
