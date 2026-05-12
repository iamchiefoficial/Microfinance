# update_client_dashboard_payments.py
import re

with open('templates/client_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add payment button to loan items
payment_button = '''
                    <div style="margin-top:10px">
                        <a href="/make_payment/{{ loan.id }}" style="background:#28a745;color:white;padding:5px 15px;text-decoration:none;border-radius:3px;display:inline-block">💰 Make Payment</a>
                    </div>
'''

# Insert after loan item content
content = content.replace('</div>{% endfor %}', payment_button + '</div>{% endfor %}')

with open('templates/client_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Client dashboard updated with payment button!')
