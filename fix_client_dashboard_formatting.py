# fix_client_dashboard_formatting.py
with open('templates/client_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace amount formatting
content = content.replace('{{ loan.amount }}', '{{ loan.amount|format_currency }}')
content = content.replace('{{ \"%.2f\"|format(loan.amount) }}', '{{ loan.amount|format_currency }}')
content = content.replace('Tsh {{ \"%.2f\"|format(loan.amount) }}', '{{ loan.amount|format_currency }}')

with open('templates/client_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Client dashboard amount formatting fixed!')
