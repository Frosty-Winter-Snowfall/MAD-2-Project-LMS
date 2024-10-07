# MAD-2-Project-LMS
This is MAD 2 project on Library Management System that i made in May 2024 term for my BS degree in Indian Institute Of Technology,Madras.It is an online library system taht manages ebooks.It has one admin that is created by default and can't be deleted  and any number of users.The admin holds maximum functionality and user can do basic ones.



# Modern Application Development II
## Project Statement
**Library Management System - V2**  
It's a multi-user app that is used to issue, grant/revoke, and maintain e-books across various sections like an online library.

---

## Frameworks to be used
- **SQLite** for data storage
- **Flask** for API
- **VueJS** for UI
- **VueJS Advanced with CLI** (only if required, not necessary)
- **Jinja2 templates** if required (Not to be used for UI)
- **Bootstrap** for HTML generation and styling (No other CSS framework is allowed)
- **Redis** for caching
- **Redis and Celery** for batch jobs

*Note: All demos should be possible on your local machine.*

---

## Roles
- **Librarian** - the maintainer of sections and e-books in the library
  - Can monitor all users and see all statistics.
  - Can create sections and e-books in the library.
  - Can grant/revoke access for an e-book.

- **General User** - an individual who wants to access an e-book from the library
  - Can browse all available sections and e-books in the library and request e-books.
  - Can request a maximum of 5 e-books at a time.
  - Can update their profile page and rate an e-book.

---

## Terminologies
- **Section**: All the e-books in the library can be classified in one or more sections (e.g., Philosophy, Science, Arts, etc.).
  - May have:
    - ID
    - Name
    - Date created
    - Description

- **E-book**: A digital format of content that can be viewed and rated and is accessible on any device that runs the web.
  - May have:
    - ID
    - Name
    - Content
    - Author(s)
    - Date issued
    - Return date

*Note: The above fields are not exhaustive; students can add more fields according to their requirements.*

---

## Application Wireframe
- **Library Management Wireframe**: *LIbrary_Management_Wireframe.png*

*Note: The wireframe is provided only to get the flow of the application and what should appear when a specific user navigates from one page to another. It is NOT mandatory to exactly replicate the views given in the wireframe. Students can work on their own frontend idea.*

---

## Core Functionalities
1. **Admin Login and User Login (RBAC)**  
   - A login/register form with fields like username, password, etc., for librarian and user.
   - The application should have only one librarian identified by their role.
   - Can use Flask security or JWT-based Token authentication to implement role-based access control.
   - Must have a suitable model to store and differentiate all types of users.

2. **Librarian Dashboard**  
   - Librarian should be added automatically whenever a new database is created.
   - Must display relevant statistics of the application, e.g., active users, grant requests, e-books issued, revoked, etc.
   - Note: Students can decide what more statistics to be shown apart from the given ones.

3. **Section Management**  
   - Create a new section to add e-books from a genre.
   - Update an existing section (e.g., name, date_created, end_date, and/or other fields).
   - Delete an existing section.

4. **E-book Management**  
   - Create e-books in a particular section.
   - Edit an existing e-book (e.g., name, content, author(s), date issued, return date, etc.).
   - Delete an existing e-book.

5. **Search for Sections and E-books**  
   - Users should be able to search for relevant e-books based on their section, authors, title, etc.
   - Users should be able to search for sections.

6. **General User Functionalities**  
   - Ability to request for/return a particular e-book.
   - A user can request a maximum of 5 e-books at a time.
   - A user can access a book for a specific period of time (e.g., N hours/days/weeks).
     - If N = 7 days, the user can return a book before 7 days; if they fail to do so, access will be automatically revoked after 7 days.
   - User can give feedback for an e-book.

*Note: Students can implement either automatic revocation after a specific period or manual revocation by the librarian.*

7. **Librarian Functionalities**  
   - Ability to view all issue/return requests from all users.
   - Ability to grant/revoke a particular e-book to a user.
   - A librarian should be able to monitor active users, grant requests, e-books issued, revoked, etc.

8. **Backend Jobs**  
   - **Scheduled Job - Daily Reminders**: 
     - Send daily reminders to users on Google Chat using webhooks, SMS, or mail.
     - Check if a user has not visited/has a return date approaching and send an alert.
     - Reminder can be sent every evening (students can choose the time).
   - **Scheduled Job - Monthly Activity Report**: 
     - Create and send a monthly report for the librarian via email using HTML.
     - Report can consist of sections & e-books issued, return dates, ratings received, etc.
     - Job should start on the first day of every month.
   - **User Triggered Async Job - Export as CSV**: 
     - Devise a CSV format for issued/returned/granted e-books done by the librarian.
     - Have a dashboard to trigger the export and send an alert once done.

9. **Performance and Caching**  
   - Add caching where required to increase performance.
   - Add cache expiry.
   - Focus on API performance.

---

## Recommended Functionalities
- Well-designed PDF reports for monthly activity (students can choose between HTML and PDF).
- Download e-books as PDF for a price (once paid and downloaded, always accessible to the user).
- External APIs/libraries for creating charts (e.g., ChartJS).
- Single responsive UI for both mobile and desktop.
- Unified UI that works across devices.
- Add to desktop feature.
- Implement frontend validation on all form fields using HTML5 validation or JavaScript.
- Implement backend validation within APIs.

---

## Optional Functionalities
- Provide styling and aesthetics to your application using simple CSS or Bootstrap.
- Incorporate a proper login system using Flask extensions like Flask_Login, Flask_Security, etc.
- Implement a dummy payment portal (just a view taking payment details for an e-book).
- Any additional features that you feel are appropriate for the application.



## How to Run the App

### Prerequisites
Before running the application, ensure you have the following installed on your machine:

1. **Python** (preferably Python 3.x)
2. **Node.js** (install from [nodejs.org](https://nodejs.org/))
3. **Vue CLI** (install using npm)

### Installation Steps

1. **Install Node.js**:
   - Download the installer from the [Node.js website](https://nodejs.org/).
   - Follow the instructions to install it on your machine.

2. **Install Vue CLI**:
   - Open a terminal or command prompt.
   - Run the following command:
     ```bash
     npm install -g @vue/cli
     ```

### Setting Up the Project

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Frosty-Winter-Snowfall/MAD-2-Project-LMS.git



### Setting Up the Project

1. **Clone the Repository**
   - Open a terminal and run:
     ```bash
     git clone https://github.com/Frosty-Winter-Snowfall/MAD-2-Project-LMS.git
     cd MAD-2-Project-LMS
     ```

2. **Navigate to the Backend Directory**
   - In the terminal, run:
     ```bash
     cd Backend
     ```

3. **Run the Flask Application**
   - Open a terminal in Visual Studio Code and run:
     ```bash
     python main.py
     ```

4. **Set Up the Frontend**
   - Open a new terminal and navigate to the frontend directory:
     ```bash
     cd ../front-all codes
     ```

5. **Install Dependencies**
   - In the terminal, run:
     ```bash
     npm install
     ```

6. **Run the Vue Application**
   - Start the Vue application:
     ```bash
     npm run serve
     ```

### Running Celery Tasks

1. **Start Redis Server**
   - Open a new command prompt and navigate to the Redis installation folder:
     ```bash
     cd C:\Users\Name\Downloads\Redis-x64-3.0.504
     redis-server.exe
     ```

   - To check if Redis is running, open another command prompt and run:
     ```bash
     cd C:\Users\Name\Downloads\Redis-x64-3.0.504
     redis-cli
     ```
   - Then type `ping`. If it responds with `PONG`, Redis is ready.

2. **Run the Flask Application Again**
   - Make sure you have all files ready and run:
     ```bash
     python main.py
     ```

3. **Open Two More Terminals for Celery**
   - Navigate to the backend folder in the first terminal and run:
     ```bash
     celery -A main.celery worker --pool=solo -l info
     ```

   - In the second terminal, run:
     ```bash
     celery -A main.celery beat --loglevel=info
     ```

4. **Open the Links to Check if Working**
   - Example link:
     ```plaintext
     http://localhost:5000/trigger_test_task
     ```



### How to Test if Celery is Working

1. **Run Celery, Beat, and Redis**
2. Open a new terminal and run:
   ```bash
   python test.py
3.See if test email was sent





