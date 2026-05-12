# fix_individual_loan_form_formatting.py
try:
    with open('templates/individual_loan_form.html', 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('{{ \"%.2f\"|format(loan.amount) }}', '{{ loan.amount|format_currency }}')
    with open('templates/individual_loan_form.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ Individual loan form updated!')
except:
    print('Individual loan form not found, skipping')
