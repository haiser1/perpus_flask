-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: perpus
-- ------------------------------------------------------
-- Server version	8.0.33-0ubuntu0.22.04.2

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
-- Table structure for table `anggota`
--

DROP TABLE IF EXISTS `anggota`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anggota` (
  `nim` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `nama` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `alamat` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `no_tlp` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `role` varchar(10) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'user',
  `id_petugas` int NOT NULL,
  PRIMARY KEY (`nim`),
  KEY `fk_anggota_petugas` (`id_petugas`),
  CONSTRAINT `fk_anggota_petugas` FOREIGN KEY (`id_petugas`) REFERENCES `petugas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anggota`
--

LOCK TABLES `anggota` WRITE;
/*!40000 ALTER TABLE `anggota` DISABLE KEYS */;
INSERT INTO `anggota` VALUES ('21.83.1234','dadang','dadang@gmail.com','pbkdf2:sha256:600000$GrMnAOHRT8JCTIzs$598091807b3adf577d58d82822893bb337dbc26afee2e0423a0973dcdabf7cad','bantul','1234','user',3),('21.83.1235','muklis','muklis@gmail.com','pbkdf2:sha256:600000$KfaWW3WbOL2OzYaj$e743fb4d58a28f2a8149c4d7be47858fba27eb9bf1326514ac36ce43ece0ebc6','bantul','081235','user',4),('21.83.1237','Dobleh','dobleh@gmail.com','pbkdf2:sha256:600000$PZKvf6XSmEiwcXph$e5bd82108c37ecc9b528f3bc6ecc60fca6bf812aedf23495c085b29fdccf8568','jogja','08123467','user',3);
/*!40000 ALTER TABLE `anggota` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `buku`
--

DROP TABLE IF EXISTS `buku`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buku` (
  `judul_buku` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `uuid` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `penulis` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `penerbit` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `tahun_terbit` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `stok_buku` int DEFAULT NULL,
  `id_petugas` int NOT NULL,
  PRIMARY KEY (`judul_buku`),
  UNIQUE KEY `uuid` (`uuid`),
  UNIQUE KEY `uuid_2` (`uuid`),
  KEY `fk_buku_petugas` (`id_petugas`),
  CONSTRAINT `fk_buku_petugas` FOREIGN KEY (`id_petugas`) REFERENCES `petugas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buku`
--

LOCK TABLES `buku` WRITE;
/*!40000 ALTER TABLE `buku` DISABLE KEYS */;
INSERT INTO `buku` VALUES ('buku satu hati','37fee080-80c8-4612-80aa-7da1e0cf067c','muhdi','ganesha','2013',15,4),('Malam Sepi Sunyi','859e71d9-d58b-4d46-a20e-d4ec8e8ajdsj','Mas','eang wiro','2019',17,4),('Si Buta Dari Gua Hantu','859e71d9-d58b-4d46-a20e-d4ec8e89wake','mark','buana','2020',13,3);
/*!40000 ALTER TABLE `buku` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `petugas`
--

DROP TABLE IF EXISTS `petugas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `petugas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `alamat` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `no_tlp` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'admin',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `petugas`
--

LOCK TABLES `petugas` WRITE;
/*!40000 ALTER TABLE `petugas` DISABLE KEYS */;
INSERT INTO `petugas` VALUES (3,'admin','admin@gmail.com','pbkdf2:sha256:600000$lFpquFGmQ9mjiJoN$0ee915051943a2c0cf82fa60b1e72b0b2f89f1e33d8ac6a13047c892532c49c3','jogja','0812345678','admin'),(4,'petugas','petugas@gmail.com','pbkdf2:sha256:600000$tgjQcaRtNbnC4KzM$92bd78aa512cc5e86536d3d90e43fb47690b33e0d52b8c88f70dd793c812d023','bogor','0812345679','admin'),(7,'markus','markus@gmali.com','pbkdf2:sha256:600000$1UvmGrvzoiY39F5c$13760f5fc548cd4828251bd22e4f2c2cc05557390fde861833b8d7ef95a5966e','jogja','08123467','admin');
/*!40000 ALTER TABLE `petugas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pinjam_kembali`
--

DROP TABLE IF EXISTS `pinjam_kembali`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pinjam_kembali` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nim_anggota` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `judul_buku` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `tgl_pinjam` datetime NOT NULL,
  `tgl_batas_pinjam` datetime NOT NULL,
  `tgl_kembali` datetime DEFAULT NULL,
  `status` enum('dipinjam','dikembalikan') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'dipinjam',
  `denda` varchar(12) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0',
  `id_petugas` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_anggota` (`nim_anggota`),
  KEY `fk_buku` (`judul_buku`),
  KEY `fk_pinjam_petugas` (`id_petugas`),
  CONSTRAINT `fk_anggota` FOREIGN KEY (`nim_anggota`) REFERENCES `anggota` (`nim`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_buku` FOREIGN KEY (`judul_buku`) REFERENCES `buku` (`judul_buku`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_pinjam_petugas` FOREIGN KEY (`id_petugas`) REFERENCES `petugas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pinjam_kembali`
--

LOCK TABLES `pinjam_kembali` WRITE;
/*!40000 ALTER TABLE `pinjam_kembali` DISABLE KEYS */;
INSERT INTO `pinjam_kembali` VALUES (17,'21.83.1235','Si Buta Dari Gua Hantu','2023-07-06 14:06:38','2023-07-13 14:06:38',NULL,'dipinjam','0',4),(18,'21.83.1235','buku satu hati','2023-07-06 14:30:29','2023-07-13 14:30:29',NULL,'dipinjam','0',4),(23,'21.83.1235','Malam Sepi Sunyi','2023-07-07 20:01:43','2023-07-14 20:01:43','2023-07-07 20:04:02','dikembalikan','0',7),(24,'21.83.1234','Malam Sepi Sunyi','2023-07-08 00:06:30','2023-07-15 00:06:30','2023-07-08 00:20:31','dikembalikan','0',3),(25,'21.83.1234','Si Buta Dari Gua Hantu','2023-07-08 00:20:20','2023-07-15 00:20:20',NULL,'dipinjam','0',3);
/*!40000 ALTER TABLE `pinjam_kembali` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-08  0:57:56
