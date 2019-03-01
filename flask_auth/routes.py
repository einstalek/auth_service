from functools import wraps

import requests
from cryptography.fernet import InvalidToken
from flask import render_template, redirect, url_for, request

from flask_auth import app, db, bcrypt, encoder_addr, content_addr
from flask_auth.forms import RegistrationForm, LoginForm
from flask_auth.models import User


def encoder_request(d: dict) -> dict:
    resp = requests.post(encoder_addr, d)
    return resp.json()


def encrypt(username: str) -> str:
    return encoder_request({'username': username}).get('token')


def decrypt(token: str) -> str:
    return encoder_request({'token': token}).get('username')


def check_token(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        token: str = request.cookies.get('token')
        username: str = request.cookies.get('username')
        if token and username:
            try:
                decrypted = decrypt(token)
                if decrypted and decrypted == username:
                    return func(*args, **kargs)
            except InvalidToken:
                pass
        return redirect(url_for("login"))
    return wrapper


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.validate():
            token = encrypt(form.username.data)
            if token:
                token = token.encode('utf-8')
                resp = redirect(url_for("home"))
                resp.set_cookie('token', token.decode('utf-8'))
                resp.set_cookie('username', form.username.data)
                return resp
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/")
def root():
    return redirect(url_for('login'))


@app.route("/home")
@check_token
def home():
    return render_template("home.html")


@app.route('/logout')
def logout():
    resp = redirect(url_for("login"))
    resp.set_cookie('token', '')
    resp.set_cookie('username', '')
    return resp


@app.route('/watch/<name>')
def watch(name: str):
    return redirect(content_addr + 'watch/' + name)


