from flask import Flask, render_template
from api import api_bp
from models import User,db,init_db
import os
from flask_jwt_extended import JWTManager

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///finance.db')  
app = Flask(__name__)

app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'production')  # 預設為 production
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'e3562575bcbb2a7966bd11de99344452824591b0ec96c4ea97ec47509101d5dd')  # 預設密鑰

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)
init_db(app)
# e3562575bcbb2a7966bd11de99344452824591b0ec96c4ea97ec47509101d5dd
app.register_blueprint(api_bp)

@app.route('/')
def home():
    return render_template('./login.html')

@app.route('/register')
def register():
    return render_template('./register.html')

@app.route('/finance')
def finance():
    return render_template('finance.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print('Server started on port 5001')  
    app.run(host='0.0.0.0', port=5001,debug=(app.config['FLASK_ENV'] == 'development'))
