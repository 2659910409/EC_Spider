-- MySQL Script generated by MySQL Workbench
-- Thu Jun 13 20:15:17 2019
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema ec_spider
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema ec_spider
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ec_spider` DEFAULT CHARACTER SET utf8 ;
USE `ec_spider` ;

-- -----------------------------------------------------
-- Table `ec_spider`.`t_store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_store` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL COMMENT '店铺名：以淘宝官网为准',
  `plt_name` VARCHAR(64) NOT NULL COMMENT '平台：淘宝/京东',
  `plt_store_id` VARCHAR(64) NOT NULL COMMENT '店铺id：以淘宝官网为准',
  `login_username` VARCHAR(64) NULL COMMENT '店铺登录账号',
  `status` INT NOT NULL DEFAULT 1 COMMENT '店铺开启状态：0 无效，1 有效',
  `url` VARCHAR(256) NULL COMMENT '店铺地址',
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`),
  INDEX `plt_store_id` (`plt_name` ASC, `plt_store_id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_store_property`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_store_property` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `store_id` INT NOT NULL COMMENT '店铺id',
  `p_type` VARCHAR(64) NOT NULL COMMENT '属性类型：prop 常规属性，task 任务流程参数',
  `p_key` VARCHAR(64) NOT NULL COMMENT '属性键',
  `p_value` VARCHAR(4096) NOT NULL COMMENT '属性值',
  `p_description` VARCHAR(4096) NULL COMMENT '描述',
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uniq2` (`store_id` ASC, `p_key` ASC) INVISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_task_log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_task_log` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `task_id` INT NOT NULL,
  `job_id` INT NOT NULL,
  `task_version` VARCHAR(64) NOT NULL,
  `task_name` VARCHAR(64) NOT NULL,
  `start_time` TIMESTAMP NULL COMMENT '开始时间',
  `end_time` TIMESTAMP NULL COMMENT '结束时间',
  `status` INT NOT NULL COMMENT '0 未开始，1 进行中，2 成功，3 失败',
  `log` VARCHAR(4096) NULL COMMENT '运行结果说明',
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_task_step_log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_task_step_log` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `task_log_id` INT NOT NULL,
  `step_name` VARCHAR(128) NOT NULL COMMENT '步骤名称',
  `step_description` VARCHAR(256) NULL,
  `status` INT NOT NULL COMMENT '运行状态：0 正常，1 异常',
  `log_level` VARCHAR(64) NOT NULL COMMENT '运行日志告警级别：info/warning/error',
  `err_code` VARCHAR(64) NULL,
  `err_message` TEXT NULL,
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_task_queue`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_task_queue` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `status` INT NOT NULL COMMENT '0 未处理，1 已处理',
  `store_id` INT NOT NULL COMMENT 't_store.id',
  `page_data_ids` VARCHAR(256) NOT NULL COMMENT '存储内容为：t_page_data.id，可存储多个page_data_id 按“,”分割',
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_page`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_page` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `website` VARCHAR(64) NOT NULL COMMENT 'BS网站/系统',
  `name` VARCHAR(64) NOT NULL COMMENT '页面名称',
  `menu_level_first` VARCHAR(64) NOT NULL COMMENT '一级菜单',
  `menu_level_second` VARCHAR(64) NULL COMMENT '二级菜单',
  `menu_level_third` VARCHAR(64) NULL,
  `url` VARCHAR(4096) NULL,
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_page_data`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_page_data` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `page_id` INT NOT NULL,
  `name` VARCHAR(64) NULL COMMENT '数据名称定义，含网页数据块名称信息',
  `status` INT NULL COMMENT '1 有效数据块/取数，0 无效数据块/不取数',
  `data_source_type` VARCHAR(64) NULL COMMENT '数据源类型：html/file',
  `data_update_freq` VARCHAR(64) NULL COMMENT '数据更新频率：day/week/month',
  `data_update_time` VARCHAR(64) NULL COMMENT '数据更新频率时间：\nday:10:00 每天10点更新\nweek:02 10:00 周二10:00更新\nmonth:16 10:00 每月16号10:00更新\n',
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_page_data_conf`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_page_data_conf` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `page_data_id` INT NOT NULL,
  `p_type` VARCHAR(64) NOT NULL COMMENT 'file类型规则\n店铺数据参数：商品id、品牌列表、类目列表等',
  `p_key` VARCHAR(64) NOT NULL COMMENT 'file_name_rule 文件名规则\nfile_type 文件类型：zip/excel/csv/txt',
  `p_value` VARCHAR(4096) NULL,
  `p_description` VARCHAR(4096) NULL,
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_job`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_job` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `task_type` VARCHAR(64) NOT NULL COMMENT '任务类型：taskStep/task/taskflow',
  `ref_task_id` INT NOT NULL COMMENT '引用id 根据type判断：taskId/TaskFlowId',
  `ref_task_version` VARCHAR(64) NOT NULL COMMENT '引用id 根据type判断：taskId/TaskFlowId',
  `job_type` VARCHAR(64) NOT NULL COMMENT '任务调度类型：实时/定时/循环(秒/分钟/小时/天/周/月)',
  `job_schedule` VARCHAR(64) NOT NULL COMMENT '任务调度',
  `status` VARCHAR(64) NOT NULL COMMENT '未开始/等待下次执行/进行中/已停止',
  `start_time` TIMESTAMP NULL,
  `stop_time` TIMESTAMP NULL COMMENT '强制终止时间',
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_data_tab`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_data_tab` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(64) NULL,
  `page_data_id` INT NULL,
  `check_name_rule` VARCHAR(256) NULL COMMENT '文件前缀规则/sheet名前缀规则',
  `business_columns` VARCHAR(4096) NULL COMMENT '业务统计字段',
  `pre_cnt` BIGINT NULL,
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_store_data_log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_store_data_log` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `store_id` INT NOT NULL,
  `data_tab_id` INT NOT NULL,
  `daily_cnt` INT NULL,
  `business_real_cnt` INT NOT NULL COMMENT '业务维度统计实际值',
  `business_pre_cnt` INT NOT NULL COMMENT '预设阀值',
  `data_last_time` TIMESTAMP NOT NULL,
  `status` VARCHAR(64) NULL COMMENT '数据下载入库成功，三方系统数据推送失败(SYCM数据晚更新)',
  `log` TEXT NULL,
  `created` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_task`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_task` (
  `id` INT NOT NULL,
  `task_name` VARCHAR(64) NULL,
  `task_description` VARCHAR(256) NULL,
  `previous_task_id` INT NULL,
  `next_task_id` INT NULL,
  `priority` INT NULL DEFAULT 1000 COMMENT '优先级：0~1000~9999，默认：1000',
  `version` VARCHAR(64) NULL,
  `support_multi_process` INT NOT NULL COMMENT '1 支持 0 不支持',
  `support_distributed` INT NOT NULL COMMENT '1 支持 0 不支持',
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  `last_job_id` INT NULL,
  `last_run_time` INT NULL,
  `last_run_status` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_task_step`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_task_step` (
  `id` INT NOT NULL,
  `task_id` INT NULL,
  `executor` VARCHAR(64) NULL,
  `step_name` VARCHAR(64) NULL,
  `step_description` VARCHAR(256) NULL,
  `retry_num` INT NULL COMMENT '重试次数',
  `timeout_duration` INT NULL COMMENT 'step执行超时时长，单位：秒',
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_task_flow`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_task_flow` (
  `id` INT NOT NULL,
  `name` VARCHAR(64) NULL,
  `description` VARCHAR(64) NULL,
  `is_start` INT NULL COMMENT '起始位置',
  `task_id` INT NULL,
  `next_task_id` INT NULL,
  `support_multi_process` INT NULL,
  `support_distributed` INT NULL,
  `priority` INT NULL,
  `version` VARCHAR(64) NULL,
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_task_step_property`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_task_step_property` (
  `id` INT NOT NULL,
  `task_step_id` INT NULL,
  `p_type` VARCHAR(64) NULL COMMENT '类型：param_default 默认入参',
  `p_key` VARCHAR(64) NULL,
  `p_value` VARCHAR(4096) NULL,
  `p_description` VARCHAR(4096) NULL,
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `ec_spider`.`t_task_property`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_task_property` (
  `id` INT NOT NULL,
  `task_id` INT NULL,
  `p_type` VARCHAR(64) NULL,
  `p_key` VARCHAR(64) NULL,
  `p_value` VARCHAR(4096) NULL,
  `p_description` VARCHAR(4096) NULL,
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `ec_spider`.`t_job_history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_job_history` (
  `id` INT NOT NULL,
  `task_type` VARCHAR(64) NULL COMMENT '任务类型：taskStep/task/taskflow',
  `ref_task_id` INT NULL COMMENT '引用id 根据type判断：taskId/TaskFlowId',
  `ref_task_version` VARCHAR(64) NULL COMMENT '引用id 根据type判断：taskId/TaskFlowId',
  `job_type` VARCHAR(64) NULL COMMENT '任务调度类型：实时/定时/循环(秒/分钟/小时/天/周/月)',
  `job_schedule` VARCHAR(64) NULL COMMENT '任务调度',
  `status` VARCHAR(64) NULL COMMENT '未开始/等待下次执行/进行中/已停止',
  `start_time` TIMESTAMP NULL,
  `stop_time` TIMESTAMP NULL COMMENT '强制终止时间',
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ec_spider`.`t_task_flow_property`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_task_flow_property` (
  `id` INT NOT NULL,
  `task_flow_id` INT NOT NULL,
  `p_type` VARCHAR(64) NOT NULL COMMENT '服务器列表，服务器并行数量\nwork列表，并行数量\n',
  `p_key` VARCHAR(64) NOT NULL,
  `p_value` VARCHAR(4096) NULL,
  `p_description` VARCHAR(4096) NULL,
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `ec_spider`.`t_data_tab_column`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ec_spider`.`t_data_tab_column` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `data_tab_id` INT NOT NULL,
  `col_name` VARCHAR(64) NOT NULL COMMENT 'file类型规则\n店铺数据参数：商品id、品牌列表、类目列表等',
  `col_type` VARCHAR(64) NULL COMMENT 'file_name_rule 文件名规则\nfile_type 文件类型：zip/excel/csv/txt',
  `col_type_length` VARCHAR(64) NULL COMMENT '字段类型长度',
  `col_description` VARCHAR(4096) NULL,
  `check_col_name` VARCHAR(64) NULL COMMENT '校验字段名称',
  `is_file_column` INT NULL COMMENT '当数据是文件类型，字段是文件中的原始字段',
  `is_primary_key` INT NULL COMMENT '数据业务主键',
  `is_data_maintenance_pk` INT NULL COMMENT '数据维护主键，当数据插入时 会按数据维护主键先删除',
  `created` TIMESTAMP NULL,
  `updated` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
