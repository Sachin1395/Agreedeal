from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

class PostForm(FlaskForm):
    title = StringField("Crop Name", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    date = StringField("Bids Ends In", validators=[DataRequired()])
    harvest = StringField("Expected Harvest Date", validators=[DataRequired()])
    amount = StringField("Amount of Produce", validators=[DataRequired()])
    baseprice = StringField("Base price", validators=[DataRequired()])
    img_url = StringField("Image URL")
    submit = SubmitField("Submit Post")

class Bid(FlaskForm):
    bid = StringField(validators=[DataRequired()], render_kw={"placeholder": "Your bid must higher than current bid"})
    submit = SubmitField("Submit Post")

class close(FlaskForm):
    submit = SubmitField("Submit Post")

