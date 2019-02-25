from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = "1c1854408dccfb5711abfbc58b2d7b6b"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from flask import redirect
home_redirect = redirect("http://localhost:8888", code=302)
from flask_auth import routes



