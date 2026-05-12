# remove_admin_loans_confirmations.py
with open('templates/admin_loans.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove confirm popups
content = content.replace('onclick="return confirm(\'Approve this loan?\')"', '')
content = content.replace('onclick="return confirm(\'Reject this loan?\')"', '')

with open('templates/admin_loans.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Confirmation popups removed from admin loans page!')
