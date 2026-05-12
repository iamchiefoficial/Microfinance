# update_client_dashboard_documents.py
with open('templates/client_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add document links to header or sidebar
doc_links = '''
            <div style="margin-bottom:20px">
                <a href="/upload_document" style="background:#17a2b8;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;margin-right:10px">📁 Upload Document</a>
                <a href="/my_documents" style="background:#6c757d;color:white;padding:10px 20px;text-decoration:none;border-radius:5px">📄 My Documents</a>
            </div>
'''

# Insert after welcome header
content = content.replace('<div class="loan-types">', doc_links + '<div class="loan-types">')

with open('templates/client_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Document links added to client dashboard!')
