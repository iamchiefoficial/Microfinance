# Ultra-simple Flask app - no database, no complexity
from flask import Flask, request, render_template_string, redirect, url_for, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'simple_key_12345'

# In-memory user storage (no database)
users = {}

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Microfinance Platform</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px; background: #f0f0f0;">
    <div style="max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h1>🏦 Microfinance Platform</h1>
        <h2>Welcome!</h2>
        <p>A simple, working microfinance system</p>
        
        <div style="margin: 20px 0;">
            <a href="/login" style="display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 5px;">Login</a>
            <a href="/register" style="display: inline-block; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; margin: 5px;">Register</a>
        </div>
        
        <div style="margin-top: 30px; padding: 20px; background: #e9ecef; border-radius: 5px;">
            <h3>✅ Features Working:</h3>
            <ul style="text-align: left; max-width: 300px; margin: auto;">
                <li>Flask web server</li>
                <li>User registration</li>
                <li>Login system</li>
                <li>Session management</li>
                <li>Dashboard</li>
            </ul>
        </div>
    </div>
</body>
</html>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        
        return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Login Failed</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px;">
    <h1>Login Failed</h1>
    <p>Invalid username or password</p>
    <a href="/login">Try Again</a>
</body>
</html>
        ''')
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Login - Microfinance</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px; background: #f0f0f0;">
    <div style="max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h1>Login</h1>
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
        
        if username in users:
            return "Username already exists!"
        
        users[username] = {
            'password': password,
            'full_name': full_name,
            'role': 'client'
        }
        
        return redirect(url_for('login'))
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Register - Microfinance</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px; background: #f0f0f0;">
    <div style="max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h1>Create Account</h1>
        <form method="post">
            <input type="text" name="full_name" placeholder="Full Name" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"><br>
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
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']
    user_info = users[username]
    
    return render_template_string(f'''
<!DOCTYPE html>
<html>
<head><title>Dashboard - Microfinance</title></head>
<body style="font-family: Arial; padding: 50px; background: #f0f0f0;">
    <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h1>🏦 Dashboard</h1>
        <h2>Welcome, {user_info['full_name']}!</h2>
        <p><strong>Username:</strong> {username}</p>
        <p><strong>Role:</strong> {user_info['role']}</p>
        
        <div style="margin-top: 30px; padding: 20px; background: #d4edda; border-radius: 5px;">
            <h3>✅ System Status: WORKING</h3>
            <ul>
                <li>✅ User authentication</li>
                <li>✅ Session management</li>
                <li>✅ Registration system</li>
                <li>✅ Dashboard display</li>
            </ul>
        </div>
        
        <form method="post" action="/logout" style="margin-top: 30px;">
            <button type="submit" style="padding: 10px 20px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer;">Logout</button>
        </form>
    </div>
</body>
</html>
    ''')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🚀 Starting Simple Microfinance Platform...")
    print("🌐 Access at: http://127.0.0.1:5000")
    print("✅ No database required - uses memory storage")
    app.run(host='127.0.0.1', port=5000, debug=True)
