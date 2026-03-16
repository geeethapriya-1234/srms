-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 15, 2026 at 10:53 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `srms`
--

-- --------------------------------------------------------

--
-- Table structure for table `departments`
--

CREATE TABLE `departments` (
  `ID` int(11) NOT NULL COMMENT 'AUTO_INCREMENT',
  `DEPT_NAME` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `departments`
--

INSERT INTO `departments` (`ID`, `DEPT_NAME`) VALUES
(1, 'CSE'),
(2, 'ECE'),
(3, 'CHEMICAL');

-- --------------------------------------------------------

--
-- Table structure for table `marks`
--

CREATE TABLE `marks` (
  `regno` varchar(50) NOT NULL,
  `subject` varchar(50) NOT NULL,
  `semester` int(11) DEFAULT NULL,
  `total` int(50) NOT NULL,
  `grade_point` varchar(50) NOT NULL,
  `percentage` float NOT NULL,
  `CGPA` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `marks`
--

INSERT INTO `marks` (`regno`, `subject`, `semester`, `total`, `grade_point`, `percentage`, `CGPA`) VALUES
('CSE001', 'MATHEMATICS', 1, 85, '9', 85, 9),
('CSE001', 'JAVA', 1, 92, '10', 92, 9),
('CSE001', 'PYTHON', 2, 78, '8', 78, 9),
('CSE001', 'DBMS', 2, 88, '9', 88, 9),
('CSE001', 'OPERATING SYSTEM', 3, 95, '10', 95, 9),
('CSE002', 'S1', 3, 99, '10', 99, 0),
('CSE002', 'S2', 3, 98, '10', 98, 0),
('CSE002', 'S3', 3, 97, '10', 97, 0),
('CSE002', 'S4', 3, 96, '10', 96, 0),
('CSE002', 'S5', 3, 95, '10', 95, 0),
('CSE003', 'S1', 1, 99, '10', 99, 0),
('CSE003', 'S2', 1, 98, '10', 98, 0),
('CSE003', 'S3', 1, 97, '10', 97, 0),
('CSE003', 'S4', 1, 96, '10', 96, 0),
('CSE003', 'S5', 1, 95, '10', 95, 0),
('CSE003', 'S1', 1, 99, '10', 99, 0),
('CSE003', 'S2', 1, 98, '10', 98, 0),
('CSE003', 'S3', 1, 97, '10', 97, 0),
('CSE003', 'S4', 1, 96, '10', 96, 0),
('CSE003', 'S5', 1, 95, '10', 95, 0),
('CSE003', 'S1', 1, 99, '10', 99, 0),
('CSE003', 'S2', 1, 98, '10', 98, 0),
('CSE003', 'S3', 1, 97, '10', 97, 0),
('CSE003', 'S4', 1, 96, '10', 96, 0),
('CSE003', 'S5', 1, 95, '10', 95, 0),
('CSE003', 'S1', 1, 99, '10', 99, 0),
('CSE003', 'S2', 1, 98, '10', 98, 0),
('CSE003', 'S3', 1, 97, '10', 97, 0),
('CSE003', 'S4', 1, 96, '10', 96, 0),
('CSE003', 'S5', 1, 95, '10', 95, 0);

-- --------------------------------------------------------

--
-- Table structure for table `semesters`
--

CREATE TABLE `semesters` (
  `ID` int(11) NOT NULL COMMENT 'AUTO_INCREMENT',
  `SEM_NAME` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `semesters`
--

INSERT INTO `semesters` (`ID`, `SEM_NAME`) VALUES
(1, '1'),
(2, '2'),
(3, '3');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL COMMENT 'auto_increment',
  `regno` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `department` varchar(50) NOT NULL,
  `semester` int(20) NOT NULL,
  `password` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `regno`, `name`, `department`, `semester`, `password`) VALUES
(1, '6362', 'GEETHA', 'CSE', 6, '1234'),
(2, 'CSE001', 'PRIYA', 'CSE', 5, '1234'),
(0, 'CSE003', 'ANKITA', '1', 1, '1234');

-- --------------------------------------------------------

--
-- Table structure for table `teachers`
--

CREATE TABLE `teachers` (
  `ID` int(20) NOT NULL COMMENT 'AUTO_INCREMENT',
  `NAME` varchar(100) NOT NULL,
  `department` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teachers`
--

INSERT INTO `teachers` (`ID`, `NAME`, `department`) VALUES
(0, 'RAVICHANDRAN', 'CSE'),
(0, 'MEHALA', 'CSE'),
(0, 'ASHOK', 'CSE'),
(0, 'KESAVPRASANTH', 'CSE');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` varchar(11) NOT NULL COMMENT 'AUTO_INCREMENT',
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
('0', 'admin', 'admin123', 'admin'),
('0', 'teacher', '123', 'teacher'),
('3', '6362', 'geetha', 'student');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
