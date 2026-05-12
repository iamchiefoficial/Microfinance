# Microfinance Platform with MySQL Database
from flask import Flask, request, render_template_string, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'microfinance_platform_2025_secure_key'

# MySQL Database Configuration
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

# Create database tables
with app.app_context():
    try:
        db.create_all()
        print("✅ MySQL database tables created successfully!")
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("💡 Make sure MySQL is running and database 'microfinance_db' exists")

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
<body style="font-family: Arial; text-align: center; padding: 50px; background: #f0f0f0;">
    <div style="max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h1>🏦 Microfinance Platform</h1>
        <h2>Login</h2>
        <form method="post">
            <input type="text" name="username" placeholder="Username" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="password" name="password" placeholder="Password" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <button type="submit" style="width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;">Login</button>
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
        
        if User.query.filter_by(username=username).first():
            return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Registration Failed</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px;">
    <div style="max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h1>Registration Failed</h1>
        <p>Username already exists!</p>
        <a href="/register" style="display: inline-block; padding: 10px 20px; background: #dc3545; color: white; text-decoration: none; border-radius: 5px;">Try Again</a>
    </div>
</body>
</html>
            ''')
        
        if User.query.filter_by(email=email).first():
            return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Registration Failed</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px;">
    <div style="max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h1>Registration Failed</h1>
        <p>Email already registered!</p>
        <a href="/register" style="display: inline-block; padding: 10px 20px; background: #dc3545; color: white; text-decoration: none; border-radius: 5px;">Try Again</a>
    </div>
</body>
</html>
            ''')
        
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            email=email,
            role='client'
        )
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Register - Microfinance Platform</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px; background: #f0f0f0;">
    <div style="max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h1>🏦 Microfinance Platform</h1>
        <h2>Create Account</h2>
        <form method="post">
            <input type="text" name="full_name" placeholder="Full Name" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="email" name="email" placeholder="Email" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
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
    
    # Get user's loans if client
    user_loans = []
    if user.role == 'client':
        user_loans = Loan.query.filter_by(client_id=user.id).order_by(Loan.created_at.desc()).limit(5).all()
    
    return render_template_string(f'''
<!DOCTYPE html>
<html>
<head><title>Dashboard - Microfinance Platform</title></head>
<body style="font-family: Arial; padding: 50px; background: #f0f0f0;">
    <div style="max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h1>🏦 Microfinance Platform</h1>
        <h2>Welcome, {user.full_name}!</h2>
        <p><strong>Username:</strong> {user.username}</p>
        <p><strong>Role:</strong> {user.role}</p>
        <p><strong>Email:</strong> {user.email}</p>
        
        <div style="margin-top: 30px; padding: 20px; background: #d4edda; border-radius: 5px;">
            <h3>✅ System Status: WORKING WITH MYSQL</h3>
            <ul>
                <li>✅ MySQL Database Connected</li>
                <li>✅ User Authentication</li>
                <li>✅ Session Management</li>
                <li>✅ Registration System</li>
                <li>✅ Dashboard Display</li>
                <li>✅ Data Persistence</li>
            </ul>
        </div>
        
        {"<div style='margin-top: 30px;'><h3>📋 Your Recent Loans:</h3>" if user_loans else ""}
        {"".join([f"<div style='border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 5px;'><strong>Amount:</strong> ${loan.amount:,}<br><strong>Purpose:</strong> {loan.purpose}<br><strong>Status:</strong> {loan.status}<br><strong>Date:</strong> {loan.created_at.strftime('%Y-%m-%d')}</div>" for loan in user_loans]) if user_loans else ""}
        {"</div>" if user_loans else ""}
        
        {"<div style='margin-top: 30px;'><form method='post' action='/apply_loan'><h3>💰 Apply for Loan:</h3><input type='number' name='amount' placeholder='Amount' required style='width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;'><br><input type='text' name='purpose' placeholder='Purpose' required style='width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;'><br><button type='submit' style='padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;'>Apply</button></form></div>" if user.role == 'client' else ""}
        
        <form method="post" action="/logout" style="margin-top: 30px;">
            <button type="submit" style="padding: 10px 20px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer;">Logout</button>
        </form>
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

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("🚀 Starting Microfinance Platform with MySQL...")
    print("🌐 Access at: http://127.0.0.1:5000")
    print("✅ Features: MySQL Database, Registration, Login, Dashboard, Loans")
    print("💾 Data persists between sessions!")
    app.run(host='127.0.0.1', port=5000, debug=False)
