# Ultra-Simple Working Microfinance Platform
from flask import Flask, request, render_template_string, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'microfinance_key_12345'

# In-memory storage (no database needed)
users = {}
loans = {}
loan_id_counter = 1
user_id_counter = 1

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
        
        if username in users and check_password_hash(users[username]['password'], password):
            session['user_id'] = users[username]['id']
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('dashboard'))
        
        return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Login Failed</title></head>
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
    global user_id_counter
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        occupation = request.form.get('occupation')
        monthly_income = request.form.get('monthly_income')
        
        if username in users:
            return "Username already exists!"
        
        users[username] = {
            'id': user_id_counter,
            'password': generate_password_hash(password),
            'full_name': full_name,
            'email': email,
            'occupation': occupation,
            'monthly_income': float(monthly_income),
            'role': 'client'
        }
        user_id_counter += 1
        
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
            <input type="text" name="occupation" placeholder="Occupation" required style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
            <input type="number" name="monthly_income" placeholder="Monthly Income" required style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
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
    
    username = session['username']
    user = users[username]
    
    # Calculate statistics
    total_clients = len([u for u in users.values() if u['role'] == 'client'])
    total_loans = len(loans)
    pending_loans = len([l for l in loans.values() if l['status'] == 'pending'])
    approved_loans = len([l for l in loans.values() if l['status'] == 'approved'])
    
    # Get recent clients
    recent_clients = [u for u in users.values() if u['role'] == 'client'][-5:]
    
    # Get user's loans
    user_loans = [l for l in loans.values() if l['client_id'] == user['id']]
    
    return render_template_string(f'''
<!DOCTYPE html>
<html>
<head><title>Dashboard - Microfinance Platform</title></head>
<body style="font-family: Arial; padding: 20px; background: #f5f5f5; min-height: 100vh;">
    <div style="max-width: 1200px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <!-- Header -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 2px solid #e0e0e0; padding-bottom: 20px;">
            <div>
                <h1 style="color: #1e3e38; margin: 0;">🏦 Microfinance Platform</h1>
                <h2 style="color: #5e8b80; margin: 5px 0;">Welcome, {user['full_name']}!</h2>
                <p style="margin: 5px 0;"><strong>Role:</strong> {user['role'].title()}</p>
                <p style="margin: 5px 0;"><strong>Email:</strong> {user['email']}</p>
            </div>
            <form method="post" action="/logout" style="margin: 0;">
                <button type="submit" style="padding: 10px 20px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer;">Logout</button>
            </form>
        </div>
        
        <!-- Statistics Cards -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px;">
            <div style="background: #667eea; color: white; padding: 25px; border-radius: 10px;">
                <h3 style="margin: 0; font-size: 16px;">Total Clients</h3>
                <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">{total_clients}</p>
                <p style="margin: 0; font-size: 14px;">Active borrowers</p>
            </div>
            <div style="background: #f093fb; color: white; padding: 25px; border-radius: 10px;">
                <h3 style="margin: 0; font-size: 16px;">Total Loans</h3>
                <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">{total_loans}</p>
                <p style="margin: 0; font-size: 14px;">All applications</p>
            </div>
            <div style="background: #4facfe; color: white; padding: 25px; border-radius: 10px;">
                <h3 style="margin: 0; font-size: 16px;">Pending Loans</h3>
                <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">{pending_loans}</p>
                <p style="margin: 0; font-size: 14px;">Awaiting approval</p>
            </div>
            <div style="background: #43e97b; color: white; padding: 25px; border-radius: 10px;">
                <h3 style="margin: 0; font-size: 16px;">Approved Loans</h3>
                <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">{approved_loans}</p>
                <p style="margin: 0; font-size: 14px;">Active loans</p>
            </div>
        </div>
        
        <!-- Recent Clients -->
        <div style="margin-bottom: 30px;">
            <h3 style="color: #1e3e38; margin-bottom: 20px;">Recent Clients</h3>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
                {"".join([f"<div style='padding: 10px; border-bottom: 1px solid #e0e0e0;'><strong>{client['full_name']}</strong> - {client['occupation']} - Income: ${client['monthly_income']:,.0f}</div>" for client in recent_clients]) if recent_clients else "<p style='color: #666; text-align: center;'>No clients registered yet</p>"}
            </div>
        </div>
        
        <!-- Your Loans -->
        {"<div style='margin-bottom: 30px;'><h3 style='color: #1e3e38;'>Your Loans</h3>" if user_loans else ""}
        {"".join([f"<div style='background: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 8px;'><strong>Amount:</strong> ${loan['amount']:,.0f}<br><strong>Purpose:</strong> {loan['purpose']}<br><strong>Status:</strong> {loan['status']}<br><strong>Applied:</strong> {loan['created_at']}</div>" for loan in user_loans]) if user_loans else ""}
        {"</div>" if user_loans else ""}
        
        <!-- Client Loan Application -->
        {"<div style='margin-bottom: 30px;'><h3 style='color: #1e3e38;'>Apply for Loan</h3><form method='post' action='/apply_loan'><input type='number' name='amount' placeholder='Loan Amount' required style='width: 200px; padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 5px;'><input type='text' name='purpose' placeholder='Purpose' required style='width: 300px; padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 5px;'><button type='submit' style='padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;'>Apply</button></form></div>" if user['role'] == 'client' else ""}
        
    </div>
</body>
</html>
    ''')

@app.route('/apply_loan', methods=['POST'])
def apply_loan():
    global loan_id_counter
    
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user = users[username]
    
    if user['role'] != 'client':
        return redirect(url_for('dashboard'))
    
    amount = request.form.get('amount')
    purpose = request.form.get('purpose')
    
    from datetime import datetime
    loans[loan_id_counter] = {
        'id': loan_id_counter,
        'client_id': user['id'],
        'client_name': user['full_name'],
        'amount': float(amount),
        'purpose': purpose,
        'status': 'pending',
        'created_at': datetime.now().strftime('%Y-%m-%d')
    }
    loan_id_counter += 1
    
    return redirect(url_for('dashboard'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

# Create default staff accounts
def create_staff_accounts():
    global user_id_counter
    staff_accounts = [
        ('System Administrator', 'admin'),
        ('General Director', 'general_director'),
        ('Managing Director', 'managing_director'),
        ('Loan Manager', 'loan_manager'),
        ('Loan Officer', 'loan_officer')
    ]
    
    for name, role in staff_accounts:
        users[name] = {
            'id': user_id_counter,
            'password': generate_password_hash('mf@123'),
            'full_name': name,
            'email': f'{role.lower()}@microfinance.com',
            'occupation': role.replace('_', ' ').title(),
            'monthly_income': 5000.0,
            'role': role
        }
        user_id_counter += 1

# Initialize staff accounts
create_staff_accounts()

if __name__ == '__main__':
    print("🚀 Starting Ultra-Simple Microfinance Platform...")
    print("🌐 Access at: http://127.0.0.1:5000")
    print("✅ Features: No Database Required, Simple & Reliable")
    print("👤 Staff Accounts Created with password: mf@123")
    print("📱 Ready to Use!")
    app.run(host='127.0.0.1', port=5000, debug=False)
