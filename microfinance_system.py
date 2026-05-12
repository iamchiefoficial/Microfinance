# Complete Professional Microfinance Banking System
from flask import Flask, request, render_template_string, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from datetime import datetime, timedelta
import decimal

app = Flask(__name__)
app.config['SECRET_KEY'] = 'microfinance_platform_pro_2025'
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
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Loan Model
class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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

# Transaction Model
class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    amount = db.Column(db.Numeric(12,2), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    balance_after = db.Column(db.Numeric(12,2))
    notes = db.Column(db.Text)
    
    loan = db.relationship('Loan', backref='transactions')

# Initialize database
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
        else:
            flash('Invalid username or password')
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Login - Microfinance Platform</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #0b2b26 0%, #1a4a3f 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .login-container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); width: 400px; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { color: #1e3e38; font-size: 28px; margin: 0; }
        .logo p { color: #5e8b80; margin: 5px 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; color: #333; font-weight: bold; }
        .form-group input { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; }
        .form-group input:focus { border-color: #1d6f5e; outline: none; }
        .btn { width: 100%; padding: 12px; background: #1d6f5e; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: background 0.3s; }
        .btn:hover { background: #155742; }
        .links { text-align: center; margin-top: 20px; }
        .links a { color: #1d6f5e; text-decoration: none; }
        .alert { background: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <h1>🏦 Microfinance Platform</h1>
            <p>Professional Banking System</p>
        </div>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="post">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="Enter username" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Enter password" required>
            </div>
            <button type="submit" class="btn">Login</button>
        </form>
        
        <div class="links">
            <p>Don't have an account? <a href="/register">Register here</a></p>
        </div>
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
            flash('Username already exists!')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!')
            return redirect(url_for('register'))
        
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
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Register - Microfinance Platform</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #0b2b26 0%, #1a4a3f 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
        .register-container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); width: 500px; max-height: 90vh; overflow-y: auto; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { color: #1e3e38; font-size: 28px; margin: 0; }
        .logo p { color: #5e8b80; margin: 5px 0; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; color: #333; font-weight: bold; }
        .form-group input, .form-group textarea { width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 8px; font-size: 14px; }
        .form-group input:focus, .form-group textarea:focus { border-color: #1d6f5e; outline: none; }
        .form-group textarea { height: 60px; resize: vertical; }
        .btn { width: 100%; padding: 12px; background: #28a745; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: background 0.3s; }
        .btn:hover { background: #218838; }
        .links { text-align: center; margin-top: 20px; }
        .links a { color: #1d6f5e; text-decoration: none; }
        .alert { background: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="register-container">
        <div class="logo">
            <h1>🏦 Microfinance Platform</h1>
            <p>Create Your Account</p>
        </div>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="post">
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" name="full_name" placeholder="Enter your full name" required>
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" name="email" placeholder="Enter your email" required>
            </div>
            <div class="form-group">
                <label>National ID</label>
                <input type="text" name="national_id" placeholder="Enter national ID" required>
            </div>
            <div class="form-group">
                <label>Occupation</label>
                <input type="text" name="occupation" placeholder="Enter your occupation" required>
            </div>
            <div class="form-group">
                <label>Monthly Income</label>
                <input type="number" name="monthly_income" placeholder="Enter monthly income" required>
            </div>
            <div class="form-group">
                <label>Phone Number</label>
                <input type="text" name="phone" placeholder="Enter phone number">
            </div>
            <div class="form-group">
                <label>Address</label>
                <textarea name="address" placeholder="Enter your address"></textarea>
            </div>
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="Choose a username" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Choose a password" required>
            </div>
            <button type="submit" class="btn">Create Account</button>
        </form>
        
        <div class="links">
            <p>Already have an account? <a href="/login">Login here</a></p>
        </div>
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
<head>
    <title>Dashboard - Microfinance Platform</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); overflow: hidden; }
        .header { background: linear-gradient(135deg, #1e3e38 0%, #2a5f54 100%); color: white; padding: 30px; display: flex; justify-content: space-between; align-items: center; }
        .header h1 { margin: 0; font-size: 32px; }
        .header .user-info { text-align: right; }
        .header .user-info h2 { margin: 0; font-size: 20px; }
        .header .user-info p { margin: 5px 0; opacity: 0.9; }
        .content { padding: 30px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px; }
        .stat-card { padding: 25px; border-radius: 12px; color: white; position: relative; overflow: hidden; }
        .stat-card::before { content: ''; position: absolute; top: 0; right: 0; width: 100px; height: 100px; background: rgba(255,255,255,0.1); border-radius: 50%; transform: translate(30px, -30px); }
        .stat-card h3 { margin: 0 0 10px 0; font-size: 16px; opacity: 0.9; }
        .stat-card .number { font-size: 36px; font-weight: bold; margin: 0; }
        .stat-card .label { margin: 5px 0 0 0; opacity: 0.8; }
        .card-blue { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card-green { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
        .card-orange { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
        .card-red { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        .card-purple { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        .section { margin-bottom: 30px; }
        .section h3 { color: #1e3e38; margin-bottom: 20px; font-size: 24px; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }
        .data-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
        .data-list { background: #f8f9fa; padding: 25px; border-radius: 12px; max-height: 400px; overflow-y: auto; }
        .data-item { background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px; border-left: 4px solid #1d6f5e; }
        .data-item h4 { margin: 0 0 5px 0; color: #1e3e38; }
        .data-item p { margin: 5px 0; color: #666; font-size: 14px; }
        .loan-item { background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px; border-left: 4px solid #ffc107; }
        .loan-item.approved { border-left-color: #28a745; }
        .loan-item.rejected { border-left-color: #dc3545; }
        .loan-item h4 { margin: 0 0 5px 0; color: #1e3e38; }
        .loan-item p { margin: 5px 0; color: #666; font-size: 14px; }
        .loan-actions { margin-top: 10px; }
        .btn { padding: 8px 16px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; margin-right: 5px; }
        .btn-approve { background: #28a745; color: white; }
        .btn-reject { background: #dc3545; color: white; }
        .btn-apply { background: #007bff; color: white; }
        .logout-btn { padding: 10px 20px; background: #dc3545; color: white; border: none; border-radius: 8px; cursor: pointer; }
        .loan-form { background: #e3f2fd; padding: 25px; border-radius: 12px; border-left: 4px solid #2196f3; }
        .loan-form form { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .loan-form input { padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .loan-form button { grid-column: 1 / -1; padding: 12px; background: #2196f3; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .empty-state { text-align: center; padding: 40px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>🏦 Microfinance Platform</h1>
                <h2>Welcome, {user.full_name}!</h2>
            </div>
            <div class="user-info">
                <h2>{user.role.title()}</h2>
                <p>{user.email}</p>
                <form method="post" action="/logout" style="margin: 10px 0 0 0;">
                    <button type="submit" class="logout-btn">Logout</button>
                </form>
            </div>
        </div>
        
        <div class="content">
            <div class="stats-grid">
                <div class="stat-card card-blue">
                    <h3>Total Clients</h3>
                    <div class="number">{total_clients}</div>
                    <div class="label">Active borrowers</div>
                </div>
                <div class="stat-card card-green">
                    <h3>Total Loans</h3>
                    <div class="number">{total_loans}</div>
                    <div class="label">All applications</div>
                </div>
                <div class="stat-card card-orange">
                    <h3>Pending Loans</h3>
                    <div class="number">{pending_loans}</div>
                    <div class="label">Awaiting approval</div>
                </div>
                <div class="stat-card card-red">
                    <h3>Approved Loans</h3>
                    <div class="number">{approved_loans}</div>
                    <div class="label">Active loans</div>
                </div>
                <div class="stat-card card-purple">
                    <h3>Portfolio Value</h3>
                    <div class="number">${total_loan_amount:,.0f}</div>
                    <div class="label">Total approved amount</div>
                </div>
            </div>
            
            <div class="data-grid">
                <div class="section">
                    <h3>Recent Clients</h3>
                    <div class="data-list">
                        {"".join([f"<div class='data-item'><h4>{client.full_name}</h4><p>{client.occupation} • Income: ${client.monthly_income:,.0f}/month</p><p>Joined: {client.created_at.strftime('%Y-%m-%d')}</p></div>" for client in recent_clients]) if recent_clients else "<div class='empty-state'>No clients registered yet</div>"}
                    </div>
                </div>
                
                <div class="section">
                    <h3>Recent Loans</h3>
                    <div class="data-list">
                        {"".join([f"<div class='data-item loan-item {loan.status}'><h4>{loan.client.full_name}</h4><p>Amount: ${loan.amount:,.0f} • {loan.purpose}</p><p>Status: {loan.status.upper()} • {loan.created_at.strftime('%Y-%m-%d')}</p></div>" for loan in recent_loans]) if recent_loans else "<div class='empty-state'>No loans yet</div>"}
                    </div>
                </div>
            </div>
            
            {"<div class='section'><h3>Pending Loans for Your Review</h3>" if pending_loan_list else ""}
            {"".join([f"<div class='loan-item'><h4>{loan.client.full_name}</h4><p>Amount: ${loan.amount:,.0f} • Purpose: {loan.purpose}</p><p>Applied: {loan.created_at.strftime('%Y-%m-%d')} • Client Income: ${loan.client.monthly_income:,.0f}/month</p><div class='loan-actions'><form method='post' action='/approve_loan' style='margin: 0;'><input type='hidden' name='loan_id' value='{loan.id}'><button type='submit' name='decision' value='approved' class='btn btn-approve'>Approve</button><button type='submit' name='decision' value='rejected' class='btn btn-reject'>Reject</button></form></div></div>" for loan in pending_loan_list]) if pending_loan_list else ""}
            {"</div>" if pending_loan_list else ""}
            
            {"<div class='section'><h3>Apply for Loan</h3><div class='loan-form'><form method='post' action='/apply_loan'><input type='number' name='amount' placeholder='Loan Amount' required><input type='text' name='purpose' placeholder='Purpose' required><input type='number' name='term_months' placeholder='Term (months)' value='12'><input type='number' name='interest_rate' placeholder='Interest Rate (%)' value='15' step='0.1'><button type='submit'>Submit Application</button></form></div></div>" if user.role == 'client' else ""}
            
        </div>
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
    
    flash('Loan application submitted successfully!')
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
    
    flash(f'Loan {decision} successfully!')
    return redirect(url_for('dashboard'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("🚀 Starting Complete Professional Microfinance Platform...")
    print("🌐 Access at: http://127.0.0.1:5000")
    print("✅ Features: Complete Banking System, MySQL Database, Professional UI")
    print("💼 Production-Ready Microfinance Banking System")
    app.run(host='127.0.0.1', port=5000, debug=False)
