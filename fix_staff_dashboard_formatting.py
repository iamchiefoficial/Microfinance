# fix_staff_dashboard_formatting.py
with open('templates/staff_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace amount formatting
content = content.replace('Tsh {{ \"%.2f\"|format(loan.amount) }}', '{{ loan.amount|format_currency }}')
content = content.replace('{{ \"%.2f\"|format(loan.amount) }}', '{{ loan.amount|format_currency }}')
content = content.replace('Tsh {{ loan.amount }}', '{{ loan.amount|format_currency }}')
content = content.replace('Tsh {{ \"%.2f\"|format(loan.amount) }}', '{{ loan.amount|format_currency }}')

# Fix monthly payment formatting
content = content.replace('Tsh {{ \"%.2f\"|format(loan.monthly_payment) }}', '{{ loan.monthly_payment|format_currency }}')

with open('templates/staff_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Staff dashboard amount formatting fixed!')
