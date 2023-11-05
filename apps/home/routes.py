# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask import session
#from apps.authentication.models import Users


from apps.home.models import Worker
def role():
    username = session.get('username')
    role = session.get('role')
    return username, role

@blueprint.route('/index')
@login_required
def index():
    username, user_role = role()
    return render_template('home/index.html', segment='index', username=username, role=user_role)


@blueprint.route('/tables')
@login_required
def show_workers():
    username, user_role = role()
    workers = Worker.query.all()  # Query the Worker table
    return render_template('home/tables.html', segment='tables', username=username, role=user_role, workers=workers)

# @blueprint.route('/tables')  # Обновленный маршрут для страницы с таблицей
# @login_required
# def show_users():
#     username, user_role = role()
#     users = Users.query.all()
#     # Получаем всех пользователей из базы данных
#     return render_template('home/tables.html', segment='tables', username=username, role=user_role, users=users)  # Передаем список пользователей в шаблон


@blueprint.route('/<template>')
@login_required
def route_template(template):
    username,user_role=role() # Получите имя пользователя из сессии
    try:
        
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment,username=username, role=user_role)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
