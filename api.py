from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from models import User,db,init_db,Transaction,TransactionType
from datetime import datetime
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity


# 初始化 Blueprint
api_bp = Blueprint('api', __name__)
bcrypt = Bcrypt()

@api_bp.route('/api/login',methods = ['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if not username or not password:
        return jsonify({'message':'Missing username or password'}),400
    user = db.session.query(User).filter_by(username = username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error':'Invalid username or password'}),401
    token = create_access_token(identity=username)
    return jsonify(access_token=token),200
    
@api_bp.route("/api/register",methods = ['POST'])
def register():
    data = request.get_json()
    if not data['username'] or not data['password']:
        return jsonify({'message':'Missing username or password'}),400
    
    if db.session.query(User).filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    
    hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username = data['username'],password = hash)
    print(f'user :{user.username} password :{user.password}')
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message':"Successfully Registered!"}),201

@api_bp.route("/api/transaction",methods = ['POST'])
@jwt_required()
def add_transactions():
    user_id = get_jwt_identity()
    data = request.get_json()
    transaction_date = datetime.strptime(data['date'], "%Y-%m-%d").date()
    transaction_type = TransactionType[data['type'].upper()]
    category = data['category']
    amount = data['amount']

    note = data['note']
    if not type or not category or not amount or not transaction_date:
        return jsonify({'message':'Missing type or category or amount or date'}),400
    
    transaction = Transaction(user_id = user_id,type = transaction_type,category = category,amount = amount,date = transaction_date,note = note)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message':"Successfully Added!"}),201

@api_bp.route("/api/transaction",methods = ['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    print(f'user_id ',user_id)
    start = request.args.get('start_date')
    end = request.args.get('end_date')
    category = request.args.get('category')
    print(f'start {start} end {end} category {category}')
    try:
        query = db.session.query(Transaction).filter_by(user_id=user_id)
        if start:
            start_obj = datetime.strptime(start, "%Y-%m-%d").date()
            query = query.filter(Transaction.date >= start_obj)
        
        if end:
            end_obj = datetime.strptime(end, "%Y-%m-%d").date()
            query = query.filter(Transaction.date <= end_obj)
        if category and category!="ALL":
            query = query.filter(Transaction.category == category)
        
        transactions = query.all()
        print(f'transactions {transactions}')
        transactions_list = [{
            "id": t.id,
            "user_id": t.user_id,
            "type": t.type.value,
            "category": t.category,
            "amount": t.amount,
            "date": str(t.date),
            "note": t.note
        } for t in transactions]
        return jsonify(transactions_list),200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@api_bp.route("/api/transaction/<int:transaction_id>",methods = ['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    user_id = get_jwt_identity()
    transaction = db.session.query(Transaction).filter_by(id = transaction_id,user_id=user_id).first()
    if not transaction:
        return jsonify({"error":"交易不存在"}),404
    try:
        db.session.delete(transaction)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({'message':"Successfully Deleted!"}),200
    