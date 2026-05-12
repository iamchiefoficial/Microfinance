# create_test_data.py
from app_fixed_workflow import app, db, User, Loan
from werkzeug.security import generate_password_hash
from datetime import datetime

with app.app_context():
    # Create a test client if not exists
    client = User.query.filter_by(username='test_client').first()
    if not client:
        client = User(
            username='test_client',
            email='client@test.com',
            full_name='Test Client',
            phone='1234567890',
            password=generate_password_hash('client123'),
            role='client',
            created_at=datetime.now()
        )
        db.session.add(client)
        db.session.commit()
        print("✅ Test client created")
    
    # Create a loan application for this client
    loan = Loan(
        client_id=client.id,
        amount=5000,
        purpose='Business',
        term_months=12,
        interest_rate=10.0,
        monthly_payment=439.58,
        status='pending',
        current_stage='loan_officer',  # Start at loan officer stage
        created_at=datetime.now()
    )
    db.session.add(loan)
    db.session.commit()
    print(f"✅ Loan #{loan.id} created for client {client.username}")
    print(f"   Current stage: {loan.current_stage}")
