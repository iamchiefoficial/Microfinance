# Mobile App API
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta

api_bp = Blueprint('api', __name__)

# ==================== AUTHENTICATION ====================

@api_bp.route('/api/login', methods=['POST'])
def api_login():
    """Mobile app login"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        db = current_app.extensions['sqlalchemy'].db
User = db.Model.metadata.tables['users']
user = db.session.execute(db.select(User).where(User.c.username == username)).scalar_one_or_none()
        
        if user and check_password_hash(user.password, password):
            # Create access token
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(days=30)
            )
            
            return jsonify({
                'success': True,
                'token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'email': user.email,
                    'phone': user.phone,
                    'role': user.role
                }
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/register', methods=['POST'])
def api_register():
    """Mobile app registration"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        full_name = data.get('full_name')
        email = data.get('email')
        phone = data.get('phone')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
        # Create new user
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            role='client',
            full_name=full_name,
            email=email,
            phone=phone,
            created_at=datetime.now()
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user_id': new_user.id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== LOAN APIS ====================

@api_bp.route('/api/my_loans', methods=['GET'])
@jwt_required()
def api_my_loans():
    """Get user's loans"""
    try:
        user_id = get_jwt_identity()
        loans = Loan.query.filter_by(client_id=user_id).order_by(Loan.created_at.desc()).all()
        
        loan_list = []
        for loan in loans:
            loan_list.append({
                'id': loan.id,
                'amount': loan.amount,
                'amount_formatted': f'Tsh {loan.amount:,.2f}',
                'purpose': loan.purpose,
                'status': loan.status,
                'current_stage': loan.current_stage,
                'stage_name': loan.get_current_stage_name() if hasattr(loan, 'get_current_stage_name') else loan.current_stage,
                'term_months': loan.term_months,
                'monthly_payment': loan.monthly_payment,
                'monthly_payment_formatted': f'Tsh {loan.monthly_payment:,.2f}',
                'created_at': loan.created_at.strftime('%Y-%m-%d %H:%M:%S') if loan.created_at else None
            })
        
        return jsonify({'success': True, 'loans': loan_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/apply_loan', methods=['POST'])
@jwt_required()
def api_apply_loan():
    """Apply for individual loan"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        amount = float(data.get('amount'))
        purpose = data.get('purpose')
        term_months = int(data.get('term_months', 12))
        monthly_payment = amount / term_months
        
        new_loan = Loan(
            client_id=user_id,
            amount=amount,
            purpose=purpose,
            term_months=term_months,
            monthly_payment=monthly_payment,
            status='pending',
            current_stage='loan_officer',
            created_at=datetime.now()
        )
        
        db.session.add(new_loan)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Loan application submitted',
            'loan_id': new_loan.id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/loan_status/<int:loan_id>', methods=['GET'])
@jwt_required()
def api_loan_status(loan_id):
    """Get loan status"""
    try:
        user_id = get_jwt_identity()
        loan = Loan.query.get_or_404(loan_id)
        
        # Check ownership
        if loan.client_id != user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Get approval history
        approvals = []
        if loan.loan_officer_id:
            officer = User.query.get(loan.loan_officer_id)
            approvals.append({
                'stage': 'Loan Officer',
                'approved_by': officer.full_name or officer.username if officer else 'Unknown',
                'date': loan.loan_officer_approved_at.strftime('%Y-%m-%d %H:%M:%S') if loan.loan_officer_approved_at else None
            })
        if loan.loan_manager_id:
            manager = User.query.get(loan.loan_manager_id)
            approvals.append({
                'stage': 'Loan Manager',
                'approved_by': manager.full_name or manager.username if manager else 'Unknown',
                'date': loan.loan_manager_approved_at.strftime('%Y-%m-%d %H:%M:%S') if loan.loan_manager_approved_at else None
            })
        
        return jsonify({
            'success': True,
            'loan': {
                'id': loan.id,
                'amount': loan.amount,
                'amount_formatted': f'Tsh {loan.amount:,.2f}',
                'purpose': loan.purpose,
                'status': loan.status,
                'current_stage': loan.current_stage,
                'term_months': loan.term_months,
                'monthly_payment': loan.monthly_payment,
                'created_at': loan.created_at.strftime('%Y-%m-%d %H:%M:%S') if loan.created_at else None,
                'approvals': approvals
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== REPAYMENT APIS ====================

@api_bp.route('/api/repayment_schedule/<int:loan_id>', methods=['GET'])
@jwt_required()
def api_repayment_schedule(loan_id):
    """Get repayment schedule"""
    try:
        user_id = get_jwt_identity()
        loan = Loan.query.get_or_404(loan_id)
        
        if loan.client_id != user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        repayments = Repayment.query.filter_by(loan_id=loan_id).order_by(Repayment.due_date).all()
        
        schedule = []
        total_paid = 0
        total_due = 0
        
        for repayment in repayments:
            total_due += repayment.amount_due
            total_paid += repayment.amount_paid
            
            schedule.append({
                'id': repayment.id,
                'due_date': repayment.due_date.strftime('%Y-%m-%d'),
                'amount_due': repayment.amount_due,
                'amount_due_formatted': f'Tsh {repayment.amount_due:,.2f}',
                'amount_paid': repayment.amount_paid,
                'status': repayment.status,
                'late_fee': repayment.late_fee,
                'payment_date': repayment.payment_date.strftime('%Y-%m-%d') if repayment.payment_date else None
            })
        
        return jsonify({
            'success': True,
            'loan': {
                'id': loan.id,
                'amount': loan.amount,
                'monthly_payment': loan.monthly_payment,
                'term_months': loan.term_months
            },
            'schedule': schedule,
            'summary': {
                'total_due': total_due,
                'total_paid': total_paid,
                'remaining_balance': total_due - total_paid,
                'payments_made': len([r for r in repayments if r.status == 'paid'])
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== PAYMENT APIS ====================

@api_bp.route('/api/make_payment', methods=['POST'])
@jwt_required()
def api_make_payment():
    """Make payment via M-Pesa"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        loan_id = data.get('loan_id')
        amount = float(data.get('amount'))
        phone_number = data.get('phone_number')
        
        loan = Loan.query.get_or_404(loan_id)
        
        if loan.client_id != user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Initiate M-Pesa payment
        from mpesa_api import mpesa
        response = mpesa.stk_push(
            phone_number=phone_number,
            amount=amount,
            account_reference=f'LOAN{loan_id}',
            transaction_desc=f'Loan repayment {loan_id}'
        )
        
        if response.get('ResponseCode') == '0':
            checkout_id = response.get('CheckoutRequestID')
            
            transaction = Payment(
                loan_id=loan_id,
                client_id=user_id,
                amount=amount,
                payment_method='M-Pesa',
                payment_type='Loan Repayment',
                transaction_id=checkout_id,
                phone_number=phone_number,
                status='pending',
                payment_date=datetime.now()
            )
            db.session.add(transaction)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Payment initiated. Check your phone to complete.',
                'checkout_request_id': checkout_id
            }), 200
        else:
            return jsonify({'success': False, 'message': response.get('ResponseDescription', 'Payment failed')}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/payment_history', methods=['GET'])
@jwt_required()
def api_payment_history():
    """Get payment history"""
    try:
        user_id = get_jwt_identity()
        payments = Payment.query.filter_by(client_id=user_id).order_by(Payment.payment_date.desc()).all()
        
        payment_list = []
        for payment in payments:
            payment_list.append({
                'id': payment.id,
                'loan_id': payment.loan_id,
                'amount': payment.amount,
                'amount_formatted': f'Tsh {payment.amount:,.2f}',
                'method': payment.payment_method,
                'status': payment.status,
                'transaction_id': payment.transaction_id,
                'date': payment.payment_date.strftime('%Y-%m-%d %H:%M:%S') if payment.payment_date else None
            })
        
        return jsonify({'success': True, 'payments': payment_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== USER PROFILE APIS ====================

@api_bp.route('/api/profile', methods=['GET'])
@jwt_required()
def api_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'phone': user.phone,
                'role': user.role,
                'joined_date': user.created_at.strftime('%Y-%m-%d') if user.created_at else None
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/update_profile', methods=['PUT'])
@jwt_required()
def api_update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'email' in data:
            user.email = data['email']
        if 'phone' in data:
            user.phone = data['phone']
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Profile updated'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== STAFF APIS (Admin only) ====================

@api_bp.route('/api/pending_approvals', methods=['GET'])
@jwt_required()
def api_pending_approvals():
    """Get pending approvals based on staff role"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if user.role == 'client':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        if user.role == 'loan_officer':
            pending = Loan.query.filter_by(current_stage='loan_officer', status='pending').all()
        elif user.role == 'loan_manager':
            pending = Loan.query.filter_by(current_stage='loan_manager', status='pending').all()
        elif user.role == 'managing_director':
            pending = Loan.query.filter_by(current_stage='managing_director', status='pending').all()
        elif user.role == 'general_director':
            pending = Loan.query.filter_by(current_stage='general_director', status='pending').all()
        else:
            pending = []
        
        loan_list = []
        for loan in pending:
            loan_list.append({
                'id': loan.id,
                'client_name': loan.client.full_name or loan.client.username,
                'amount': loan.amount,
                'amount_formatted': f'Tsh {loan.amount:,.2f}',
                'purpose': loan.purpose,
                'term_months': loan.term_months,
                'created_at': loan.created_at.strftime('%Y-%m-%d')
            })
        
        return jsonify({'success': True, 'pending_approvals': loan_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/approve_loan/<int:loan_id>', methods=['POST'])
@jwt_required()
def api_approve_loan(loan_id):
    """Approve loan (direct, no confirmation)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        loan = Loan.query.get_or_404(loan_id)
        
        if user.role == 'loan_officer' and loan.current_stage == 'loan_officer':
            loan.current_stage = 'loan_manager'
            loan.loan_officer_id = user.id
            loan.loan_officer_approved_at = datetime.now()
        elif user.role == 'loan_manager' and loan.current_stage == 'loan_manager':
            loan.current_stage = 'managing_director'
            loan.loan_manager_id = user.id
            loan.loan_manager_approved_at = datetime.now()
        elif user.role == 'managing_director' and loan.current_stage == 'managing_director':
            loan.current_stage = 'general_director'
            loan.managing_director_id = user.id
            loan.managing_director_approved_at = datetime.now()
        elif user.role == 'general_director' and loan.current_stage == 'general_director':
            loan.status = 'approved'
            loan.current_stage = 'completed'
            loan.general_director_id = user.id
            loan.general_director_approved_at = datetime.now()
        else:
            return jsonify({'success': False, 'message': 'Cannot approve at this stage'}), 400
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Loan approved', 'new_stage': loan.current_stage}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/reject_loan/<int:loan_id>', methods=['POST'])
@jwt_required()
def api_reject_loan(loan_id):
    """Reject loan"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        loan = Loan.query.get_or_404(loan_id)
        
        if user.role == 'loan_officer' and loan.current_stage == 'loan_officer':
            loan.status = 'rejected'
        elif user.role == 'loan_manager' and loan.current_stage == 'loan_manager':
            loan.current_stage = 'loan_officer'
        elif user.role == 'managing_director' and loan.current_stage == 'managing_director':
            loan.current_stage = 'loan_manager'
        elif user.role == 'general_director' and loan.current_stage == 'general_director':
            loan.current_stage = 'managing_director'
        else:
            return jsonify({'success': False, 'message': 'Cannot reject at this stage'}), 400
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Loan rejected/sent back'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== STATISTICS APIS ====================

@api_bp.route('/api/dashboard_stats', methods=['GET'])
@jwt_required()
def api_dashboard_stats():
    """Get dashboard statistics"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if user.role == 'client':
            loans = Loan.query.filter_by(client_id=user.id).all()
            total_loans = len(loans)
            active_loans = len([l for l in loans if l.status == 'approved'])
            completed_loans = len([l for l in loans if l.status == 'completed'])
            pending_loans = len([l for l in loans if l.status == 'pending'])
            
            return jsonify({
                'success': True,
                'stats': {
                    'total_loans': total_loans,
                    'active_loans': active_loans,
                    'completed_loans': completed_loans,
                    'pending_loans': pending_loans
                }
            }), 200
        else:
            # Staff stats
            total_clients = User.query.filter_by(role='client').count()
            total_loans = Loan.query.count()
            pending_approvals = Loan.query.filter_by(status='pending').count()
            
            return jsonify({
                'success': True,
                'stats': {
                    'total_clients': total_clients,
                    'total_loans': total_loans,
                    'pending_approvals': pending_approvals
                }
            }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
