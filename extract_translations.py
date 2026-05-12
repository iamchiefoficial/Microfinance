# extract_translations.py
import os

# Create messages.pot template
template_content = '''msgid ""
msgstr ""
"Project-Id-Version: Orethan Microfinance\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2024-01-01 00:00+0000\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

# Login Page
msgid "Login"
msgstr ""

msgid "Username"
msgstr ""

msgid "Password"
msgstr ""

msgid "Don't have an account? Register here"
msgstr ""

msgid "Invalid username or password!"
msgstr ""

msgid "Welcome"
msgstr ""

msgid "Logout"
msgstr ""

# Dashboard
msgid "Client Portal"
msgstr ""

msgid "Staff Portal"
msgstr ""

msgid "Admin Portal"
msgstr ""

msgid "Apply for Individual Loan"
msgstr ""

msgid "Apply for Group Loan"
msgstr ""

msgid "Total Loans"
msgstr ""

msgid "Active Loans"
msgstr ""

msgid "Completed Loans"
msgstr ""

msgid "My Loan Applications"
msgstr ""

msgid "No loan applications yet"
msgstr ""

# Staff Dashboard
msgid "Pending Your Approval"
msgstr ""

msgid "Loans Pending Your Review"
msgstr ""

msgid "Approve"
msgstr ""

msgid "Reject"
msgstr ""

msgid "Total Clients"
msgstr ""

msgid "Total Staff"
msgstr ""

msgid "Loan Details"
msgstr ""

msgid "Client Name"
msgstr ""

msgid "Purpose"
msgstr ""

msgid "Term"
msgstr ""

msgid "Monthly Payment"
msgstr ""

msgid "Application Date"
msgstr ""

msgid "All Registered Clients"
msgstr ""

# Registration
msgid "Register"
msgstr ""

msgid "Full Name"
msgstr ""

msgid "Email"
msgstr ""

msgid "Phone Number"
msgstr ""

msgid "Confirm Password"
msgstr ""

msgid "Registration successful!"
msgstr ""

msgid "Username already exists"
msgstr ""

# Loan Application
msgid "Loan Amount"
msgstr ""

msgid "Select purpose"
msgstr ""

msgid "Repayment Period"
msgstr ""

msgid "Submit Application"
msgstr ""

msgid "Loan application submitted successfully"
msgstr ""

# Notifications
msgid "Loan approved"
msgstr ""

msgid "Loan rejected"
msgstr ""

msgid "Payment received"
msgstr ""

msgid "Document uploaded successfully"
msgstr ""

# Errors
msgid "Access denied"
msgstr ""

msgid "Page not found"
msgstr ""

msgid "Server error"
msgstr ""

# Buttons
msgid "Save"
msgstr ""

msgid "Cancel"
msgstr ""

msgid "Delete"
msgstr ""

msgid "Edit"
msgstr ""

msgid "View"
msgstr ""

msgid "Download"
msgstr ""

msgid "Upload"
msgstr ""

msgid "Search"
msgstr ""

msgid "Filter"
msgstr ""

msgid "Export"
msgstr ""

msgid "Print"
msgstr ""

# Status
msgid "Pending"
msgstr ""

msgid "Approved"
msgstr ""

msgid "Rejected"
msgid_plural "Rejected"
msgstr[0] ""
msgstr[1] ""

msgid "Disbursed"
msgstr ""

msgid "Completed"
msgstr ""

# Months
msgid "January"
msgstr ""

msgid "February"
msgstr ""

msgid "March"
msgstr ""

msgid "April"
msgstr ""

msgid "May"
msgstr ""

msgid "June"
msgstr ""

msgid "July"
msgstr ""

msgid "August"
msgstr ""

msgid "September"
msgstr ""

msgid "October"
msgstr ""

msgid "November"
msgstr ""

msgid "December"
msgstr ""

# Days
msgid "Monday"
msgstr ""

msgid "Tuesday"
msgstr ""

msgid "Wednesday"
msgstr ""

msgid "Thursday"
msgstr ""

msgid "Friday"
msgstr ""

msgid "Saturday"
msgstr ""

msgid "Sunday"
msgstr ""
'''

with open('messages.pot', 'w', encoding='utf-8') as f:
    f.write(template_content)
print('✅ Translation template created!')
