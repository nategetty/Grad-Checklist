-- Test data for the module MAJOR IN COMPUTER SCIENCE.

USE Courses;

INSERT INTO Subject
VALUES
    ('COMPSCI', 'Computer Science', 'C', NULL),
    ('DATASCI', 'Data Science', 'C', NULL),
    ('ENGSCI', 'Engineering Science', 'C', NULL),
    ('APPLMATH', 'Applied Mathematics', 'C', NULL),
    ('MATH', 'Mathematics', 'C', NULL),
    ('CALCULUS', 'Calculus', 'C', NULL),
    ('NMM', 'Numerical and Mathematical Methods', 'C', NULL),
    ('SCIENCE', 'Science', 'C', NULL);

INSERT INTO Course
VALUES
    (0, 'COMPSCI', 1025, 'A/B', 'COMPUTER SCIENCE FUNDAMENTALS I', 'Description', 'Extra info'),
    (0, 'COMPSCI', 1026, 'A/B', 'COMPUTER SCIENCE FUNDAMENTALS I', 'Description', 'Extra info'),
    (0, 'DATASCI', 1200, 'A/B', 'PROGRAMMING FOR DATA SCIENCE', 'Description', 'Extra info'),
    (0, 'ENGSCI', 1036, 'A/B', 'PROGRAMMING FUNDAMENTALS FOR ENGINEERS', 'Description', 'Extra info'),
    (0, 'COMPSCI', 1027, 'A/B', 'COMPUTER SCIENCE FUNDAMENTALS II', 'Description', 'Extra info'),
    (0, 'COMPSCI', 1037, 'A/B', 'COMPUTER SCIENCE FUNDAMENTALS II', 'Description', 'Extra info'),
    (0, 'APPLMATH', 1201, 'A/B', 'CALCULUS AND PROBABILITY WITH BIOLOGICAL APPLICATIONS', 'Description', 'Extra info'),
    (0, 'CALCULUS', 1000, 'A/B', 'CALCULUS I', 'Description', 'Extra info'),
    (0, 'CALCULUS', 1301, 'A/B', 'CALCULUS II', 'Description', 'Extra info'),
    (0, 'CALCULUS', 1500, 'A/B', 'CALCULUS I FOR THE MATHEMATICAL SCIENCES', 'Description', 'Extra info'),
    (0, 'CALCULUS', 1501, 'A/B', 'CALCULUS II FOR MATHEMATICAL AND PHYSICAL SCIENCES', 'Description', 'Extra info'),
    (0, 'MATH', 1600, 'A/B', 'LINEAR ALGEBRA I', 'Description', 'Extra info'),
    (0, 'NMM', 1411, 'A/B', 'LINEAR ALGEBRA WITH NUMERICAL ANALYSIS FOR ENGINEERING', 'Description', 'Extra info'),
    (0, 'NMM', 1412, 'A/B', 'CALCULUS FOR ENGINEERS I', 'Description', 'Extra info'),
    (0, 'NMM', 1414, 'A/B', 'CALCULUS FOR ENGINEERS II', 'Description', 'Extra info'),
    (0, 'COMPSCI', 2208, 'A/B', 'INTRODUCTION TO COMPUTER ORGANIZATION AND ARCHITECTURE', 'Description', 'Extra info'),
    (0, 'COMPSCI', 2209, 'A/B', 'APPLIED LOGIC FOR COMPUTER SCIENCE', 'Description', 'Extra info'),
    (0, 'COMPSCI', 2210, 'A/B', 'DATA STRUCTURES AND ALGORITHMS', 'Description', 'Extra info'),
    (0, 'COMPSCI', 2211, 'A/B', 'SOFTWARE TOOLS AND SYSTEMS PROGRAMMING', 'Description', 'Extra info'),
    (0, 'COMPSCI', 2212, 'A/B', 'INTRODUCTION TO SOFTWARE ENGINEERING', 'Description', 'Extra info'),
    (0, 'COMPSCI', 3305, 'A/B', 'OPERATING SYSTEMS', 'Description', 'Extra info'),
    (0, 'COMPSCI', 3307, 'A/B/Y', 'OBJECT-ORIENTED DESIGN AND ANALYSIS', 'Description', 'Extra info'),
    (0, 'COMPSCI', 2214, 'A/B', 'DISCRETE STRUCTURES FOR COMPUTING', 'Description', 'Extra info'),
    (0, 'MATH', 2155, 'F/G', 'MATHEMATICAL STRUCTURES', 'Description', 'Extra info'),
    (0, 'DATASCI', 3000, 'A/B', 'INTRODUCTION TO MACHINE LEARNING', 'Description', 'Extra info'),
    (0, 'SCIENCE', 3377, 'A/B', 'PROJECT MANAGEMENT FOR THE SCIENCES', 'Description', 'Extra info'),
    (0, 'MATH', 2156, 'A/B', 'MATHEMATICAL STRUCTURES II', 'Description', 'Extra info'),
    (0, 'MATH', 3159, 'A/B', 'INTRODUCTION TO CRYPTOGRAPHY', 'Description', 'Extra info');

INSERT INTO Module
VALUES
    (0, 'MAJOR IN COMPUTER SCIENCE');

-- id, total_credit, min_grade, req_avg
INSERT INTO Requirement
VALUES
    (0, 0.5, 65, NULL),
    (0, 0.5, 65, NULL),
    (0, 1.0, 60, NULL),
    (0, 3.5, 50, NULL),
    (0, 0.5, 50, NULL),
    (0, 2.0, 50, NULL);

-- module_id, req_id, is_admission
INSERT INTO ModuleRequirement
VALUES
    (1, 1, 1),
    (1, 2, 1),
    (1, 3, 1),
    (1, 4, 0),
    (1, 5, 0),
    (1, 6, 0);

-- id, req_id, course_id, min_level
INSERT INTO RequirementCourse
VALUES
    (0, 1, 1),
    (0, 1, 2),
    (0, 1, 3),
    (0, 1, 4),
    (0, 2, 5),
    (0, 2, 6),
    (0, 3, 7),
    (0, 3, 8),
    (0, 3, 9),
    (0, 3, 10),
    (0, 3, 11),
    (0, 3, 12),
    (0, 3, 13),
    (0, 3, 14),
    (0, 3, 15),
    (0, 4, 16),
    (0, 4, 17),
    (0, 4, 18),
    (0, 4, 19),
    (0, 4, 20),
    (0, 4, 21),
    (0, 4, 22),
    (0, 5, 23),
    (0, 5, 24),
    (0, 6, 25),
    (0, 6, 26),
    (0, 6, 27),
    (0, 6, 28);

INSERT INTO RequirementCourseLevel
VALUES
    (0, 6, 'COMPSCI', 3000);