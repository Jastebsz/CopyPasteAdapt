# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask import session,Blueprint
#from apps.authentication.models import Users
from geopy.geocoders import Nominatim
from apps import db
from apps.home.models import Worker,Users,Full_tasks,Schedule,Points,Tasks
from apps.home.function import line_tasks, distribute_tasks, delete_last_two_schedule
from flask import request, jsonify
# line_tasks()                          # создание очереди
# distribute_tasks()                    # распределение задач
# delete_last_two_schedule()            # удаление лишних расписаний
# TODO: для blueprint задач доавить всязь двух таблиц(установление юзера по задачам)
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
    username,user_role=role() 
    try:
        if not template.endswith('.html'):
            template += '.html'
        segment = get_segment(request)
        if template == 'tables.html':
            workers=Worker.query.all()[:3]
            users=Users.query.all()[:3]
            points=Points.query.all()[:3]
            return render_template("home/" + template, segment=segment, username=username, role=user_role, workers=workers,users=users,points=points)
        if template == 'workers.html':
            workers=Worker.query.all()
            return render_template("home/" + template, segment=segment, username=username, role=user_role, workers=workers)
        if template == 'users.html':
            users=Users.query.all()
            for user in users:
                user.password='***'
            return render_template("home/" + template, segment=segment, username=username, role=user_role, users=users)
        if template == 'points.html':
            points=Points.query.all()
            return render_template("home/" + template, segment=segment, username=username, role=user_role, points=points)
        if template == 'billing.html':
            tasks=Tasks.query.all()
            # TODO Здесь необходимо связать таблицы Full_tasks и Worker и подать странице новую БД( строки в html, под них форматировать не обязательно: ID,ФИО,task_title,task_priority,point_address,date,status)
            #return render_template("home/" + template, segment=segment, username=username, role=user_role, tasks=tasks,full_tasks=full_tasks)
            return render_template("home/" + template, segment=segment, username=username, role=user_role,tasks=tasks)
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
        worker_id = int(data['id'])  # Преобразуем ID в целое число
        worker = db.session.query(Worker).filter(Worker.id == worker_id).first()
        if worker:
            print(data['id'])
            worker.FIO = data['FIO']
            print(worker.FIO)
            worker.location = data['location']
            worker.grade = data['grade']
        else:
            new_worker = Worker(**data)
            db.session.add(new_worker)
        db.session.commit()  
        return jsonify({'message': 'Данные сотрудников успешно обновлены'})
    except Exception as e:
        print(str(e))  # Добавим вывод ошибки в консоль
        return jsonify({'error': 'Произошла ошибка при обновлении данных сотрудников'}), 500


    
    
@blueprint.route('/delete_worker/<id>', methods=['POST'])
@login_required
def delete_worker(id):
    try:
        row_to_delete = db.session.query(Worker).filter(Worker.id == id).first()
        print(1)
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

# @blueprint.route('/add_workers', methods=['GET', 'POST'])
# @login_required
# def add():
#     username = session.get('username')
#     user_role = request.form.get('role')
#     FIO = session.get('FIO')
#     location = request.form.get('location')
#     grade=request.form.get('grade')
#     user = Worker.query.filter_by(FIO=FIO).first()
#     if user:
#         return render_template('accounts/register.html',
#                                    msg='ФИО уже существует',
#                                    success=False,
#                                  username=username, role=user_role)
#     user = Users(**request.form)
#     db.session.add(user)
#     db.session.commit()

#     return render_template('home/add_workers.html',
#                                msg='Аккаунт успешно создан',
#                                success=True,
#                                 username=username, role=user_role)


#Удаление сотрудников из таблицы points
@blueprint.route('/delete_points/<id>', methods=['POST'])
@login_required
def delete_points(id):
    try:
        row_to_delete = db.session.query(Points).filter(Points.id == id).first()
        print(1)
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
    
    
    #Добавление/изменение сотрудников в таблице points
@blueprint.route('/update_points/<id>', methods=['POST'])
@login_required
def update_points(id):
    try:
        data = request.json 
        print(data)
        print(data['id'])
        point = db.session.query(Points).filter(Points.id == int(data['id'])).first()
        if point:
            point.address= data['address']
            point.connected= data['connected']
            point.delivered= bool(data['delivered'])
            point.days_last_card= data['days_last_card']
            point.num_approved_app= data['num_approved_app']
            point.num_card= data['num_card']
        else:
            new_point = Points(**data)
            db.session.add(new_point)
        db.session.commit()  
        return jsonify({'message': 'Данные  успешно обновлены'})
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return jsonify({'error': 'Произошла ошибка при обновлении'}), 500
    