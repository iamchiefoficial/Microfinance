# create_admin_dashboard.py
content = '''<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard - Orethan Microfinance</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial;background:#f5f5f5}
        .header{background:#2c5aa6;color:white;padding:20px}
        .header-content{max-width:1400px;margin:0 auto;display:flex;justify-content:space-between}
        .sidebar{width:250px;background:#343a40;color:white;position:fixed;height:100%;padding:20px}
        .sidebar a{color:white;text-decoration:none;display:block;padding:10px;margin:5px 0;border-radius:5px}
        .sidebar a:hover{background:#2c5aa6}
        .main{margin-left:250px;padding:20px}
        .stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin-bottom:30px}
        .stat-card{background:white;padding:20px;border-radius:10px;text-align:center;box-shadow:0 2px 5px rgba(0,0,0,0.1)}
        .stat-number{font-size:36px;font-weight:bold;color:#2c5aa6}
        .section{background:white;border-radius:10px;padding:20px;margin-bottom:30px;box-shadow:0 2px 5px rgba(0,0,0,0.1)}
        .section-title{font-size:20px;margin-bottom:20px;border-bottom:2px solid #2c5aa6;padding-bottom:10px}
        table{width:100%;border-collapse:collapse}
        th,td{padding:10px;text-align:left;border-bottom:1px solid #ddd}
        th{background:#f8f9fa}
        .badge{padding:3px 8px;border-radius:5px;font-size:12px}
        .badge-pending{background:#fff3cd;color:#856404}
        .badge-approved{background:#d4edda;color:#155724}
        .badge-rejected{background:#f8d7da;color:#721c24}
        .btn{background:#2c5aa6;color:white;padding:5px 10px;border:none;border-radius:3px;cursor:pointer}
        .btn-danger{background:#dc3545}
        .btn-success{background:#28a745}
        .logout-btn{background:rgba(255,255,255,0.2);color:white;padding:5px 15px;border-radius:5px;text-decoration:none}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div><h1>🏦 ORETHAN MICROFINANCE</h1><p>Admin Portal</p></div>
            <div><div>Welcome, {{ user.full_name or user.username }} (Admin)</div><a href="/logout" class="logout-btn">Logout</a></div>
        </div>
    </div>
    <div class="sidebar">
        <h3>Menu</h3>
        <a href="/admin_dashboard">📊 Dashboard</a>
        <a href="/admin/users">👥 Manage Users</a>
        <a href="/admin/loans">💰 Manage Loans</a>
        <a href="/dashboard">🔙 Back to Main</a>
    </div>
    <div class="main">
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
                <tr><th>Stage</th><th>Count</th></tr>
                <tr><td>Loan Officer</td><td>{{ loans_by_stage.loan_officer }}</td></tr>
                <tr><td>Loan Manager</td><td>{{ loans_by_stage.loan_manager }}</td></tr>
                <tr><td>Managing Director</td><td>{{ loans_by_stage.managing_director }}</td></tr>
                <tr><td>General Director</td><td>{{ loans_by_stage.general_director }}</td></tr>
                <tr><td>Completed</td><td>{{ loans_by_stage.completed }}</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h3 class="section-title">🕐 Recent Loan Applications</h3>
            <table>
                <tr><th>ID</th><th>Client</th><th>Amount</th><th>Status</th><th>Stage</th><th>Date</th></tr>
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
            </table>
        </div>
        
        <div class="section">
            <h3 class="section-title">👤 Recent User Registrations</h3>
            <table>
                <tr><th>Username</th><th>Role</th><th>Registered</th></tr>
                {% for u in recent_users %}
                <tr>
                    <td>{{ u.username }}</td>
                    <td>{{ u.role|title }}</td>
                    <td>{{ u.created_at.strftime('%Y-%m-%d') if u.created_at else 'N/A' }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </div>
</body>
</html>'''

with open('templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Admin dashboard created!')
