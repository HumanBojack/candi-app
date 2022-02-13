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


class LoginPage(Resource):
    """[Allow to ask login and generate the template of login.html on login path]

    Returns:
        [str]: [login page code]
    """

    form = Login()

    def get(self):
        if self.form.validate_on_submit():
            self.post()
        return render_template("login.html", form=self.form)

    def post(self):
        user = User.query.filter_by(email=self.form.email.data).first()
        if user and check_password_hash(user.password, self.form.password.data):
            login_user(user)
            flash(
                f"Vous êtes connecté en tant que : {user.first_name} {user.last_name}",
                category="success",
            )
            if user.is_admin == 1:
                return redirect(url_for("admin_board_page"))
            else:
                return redirect(url_for("board_page"))
        else:
            flash("Adresse email ou mot de passe invalide", category="danger")


class LogoutPage(Resource):
    @login_required
    def get():
        """[Allows to disconnect the user and redirect to the home page]"""
        logout_user()
        flash("Vous êtes correctement déconnecté", category="success")
        return redirect(url_for("home"))
