# fix_client_loan_history_formatting.py
with open('templates/client_loan_history.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace amount formatting
content = content.replace('Tsh {{ \"%.2f\"|format(loan.amount) }}', '{{ loan.amount|format_currency }}')
content = content.replace('{{ \"%.2f\"|format(loan.amount) }}', '{{ loan.amount|format_currency }}')

with open('templates/client_loan_history.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Client loan history amount formatting fixed!')
