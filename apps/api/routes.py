# -*- encoding: utf-8 -*-

from apps.api import blueprint
from flask import jsonify
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.api.function_api import get_schedule_for_worker_on_day, get_schedule_for_worker_on_interval, save_task_сompleted
from datetime import datetime


@blueprint.route('/authorization')
@login_required                                         # Это тут нужно?
def authorization():                                    # Коля, это к тебе, и чекни коммент к последнему обработчику


    data = {'ТУТ': 'ПОКА', 'НЕ': 'ГОТОВО'}

    return jsonify(data)

@blueprint.route('/schedule_worker_on_day', methods=['POST'])
def schedule_on_day():
    try:
        data = request.get_json()  # data = {"date": "2023_11_08", "worker_id": 1}
        date = data["date"]
        worker_id = data["worker_id"]
        schedule = get_schedule_for_worker_on_day(date, worker_id)
        if schedule:
            return jsonify(schedule)
        else:
            return jsonify({'error': 'Расписание не найдено'}), 404
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка при получении расписания'}), 500

@blueprint.route('/schedule_worker_on_interval', methods=['POST'])
def schedule_on_interval():
    try:
        data = request.get_json()  # data = {"start_date": "2023_11_01", "end_date": "2023_11_10", "worker_id": 1}
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        worker_id = data.get("worker_id")

        start_date = datetime.strptime(start_date_str, "%Y_%m_%d")
        end_date = datetime.strptime(end_date_str, "%Y_%m_%d")

        schedule_data = get_schedule_for_worker_on_interval(start_date, end_date, worker_id)

        if schedule_data:
            return jsonify(schedule_data)
        else:
            return jsonify({'error': 'Расписание не найдено'}), 404
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка при получении расписания'}), 500

@blueprint.route('/statistic', methods=['POST'])
def statistic():


    data = {'ТУТ': 'ПОКА', 'НЕ': 'ГОТОВО'}

    return jsonify(data)

@blueprint.route('/task_сompleted', methods=['POST'])
def task_сompleted():
    data = request.get_json()   # data = {"task_idt": "305620464419692773492314257386895579457"}
    try:
        idt = data.get("task_idt")
        if save_task_сompleted(idt):
            return jsonify({'message': 'Результат сохранен'})
        else:
            return jsonify({'error': 'Ошибка сохранения результата в БД'}), 404
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка при сохранении результата'}), 500


@blueprint.route('/task_notification', methods=['POST'])                        # Скорее всего надо реализовать не тут
def task_notification():                                                        # (или как-то передавать потом на веб)


    data = {'ТУТ': 'ПОКА', 'НЕ': 'ГОТОВО'}

    return jsonify(data)

@blueprint.route('/user_information', methods=['POST'])                         # Скорее всего надо отправлять во время
def user_information():                                                         # авторизации во время авторизации


    data = {'ТУТ': 'ПОКА', 'НЕ': 'ГОТОВО'}

    return jsonify(data)
