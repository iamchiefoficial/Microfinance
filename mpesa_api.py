import requests
import base64
import json
from datetime import datetime
from flask import current_app

class MpesaAPI:
    """M-Pesa API Integration for Tanzania"""
    
    def __init__(self):
        # Sandbox credentials from your Postman collection
        self.consumer_key = 'UnDvUCktXcQDyRScx0uAnJlA7rboMWhSnAxvhSOYQiX8QU0t'
        self.consumer_secret = 'eP7nwvhM3OwL0nVhRlOCsGnRawPi32BkENmT33NygDpdYdq5sy1WyAshdCnidCkb'
        self.base_url = 'https://sandbox.safaricom.co.ke'
        self.shortcode = '174379'  # Paybill shortcode
        self.passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        self.callback_url = 'https://orethan-microfinance.com/callback'  # Update with your actual URL
        
    def get_access_token(self):
        """Get OAuth access token"""
        try:
            auth = base64.b64encode(f'{self.consumer_key}:{self.consumer_secret}'.encode()).decode()
            url = f'{self.base_url}/oauth/v1/generate?grant_type=client_credentials'
            headers = {'Authorization': f'Basic {auth}'}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                token = response.json().get('access_token')
                return token
            else:
                print(f'Token error: {response.text}')
                return None
        except Exception as e:
            print(f'Error getting token: {e}')
            return None
    
    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        """Send STK Push to customer phone - Lipa Na M-Pesa Online"""
        try:
            token = self.get_access_token()
            if not token:
                return {'ResponseCode': '1', 'ResponseDescription': 'Failed to get token'}
            
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = base64.b64encode(f'{self.shortcode}{self.passkey}{timestamp}'.encode()).decode()
            
            url = f'{self.base_url}/mpesa/stkpush/v1/processrequest'
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # Format phone number (remove 0 or +255, add 254 for Kenya)
            phone = ''.join(filter(str.isdigit, phone_number))
            if phone.startswith('0'):
                phone = '254' + phone[1:]
            elif phone.startswith('255'):
                phone = '254' + phone[3:]
            elif not phone.startswith('254'):
                phone = '254' + phone
            
            payload = {
                'BusinessShortCode': self.shortcode,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': int(amount),
                'PartyA': phone,
                'PartyB': self.shortcode,
                'PhoneNumber': phone,
                'CallBackURL': self.callback_url,
                'AccountReference': account_reference[:12],
                'TransactionDesc': transaction_desc[:13]
            }
            
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            return {'ResponseCode': '1', 'ResponseDescription': str(e)}
    
    def query_status(self, checkout_request_id):
        """Query transaction status"""
        try:
            token = self.get_access_token()
            if not token:
                return {'ResponseCode': '1', 'ResponseDescription': 'Failed to get token'}
            
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = base64.b64encode(f'{self.shortcode}{self.passkey}{timestamp}'.encode()).decode()
            
            url = f'{self.base_url}/mpesa/stkpushquery/v1/query'
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'BusinessShortCode': self.shortcode,
                'Password': password,
                'Timestamp': timestamp,
                'CheckoutRequestID': checkout_request_id
            }
            
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            return {'ResponseCode': '1', 'ResponseDescription': str(e)}
    
    def simulate_c2b_payment(self, amount, msisdn, bill_ref):
        """Simulate C2B payment (for testing)"""
        try:
            token = self.get_access_token()
            if not token:
                return {'ResponseCode': '1', 'ResponseDescription': 'Failed to get token'}
            
            url = f'{self.base_url}/mpesa/c2b/v1/simulate'
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'ShortCode': self.shortcode,
                'CommandID': 'CustomerPayBillOnline',
                'Amount': int(amount),
                'Msisdn': msisdn,
                'BillRefNumber': bill_ref
            }
            
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            return {'ResponseCode': '1', 'ResponseDescription': str(e)}

# Create a global instance
mpesa = MpesaAPI()
