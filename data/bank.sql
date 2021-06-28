/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2021/5/11 20:47:48                           */
/*==============================================================*/


/*
drop database if exists db_lab3;

create database db_lab3;
*/

use db_lab3;



/*==============================================================*/
/* Table: 员工                                                    */
/*==============================================================*/
create table 员工
(
   支行名称                 varchar(128) not null,
   部门号                  numeric(8,0) not null,
   员工身份证号               numeric(18,0) not null,
   员工姓名                 varchar(32),
   员工电话号码               numeric(11,0),
   员工家庭地址               varchar(1024),
   员工类型                 bool,
   开始工作的日期              date,
   primary key (支行名称, 部门号, 员工身份证号)
);

/*==============================================================*/
/* Table: 客户                                                    */
/*==============================================================*/
create table 客户
(
   客户身份证号               numeric(18,0) not null,
   客户姓名                 varchar(32),
   客户联系电话               numeric(11,0),
   客户家庭住址               varchar(1024),
   联系人姓名                varchar(32),
   联系人手机号               numeric(11,0),
   联系人email             varchar(64),
   联系人与客户的关系            varchar(128),
   primary key (客户身份证号)
);

/*==============================================================*/
/* Table: 客户在银行的账户                                              */
/*==============================================================*/
create table 客户在银行的账户
(
   支行名称                 varchar(128) not null,
   客户身份证号               numeric(18,0) not null,
   账户类型                 bool not null,
   primary key (支行名称, 客户身份证号, 账户类型)
);


/*==============================================================*/
/* Table: 储蓄账户                                                  */
/*==============================================================*/
create table 储蓄账户
(
   账户号                  numeric(8,0) not null,
   利率                   float,
   货币类型                 varchar(32),
   primary key (账户号)
);

/*==============================================================*/
/* Table: 支票账户                                                  */
/*==============================================================*/
create table 支票账户
(
   账户号                  numeric(8,0) not null,
   透支额                  float(8,2),
   primary key (账户号)
);

/*==============================================================*/
/* Table: 支行                                                    */
/*==============================================================*/
create table 支行
(
   支行名称                 varchar(128) not null,
   支行资产                 float(12,2),
   primary key (支行名称)
);

/*==============================================================*/
/* Table: 负责                                                    */
/*==============================================================*/
create table 负责
(
   支行名称                 varchar(128) not null,
   部门号                  numeric(8,0) not null,
   员工身份证号               numeric(18,0) not null,
   客户身份证号               numeric(18,0) not null,
   负责类型                 national varchar(1),
   primary key (支行名称, 部门号, 员工身份证号, 客户身份证号)
);

/*==============================================================*/
/* Table: 账户                                                    */
/*==============================================================*/
create table 账户
(
   账户号                  numeric(8,0) not null,
   支行名称                 varchar(128) not null,
   余额                   float(8,2),
   开户日期                 date,
   客户身份证号               numeric(18,0) not null,
   最近访问日期               date,
   primary key (账户号)
);

/*==============================================================*/
/* Table: 贷款                                                    */
/*==============================================================*/
create table 贷款
(
   贷款号                  numeric(8,0) not null,
   支行名称                 varchar(128) not null,
   客户身份证号               numeric(18,0) not null,
   所贷金额                 float(8,2),
   逐次支付情况               numeric(8,0),
   primary key (贷款号)
);

/*==============================================================*/
/* Table: 贷款付款                                                  */
/*==============================================================*/
create table 贷款付款
(
   贷款号                  numeric(8,0) not null,
   付款码                  numeric(8,0) not null,
   付款日期                 date not null,
   付款金额                 float(8,2) not null,
   primary key (贷款号, 付款码)
);

/*==============================================================*/
/* Table: 部门                                                    */
/*==============================================================*/
create table 部门
(
   支行名称                 varchar(128) not null,
   部门号                  numeric(8,0) not null,
   部门名称                 varchar(128),
   部门类型                 national varchar(255),
   部门经理身份证号             numeric(18,0),
   primary key (支行名称, 部门号)
);


alter table 储蓄账户 add constraint FK_账户类型 foreign key (账户号)
      references 账户 (账户号) on delete restrict on update restrict;

alter table 员工 add constraint FK_所属 foreign key (支行名称, 部门号)
      references 部门 (支行名称, 部门号) on delete restrict on update restrict;

alter table 客户在银行的账户 add constraint FK_Relationship_6 foreign key (支行名称)
      references 支行 (支行名称) on delete restrict on update restrict;

alter table 客户在银行的账户 add constraint FK_Relationship_7 foreign key (客户身份证号)
      references 客户 (客户身份证号) on delete restrict on update restrict;

alter table 支票账户 add constraint FK_账户类型2 foreign key (账户号)
      references 账户 (账户号) on delete restrict on update restrict;

alter table 负责 add constraint FK_负责 foreign key (支行名称, 部门号, 员工身份证号)
      references 员工 (支行名称, 部门号, 员工身份证号) on delete restrict on update restrict;

alter table 负责 add constraint FK_负责2 foreign key (客户身份证号)
      references 客户 (客户身份证号) on delete restrict on update restrict;

alter table 账户 add constraint FK_开户 foreign key (支行名称)
      references 支行 (支行名称) on delete restrict on update restrict;

alter table 账户 add constraint FK_持有 foreign key (客户身份证号)
      references 客户 (客户身份证号) on delete restrict on update restrict;

alter table 贷款 add constraint FK_借贷 foreign key (客户身份证号)
      references 客户 (客户身份证号) on delete restrict on update restrict;

alter table 贷款 add constraint FK_发放 foreign key (支行名称)
      references 支行 (支行名称) on delete restrict on update restrict;

alter table 贷款付款 add constraint FK_逐次支付情况 foreign key (贷款号)
      references 贷款 (贷款号) on delete restrict on update restrict;

alter table 部门 add constraint FK_上属 foreign key (支行名称)
      references 支行 (支行名称) on delete restrict on update restrict;

