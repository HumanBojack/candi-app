from flask_wtf import FlaskForm
from wtforms import PasswordField,EmailField,SubmitField,StringField
from wtforms.validators import Length,DataRequired,Email,EqualTo,ValidationError

class Login(FlaskForm):
    """[Form to login]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    password = PasswordField(label="Mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Se connecter")

class AddCandidacy(FlaskForm):
    """[Form to add candidacy]
    """
    entreprise = StringField(label='Entreprise', validators=[DataRequired()])
    contact_full_name = StringField(label='contact_full_name', validators=[DataRequired()])
    contact_email = StringField(label='contact_email', validators=[DataRequired()])
    contact_mobilephone = StringField(label='contact_mobilephone')
    submit = SubmitField(label='Ajouter')

class ModifyProfile(FlaskForm):
    """[Form to modify profile]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    current_password = PasswordField(label="Mot de passe actuel:", validators = [DataRequired()])
    new_password = PasswordField(label="Nouveau mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Valider")

class ModifyCandidacy(FlaskForm):
    """[form to modify candidacy]
    """
    contact_full_name = StringField(label='contact_full_name', validators=[DataRequired()])
    contact_email = StringField(label='contact_email', validators=[DataRequired()])
    contact_mobilephone = StringField(label='contact_mobilephone')
    status = StringField(label='Status', validators=[DataRequired()])

    submit = SubmitField(label="Valider")
    
class RecoverPw(FlaskForm):
    """[Form to login]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    submit = SubmitField(label='Valider')
class RecoverModifyPw(FlaskForm):
    """[Form to login]
    """
    password = PasswordField(label="Password:", validators = [DataRequired()])
    verify_password = PasswordField(label="Verify password:", validators = [DataRequired()])
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
    phone = StringField(label="Phone number (Optionnal):")
    password = PasswordField(label="Password:", validators = [DataRequired()])
    verify_password = PasswordField(label="Verify password:", validators = [DataRequired()])
    
    
    submit = SubmitField(label='Valider')