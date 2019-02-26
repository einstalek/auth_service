from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from cryptography.fernet import Fernet


app = Flask(__name__)
app.config['SECRET_KEY'] = "1c1854408dccfb5711abfbc58b2d7b6b"
app.config['TOKEN_SECRET_KEY'] = Fernet.generate_key()
encoder = Fernet(app.config['TOKEN_SECRET_KEY'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from flask_auth import routes



