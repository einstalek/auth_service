from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = "1c1854408dccfb5711abfbc58b2d7b6b"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
db = SQLAlchemy(app)
encoder_addr = "http://localhost:5557/"
bcrypt = Bcrypt(app)


from flask_auth import routes



