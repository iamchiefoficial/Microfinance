# create_clean_form.py
html_content = '<!DOCTYPE html><html><head><title>Group Loan</title><meta charset="UTF-8"><style>body{font-family:Arial;background:#f0f0f0;padding:20px}.container{max-width:800px;margin:0 auto;background:white;padding:30px;border-radius:10px}input,select{width:100%;padding:8px;margin-bottom:15px}.btn-submit{background:#2c5aa6;color:white;padding:12px;border:none;width:100%}.section{background:#f9f9f9;padding:15px;margin-bottom:20px}h2{color:#2c5aa6}</style></head><body><div class="container"><h2>ORETHAN MICROFINANCE</h2><h3>FOMU YA MKOPO WA KIKUNDI</h3><form method="POST" action="/submit_group_loan"><div class="section"><h4>1. TAARIFA ZA MWOMBAJI</h4><label>Jina kamili:</label><input type="text" name="applicant_full_name" required><label>Jinsia:</label><select name="gender"><option>Me</option><option>Ke</option></select><label>Simu:</label><input type="tel" name="phone"></div><div class="section"><h4>2. KIASI CHA MKOPO</h4><label>Kiasi (Tsh):</label><input type="number" name="loan_amount" required><label>Malengo:</label><textarea name="loan_purpose" rows="3"></textarea></div><button type="submit" class="btn-submit">WASILISHA MAOMBI</button></form><a href="/client_dashboard">Back</a></div></body></html>'

with open("templates/group_loan_form.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Clean HTML form created!")
print("📁 File: templates/group_loan_form.html")
print("📏 Size:", len(html_content), "characters")
