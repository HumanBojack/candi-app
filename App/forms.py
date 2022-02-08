from flask_wtf import FlaskForm
from wtforms import PasswordField,EmailField,SubmitField,StringField,SelectField,IntegerField,RadioField
from wtforms.validators import Length,DataRequired,Email,EqualTo,ValidationError,Optional
from .models import User, Location, Company

class Login(FlaskForm):
    """[Form to login]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    password = PasswordField(label="Mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Se connecter")
    
class Candidacy(FlaskForm):
    """[Create the basis of the Candidacies forms]
    """
    company_choices = [(g.id, g.name) for g in Company.query.all()]
    company_id = SelectField(coerce=int, choices=company_choices)

    location_choices = [(g.id, g.region) for g in Location.query.all()]
    location_id = SelectField(label="Le lieu de cette entreprise / antenne", coerce=int, choices=location_choices)

    contact_full_name = StringField(label='Nom de la personne contactee', validators=[DataRequired()])
    contact_email = EmailField(label='Email de cette derniere') #, validators=[Email(message="Veuillez entrer une adresse email valide")])
    contact_phone = IntegerField(label='Son numero de telephone', validators=[Optional()])
    job_title = SelectField("Intitule du poste", choices=[(0, "Data Analyst"), (1, "Data Scientist"), (2, "Data Engineer"), (3, "Dev IA"), (4, "Dev Python"), (5, "Autre")])
    contact_link = StringField(label="Lien de l'annonce / du site") #, validators=[URL(message="Veuillez entrer un lien valide")])
class AddCandidacy(Candidacy):
    """[Form to add candidacy]
    """
    radio = RadioField(choices=[(0, "Entreprise existante"), (1, "Nouvelle entreprise")], default=0)
    new_company_name = StringField(label="Nom")
    new_company_sector = SelectField(label="Secteur", choices=[(0,"Marketing"), (1, "Médical"), (2, "Industrie")])
    new_company_type = SelectField(label="Type", choices=[(0, "Startup"), (1, "ESN"), (2, "Gros groupe")])

    submit = SubmitField(label='Ajouter')
class ModifyCandidacy(Candidacy): # We should inherit add and modify from a candidacy class
    """[form to modify candidacy]
    """
    status = SelectField(label="Status de la demande", choices=[(0, "En cours"), (1, "Accepté"), (2, "Refusé")])
    submit = SubmitField(label="Valider")

class ModifyProfile(FlaskForm):
    """[Form to modify profile]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    current_password = PasswordField(label="Mot de passe actuel:", validators = [DataRequired()])
    new_password = PasswordField(label="Nouveau mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Valider")
