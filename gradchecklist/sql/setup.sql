CREATE DATABASE Courses;
USE Courses;

CREATE TABLE Subject (
    code VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
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
    ('E', 1, 1),
    ('F', 0.5, 1),
    ('G', 0.5, 1),
    ('F/G', 0.5, 1);

CREATE TABLE CourseCategory (
    category CHAR PRIMARY KEY
);

INSERT INTO CourseCategory
VALUES
    ('A'),
    ('B'),
    ('C');

CREATE TABLE Course (
    id INT PRIMARY KEY AUTO_INCREMENT,
    subject_code VARCHAR(255) NOT NULL,
    number INT NOT NULL,
    suffix VARCHAR(255) NOT NULL,
    category CHAR NOT NULL,
    category_2 CHAR,
    description TEXT,
    extra_information TEXT,
    UNIQUE (subject_code, number),
    FOREIGN KEY (subject_code) REFERENCES Subject(code),
    FOREIGN KEY (suffix) REFERENCES CourseSuffix(suffix),
    FOREIGN KEY (category) REFERENCES CourseCategory(category),
    FOREIGN KEY (category_2) REFERENCES CourseCategory(category)
);

CREATE TABLE Module (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Requirement (
    id INT PRIMARY KEY AUTO_INCREMENT,
    total_credit DECIMAL(5, 2) NOT NULL,
    minimum_grade INT,
    required_average INT
);

CREATE TABLE ModuleRequirement (
    module_id INT NOT NULL,
    requirement_id INT NOT NULL,
    is_admission bool NOT NULL,
    PRIMARY KEY (module_id, requirement_id),
    FOREIGN KEY (module_id) REFERENCES Module(id),
    FOREIGN KEY (requirement_id) REFERENCES Requirement(id)
);

CREATE TABLE Prerequisite (
    course_id INT NOT NULL,
    requirement_id INT NOT NULL,
    PRIMARY KEY (course_id, requirement_id),
    FOREIGN KEY (course_id) REFERENCES Course(id),
    FOREIGN KEY (requirement_id) REFERENCES Requirement(id)
);

CREATE TABLE RequirementCourse (
    id INT PRIMARY KEY AUTO_INCREMENT,
    requirement_id INT NOT NULL,
    course_id INT,
    minimum_level INT,
    CHECK (course_id IS NOT NULL OR minimum_level IS NOT NULL),
    UNIQUE (requirement_id, course_id),
    UNIQUE (requirement_id, minimum_level),
    FOREIGN KEY (requirement_id) REFERENCES Requirement(id),
    FOREIGN KEY (course_id) REFERENCES Course(id)
);

CREATE TABLE Antirequisite (
    course_id INT NOT NULL,
    antirequisite_course_id INT NOT NULL,
    PRIMARY KEY (course_id, antirequisite_course_id),
    FOREIGN KEY (course_id) REFERENCES Course(id),
    FOREIGN KEY (antirequisite_course_id) REFERENCES Course(id)
);
