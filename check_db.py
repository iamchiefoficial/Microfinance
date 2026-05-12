# check_db.py
from app_fixed_workflow import app, db, User, Loan

with app.app_context():
    print("=== USERS ===")
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Name: {user.username}, Role: {user.role}")
    
    print("\n=== LOANS ===")
    loans = Loan.query.all()
    for loan in loans:
        print(f"ID: {loan.id}, Client: {loan.client_id}, Stage: {loan.current_stage}, Status: {loan.status}")
