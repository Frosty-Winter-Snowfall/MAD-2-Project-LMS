from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,func
from datetime import datetime,timedelta
from flask import Flask



db=SQLAlchemy()


# models

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))


class Consumer(db.Model):
    __tablename__ = 'user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    fname=db.Column(db.String(200),nullable=False)
    lname=db.Column(db.String(200),nullable=False)
    username=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)
    active = db.Column(db.Boolean())
    borrowed_books = db.relationship('BorrowHistory', backref='consumer', lazy=True, cascade='all, delete-orphan')
    notification = db.relationship('Notification', backref='consumer', lazy=True, cascade='all, delete-orphan')
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))

class BorrowHistory(db.Model):
    __tablename__ = 'borrow_history'
    bbid = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    book_name = db.Column(db.String(200), nullable=False)
    date_issued = db.Column(db.DateTime, default=datetime.now)
    is_approved = db.Column(db.Boolean, default=False)
    return_date = db.Column(db.DateTime)
    def __init__(self, id, filename,book_id, book_name, is_approved, date_issued, return_date):
        self.id = id
        self.filename=filename
        self.book_name=book_name
        self.book_id = book_id
        self.is_approved = is_approved
        self.date_issued = date_issued
        self.return_date =return_date

class Notification(db.Model):
    __tablename__ = 'notification'
    nid = db.Column(db.Integer, primary_key=True, unique=True)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    filename = db.Column(db.String(200), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=True)
    consumer_name = db.Column(db.String(200), nullable=False)
    book_name = db.Column(db.String(200), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    date_issued = db.Column(db.DateTime, default=datetime.now)
    return_date = db.Column(db.DateTime, nullable=False)
    is_returned = db.Column(db.Boolean, default=False)
    returned_date = db.Column(db.DateTime, nullable=True)
    feedback_content = db.Column(db.Text, nullable=True)
    def __init__(self, id, filename, consumer_name, book_id, book_name, is_approved, date_issued, return_date,is_returned=False, returned_date=None,feedback_content=None):
        self.id = id
        self.filename = filename
        self.consumer_name = consumer_name
        self.book_id = book_id
        self.book_name = book_name
        self.is_approved = is_approved
        self.date_issued = date_issued
        self.return_date = return_date
        self.is_returned = is_returned
        self.returned_date=returned_date
        self.feedback_content=feedback_content

class Section(db.Model):
    __tablename__ = 'section'
    sid=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    section_name = db.Column(db.String(200), nullable=False, unique=True)
    books = db.relationship('Book', backref='section', lazy=True)
    date_created=db.Column(db.DateTime, default=datetime.now)
    description=db.Column(db.String(200))
    def __init__(self,section_name,description,date_created=None):
        self.section_name=section_name
        self.description=description 
        self.date_created=date_created or datetime.now()

class Book(db.Model):
    __tablename__ = 'book'
    book_id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    filename=db.Column(db.String(200),nullable=False)
    book_name=db.Column(db.String(200),nullable=False,unique=True)
    book_content=db.Column(db.String(200))
    book_author=db.Column(db.String(200),nullable=False)
    date_issued=db.Column(db.DateTime, default=datetime.now)
    return_date = db.Column(db.DateTime)
    section_id = db.Column(db.Integer, db.ForeignKey('section.sid'), nullable=True)
    borrow_history = db.relationship('BorrowHistory', backref='book', lazy='dynamic',cascade='all, delete-orphan')
    notification = db.relationship('Notification', backref='book', lazy='dynamic',cascade='all, delete-orphan')
    def __init__(self,filename,book_name, book_content,book_author, section_id=None):
        self.filename=filename
        self.book_name = book_name
        self.book_content = book_content
        self.book_author = book_author
        self.date_issued = datetime.now()   
        self.return_date = datetime.now() + timedelta(days=7)
        self.section_id = section_id
    def to_dict(self):
        return {
            'book_name': self.book_name,
            'content': self.book_content,
            'author': self.book_author,
            'date_issued': self.date_issued,
            'return_date': self.return_date
        }
