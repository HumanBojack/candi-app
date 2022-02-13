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


class AddCandidacy(Resource):
    """[Allow to generate the template of add_candidacy.html on candidacy path to add candidacy in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [Candidacy code page]
    """

    form = AddCandidacy()

    @login_required
    def get(self):
        if self.form.validate_on_submit():
            self.post()
        return render_template("add_candidacy.html", form=self.form)

    @login_required
    def post(self):
        if self.form.radio.data == "1":
            company = Company(
                name=self.form.new_company_name.data,
                sector=self.form.new_company_sector.data,
                type=self.form.new_company_type.data,
            )
            company.save_to_db()  # should add a try and except on this in order to redirect if there is a problem
            company_id = company.id
        else:
            company_id = self.form.company_id.data

        contact_phone = None
        if self.form.contact_phone.data != "":
            contact_phone = self.form.contact_phone.data

        Candidacy(
            user_id=current_user.id,
            company_id=company_id,
            location_id=self.form.location_id.data,
            contact_full_name=self.form.contact_full_name.data,
            contact_email=self.form.contact_email.data,
            contact_phone=contact_phone,
            job_title=self.form.job_title.data,
            contact_link=self.form.contact_link.data,
            date=self.form.date.data,
        ).save_to_db()
        flash("Nouvelle Candidature ajouté ", category="success")
        return redirect(url_for("board_page"))


class UpdateCandidacy(Resource):
    """[Allow to generate the template of modify_candidacy.html on modify_candidacy path to modify candidacy in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [modify candidacy code page]
    """

    @login_required
    def get(self, id):
        self.candidacy = Candidacy.query.get_or_404(id)
        candidacy_js = self.candidacy.json()
        self.form = ModifyCandidacy(**candidacy_js)
        if self.form.validate_on_submit():
            self.post(id)
        return render_template(
            "modify_candidacy.html", form=self.form, candidacy=self.candidacy.json()
        )

    @login_required
    def post(self, id):
        self.candidacy.company_id = self.form.company_id.data
        self.candidacy.contact_full_name = self.form.contact_full_name.data
        self.candidacy.contact_email = self.form.contact_email.data
        if self.form.contact_phone.data == "":
            self.candidacy.contact_phone = None
        else:
            self.candidacy.contact_phone = self.form.contact_phone.data
        self.candidacy.job_title = self.form.job_title.data
        self.candidacy.contact_link = self.form.contact_link.data
        self.candidacy.status = self.form.status.data
        self.candidacy.date = self.form.date.data  # .strftime("%Y-%m-%d")

        try:
            self.candidacy.save_to_db()
            return redirect(url_for("board_page"))
        except:
            flash("Something goes wrong", category="danger")

    @login_required
    def delete(self, id):
        """[Allow to delete candidacy in the BDD with the id and redirect to board page]"""

        # candidacy_id = request.args.get("id")
        # Candidacy.query.filter_by(id=candidacy_id).first().delete_from_db()
        Candidacy.query.get_or_404(id).delete_from_db()
        flash("Candidature supprimé avec succés", category="success")
        return redirect(url_for("board_page"))
