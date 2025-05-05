-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 26, 2025 at 08:21 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `25newfacebankdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `beneficiarytb`
--

CREATE TABLE `beneficiarytb` (
  `id` bigint(250) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `AccName` varchar(250) NOT NULL,
  `AccountNo` varchar(250) NOT NULL,
  `IfscCode` varchar(250) NOT NULL,
  `BankName` varchar(250) NOT NULL,
  `Address` varchar(2000) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `beneficiarytb`
--

INSERT INTO `beneficiarytb` (`id`, `UserName`, `AccName`, `AccountNo`, `IfscCode`, `BankName`, `Address`) VALUES
(1, 'sangeeth', 'sangeeth123', '9486365535357', 'iFSC78900', 'sbi', 'saf'),
(2, 'sangeeth', 'sangeeth123', '9486365535357', 'iFSC78900', 'sbi', 'saf');

-- --------------------------------------------------------

--
-- Table structure for table `multitb`
--

CREATE TABLE `multitb` (
  `id` bigint(10) NOT NULL auto_increment,
  `Account` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `multitb`
--

INSERT INTO `multitb` (`id`, `Account`, `UserName`) VALUES
(1, '9486365535357', 'san'),
(2, '948636553535788', 'sangeeth');

-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `id` bigint(50) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Age` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `AccountNo` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Pin` varchar(250) NOT NULL,
  `Status` varchar(250) NOT NULL,
  `Balance` decimal(20,2) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`id`, `Name`, `Age`, `Mobile`, `Email`, `Address`, `AccountNo`, `UserName`, `Password`, `Pin`, `Status`, `Balance`) VALUES
(1, 'sangeeth Kumar', '23', '9486365535', 'sangeeth5535@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', '9486365535357', 'san', 'san', '1234', 'Active', '0.00'),
(2, 'sangeeth Kumar', '23', '9486365535', 'sangeeth5535@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', '948636553535788', 'sangeeth', 'sangeeth', '1234', 'Active', '6400.00');

-- --------------------------------------------------------

--
-- Table structure for table `temptb`
--

CREATE TABLE `temptb` (
  `id` bigint(10) NOT NULL auto_increment,
  `AccountNo` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `OTP` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `temptb`
--


-- --------------------------------------------------------

--
-- Table structure for table `transtb`
--

CREATE TABLE `transtb` (
  `id` bigint(20) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `AccountNo` varchar(250) NOT NULL,
  `BName` varchar(250) NOT NULL,
  `BAccountNo` varchar(250) NOT NULL,
  `Currency` varchar(250) NOT NULL,
  `Date` varchar(250) NOT NULL,
  `Hash1` varchar(250) NOT NULL,
  `Hash2` varchar(250) NOT NULL,
  `Type` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `transtb`
--

INSERT INTO `transtb` (`id`, `UserName`, `AccountNo`, `BName`, `BAccountNo`, `Currency`, `Date`, `Hash1`, `Hash2`, `Type`) VALUES
(1, 'sangeeth', '948636553535788', 'sangeeth', '948636553535788', '8000', '2025-Apr-26', '0', '17C1B67142FDC66FF9131E6532449CC57B5CEC4A23F61DEF1EB0A48162AA6FFA', 'Deposit'),
(2, 'sangeeth', '948636553535788', 'sangeeth123', '9486365535357', '800', '2025-Apr-26', '17C1B67142FDC66FF9131E6532449CC57B5CEC4A23F61DEF1EB0A48162AA6FFA', '6535B5AAC48684C62B8B2B059BF21A32DCFA29FFFE9A16491AF6D94745DBD425', 'Transaction'),
(3, 'sangeeth', '948636553535788', 'sangeeth', '948636553535788', '800', '2025-Apr-26', '6535B5AAC48684C62B8B2B059BF21A32DCFA29FFFE9A16491AF6D94745DBD425', 'A1BFA1665F464490B3412A041A8ADE2E4AF558F70F2988DF3EA2B794C210B258', 'Withdraw');
