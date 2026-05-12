# create_make_payment.py
content = '''<!DOCTYPE html>
<html>
<head>
    <title>Make Payment - Orethan Microfinance</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial;background:#f5f5f5;padding:20px}
        .container{max-width:600px;margin:0 auto;background:white;padding:30px;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}
        h1{color:#2c5aa6;margin-bottom:20px}
        .form-group{margin-bottom:20px}
        label{display:block;font-weight:bold;margin-bottom:8px;color:#555}
        input,select{width:100%;padding:10px;border:1px solid #ddd;border-radius:5px;font-size:14px}
        button{background:#2c5aa6;color:white;padding:12px;border:none;border-radius:5px;cursor:pointer;width:100%;font-size:16px}
        .btn-back{background:#6c757d;margin-bottom:20px}
        .payment-methods{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:20px}
        .method-card{border:1px solid #ddd;border-radius:5px;padding:15px;text-align:center;cursor:pointer;transition:all 0.3s}
        .method-card:hover{border-color:#2c5aa6;background:#f0f0ff}
        .method-card.selected{border-color:#2c5aa6;background:#e8e8ff}
        .method-icon{font-size:30px;margin-bottom:5px}
        .bank-details{display:none;margin-top:20px;padding:15px;background:#f8f9fa;border-radius:5px}
        .alert{background:#d4edda;color:#155724;padding:10px;border-radius:5px;margin-bottom:20px}
    </style>
</head>
<body>
    <div class="container">
        <a href="/client_dashboard" class="btn-back" style="display:inline-block;padding:8px 15px;background:#6c757d;color:white;text-decoration:none;border-radius:5px;margin-bottom:20px">← Back</a>
        <h1>💰 Make Loan Payment</h1>
        <p><strong>Loan Amount:</strong> Tsh {{ "%.2f"|format(loan.amount) }}</p>
        <p><strong>Loan ID:</strong> #{{ loan.id }}</p>
        
        <form method="POST" id="paymentForm">
            <div class="form-group">
                <label>Payment Method</label>
                <div class="payment-methods">
                    <div class="method-card" onclick="selectMethod('M-Pesa')">
                        <div class="method-icon">📱</div>
                        <div>M-Pesa</div>
                    </div>
                    <div class="method-card" onclick="selectMethod('Tigo Pesa')">
                        <div class="method-icon">📱</div>
                        <div>Tigo Pesa</div>
                    </div>
                    <div class="method-card" onclick="selectMethod('Airtel Money')">
                        <div class="method-icon">📱</div>
                        <div>Airtel Money</div>
                    </div>
                    <div class="method-card" onclick="selectMethod('NMB Bank')">
                        <div class="method-icon">🏦</div>
                        <div>NMB Bank</div>
                    </div>
                    <div class="method-card" onclick="selectMethod('CRDB Bank')">
                        <div class="method-icon">🏦</div>
                        <div>CRDB Bank</div>
                    </div>
                </div>
                <input type="hidden" name="payment_method" id="payment_method" required>
            </div>
            
            <div class="form-group">
                <label>Amount (Tsh)</label>
                <input type="number" name="amount" required min="1000" step="1000" placeholder="Enter amount">
            </div>
            
            <div id="mobileMoneyFields" style="display:none">
                <div class="form-group">
                    <label>Phone Number</label>
                    <input type="tel" name="phone_number" placeholder="0xxxxxxxxx">
                </div>
            </div>
            
            <div id="bankFields" style="display:none">
                <div class="form-group">
                    <label>Account Number</label>
                    <input type="text" name="account_number" placeholder="Account number">
                </div>
                <div class="form-group">
                    <label>Bank Name</label>
                    <input type="text" name="bank_name" id="bank_name" placeholder="Bank name">
                </div>
            </div>
            
            <button type="submit">Process Payment</button>
        </form>
        
        <div style="margin-top:20px;padding:15px;background:#e8f4fd;border-radius:5px">
            <h3>Payment Instructions:</h3>
            <p>📱 <strong>Mobile Money:</strong> Enter your registered phone number</p>
            <p>🏦 <strong>Bank Transfer:</strong> Use your account number</p>
            <p>✅ Payment will be processed immediately</p>
        </div>
    </div>
    
    <script>
        function selectMethod(method) {
            document.getElementById('payment_method').value = method;
            
            // Reset selection
            document.querySelectorAll('.method-card').forEach(card => {
                card.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');
            
            // Show/hide fields
            if (method.includes('M-Pesa') || method.includes('Tigo') || method.includes('Airtel')) {
                document.getElementById('mobileMoneyFields').style.display = 'block';
                document.getElementById('bankFields').style.display = 'none';
            } else {
                document.getElementById('mobileMoneyFields').style.display = 'none';
                document.getElementById('bankFields').style.display = 'block';
                document.getElementById('bank_name').value = method;
            }
        }
    </script>
</body>
</html>'''

with open('templates/make_payment.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Payment template created!')
