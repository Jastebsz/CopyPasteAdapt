from apps import db # Import the SQLAlchemy database instance


    

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