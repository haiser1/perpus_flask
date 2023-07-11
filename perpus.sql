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
  `uuid` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
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
INSERT INTO `anggota` VALUES ('21.83.0702','markus','markus@gmail.com','pbkdf2:sha256:600000$iFLXQVb7fj5zfzKm$e5d3d2870d7f113697f025b7a053f1c5f7377f02cac75e82e68761e67e9ea5e6','Konoha','0812346789','user',3,'aee96d61-3952-4fd7-9c82-556e40253b63'),('21.83.1234','mark','mark@gmail.com','pbkdf2:sha256:600000$qNusVwyO4Fkl9rpU$ab6af91fda2dc63bab0de9cc170e6c8c9d484d40aabec52585212a6a274f229f','Konoha','0812346789','user',3,'6fb58989-e8a6-4b93-924b-ca2331cce57d'),('21.83.1235','muklis','muklis@gmail.com','pbkdf2:sha256:600000$hJXh33z7rFdo2AM4$5f76e41adf4e614ebcf23b51cade1f2a61220cf9f14cc4a60f96d8d2c67e0b28','bantul','081235','user',4,'29b40f7d-0a6c-452e-a32f-69d9846ab8f8'),('21.83.1237','Dobleh','dobleh@gmail.com','pbkdf2:sha256:600000$PZKvf6XSmEiwcXph$e5bd82108c37ecc9b528f3bc6ecc60fca6bf812aedf23495c085b29fdccf8568','jogja','08123467','user',3,'59a920b4-3c75-403c-a6a1-d9d27f64233a');
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
  `uuid` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `penulis` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `penerbit` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `tahun_terbit` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `stok_buku` int DEFAULT NULL,
  `id_petugas` int NOT NULL,
  PRIMARY KEY (`judul_buku`),
  KEY `fk_buku_petugas` (`id_petugas`),
  CONSTRAINT `fk_buku_petugas` FOREIGN KEY (`id_petugas`) REFERENCES `petugas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buku`
--

LOCK TABLES `buku` WRITE;
/*!40000 ALTER TABLE `buku` DISABLE KEYS */;
INSERT INTO `buku` VALUES ('buku satu hati','37fee080-80c8-4612-80aa-7da1e0cf067c','muhdi','ganesha','2013',14,3),('Malam Sepi Sunyi','859e71d9-d58b-4d46-a20e-d4ec8e8ajdsj','Mas','eang wiro','2019',17,4),('Si Buta Dari Gua Hantu','859e71d9-d58b-4d46-a20e-d4ec8e89wake','mark','buana','2020',12,3);
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
  `uuid` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `petugas`
--

LOCK TABLES `petugas` WRITE;
/*!40000 ALTER TABLE `petugas` DISABLE KEYS */;
INSERT INTO `petugas` VALUES (3,'admin','admin@gmail.com','pbkdf2:sha256:600000$xQ37VWGPZ6aKi6WN$3bf8dda3fc5bddd94ce8e5eda17a295eb8679e10d1b8fad2471412d68e3ea01d','jogja','0812345678','admin','b0418746-6aac-46a6-af68-8e48e919ba24'),(4,'petugas','petugas@gmail.com','pbkdf2:sha256:600000$tgjQcaRtNbnC4KzM$92bd78aa512cc5e86536d3d90e43fb47690b33e0d52b8c88f70dd793c812d023','bogor','0812345679','admin','3b825b97-3732-4b60-9d2a-e31e29f478bd'),(7,'rabin','rabin@gmali.com','pbkdf2:sha256:600000$Q3elXzm0NdlY94BL$cae2240b3d6fe14fa5178d1c742993e7eaf640ee600c7d92b26cbc1855f92974','jogja','08123467','admin','cc85b866-d5f1-4ebf-a193-87411cb6a1bf');
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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pinjam_kembali`
--

LOCK TABLES `pinjam_kembali` WRITE;
/*!40000 ALTER TABLE `pinjam_kembali` DISABLE KEYS */;
INSERT INTO `pinjam_kembali` VALUES (17,'21.83.1235','Si Buta Dari Gua Hantu','2023-07-06 14:06:38','2023-07-13 14:06:38',NULL,'dipinjam','0',4),(18,'21.83.1235','buku satu hati','2023-07-06 14:30:29','2023-07-13 14:30:29','2023-07-08 16:10:23','dikembalikan','0',3),(23,'21.83.1235','Malam Sepi Sunyi','2023-07-07 20:01:43','2023-07-14 20:01:43','2023-07-07 20:04:02','dikembalikan','0',7),(24,'21.83.1234','Malam Sepi Sunyi','2023-07-08 00:06:30','2023-07-15 00:06:30','2023-07-08 00:20:31','dikembalikan','0',3),(25,'21.83.1234','Si Buta Dari Gua Hantu','2023-07-08 00:20:20','2023-07-15 00:20:20',NULL,'dipinjam','0',3),(26,'21.83.1237','buku satu hati','2023-07-08 02:43:16','2023-07-15 02:43:16',NULL,'dipinjam','0',3),(27,'21.83.1234','buku satu hati','2023-07-08 02:44:02','2023-07-15 02:44:02',NULL,'dipinjam','0',3),(28,'21.83.0702','Si Buta Dari Gua Hantu','2023-07-11 19:07:04','2023-07-18 19:07:04',NULL,'dipinjam','0',3);
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

-- Dump completed on 2023-07-11 19:36:36
