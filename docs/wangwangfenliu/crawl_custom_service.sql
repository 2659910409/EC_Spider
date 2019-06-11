/*
Navicat MySQL Data Transfer

Source Server         : 128.71.100.132
Source Server Version : 80013
Source Host           : 128.71.100.132:3306
Source Database       : wangwang

Target Server Type    : MYSQL
Target Server Version : 80013
File Encoding         : 65001

Date: 2019-06-10 17:51:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for crawl_custom_service
-- ----------------------------
DROP TABLE IF EXISTS `crawl_custom_service`;
CREATE TABLE `crawl_custom_service` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `crawl_time` datetime DEFAULT NULL,
  `shop_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `shop_nick` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `value1` int(11) unsigned DEFAULT NULL,
  `value2` int(11) unsigned DEFAULT NULL,
  `value3` int(11) unsigned DEFAULT NULL,
  `value4` decimal(10,1) unsigned DEFAULT NULL,
  `value5` int(10) unsigned DEFAULT NULL,
  `value6` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=145455 DEFAULT CHARSET=utf8;
