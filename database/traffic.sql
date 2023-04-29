-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 29, 2023 at 06:10 PM
-- Server version: 5.7.36
-- PHP Version: 8.0.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `traffic`
--

-- --------------------------------------------------------

--
-- Table structure for table `best_results`
--

CREATE TABLE `best_results` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `iterations` int(11) NOT NULL,
  `phases` json NOT NULL,
  `fitness` decimal(20,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `optimization_id` int(11) DEFAULT '6'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `iterations`
--

CREATE TABLE `iterations` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `optimization_id` bigint(20) UNSIGNED NOT NULL,
  `iterations` int(11) NOT NULL,
  `steps` int(11) NOT NULL,
  `avg_phase` decimal(20,2) NOT NULL,
  `waiting_time` decimal(20,2) NOT NULL,
  `travel_time` decimal(20,2) NOT NULL,
  `total_delay` decimal(8,2) NOT NULL,
  `num_stops` int(11) NOT NULL,
  `co2_emission` decimal(20,2) NOT NULL,
  `co_emission` decimal(20,2) NOT NULL,
  `fuel_consumption` decimal(20,2) NOT NULL,
  `noise_emission` decimal(20,2) NOT NULL,
  `arrived_cars` int(11) NOT NULL,
  `departed_cars` int(11) NOT NULL,
  `current_simulation_time` decimal(20,2) NOT NULL,
  `phases` json NOT NULL,
  `fitness` decimal(20,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `best_results`
--
ALTER TABLE `best_results`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `iterations`
--
ALTER TABLE `iterations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `iterations_optimization_id_foreign` (`optimization_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `best_results`
--
ALTER TABLE `best_results`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `iterations`
--
ALTER TABLE `iterations`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
