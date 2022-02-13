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
from App.tools import admin_required


class Board(Resource):
    @login_required
    def get(self):
        """[Allow to generate the template of board.html on board path, if user is authenticated else return on login]

        Returns:
            [str]: [board page code different if the user is admin or not]
        """
        if current_user.is_admin:
            return render_template(
                "admin_board.html", user_candidacy=Candidacy.all_candidacies_to_list()
            )
        else:
            return render_template(
                "board.html", user_candidacy=Candidacy.user_to_json(current_user.id)
            )
