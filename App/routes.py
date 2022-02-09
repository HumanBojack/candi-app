from functools import wraps
from flask import render_template, redirect, url_for, flash, request
from .models import User, Candidacy, Company, Location
from flask_restful import abort
from App import app, db, app, mail
from .forms import AccountCreation, AccountGeneration, Login, AddCandidacy, ModifyCandidacy, ModifyPassword, RecoverModifyPw, RecoverPw
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from random import *
import string
from datetime import datetime

def admin_required(func):
    """
    Modified login_required decorator to restrict access to admin group.
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        if current_user.is_admin != 1:     
            flash("You don't have permission to access this resource.", "warning")
            return redirect(url_for("home_page"))
        return func(*args, **kwargs)
    return decorator

def send_mail(title, body, email):
    msg = Message(f'{title}', sender = 'candi.app.mailer@gmail.com', recipients = [f'{email}'])
    msg.body = f'{body}'
    mail.send(msg)

def generate_confirmation_token(data):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(data, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        data = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return data

@app.route('/')
@app.route('/home')
def home_page():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """[Allow to ask login and generate the template of login.html on login path]

    Returns:
        [str]: [login page code]
    """
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Vous êtes connecté en tant que : {user.first_name} {user.last_name}",category="success")
            if user.is_admin == 1:
                return redirect(url_for('admin_board_page'))
            else:
                return redirect(url_for('board_page'))
        else:
            flash('Adresse email ou mot de passe invalide',category="danger")
    return render_template('login.html',form=form)

@app.route('/forgotten_pw', methods=['GET','POST'])
def forgotten_pw():
    form = RecoverPw()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_confirmation_token(user.email)
            
            subject = "Password reset requested"
            
            recover_url = url_for(
                'recover_pw',
                token=token,
                _external=True)
            
            send_mail(subject, recover_url, user.email)
            return redirect(url_for('home_page'))
        
    return render_template('recover_password.html',form=form)

@app.route('/recover_pw/<token>', methods=['GET', 'POST'])
def recover_pw(token):
    try:
        email = confirm_token(token, expiration=3600)
    except:
        abort(404)
    form = RecoverModifyPw()
    if form.validate_on_submit():
        if form.password.data == form.verify_password.data:
            user = User.query.filter_by(email=email).first()
            user.password = generate_password_hash(form.password.data, method='sha256')
            user.save_to_db()
            flash(f"Vous êtes connecté en tant que : {user.first_name} {user.last_name}",category="success")
            return redirect(url_for('login_page'))
    return render_template('recover_modify_password.html',form=form)
                
@app.route('/board', methods=['GET','POST'])
@login_required
def board_page():
    """[Allow to generate the template of board.html on board path, if user is authenticated else return on login]

    Returns:
        [str]: [board page code different if the user is admin or not]
    """
    usercandidacy_attributs = [column.key for column in Candidacy.__table__.columns]
    return render_template('board.html', title = usercandidacy_attributs , user_candidacy = Candidacy.user_to_json(current_user.id)) #Candidacy.find_by_user_id(current_user.id))

@app.route('/admin_board', methods=['GET','POST'])
@login_required
@admin_required
def admin_board_page():
    return render_template('admin_board.html', user_candidacy=Candidacy.all_candidacies_to_list())

@app.route('/logout')
@login_required
def logout_page():
    """[Allows to disconnect the user and redirect to the home page]
    """
    logout_user()
    flash('Vous êtes correctement déconnecté',category="success")
    return redirect(url_for('home_page'))

@app.route('/candidature', methods= ['GET', 'POST'])
@login_required
def add_candidature():
    """[Allow to generate the template of add_candidacy.html on candidacy path to add candidacy in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [Candidacy code page]
    """
    form = AddCandidacy()
    if form.validate_on_submit():
        if form.radio.data == "1":
            company = Company(
                name=form.new_company_name.data,
                sector=form.new_company_sector.data,
                type=form.new_company_type.data
            )
            company.save_to_db() # should add a try and except on this in order to redirect if there is a problem
            company_id = company.id
        else:
            company_id = form.company_id.data

        Candidacy(
            user_id=current_user.id,
            company_id=company_id, #form.company_id.get('data'),
            location_id=form.location_id.data,
            contact_full_name=form.contact_full_name.data,
            contact_email=form.contact_email.data,
            contact_phone=form.contact_phone.data,
            job_title=form.job_title.data,
            contact_link=form.contact_link.data,
            date=form.date.data
        ).save_to_db()
        flash('Nouvelle Candidature ajouté ', category='success')
        return redirect(url_for('board_page'))
    return render_template('add_candidacy.html', form=form)

@app.route('/modify_password', methods=['GET', 'POST'])
@login_required
def modify_password():
    """[Allow to generate the template of modify_password.html on modify_password path to modify profile in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [modify password code page]
    """
    form = ModifyPassword()
    if form.validate_on_submit():
        if  check_password_hash(current_user.password, form.current_password.data):
            if form.new_password.data == form.verify_new_password.data:
                current_user.password = generate_password_hash(form.new_password.data, method='sha256')
                db.session.add(current_user)
                db.session.commit()

                flash(f"Votre mot de passe a été modifié",category="success")
                return redirect(url_for('board_page'))
            else:
                flash('Les mots de passe ne correspondent pas',category="danger")
        else:
            flash('Mot de passe actuel invalide',category="danger")
    return render_template('modify_password.html',form=form)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def modify_candidacy(id):
    """[Allow to generate the template of modify_candidacy.html on modify_candidacy path to modify candidacy in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [modify candidacy code page]
    """
    candidacy = Candidacy.query.get_or_404(id)
    candidacy_js = candidacy.json()
    candidacy_js["date"] = datetime.strptime(candidacy_js["date"], "%Y-%m-%d")
    form = ModifyCandidacy(**candidacy_js)

    if form.validate_on_submit():
        candidacy.company_id = form.company_id.data
        candidacy.contact_full_name = form.contact_full_name.data
        candidacy.contact_email = form.contact_email.data
        candidacy.contact_phone = form.contact_phone.data
        candidacy.job_title = form.job_title.data
        candidacy.contact_link = form.contact_link.data
        candidacy.status = form.status.data
        candidacy.date = form.date.data # .strftime("%Y-%m-%d")

        try:
            candidacy.save_to_db()
            return redirect(url_for('board_page'))
        except:
            flash('Something goes wrong',category="danger")

    return render_template('modify_candidacy.html', form=form , candidacy=candidacy.json())
    
@app.route('/delete_candidacy')
@login_required
def delete_candidacy():
    """[Allow to delete candidacy in the BDD with the id and redirect to board page]"""

    candidacy_id = request.args.get('id')
    Candidacy.query.filter_by(id=candidacy_id).first().delete_from_db()
    flash("Candidature supprimé avec succés",category="success")
    return redirect(url_for('board_page'))

@app.route('/account_generation', methods=['GET', 'POST'])
@login_required
@admin_required
def account_generation():
    form = AccountGeneration()
    if form.validate_on_submit():
        characters = string.ascii_letters + string.punctuation  + string.digits
        password =  "".join(choice(characters) for x in range(randint(8, 16)))
        
        user = User()
        user.email = form.email.data
        user.promotion = form.promotion.data
        user.is_admin = False
        user.last_name = 'Unknown'
        user.first_name = 'Unknown'
        user.password = generate_password_hash(password, method='sha256')
        jsonuser = user.json()
        token = generate_confirmation_token(jsonuser)
                
        subject = "Account creation request"
                
        recover_url = url_for(
            'account_creation',
            token=token,
            _external=True)
                
        send_mail(subject, recover_url, user.email)
        flash('The email have been sent', category= 'success')
        return redirect(url_for('account_generation'))
    return render_template('account_generation.html', form=form)

@app.route('/account_creation/<token>', methods=['GET', 'POST'])
def account_creation(token):
    try:
        user = confirm_token(token, expiration=3600)
    except:
        abort(404)
    form = AccountCreation()
    if form.validate_on_submit():
        if form.password.data == form.verify_password.data:
            new_user = User()
            new_user.email = user['email']
            new_user.is_admin = user['is_admin']
            new_user.promotion = user['promotion']
            new_user.password = generate_password_hash(form.password.data, method='sha256')
            new_user.first_name = form.first_name.data
            new_user.last_name = form.last_name.data
            if form.phone.data:
                new_user.phone_number = form.phone.data
            new_user.save_to_db()
            flash('Account created', category='success')
            return redirect(url_for('login_page'))
        else:
            flash('Failed', category='danger')
    return render_template('account_creation.html',form=form)
