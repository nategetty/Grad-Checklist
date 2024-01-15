CREATE DATABASE Courses;
USE Courses;

CREATE TABLE CourseCategory (
    category CHAR PRIMARY KEY
);

INSERT INTO CourseCategory
VALUES
    ('A'),
    ('B'),
    ('C');

CREATE TABLE Subject (
    code VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    category CHAR,
    category_2 CHAR,
    FOREIGN KEY (category) REFERENCES CourseCategory(category),
    FOREIGN KEY (category_2) REFERENCES CourseCategory(category)
);

CREATE TABLE CourseSuffix (
    suffix VARCHAR(255) PRIMARY KEY,
    credit DECIMAL(5, 2) NOT NULL,
    is_essay BOOL NOT NULL
);

INSERT INTO CourseSuffix
VALUES
    ('', 1, 0),
    ('A', 0.5, 0),
    ('B', 0.5, 0),
    ('A/B', 0.5, 0),
    ('A/B/Y', 0.5, 0),
    ('E', 1, 1),
    ('F', 0.5, 1),
    ('G', 0.5, 1),
    ('F/G', 0.5, 1);

CREATE TABLE Course (
    id INT PRIMARY KEY AUTO_INCREMENT,
    subject_code VARCHAR(255) NOT NULL,
    number INT NOT NULL,
    suffix VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    extra_information TEXT,
    UNIQUE (subject_code, number),
    FOREIGN KEY (subject_code) REFERENCES Subject(code),
    FOREIGN KEY (suffix) REFERENCES CourseSuffix(suffix)
);

CREATE TABLE Module (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
    -- maybe add date for grandfathering rules
);

CREATE TABLE ModuleRequirement (
    id INT PRIMARY KEY AUTO_INCREMENT,
    module_id INT NOT NULL,
    total_credit DECIMAL(5, 2) NOT NULL,
    minimum_grade INT,
    required_average INT,
    is_admission BIT NOT NULL,
    FOREIGN KEY (module_id) REFERENCES Module(id)
);

CREATE TABLE ModuleRequirementCourse (
    requirement_id INT,
    course_id INT,
    PRIMARY KEY (requirement_id, course_id),
    FOREIGN KEY (requirement_id) REFERENCES ModuleRequirement(id),
    FOREIGN KEY (course_id) REFERENCES Course(id)
);

-- Example from academic calendar:
-- 0.5 course from: Computer Science courses at the 3000 level or above
CREATE TABLE ModuleRequirementSubject (
    id INT PRIMARY KEY AUTO_INCREMENT,
    requirement_id INT NOT NULL,
    subject_code VARCHAR(255) NOT NULL,
    minimum_level INT NOT NULL,
    FOREIGN KEY (requirement_id) REFERENCES ModuleRequirement(id),
    FOREIGN KEY (subject_code) REFERENCES Subject(code)
);

CREATE TABLE Prerequisite (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    total_credit DECIMAL(5, 2) NOT NULL,
    minimum_grade INT,
    FOREIGN KEY (course_id) REFERENCES Course(id)
);

CREATE TABLE PrerequisiteCourse (
    prerequisite_id INT,
    required_course_id INT,
    PRIMARY KEY (prerequisite_id, required_course_id),
    FOREIGN KEY (prerequisite_id) REFERENCES Prerequisite(id),
    FOREIGN KEY (required_course_id) REFERENCES Course(id)
);

CREATE TABLE Antirequisite (
    course_id INT NOT NULL,
    antirequisite_course_id INT NOT NULL,
    PRIMARY KEY (course_id, antirequisite_course_id),
    FOREIGN KEY (course_id) REFERENCES Course(id),
    FOREIGN KEY (antirequisite_course_id) REFERENCES Course(id)
);

-- Views



-- Indices


