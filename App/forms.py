from flask_wtf import FlaskForm
from wtforms import PasswordField,EmailField,SubmitField,StringField, SelectField
from wtforms.validators import Length,DataRequired,Email,EqualTo,ValidationError,URL
from .models import User

class Login(FlaskForm):
    """[Form to login]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    password = PasswordField(label="Mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Se connecter")


class AddCandidacy(FlaskForm):
    """[Form to add candidacy]
    """
    company_id = StringField(label='Entreprise', validators=[DataRequired()]) # a changer
    contact_full_name = StringField(label='Nom de la personne contactee', validators=[DataRequired()])
    contact_email = EmailField(label='Email de cette derniere') #, validators=[Email(message="Veuillez entrer une adresse email valide")])
    contact_phone = StringField(label='Son numero de telephone')
    job_title = SelectField("Intitule du poste", choices=[(0, "Data Analyst"), (1, "Data Scientist"), (2, "Data Engineer"), (3, "Dev IA"), (4, "Dev Python"), (5, "Autre")])
    contact_link = StringField(label="Lien de l'annonce / du site") #, validators=[URL(message="Veuillez entrer un lien valide")])
    submit = SubmitField(label='Ajouter')
class ModifyCandidacy(FlaskForm): # We should inherit add and modify from a candidacy class
    """[form to modify candidacy]
    """
    company_id = StringField(label='Entreprise', validators=[DataRequired()]) # a changer
    contact_full_name = StringField(label='Nom de la personne contactee', validators=[DataRequired()])
    contact_email = EmailField(label='Email de cette derniere') #, validators=[Email(message="Veuillez entrer une adresse email valide")])
    contact_phone = StringField(label='Son numero de telephone')
    job_title = SelectField("Intitule du poste", choices=[(0, "Data Analyst"), (1, "Data Scientist"), (2, "Data Engineer"), (3, "Dev IA"), (4, "Dev Python"), (5, "Autre")])
    contact_link = StringField(label="Lien de l'annonce / du site") #, validators=[URL(message="Veuillez entrer un lien valide")])
    status = SelectField(label="Status de la demande", choices=[(0, "En cours"), (1, "Accepté"), (2, "Refusé")])

    submit = SubmitField(label="Valider")

class ModifyProfile(FlaskForm):
    """[Form to modify profile]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    current_password = PasswordField(label="Mot de passe actuel:", validators = [DataRequired()])
    new_password = PasswordField(label="Nouveau mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Valider")
