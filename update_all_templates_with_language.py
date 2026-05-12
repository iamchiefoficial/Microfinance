# update_all_templates_with_language.py
templates = ['client_dashboard.html', 'staff_dashboard.html', 'admin_dashboard.html']
for template in templates:
    try:
        with open(f'templates/{template}', 'r', encoding='utf-8') as f:
            content = f.read()
        if 'language_switcher' not in content:
            content = content.replace('<div class="header-content">', '<div class="header-content">\n            {% include "language_switcher.html" %}')
            with open(f'templates/{template}', 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'✅ Language switcher added to {template}')
        else:
            print(f'ℹ️ Language switcher already exists in {template}')
    except:
        print(f'⚠️ {template} not found')
