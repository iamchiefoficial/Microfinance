# fix_admin_loans_full.py
content = '''<!DOCTYPE html>
<html>
<head>
    <title>Manage Loans - Orethan Microfinance</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial;background:#f5f5f5;min-height:100vh}
        .app-container {display:flex;min-height:100vh}
        .sidebar {
            width:280px;
            background:#1a1a2e;
            color:white;
            position:fixed;
            top:0;
            left:0;
            height:100vh;
            overflow-y:auto;
            z-index:100;
        }
        .sidebar-header {padding:20px;text-align:center;border-bottom:1px solid #333;margin-bottom:20px}
        .sidebar-header h3 {color:#2c5aa6}
        .sidebar-nav {padding:0 15px}
        .sidebar-nav a {color:white;text-decoration:none;display:block;padding:12px 15px;margin:5px 0;border-radius:8px}
        .sidebar-nav a:hover {background:#2c5aa6;transform:translateX(5px)}
        .sidebar-nav .nav-header {font-size:12px;color:#888;margin-top:20px;margin-bottom:10px;padding-left:10px}
        .sidebar-nav hr {margin:15px 0;border-color:#333}
        .main-content {margin-left:280px;flex:1;padding:20px;min-height:100vh}
        .header {background:#2c5aa6;color:white;padding:20px;border-radius:10px;margin-bottom:20px}
        .header-content {display:flex;justify-content:space-between;align-items:center}
        .section {background:white;border-radius:10px;padding:20px;box-shadow:0 2px 5px rgba(0,0,0,0.1)}
        .section-title {font-size:20px;margin-bottom:20px;border-bottom:2px solid #2c5aa6;padding-bottom:10px}
        table {width:100%;border-collapse:collapse}
        th,td {padding:12px;text-align:left;border-bottom:1px solid #ddd}
        th {background:#f8f9fa}
        .badge {padding:3px 8px;border-radius:5px;font-size:12px}
        .badge-pending {background:#fff3cd;color:#856404}
        .badge-approved {background:#d4edda;color:#155724}
        .badge-rejected {background:#f8d7da;color:#721c24}
        .btn {background:#2c5aa6;color:white;padding:5px 10px;border:none;border-radius:3px;cursor:pointer;margin:2px}
        .btn-success {background:#28a745}
        .btn-danger {background:#dc3545}
        .logout-btn {background:rgba(255,255,255,0.2);color:white;padding:5px 15px;border-radius:5px;text-decoration:none}
    </style>
</head>
<body>
    <div class="app-container">
        <div class="sidebar">
            <div class="sidebar-header"><h3>🏦 ORETHAN</h3><p style="font-size:12px;color:#888">Admin Portal</p></div>
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
        <div class="main-content">
            <div class="header">
                <div class="header-content">
                    <div><h1>Manage Loans</h1><p>View and manage all loan applications</p></div>
                    <a href="/logout" class="logout-btn">Logout</a>
                </div>
            </div>
            <div class="section">
                <h3 class="section-title">💰 All Loan Applications</h3>
                <table>
                    <thead><tr><th>ID</th><th>Client</th><th>Amount (Tsh)</th><th>Purpose</th><th>Status</th><th>Stage</th><th>Date</th><th>Actions</th></tr></thead>
                    <tbody>
                        {% for loan in loans %}
                        <tr>
                            <td>{{ loan.id }}</td>
                            <td>{{ loan.client.full_name or loan.client.username if loan.client else 'Unknown' }}</td>
                            <td>{{ "%.2f"|format(loan.amount) }}</td>
                            <td>{{ loan.purpose }}</td>
                            <td><span class="badge badge-{{ loan.status }}">{{ loan.status|upper }}</span></td>
                            <td>{{ loan.current_stage|replace('_', ' ')|title }}</td>
                            <td>{{ loan.created_at.strftime('%Y-%m-%d') if loan.created_at else 'N/A' }}</td>
                            <td>{% if loan.status == 'pending' %}<form method="POST" action="/admin/approve_loan/{{ loan.id }}" style="display:inline"><button type="submit" class="btn btn-success" onclick="return confirm('Approve this loan?')">✓ Approve</button></form><form method="POST" action="/admin/reject_loan/{{ loan.id }}" style="display:inline"><button type="submit" class="btn btn-danger" onclick="return confirm('Reject this loan?')">✗ Reject</button></form>{% else %}<span style="color:#999;">Already {{ loan.status }}</span>{% endif %}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>'''

with open('templates/admin_loans.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ admin_loans.html fixed with full height sidebar!')
