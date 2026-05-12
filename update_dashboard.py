# update_dashboard.py
content = '''<!DOCTYPE html>
<html>
<head>
    <title>Client Dashboard - Orethan Microfinance</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial;background:#f5f5f5}
        .header{background:#2c5aa6;color:white;padding:20px}
        .header-content{max-width:1200px;margin:0 auto;display:flex;justify-content:space-between}
        .container{max-width:1200px;margin:30px auto;padding:0 20px}
        .loan-types{display:flex;gap:30px;justify-content:center;margin-bottom:40px;flex-wrap:wrap}
        .loan-card{background:white;border-radius:10px;padding:30px;text-align:center;width:280px}
        .loan-icon{font-size:60px;margin-bottom:20px}
        .loan-title{font-size:24px;font-weight:bold;margin-bottom:10px}
        .btn-individual{background:#28a745;color:white;padding:12px 30px;border:none;border-radius:5px;cursor:pointer;width:100%}
        .btn-group{background:#17a2b8;color:white;padding:12px 30px;border:none;border-radius:5px;cursor:pointer;width:100%}
        .logout-btn{background:rgba(255,255,255,0.2);color:white;padding:5px 15px;border-radius:5px;text-decoration:none}
        .stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:30px}
        .stat-card{background:white;padding:20px;border-radius:10px;text-align:center}
        .stat-number{font-size:36px;font-weight:bold;color:#2c5aa6}
        .loans-section{background:white;border-radius:10px;padding:20px}
        .loan-item{border:1px solid #ddd;padding:15px;margin-bottom:15px;border-radius:5px}
        .loan-status{padding:3px 10px;border-radius:15px;font-size:12px}
        .status-pending{background:#fff3cd;color:#856404}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div><h1>🏦 ORETHAN MICROFINANCE</h1><p>Client Portal</p></div>
            <div><div>Welcome, {{ user.full_name or user.username }}</div><a href="/logout" class="logout-btn">Logout</a></div>
        </div>
    </div>
    <div class="container">
        <div class="loan-types">
            <div class="loan-card">
                <div class="loan-icon">💰</div>
                <div class="loan-title">Individual Loan</div>
                <button class="btn-individual" onclick="window.location.href='/individual_loan_form'">Apply Now</button>
            </div>
            <div class="loan-card">
                <div class="loan-icon">👥</div>
                <div class="loan-title">Group Loan</div>
                <button class="btn-group" onclick="window.location.href='/group_loan_form_new'">Apply Now</button>
            </div>
        </div>
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-number">{{ total_loans }}</div><div>Total Loans</div></div>
            <div class="stat-card"><div class="stat-number">{{ active_loans }}</div><div>Active Loans</div></div>
            <div class="stat-card"><div class="stat-number">{{ completed_loans }}</div><div>Completed Loans</div></div>
        </div>
        <div class="loans-section">
            <h3>My Loan Applications</h3>
            {% for loan in loans %}<div class="loan-item"><strong>Tsh {{ "%.2f"|format(loan.amount) }}</strong> - <span class="loan-status status-{{ loan.status }}">{{ loan.status|upper }}</span><br>Purpose: {{ loan.purpose }}<br>Applied: {{ loan.created_at.strftime('%Y-%m-%d') }}</div>{% endfor %}
        </div>
    </div>
</body>
</html>'''

with open('templates/client_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Client dashboard updated - Group loan button points to new route')
