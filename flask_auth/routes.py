from flask import render_template, redirect, url_for, request
from flask_auth import app, db, bcrypt
from flask_auth.models import User
from flask_auth.forms import RegistrationForm, LoginForm
from flask_auth import encoder


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.validate():
            # TODO: шифрование и дешифрование вынести в отдельный сервис
            token = encoder.encrypt(form.username.data.encode('utf-8'))
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
def home():
    token = request.cookies.get('token')
    username = request.cookies.get('username')
    if token and username:
        try:
            # TODO: шифрование и дешифрование вынести в отдельный сервис
            if encoder.decrypt(token.encode('utf-8')).decode('utf-8') == username:
                return "Welcome, " + username
        except:
            pass
    return redirect(url_for("login"))


@app.route('/logout')
def logout():
    resp = redirect(url_for("login"))
    resp.set_cookie('token', '')
    resp.set_cookie('username', '')
    return resp

