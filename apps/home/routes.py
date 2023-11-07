# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask import session,Blueprint
#from apps.authentication.models import Users
from geopy.geocoders import Nominatim
from apps import db
from apps.home.models import Worker,Users,Full_tasks,Schedule,Scheduler

from flask import request, jsonify



@blueprint.route('/update_users', methods=['POST'])
def update_users():
    try:
        data = request.json  # Получите данные, отправленные с фронтенда

        # Пройдитесь по данным и обновите каждого пользователя в базе данных
        for item in data:
            user_id = item['id']
            username = item['username']
            role = item['role']

            user = Users.query.get(user_id)
            if user:
                user.username = username
                user.role = role
            print('Hello')
        db.session.commit()  # Сохраните изменения в базе данных

        return jsonify({'message': 'Данные пользователей успешно обновлены'})
    except Exception as e:
            return jsonify({'error': 'Произошла ошибка при обновлении данных пользователей'}), 500

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

def workers_func():
    workers=Worker.query.all()
    # for worker in workers:
    #             # Разбиваем координаты на широту и долготу
    #     latitude, longitude = map(float, worker.location.split(', '))
                    
    #                 # Выполняем геокодирование
    #     location_data = geolocator.reverse(f"{latitude}, {longitude}", language='ru', exactly_one=True)
                    
    #                 # Получаем адрес и обновляем поле location
    #     if location_data:
    #         address_elements = location_data.address.split(', ')
    #                     # Переупорядочиваем элементы адреса в нужной последовательности
    #         address = f"{address_elements[3]}, {address_elements[1]}, {address_elements[0]}"
    #                     # Обновим поле location
    #         worker.location = address
    return workers


# Здесь определите другие модели данных, если необходимо

def find_task_data_by_idt(idt):
    task = Full_tasks.query.filter_by(idt=idt).first()
    if task:
        # Вернуть данные о задаче в виде словаря
        return {
            "idt": task.idt,
            "task_title":task.task_title,
            "task_priority":task.task_priority,
            "task_level":task.task_level,
            "address": task.point_address,
            "date":task.date
            # Добавьте другие поля, если они нужны
        }
    else:
        # Если задача с указанным idt не найдена, вернуть None или другое значение по умолчанию
        return None


from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="myGeocoder")
@blueprint.route('/<template>', methods=['GET', 'POST'])
@login_required
def route_template(template):
    workers=Worker.query.all()
    users=Users.query.all()
    full_tasks=Full_tasks.query.all()
    username,user_role=role() # Получите имя пользователя из сессии
    try:
        
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)
        if template == 'tables.html':
            workers=Worker.query.all()[:3]
            users=Users.query.all()[:3]
            full_tasks=Full_tasks.query.all()
            schedule=Schedule.query.all()
            

            # result_full = []
            # task_user_mapping = {}

            # for user in users:
            #     for task in user.tasks:
            #         task_user_mapping[task.idt] = user

            # for key, idt in result:
            #     if idt in task_user_mapping:
            #         user = task_user_mapping[idt]
            #         # Получаем данные о задаче
            #         task_data = find_task_data_by_idt(idt)
            #         if task_data:
            #             new = Scheduler(
            #                 id=key,
            #                 task_title=task_data.task_title,
            #                 task_priority=task_data.task_priority,
            #                 task_level=task_data.task_level,
            #                 point_address=task_data.point_address,
            #                 status=task_data.status,
            #                 username=user.username  # Добавляем имя пользователя
            #             )
            #             result_full.append(new)
                
            
            
            # for worker in workers:
            #     # Разбиваем координаты на широту и долготу
            #     latitude, longitude = map(float, worker.location.split(', '))
                
            #     # Выполняем геокодирование
            #     location_data = geolocator.reverse(f"{latitude}, {longitude}", language='ru', exactly_one=True)
                
            #     # Получаем адрес и обновляем поле location
            #     if location_data:
            #         address_elements = location_data.address.split(', ')
            #         # Переупорядочиваем элементы адреса в нужной последовательности
            #         address = f"{address_elements[3]}, {address_elements[1]}, {address_elements[0]}"
            #         # Обновим поле location
            #         worker.location = address

            # # Теперь у вас есть обновленные записи работников
            return render_template("home/" + template, segment=segment, username=username, role=user_role, workers=workers,users=users)
        if template == 'workers.html':
            workers=workers_func()
            # Теперь у вас есть обновленные записи работников
            return render_template("home/" + template, segment=segment, username=username, role=user_role, workers=workers)
        if template == 'users.html':
            users=Users.query.all()
            for user in users:
                user.password='***'
            # Теперь у вас есть обновленные записи работников
            return render_template("home/" + template, segment=segment, username=username, role=user_role, users=users)

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
