from functools import wraps
from flask import render_template, redirect, url_for, flash, request
from flask_restful import abort
from App import app, db, app, mail, api
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

# from App.routes.account import Account
from App.routes.auth import LoginPage, LogoutPage
from App.routes.boards import Board

# from App.routes.candidacies import Candidacies
from App.routes.statics import Home

api.add_resource(Home, "/")
api.add_resource(Board, "/board")
api.add_resource(LoginPage, "/login")
api.add_resource(LogoutPage, "/logout")
