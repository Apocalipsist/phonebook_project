from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class Contact(FlaskForm):
    first = StringField('First Name', validators=[DataRequired()])
    last = StringField('Last name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    home = StringField('Address', validators=[DataRequired()])
    submit = SubmitField()


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    user_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[
                                 DataRequired(), EqualTo('password')])
    submit = SubmitField()


class LogInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()
