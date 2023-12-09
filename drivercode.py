# TA Management Suite




#--------------------------------------------------------------------------


port=5555



#---------------------------------------------------------------------------


from flask import *
import sqlite3
import random
import pypyodbc
from db_utils import *
from email_sender import *
import datetime

def killProcessRunningAtPort(port):
    import subprocess
    port=str(port)
    command="netstat -ano | findstr :"+port
    output=subprocess.getoutput(command).split('\n')
    PIDs=[]
    for i in output:
        if "127.0.0.1:"+port in i and "LISTENING" in i:
            PIDs.append(i.split()[-1])
    for i in PIDs:
        print("Killing "+i)
        subprocess.getoutput("taskkill /PID "+i+" /F")


#-------------------Database Logic------------------------------


db_config = {
    "Driver": "ODBC Driver 17 for SQL Server",
    "ServerName": "devdbinstance01.database.windows.net",
    "DatabaseName": "TAManagementSuite",
    "UserID": "ServerAdminPro",
    "Password": "S3cure#Adm!nPr0",
    "Encrypt": "yes",
    "TrustServerCertificate": "no",
    "ConnectionTimeout": 130
}

db_cursor = get_db_cursor_obj(db_config["Driver"],
                              db_config["ServerName"],
                              db_config["DatabaseName"],
                              db_config["UserID"],
                              db_config["Password"],
                              autocommit=True)


if db_cursor:
    print('Connected to Azure SQL Server Database')

#Global Variables

logged_in_user_id = None
logged_in_user_role = None
logged_in_user_email = None


#---------------------
app=Flask(__name__) 

        
@app.route('/TAManagementSuite/home')
def home_page():
    return render_template("home.html")

def display_results(title, columns, rows):
    # Combine columns and rows into table_data
    table_data = [dict(zip(columns, row)) for row in rows]
    return render_template('results.html', title=title, table_data=table_data)



#--------------------------TAApplicant--------------------------------

@app.route('/TAManagementSuite/TAApplicant/Login')
def ta_applicant_login():
    return render_template("ta_applicant_login.html")

@app.route('/TAManagementSuite/TAApplicant/Home', methods=['GET'])
def ta_applicant_landing():
    global logged_in_user_id, logged_in_user_role, logged_in_user_email
    
    user_id = request.args.get('user_id')
    password = request.args.get('password')
    print(user_id, password)

    users_list = get_table_rows(db_cursor, 'Users')
    print(users_list)

    for user in users_list:
        if user[0] == user_id and user[1] == password and user[-1] == 'TAApplicant':

            logged_in_user_id = user_id
            logged_in_user_role = 'TAApplicant'
            logged_in_user_email = user[2]
            
            send_email(user[2], 'TA Management Suite - Login Alert', 'Hey User, You are logged into TA Management Suite App as TA Applicant')
            return render_template("ta_applicant_landing.html")
    return render_template("ta_applicant_login.html")

@app.route('/TAManagementSuite/TAApplicant/SubmitApplication', methods=['GET'])
def ta_applicant_submit_application():
    student_id = request.args.get('student_id')
    email = request.args.get('email')
    course_id = request.args.get('course_id')
    skills = request.args.get('skills')
    additional_info = request.args.get('additionalInfo')
    cv = None
    # Get the current date and time
    current_date_time = datetime.datetime.now()

    # Format it as a string in the desired format (e.g., 'yyyy-mm-dd HH:MM:SS')
    current_date_time = current_date_time.strftime('%Y-%m-%d %H:%M:%S')

    insert_into_table (db_cursor, 'TAApplications', ['StudentID', 'CourseID', 'CV', 'Skills', 'Status', 'Experience', 'SubmissionDate'], [logged_in_user_id, course_id, 'CV Content', skills, 'Submitted', 0, current_date_time])
    return render_template('ta_applicant_landing.html')  # Replace with your actual response or template
    return "Application submitted successfully!"

@app.route('/TAManagementSuite/TAApplicant/Register')
def ta_applicant_register():
    return render_template("ta_applicant_register.html")



# Function to insert data into the Users table
def insert_user_data(cursor, user_id, email, password, role = 'TAApplicant'):


    # Insert the user data into the Users table
    insert_into_table(cursor, 'Users', ['UserID', 'Password', 'Email', 'Role'],
                     [user_id, password, email, role])


# Function to insert data into the TAApplicantProfile table
def insert_profile_data(cursor, student_id, first_name, last_name, email, contact_number, address, cgpa, additional_info):
    # Insert the profile data into the TAApplicantProfile table
    insert_into_table(cursor, 'TAApplicantProfile',
                     ['StudentID', 'FirstName', 'LastName', 'Email',
                      'ContactNumber', 'Address', 'CGPA', 'AdditionalInformation'],
                     [student_id, first_name, last_name, email,
                      contact_number, address, cgpa, additional_info])


@app.route('/TAManagementSuite/TAApplicant/RegisterUser', methods=['GET'])
def ta_applicant_register_user():
    # Extract form data
    student_id = request.args.get('student_id')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    contact_number = request.args.get('contact_number')
    address = request.args.get('address')
    cgpa = 0 if request.args.get('cgpa') is None else float(request.args.get('cgpa'))
    additional_info = request.args.get('additional_info')
    password = request.args.get('password')
    print(student_id, first_name, last_name, email, contact_number, address, cgpa, additional_info)
    # Insert user data into Users table and get the generated UserID
    user_id = insert_user_data(db_cursor, student_id, email, password)

    # Insert profile data into TAApplicantProfile table
    insert_profile_data(db_cursor, student_id, first_name, last_name, email, contact_number, address, cgpa, additional_info)

    return f"User {student_id} registered successfully!"



@app.route('/TAManagementSuite/TAApplicant/CheckStatus')
def ta_applicant_check_status():
    course_id = request.args.get('course_id')
    TAReviews_list = get_table_rows(db_cursor, 'TAReviews')
    rows = []
    print(TAReviews_list)
    for row in TAReviews_list:
        if row[1] == logged_in_user_id and row[2] == course_id:
            print(row)
            rows.append(row[3:])
    return display_results(f'{logged_in_user_id} Appliation Status for {course_id}', ['InstructorID', 'Rating', 'Status', 'Comments', 'DateOfStatusUpdation'], rows)


@app.route('/TAManagementSuite/TAApplicant/YourData')
def ta_applicant_your_data():
    TAApplicantProfile_list = get_table_rows(db_cursor, 'TAApplicantProfile')
    rows = []
    for row in TAApplicantProfile_list:
        if row[1] == logged_in_user_id:
            print(row)
            rows.append(row[1:])
    return display_results(f'{logged_in_user_id} User Details', ['StudentID', 'FirstName', 'LastName', 'Email', 'ContactNumber', 'Address', 'CGPA', 'AdditionalInformation'], rows)
    
#-------------------Department Staff-----------------------

@app.route('/TAManagementSuite/DepartmentStaff/Login')
def department_staff_login():
    return render_template("department_staff_login.html")

@app.route('/TAManagementSuite/DepartmentStaff/Home', methods=['GET'])
def department_staff_landing():
    global logged_in_user_id, logged_in_user_role, logged_in_user_email
    
    user_id = request.args.get('user_id')
    password = request.args.get('password')
    print(user_id, password)

    users_list = get_table_rows(db_cursor, 'Users')
    print(users_list)

    for user in users_list:
        if user[0] == user_id and user[1] == password and user[-1] == 'DepartmentStaff':

            logged_in_user_id = user_id
            logged_in_user_role = 'DepartmentStaff'
            logged_in_user_email = user[2]
            
            #send_email(user[2], 'TA Management Suite - Login Alert', 'Hey User, You are logged into TA Management Suite App as DepartmentStaff')
            return render_template("department_staff_landing.html")
    return render_template("department_staff_login.html")


@app.route('/TAManagementSuite/DepartmentStaff/Register')
def department_staff_register():
    
    return render_template("department_staff_register.html")

@app.route('/TAManagementSuite/DepartmentStaff/RegisterUser')
def department_staff_register_user():
    # Extract form data
    full_name = request.args.get('full_name')
    email = request.args.get('email')
    user_id = request.args.get('user_id')
    email = request.args.get('email')
    password = request.args.get('password')
    confirm_password = request.args.get('confirm_password')

    print(full_name, email, user_id, email, password, )
    insert_user_data(db_cursor, user_id, email, password, 'DepartmentStaff')

    return f"User {user_id} registered successfully!"

@app.route('/TAManagementSuite/DepartmentStaff/AddCourse', methods=['GET'])
def department_staff_add_course():
    # Retrieve form data from request object
    course_id = request.args.get('course_id')
    course_name = request.args.get('course_name')
    description = request.args.get('description')
    instructor_id = request.args.get('instructor_id')
    num_ta_req = request.args.get('num_ta_req')
    skills_req = request.args.get('skills_req')

    # Define the columns and the row values
    cols = ["CourseID", "CourseName", "Description", "InstructorID", "NumTARequired", "SkillsRequired"]
    row = [course_id, course_name, description, instructor_id, num_ta_req, skills_req]
    print(row)
    # Insert the data into the Courses table
    insert_into_table(db_cursor, 'Courses', cols, row)
    
    return "New Course Added"

@app.route('/TAManagementSuite/DepartmentStaff/ShowInstructors', methods=['GET'])
def department_staff_show_instructors():
    Instructors_list = get_table_rows(db_cursor, 'Instructors')
    return display_results(title = 'Instructors', columns = ['InstructorID', 'InstructorName', 'CourseID', 'CourseName'], rows = Instructors_list)


@app.route('/TAManagementSuite/DepartmentStaff/RunPreliminaryMatching', methods=['GET'])    
def department_staff_run_preliminary_matching():
    CourseAssignments_list = get_table_rows(db_cursor, 'CourseAssignments')
    users_list = get_table_rows(db_cursor, 'Users')
    #('C004', 'U002', 'U005', 'Fall', 2023);
    for row in CourseAssignments_list:
        for row2 in users_list:
            if row[2] == row2[0]:
                send_email(row2[2], 'TA Management Suite - PreliminaryMatching Alert', f'Hey User, PreliminaryMatching Made with your Course Application {row[1]}')
    
    return "Ran Preliminary Matching, Go back to Main"

@app.route('/TAManagementSuite/DepartmentStaff/SendPreliminaryMatching', methods=['GET'])    
def department_staff_send_preliminary_matching():
    CourseAssignments_list = get_table_rows(db_cursor, 'CourseAssignments')
    users_list = get_table_rows(db_cursor, 'Users')
    #('C004', 'U002', 'U005', 'Fall', 2023);
    for row in CourseAssignments_list:
        for row2 in users_list:
            if row2[-1] == 'TACommittee':
                send_email(row2[2], 'TA Management Suite - PreliminaryMatching Alert', f'Dear TA Committee, PreliminaryMatching Made with Course Application {row[2]}:{row[1]}')
    return "Sent Preliminary Matching, Go back to Main"
#-------------------TA Committee-----------------------

@app.route('/TAManagementSuite/TACommittee/Login')
def ta_committee_login():
    return render_template("ta_committee_login.html")

@app.route('/TAManagementSuite/TACommittee/Home', methods=['GET'])
def ta_committee_landing():
    global logged_in_user_id, logged_in_user_role, logged_in_user_email
    
    user_id = request.args.get('user_id')
    password = request.args.get('password')
    print(user_id, password)

    users_list = get_table_rows(db_cursor, 'Users')
    print(users_list)

    for user in users_list:
        if user[0] == user_id and user[1] == password and user[-1] == 'TACommittee':

            logged_in_user_id = user_id
            logged_in_user_role = 'TACommittee'
            logged_in_user_email = user[2]
            
            send_email(user[2], 'TA Management Suite - Login Alert', 'Hey User, You are logged into TA Management Suite App as TACommittee')
            return render_template("ta_committee_landing.html")
    return render_template("ta_committee_login.html")


@app.route('/TAManagementSuite/TACommittee/Register')
def ta_committee_register():
    return render_template("ta_committee_register.html")

@app.route('/TAManagementSuite/TACommittee/RegisterUser', methods=['GET'])
def ta_committee_register_user():
    # Extract form data
    full_name = request.args.get('full_name')
    email = request.args.get('email')
    user_id = request.args.get('user_id')
    email = request.args.get('email')
    password = request.args.get('password')
    confirm_password = request.args.get('confirm_password')

    print(full_name, email, user_id, email, password, )
    insert_user_data(db_cursor, user_id, email, password, 'TACommittee')

    return f"User {user_id} registered successfully!"

@app.route('/TAManagementSuite/TACommittee/ApplicationsReview', methods=['GET'])
def ta_committee_applications_review():
    # Retrieve form data from request object
    TAApplications_list = get_table_rows(db_cursor, 'TAApplications')
    return display_results(title = 'All TAApplications', columns = ['ApplicationID', 'StudentID', 'CourseID', 'CV', 'Skills', 'Status', 'Experience', 'SubmissionDate'], rows = TAApplications_list)


@app.route('/TAManagementSuite/TACommittee/ReccomendationsReview', methods=['GET'])
def ta_committee_show_reccomendations_review():
    TAReviews_list = get_table_rows(db_cursor, 'TAReviews')
    rows = []
    print(TAReviews_list)
    for row in TAReviews_list:
        if True:
            print(row)
            rows.append(row[1:])
    return display_results(f'TAReviews_list by Department Staff', ['StudentID', 'CourseID', 'InstructorID', 'Rating', 'Status', 'Comments', 'DateOfStatusUpdation'], rows)


@app.route('/TAManagementSuite/TACommittee/FinalDecisions', methods=['GET'])
def ta_committee_show_final_decisions():
    TAReviews_list = get_table_rows(db_cursor, 'TAReviews')
    rows = []
    print(TAReviews_list)
    for row in TAReviews_list:
        if True:
            print(row)
            rows.append(row[1:])
    return display_results(f'TAReviews_list by Department Staff', ['StudentID', 'CourseID', 'InstructorID', 'Rating', 'Status', 'Comments', 'DateOfStatusUpdation'], rows)

#----------------------------------------------------------------------------------------------------------


@app.route('/TAManagementSuite/Instructor/Login')
def instructor_login():
    return render_template("instructor_login.html")

@app.route('/TAManagementSuite/Instructor/Home', methods=['GET'])
def instructor_landing():
    global logged_in_user_id, logged_in_user_role, logged_in_user_email
    
    user_id = request.args.get('user_id')
    password = request.args.get('password')
    print(user_id, password)

    users_list = get_table_rows(db_cursor, 'Users')
    print(users_list)

    for user in users_list:
        if user[0] == user_id and user[1] == password and user[-1] == 'Instructor':

            logged_in_user_id = user_id
            logged_in_user_role = 'Instructor'
            logged_in_user_email = user[2]
            
            #send_email(user[2], 'TA Management Suite - Login Alert', 'Hey User, You are logged into TA Management Suite App as Instructor')
            return render_template("instructor_landing.html")
    return render_template("instructor_login.html")


@app.route('/TAManagementSuite/Instructor/Register')
def instructor_register():
    return render_template("instructor_register.html")

@app.route('/TAManagementSuite/Instructor/RegisterUser', methods=['GET'])
def instructor_register_user():
    # Extract form data
    full_name = request.args.get('full_name')
    email = request.args.get('email')
    user_id = request.args.get('user_id')
    email = request.args.get('email')
    password = request.args.get('password')
    confirm_password = request.args.get('confirm_password')

    print(full_name, email, user_id, email, password, )
    insert_user_data(db_cursor, user_id, email, password, 'Instructor')

    return f"User {user_id} registered successfully!"

@app.route('/TAManagementSuite/Instructor/TAsUnderMe', methods=['GET'])
def instructor_TAsUnderMe():
    CourseAssignments_list = get_table_rows(db_cursor, 'CourseAssignments')
    rows = []
    for row in CourseAssignments_list:
        if row[-3] == logged_in_user_id:
            rows.append([row[-4], row[-5]])
    return display_results(f'TAs Woring Under You', ['StudentID', 'CourseID'], rows)


@app.route('/TAManagementSuite/Instructor/PerformanceAssessment', methods=['GET'])
def instructor_PerformanceAssessment():
    #StudentID = request.form.get('StudentID')
    #Rating = request.form.get('Rating')
    #Comments = request.form.get('Comments')

    #update_query = "UPDATE TAReviews SET Rating = Rating, Comments = Comments WHERE StudentID = StudentID"
    #db_cursor.execute(update_query, (Rating, Comments, StudentID))


    TAReviews_list = get_table_rows(db_cursor, 'TAReviews')
    rows = []
    print(TAReviews_list)
    for row in TAReviews_list:
        if True:
            print(row)
            rows.append(row[1:])
    return display_results(f'TAReviews_list by Department Staff', ['StudentID', 'CourseID', 'InstructorID', 'Rating', 'Status', 'Comments', 'DateOfStatusUpdation'],rows)
@app.route('/TAManagementSuite/Instructor/ViewAssignments', methods=['GET'])
def instructor_ViewAssignments():
    CourseAssignments_list = get_table_rows(db_cursor, 'CourseAssignments')
    rows = []
    for row in CourseAssignments_list:
        if row[-3] == logged_in_user_id:
            rows.append([row[-4], row[-5]])
    return display_results(f'Course Assignments of TAs under You', ['StudentID', 'CourseID'], rows)

@app.route('/TAManagementSuite/Instructor/EvaluationNotification', methods=['GET'])
def instructor_EvaluationNotification():
    return render_template("instructor_register.html")


#------------------------------------------------------------------------
if __name__ =='__main__':
    killProcessRunningAtPort(port)
    print("To access application, go to:","http://127.0.0.1:"+str(port)+"/TAManagementSuite/home\n\n\n")
    print("Server Traffic and other details:\n")
    app.run(host="localhost", port=port,debug = True)
