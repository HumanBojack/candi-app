from flask_wtf import FlaskForm
from wtforms import PasswordField,EmailField,SubmitField,StringField,SelectField,IntegerField,RadioField,DateField
from wtforms.validators import Length,DataRequired,Email,EqualTo,Regexp,Optional
from .models import User, Location, Company
from App.static import constant
from datetime import datetime

class Login(FlaskForm):
    """[Form to login]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    password = PasswordField(label="Mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Se connecter")
    
class Candidacy(FlaskForm):
    """[Create the basis of the Candidacies forms]
    """
    try:
        company_choices = [(g.id, g.name) for g in Company.query.all()]
        company_id = SelectField(coerce=int, choices=company_choices)
        location_choices = [(g.id, g.region) for g in Location.query.all()]
        location_id = SelectField(label="Le lieu de cette entreprise / antenne", coerce=int, choices=location_choices)
    except:
        pass
    
    date = DateField(label="Date d'inscription", default=datetime.today)
    contact_full_name = StringField(label='Nom de la personne contactee', validators=[DataRequired()])
    contact_email = EmailField(label='Email de cette derniere') #, validators=[Email(message="Veuillez entrer une adresse email valide")])
    contact_phone = StringField(label='Son numero de telephone', validators = [Regexp('^[\\+33|0|0033][1-9][0-9]{8}$', message='Invalide phone number')])
    job_title = SelectField("Intitule du poste", choices=constant.JOB_TITLES)
    contact_link = StringField(label="Lien de l'annonce / du site") #, validators=[URL(message="Veuillez entrer un lien valide")])
class AddCandidacy(Candidacy):
    """[Form to add candidacy]
    """
    radio = RadioField(choices=[(0, "Entreprise existante"), (1, "Nouvelle entreprise")], default=0)
    new_company_name = StringField(label="Nom")
    new_company_sector = SelectField(label="Secteur", choices=constant.COMPANY_SECTOR)
    new_company_type = SelectField(label="Type", choices=constant.COMPANY_TYPE)
    submit = SubmitField(label='Ajouter')
class ModifyCandidacy(Candidacy): # We should inherit add and modify from a candidacy class
    """[form to modify candidacy]
    """
    status = SelectField(label="Status de la demande", choices=constant.STATUS)
    submit = SubmitField(label="Valider")

class ModifyPassword(FlaskForm):
    """[Form to modify profile]
    """
    current_password = PasswordField(label="Mot de passe actuel:", validators = [DataRequired()])
    new_password = PasswordField(label="Nouveau mot de passe:", validators = [DataRequired(),
        Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$', message='Minimum eight characters, at least one upper case, one lower case, one number and one special character'),
        EqualTo('verify_new_password', message='Password must match')])
    verify_new_password = PasswordField(label="Valider nouveau mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Valider")

class RecoverPw(FlaskForm):
    """[Form to login]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    submit = SubmitField(label='Valider')
class RecoverModifyPw(FlaskForm):
    """[Form to login]
    """
    password = PasswordField(label="Password:", validators = [DataRequired(),
        Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$', message='Minimum eight characters, at least one upper case, one lower case, one number and one special character'),
        EqualTo('verify_password', message='Password must match')])
    verify_password = PasswordField(label="Verify password:", validators=[DataRequired()])
    submit = SubmitField(label='Valider')
    
class AccountGeneration(FlaskForm):
    """[Form to login]
    """
    promotion = StringField(label="Promotion:", validators=[DataRequired()])
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    submit = SubmitField(label='Valider')
    
class AccountCreation(FlaskForm):
    """[Form to login]
    """
    first_name = StringField(label="First name:", validators=[DataRequired()])
    last_name = StringField(label="Last name:", validators = [DataRequired()])
    phone = StringField(label="Phone number (Optionnal):", validators = [Regexp('^[\\+33|0|0033][1-9][0-9]{8}$', message='Invalide phone number')])
    password = PasswordField(label="Password:", validators = [DataRequired(),
        Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$', message='Minimum eight characters, at least one upper case, one lower case, one number and one special character'),
        EqualTo('verify_password', message='Password must match')])
    verify_password = PasswordField(label="Verify password:", validators = [DataRequired()])
    submit = SubmitField(label='Valider')
