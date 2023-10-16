-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.7.3-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping database structure for wal-sales-orders
CREATE DATABASE IF NOT EXISTS `cpc-sales-orders` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci */;
USE `cpc-sales-orders`;

-- Dumping structure for table wal-sales-orders.event_logs
CREATE TABLE IF NOT EXISTS `event_logs` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `content` varchar(5000) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `time` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1227 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;


-- Dumping structure for table wal-sales-orders.event_type
CREATE TABLE IF NOT EXISTS `event_type` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_type` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  PRIMARY KEY (`event_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;


-- Dumping structure for table wal-sales-orders.shopifyorders
CREATE TABLE IF NOT EXISTS `shopifyorders` (
  `home_number` int(11) DEFAULT NULL,
  `id` bigint(20) DEFAULT NULL,
  `subject_id` bigint(20) DEFAULT NULL,
  `created_at` text COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `message` text COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `pushed` tinyint(4) DEFAULT NULL,
  `last_item` tinyint(4) DEFAULT NULL,
  `attempts` int(11) DEFAULT 1,
  `accountancy_push` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

-- Dumping structure for table wal-sales-orders.sku_unit_cost
CREATE TABLE IF NOT EXISTS `sku_unit_cost` (
  `sku` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `unit_cost` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

/*!40000 ALTER TABLE `sku_unit_cost` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
