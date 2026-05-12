# create_swahili_translation.py
swahili_content = '''msgid ""
msgstr ""
"Project-Id-Version: Orethan Microfinance\\n"
"Language: sw\\n"
"Content-Type: text/plain; charset=utf-8\\n"

# Login Page
msgid "Login"
msgstr "Ingia"

msgid "Username"
msgstr "Jina la mtumiaji"

msgid "Password"
msgstr "Nenosiri"

msgid "Don't have an account? Register here"
msgstr "Huna akaunti? Jisajili hapa"

msgid "Invalid username or password!"
msgstr "Jina la mtumiaji au nenosiri si sahihi!"

msgid "Welcome"
msgstr "Karibu"

msgid "Logout"
msgstr "Toka"

# Dashboard
msgid "Client Portal"
msgstr "Lango la Mteja"

msgid "Staff Portal"
msgstr "Lango la Mfanyakazi"

msgid "Admin Portal"
msgstr "Lango la Msimamizi"

msgid "Apply for Individual Loan"
msgstr "Omba Mkopo wa Binafsi"

msgid "Apply for Group Loan"
msgstr "Omba Mkopo wa Kikundi"

msgid "Total Loans"
msgstr "Jumla ya Mikopo"

msgid "Active Loans"
msgstr "Mikopo Inayoendelea"

msgid "Completed Loans"
msgstr "Mikopo Iliyokamilika"

msgid "My Loan Applications"
msgstr "Maombi Yangu ya Mkopo"

msgid "No loan applications yet"
msgstr "Hakuna maombi ya mkopo bado"

# Staff Dashboard
msgid "Pending Your Approval"
msgstr "Inasubiri Idhini Yako"

msgid "Loans Pending Your Review"
msgstr "Mikopo Inayosubiri Ukaguzi Wako"

msgid "Approve"
msgstr "Kubali"

msgid "Reject"
msgstr "Kataa"

msgid "Total Clients"
msgstr "Jumla ya Wateja"

msgid "Total Staff"
msgstr "Jumla ya Wafanyakazi"

msgid "Loan Details"
msgstr "Maelezo ya Mkopo"

msgid "Client Name"
msgstr "Jina la Mteja"

msgid "Purpose"
msgstr "Madhumuni"

msgid "Term"
msgstr "Muda"

msgid "Monthly Payment"
msgstr "Malipo ya Mwezi"

msgid "Application Date"
msgstr "Tarehe ya Ombi"

msgid "All Registered Clients"
msgstr "Wateja Wote Waliojisajili"

# Registration
msgid "Register"
msgstr "Jisajili"

msgid "Full Name"
msgstr "Jina Kamili"

msgid "Email"
msgstr "Barua pepe"

msgid "Phone Number"
msgstr "Nambari ya Simu"

msgid "Confirm Password"
msgstr "Thibitisha Nenosiri"

msgid "Registration successful!"
msgstr "Umejisajili kikamilifu!"

msgid "Username already exists"
msgstr "Jina la mtumiaji tayari lipo"

# Loan Application
msgid "Loan Amount"
msgstr "Kiasi cha Mkopo"

msgid "Select purpose"
msgstr "Chagua madhumuni"

msgid "Repayment Period"
msgstr "Muda wa Kulipa"

msgid "Submit Application"
msgstr "Wasilisha Ombi"

msgid "Loan application submitted successfully"
msgstr "Ombi la mkopo limewasilishwa kikamilifu"

# Notifications
msgid "Loan approved"
msgstr "Mkopo umekubaliwa"

msgid "Loan rejected"
msgstr "Mkopo umekataliwa"

msgid "Payment received"
msgstr "Malipo yamepokelewa"

msgid "Document uploaded successfully"
msgstr "Hati imepakiwa kikamilifu"

# Errors
msgid "Access denied"
msgstr "Hakuna ruhusa"

msgid "Page not found"
msgstr "Ukurasa haupatikani"

msgid "Server error"
msgstr "Hitilafu ya seva"

# Buttons
msgid "Save"
msgstr "Hifadhi"

msgid "Cancel"
msgstr "Ghairi"

msgid "Delete"
msgstr "Futa"

msgid "Edit"
msgstr "Hariri"

msgid "View"
msgstr "Angalia"

msgid "Download"
msgstr "Pakua"

msgid "Upload"
msgstr "Pakia"

msgid "Search"
msgstr "Tafuta"

msgid "Filter"
msgstr "Chuja"

msgid "Export"
msgstr "Hamisha"

msgid "Print"
msgstr "Chapisha"

# Status
msgid "Pending"
msgstr "Inasubiri"

msgid "Approved"
msgstr "Imekubaliwa"

msgid "Rejected"
msgstr "Imekataliwa"

msgid "Disbursed"
msgstr "Imetolewa"

msgid "Completed"
msgstr "Imekamilika"

# Months
msgid "January"
msgstr "Januari"

msgid "February"
msgstr "Februari"

msgid "March"
msgstr "Machi"

msgid "April"
msgstr "Aprili"

msgid "May"
msgstr "Mei"

msgid "June"
msgstr "Juni"

msgid "July"
msgstr "Julai"

msgid "August"
msgstr "Agosti"

msgid "September"
msgstr "Septemba"

msgid "October"
msgstr "Oktoba"

msgid "November"
msgstr "Novemba"

msgid "December"
msgstr "Desemba"

# Days
msgid "Monday"
msgstr "Jumatatu"

msgid "Tuesday"
msgstr "Jumanne"

msgid "Wednesday"
msgstr "Jumatano"

msgid "Thursday"
msgstr "Alhamisi"

msgid "Friday"
msgstr "Ijumaa"

msgid "Saturday"
msgstr "Jumamosi"

msgid "Sunday"
msgstr "Jumapili"
'''

with open('translations/sw/LC_MESSAGES/messages.po', 'w', encoding='utf-8') as f:
    f.write(swahili_content)
print('✅ Swahili translation file created!')
