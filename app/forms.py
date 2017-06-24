from flask_wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required
from wtforms.widgets import TextArea
from wtforms.fields import StringField

class LoginForm(Form):
    login = TextField('login', validators = [Required()])
    password = TextField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class FilterForm(Form):
    city = TextField('city', validators = [Required ()])
    age_from = TextField('age_from', validators = [Required ()])
    age_to = TextField('age_to', validators = [Required ()])
    school_year = TextField('school_year', validators = [Required ()])
    school = TextField('school', validators = [Required ()])
    name = TextField('q', validators = [Required ()])

class DeliveryForm(Form):
    text = StringField('text', widget=TextArea(), validators = [Required ()])
    name = TextField('school', validators = [Required ()])