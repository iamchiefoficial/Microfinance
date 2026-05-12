# remove_admin_confirmations.py
with open('templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove confirm popups
content = content.replace('onclick="return confirm(\'Approve this loan?\')"', '')
content = content.replace('onclick="return confirm(\'Reject this loan?\')"', '')
content = content.replace('onclick="return confirm', '')

with open('templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Confirmation popups removed from admin dashboard!')
