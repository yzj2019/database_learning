-- MySQL dump 10.13  Distrib 8.0.25, for Linux (x86_64)
--
-- Host: localhost    Database: db_lab3
-- ------------------------------------------------------
-- Server version	8.0.25

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
-- Table structure for table `借贷`
--

DROP TABLE IF EXISTS `借贷`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `借贷` (
  `贷款号` decimal(8,0) NOT NULL,
  `客户身份证号` decimal(18,0) NOT NULL,
  PRIMARY KEY (`贷款号`,`客户身份证号`),
  KEY `FK_借贷2` (`客户身份证号`),
  CONSTRAINT `FK_借贷` FOREIGN KEY (`贷款号`) REFERENCES `贷款` (`贷款号`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_借贷2` FOREIGN KEY (`客户身份证号`) REFERENCES `客户` (`客户身份证号`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `借贷`
--

LOCK TABLES `借贷` WRITE;
/*!40000 ALTER TABLE `借贷` DISABLE KEYS */;
/*!40000 ALTER TABLE `借贷` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `储蓄账户`
--

DROP TABLE IF EXISTS `储蓄账户`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `储蓄账户` (
  `账户号` decimal(8,0) NOT NULL,
  `利率` float DEFAULT NULL,
  `货币类型` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`账户号`),
  CONSTRAINT `FK_账户类型` FOREIGN KEY (`账户号`) REFERENCES `账户` (`账户号`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `储蓄账户`
--

LOCK TABLES `储蓄账户` WRITE;
/*!40000 ALTER TABLE `储蓄账户` DISABLE KEYS */;
INSERT INTO `储蓄账户` VALUES (1,0.025,'人民币'),(3,0.025,'人民币'),(4,0.025,'人民币');
/*!40000 ALTER TABLE `储蓄账户` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `员工`
--

DROP TABLE IF EXISTS `员工`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `员工` (
  `支行名称` varchar(128) NOT NULL,
  `部门号` decimal(8,0) NOT NULL,
  `员工身份证号` decimal(18,0) NOT NULL,
  `员工姓名` varchar(32) DEFAULT NULL,
  `员工电话号码` decimal(11,0) DEFAULT NULL,
  `员工家庭地址` varchar(1024) DEFAULT NULL,
  `员工类型` tinyint(1) DEFAULT NULL,
  `开始工作的日期` date DEFAULT NULL,
  PRIMARY KEY (`支行名称`,`部门号`,`员工身份证号`),
  CONSTRAINT `FK_所属` FOREIGN KEY (`支行名称`, `部门号`) REFERENCES `部门` (`支行名称`, `部门号`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `员工`
--

LOCK TABLES `员工` WRITE;
/*!40000 ALTER TABLE `员工` DISABLE KEYS */;
/*!40000 ALTER TABLE `员工` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `客户`
--

DROP TABLE IF EXISTS `客户`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `客户` (
  `客户身份证号` decimal(18,0) NOT NULL,
  `客户姓名` varchar(32) DEFAULT NULL,
  `客户联系电话` decimal(11,0) DEFAULT NULL,
  `客户家庭住址` varchar(1024) DEFAULT NULL,
  `联系人姓名` varchar(32) DEFAULT NULL,
  `联系人手机号` decimal(11,0) DEFAULT NULL,
  `联系人email` varchar(64) DEFAULT NULL,
  `联系人与客户的关系` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`客户身份证号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `客户`
--

LOCK TABLES `客户` WRITE;
/*!40000 ALTER TABLE `客户` DISABLE KEYS */;
INSERT INTO `客户` VALUES (372301200000000000,'于子健',19912345678,'安徽省合肥市中国科学技术大学中校区','于子健',18887654321,'name@example.com','本人'),(372301200000000001,'张三',19912345678,'安徽省合肥市中国科学技术大学中校区','张三',18887654321,'name@example.com','本人'),(372301200000000002,'李四',19912345679,'安徽省合肥市中国科学技术大学中校区','李四',18887654321,'name@example.com','本人'),(372301200000000003,'王五',19912345678,'安徽省合肥市中国科学技术大学中校区','王五',18887654321,'name@example.com','本人'),(372301200000000004,'马六',19912345678,'安徽省合肥市中国科学技术大学中校区','马六',18887654321,'name@example.com','本人');
/*!40000 ALTER TABLE `客户` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `客户在银行的账户`
--

DROP TABLE IF EXISTS `客户在银行的账户`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `客户在银行的账户` (
  `支行名称` varchar(128) NOT NULL,
  `客户身份证号` decimal(18,0) NOT NULL,
  `账户类型` tinyint(1) NOT NULL,
  PRIMARY KEY (`支行名称`,`客户身份证号`,`账户类型`),
  KEY `FK_Relationship_7` (`客户身份证号`),
  CONSTRAINT `FK_Relationship_6` FOREIGN KEY (`支行名称`) REFERENCES `支行` (`支行名称`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_Relationship_7` FOREIGN KEY (`客户身份证号`) REFERENCES `客户` (`客户身份证号`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `客户在银行的账户`
--

LOCK TABLES `客户在银行的账户` WRITE;
/*!40000 ALTER TABLE `客户在银行的账户` DISABLE KEYS */;
INSERT INTO `客户在银行的账户` VALUES ('云银行中科大支行',372301200000000000,0),('云银行中科大支行',372301200000000000,1),('云银行中科大支行',372301200000000001,0),('云银行中科大支行',372301200000000001,1),('云银行中科大支行',372301200000000002,0),('云银行中科大支行',372301200000000002,1);
/*!40000 ALTER TABLE `客户在银行的账户` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `支票账户`
--

DROP TABLE IF EXISTS `支票账户`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `支票账户` (
  `账户号` decimal(8,0) NOT NULL,
  `透支额` float(8,2) DEFAULT NULL,
  PRIMARY KEY (`账户号`),
  CONSTRAINT `FK_账户类型2` FOREIGN KEY (`账户号`) REFERENCES `账户` (`账户号`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `支票账户`
--

LOCK TABLES `支票账户` WRITE;
/*!40000 ALTER TABLE `支票账户` DISABLE KEYS */;
INSERT INTO `支票账户` VALUES (2,20000.00),(5,20000.00),(6,20000.00);
/*!40000 ALTER TABLE `支票账户` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `支行`
--

DROP TABLE IF EXISTS `支行`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `支行` (
  `支行名称` varchar(128) NOT NULL,
  `支行资产` float(8,2) DEFAULT NULL,
  PRIMARY KEY (`支行名称`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `支行`
--

LOCK TABLES `支行` WRITE;
/*!40000 ALTER TABLE `支行` DISABLE KEYS */;
INSERT INTO `支行` VALUES ('云银行中科大支行',299000.00);
/*!40000 ALTER TABLE `支行` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `负责`
--

DROP TABLE IF EXISTS `负责`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `负责` (
  `支行名称` varchar(128) NOT NULL,
  `部门号` decimal(8,0) NOT NULL,
  `员工身份证号` decimal(18,0) NOT NULL,
  `客户身份证号` decimal(18,0) NOT NULL,
  `负责类型` varchar(1) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`支行名称`,`部门号`,`员工身份证号`,`客户身份证号`),
  KEY `FK_负责2` (`客户身份证号`),
  CONSTRAINT `FK_负责` FOREIGN KEY (`支行名称`, `部门号`, `员工身份证号`) REFERENCES `员工` (`支行名称`, `部门号`, `员工身份证号`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_负责2` FOREIGN KEY (`客户身份证号`) REFERENCES `客户` (`客户身份证号`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `负责`
--

LOCK TABLES `负责` WRITE;
/*!40000 ALTER TABLE `负责` DISABLE KEYS */;
/*!40000 ALTER TABLE `负责` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `账户`
--

DROP TABLE IF EXISTS `账户`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `账户` (
  `账户号` decimal(8,0) NOT NULL,
  `支行名称` varchar(128) NOT NULL,
  `余额` float(8,2) DEFAULT NULL,
  `开户日期` date DEFAULT NULL,
  `客户身份证号` decimal(18,0) NOT NULL,
  `最近访问日期` date DEFAULT NULL,
  PRIMARY KEY (`账户号`),
  KEY `FK_开户` (`支行名称`),
  CONSTRAINT `FK_开户` FOREIGN KEY (`支行名称`) REFERENCES `支行` (`支行名称`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `账户`
--

LOCK TABLES `账户` WRITE;
/*!40000 ALTER TABLE `账户` DISABLE KEYS */;
INSERT INTO `账户` VALUES (1,'云银行中科大支行',1000.00,'2021-06-28',372301200000000000,'2021-06-28'),(2,'云银行中科大支行',0.00,'2021-06-28',372301200000000000,'2021-06-28'),(3,'云银行中科大支行',1000.00,'2021-06-28',372301200000000001,'2021-06-28'),(4,'云银行中科大支行',1000.00,'2021-06-28',372301200000000002,'2021-06-28'),(5,'云银行中科大支行',0.00,'2021-06-28',372301200000000001,'2021-06-28'),(6,'云银行中科大支行',0.00,'2021-06-28',372301200000000002,'2021-06-28');
/*!40000 ALTER TABLE `账户` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `贷款`
--

DROP TABLE IF EXISTS `贷款`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `贷款` (
  `贷款号` decimal(8,0) NOT NULL,
  `支行名称` varchar(128) NOT NULL,
  `所贷金额` float(8,2) DEFAULT NULL,
  `逐次支付情况` decimal(8,0) DEFAULT NULL,
  PRIMARY KEY (`贷款号`),
  KEY `FK_发放` (`支行名称`),
  CONSTRAINT `FK_发放` FOREIGN KEY (`支行名称`) REFERENCES `支行` (`支行名称`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `贷款`
--

LOCK TABLES `贷款` WRITE;
/*!40000 ALTER TABLE `贷款` DISABLE KEYS */;
/*!40000 ALTER TABLE `贷款` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `贷款付款`
--

DROP TABLE IF EXISTS `贷款付款`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `贷款付款` (
  `付款码` decimal(8,0) NOT NULL,
  `付款日期` date NOT NULL,
  `付款金额` float(8,2) NOT NULL,
  `贷款号` decimal(8,0) NOT NULL,
  PRIMARY KEY (`贷款号`,`付款码`,`付款日期`,`付款金额`),
  CONSTRAINT `FK_逐次支付情况` FOREIGN KEY (`贷款号`) REFERENCES `贷款` (`贷款号`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `贷款付款`
--

LOCK TABLES `贷款付款` WRITE;
/*!40000 ALTER TABLE `贷款付款` DISABLE KEYS */;
/*!40000 ALTER TABLE `贷款付款` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `部门`
--

DROP TABLE IF EXISTS `部门`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `部门` (
  `支行名称` varchar(128) NOT NULL,
  `部门号` decimal(8,0) NOT NULL,
  `部门名称` varchar(128) DEFAULT NULL,
  `部门类型` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `部门经理身份证号` decimal(18,0) DEFAULT NULL,
  PRIMARY KEY (`支行名称`,`部门号`),
  CONSTRAINT `FK_上属` FOREIGN KEY (`支行名称`) REFERENCES `支行` (`支行名称`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `部门`
--

LOCK TABLES `部门` WRITE;
/*!40000 ALTER TABLE `部门` DISABLE KEYS */;
/*!40000 ALTER TABLE `部门` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-28  5:27:03
