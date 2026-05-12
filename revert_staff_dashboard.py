# revert_staff_dashboard.py
content = '''<!DOCTYPE html>
<html>
<head>
    <title>Staff Dashboard - Orethan Microfinance</title>
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
        .sidebar-nav a {color:white;text-decoration:none;display:block;padding:12px 15px;margin:5px 0;border-radius:8px;transition:all 0.3s}
        .sidebar-nav a:hover {background:#2c5aa6;transform:translateX(5px)}
        .sidebar-nav .nav-header {font-size:12px;color:#888;margin-top:20px;margin-bottom:10px;padding-left:10px}
        .sidebar-nav hr {margin:15px 0;border-color:#333}
        .main-content {margin-left:280px;flex:1;padding:20px;min-height:100vh}
        .header {background:#2c5aa6;color:white;padding:20px;border-radius:10px;margin-bottom:20px}
        .header-content {display:flex;justify-content:space-between;align-items:center}
        .stats-grid {display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin-bottom:30px}
        .stat-card {background:white;padding:20px;border-radius:10px;text-align:center;box-shadow:0 2px 5px rgba(0,0,0,0.1)}
        .stat-number {font-size:36px;font-weight:bold;color:#2c5aa6}
        .section {background:white;border-radius:10px;padding:20px;margin-bottom:30px;box-shadow:0 2px 5px rgba(0,0,0,0.1)}
        .section-title {font-size:20px;margin-bottom:20px;border-bottom:2px solid #2c5aa6;padding-bottom:10px}
        .loan-card {border:1px solid #ddd;border-radius:8px;padding:15px;margin-bottom:15px}
        .loan-header {display:flex;justify-content:space-between;margin-bottom:10px}
        .loan-amount {font-size:18px;font-weight:bold;color:#28a745}
        .stage-badge {padding:3px 10px;border-radius:15px;font-size:12px;background:#fff3cd;color:#856404}
        .loan-details {display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:10px 0;font-size:14px}
        .btn-approve {background:#28a745;color:white;padding:8px 20px;border:none;border-radius:5px;cursor:pointer}
        .btn-reject {background:#dc3545;color:white;padding:8px 20px;border:none;border-radius:5px;cursor:pointer}
        .logout-btn {background:rgba(255,255,255,0.2);color:white;padding:5px 15px;border-radius:5px;text-decoration:none}
        .alert {padding:12px;border-radius:8px;margin-bottom:20px}
        .alert-success {background:#d4edda;color:#155724}
        .alert-danger {background:#f8d7da;color:#721c24}
    </style>
</head>
<body>
    <div class="app-container">
        <div class="sidebar">
            <div class="sidebar-header"><h3>🏦 ORETHAN</h3><p>Staff Portal</p></div>
            <div class="sidebar-nav">
                <a href="/staff_dashboard">📊 Dashboard</a>
                <hr>
                <a href="/dashboard">🔙 Main Portal</a>
                <a href="/logout">🚪 Logout</a>
            </div>
        </div>
        <div class="main-content">
            <div class="header">
                <div class="header-content">
                    <div><h1>Staff Dashboard</h1><p>Welcome, {{ user.full_name or user.username }} ({{ user.role|replace('_', ' ')|title }})</p></div>
                    <a href="/logout" class="logout-btn">Logout</a>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card"><div class="stat-number">{{ total_clients }}</div><div>Total Clients</div></div>
                <div class="stat-card"><div class="stat-number">{{ total_loans }}</div><div>Total Loans</div></div>
                <div class="stat-card"><div class="stat-number">{{ pending_for_me }}</div><div>Pending My Approval</div></div>
            </div>
            
            <div class="section">
                <h3 class="section-title">📋 Pending Loan Approvals</h3>
                {% if pending_loans %}
                    {% for loan in pending_loans %}
                    <div class="loan-card">
                        <div class="loan-header">
                            <span class="loan-amount">Tsh {{ "%.2f"|format(loan.amount) }}</span>
                            <span class="stage-badge">{{ loan.current_stage|replace('_', ' ')|title }}</span>
                        </div>
                        <div class="loan-details">
                            <div><strong>Client:</strong> {{ loan.client.full_name or loan.client.username if loan.client else 'Unknown' }}</div>
                            <div><strong>Purpose:</strong> {{ loan.purpose }}</div>
                            <div><strong>Term:</strong> {{ loan.term_months }} months</div>
                        </div>
                        <div>
                            <form method="POST" action="/approve_loan/{{ loan.id }}" style="display:inline">
                                <button type="submit" class="btn-approve" onclick="return confirm('Approve this loan?')">✅ Approve</button>
                            </form>
                            <form method="POST" action="/reject_loan/{{ loan.id }}" style="display:inline">
                                <button type="submit" class="btn-reject" onclick="return confirm('Reject this loan?')">❌ Reject</button>
                            </form>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <p>No loans pending your approval.</p>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>'''

with open('templates/staff_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Staff dashboard reverted to working version!')
