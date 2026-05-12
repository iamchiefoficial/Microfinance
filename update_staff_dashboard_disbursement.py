# update_staff_dashboard_disbursement.py
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
        table {width:100%;border-collapse:collapse}
        th,td {padding:12px;text-align:left;border-bottom:1px solid #ddd}
        th {background:#f8f9fa}
        .badge {padding:3px 8px;border-radius:5px;font-size:12px}
        .badge-pending {background:#fff3cd;color:#856404}
        .badge-approved {background:#d4edda;color:#155724}
        .badge-disbursed {background:#17a2b8;color:white}
        .badge-completed {background:#28a745;color:white}
        .btn {background:#2c5aa6;color:white;padding:5px 10px;border:none;border-radius:3px;cursor:pointer;margin:2px;text-decoration:none;display:inline-block}
        .btn-success {background:#28a745}
        .btn-danger {background:#dc3545}
        .btn-warning {background:#fd7e14}
        .btn-info {background:#17a2b8}
        .logout-btn {background:rgba(255,255,255,0.2);color:white;padding:5px 15px;border-radius:5px;text-decoration:none}
        .alert {padding:12px;border-radius:8px;margin-bottom:20px}
        .alert-success {background:#d4edda;color:#155724}
        .alert-danger {background:#f8d7da;color:#721c24}
        .alert-warning {background:#fff3cd;color:#856404}
    </style>
</head>
<body>
    <div class="app-container">
        <div class="sidebar">
            <div class="sidebar-header"><h3>🏦 ORETHAN</h3><p style="font-size:12px;color:#888">Staff Portal</p></div>
            <div class="sidebar-nav">
                <div class="nav-header">MAIN NAVIGATION</div>
                <a href="/staff_dashboard">📊 Dashboard</a>
                <hr>
                <div class="nav-header">SYSTEM</div>
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
            
            <!-- Pending Approval Section -->
            <div class="section">
                <h3 class="section-title">📋 Pending Approval</h3>
                {% if pending_loans %}
                <table>
                    <thead><tr><th>ID</th><th>Client</th><th>Amount</th><th>Purpose</th><th>Current Stage</th><th>Actions</th></tr></thead>
                    <tbody>
                        {% for loan in pending_loans %}
                        <tr>
                            <td>{{ loan.id }}</td>
                            <td>{{ loan.client.full_name or loan.client.username if loan.client else 'Unknown' }}</td>
                            <td>Tsh {{ "%.2f"|format(loan.amount) }}</td>
                            <td>{{ loan.purpose }}</td>
                            <td><span class="badge badge-pending">{{ loan.current_stage|replace('_', ' ')|title }}</span></td>
                            <td>
                                <form method="POST" action="/approve_loan/{{ loan.id }}" style="display:inline">
                                    <button type="submit" class="btn btn-success" onclick="return confirm('Approve this loan?')">✓ Approve</button>
                                </form>
                                <form method="POST" action="/reject_loan/{{ loan.id }}" style="display:inline">
                                    <button type="submit" class="btn btn-danger" onclick="return confirm('Reject this loan?')">✗ Reject</button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p>No loans pending your approval.</p>
                {% endif %}
            </div>
            
            <!-- Approved Loans Ready for Disbursement -->
            <div class="section">
                <h3 class="section-title">💰 Approved Loans - Ready for Disbursement</h3>
                {% if approved_loans %}
                <table>
                    <thead><tr><th>ID</th><th>Client</th><th>Amount</th><th>Purpose</th><th>Approved By</th><th>Actions</th></tr></thead>
                    <tbody>
                        {% for loan in approved_loans %}
                        <tr>
                            <td>{{ loan.id }}</td>
                            <td>{{ loan.client.full_name or loan.client.username if loan.client else 'Unknown' }}</td>
                            <td>Tsh {{ "%.2f"|format(loan.amount) }}</td>
                            <td>{{ loan.purpose }}</td>
                            <td>General Director</td>
                            <td>
                                <a href="/disburse_loan/{{ loan.id }}" class="btn btn-info">💰 Disburse Loan</a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p>No approved loans ready for disbursement.</p>
                {% endif %}
            </div>
            
            <!-- Disbursed Loans -->
            <div class="section">
                <h3 class="section-title">✅ Disbursed Loans</h3>
                {% if disbursed_loans %}
                <table>
                    <thead><tr><th>ID</th><th>Client</th><th>Amount</th><th>Disbursement Method</th><th>Date</th><th>Status</th></tr></thead>
                    <tbody>
                        {% for loan in disbursed_loans %}
                        <tr>
                            <td>{{ loan.id }}</td>
                            <td>{{ loan.client.full_name or loan.client.username if loan.client else 'Unknown' }}</td>
                            <td>Tsh {{ "%.2f"|format(loan.amount) }}</td>
                            <td>{{ loan.disbursement_method if loan.disbursement_method else 'Not specified' }}</td>
                            <td>{{ loan.disbursement_date.strftime('%Y-%m-%d') if loan.disbursement_date else 'Pending' }}</td>
                            <td><span class="badge badge-disbursed">Disbursed</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p>No loans disbursed yet.</p>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>'''

with open('templates/staff_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Staff dashboard updated with disbursement section!')
