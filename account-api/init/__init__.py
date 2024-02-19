from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import uuid
from passlib.hash import sha256_crypt
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object("init.config.Config")
db = SQLAlchemy(app)

migrate = Migrate(app, db)

@dataclass
class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(50), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = sha256_crypt.hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def json(self):
        return {'id': self.id, 'account_id': self.account_id, 'email': self.email, 'password': self.password, 'first_name': self.first_name, 'last_name': self.last_name}

@app.get("/")
def read_root():
    return {"Endpoint": "Account"}

@app.get("/health")
def health_check():
    content = {"status": "ok"}
    return jsonify(status="ok")

# create a account
@app.route('/api/accounts', methods=['POST'])
def create_account():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        new_account = Account(email=email, password=password, first_name=first_name, last_name=last_name)
        db.session.add(new_account)
        db.session.commit()
        return make_response(jsonify({'message': 'Account created'}), 201)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    try:
        accounts = Account.query.all()
        return make_response(jsonify([account.json() for account in accounts]), 200)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# get account by account_id
@app.route('/api/accounts/<string:account_id>', methods=['GET'])
def get_account(account_id):
    try:
        account = Account.query.filter_by(account_id=account_id).first()
        if account:
            return make_response(jsonify({'account': account.json()}), 200)
        return make_response(jsonify({'message': 'AccountID not found'}), 404)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# delete account
@app.route('/api/accounts/<string:account_id>', methods=['DELETE'])
def delete_account(account_id):
    try:
        account = Account.query.filter_by(account_id=account_id).first()
        if account:
            db.session.delete(account)
            db.session.commit()
            return make_response(jsonify({'message': 'Account deleted'}), 200)
        return make_response(jsonify({'message': 'Account not found'}), 404)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
