# create_language_switcher.py
content = '''<div style="display:inline-block; margin-left:15px;">
    <a href="/set_language/en" style="color:white; text-decoration:none; padding:5px 10px; background:rgba(255,255,255,0.2); border-radius:5px; margin-right:5px;">🇬🇧 EN</a>
    <a href="/set_language/sw" style="color:white; text-decoration:none; padding:5px 10px; background:rgba(255,255,255,0.2); border-radius:5px;">🇹🇿 SW</a>
</div>'''
with open('templates/language_switcher.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Language switcher template created!')
