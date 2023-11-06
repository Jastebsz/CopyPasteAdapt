# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask import session,Blueprint
#from apps.authentication.models import Users
from geopy.geocoders import Nominatim
from apps import db
from apps.home.models import Worker
def role():
    username = session.get('username')
    role = session.get('role')
    return username, role

@blueprint.route('/index')
@login_required
def index():
    username, user_role = role()
    workers = Worker.query.all()[:5]

    return render_template('home/index.html', segment='index', username=username, role=user_role,workers=workers)

# @blueprint.route('/temlpate/tables',methods=["POST", "GET"])
# @login_required
# def tables():
#     username, user_role = role()
#     segment = get_segment(request)
#     workers = Worker.query.all()  # Запрос к таблице Worker
#     return render_template("home/tables.html", segment=segment, username=username, role=user_role, workers=workers)

# @blueprint.route('/billin', methods=['GET', 'POST'])
# @login_required
# def show_billing():
#     username, user_role = role()
#     return render_template('home/billing.html', segment='billing', username=username, role=user_role)

# @blueprint.route('/calendar', methods=['GET', 'POST'])
# @login_required
# def show_calendar():
#     username, user_role = role()
#     return render_template('home/calendar.html', segment='calendar', username=username, role=user_role)

# @blueprint.route('/notifications')
# @login_required
# def show_notification():
#     username, user_role = role()
#     return render_template('home/notifications.html', segment='notifications', username=username, role=user_role)

# @blueprint.route('/profile')
# @login_required
# def show_profile():
#     username, user_role = role()
#     return render_template('home/profile.html', segment='profile', username=username, role=user_role)

# @blueprint.route('/tables')  # Обновленный маршрут для страницы с таблицей
# @login_required
# def show_users():
#     username, user_role = role()
#     users = Users.query.all()
#     # Получаем всех пользователей из базы данных
#     return render_template('home/tables.html', segment='tables', username=username, role=user_role, users=users)  # Передаем список пользователей в шаблон
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="myGeocoder")
@blueprint.route('/<template>', methods=['GET', 'POST'])
@login_required
def route_template(template):
    username,user_role=role() # Получите имя пользователя из сессии
    try:
        
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)
        if template == 'tables.html':
            workers = Worker.query.all()[:3]
            for worker in workers:
                # Разбиваем координаты на широту и долготу
                latitude, longitude = map(float, worker.location.split(', '))
                
                # Выполняем геокодирование
                location_data = geolocator.reverse(f"{latitude}, {longitude}", language='ru', exactly_one=True)
                
                # Получаем адрес и обновляем поле location
                if location_data:
                    address_elements = location_data.address.split(', ')
                    # Переупорядочиваем элементы адреса в нужной последовательности
                    address = f"{address_elements[3]}, {address_elements[1]}, {address_elements[0]}"
                    # Обновим поле location
                    worker.location = address

            # Теперь у вас есть обновленные записи работников
            return render_template("home/" + template, segment=segment, username=username, role=user_role, workers=workers)
        if template == 'workers.html':
            workers = Worker.query.all()
            for worker in workers:
                # Разбиваем координаты на широту и долготу
                latitude, longitude = map(float, worker.location.split(', '))
                
                # Выполняем геокодирование
                location_data = geolocator.reverse(f"{latitude}, {longitude}", language='ru', exactly_one=True)
                
                # Получаем адрес и обновляем поле location
                if location_data:
                    address_elements = location_data.address.split(', ')
                    # Переупорядочиваем элементы адреса в нужной последовательности
                    address = f"{address_elements[3]}, {address_elements[1]}, {address_elements[0]}"
                    # Обновим поле location
                    worker.location = address

            # Теперь у вас есть обновленные записи работников
            return render_template("home/" + template, segment=segment, username=username, role=user_role, workers=workers)


        # Serve the file (if exists) from app/templates/home/FILE.html
        else:
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
from flask import request, jsonify

@blueprint.route('/update_worker/<int:worker_id>', methods=['POST'])
def update_worker(worker_id):
    # Получите данные из запроса
    data = request.json

    # Найдите сотрудника по ID
    worker = Worker.query.get(worker_id)

    if worker:
        # Обновите данные сотрудника
        for field, value in data.items():
            setattr(worker, field, value)

        # Сохраните изменения в базе данных
        db.session.commit()

        return jsonify({'message': 'Данные успешно обновлены'})
    else:
        return jsonify({'error': 'Сотрудник не найден'}), 404
