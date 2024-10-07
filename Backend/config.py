import os
from celery.schedules import crontab

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'SecretKey@')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Celery Configuration
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_ROUTES = {
        'main.check_and_send_reminders': {'queue': 'default'},
        'main.generate_monthly_report': {'queue': 'default'},
        'main.generate_csv_task': {'queue': 'default'},
        'main.send_email_notification': {'queue': 'default'},
        'main.export_books_to_csv': {'queue': 'default'},
    }
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60  

    CELERY_BEAT_SCHEDULE = {
        'daily-reminder': {
            'task': 'main.check_and_send_reminders',
            'schedule': crontab(hour=18, minute=0)  # every day at 6 PM
        },
        'monthly-report': {
            'task': 'main.generate_monthly_report',
            'schedule': crontab(day_of_month=1, hour=0, minute=0)  # 1st of every month at midnight
        }
    }

    # Brevo SMTP Configuration
    SMTP_SERVER_HOST = 'smtp-relay.brevo.com'
    SMTP_SERVER_PORT = 587
    SENDER_EMAIL='urjaswibanerjee@gmail.com'
    SENDER_PASSWORD='YourPassHere'


    # Cache Configuration
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 3
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Brevo API Key
    BREVO_API_KEY = os.getenv('BREVO_API_KEY', 'Your-Api-Key')
