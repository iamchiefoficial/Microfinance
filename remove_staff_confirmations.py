# remove_staff_confirmations.py
with open('templates/staff_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove confirm popup from approve buttons
content = content.replace('onclick="return confirm(\'Approve this loan? Client will be notified.\')"', '')
content = content.replace('onclick="return confirm(\'Approve this loan?\')"', '')
content = content.replace('onclick="return confirm(\'Reject this loan?\')"', '')

# Also remove any other confirm dialogs
content = content.replace('onclick="return confirm', '')

with open('templates/staff_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Confirmation popups removed from staff dashboard!')
