# fix_admin_users.py
with open('templates/admin_users.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the sidebar link
content = content.replace('/dashboard', '/admin_dashboard')
content = content.replace('Back to Main', 'Admin Dashboard')

with open('templates/admin_users.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ admin_users.html sidebar fixed!')
