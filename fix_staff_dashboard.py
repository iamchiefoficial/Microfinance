# fix_staff_dashboard.py
with open('templates/staff_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add a simple navigation section if not present
if '<div class="navigation">' not in content:
    # Add navigation after header
    nav_section = '''
    <div class="navigation" style="background:#f8f9fa;padding:10px;margin-bottom:20px;border-radius:5px">
        <a href="/staff_dashboard" style="margin-right:15px;text-decoration:none;color:#2c5aa6;font-weight:bold">📊 Dashboard</a>
        <a href="/dashboard" style="text-decoration:none;color:#6c757d">🔙 Main Portal</a>
    </div>'''
    
    # Insert after the header div
    content = content.replace('</div>\n    <div class="container">', '</div>' + nav_section + '\n    <div class="container">')

with open('templates/staff_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Staff dashboard navigation updated!')
