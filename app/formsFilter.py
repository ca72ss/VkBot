from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class FilterForm(Form):
	city = TextField('city', validators = [Required ()])