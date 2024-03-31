-- Initial database design done by Kiran Timalsina for first git push

-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 31, 2024 at 05:49 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tst-echallan`
--

-- --------------------------------------------------------

--
-- Table structure for table `challanhistory`
--

CREATE TABLE `challanhistory` (
  `challannumber` varchar(255) NOT NULL,
  `registrationNumber` varchar(255) DEFAULT NULL,
  `violationReason` varchar(255) DEFAULT NULL,
  `violationId` varchar(255) DEFAULT NULL,
  `chargedAmount` decimal(10,2) DEFAULT NULL,
  `dateIssued` date DEFAULT NULL,
    `issuedLocation` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `officer`
--

CREATE TABLE `officer` (
  `officerId` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `badgeNumber` varchar(255) DEFAULT NULL,
  `rank` varchar(255) DEFAULT NULL,
  `assignedLocation` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userid` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `usertype` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `vehicle`
--

CREATE TABLE `vehicle` (
  `vehicleId` varchar(255) NOT NULL,
  `RegistrationId` int(11) DEFAULT NULL,
  `RegistrationNumber` varchar(255) DEFAULT NULL,
  `registrationdate` date DEFAULT NULL,
  `vehicleType` varchar(255) DEFAULT NULL,
  `vehicleMake` varchar(255) DEFAULT NULL,
  `VehicleModel` varchar(255) DEFAULT NULL,
  `ChasisNumber` varchar(255) DEFAULT NULL,
  `EngineNumber` varchar(255) DEFAULT NULL,
  `VehicleCategory` varchar(255) DEFAULT NULL,
  `VehicleCustomtaxId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `vehicleowner`
--

CREATE TABLE `vehicleowner` (
  `vehicleid` varchar(255) DEFAULT NULL,
  `registrationNumber` varchar(255) NOT NULL,
  `citizenId` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `RegistrationExp` date DEFAULT NULL,
  `RegistrationStatus` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `challanhistory`
--
ALTER TABLE `challanhistory`
  ADD PRIMARY KEY (`challannumber`),
  ADD KEY `registrationNumber` (`registrationNumber`);

--
-- Indexes for table `officer`
--
ALTER TABLE `officer`
  ADD PRIMARY KEY (`officerId`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userid`);

--
-- Indexes for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD PRIMARY KEY (`vehicleId`);

--
-- Indexes for table `vehicleowner`
--
ALTER TABLE `vehicleowner`
  ADD PRIMARY KEY (`registrationNumber`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `challanhistory`
--
ALTER TABLE `challanhistory`
  ADD CONSTRAINT `challanhistory_ibfk_1` FOREIGN KEY (`registrationNumber`) REFERENCES `vehicleowner` (`registrationNumber`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
