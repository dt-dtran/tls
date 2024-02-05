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

    def __init__(self, email, password):
        self.email = email
        self.password = sha256_crypt.hash(password)

    def json(self):
        return {'id': self.id, 'account_id': self.account_id, 'email': self.email, 'password': self.password}

@app.get("/")
def read_root():
    accounts = Account.query.all()
    return jsonify(accounts)

# create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)

# create a account
@app.route('/accounts', methods=['POST'])
def create_account():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        new_account = Account(email=email, password=password)
        db.session.add(new_account)
        db.session.commit()
        return make_response(jsonify({'message': 'Account created'}), 201)
    # except IntegrityError as e:
    #     db.session.rollback()
    #     return jsonify({'error': 'Account already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/accounts', methods=['GET'])
def get_accounts():
    try:
        accounts = Account.query.all()
        return make_response(jsonify([account.json() for account in accounts]), 200)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# get account by account_id
@app.route('/accounts/<string:account_id>', methods=['GET'])
def get_account(account_id):
    try:
        account = Account.query.filter_by(account_id=account_id).first()
        if account:
            return make_response(jsonify({'account': account.json()}), 200)
        return make_response(jsonify({'message': 'AccountID not found'}), 404)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# delete account
@app.route('/accounts/<string:account_id>', methods=['DELETE'])
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
