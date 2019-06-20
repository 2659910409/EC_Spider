
-- 数据表建表语句，扔这里

-- ----------------------------
-- Table structure for app_ca_product360_flow_day
-- ----------------------------
DROP TABLE IF EXISTS `app_ca_product360_flow_day`;
CREATE TABLE `app_ca_product360_flow_day`  (
  `店铺id` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `店铺` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `日期` date NULL DEFAULT NULL,
  `商品id` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `来源名称` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `访客数` bigint(20) NULL DEFAULT NULL,
  `浏览量` bigint(20) NULL DEFAULT NULL,
  `支付金额` decimal(18, 2) NULL DEFAULT NULL,
  `浏览量占比` decimal(18, 4) NULL DEFAULT NULL,
  `店内跳转人数` bigint(20) NULL DEFAULT NULL,
  `跳出本店人数` bigint(20) NULL DEFAULT NULL,
  `收藏人数` bigint(20) NULL DEFAULT NULL,
  `加购人数` bigint(20) NULL DEFAULT NULL,
  `下单买家数` bigint(20) NULL DEFAULT NULL,
  `下单转化率` decimal(18, 4) NULL DEFAULT NULL,
  `支付件数` bigint(20) NULL DEFAULT NULL,
  `支付买家数` bigint(20) NULL DEFAULT NULL,
  `支付转化率` decimal(18, 4) NULL DEFAULT NULL,
  `直接支付买家数` bigint(20) NULL DEFAULT NULL,
  `收藏商品_支付买家数` bigint(20) NULL DEFAULT NULL,
  `粉丝支付买家数` bigint(20) NULL DEFAULT NULL,
  `加购商品_支付买家数` bigint(20) NULL DEFAULT NULL,
  `入库时间` timestamp(0) NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

