# remove_disbursement_confirmations.py
with open('templates/disburse_loan.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove confirm popup from disbursement
content = content.replace('onclick="return confirm(\'Confirm disbursement of Tsh \' + document.querySelector(\'[name=amount]\').value + \' to client?\')"', '')

with open('templates/disburse_loan.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Confirmation popups removed from disbursement page!')
