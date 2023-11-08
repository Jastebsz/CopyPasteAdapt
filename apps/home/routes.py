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
from function import line_tasks, distribute_tasks, delete_last_two_schedule
from flask import request, jsonify
# line_tasks()                          # создание очереди
# distribute_tasks()                    # распределение задач
# delete_last_two_schedule()            # удаление лишних расписаний
# @blueprint.route('/update_worker/<int:worker_id>', methods=['POST'])
# def update_worker(worker_id):
#     try:
#         data = request.json  # Получите данные, отправленные с фронтенда
#         # Пройдитесь по данным и обновите соответствующего работника в базе данных
#         user = Worker.query.get(worker_id)
#         if user:
#             for key, value in data.items():
#                 setattr(user, key, value)
#         db.session.commit()  # Сохраните изменения в базе данных

#         return jsonify({'message': 'Данные работника успешно обновлены'})
#     except Exception as e:
#         return jsonify({'error': 'Произошла ошибка при обновлении данных работника'}), 500
    
#Получение имени пользователя и роли    
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

@blueprint.route('/<template>', methods=['GET', 'POST'])
@login_required
def route_template(template):
    workers=Worker.query.all()
    users=Users.query.all()
    full_tasks=Full_tasks.query.all()
    username,user_role=role() 
    try:
        if not template.endswith('.html'):
            template += '.html'
        segment = get_segment(request)
        if template == 'tables.html':
            workers=Worker.query.all()[:3]
            users=Users.query.all()[:3]
            full_tasks=Full_tasks.query.all()
            schedule=Schedule.query.all()
            return render_template("home/" + template, segment=segment, username=username, role=user_role, workers=workers,users=users)
        if template == 'workers.html':
            workers=Worker.query.all()
            return render_template("home/" + template, segment=segment, username=username, role=user_role, workers=workers)
        if template == 'users.html':
            users=Users.query.all()
            for user in users:
                user.password='***'
            return render_template("home/" + template, segment=segment, username=username, role=user_role, users=users)
        else:
            return render_template("home/" + template, segment=segment,username=username, role=user_role)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
#Обновление строки таблицы users
@blueprint.route('/update_user/<id>', methods=['POST'])
@login_required
def update_users(id):
    try:
        data = request.json
        print(data)
        print(data['id'])
        user = db.session.query(Users).filter(Users.id == data['id']).first()
        if user:
            user.username = data['username']
            user.role = data['role']
            user.worker_FIO= data['worker_FIO']
        db.session.commit()
        return jsonify({'message': 'Данные пользователей успешно обновлены'})
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка при обновлении данных пользователей'}), 500
#Удаление строки из таблицы users    
@blueprint.route('/delete_user/<username>', methods=['POST'])
@login_required
def delete_user(username):
    try:
        row_to_delete = db.session.query(Users).filter(Users.username == username).first()
        print(row_to_delete)
        if  row_to_delete:
            print(row_to_delete)
            db.session.delete(row_to_delete)
            db.session.commit()
            db.session.execute("VACUUM")
            return jsonify({'message': 'Пользователь успешно удален'})
        else:
            return jsonify({'error': 'Пользователь не найден'}), 404
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return jsonify({'error': 'Произошла ошибка при удалении пользователя'}), 500

#Добавление/изменение сотрудников в таблице workers
@blueprint.route('/update_worker/<id>', methods=['POST'])
@login_required
def update_workers(id):
    try:
        data = request.json 
        print(data)
        print(data['id'])
        worker = db.session.query(Worker).filter(Worker.id == int(data['id'])).first()
        if worker:
            worker.FIO = data['FIO']
            worker.location = data['location']
            worker.grade = data['grade']
        else:
            new_worker = Worker(**data)
            db.session.add(new_worker)
        db.session.commit()  
        return jsonify({'message': 'Данные сотрудников успешно обновлены'})
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка при обновлении данных сотрудников'}), 500


@blueprint.route('/add_workers', methods=['GET', 'POST'])
@login_required
def add():
    username = session.get('username')
    user_role = request.form.get('role')
    FIO = session.get('FIO')
    location = request.form.get('location')
    grade=request.form.get('grade')
    user = Worker.query.filter_by(FIO=FIO).first()
    if user:
        return render_template('accounts/register.html',
                                   msg='ФИО уже существует',
                                   success=False,
                                 username=username, role=user_role)
    user = Users(**request.form)
    db.session.add(user)
    db.session.commit()

    return render_template('home/add_workers.html',
                               msg='Аккаунт успешно создан',
                               success=True,
                                username=username, role=user_role)


#Удаление сотрудников из таблицы workers
@blueprint.route('/delete_worker/<id>', methods=['POST'])
@login_required
def delete_worker(username):
    try:
        row_to_delete = db.session.query(Users).filter(Users.username == username).first()
        print(row_to_delete)
        if  row_to_delete:
            print(row_to_delete)
            db.session.delete(row_to_delete)
            db.session.commit()  # Сохранить изменения
            db.session.execute("VACUUM")
            return jsonify({'message': 'Пользователь успешно удален'})
        else:
            return jsonify({'error': 'Пользователь не найден'}), 404
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return jsonify({'error': 'Произошла ошибка при удалении пользователя'}), 500