import psycopg2
from psycopg2 import sql

# CONFIGURATION 
# Database login details
DB_NAME = "student_management" # Database name
DB_USER = "postgres" # Database user
DB_PASS = "student12" # Password
DB_HOST = "localhost" # Server location


# CONNECTION HELPER
def connect_to_db():
    # Establishes and returns a connection to the PostgreSQL database 
    conn = None
    try: # Connecting using the defined configuration details
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST
        )
        return conn
    except psycopg2.Error as e:
        # Print a message if connection fails. For example wrong password, database down, wrong database name) 
        print(f"Error connecting to database. Check credentials, host, and port.")
        print(f"PostgreSQL Error Details: {e}")
        return None


# READ ALL FUNCTION
def getAllStudents():
    # Displays all student records from the database. (the 'READ' part of CURD)
    conn = connect_to_db()
    if conn is None:
        return # Exit if connection failed
    try: 
        cur = conn.cursor()

        # 1 SQL qurery to select all data in order by ID
        cur.execute("SELECT student_id, first_name, last_name, email, enrollment_date FROM students ORDER By student_id;")

        # 2 Fetch all rows
        students = cur.fetchall()

        # 3 Prints the results clearly to the console
        print("\n--- Student Records ---")
        if students:

            # Print column headers with padding for a clean look 
            print(f"{'ID' :<4} | {'First Name':<15} | {'Last Name' : <15} | {'Email' :<30} | {'Enrollment Date' :<15} ")
            print("-" * 80)
            for student in students:
                # Formatting each row. student 
                print(f"{student[0]:<4} | {student[1]:<15} | {student[2]:<15} | {student[3]:<30} | {student[4].strftime('%Y-%m-%d'):<15}")
        else:
            print("No students found in the table.")

        cur.close()

    except psycopg2.Error as e:
        print(f"Error during getAllStudents: {e}")
    finally:
        if conn:
            conn.close()  # Always close the connection when finished

        
# CREATE FUNCTION
def addStudent(first_name, last_name, email, enrollment_date):
    # Inserts a new student record into the students table, so 'ADD'
    conn = connect_to_db()
    if conn is None:
        return 

    try:
        cur = conn.cursor()
        
        # SQL query using placeholders (%s) for secure data insertion (prevents SQL injection)
        insert_query = """
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s);
        """
        
        # Data tuple containing the values to be inserted
        data = (first_name, last_name, email, enrollment_date)
        
        cur.execute(insert_query, data)
        
        # Commit the transaction to make the changes permanent in the database
        conn.commit()
        print(f"\nSUCCESS: Added new student: {first_name} {last_name}")

        cur.close()

    except psycopg2.IntegrityError as e:

        # Handles specific errors such as inserting an email that already exists so like duplicates.
        print(f"\nERROR: Failed to add student. A student with that email might already exist.")
        print(f"PostgreSQL Error Details: {e}")
    except psycopg2.Error as e:
        print(f"\nError during addStudent: {e}")
    finally:
        if conn:
            conn.close()
       


# UPDATE FUNCTION
def updateStudentEmail(student_id, new_email):
    # Updates the email address for a student with the specified ID when inserted
    conn = connect_to_db()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        
        # SQL query to update the email where the 'student_id' matches
        update_query = """
            UPDATE students
            SET email = %s
            WHERE student_id = %s;
        """
        
        data = (new_email, student_id)
        
        cur.execute(update_query, data)
        
        # Check if any row was actually updated, and how many were affected to confirm all the required students were updated
        if cur.rowcount == 0:
            print(f"\nALERT: No student found with ID {student_id}. Email was not updated.")
        else:
            conn.commit()
            print(f"\nSUCCESS: Updated email for student ID {student_id} to {new_email}.")

        cur.close()

    except psycopg2.Error as e:
        print(f"\nError during updateStudentEmail: {e}")
    finally:
        if conn:
            conn.close()
    

# DELETE FUNCTION
def deleteStudent(student_id):
    # Deletes the record of the student with the specified ID that was inserted
    conn = connect_to_db()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        
        # SQL query to delete the student where the 'student_id' matches
        delete_query = """
            DELETE FROM students
            WHERE student_id = %s;
        """
        
        data = (student_id,) # Note to self: the comma is important for pythin to treat this as a single-item tuple
        cur.execute(delete_query, data)
        
        # Checking if any row was actually deleted to confirm the student has been removed
        if cur.rowcount == 0:
            print(f"\nALERT: No student found with ID {student_id}. No record was deleted.")
        else:
            conn.commit()
            print(f"\nSUCCESS: Deleted student record with ID {student_id}.")

        cur.close()


    except psycopg2.Error as e:

        print(f"\nError during deleteStudent: {e}")

    finally:
        if conn:
            conn.close()




# User frinedly interactive interface

def display_menu():

    """Prints the main menu options to the console."""
    print("\n" + "="*40) # Decorative line for a clean look
    print("  STUDENT MANAGEMENT SYSTEM (PostgreSQL CRUD)")
    print("="*40) # Decorative line for a clean look
    print("1. Display All Students In The Table (Read)")
    print("2. Add New Student To The Table (Create)")
    print("3. Update Student Email (Update)")
    print("4. Delete Student From The Table (Delete)")
    print("5. Exit Application")
    print("="*40) # Decorative line for a clean look :)




def main_menu():
    # Starts the application loop and handles user choices
    while True:
        display_menu()
        
        # Taking user input
        user_input = input("Choose an option (1-5) to proceed: ").strip() 
        
        if user_input == '1':
            # Print option 1: Display all students (READ operation)
            print("\n--- Listing All Students ---")
            getAllStudents()
            
        elif user_input == '2':
            # Option 2: Add a new student (CREATE operation)
            print("\n--- ADD NEW STUDENT RECORD ---")
            try:
                # Gathering all the needed info
                f_name = input("First Name: ")
                l_name = input("Last Name: ")
                stu_email = input("Email: ")
                # Important: Date format must be correct for SQL!
                enroll_date = input("Enrollment Date (YYYY-MM-DD): ") 
                
                addStudent(f_name, l_name, stu_email, enroll_date)
            except Exception:
                # General catch for issues like hitting Ctrl+C or weird inputs
                print("\nError gathering student details. Please try again.")
            
        elif user_input == '3':
            # Option 3: Update an existing student's email (UPDATE operation)
            print("\n--- UPDATE STUDENT EMAIL ---")
            try:
                # Show existing IDs before asking for one
                getAllStudents() 
                target_id = int(input("Enter Student ID to modify: "))
                new_mail = input("Enter NEW Email Address: ")
                
                updateStudentEmail(target_id, new_mail)
            except ValueError:
                print("Input error! ID must be a whole number.")
            except Exception as err:
                # Catch other potential database or input issues
                print(f"Update failed due to an error: {err}")
                
        elif user_input == '4':
            # Option 4: Delete a student record (DELETE operation)
            print("\n--- DELETE STUDENT RECORD ---")
            try:
                # Show list for convenience
                getAllStudents() 
                target_id = int(input("Enter Student ID to delete: "))
                
                deleteStudent(target_id)
            except ValueError:
                print("Input error! ID must be a whole number.")
                
        elif user_input == '5':
            # Option 5: Exit the application gracefully
            print("\nExiting application. Have a good one!")
            break
            
        else:
            # Catching invalid menu inputs
            print(f"'{user_input}' isn't a valid option. Enter a number between 1 and 5.")

# The application starts here!
if __name__ == '__main__':
    main_menu()


# def main_menu():
#     """Runs the main application loop, prompting the user for action."""
#     while True:
#         display_menu()
#         choice = input("Enter your choice (1-5): ").strip()
        
#         if choice == '1':
#             # READ: Get All Students
#             getAllStudents()
            
#         elif choice == '2':
#             # CREATE: Add New Student
#             print("\n--- ADD NEW STUDENT ---")
#             try:
#                 first_name = input("Enter First Name: ")
#                 last_name = input("Enter Last Name: ")
#                 email = input("Enter Email: ")
#                 enrollment_date = input("Enter Enrollment Date (YYYY-MM-DD): ")
#                 addStudent(first_name, last_name, email, enrollment_date)
#             except Exception as e:
#                 print(f"Invalid input. Please check the date format or try again.")
            
#         elif choice == '3':
#             # UPDATE: Update Student Email
#             print("\n--- UPDATE STUDENT EMAIL ---")
#             try:
#                 # Always show current students first to help the user know which ID to choose
#                 getAllStudents() 
#                 student_id = int(input("Enter Student ID to update: "))
#                 new_email = input("Enter New Email Address: ")
#                 updateStudentEmail(student_id, new_email)
#             except ValueError:
#                 print("Invalid input. Student ID must be a number.")
#             except Exception as e:
#                 print(f"An error occurred: {e}")
                
#         elif choice == '4':
#             # DELETE: Delete Student
#             print("\n--- DELETE STUDENT ---")
#             try:
#                 # Always show current students first to help the user choose ID
#                 getAllStudents() 
#                 student_id = int(input("Enter Student ID to delete: "))
#                 deleteStudent(student_id)
#             except ValueError:
#                 print("Invalid input. Student ID must be a number.")
                
#         elif choice == '5':
#             # EXIT
#             print("Exiting application. Goodbye!")
#             break
            
#         else:
#             print("Invalid choice. Please enter a number between 1 and 5.")




# if __name__ == '__main__':
#     main_menu()








# # TEST
# if __name__ == '__main__':

#     # # --- 1. Initial Read ---
#     # print("--- 1. Testing Read (Initial Records) ---")
#     # getAllStudents()
    
#     # # --- 2. Create Test ---
#     # print("\n--- 2. Testing Create (Adding a New Student) ---")
#     # new_first = "Alice"
#     # new_last = "Wonder"
#     # new_email = "alice.wonder@example.com"
#     # new_date = "2024-05-15" 
#     # addStudent(new_first, new_last, new_email, new_date)
    
#     # # --- 3. Read After Create ---
#     # print("\n--- 3. Testing Read (After Adding Alice) ---")
#     # getAllStudents()

#     # # --- 4. Update Test (Updating John Doe's email - ID 1) ---
#     # print("\n--- 4. Testing Update (Changing John Doe's email) ---")
#     # john_id = 1
#     # new_john_email = "john.doe.updated@university.edu"
#     # updateStudentEmail(john_id, new_john_email)
    
#     # # --- 5. Read After Update ---
#     # print("\n--- 5. Testing Read (After Updating John Doe) ---")
#     # getAllStudents()

#     # --- 6. Delete Test (Deleting Alice Wonder - ID 4) ---
#     # print("\n--- 6. Testing Delete (Removing Alice Wonder) ---")
#     # alice_id = 4 
#     # deleteStudent(alice_id)
    
#     # # --- 7. Final Read After Delete ---
#     # print("\n--- 7. Testing Read (Final check, should be 3 records) ---")
#     # getAllStudents()

#     print("\nTest complete.")