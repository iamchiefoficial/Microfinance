# fix_admin_loans_formatting.py
with open('templates/admin_loans.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace amount formatting
content = content.replace('{{ \"%.2f\"|format(loan.amount) }}', '{{ loan.amount|format_currency }}')

with open('templates/admin_loans.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Admin loans amount formatting fixed!')
