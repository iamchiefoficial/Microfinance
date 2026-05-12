# create_minimal_form.py
html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Group Loan Form</title>
</head>
<body>
    <h1>ORETHAN MICROFINANCE</h1>
    <h2>FOMU YA MKOPO WA KIKUNDI</h2>
    <form method="POST" action="/submit_group_loan">
        <label>Jina kamili:</label>
        <input type="text" name="applicant_full_name" required><br><br>
        <label>Kiasi cha mkopo (Tsh):</label>
        <input type="number" name="loan_amount" required><br><br>
        <button type="submit">WASILISHA</button>
    </form>
    <br>
    <a href="/client_dashboard">Back to Dashboard</a>
</body>
</html>"""

with open("templates/group_loan_form.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Clean minimal form created!")
print("📁 File: templates/group_loan_form.html")
print("📏 Size:", len(html_content), "characters")
