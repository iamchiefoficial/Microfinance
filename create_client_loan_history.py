# create_client_loan_history.py
content = '''<!DOCTYPE html>
<html>
<head>
    <title>Loan History - {{ client.full_name or client.username }}</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial;background:#f5f5f5;padding:20px}
        .container{max-width:1000px;margin:0 auto;background:white;padding:30px;border-radius:10px}
        h1{color:#2c5aa6}
        .client-info{background:#e8f4fd;padding:15px;border-radius:5px;margin:20px 0}
        table{width:100%;border-collapse:collapse}
        th,td{padding:12px;text-align:left;border-bottom:1px solid #ddd}
        th{background:#2c5aa6;color:white}
        .badge{padding:3px 8px;border-radius:5px;font-size:12px}
        .badge-pending{background:#fff3cd;color:#856404}
        .badge-approved{background:#d4edda;color:#155724}
        .badge-disbursed{background:#17a2b8;color:white}
        .btn-back{background:#6c757d;color:white;padding:8px 15px;text-decoration:none;border-radius:5px;display:inline-block}
    </style>
</head>
<body>
    <div class="container">
        <a href="/staff_dashboard" class="btn-back">← Back to Dashboard</a>
        <h1>📋 Loan History</h1>
        
        <div class="client-info">
            <h3>Client Information</h3>
            <p><strong>Name:</strong> {{ client.full_name or client.username }}</p>
            <p><strong>Email:</strong> {{ client.email or 'N/A' }}</p>
            <p><strong>Phone:</strong> {{ client.phone or 'N/A' }}</p>
            <p><strong>Registered:</strong> {{ client.created_at.strftime('%Y-%m-%d') if client.created_at else 'N/A' }}</p>
        </div>
        
        <h3>Loan Applications</h3>
        <table>
            <thead>
                <tr><th>Loan ID</th><th>Amount</th><th>Purpose</th><th>Status</th><th>Stage</th><th>Date</th></tr>
            </thead>
            <tbody>
                {% for loan in loans %}
                <tr>
                    <td>#{{ loan.id }}</td>
                    <td>Tsh {{ "%.2f"|format(loan.amount) }}</td>
                    <td>{{ loan.purpose }}</td>
                    <td><span class="badge badge-{{ loan.status }}">{{ loan.status|upper }}</span></td>
                    <td>{{ loan.current_stage|replace('_', ' ')|title }}</td>
                    <td>{{ loan.created_at.strftime('%Y-%m-%d') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>'''
with open('templates/client_loan_history.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Client loan history template created!')
