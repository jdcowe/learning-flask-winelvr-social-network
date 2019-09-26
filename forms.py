from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import IMAGES


class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[InputRequired('Name is required.'), Length(
        max=100, message='The name must be under 100 characters')])
    username = StringField('Username', validators=[InputRequired(
        'Usename is required.'), Length(max=30, message='The name must be under 30 characters')])
    password = PasswordField('Password', validators=[
                             InputRequired('Password is required.')])
    image = FileField(validators=[FileAllowed(
        IMAGES, 'Only images are allowed')])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(
        'Usename is required.'), Length(max=30, message='The name must be under 30 characters')])
    password = PasswordField('Password', validators=[
                             InputRequired('Password is required.')])
    remember = BooleanField('Remember me')


class PostForm(FlaskForm):
    text = TextAreaField('Message', validators=[
                         InputRequired('Message is Required')])
