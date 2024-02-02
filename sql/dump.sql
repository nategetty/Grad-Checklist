-- MySQL dump 10.13  Distrib 8.3.0, for macos13.6 (arm64)
--
-- Host: localhost    Database: gradchecklist
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Antirequisite`
--

DROP TABLE IF EXISTS `Antirequisite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Antirequisite` (
  `course_id` int NOT NULL,
  `antirequisite_course_id` int NOT NULL,
  PRIMARY KEY (`course_id`,`antirequisite_course_id`),
  KEY `antirequisite_course_id` (`antirequisite_course_id`),
  CONSTRAINT `antirequisite_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `Course` (`id`),
  CONSTRAINT `antirequisite_ibfk_2` FOREIGN KEY (`antirequisite_course_id`) REFERENCES `Course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Antirequisite`
--

LOCK TABLES `Antirequisite` WRITE;
/*!40000 ALTER TABLE `Antirequisite` DISABLE KEYS */;
/*!40000 ALTER TABLE `Antirequisite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Course`
--

DROP TABLE IF EXISTS `Course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `subject_code` varchar(255) NOT NULL,
  `number` int NOT NULL,
  `suffix` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text,
  `extra_information` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subject_code` (`subject_code`,`number`),
  UNIQUE KEY `IdxCourseNumber` (`subject_code`,`number`),
  KEY `suffix` (`suffix`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`subject_code`) REFERENCES `Subject` (`code`),
  CONSTRAINT `course_ibfk_2` FOREIGN KEY (`suffix`) REFERENCES `CourseSuffix` (`suffix`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Course`
--

LOCK TABLES `Course` WRITE;
/*!40000 ALTER TABLE `Course` DISABLE KEYS */;
INSERT INTO `Course` VALUES (1,'COMPSCI',1025,'A/B','COMPUTER SCIENCE FUNDAMENTALS I','Course DescriptionThe nature of Computer Science as a discipline; the design and analysis of algorithms and their implementation as modular, reliable, well-documented programs written in a modern programming language. Intended for students with significant programming experience in at least one high-level block-structured or object-oriented language.','3 lecture hours.'),(2,'COMPSCI',1026,'A/B','COMPUTER SCIENCE FUNDAMENTALS I','Course DescriptionThe nature of Computer Science as a discipline; the design and analysis of algorithms and their implementation as modular, reliable, well-documented programs written in  a modern programming language. Intended for students with little or no background in programming.','3 lecture hours, 2 laboratory/tutorial hours.'),(3,'DATASCI',1200,'A/B','PROGRAMMING FOR DATA SCIENCE','Course DescriptionProgramming for Data Science is intended for students with little or no background in programming. Design and analysis of algorithms and their implementation as modular, reliable, well-documented programs written in a modern programming language.','3 lecture hours/week, 2 laboratory hours/week.'),(4,'ENGSCI',1036,'A/B','PROGRAMMING FUNDAMENTALS FOR ENGINEERS','Course DescriptionDesigning, implementing and testing computer programs using Java and MATLAB to fulfill given specifications for small problems using sound engineering principles and processes. Awareness of the engineering aspects of the process of constructing a computer program.','3 lecture hours, 2 laboratory hours.'),(5,'COMPSCI',1027,'A/B','COMPUTER SCIENCE FUNDAMENTALS II','Course DescriptionA continuation for bothComputer Science 1025A/BandComputer Science 1026A/B. Data organization and manipulation; abstract data types and their implementations in a modern programming language; lists, stacks, queues, trees; recursion; file handling and storage.','3 lecture hours, 1 laboratory/tutorial hour.'),(6,'COMPSCI',1037,'A/B','COMPUTER SCIENCE FUNDAMENTALS II','Course DescriptionA continuation forEngineering Science 1036A/B. Data organization and manipulation; abstract data types and their implementations in the C programming language; lists, stacks, queues, trees; pointers; recursion; file handling and storage. Intended for students in the Faculty of Engineering.','3 lecture hours, 2 laboratory/tutorial hour.'),(7,'APPLMATH',1201,'A/B','CALCULUS AND PROBABILITY WITH BIOLOGICAL APPLICATIONS','Course DescriptionApplications of integration, integration using mathematical software packages. Scaling and allometry. Basic probability theory. Fundamentals of linear algebra: vectors, matrices, matrix algebra. Difference and differential equations. Each topic will be illustrated by examples and applications from the biological sciences, such as population growth, predator-prey dynamics, age-structured populations.','4 lecture hours.'),(8,'CALCULUS',1000,'A/B','CALCULUS I','Course DescriptionReview of limits and derivatives of exponential, logarithmic and rational functions. Trigonometric functions and their inverses. The derivatives of the trig functions and their inverses. L\'Hospital\'s rules. The definite integral. Fundamental theorem of Calculus. Simple substitution. Applications including areas of regions and volumes of solids of revolution.','4 lecture hours.'),(9,'CALCULUS',1301,'A/B','CALCULUS II','Course DescriptionFor students requiring the equivalent of a full course in calculus at a less rigorous level thanCalculus 1501A/B.  Integration by parts, partial fractions, integral tables, geometric series, harmonic series, Taylor series with applications, arc length of parametric and polar curves, first order linear and separable differential equations with applications.','4 lecture hours.'),(10,'CALCULUS',1500,'A/B','CALCULUS I FOR THE MATHEMATICAL SCIENCES','Course DescriptionAn enriched version ofCalculus 1000A/B. Basic set theory and an introduction to mathematical rigour. The precise definition of limit. Derivatives of exponential, logarithmic, rational trigonometric functions. L\'Hospital\'s rule. The definite integral. Fundamental theorem of Calculus. Integration by substitution. Applications.','4 lecture hours.'),(11,'CALCULUS',1501,'A/B','CALCULUS II FOR MATHEMATICAL AND PHYSICAL SCIENCES','Course DescriptionStudents who intend to pursue a degree in Actuarial Science, Applied Mathematics, Astronomy, Mathematics, Physics, or Statistics should take this course. Techniques of integration; The Mean Value Theorem and its consequences; series, Taylor series with applications; parametric and polar curves with applications; first order linear and separable differential equations with applications.','4 lecture hours.'),(12,'MATH',1600,'A/B','LINEAR ALGEBRA I','Course DescriptionProperties and applications of vectors; matrix algebra; solving systems of linear equations; determinants; vector spaces; orthogonality; eigenvalues and eigenvectors.','3 lecture hours, 1 laboratory hour.'),(13,'NMM',1411,'A/B','LINEAR ALGEBRA WITH NUMERICAL ANALYSIS FOR ENGINEERING','Course DescriptionMatrix operations, systems of linear equations, linear spaces and transformations, determinants, eigenvalues and eigenvectors, applications of interest to Engineers including diagonalization of matrices, quadratic forms, orthogonal transformations; introduction to MATLAB with applications from linear algebra.','3 lecture hours, 2 computer lab or tutorial hours. Restricted to students in the Faculty of Engineering.'),(14,'NMM',1412,'A/B','CALCULUS FOR ENGINEERS I','Course DescriptionIntroduction to complex numbers, limits, continuity, differentiation of functions of one variable with applications, extreme values, l’Hospital’s rule, antiderivatives, definite integrals, the Fundamental Theorem of Calculus, the method of substitution.','3 lecture hours, 1 tutorial hour.Numerical and Mathematical Methods 1412A/Bis a suitable prerequisite for any course that listsCalculus 1000A/Bas prerequisite. Restricted to students in the Faculty of Engineering.'),(15,'NMM',1414,'A/B','CALCULUS FOR ENGINEERS II','Course DescriptionTechniques of integration, areas and volumes, arclength and surfaces of revolution, applications to physics and engineering, first order differential equations, parametric curves, polar coordinates, sequences and series, vectors and geometry, vector functions, partial differentiation with applications.','3 lecture hours, 1 tutorial hour.Numerical and Mathematical Methods 1414A/Bis a suitable prerequisite for any course that listsCalculus 1501A/Bas pre-requisite. Restricted to students in the Faculty of Engineering.'),(16,'COMPSCI',3388,'A/B','COMPUTER GRAPHICS I','Course DescriptionThe viewing pipeline; clipping and visibility problems. The graphical kernel system; picture generation and user interfaces.','3 lecture hours.'),(17,'COMPSCI',4442,'A/B','ARTIFICIAL INTELLIGENCE II','Course DescriptionA selection from: first order logic and theorem proving; computational linguistics; computer vision; robotics; knowledge acquisition; machine learning.','3 lecture hours.'),(18,'COMPSCI',4482,'A/B','GAME PROGRAMMING','Course DescriptionCore concepts and techniques of game programming, including the development and usage of game engines for the creation of games. Topics from: game engine architecture; real-time 2D and 3D rendering; character animation; shaders; real-time physics simulation, artificial intelligence, and networking; procedural methods; player input and controls; platform considerations; tools development.','3 lecture hours.'),(39,'COMPSCI',2208,'A/B','INTRODUCTION TO COMPUTER ORGANIZATION AND ARCHITECTURE','Course DescriptionThis course gives an understanding of what a modern computer can do. It covers the internal representation of various data types and focuses on the architectural components of computers (how these components are interconnected and the nature of the information flow between them). Assembly language is used to reinforce these issues.','3 lecture hours, 1 laboratory hour, 1 tutorial hour.'),(40,'COMPSCI',2209,'A/B','APPLIED LOGIC FOR COMPUTER SCIENCE','Course DescriptionPropositional and predicate logic; representing static and dynamic properties of real-world systems; logic as a tool for representation, reasoning and calculation; logic and programming.','3 lecture hours, 1 laboratory/tutorial hour.'),(41,'COMPSCI',2210,'A/B','DATA STRUCTURES AND ALGORITHMS','Course DescriptionLists, stacks, queues, priority queues, trees, graphs, and their associated algorithms; file structures; sorting, searching, and hashing techniques; time and space complexity.','3 lecture hours.'),(42,'COMPSCI',2211,'A/B','SOFTWARE TOOLS AND SYSTEMS  PROGRAMMING','Course DescriptionAn introduction to software tools and systems programming. Topics include: understanding how programs execute (compilation, linking and loading); an introduction to a complex operating system (UNIX); scripting languages; the C programming language; system calls; memory management; libraries; multi-component program organization and builds; version control; debuggers and profilers.','3 lecture hours, 1 laboratory/tutorial hour.'),(43,'COMPSCI',2212,'A/B','INTRODUCTION TO SOFTWARE ENGINEERING','Course DescriptionA team project course that provides practical experience in the software engineering field. Introduction to the structure and unique characteristics of large software systems, and concepts and techniques in the design, management and implementation of large software systems.','3 lecture/tutorial hours.'),(44,'COMPSCI',3305,'A/B','OPERATING SYSTEMS','Course DescriptionSurvey of major operating systems; interprocess communication; multi-tasking; scheduling; memory management; performance and measurement issues; trade-offs in operating system design; concurrency and deadlock.','3 lecture hours.'),(45,'COMPSCI',3307,'A/B','OBJECT-ORIENTED DESIGN AND ANALYSIS','Course DescriptionSoftware design and analysis techniques with particular emphasis on object-oriented design and analysis; a team project will be developed using an object-oriented language such as Java, C++ or Smalltalk.','3 lecture hours.'),(46,'COMPSCI',3331,'A/B','FOUNDATIONS OF COMPUTER SCIENCE I','Course DescriptionLanguages as sets of strings over an alphabet; operations on languages; finite automata, regular expressions; language hierarchy; Turing machines; models of computation.','3 lecture hours.'),(47,'COMPSCI',3340,'A/B','ANALYSIS OF ALGORITHMS I','Course DescriptionUpper and lower time and space bounds; levels of intractability; graph algorithms; greedy algorithms; dynamic algorithms; exhaustive search techniques; parallel algorithms.','3 lecture hours.'),(48,'COMPSCI',3342,'A/B','ORGANIZATION OF PROGRAMMING LANGUAGES','Course DescriptionSpecification and analysis of programming languages; data types and structures; bindings and access structures; run-time behavior of programs; compilation vs. interpretation. Comparative presentation of at least three programming languages addressing the above concepts.','3 lecture hours.'),(49,'COMPSCI',3350,'A/B','COMPUTER ORGANIZATION','Course DescriptionTopics include: semiconductor technologies, gates and circuits, buses, semiconductor memories, peripheral interfaces, I/O techniques, A/D conversion, standards, RISC.','3 lecture hours.'),(50,'COMPSCI',2214,'A/B','DISCRETE STRUCTURES FOR COMPUTING','Course DescriptionThis course presents an introduction to the mathematical foundations of computer science, with an emphasis on mathematical reasoning, combinatorial analysis, discrete structures, applications and modeling, and algorithmic thinking. Topics include sets, functions, relations, algorithms, number theory, matrices, mathematical reasoning, counting, graphs and trees.','3 lecture hours, 1 laboratory/tutorial hour.'),(51,'MATH',2155,'F/G','MATHEMATICAL STRUCTURES','Course DescriptionThis course provides an introduction to logical reasoning and proofs. Topics include sets, counting (permutations and combinations), mathematical induction, relations and functions, partial order relations, equivalence relations, binary operations, elementary group theory and applications to error-correcting codes.','3 lecture hours.'),(52,'WRITING',2101,'F/G','INTRODUCTION TO EXPOSITORY WRITING','Course DescriptionAn introduction to the basic principles and techniques of good writing. The course will emphasize practical work and the development of writing skills for a variety of subjects and disciplines.','3 hours.'),(53,'WRITING',2111,'F/G','WRITING IN THE WORLD:  INTRODUCTION TO PROFESSIONAL WRITING','Course DescriptionThis course will introduce students to various genres of workplace writing such as letters, memos, and reports. Topics include: employment communications (application letters and resumes); business writing style; positive, negative, and persuasive messages; cross-cultural communication; oral communication.','3 hours.'),(54,'WRITING',2125,'F/G','LET ME EXPLAIN IT TO YOU: EXPOSITION & VISUAL RHETORIC','Course DescriptionAn intensive, practical study of exposition in discursive prose, this course aims to develop students\' abilities to think critically and write persuasively using argumentation, visual rhetoric, and relevant source materials. Students consider diverse types of prose across disciplines and focus on essay development through writing, rewriting, and revision.','3 lecture hours.'),(55,'WRITING',2131,'F/G','NO BONES ABOUT IT:  WRITING IN THE SCIENCES','Course DescriptionWriting in the Sciences introduces students to the basic principles and genres of writing required for science students in their undergraduate careers: lab reports, summaries of scientific research, and scientific review essays. The course will focus on drafting and revising various reports written on scientific topics.','3 hours.'),(56,'COMPSCI',4490,'Z','THESIS','Course DescriptionA project or research paper completed with minimal faculty supervision. An oral presentation plus a written submission will be required.','3 lecture hours.'),(57,'DATASCI',3000,'A/B','INTRODUCTION TO MACHINE LEARNING','Course DescriptionBasic principles of machine learning (estimation, optimization, prediction, generalization, bias-variance trade-off, regularization) in the context of supervised (linear models, decision trees, deep neuronal networks) and unsupervised (clustering and dimensionality reduction) statistical learning techniques. The course emphasizes the ability to apply techniques to real data sets and critically evaluate their performance.','2 lecture hours/week, 2 lab hour/week. For a full list of Introductory Statistics courses please see: https://www.westerncalendar.uwo.ca/Departments.cfm?DepartmentID=55&SelectedCalendar=Live&ArchiveID='),(58,'SCIENCE',3377,'A/B','PROJECT MANAGEMENT FOR THE SCIENCES','Course DescriptionFundamental techniques, theories, and tools for managing successful projects in the Sciences. Project management standards and life cycles; resourcing, scheduling and estimating techniques for project management; project management organizational concerns, including project economic analysis, human resources, proposal development, risk management, funding models, procurement, and strategic alignments.','3 lecture hours.'),(59,'MATH',2156,'A/B','MATHEMATICAL STRUCTURES II','Course DescriptionThis course continues the development of logical reasoning and proofs begun inMathematics 2155F/G. Topics include elementary number theory (gcd, lcm, Euclidean algorithm, congruences, Chinese remainder theorem) and graph theory (connectedness, complete, regular and bipartite graphs; trees and spanning trees, Eulerian and Hamiltonian graphs, planar graphs; vertex, face and edge colouring; chromatic polynomials).','3 lecture hours.'),(60,'MATH',3159,'A/B','INTRODUCTION TO CRYPTOGRAPHY','Course DescriptionModern cryptological algorithms will be discussed with an emphasis placed on their mathematical foundation. Main topics will include: basic number theory, complexity of algorithms, symmetric-key cryptosystems, public-key cryptosystems, RSA encryption, primality and factoring, discrete logarithms, elliptic curves and information theory.','3 lecture hours.'),(61,'STATS',2141,'A/B','APPLIED PROBABILITY AND STATISTICS FOR ENGINEERS','Course DescriptionAn introduction to statistics with emphasis on the applied probability models used in Electrical and Civil Engineering and elsewhere.  Topics covered include samples, probability, probability distributions, estimation (including comparison of means), correlation and regression.','3 lecture hours, 1 tutorial hour. This course cannot be taken for credit in any module in Data Science, Statistics, Actuarial Science, or Financial Modelling, other than the Minor in Applied Statistics, the Minor in Applied Financial Modeling, the Minor in Data Science, or the Certificate in Data Science.'),(62,'STATS',2244,'A/B','STATISTICS FOR SCIENCE','Course DescriptionAn introductory course in the application of statistical methods, intended for students in departments other than Statistical and Actuarial Sciences, Applied Mathematics, Mathematics, or students in the Faculty of Engineering. Topics include sampling, confidence intervals, analysis of variance, regression and correlation.','2 lecture hours, 3 lab hours. This course cannot be taken for credit in any module in Data Science, Statistics, Actuarial Science, or Financial Modelling other than the Minor in Applied Statistics, the Minor in Data Science, or the Certificate in Data Science.'),(63,'BIOLOGY',2244,'A/B','STATISTICS FOR SCIENCE','Course DescriptionAn introductory course in the application of statistical methods, intended for students in departments other than Statistical and Actuarial Sciences, Applied Mathematics, Mathematics, or students in the Faculty of Engineering. Topics include sampling, confidence intervals, analysis of variance, regression and correlation.','2 lecture hours, 3 laboratory hours. It may NOT be used in any degree as a 2000-level half course in Biology with a laboratory component.Biology 2244A/Band Statistics 2244A/B are the same, cross-listed courses.'),(64,'STATS',2857,'A/B','PROBABILITY AND STATISTICS I','Course DescriptionProbability axioms, conditional probability, Bayes\' theorem. Random variables motivated by real data and examples. Parametric univariate models as data reduction and description strategies. Multivariate distributions, expectation and variance. Likelihood function will be defined and exploited as a means of estimating parameters in certain simple situations.','3 lecture hours, 1 tutorial hour.'),(65,'COMPSCI',4470,'Y','SOFTWARE MAINTENANCE AND CONFIGURATION MANAGMENT','Course DescriptionAn examination of industrial-style software development issues related to managing and maintaining large-scale software systems; in a group project, students will examine software maintenance and configuration management concepts, tools, techniques, risks and benefits; case studies.','3 lecture hours.');
/*!40000 ALTER TABLE `Course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CourseCategory`
--

DROP TABLE IF EXISTS `CourseCategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CourseCategory` (
  `category` char(1) NOT NULL,
  PRIMARY KEY (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CourseCategory`
--

LOCK TABLES `CourseCategory` WRITE;
/*!40000 ALTER TABLE `CourseCategory` DISABLE KEYS */;
INSERT INTO `CourseCategory` VALUES ('A'),('B'),('C'),('Y'),('Z');
/*!40000 ALTER TABLE `CourseCategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CourseSuffix`
--

DROP TABLE IF EXISTS `CourseSuffix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CourseSuffix` (
  `suffix` varchar(255) NOT NULL,
  `credit` decimal(5,2) NOT NULL,
  `is_essay` bit(1) NOT NULL,
  PRIMARY KEY (`suffix`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CourseSuffix`
--

LOCK TABLES `CourseSuffix` WRITE;
/*!40000 ALTER TABLE `CourseSuffix` DISABLE KEYS */;
INSERT INTO `CourseSuffix` VALUES ('',1.00,_binary '\0'),('A',0.50,_binary '\0'),('A/B',0.50,_binary '\0'),('A/B/Y',0.50,_binary '\0'),('B',0.50,_binary '\0'),('E',1.00,_binary ''),('F',0.50,_binary ''),('F/G',0.50,_binary ''),('G',0.50,_binary ''),('Y',0.50,_binary '\0'),('Z',0.50,_binary '');
/*!40000 ALTER TABLE `CourseSuffix` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Module`
--

DROP TABLE IF EXISTS `Module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Module` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `IdxModuleName` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Module`
--

LOCK TABLES `Module` WRITE;
/*!40000 ALTER TABLE `Module` DISABLE KEYS */;
INSERT INTO `Module` VALUES (1,'HONOURS SPECIALIZATION IN COMPUTER SCIENCE');
/*!40000 ALTER TABLE `Module` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ModuleRequirement`
--

DROP TABLE IF EXISTS `ModuleRequirement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ModuleRequirement` (
  `id` int NOT NULL AUTO_INCREMENT,
  `module_id` int NOT NULL,
  `total_credit` decimal(5,2) NOT NULL,
  `minimum_grade` int DEFAULT NULL,
  `required_average` int DEFAULT NULL,
  `is_admission` bit(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `modulerequirement_ibfk_1` FOREIGN KEY (`module_id`) REFERENCES `Module` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ModuleRequirement`
--

LOCK TABLES `ModuleRequirement` WRITE;
/*!40000 ALTER TABLE `ModuleRequirement` DISABLE KEYS */;
INSERT INTO `ModuleRequirement` VALUES (1,1,0.50,65,NULL,_binary ''),(2,1,0.50,65,NULL,_binary ''),(3,1,1.00,NULL,NULL,_binary ''),(4,1,5.50,NULL,NULL,_binary '\0'),(5,1,0.50,NULL,NULL,_binary '\0'),(6,1,0.50,NULL,NULL,_binary '\0'),(7,1,0.50,NULL,NULL,_binary '\0'),(8,1,1.00,NULL,NULL,_binary '\0'),(9,1,0.50,NULL,NULL,_binary '\0'),(10,1,0.50,NULL,NULL,_binary '\0');
/*!40000 ALTER TABLE `ModuleRequirement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ModuleRequirementCourse`
--

DROP TABLE IF EXISTS `ModuleRequirementCourse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ModuleRequirementCourse` (
  `requirement_id` int NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`requirement_id`,`course_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `modulerequirementcourse_ibfk_1` FOREIGN KEY (`requirement_id`) REFERENCES `ModuleRequirement` (`id`),
  CONSTRAINT `modulerequirementcourse_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `Course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ModuleRequirementCourse`
--

LOCK TABLES `ModuleRequirementCourse` WRITE;
/*!40000 ALTER TABLE `ModuleRequirementCourse` DISABLE KEYS */;
INSERT INTO `ModuleRequirementCourse` VALUES (1,1),(1,2),(1,3),(1,4),(2,5),(2,6),(3,7),(3,8),(3,9),(3,10),(3,11),(3,12),(3,13),(3,14),(3,15),(4,39),(4,40),(4,41),(4,42),(4,43),(4,44),(4,45),(4,46),(4,47),(4,48),(4,49),(5,50),(5,51),(6,52),(6,53),(6,54),(6,55),(7,56),(8,57),(9,58),(9,59),(9,60),(10,61),(10,62),(10,63),(10,64);
/*!40000 ALTER TABLE `ModuleRequirementCourse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ModuleRequirementSubject`
--

DROP TABLE IF EXISTS `ModuleRequirementSubject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ModuleRequirementSubject` (
  `id` int NOT NULL AUTO_INCREMENT,
  `requirement_id` int NOT NULL,
  `subject_code` varchar(255) NOT NULL,
  `minimum_level` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `requirement_id` (`requirement_id`),
  KEY `subject_code` (`subject_code`),
  CONSTRAINT `modulerequirementsubject_ibfk_1` FOREIGN KEY (`requirement_id`) REFERENCES `ModuleRequirement` (`id`),
  CONSTRAINT `modulerequirementsubject_ibfk_2` FOREIGN KEY (`subject_code`) REFERENCES `Subject` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ModuleRequirementSubject`
--

LOCK TABLES `ModuleRequirementSubject` WRITE;
/*!40000 ALTER TABLE `ModuleRequirementSubject` DISABLE KEYS */;
/*!40000 ALTER TABLE `ModuleRequirementSubject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Prerequisite`
--

DROP TABLE IF EXISTS `Prerequisite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Prerequisite` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `total_credit` decimal(5,2) NOT NULL,
  `minimum_grade` int DEFAULT NULL,
  `alternative_to` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  KEY `alternative_to` (`alternative_to`),
  CONSTRAINT `prerequisite_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `Course` (`id`),
  CONSTRAINT `prerequisite_ibfk_2` FOREIGN KEY (`alternative_to`) REFERENCES `Prerequisite` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Prerequisite`
--

LOCK TABLES `Prerequisite` WRITE;
/*!40000 ALTER TABLE `Prerequisite` DISABLE KEYS */;
/*!40000 ALTER TABLE `Prerequisite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PrerequisiteCourse`
--

DROP TABLE IF EXISTS `PrerequisiteCourse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PrerequisiteCourse` (
  `prerequisite_id` int NOT NULL,
  `required_course_id` int NOT NULL,
  PRIMARY KEY (`prerequisite_id`,`required_course_id`),
  KEY `required_course_id` (`required_course_id`),
  CONSTRAINT `prerequisitecourse_ibfk_1` FOREIGN KEY (`prerequisite_id`) REFERENCES `Prerequisite` (`id`),
  CONSTRAINT `prerequisitecourse_ibfk_2` FOREIGN KEY (`required_course_id`) REFERENCES `Course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PrerequisiteCourse`
--

LOCK TABLES `PrerequisiteCourse` WRITE;
/*!40000 ALTER TABLE `PrerequisiteCourse` DISABLE KEYS */;
/*!40000 ALTER TABLE `PrerequisiteCourse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Subject`
--

DROP TABLE IF EXISTS `Subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Subject` (
  `code` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `category` char(1) DEFAULT NULL,
  `category_2` char(1) DEFAULT NULL,
  PRIMARY KEY (`code`),
  UNIQUE KEY `name` (`name`),
  KEY `category` (`category`),
  KEY `category_2` (`category_2`),
  CONSTRAINT `subject_ibfk_1` FOREIGN KEY (`category`) REFERENCES `CourseCategory` (`category`),
  CONSTRAINT `subject_ibfk_2` FOREIGN KEY (`category_2`) REFERENCES `CourseCategory` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Subject`
--

LOCK TABLES `Subject` WRITE;
/*!40000 ALTER TABLE `Subject` DISABLE KEYS */;
INSERT INTO `Subject` VALUES ('ACTURSCI','Actuarial Science','C',NULL),('ADS','Analytics and Decision Sciences','A',NULL),('AH','Art History','B',NULL),('AISE','Artificial Intelligence Systems Engineering','C',NULL),('AMERICAN','American Studies','A',NULL),('ANATCELL','Anatomy and Cell Biology','C',NULL),('ANTHRO','Anthropology','A',NULL),('APPLMATH','Applied Mathematics','C',NULL),('ARABIC','Arabic','B',NULL),('ARTHUM','Arts and Humanities','B',NULL),('ASL','American Sign Language','B',NULL),('ASTRONOM','Astronomy','C',NULL),('BIOCHEM','Biochemistry','C',NULL),('BIOLOGY','Biology','C',NULL),('BIOSTATS','Biostatistics','C',NULL),('BME','Biomedical Engineering','C',NULL),('BUSINESS','Business Administration','A',NULL),('CA','Creative Arts','A','B'),('CALCULUS','Calculus','C',NULL),('CANADIAN','Canadian Studies','A',NULL),('CBE','Chemical and Biochemical Engineering','C',NULL),('CEE','Civil and Environmental Engineering','C',NULL),('CGS','Centre for Global Studies','A',NULL),('CHEM','Chemistry','C',NULL),('CHEMBIO','Chemical Biology','C',NULL),('CHINESE','Chinese','B',NULL),('CLASSICS','Classical Studies','B',NULL),('COMMSCI','Communication Sciences and Disorders','C',NULL),('COMPLIT','Comparative Literature and Culture','B',NULL),('COMPSCI','Computer Science','C',NULL),('CYS','Childhood and Youth Studies','A',NULL),('DANCE','Dance','A',NULL),('DATASCI','Data Science','C',NULL),('DIGICOMM','Digital Communication','A',NULL),('DIGIHUM','Digital Humanities','B',NULL),('DISABST','Disability Studies','A',NULL),('EARTHSCI','Earth Sciences','C',NULL),('ECE','Electrical and Computer Engineering','C',NULL),('ECONOMIC','Economics','A',NULL),('EDUC','Education','A',NULL),('ELI','Engineering Leadership and Innovation','C',NULL),('ENGLISH','English','B',NULL),('ENGSCI','Engineering Science','C',NULL),('ENVIRSCI','Environmental Science','C',NULL),('EPID','Epidemiology','C',NULL),('EPIDEMIO','Epidemiology and Biostatistics','C',NULL),('FAMLYSTU','Family Studies and Human Development','A',NULL),('FILM','Film Studies','B',NULL),('FIMS','Faculty of Information and Media Studies','A',NULL),('FINMOD','Financial Modelling','C',NULL),('FOODNUTR','Foods and Nutrition','A',NULL),('FRENCH','French','B',NULL),('GEOGRAPH','Geography','A',NULL),('GERMAN','German','B',NULL),('GGB','Global Great Books','B',NULL),('GLE','Governance, Leadership and Ethics','A',NULL),('GREEK','Greek','B',NULL),('GSWS','Gender, Sexuality, and Women’s Studies','A','B'),('HEALTSCI','Health Sciences','A',NULL),('HEBREW','Hebrew','B',NULL),('HINDI','Hindi','B',NULL),('HISTORY','History','A',NULL),('HISTSCI','History of Science','C',NULL),('HUMANECO','Human Ecology','A',NULL),('HUMANIT','Humanitie',NULL,NULL),('HUMANRS','Human Rights Studies','A',NULL),('ICC','Intercultural Communications','B',NULL),('IE','Integrated Engineering','C',NULL),('INDIGSTU','Indigenous Studies','A',NULL),('INTEGSCI','Integrated Science','C',NULL),('INTERDIS','Interdisciplinary Studies','A',NULL),('INTREL','International Relations','A',NULL),('ITALIAN','Italian','B',NULL),('ITALST','Italian Studies','B',NULL),('JAPANESE','Japanese','B',NULL),('JEWISH','Jewish Studies','A',NULL),('KINESIOL','Kinesiology','A',NULL),('KOREAN','Korean','B',NULL),('LATIN','Latin','B',NULL),('LAW','Law','A',NULL),('LINGUIST','Linguistics','A','B'),('LS','Leadership Studies','A',NULL),('MATH','Mathematics','C',NULL),('MBI','Medical Bioinformatics','C',NULL),('MCS','Museum and Curatorial Studies','B',NULL),('MEDBIO','Medical Biophysics','C',NULL),('MEDIEVAL','Medieval Studies','B',NULL),('MEDSCIEN','Medical Sciences','C',NULL),('MICROIMM','Microbiology and Immunology','C',NULL),('MIT','Media, Information and Technoculture','A',NULL),('MME','Mechanical and Materials Engineering','C',NULL),('MOS','Management and Organizational Studies','A',NULL),('MSE','Mechatronic Systems Engineering','C',NULL),('MUSIC','Music','A',NULL),('NEURO','Neuroscience','C',NULL),('NMM','Numerical and Mathematical Methods','C',NULL),('NURSING','Nursing','A',NULL),('ONEHEALT','One Health','C',NULL),('PATHOL','Pathology','C',NULL),('PERSIAN','Persian','B',NULL),('PHARM','Pharmacology','C',NULL),('PHILOSOP','Philosophy','B',NULL),('PHYSICS','Physics','C',NULL),('PHYSIOL','Physiology','C',NULL),('PHYSPHRM','Physiology and Pharmacology','C',NULL),('POLISCI','Political Science','A',NULL),('PORTUGSE','Portuguese','B',NULL),('PPE','Politics, Philosophy, and Economics','A',NULL),('PSYCHOL','Psychology','A',NULL),('REHABSCI','Rehabilitation Sciences','A',NULL),('RELSTUD','Religious Studies','B',NULL),('RUSSIAN','Russian','B',NULL),('SA','Studio Art','B',NULL),('SCHOLARS','Scholars Elective',NULL,NULL),('SCIENCE','Science','C',NULL),('SE','Software Engineering','C',NULL),('SOCIOLOG','Sociology','A',NULL),('SOCLJUST','Social Justice and Peace Studies','A',NULL),('SOCSCI','Social Science','A',NULL),('SOCWORK','Social Work','A',NULL),('SPANISH','Spanish','B',NULL),('SPEECH','Speech','B',NULL),('STATS','Statistical Sciences','C',NULL),('THANAT','Thanatology','A',NULL),('THEATRE','Theatre Studies','B',NULL),('THEOLST','Theological Studies','B',NULL),('TJ','Transitional Justice','A',NULL),('TNLA','The New Liberal Arts','B',NULL),('WORLDLIT','World Literatures and Cultures','B',NULL),('WRITING','Writing','B',NULL);
/*!40000 ALTER TABLE `Subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vcourse`
--

DROP TABLE IF EXISTS `vcourse`;
/*!50001 DROP VIEW IF EXISTS `vcourse`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vcourse` AS SELECT 
 1 AS `id`,
 1 AS `subject_code`,
 1 AS `subject_name`,
 1 AS `number`,
 1 AS `suffix`,
 1 AS `credit`,
 1 AS `is_essay`,
 1 AS `category`,
 1 AS `category_2`,
 1 AS `name`,
 1 AS `description`,
 1 AS `extra_information`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vcourse`
--

/*!50001 DROP VIEW IF EXISTS `vcourse`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vcourse` AS select `course`.`id` AS `id`,`course`.`subject_code` AS `subject_code`,`subject`.`name` AS `subject_name`,`course`.`number` AS `number`,`course`.`suffix` AS `suffix`,`coursesuffix`.`credit` AS `credit`,`coursesuffix`.`is_essay` AS `is_essay`,`subject`.`category` AS `category`,`subject`.`category_2` AS `category_2`,`course`.`name` AS `name`,`course`.`description` AS `description`,`course`.`extra_information` AS `extra_information` from ((`course` left join `subject` on((`subject`.`code` = `course`.`subject_code`))) left join `coursesuffix` on((`coursesuffix`.`suffix` = `course`.`suffix`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-02 15:36:57
