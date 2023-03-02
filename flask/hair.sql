-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 28, 2023 at 09:44 AM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 7.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hair`
--

-- --------------------------------------------------------

--
-- Table structure for table `history`
--

CREATE TABLE `history` (
  `id` int(11) NOT NULL,
  `image` varchar(255) NOT NULL,
  `face` varchar(255) NOT NULL,
  `timestamp` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `history`
--

INSERT INTO `history` (`id`, `image`, `face`, `timestamp`) VALUES
(47, '1673882751139719.jpg', 'Square', '1673882751.139719'),
(48, '1673884859986104.jpg', 'Diamond', '1673884859.986104'),
(49, '1673885565805276.jpg', 'Round', '1673885565.805276'),
(50, '1673885702923879.jpg', 'Oval', '1673885702.923879'),
(51, '1673887213735568.jpg', 'Square', '1673887213.735568'),
(52, '167392813731571.jpg', 'Round', '1673928137.31571'),
(53, '1673928636087535.jpg', 'Triangle', '1673928636.087535'),
(54, '1673928663284435.jpg', 'Oblong', '1673928663.284435'),
(55, '1674003239671241.jpg', 'Square', '1674003239.671241'),
(56, '167400326126015.jpg', 'Triangle', '1674003261.26015'),
(57, '1674003968004744.jpg', 'Oblong', '1674003968.004744'),
(58, '1674004548911226.jpg', 'Heart', '1674004548.911226'),
(59, '1674004574608552.jpg', 'Oblong', '1674004574.608552'),
(60, '1674005223435392.jpg', 'Diamond', '1674005223.435392'),
(61, '1674007828223077.jpg', 'Round', '1674007828.223077'),
(62, '1674007927654443.jpg', 'Oblong', '1674007927.654443'),
(63, '1674007958588613.jpg', 'Oblong', '1674007958.588613'),
(64, '1674008015542696.jpg', 'Oval', '1674008015.542696'),
(65, '1674008064257167.jpg', 'Oblong', '1674008064.257167'),
(66, '1674137641543183.jpg', 'Round', '1674137641.543183'),
(67, '1674137811653606.jpg', 'Diamond', '1674137811.653606'),
(68, '1674137836087402.jpg', 'Round', '1674137836.087402'),
(69, '1674893477722141.jpg', 'Oval', '1674893477.722141'),
(70, '1674893512919911.jpg', 'Diamond', '1674893512.919911');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `username`, `password`) VALUES
(1, 'hair@gmail.com', 'admin', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `history`
--
ALTER TABLE `history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=71;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
