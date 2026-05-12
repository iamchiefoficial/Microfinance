# fix_admin_dashboard_full.py
content = '''<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard - Orethan Microfinance</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial;background:#f5f5f5;min-height:100vh}
        
        /* Full height layout */
        .app-container {display:flex;min-height:100vh}
        
        /* Sidebar - full height, fixed, no gaps */
        .sidebar {
            width:280px;
            background:#1a1a2e;
            color:white;
            position:fixed;
            top:0;
            left:0;
            height:100vh;
            overflow-y:auto;
            box-shadow:2px 0 5px rgba(0,0,0,0.1);
            z-index:100;
        }
        
        .sidebar-header {
            padding:20px;
            text-align:center;
            border-bottom:1px solid #333;
            margin-bottom:20px;
        }
        
        .sidebar-header h3 {
            color:#2c5aa6;
            margin-bottom:5px;
        }
        
        .sidebar-nav {
            padding:0 15px;
        }
        
        .sidebar-nav a {
            color:white;
            text-decoration:none;
            display:block;
            padding:12px 15px;
            margin:5px 0;
            border-radius:8px;
            transition:all 0.3s;
        }
        
        .sidebar-nav a:hover {
            background:#2c5aa6;
            transform:translateX(5px);
        }
        
        .sidebar-nav .nav-header {
            font-size:12px;
            color:#888;
            margin-top:20px;
            margin-bottom:10px;
            padding-left:10px;
        }
        
        .sidebar-nav hr {
            margin:15px 0;
            border-color:#333;
        }
        
        /* Main content - offset by sidebar width */
        .main-content {
            margin-left:280px;
            flex:1;
            padding:20px;
            min-height:100vh;
        }
        
        .header {
            background:#2c5aa6;
            color:white;
            padding:20px;
            border-radius:10px;
            margin-bottom:20px;
        }
        
        .stats-grid {
            display:grid;
            grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
            gap:20px;
            margin-bottom:30px
        }
        
        .stat-card {
            background:white;
            padding:20px;
            border-radius:10px;
            text-align:center;
            box-shadow:0 2px 5px rgba(0,0,0,0.1)
        }
        
        .stat-number {
            font-size:36px;
            font-weight:bold;
            color:#2c5aa6
        }
        
        .section {
            background:white;
            border-radius:10px;
            padding:20px;
            margin-bottom:30px;
            box-shadow:0 2px 5px rgba(0,0,0,0.1)
        }
        
        .section-title {
            font-size:20px;
            margin-bottom:20px;
            border-bottom:2px solid #2c5aa6;
            padding-bottom:10px
        }
        
        table {
            width:100%;
            border-collapse:collapse
        }
        
        th,td {
            padding:10px;
            text-align:left;
            border-bottom:1px solid #ddd
        }
        
        th {
            background:#f8f9fa
        }
        
        .badge {
            padding:3px 8px;
            border-radius:5px;
            font-size:12px
        }
        
        .badge-pending {
            background:#fff3cd;
            color:#856404
        }
        
        .badge-approved {
            background:#d4edda;
            color:#155724
        }
        
        .badge-rejected {
            background:#f8d7da;
            color:#721c24
        }
        
        .logout-btn {
            background:rgba(255,255,255,0.2);
            color:white;
            padding:5px 15px;
            border-radius:5px;
            text-decoration:none
        }
        
        .logout-btn:hover {
            background:rgba(255,255,255,0.3)
        }
        
        .header-content {
            display:flex;
            justify-content:space-between;
            align-items:center
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="sidebar-header">
                <h3>🏦 ORETHAN</h3>
                <p style="font-size:12px;color:#888">Microfinance System</p>
            </div>
            <div class="sidebar-nav">
                <div class="nav-header">MAIN NAVIGATION</div>
                <a href="/admin_dashboard">📊 Admin Dashboard</a>
                <a href="/admin/users">👥 Manage Users</a>
                <a href="/admin/loans">💰 Manage Loans</a>
                <hr>
                <div class="nav-header">SYSTEM</div>
                <a href="/dashboard">🔙 Main Portal</a>
                <a href="/logout">🚪 Logout</a>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="main-content">
            <div class="header">
                <div class="header-content">
                    <div>
                        <h1>Admin Dashboard</h1>
                        <p>Welcome, {{ user.full_name or user.username }} (Administrator)</p>
                    </div>
                    <a href="/logout" class="logout-btn">Logout</a>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card"><div class="stat-number">{{ total_users }}</div><div>Total Users</div></div>
                <div class="stat-card"><div class="stat-number">{{ total_clients }}</div><div>Clients</div></div>
                <div class="stat-card"><div class="stat-number">{{ total_staff }}</div><div>Staff</div></div>
                <div class="stat-card"><div class="stat-number">{{ total_loans }}</div><div>Total Loans</div></div>
                <div class="stat-card"><div class="stat-number">{{ pending_loans }}</div><div>Pending</div></div>
                <div class="stat-card"><div class="stat-number">{{ approved_loans }}</div><div>Approved</div></div>
            </div>
            
            <div class="section">
                <h3 class="section-title">📋 Loans by Stage</h3>
                <table>
                    <thead><tr><th>Stage</th><th>Count</th></tr></thead>
                    <tbody>
                        <tr><td>Loan Officer</td><td>{{ loans_by_stage.loan_officer }}</td></tr>
                        <tr><td>Loan Manager</td><td>{{ loans_by_stage.loan_manager }}</td></tr>
                        <tr><td>Managing Director</td><td>{{ loans_by_stage.managing_director }}</td></tr>
                        <tr><td>General Director</td><td>{{ loans_by_stage.general_director }}</td></tr>
                        <tr><td>Completed</td><td>{{ loans_by_stage.completed }}</td></tr>
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h3 class="section-title">🕐 Recent Loan Applications</h3>
                <table>
                    <thead><tr><th>ID</th><th>Client</th><th>Amount</th><th>Status</th><th>Stage</th><th>Date</th></tr></thead>
                    <tbody>
                        {% for loan in recent_loans %}
                        <tr>
                            <td>{{ loan.id }}</td>
                            <td>{{ loan.client.full_name or loan.client.username if loan.client else 'Unknown' }}</td>
                            <td>Tsh {{ "%.2f"|format(loan.amount) }}</td>
                            <td><span class="badge badge-{{ loan.status }}">{{ loan.status|upper }}</span></td>
                            <td>{{ loan.current_stage|replace('_', ' ')|title }}</td>
                            <td>{{ loan.created_at.strftime('%Y-%m-%d') if loan.created_at else 'N/A' }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h3 class="section-title">👤 Recent User Registrations</h3>
                <table>
                    <thead><tr><th>Username</th><th>Role</th><th>Registered</th></tr></thead>
                    <tbody>
                        {% for u in recent_users %}
                        <tr>
                            <td>{{ u.username }}</td>
                            <td>{{ u.role|title }}</td>
                            <td>{{ u.created_at.strftime('%Y-%m-%d') if u.created_at else 'N/A' }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>'''

with open('templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ admin_dashboard.html fixed with full height sidebar!')
