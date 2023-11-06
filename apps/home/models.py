from apps import db # Import the SQLAlchemy database instance
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

    

class Worker(db.Model):
    __tablename__ = 'Worker'

    id = db.Column(db.Integer, primary_key=True)
    FIO = db.Column(db.String(64), unique=True)
    location = db.Column(db.String(64))
    grade = db.Column(db.String(128))  # Store the hashed password as a string

    def __init__(self, FIO, location, grade):
        self.FIO = FIO
        self.location = location
        self.grade = grade
    def __repr__(self):
        return '<Worker {}>'.format(self.body)  
    
class Tasks(db.Model):
    __tablename__ = 'Tasks'
    type = db.Column(db.Integer, primary_key=True)                      # тип
    title = db.Column(db.String(100), nullable=False)                   # название
    priority = db.Column(db.String(30), nullable=False)                 # приоритет
    lead_time = db.Column(db.Float, nullable=False)                     # время
    condition = db.Column(db.String(120), nullable=False)               # условие
    level = db.Column(db.String(30), nullable=False) 

    def __init__(self,type, title, priority, lead_time,condition,level):
        self.type = type
        self.title = title
        self.priority = priority
        self.lead_time=lead_time
        self.condition=condition
        self.level = level
    def __repr__(self):
        return '<Tasks {}>'.format(self.body) 
class Points(db.Model):
    __tablename__ = 'Points'
    id = db.Column(db.Integer, primary_key=True)                        # номер точки
    address = db.Column(db.String(100), nullable=False)                 # адрес точки
    connected = db.Column(db.String(80), nullable=False)                # когда подключена точка
    delivered = db.Column(db.Boolean, default=False)                    # карты и материалы доставлены
    days_last_card = db.Column(db.Integer)                              # кол-во дней после выдачи последней карты
    num_approved_app = db.Column(db.Integer)                            # кол-во одобренных заявок
    num_card = db.Column(db.Integer)                                    # кол-во выданных карт
    def __init__(self, id, address, connected,delivered,days_last_card,num_approved_app,num_card):
        self.id = id
        self.address = address
        self.connected = connected
        self.delivered = delivered
        self.days_last_card = days_last_card
        self.num_approved_app = num_approved_app
        self.num_card=num_card
    def __repr__(self):
        return '<Points {}>'.format(self.body)     

class Full_tasks(db.Model):
    __tablename__ = 'Full_tasks'
    idt = db.Column(db.Integer, primary_key=True)                      # тип
    task_type = db.Column(db.String(100), nullable=False)                   # название
    task_title = db.Column(db.String(30), nullable=False)                 # приоритет
    task_priority = db.Column(db.Float, nullable=False)                     # время
    task_lead_time = db.Column(db.String(120), nullable=False)               # условие
    task_level = db.Column(db.String(30), nullable=False) 
    point_id=db.Column(db.String(30), nullable=False)
    point_address=db.Column(db.String(30), nullable=False)
    date=db.Column(db.String(30), nullable=False)
    status=db.Column(db.String(30), nullable=False)
    def __init__(self,idt, task_type, task_title, task_priority,task_lead_time,task_level,point_id,point_address):
        self.idt = idt                     
        self.task_type =task_type         
        self.task_title =task_title
        self.task_priority =task_priority                  
        self.task_lead_time =task_lead_time    
        self.task_level =task_level 
        self.point_id=point_id
        self.point_address=point_address

    def __repr__(self):
        return '<Full_tasks {}>'.format(self.body) 