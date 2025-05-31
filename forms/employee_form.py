from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired

class EmployeeForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    date_hire = DateField('Date d\'embauche', validators=[DataRequired()])
    poste_id = SelectField('Poste', coerce=int, validators=[DataRequired()]) 