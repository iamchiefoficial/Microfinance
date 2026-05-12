# remove_admin_users_confirmations.py
with open('templates/admin_users.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove confirm popup from delete user
content = content.replace('onclick="return confirm(\'Delete this user?\')"', '')

with open('templates/admin_users.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Confirmation popups removed from admin users page!')
