from celery import Celery
from flask import Flask, render_template
from flask_mail import Message
from datetime import datetime, timedelta
import pdfkit
import csv
from flask_mail import Mail,Message
from config import Config  
from models import Consumer, Book, Section, Notification, BorrowHistory,db


def make_celery(app):
    celery = Celery(
        "main",
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=['main'],
        enable_utc=True,
        timezone="Asia/Kolkata"
    )
   

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.from_object(Config)
celery = make_celery(app)
