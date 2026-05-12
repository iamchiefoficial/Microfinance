# create_admin_users.py
content = '''<!DOCTYPE html>
<html>
<head>
    <title>Manage Users - Orethan Microfinance</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial;background:#f5f5f5}
        .header{background:#2c5aa6;color:white;padding:20px}
        .header-content{max-width:1400px;margin:0 auto;display:flex;justify-content:space-between}
        .sidebar{width:250px;background:#343a40;color:white;position:fixed;height:100%;padding:20px}
        .sidebar a{color:white;text-decoration:none;display:block;padding:10px;margin:5px 0;border-radius:5px}
        .sidebar a:hover{background:#2c5aa6}
        .main{margin-left:250px;padding:20px}
        .section{background:white;border-radius:10px;padding:20px;margin-bottom:30px;box-shadow:0 2px 5px rgba(0,0,0,0.1)}
        .section-title{font-size:20px;margin-bottom:20px;border-bottom:2px solid #2c5aa6;padding-bottom:10px}
        table{width:100%;border-collapse:collapse}
        th,td{padding:12px;text-align:left;border-bottom:1px solid #ddd}
        th{background:#f8f9fa}
        .badge{padding:3px 8px;border-radius:5px;font-size:12px}
        .badge-admin{background:#dc3545;color:white}
        .badge-client{background:#28a745;color:white}
        .badge-staff{background:#17a2b8;color:white}
        .btn{background:#dc3545;color:white;padding:5px 10px;border:none;border-radius:3px;cursor:pointer}
        .btn:hover{opacity:0.8}
        .logout-btn{background:rgba(255,255,255,0.2);color:white;padding:5px 15px;border-radius:5px;text-decoration:none}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div><h1>🏦 ORETHAN MICROFINANCE</h1><p>Admin Portal - Manage Users</p></div>
            <div><div>Welcome, Admin</div><a href="/logout" class="logout-btn">Logout</a></div>
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
        <div class="section">
            <h3 class="section-title">👥 All System Users</h3>
            <table>
                <thead>
                    <tr><th>ID</th><th>Username</th><th>Full Name</th><th>Email</th><th>Phone</th><th>Role</th><th>Registered</th><th>Action</th></tr>
                </thead>
                <tbody>
                    {% for user in users %}
                    <tr>
                        <td>{{ user.id }}</td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.full_name or 'N/A' }}</td>
                        <td>{{ user.email or 'N/A' }}</td>
                        <td>{{ user.phone or 'N/A' }}</td>
                        <td><span class="badge badge-{{ user.role }}">{{ user.role|upper }}</span></td>
                        <td>{{ user.created_at.strftime('%Y-%m-%d') if user.created_at else 'N/A' }}</td>
                        <td>
                            {% if user.role != 'admin' %}
                            <form method="POST" action="/admin/delete_user/{{ user.id }}" onsubmit="return confirm('Delete this user?')">
                                <button type="submit" class="btn">Delete</button>
                            </form>
                            {% else %}
                            <span style="color:#999;">Protected</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>'''

with open('templates/admin_users.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ admin_users.html created!')
