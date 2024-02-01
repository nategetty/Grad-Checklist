-- Test data for the module MAJOR IN COMPUTER SCIENCE.

USE gradchecklist;

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
    (0, 'MATH', 3159, 'A/B', 'INTRODUCTION TO CRYPTOGRAPHY', 'Description', 'Extra info'),
    (0, 'COMPSCI', 3331, 'A/B', 'FOUNDATIONS OF COMPUTER SCIENCE I', 'Description', 'Extra info'),
    (0, 'COMPSCI', 3340, 'A/B', 'ANALYSIS OF ALGORITHMS I', 'Description', 'Extra info');

INSERT INTO Module
VALUES
    (0, 'MAJOR IN COMPUTER SCIENCE');

-- id, total_credit, min_grade, req_avg
INSERT INTO ModuleRequirement
VALUES
    (0, 1, 0.5, 65, NULL, 1),
    (0, 1, 0.5, 65, NULL, 1),
    (0, 1, 1.0, 60, NULL, 1),
    (0, 1, 3.5, 50, NULL, 0),
    (0, 1, 0.5, 50, NULL, 0),
    (0, 1, 2.0, 50, NULL, 0);

-- id, req_id, course_id, min_level
INSERT INTO ModuleRequirementCourse
VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 5),
    (2, 6),
    (3, 7),
    (3, 8),
    (3, 9),
    (3, 10),
    (3, 11),
    (3, 12),
    (3, 13),
    (3, 14),
    (3, 15),
    (4, 16),
    (4, 17),
    (4, 18),
    (4, 19),
    (4, 20),
    (4, 21),
    (4, 22),
    (5, 23),
    (5, 24),
    (6, 25),
    (6, 26),
    (6, 27),
    (6, 28);

INSERT INTO ModuleRequirementSubject
VALUES
    (0, 6, 'COMPSCI', 3000);

INSERT INTO Prerequisite
VALUES
    (0, 20, 1.0, 50, NULL),
    (0, 29, 0.5, 50, NULL),
    (0, 30, 1.0, 50, NULL),
    (0, 30, 0.5, 50, NULL);

INSERT INTO PrerequisiteCourse
VALUES
    (1, 18),
    (1, 19),
    (2, 23),
    (2, 24),
    (3, 18),
    (3, 19),
    (4, 23),
    (4, 24);
