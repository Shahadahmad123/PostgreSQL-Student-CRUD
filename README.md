# PostgreSQL-Student-CRUD
A Python application demonstrating CRUD operations on a PostgreSQL database using 

This is to demonstrate the Create, Read, Update, and Delete (CRUD) operation by connecting to a PostgreSQL databse (pgAdmin) and managing student records. Python is the programming language that was used for this assingment. 

Follow the upcoming steps to set up the necessary environemnt and the PostgreSQL databse if not already done. (If done previusly, please skip this part 1.1):

1.1 Your software requirments:
* Must have the latest Python version installed on your device. (make sure when you install python, it is installed with the PATH added)
* You can install it through https://www.python.org/downloads
* Must have the latest PostgreSQL version. You can install it through https://www.postgresql.org/download
* Install the Python driver for the PostgreSQL (psycopg2-binary) using the following command in your command prompt: pip install psycopg2-binary

1.2 Databse and Table Creation:

* Start by launching pgAdmin4 on your computer
* The databse i created is called 'student_management'
* When the databse is created, start a new Query and run the scripts in db_setup.sql file which is located in this repository.
* Once the script is succefully executed, make sure the table has been created so you can proceed into the next step which is the implementation.


1.3 Application Configuration:

* Open the app.py file
* You must update DB_NAME, DB_USER, and DB_PASS variables near the top of the file to match YOUR local PostgreSQL credentials.

2. Executing the Application:

The application uses a very simple interactive menu I made so the demonstration is easier and cleaner.
* To execute the script, run the application from your terminal in the same directory as the app.py file. The command is: python app.py
* The application will start with a full menu of 5 options.
* Enter the corresponding number to the option you want to preform the desired CRUD operation.
* Once you finish, you can check all the results in pgAdmin4 table by executing this query: SELECT * FROM students;


4. Video Demonstration Link: 

  
