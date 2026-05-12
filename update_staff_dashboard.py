# update_staff_dashboard.py
content = '''<!DOCTYPE html>
<html>
<head>
    <title>Staff Dashboard - Orethan Microfinance</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial;background:#f5f5f5}
        .header{background:#2c5aa6;color:white;padding:20px}
        .header-content{max-width:1200px;margin:0 auto;display:flex;justify-content:space-between}
        .container{max-width:1200px;margin:30px auto;padding:0 20px}
        .stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:30px}
        .stat-card{background:white;padding:20px;border-radius:10px;text-align:center}
        .stat-number{font-size:36px;font-weight:bold;color:#2c5aa6}
        .section{background:white;border-radius:10px;padding:20px;margin-bottom:30px}
        .section-title{font-size:20px;margin-bottom:20px;border-bottom:2px solid #2c5aa6;padding-bottom:10px}
        .loan-card{border:1px solid #ddd;border-radius:8px;padding:15px;margin-bottom:15px;background:#fafafa}
        .loan-header{display:flex;justify-content:space-between;margin-bottom:10px}
        .loan-amount{font-size:20px;font-weight:bold;color:#28a745}
        .stage-badge{padding:3px 10px;border-radius:15px;font-size:12px;background:#fff3cd;color:#856404}
        .loan-details{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:10px 0;font-size:14px}
        .loan-actions{margin-top:15px;display:flex;gap:10px}
        .btn-approve{background:#28a745;color:white;padding:8px 20px;border:none;border-radius:5px;cursor:pointer}
        .btn-reject{background:#dc3545;color:white;padding:8px 20px;border:none;border-radius:5px;cursor:pointer}
        .logout-btn{background:rgba(255,255,255,0.2);color:white;padding:5px 15px;border-radius:5px;text-decoration:none}
        .alert{padding:12px;border-radius:8px;margin-bottom:20px}
        .alert-success{background:#d4edda;color:#155724}
        .alert-danger{background:#f8d7da;color:#721c24}
        .alert-warning{background:#fff3cd;color:#856404}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div><h1>🏦 ORETHAN MICROFINANCE</h1><p>Staff Portal</p></div>
            <div><div>Welcome, {{ user.full_name or user.username }}</div><div>{{ user.role|replace('_', ' ')|title }}</div><a href="/logout" class="logout-btn">Logout</a></div>
        </div>
    </div>
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-number">{{ total_clients }}</div><div>Total Clients</div></div>
            <div class="stat-card"><div class="stat-number">{{ total_loans }}</div><div>Total Loans</div></div>
            <div class="stat-card"><div class="stat-number">{{ pending_for_me }}</div><div>Pending My Approval</div></div>
        </div>
        
        <div class="section">
            <h3 class="section-title">📋 Loans Pending Your Review</h3>
            {% if pending_loans %}
                {% for loan in pending_loans %}
                    <div class="loan-card">
                        <div class="loan-header">
                            <span class="loan-amount">Tsh {{ "%.2f"|format(loan.amount) }}</span>
                            <span class="stage-badge">Stage: {{ loan.get_current_stage_name() if loan.get_current_stage_name else loan.current_stage|replace('_', ' ')|title }}</span>
                        </div>
                        <div class="loan-details">
                            <div><strong>Client:</strong> {{ loan.client.full_name or loan.client.username if loan.client else 'Unknown' }}</div>
                            <div><strong>Purpose:</strong> {{ loan.purpose }}</div>
                            <div><strong>Term:</strong> {{ loan.term_months }} months</div>
                            <div><strong>Applied:</strong> {{ loan.created_at.strftime('%Y-%m-%d') if loan.created_at else 'N/A' }}</div>
                        </div>
                        <div class="loan-actions">
                            <form method="POST" action="/approve_loan/{{ loan.id }}" style="display:inline" onsubmit="return confirm('Approve this loan?')">
                                <button type="submit" class="btn-approve">✅ Approve</button>
                            </form>
                            <form method="POST" action="/reject_loan/{{ loan.id }}" style="display:inline" onsubmit="return confirm('Reject this loan?')">
                                <button type="submit" class="btn-reject">❌ Reject</button>
                            </form>
                        </div>
                    </div>
                {% endfor %}
            {% else %}
                <p>No loans pending your review.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>'''

with open('templates/staff_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Staff dashboard updated successfully!')
