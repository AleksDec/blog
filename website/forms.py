from turtle import title
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField
from datetime import date

class NewPost(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    subtitle = StringField(label='Subtitle', validators=[DataRequired()])
    img_url = StringField(label='Image URL', validators=[DataRequired(), URL()])
    body = CKEditorField(label='Content', validators=[DataRequired()])
    submit = SubmitField(label='Zapisz')