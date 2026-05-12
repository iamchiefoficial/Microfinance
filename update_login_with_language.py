# update_login_with_language.py
with open('templates/login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add language switcher to header
content = content.replace('<div class="header-content">', '<div class="header-content">\n            {% include "language_switcher.html" %}')

with open('templates/login.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Login template updated with language switcher!')
