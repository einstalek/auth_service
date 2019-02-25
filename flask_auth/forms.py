from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, DataRequired, Email
from flask_auth.models import User
from flask_auth import bcrypt
from wtforms import ValidationError


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(),
                                       Length(5, 20)])
    password = PasswordField("Password",
                             validators=[DataRequired(),
                                         Length(5, 20)])
    email = StringField("Email",
                        validators=[DataRequired(),
                                    Email()])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already taken')


class LoginForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(),
                                       Length(5, 20)])
    password = PasswordField("Password",
                             validators=[DataRequired(),
                                         Length(5, 20)])
    submit = SubmitField("Sign In")

    def validate(self) -> bool:
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, self.password.data):
                return True
        return False
