# create_disburse_loan.py
content = '''<!DOCTYPE html>
<html>
<head>
    <title>Disburse Loan - Orethan Microfinance</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial;background:#f5f5f5;padding:20px}
        .container{max-width:600px;margin:0 auto;background:white;padding:30px;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}
        h1{color:#2c5aa6;margin-bottom:20px}
        .loan-info{background:#e8f4fd;padding:15px;border-radius:5px;margin-bottom:20px}
        .form-group{margin-bottom:20px}
        label{display:block;font-weight:bold;margin-bottom:8px;color:#555}
        input,select{width:100%;padding:10px;border:1px solid #ddd;border-radius:5px;font-size:14px}
        button{background:#28a745;color:white;padding:12px;border:none;border-radius:5px;cursor:pointer;width:100%;font-size:16px}
        .btn-back{background:#6c757d;margin-bottom:20px;display:inline-block;padding:8px 15px;color:white;text-decoration:none;border-radius:5px}
        .method-card{border:1px solid #ddd;border-radius:5px;padding:15px;margin:10px 0;cursor:pointer;transition:all 0.3s}
        .method-card:hover{border-color:#2c5aa6;background:#f0f0ff}
        .method-card.selected{border-color:#2c5aa6;background:#e8e8ff}
        .method-icon{font-size:24px;margin-right:10px}
        .bank-fields{display:none;margin-top:20px;padding:15px;background:#f8f9fa;border-radius:5px}
    </style>
</head>
<body>
    <div class="container">
        <a href="/staff_dashboard" class="btn-back">← Back to Dashboard</a>
        <h1>💰 Disburse Loan</h1>
        
        <div class="loan-info">
            <p><strong>Loan ID:</strong> #{{ loan.id }}</p>
            <p><strong>Client:</strong> {{ loan.client.full_name or loan.client.username }}</p>
            <p><strong>Amount:</strong> Tsh {{ "%.2f"|format(loan.amount) }}</p>
            <p><strong>Purpose:</strong> {{ loan.purpose }}</p>
        </div>
        
        <form method="POST">
            <div class="form-group">
                <label>Disbursement Method</label>
                <div onclick="selectMethod('M-Pesa')" class="method-card" id="method-mpesa">
                    <span class="method-icon">📱</span> M-Pesa - Send to phone number
                </div>
                <div onclick="selectMethod('Tigo Pesa')" class="method-card" id="method-tigo">
                    <span class="method-icon">📱</span> Tigo Pesa - Send to phone number
                </div>
                <div onclick="selectMethod('Airtel Money')" class="method-card" id="method-airtel">
                    <span class="method-icon">📱</span> Airtel Money - Send to phone number
                </div>
                <div onclick="selectMethod('NMB Bank')" class="method-card" id="method-nmb">
                    <span class="method-icon">🏦</span> NMB Bank - Bank Transfer
                </div>
                <div onclick="selectMethod('CRDB Bank')" class="method-card" id="method-crdb">
                    <span class="method-icon">🏦</span> CRDB Bank - Bank Transfer
                </div>
                <input type="hidden" name="method" id="disbursement_method" required>
            </div>
            
            <div class="form-group">
                <label>Amount to Disburse (Tsh)</label>
                <input type="number" name="amount" value="{{ loan.amount }}" required step="1000">
            </div>
            
            <div id="mobileFields" style="display:none">
                <div class="form-group">
                    <label>Phone Number</label>
                    <input type="tel" name="phone_number" placeholder="Enter phone number (e.g., 07xxxxxxxx)">
                </div>
            </div>
            
            <div id="bankFields" style="display:none">
                <div class="form-group">
                    <label>Account Number</label>
                    <input type="text" name="account_number" placeholder="Enter account number">
                </div>
                <div class="form-group">
                    <label>Account Holder Name</label>
                    <input type="text" name="account_holder" placeholder="Enter account holder name">
                </div>
            </div>
            
            <button type="submit" onclick="return confirm('Confirm disbursement of Tsh ' + document.querySelector('[name=amount]').value + ' to client?')">Confirm Disbursement</button>
        </form>
        
        <div style="margin-top:20px;padding:15px;background:#fff3cd;border-radius:5px">
            <h3>⚠️ Important:</h3>
            <p>Once disbursed, this action cannot be undone.</p>
            <p>Client will be notified via SMS/Email if configured.</p>
        </div>
    </div>
    
    <script>
        function selectMethod(method) {
            document.getElementById('disbursement_method').value = method;
            
            // Reset selection
            document.querySelectorAll('.method-card').forEach(card => {
                card.classList.remove('selected');
            });
            if (method === 'M-Pesa') document.getElementById('method-mpesa').classList.add('selected');
            if (method === 'Tigo Pesa') document.getElementById('method-tigo').classList.add('selected');
            if (method === 'Airtel Money') document.getElementById('method-airtel').classList.add('selected');
            if (method === 'NMB Bank') document.getElementById('method-nmb').classList.add('selected');
            if (method === 'CRDB Bank') document.getElementById('method-crdb').classList.add('selected');
            
            // Show/hide fields
            if (method.includes('Bank')) {
                document.getElementById('mobileFields').style.display = 'none';
                document.getElementById('bankFields').style.display = 'block';
            } else {
                document.getElementById('mobileFields').style.display = 'block';
                document.getElementById('bankFields').style.display = 'none';
            }
        }
    </script>
</body>
</html>'''

with open('templates/disburse_loan.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Disbursement form created!')
