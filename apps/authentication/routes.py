# -*- encoding: utf-8 -*-
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users
from flask import session
from apps.authentication.util import verify_pass

def role1():
    username = session.get('username')
    role = session.get('role')
    return username, role



@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        # Read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check if the user exists in the database
        if user:
            # Check the password
            if verify_pass(password, user.password):
                session['username'] = user.username  # Save the username in the session
                session['role'] = user.role
                login_user(user)

                # Check if the user is an admin
                if user.role == 'admin' and user is not None:
                    return redirect(url_for('authentication_blueprint.route_default'))
                elif user.role != 'admin':
                    # User is not an admin, show a message
                    return render_template('accounts/login.html',
                                           msg='У вас недостаточно прав для доступа',
                                            form=login_form)
                else:    
                    # В случае, когда пользователь не существует
                    return render_template('accounts/login.html',
                                        msg='Обратитесь к администратору для создания аккаунта',
                                        form=LoginForm())  # Передайте пустую форму
            # Password is incorrect
            return render_template('accounts/login.html',
                                   msg='Неверное имя пользователя или пароль',
                                   form=login_form)

        # User doesn't exist in the database
        return render_template('accounts/login.html',
                               msg='Обратитесь к администратору для создания аккаунта',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)

    return redirect(url_for('home_blueprint.index'))



@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    username = session.get('username')
    user_role = session.get('role')
    create_account_form = CreateAccountForm(request.form)
    
    if 'register' in request.form:
        new_username = request.form['username']
        role = request.form['role']

        # Check if the new username exists
        user = Users.query.filter_by(username=new_username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Имя пользователя уже существует',
                                   success=False,
                                   form=create_account_form, username=username, role=user_role)

        # Create the user with the new username
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='Аккаунт успешно создан',
                               success=True,
                               form=create_account_form, username=username, role=user_role)

    else:
        return render_template('accounts/register.html', form=create_account_form, username=username, role=user_role)



@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
