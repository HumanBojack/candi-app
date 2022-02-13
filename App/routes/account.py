from functools import wraps
from flask import render_template, redirect, url_for, flash, request
from flask_restful import abort
from App import app, db, app, mail
from App.models.candidacies import Candidacy
from App.models.users import User
from App.models.companies import Company
from App.forms import (
    AccountCreation,
    AccountGeneration,
    Login,
    AddCandidacy,
    ModifyCandidacy,
    ModifyPassword,
    RecoverModifyPw,
    RecoverPw,
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from random import *
import string
import os
from flask_restful import Resource
from App.tools import (
    generate_confirmation_token,
    send_mail,
    confirm_token,
    admin_required,
)


class ForgottenPw(Resource):
    form = RecoverPw()

    def get(self):
        if self.form.validate_on_submit():
            self.post()
        return render_template("recover_password.html", form=self.form)

    def post(self):
        user = User.query.filter_by(email=self.form.email.data).first()
        if user:
            token = generate_confirmation_token(user.email)

            subject = "Password reset requested"

            recover_url = url_for("recover_pw", token=token, _external=True)

            send_mail(subject, recover_url, user.email)
            flash("An email has been sent to your address", category="success")
            return redirect(url_for("home_page"))
        else:
            flash(
                "Aucun compte connu lié à cette addresse, veuillez vous inscrire",
                category="danger",
            )


class RecoverPw(Resource):

    form = RecoverModifyPw()

    def get(self, token):
        if self.form.validate_on_submit():
            self.post(token)
        return render_template("recover_modify_password.html", form=self.form)

    def post(self, token):
        try:
            email = confirm_token(token, expiration=3600)
        except:
            abort(404)
        if self.form.password.data == self.form.verify_password.data:
            user = User.query.filter_by(email=email).first()
            user.password = generate_password_hash(
                self.form.password.data, method="sha256"
            )
            user.save_to_db()
            flash(f"Votre mot de passe a été modifié", category="success")
            return redirect(url_for("login_page"))


class ModifyPassword(Resource):
    """[Allow to generate the template of modify_password.html on modify_password path to modify profile in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [modify password code page]
    """

    form = ModifyPassword()

    @login_required
    def get(self):
        if self.form.validate_on_submit():
            self.post()
        return render_template("modify_password.html", form=self.form)

    @login_required
    def post(self):
        if check_password_hash(current_user.password, self.form.current_password.data):
            if self.form.new_password.data == self.form.verify_new_password.data:
                current_user.password = generate_password_hash(
                    self.form.new_password.data, method="sha256"
                )
                db.session.add(current_user)
                db.session.commit()

                flash(f"Votre mot de passe a été modifié", category="success")
                return redirect(url_for("board_page"))
            else:
                flash("Les mots de passe ne correspondent pas", category="danger")
        else:
            flash("Mot de passe actuel invalide", category="danger")


class AccountGeneration(Resource):

    form = AccountGeneration()

    @login_required
    @admin_required
    def get(self):
        if self.form.validate_on_submit():
            self.post()
        return render_template("account_generation.html", form=self.form)

    @login_required
    @admin_required
    def post(self):
        characters = string.ascii_letters + string.punctuation + string.digits
        password = "".join(choice(characters) for x in range(randint(8, 16)))

        user = User()
        user.email = self.form.email.data
        user.promotion = self.form.promotion.data
        user.is_admin = 0
        user.last_name = "Unknown"
        user.first_name = "Unknown"
        user.password = generate_password_hash(password, method="sha256")
        jsonuser = user.json()
        token = generate_confirmation_token(jsonuser)

        subject = "Account creation request"

        recover_url = url_for("account_creation", token=token, _external=True)

        send_mail(subject, recover_url, user.email)
        flash("The email have been sent", category="success")
        return redirect(url_for("account_generation"))


class AccountCreation(Resource):

    form = AccountCreation()

    def get(self, token):
        if self.form.validate_on_submit():
            self.post()
        return render_template("account_creation.html", form=self.form)

    def post(self, token):
        try:
            user = confirm_token(token, expiration=3600)
        except:
            abort(404)
        if self.form.password.data == self.form.verify_password.data:
            new_user = User()
            new_user.email = user["email"]
            new_user.is_admin = user["is_admin"]
            new_user.promotion = user["promotion"]
            new_user.password = generate_password_hash(
                self.form.password.data, method="sha256"
            )
            new_user.first_name = self.form.first_name.data
            new_user.last_name = self.form.last_name.data
            new_user.phone_number = None
            if self.form.phone.data == "":
                new_user.phone_number = self.form.phone.data
            new_user.save_to_db()
            flash("Account created", category="success")
            return redirect(url_for("login_page"))
        else:
            flash("Failed", category="danger")
