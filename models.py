from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)  # 'student' or 'teacher'
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(50), nullable=True)  # Only for students
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student_subjects = db.relationship('StudentSubject', backref='student', lazy=True, cascade='all, delete-orphan')
    teacher_subjects = db.relationship('TeacherSubject', backref='teacher', lazy=True, cascade='all, delete-orphan')
    submitted_queries = db.relationship('Query', foreign_keys='Query.student_id', backref='student', lazy=True)
    received_queries = db.relationship('Query', foreign_keys='Query.teacher_id', backref='teacher', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_student(self):
        return self.role == 'student'
    
    def is_teacher(self):
        return self.role == 'teacher'

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    
    # Relationships
    student_subjects = db.relationship('StudentSubject', backref='subject', lazy=True, cascade='all, delete-orphan')
    teacher_subjects = db.relationship('TeacherSubject', backref='subject', lazy=True, cascade='all, delete-orphan')
    queries = db.relationship('Query', backref='subject', lazy=True)

class StudentSubject(db.Model):
    __tablename__ = 'student_subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('student_id', 'subject_id', name='unique_student_subject'),)

class TeacherSubject(db.Model):
    __tablename__ = 'teacher_subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('teacher_id', 'subject_id', name='unique_teacher_subject'),)

class Query(db.Model):
    __tablename__ = 'queries'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    reply = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending', nullable=False)  # 'pending' or 'answered'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def is_pending(self):
        return self.status == 'pending'
    
    def is_answered(self):
        return self.status == 'answered'
