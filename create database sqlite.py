import sqlite3

def create_tables(conn):
    # SQL commands to create each table
    tables_sql = [
        '''
        CREATE TABLE IF NOT EXISTS Users (
            UserID NVARCHAR(10) PRIMARY KEY,
            Password NVARCHAR(255) NOT NULL,
            Email NVARCHAR(100) NOT NULL UNIQUE,
            Role NVARCHAR(50) NOT NULL
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS TAApplicantProfile (
            UserProfileID INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentID NVARCHAR(10) NOT NULL,
            FirstName NVARCHAR(50) NOT NULL,
            LastName NVARCHAR(50) NOT NULL,
            Email NVARCHAR(50) NOT NULL,
            ContactNumber NVARCHAR(15),
            Address NVARCHAR(255),
            CGPA FLOAT CHECK (CGPA <= 4),
            AdditionalInformation TEXT,
            FOREIGN KEY (StudentID) REFERENCES Users(UserID)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS TAApplications (
            ApplicationID INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentID NVARCHAR(10) NOT NULL,
            CourseID NVARCHAR(10) NOT NULL,
            CV TEXT,
            Skills TEXT,
            Status NVARCHAR(50) NOT NULL,
            Experience INT,
            SubmissionDate DATETIME NOT NULL,
            FOREIGN KEY (StudentID) REFERENCES Users(UserID),
            FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS Courses (
            CourseID NVARCHAR(10) PRIMARY KEY,
            CourseName NVARCHAR(50) NOT NULL,
            Description TEXT,
            InstructorID NVARCHAR(10),
            NumTARequired INT,
            SkillsRequired TEXT,
            FOREIGN KEY (InstructorID) REFERENCES Users(UserID)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS TAExperience (
            ExperienceID INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentID NVARCHAR(10) NOT NULL,
            CourseID NVARCHAR(10) NOT NULL,
            CourseName NVARCHAR(100),
            Institution NVARCHAR(100),
            StartDate DATE,
            EndDate DATE,
            FOREIGN KEY (StudentID) REFERENCES Users(UserID),
            FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS CourseAssignments (
            AssignmentID INTEGER PRIMARY KEY AUTOINCREMENT,
            CourseID NVARCHAR(10) NOT NULL,
            StudentID NVARCHAR(10) NOT NULL,
            InstructorID NVARCHAR(10),
            Term NVARCHAR(20),
            Year INT,
            FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
            FOREIGN KEY (StudentID) REFERENCES Users(UserID),
            FOREIGN KEY (InstructorID) REFERENCES Users(UserID)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS TAReviews (
            ReviewID INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentID NVARCHAR(10) NOT NULL,
            CourseID NVARCHAR(10) NOT NULL,
            InstructorID NVARCHAR(10) NOT NULL,
            Rating INT,
            Status NVARCHAR(50) CHECK (Status IN ('Submitted', 'Under Review', 'Decision Made')),
            Comments TEXT,
            DateOfStatusUpdation DATETIME,
            FOREIGN KEY (StudentID) REFERENCES Users(UserID),
            FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
            FOREIGN KEY (InstructorID) REFERENCES Users(UserID)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS Instructors (
            InstructorID NVARCHAR(10) PRIMARY KEY,
            InstructorName NVARCHAR(100),
            CourseID NVARCHAR(10),
            CourseName NVARCHAR(50),
            FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS TAPerformanceAssessment (
            AssessmentID INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentID NVARCHAR(10) NOT NULL,
            CourseID NVARCHAR(10) NOT NULL,
            InstructorID NVARCHAR(10) NOT NULL,
            Rating INT,
            Comments TEXT,
            FOREIGN KEY (StudentID) REFERENCES Users(UserID),
            FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
            FOREIGN KEY (InstructorID) REFERENCES Instructors(InstructorID)
        );
        '''
    ]

    for sql in tables_sql:
        conn.execute(sql)

def insert_sample_data(conn):
    pass

# Example usage
if __name__ == "__main__":
    conn = sqlite3.connect('TAManagementSuite.db')
    create_tables(conn)
    insert_sample_data(conn)
    conn.close()
