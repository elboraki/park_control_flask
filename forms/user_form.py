from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired(), Length(min=2, max=50)])
    prenom = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    login = StringField('Login', validators=[DataRequired(), Length(min=4, max=20)])
    mot_passe = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    role_id = SelectField('Rôle', coerce=int, validators=[DataRequired()]) 