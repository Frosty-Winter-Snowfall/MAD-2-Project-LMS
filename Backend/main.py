from flask import Flask,request,render_template,redirect,url_for,send_from_directory,current_app, request,session,jsonify,send_file
from flask_restful import Api,Resource,abort,reqparse,marshal_with,fields
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Consumer,Role,Book,Section,Notification,BorrowHistory,Role,RolesUsers
from sqlalchemy import or_,func
from datetime import datetime,timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.orm import Session
import os
from config import Config
from models import db
from flask_caching import Cache
from flask_mail import Mail,Message
from tasks import make_celery
from celery import Celery
from celery.result import AsyncResult
from celery.schedules import crontab, timedelta
import time
import pdfkit
import csv


UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app=Flask(__name__)
app.secret_key = 'SecretKey'
app.config['SESSION_TYPE'] = 'redis'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config.from_object(Config)
# flask_cors-4.0.1 flask-security-3.0.0 
CORS(app)
api=Api(app)


# Function to create roles
def create_roles_and_admin():
    if not Role.query.filter_by(name='admin').first():
        admin_role = Role(name='admin', description='Administrator role')
        db.session.add(admin_role)
    if not Role.query.filter_by(name='user').first():
        user_role = Role(name='user', description='Regular user role')
        db.session.add(user_role)
    db.session.commit()
    admin = {
        'fname': 'L',
        'lname': 'Lawliet',
        'username': 'Future_Winter',
        'password': '1234'
    }
    if not Consumer.query.filter_by(username=admin['username']).first():
        admin_user = Consumer(
            fname=admin['fname'],
            lname=admin['lname'],
            username=admin['username'],
            password=generate_password_hash(admin['password'])
        )
        admin_role = Role.query.filter_by(name='admin').first()
        admin_user.roles.append(admin_role)
        db.session.add(admin_user)
        db.session.commit()
        print('Admin user created or already exists')

celery = make_celery(app)
cache = Cache(app)


db.init_app(app)
with app.app_context():
    db.create_all()
    create_roles_and_admin()




# celery

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from config import Config 
import base64
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from config import Config  

# Configure API key authorization
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = Config.BREVO_API_KEY
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def send_email(subject, html_content, to_address=None, receiver_username=None, attachment=None, filename=None):
    sender = {"name": "Name", "email": Config.SENDER_EMAIL}
    if to_address:
        to = [{"email": "email@gmail.com", "name": "Name"},
              {"email": to_address, "name": receiver_username}]
    else:
        to = [{"email": "name@gmail.com", "name": "name"}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)
    attachments = []
    if attachment and filename:
        attachments.append({
            "content": base64.b64encode(attachment.getvalue()).decode('utf-8'),
            "name": filename
        })
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        html_content=html_content,
        sender=sender, 
        subject=subject,
        attachment=attachments  
    )
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Email sent successfully")
        return {"message": "Email sent successfully!"}
    except ApiException as e:
        print(f"Exception when calling SMTPApi->send_transac_email: {e}\n")
        return {"message": "Failed to send email.", "error": str(e)}


@celery.task
def send_reminder(user_id):
    logger.info(f"Sending reminder to user with ID: {user_id}")
    user = Consumer.query.get(user_id)
    if user:
        send_email(
        address="name2@gmail.com",
                      subject="This is a reminder to return your book.")
    return f"Reminder sent to user {user_id}."

@celery.task
def check_and_send_reminders():
    today = datetime.now()
    upcoming_return_date = today + timedelta(days=1)
    notifications_to_remind = Notification.query.filter(
        Notification.return_date >= today,
        Notification.return_date <= upcoming_return_date,
        Notification.is_returned == False  
    ).all()
    for reminder in notifications_to_remind:
        send_email(
            subject="Reminder",
            html_content=f"Reminder for: {reminder.message}",
            to_address=reminder.user.username,
            receiver_username=reminder.user.username
        )
        print(f"Reminder sent to {reminder.user.username} for {reminder.message}")
    return "Reminders sent."

@celery.task
def generate_monthly_report():
    statistics = {
        'total_users': db.session.query(db.func.count(Consumer.id)).scalar(),
        'total_books': db.session.query(db.func.count(Book.book_id)).scalar(),
        'total_borrowed_books': db.session.query(db.func.count(BorrowHistory.bbid)).scalar(),
        'notification_pending': db.session.query(db.func.count(Notification.nid)).filter_by(is_approved=False).scalar(),
        'all_sections': db.session.query(db.func.count(Section.sid)).scalar(),
        'active_users': db.session.query(db.func.count(Consumer.id)).filter_by(active=True).scalar()
    }
    csv_output = io.StringIO()
    csv_writer = csv.writer(csv_output)
    csv_writer.writerow(['Statistic', 'Value'])
    for key, value in statistics.items():
        csv_writer.writerow([key, value])
    csv_output.seek(0)
    csv_attachment = io.BytesIO(csv_output.getvalue().encode('utf-8'))
    send_email(
        subject="Monthly Activity Report",
        html_content="Please find the monthly report attached.",
        to_address="name2@gmail.com",
        attachment=csv_attachment,
        filename="monthly_report.csv"
    )
    return "Monthly report generated and sent."

@celery.task
def generate_csv_task():
    data = BorrowHistory.query.all()
    filepath = 'static/export.csv'
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Content', 'Author', 'Date Issued', 'Return Date'])
        for item in data:
            writer.writerow([item.book_name, item.filename, item.book.book_author, item.date_issued, item.return_date])
    print("CSV export completed, now sending email")
    with open(filepath, 'rb') as f:
        csv_attachment = io.BytesIO(f.read())
    send_email(
        subject="CSV Report",
        html_content="Please find the CSV report attached.",
        to_address="name2@gmail.com",
        attachment=csv_attachment,
        filename="export.csv"
    )
    return f'Export completed, CSV file saved as {filepath}.'


# Define periodic tasks
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        timedelta(seconds=60),
        check_and_send_reminders.s(),  
        name='send_reminder_every_10_seconds',
    )
    sender.add_periodic_task(
        crontab(hour=17, minute=0),
        check_and_send_reminders.s(), 
        name='send_reminder_at_5pm',
    )

# Define routes
@app.route("/trigger_check_and_send_reminders")
def trigger_check_and_send_reminders():
    task = check_and_send_reminders.delay()
    return jsonify({"Task_id": task.id})

@app.route("/trigger_monthly_report")
def trigger_monthly_report():
    task = generate_monthly_report.delay()
    return jsonify({"Task_id": task.id})

@app.route("/trigger_generate_csv_task")
def trigger_generate_csv_task():
    task = generate_csv_task.delay()
    return jsonify({"Task_id": task.id})

@app.route("/status/<task_id>")
def check_status(task_id):
    res = AsyncResult(task_id, app=celery)
    return {
        "Task_id": res.id,
        "Task_state": res.state,
        "Task_result": res.result
    }

@app.route("/download_file")
def download_file():
    return send_file('static/export.csv')

@app.route("/download_monthly_report")
def download_monthly_report():
    return send_file('static/monthly_report.pdf')


# lib celery

import io
import traceback

@celery.task
def send_email_notification(csv_filename):
    with app.app_context():
        try:
            subject = "CSV Export Completed"
            html_content = f"Your CSV export has been completed. Find the file attached: {csv_filename}."
            to_address = "name@gmail.com"
            receiver_username = "name"
            with open(csv_filename, 'rb') as file:
                attachment = io.BytesIO(file.read())
                send_email(
                    subject=subject,
                    html_content=html_content,
                    to_address=to_address,
                    receiver_username=receiver_username,
                    attachment=attachment,
                    filename=csv_filename
                )
            print(f"Email sent with attachment: {csv_filename}")
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise

@celery.task
def export_books_to_csv():
    logger.info("Starting CSV export task")
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Book Name', 'Content', 'Author', 'Date Issued', 'Return Date'])
    books = Book.query.all()
    for book in books:
        writer.writerow([
            book.book_name,
            book.book_content,
            book.book_author,
            book.date_issued,
            book.return_date
        ])
    csv_data = output.getvalue()
    output.close()
    csv_filename = 'exported_books.csv'
    with open(csv_filename, 'w') as f:
        f.write(csv_data)
    logger.info("CSV export completed, now sending email")
    send_email_notification.delay(csv_filename)
    return f'Export completed, CSV file saved as {csv_filename}.'


@app.route('/trigger_csv_export', methods=['POST'])
def trigger_csv_export():
    export_books_to_csv.delay() 
    return jsonify({"message": "CSV export has been triggered."}), 202


# api

api=Api(prefix='/api')

admin={
    'id':'1','fname':'L','lname':'Lawliet',
    'username':'Future_winter','password':'1234'
}


class UserAPI(Resource):
    def get(self, id=None):
        if id:
            user = Consumer.query.get(id)
            if user:
                return jsonify({
                    'id': user.id,
                    'fname': user.fname,
                    'lname': user.lname,
                    'username': user.username,
                    'active': user.active,
                    'roles':[role.name for role in user.roles]
                })
            return jsonify({'error': 'User not found'}), 404
        else:
            users = Consumer.query.all()
            return jsonify([{
                'id': user.id,
                'fname': user.fname,
                'lname': user.lname,
                'username': user.username,
                'active': user.active,
                'roles':[role.name for role in user.roles]
            } for user in users])
    
    def post(self,id=None):
            data = request.get_json()
            fname = data.get('fname')
            lname = data.get('lname')
            username = data.get('username')
            password = data.get('password')
            if None not in (fname, lname, username, password):
                user = Consumer.query.filter_by(username=username).first()
                if user is None:
                    new_user = Consumer(fname=fname, lname=lname, username=username, password=password)
                    user_role = Role.query.filter_by(name='user').first()
                    new_user.roles.append(user_role)
                    db.session.add(new_user)
                    db.session.commit()
                    return jsonify({'message': 'Consumer added successfully'})
                else:
                    return jsonify({'error': 'Username already exists'}), 400
            else:
                return jsonify({'error': 'Please provide all required fields'}), 400
    
    def put(self,id):
        consumer = Consumer.query.get(id)
        if consumer:
            data = request.get_json()
            consumer.fname = data.get('fname', consumer.fname)
            consumer.lname = data.get('lname', consumer.lname)
            consumer.username = data.get('username', consumer.username)
            password = data.get('password')
            if password:
                consumer.password = password
            db.session.commit()
            return jsonify({'message': 'Consumer updated successfully'})
        else:
            return jsonify({'error': 'Consumer not found'}), 404

    def delete(self,id):
         consumer = Consumer.query.get(id)
         if consumer:
            db.session.delete(consumer)
            db.session.commit()
            return jsonify({'message': 'Consumer deleted successfully'})
         else:
            return jsonify({'error': 'Consumer not found'}), 404


class BookAPI(Resource):
    def get(self, id=None):
        if id:
            book = Book.query.get(id)
            if book:
                return jsonify({
                    'id': book.book_id,
                    'name': book.book_name,
                    'content': book.book_content,
                    'author': book.book_author,
                    'section_id': book.section_id,
                    'date_issued': book.date_issued,
                    'return_date': book.return_date
                })
            return jsonify({'error': 'Book not found'}), 404
        else:
            book = Book.query.all()
            return jsonify([{
                'id': book.book_id,
                'name': book.book_name,
                'content': book.book_content,
                'author': book.book_author,
                'section_id': book.section_id,
                'date_issued': book.date_issued,
                'return_date': book.return_date
            } for book in book])
    
    def post(self):
        data = request.get_json()
        name = data.get('name')
        content = data.get('content')
        author = data.get('author')
        section_id = data.get('section_id')
        filename = data.get('filename')
        if None not in (name, content, author, filename):
            new_book = Book(book_name=name, book_content=content, book_author=author, section_id=section_id, filename=filename)
            db.session.add(new_book)
            db.session.commit()
            return jsonify({'message': 'Book added successfully'})
        else:
            return jsonify({'error': 'Please provide all required fields'}), 400
    
    def put(self, id):
        book = Book.query.get(id)
        if book:
            data = request.get_json()
            book.book_name = data.get('name', book.book_name)
            book.book_content = data.get('content', book.book_content)
            book.book_author = data.get('author', book.book_author)
            book.section_id = data.get('section_id', book.section_id)
            db.session.commit()
            return jsonify({'message': 'Book updated successfully'})
        else:
            return jsonify({'error': 'Book not found'}), 404
    
    def delete(self, id):
        book = Book.query.get(id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify({'message': 'Book deleted successfully'})
        else:
            return jsonify({'error': 'Book not found'}), 404


class SectionAPI(Resource):
    def get(self, id=None):
        if id:
            section = Section.query.get(id)
            if section:
                return jsonify({
                    'id': section.sid,
                    'name': section.section_name,
                    'description': section.description,
                    'date_created': section.date_created,
                    'book_count': len(section.books)
                })
            return jsonify({'error': 'Section not found'}), 404
        else:
            sections = Section.query.all()
            return jsonify([{
                'id': section.sid,
                'name': section.section_name,
                'description': section.description,
                'date_created': section.date_created,
                'book_count': len(section.books)
            } for section in sections])
    
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        if None not in (name, description):
            new_section = Section(section_name=name, description=description)
            db.session.add(new_section)
            db.session.commit()
            return jsonify({'message': 'Section added successfully'})
        else:
            return jsonify({'error': 'Please provide all required fields'}), 400
    
    def put(self, id):
        section = Section.query.get(id)
        if section:
            data = request.get_json()
            section.section_name = data.get('name', section.section_name)
            section.description = data.get('description', section.description)
            db.session.commit()
            return jsonify({'message': 'Section updated successfully'})
        else:
            return jsonify({'error': 'Section not found'}), 404
    
    def delete(self, id):
        section = Section.query.get(id)
        if section:
            db.session.delete(section)
            db.session.commit()
            return jsonify({'message': 'Section deleted successfully'})
        else:
            return jsonify({'error': 'Section not found'}), 404


# user login/signup

@app.route('/usersignup', methods=['POST'])
def signup():
        data = request.get_json()
    
        fname = data.get('fname')
        lname = data.get('lname')
        username = data.get('username')
        password = data.get('password')
        if None in (fname, lname, username, password):
            raise ValueError("Please provide all required fields")

        user = Consumer.query.filter_by(username=username).first()
        if user:
            raise ValueError("Username already exists")
        hashed_password = generate_password_hash(password)
        new_user = Consumer(fname=fname, lname=lname, username=username, password=hashed_password)
        user_role = Role.query.filter_by(name='user').first()
        new_user.roles.append(user_role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Consumer added successfully'}), 201
        

@app.route('/userlogin',methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if None in (username, password):
        return jsonify({'error': 'Please provide both username and password'}), 400

    user = Consumer.query.filter_by(username=username).first()
    if user and check_password_hash(user.password,password):
        session['user_id'] = user.id
        user.active = True
        db.session.commit()
        return jsonify({'id': user.id,'username':user.username ,'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401



# librarian login
@app.route('/llogin',methods=['POST'])
def llogin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if None in (username, password):
        return jsonify({'error': 'Please provide both username and password'}), 400
    user = Consumer.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        librarian_role = Role.query.filter_by(name='admin').first()
        if librarian_role and librarian_role in user.roles:
            user.active = True
            db.session.commit()
            return jsonify({'id': user.id, 'username': user.username, 'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'User does not have librarian privileges'}), 403
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


# get links

@app.route('/books', methods=['GET'])
@cache.cached(timeout=5)
def get_books():
    books = Book.query.all()
    books_list = [{
        'id': book.book_id,
        'name': book.book_name,
        'content': book.book_content,
        'author': book.book_author,
    } for book in books]
    return jsonify(books_list), 200

@app.route('/sections', methods=['GET'])
@cache.cached(timeout=5)
def get_sections():
    sections = Section.query.all()
    sections_list = [{
        'id': section.sid,
        'name': section.section_name,
        'book_count': len(section.books),
        'books': [{'name': book.book_name, 'author': book.book_author} for book in section.books]
    } for section in sections]
    return jsonify(sections_list), 200

@app.route('/section', methods=['GET'])
@cache.cached(timeout=5)
def get_section():
    sections = Section.query.all()
    sections_list = [{
        'id': section.sid,
        'name': section.section_name } for section in sections]
    return jsonify(sections_list), 200

@app.route('/books_in_section/<int:section_id>', methods=['GET'])
@cache.cached(timeout=5)
def get_books_in_section(section_id):
    books = Book.query.filter_by(section_id=section_id).all()
    books_list = [{'book_id': book.book_id, 'book_name': book.book_name} for book in books]
    return jsonify(books_list)

@app.route('/users', methods=['GET'])
@cache.cached(timeout=5)
def get_users():
    user_role = Role.query.filter_by(name='user').first()
    if not user_role:
        return jsonify({'message': 'Role not found.'}), 404
    users = Consumer.query.join(RolesUsers, RolesUsers.user_id == Consumer.id)\
                          .filter(RolesUsers.role_id == user_role.id).all()
    users_list = [{
        'id': user.id,
        'name': user.username,
        'active': user.active
    } for user in users]
    return jsonify(users_list)

@app.route('/borrow_requests', methods=['GET'])
@cache.cached(timeout=5)
def get_borrow_requests():
    borrow_requests = BorrowHistory.query.filter_by(is_approved=False).all()
    requests_list = [{
        'request_id': req.bbid,
        'consumer_id': req.id,
        'book_id': req.book_id,
        'book_name': req.book_name,
        'date_issued': req.date_issued,
        'return_date': req.return_date
    } for req in borrow_requests]
    return jsonify(requests_list)

# books handling
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/addbooks', methods=['POST'])
def addbooks():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        book_name = request.form.get('name')
        book_author = request.form.get('author')
        book_content = request.form.get('content')
        if None not in (filename,book_name,book_content,book_author):
            booki = Book.query.filter_by(filename=file.filename).first()
            if booki is None:
                    newbook=Book(filename=filename,book_name=book_name,book_content=book_content,book_author=book_author)
                    db.session.add(newbook)
                    db.session.commit()
                    return jsonify({"message": "Book uploaded successfully"}), 200        
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/editbook/<int:book_id>', methods=['POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    book_name = request.form.get('book_name')
    book_author = request.form.get('book_author')
    book_content = request.form.get('book_content')
    file = request.files.get('file')

    if book_name:
        book.book_name = book_name
    if book_author:
        book.book_author = book_author
    if book_content:
        book.book_content = book_content
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], book.filename)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)
        book.filename = filename

    db.session.commit()
    return jsonify({'message': 'Book edited successfully'}), 200

@app.route('/deletebook/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if book.filename:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], book.filename))
        except OSError:
            pass 
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully!'}), 200
    return jsonify({'message': 'Book not found.'}), 404


# section handling

@app.route('/addsections', methods=['POST'])
def addsections():
        section_name = request.form.get('name')
        section_content = request.form.get('content')
        if not section_name or not section_content:
            return jsonify({"error": "Missing section name or content"}), 400
        
        secti = Section.query.filter_by(section_name=section_name).first()
        if secti is None:
                new_section = Section(section_name=section_name, description=section_content)
                db.session.add(new_section)
                db.session.commit()
                return jsonify({"message": "Section uploaded successfully"}), 200
        else:
                return jsonify({"error": "Section already exists"}), 400
    
        
@app.route('/addbooktosection', methods=['POST'])
def add_book_to_section():
    book_id = request.form.get('book_id')
    section_id = request.form.get('section_id')
    
    if not all([book_id, section_id]):
        return jsonify({'error': 'Missing data'}), 400

    book = Book.query.get(book_id)
    section = Section.query.get(section_id)
    if not book or not section:
        return jsonify({'error': 'Book or Section not found'}), 404

    book.section_id = section_id
    db.session.commit()

    return jsonify({'message': 'Book added to section successfully'}), 201

@app.route('/removebookfromsection/<int:book_id>', methods=['DELETE'])
def remove_book_from_section(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    if book.section_id is not None:
        book.section_id = None
        db.session.commit()
        return jsonify({"message": "Book removed from section successfully"}), 200
    else:
        return jsonify({"message": "Book is not in any section"}), 400

@app.route('/editsections/<int:section_id>', methods=['POST'])
def edit_section(section_id):
    section = Section.query.get(section_id)
    if not section:
        return jsonify({'error': 'Section not found.'}), 404
    new_name = request.form.get('new_name')
    new_content = request.form.get('new_content')
    if new_name:
        section.section_name = new_name
    if new_content:
        section.description = new_content
    db.session.commit()
    return jsonify({'message': 'Section edited successfully!'}), 200


@app.route('/deletesection/<int:section_id>', methods=['POST'])
def delete_section(section_id):
    section = Section.query.filter_by(sid=section_id).first()
    if section:
        db.session.delete(section)
        db.session.commit()
        return jsonify({'message': 'Section deleted successfully!'}), 200
    return jsonify({'message': 'Section not found.'}), 404


# user handling

@app.route('/deleteuser/<int:id>', methods=['POST'])
def delete_user(id):
    user = Consumer.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User banned successfully!'}), 200
    return jsonify({'message': 'User not found.'}), 404


# book borrow


@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    print(f"Received book_id: {book_id}") 
    consumer_id = request.json.get('consumer_id')
    consumer_name = request.json.get('consumer_name')
    pending_request = BorrowHistory.query.filter_by(id=consumer_id, book_id=book_id, is_approved=False).first()
    if pending_request:
        return jsonify({'message': 'You already have a pending borrowing request for this book.'}), 400
    approved_borrowing = BorrowHistory.query.filter_by(id=consumer_id, book_id=book_id, is_approved=True).first()
    if approved_borrowing:
        return jsonify({'message': 'You have already borrowed this book.'}), 400
    borrowed_books_count = BorrowHistory.query.filter_by(id=consumer_id, is_approved=True).count()
    if borrowed_books_count >= 5:
        return jsonify({'message': 'You have already borrowed the maximum number of books.'}), 400
    book = Book.query.filter_by(book_id=book_id).first()
    if not book:
        return jsonify({'message': 'Book not found.'}), 404
    date_issued = datetime.now()
    return_date = date_issued + timedelta(days=7)
    borrow_history = BorrowHistory(
        id=consumer_id,
        book_id=book.book_id,
        filename=book.filename,
        book_name=book.book_name,
        is_approved=False,
        date_issued=date_issued,
        return_date=return_date
    )
    notification = Notification(
        id=consumer_id,
        book_id=book.book_id,
        filename=book.filename,
        book_name=book.book_name,
        consumer_name=consumer_name,
        is_approved=False,
        date_issued=date_issued,
        return_date=return_date
    )
    consumer = Consumer.query.filter_by(id=consumer_id).first()
    if consumer:
        consumer.active = True
        db.session.commit()
    else:
        return jsonify({'message': 'Consumer not found.'}), 404
    db.session.add(borrow_history)
    db.session.add(notification)
    db.session.commit()
    borrowed_books = BorrowHistory.query.filter_by(id=consumer_id).all()
    borrowed_books_list = [{
        'book_id': b.book_id,
        'book_name': b.book_name,
        'date_issued': b.date_issued,
        'return_date': b.return_date,
        'is_approved': b.is_approved
    } for b in borrowed_books]
    return jsonify({
        'message': 'Book borrowing request submitted successfully.',
        'borrowed_books': borrowed_books_list
    }), 200

@app.route('/mybooks/<int:user_id>', methods=['GET'])
@cache.cached(timeout=5)
def get_my_books(user_id):
    borrowed_books = Notification.query.filter_by(id=user_id, is_approved=True).all()
    if not borrowed_books:
        return jsonify({'message': 'No borrowed books found.'}), 404 
    borrowed_books_list = []
    for book in borrowed_books:
        borrowed_books_list.append({
            'nid':book.nid,
            'id':book.id,
            'book_id': book.book_id,
            'book_name': book.book_name,
            'filename':book.filename,
            'date_issued': book.date_issued,
            'return_date': book.return_date,
            'is_returned': book.is_returned,
            'is_approved':book.is_approved
        }) 
    return jsonify({
        'borrowed_books': borrowed_books_list
    }), 200

@app.route('/read_book/<int:nid>',methods=['GET'])
def read_book(nid):
    books_folder = UPLOAD_FOLDER
    book_path=[]
    notification = Notification.query.get(nid)
    if notification and notification.is_approved:
        if datetime.now() > notification.return_date:
            notification.is_returned = True
            notification.returned_date = datetime.now()
            notification.is_approved=False
            db.session.commit()
            print('book revoked')
            return jsonify({"msg": "Book revoked due to overdue"}), 403
        book_path = os.path.join(books_folder, notification.filename)
        print(book_path)
        return send_from_directory(books_folder, notification.filename)
    return jsonify({'message': 'Book not found'}), 404

@app.route('/return_book/<int:nid>', methods=['POST'])
def return_book(nid):
    notification = Notification.query.get(nid)
    if notification and notification.is_approved:
        notification.is_returned = True
        notification.returned_date = datetime.now()
        notification.is_approved = False
        db.session.commit()
        return jsonify({'message': 'Book returned successfully'}), 200
    return jsonify({'message': 'Unauthorized or book not found'}), 404



# feedback

@app.route('/feedback/<int:nid>', methods=['POST'])
def feedback(nid):
    notification = Notification.query.get(nid)
    if notification and notification.is_approved:
        feedback_content = request.json.get('feedback_content')
        notification.feedback_content = feedback_content
        db.session.commit()
        return jsonify({'message': 'Feedback submitted successfully'}), 200
    return jsonify({'message': 'Unauthorized or book not found'}), 404

@app.route('/seefeedback', methods=['GET'])
@cache.cached(timeout=5)
def seefeedback():
    feedbacks = Notification.query.filter(Notification.feedback_content.isnot(None)).all()
    feedback_list = [
        {
            'nid': feedback.nid,
            'consumer_name':feedback.consumer_name,
            'book_name': feedback.book_name,
            'feedback_content': feedback.feedback_content
        } 
        for feedback in feedbacks
    ]
    return jsonify(feedback_list)

@app.route('/deletefeedback/<int:nid>', methods=['DELETE'])
def deletefeedback(nid):
    notification = Notification.query.get(nid)
    if notification:
        notification.feedback_content = None
        db.session.commit()
        return jsonify({'message': 'Feedback deleted successfully'}), 200
    return jsonify({'message': 'Feedback not found'}), 404



# notification handling

@app.route('/notifications', methods=['GET'])
@cache.cached(timeout=5)
def get_notifications():
    notifications = Notification.query.filter_by(is_approved=False).all()
    notifications_list = [{
        'nid': notification.nid,
        'id': notification.id,
        'filename': notification.filename,
        'book_id': notification.book_id,
        'consumer_name': notification.consumer_name,
        'book_name': notification.book_name,
        'is_approved': notification.is_approved,
        'date_issued': notification.date_issued,
        'return_date': notification.return_date,
        'is_returned': notification.is_returned,
        'returned_date':notification.returned_date
    } for notification in notifications]
    return jsonify(notifications_list)

@app.route('/process_notification/<int:nid>', methods=['POST'])
def process_notification(nid):
    notification = Notification.query.filter_by(nid=nid).first()
    if notification:
        notification.is_approved = True
        borrow_history = BorrowHistory.query.filter_by(book_id=notification.book_id).first()
        if borrow_history:
            borrow_history.is_approved = True
        db.session.commit()
        return jsonify({'message': f'Notification {nid} approved successfully'}), 200
    return jsonify({'message': f'Notification {nid} not found'}), 404

@app.route('/ignore_notification/<int:nid>', methods=['POST'])
def ignore_notification(nid):
    notification = Notification.query.filter_by(nid=nid).first()
    if notification:
        borrow = BorrowHistory.query.filter_by(book_id=notification.book_id).first()
        db.session.delete(notification)
        if borrow:
            db.session.delete(borrow)
        db.session.commit()
        return jsonify({'message': f'Notification ignored successfully'}), 200
    return jsonify({'message': f'Notification not found'}), 404


# logout/del acc

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"msg": "Logged out successfully"}), 200

@app.route('/deleteaccount/<int:id>', methods=['POST'])
def delete_account(id):
        user = Consumer.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            session.pop('user_id', None)
            return jsonify({"msg": "Account deleted successfully"}), 200
        else:
            return jsonify({"msg": "User not found"}), 404
    
# stats

@app.route('/statistics')
@cache.cached(timeout=5)
def get_statistics():
    total_users = db.session.query(func.count(Consumer.id)).scalar()
    total_books = db.session.query(func.count(Book.book_id)).scalar()
    total_borrowed_books = db.session.query(func.count(BorrowHistory.bbid)).scalar()
    total_notifications = db.session.query(func.count(Notification.nid)).filter_by(is_approved=False).scalar()
    all_sections= db.session.query(func.count(Section.sid)).scalar()
    active_users = db.session.query(func.count(Consumer.id)).filter_by(active=True).scalar()

    statistics = {
        'total_users': total_users,
        'total_books': total_books,
        'total_borrowed_books': total_borrowed_books,
        'total_notifications': total_notifications,
        'all_sections': all_sections,
        'active_users': active_users,
    }
    
    return jsonify(statistics)

# add routes

api.add_resource(UserAPI, '/usersapi', '/usersapi/<int:id>')
api.add_resource(BookAPI, '/api/books')
api.add_resource(SectionAPI, '/api/sections')

if __name__=='__main__':
    app.run(debug=True)

        
       




