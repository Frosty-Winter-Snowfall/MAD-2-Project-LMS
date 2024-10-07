from main import app, celery

if __name__ == '__main__':
    with app.app_context():
        celery.worker_main(argv=['worker', '--loglevel=info'])
