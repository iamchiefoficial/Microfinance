# finish_form.py
with open("templates/group_loan_form.html", "a", encoding="utf-8") as f:
    f.write("<label>Kiasi cha mkopo (Tsh):</label>\n")
    f.write('<input type="number" name="loan_amount" required><br><br>\n')
    f.write('<button type="submit">WASILISHA</button>\n')
    f.write('</form>\n')
    f.write('<a href="/client_dashboard">Back to Dashboard</a>\n')
    f.write('</body>\n')
    f.write('</html>\n')

print("✅ Minimal form completed!")
