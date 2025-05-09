from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm
from ..models import User

users = Blueprint("users", __name__)

""" ************ User Management views ************ """


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('activities.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()
        return redirect(url_for('users.login'))
    
    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('activities.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if (user is not None and
            bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user)
            return redirect(url_for('users.account'))
        else:    
            flash("Login failed. Check your username and/or password")
    
    return render_template("login.html", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('activities.index')) 


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            # TODO: handle update username form submit
            new_user = update_username_form.username.data
            current_user.modify(username=new_user)
            current_user.save()
            return redirect(url_for('users.account'))
    
    
    return render_template("account.html", update_username_form=update_username_form)

    