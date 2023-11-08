
from apps import db


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)                        #
    FIO = db.Column(db.String(80), unique=True, nullable=False)         # фио
    location = db.Column(db.String(80), nullable=False)                 # адрес локации
    grade = db.Column(db.String(80), nullable=False)                    # грейд

class Tasks(db.Model):
    type = db.Column(db.Integer, primary_key=True)                      # тип
    title = db.Column(db.String(100), nullable=False)                   # название
    priority = db.Column(db.String(30), nullable=False)                 # приоритет
    lead_time = db.Column(db.Float, nullable=False)                     # время
    condition = db.Column(db.String(120), nullable=False)               # условие
    level = db.Column(db.String(30), nullable=False)                    # требуемый уровень сотрудника

class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)                        # номер точки
    address = db.Column(db.String(100), nullable=False)                 # адрес точки
    connected = db.Column(db.String(80), nullable=False)                # когда подключена точка
    delivered = db.Column(db.Boolean, default=False)                    # карты и материалы доставлены
    days_last_card = db.Column(db.Integer)                              # кол-во дней после выдачи последней карты
    num_approved_app = db.Column(db.Integer)                            # кол-во одобренных заявок
    num_card = db.Column(db.Integer)                                    # кол-во выданных карт

class Undistr_tasks(db.Model):
    idt = db.Column(db.String(100), primary_key=True)
    task_type = db.Column(db.Integer, nullable=False)                   # тип задачи
    task_title = db.Column(db.String(100), nullable=False)              # название задачи
    task_priority = db.Column(db.String(30), nullable=False)            # приоритет задачи
    task_lead_time = db.Column(db.Float, nullable=False)                # время выполнения задачи
    task_level = db.Column(db.String(30), nullable=False)               # требуемый уровень сотрудника для выполнения задачи
    point_id = db.Column(db.Integer, nullable=False)                    # номер точки
    point_address = db.Column(db.String(100), nullable=False)           # адрес точки
    date = db.Column(db.String(10), nullable=False)                     # дата создания задачи

class Full_tasks(db.Model):
    idt = db.Column(db.String(100), primary_key=True)
    task_type = db.Column(db.Integer, nullable=False)                   # тип задачи
    task_title = db.Column(db.String(100), nullable=False)              # название задачи
    task_priority = db.Column(db.String(30), nullable=False)            # приоритет задачи
    task_lead_time = db.Column(db.Float, nullable=False)                # время выполнения задачи + время в пути (если задача уже назначена)
    task_level = db.Column(db.String(30), nullable=False)               # требуемый уровень сотрудника для выполнения задачи
    point_id = db.Column(db.Integer, nullable=False)                    # номер точки
    point_address = db.Column(db.String(100), nullable=False)           # адрес точки
    date = db.Column(db.String(10), nullable=False)                     # дата создания задачи
    status = db.Column(db.String(10), nullable=False)                   # статус задачи ('finish' - завершена,
                                                                        # 'active' - в расписании сотрудника,
                                                                        # 'wait' - в очереди)

class Worker_last_location(db.Model):
    id = db.Column(db.Integer, primary_key=True)                        #
    last_location = db.Column(db.String(80), nullable=False)                 # адрес последней локации

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)  # дата в формате 'гггг_мм_дд'
    schedule = db.Column(db.LargeBinary, nullable=False)  # JSON данные как BLOB

    # Пример schedule {worker_id: {"schedule": {time_interval: IDT}}}
    # schedule = {
    #     "1": {"schedule": {"09:00 - 11:00": 1,
    #                        "11:30 - 14:00": 3,
    #                        "14:45 - 16:45": 2}
    #           },
    #     "2": {"schedule": {"09:00 - 10:00": 3,
    #                        "10:30 - 11:30": 3,
    #                        "12:30 - 14:30": 2,
    #                        "14:45 - 16:45": 1}
    #           },
    #     "3": {"schedule": {"09:00 - 11:00": 1,
    #                        "11:30 - 14:00": 3,
    #                        "14:45 - 16:45": 2}
    #           },
    #     "4": {"schedule": {"09:00 - 11:00": 1,
    #                        "11:30 - 14:00": 3,
    #                        "14:45 - 16:45": 2}
    #           },
    #     "5": {"schedule": {"09:00 - 11:00": 1,
    #                        "11:30 - 14:00": 3,
    #                        "14:45 - 16:45": 2}
    #           },
    #     "6": {"schedule": {"09:00 - 11:00": 1,
    #                        "11:30 - 14:00": 3,
    #                        "14:45 - 16:45": 2}
    #           },
    #     "7": {"schedule": {"09:00 - 11:00": 1,
    #                        "11:30 - 14:00": 3,
    #                        "14:45 - 16:45": 2}
    #           },
    #     "8": {"schedule": {"09:00 - 11:00": 1,
    #                        "11:30 - 14:00": 3,
    #                        "14:45 - 16:45": 2}
    #           }
    # }