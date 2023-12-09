


-- Users Table/ for authentication purpouses
CREATE TABLE Users (
    UserID NVARCHAR(10) NOT NULL, -- student id for TAs
    Password NVARCHAR(255) NOT NULL,
    Email NVARCHAR(100) NOT NULL,
    Role NVARCHAR(50) NOT NULL
);

-- UserProfile Table
CREATE TABLE TAApplicantProfile (
    UserProfileID INT IDENTITY(1,1) PRIMARY KEY,
    StudentID NVARCHAR(10) FOREIGN KEY REFERENCES Users(UserID),
    FirstName NVARCHAR(50),-- req
    LastName NVARCHAR(50),-- req
    Email NVARCHAR(50) -- req
    ContactNumber NVARCHAR(15),-- req
    Address NVARCHAR(255),
    CGPA float <=4  -- req
    AdditionalInformation NVARCHAR(MAX)
);



-- Applications Table
CREATE TABLE TAApplications (
    StudentID NVARCHAR(10) FOREIGN KEY REFERENCES Users(StudentID),
    Email 
    CourseID NVARCHAR(10) FOREIGN KEY REFERENCES Courses(CourseID),
    CV NVARCHAR(MAX),
    Skills NVARCHAR(MAX),
    Status NVARCHAR(50) NOT NULL,
    Experience int 
    SubmissionDate DATETIME NOT NULL
); -- make user id + course id as primary key

-- Courses Table
CREATE TABLE Courses (
    CourseID NVARCHAR(10) NOT NULL,
    CourseName NVARCHAR(50) NOT NULL,
    Description NVARCHAR(MAX),
    InstructorID INT FOREIGN KEY REFERENCES Users(UserID),
    NumTARequired Int
    SkillsRequired NVARCHAR / JSON -- comma seperated values/ json
);



-- TAExperience Table
CREATE TABLE TAExperience (
    user id + course id FOREIGN KEY REFERENCES TAApplications(user id + course id),
    CourseName NVARCHAR(100),
    Institution NVARCHAR(100),
    StartDate DATE,
    EndDate DATE
);

-- CourseAssignments Table
CREATE TABLE CourseAssignments (
    CourseID INT FOREIGN KEY REFERENCES Courses(CourseID),
    StudentID INT FOREIGN KEY REFERENCES Users(StudentID),
    InstructorID
    Term NVARCHAR(20),
    Year INT
);

-- TAReviews Table
CREATE TABLE TAReviews (
    StudentID ref TAApplications
    CourseID ref Courses
    InstructorID Varchar(10) FOREIGN KEY REFERENCES Users(UserID),
    Rating INT,
    Status VARCHAR (Submitted, Under Review, Decision Made)
    Comments NVARCHAR(MAX),
    DateOfStatusUpdation DATETIME
); -- gets updated by TA applicants, dept staffs


CREATE TABLE Instructors

 
InstructorID
InstructorName
CourseID
CourseName



TAPerformanceAssessment

StudentID
CourseID
InstructorID
Rating int
Comments VARCHAR
------------------------------------------------------------------------
-- Notifications Table
CREATE TABLE Notifications (
    NotificationID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    Type NVARCHAR(50),
    Message NVARCHAR(MAX),
    DateSent DATETIME
);

-- AuditLogs Table
CREATE TABLE AuditLogs (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    ActionType NVARCHAR(50),
    Description NVARCHAR(MAX),
    Timestamp DATETIME DEFAULT GETDATE()
);
