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
/* Table: Loan                                                    */
/*==============================================================*/
create table LoanRecord
(
   LoanNumber                  numeric(8,0) not null,
   CustomerIDNumber               numeric(18,0) not null,
   primary key (LoanNumber, CustomerIDNumber)
);

/*==============================================================*/
/* Table: SavingAccount                                                  */
/*==============================================================*/
create table SavingAccount
(
   AccountNumber                  numeric(8,0) not null,
   SubBankName                 varchar(128),
   balance                   float(8,2),
   AccountOpeningDate                 date,
   InterestRate                   float,
   CurrencyType                 varchar(32),
   primary key (AccountNumber)
);

/*==============================================================*/
/* Table: Staff                                                    */
/*==============================================================*/
create table Staff
(
   SubBankName                 varchar(128) not null,
   DepartmentNumber                  numeric(8,0) not null,
   StaffIDNumber               numeric(18,0) not null,
   StaffName                 varchar(32),
   StaffPhoneNumber               numeric(11,0),
   StaffHomeAddress               varchar(1024),
   StaffType                 bool,
   StaffStartWorkingDate              date,
   primary key (SubBankName, DepartmentNumber, StaffIDNumber)
);

/*==============================================================*/
/* Table: Customer                                                    */
/*==============================================================*/
create table Customer
(
   CustomerIDNumber               numeric(18,0) not null,
   CustomerName                 varchar(32),
   CustomerPhoneNumber               numeric(11,0),
   CustomerHomeAddress               varchar(1024),
   CustomerCPName                varchar(32),
   CustomerCPPhoneNumber               numeric(11,0),
   CustomerCPEmail             varchar(64),
   CustomerCPRelationship            varchar(128),
   primary key (CustomerIDNumber)
);

/*==============================================================*/
/* Table: CustomerAccount                                              */
/*==============================================================*/
create table CustomerAccount
(
   SubBankName                 varchar(128) not null,
   CustomerIDNumber               numeric(18,0) not null,
   AccountType                 bool not null,
   primary key (SubBankName, CustomerIDNumber, AccountType)
);

/*==============================================================*/
/* Table: Hold                                                    */
/*==============================================================*/
create table Hold
(
   AccountNumber                  numeric(8,0) not null,
   CustomerIDNumber               numeric(18,0) not null,
   LastAccessDate               date,
   primary key (AccountNumber, CustomerIDNumber)
);

/*==============================================================*/
/* Table: CheckingAccount                                                  */
/*==============================================================*/
create table CheckingAccount
(
   AccountNumber                  numeric(8,0) not null,
   SubBankName                 varchar(128),
   balance                   float(8,2),
   AccountOpeningDate                 date,
   OverdraftAmount                  float(8,2),
   primary key (AccountNumber)
);

/*==============================================================*/
/* Table: SubBank                                                    */
/*==============================================================*/
create table SubBank
(
   SubBankName                 varchar(128) not null,
   SubBankAssets                 float(8,2),
   primary key (SubBankName)
);

/*==============================================================*/
/* Table: Charge                                                    */
/*==============================================================*/
create table Charge
(
   SubBankName                 varchar(128) not null,
   DepartmentNumber                  numeric(8,0) not null,
   StaffIDNumber               numeric(18,0) not null,
   CustomerIDNumber               numeric(18,0) not null,
   ChargeType                 national varchar(1),
   primary key (SubBankName, DepartmentNumber, StaffIDNumber, CustomerIDNumber)
);

/*==============================================================*/
/* Table: Account                                                    */
/*==============================================================*/
create table Account
(
   AccountNumber                  numeric(8,0) not null,
   SubBankName                 varchar(128) not null,
   balance                   float(8,2),
   AccountOpeningDate                 date,
   primary key (AccountNumber)
);

/*==============================================================*/
/* Table: Loan                                                    */
/*==============================================================*/
create table Loan
(
   LoanNumber                  numeric(8,0) not null,
   SubBankName                 varchar(128) not null,
   LoanAmount                 float(8,2),
   LoanHowToPay               numeric(8,0),
   primary key (LoanNumber)
);

/*==============================================================*/
/* Table: LoanPayment                                                  */
/*==============================================================*/
create table LoanPayment
(
   LoanPaymentCode                  numeric(8,0) not null,
   LoanPaymentDate                 date not null,
   LoanPaymentAmount                 float(8,2) not null,
   LoanNumber                  numeric(8,0) not null,
   primary key (LoanNumber, LoanPaymentCode, LoanPaymentDate, LoanPaymentAmount)
);

/*==============================================================*/
/* Table: Department                                                    */
/*==============================================================*/
create table Department
(
   SubBankName                 varchar(128) not null,
   DepartmentNumber                  numeric(8,0) not null,
   DepartmentName                 varchar(128),
   DepartmentType                 national varchar(255),
   DepartmentManagerIDNumber             numeric(18,0),
   primary key (SubBankName, DepartmentNumber)
);

alter table LoanRecord add constraint FK_LoanRecord foreign key (LoanNumber)
      references Loan (LoanNumber) on delete restrict on update restrict;

alter table LoanRecord add constraint FK_LoanRecord2 foreign key (CustomerIDNumber)
      references Customer (CustomerIDNumber) on delete restrict on update restrict;

alter table SavingAccount add constraint FK_AccountType foreign key (AccountNumber)
      references Account (AccountNumber) on delete restrict on update restrict;

alter table Staff add constraint FK_hired foreign key (SubBankName, DepartmentNumber)
      references Department (SubBankName, DepartmentNumber) on delete restrict on update restrict;

alter table CustomerAccount add constraint FK_Relationship_6 foreign key (SubBankName)
      references SubBank (SubBankName) on delete restrict on update restrict;

alter table CustomerAccount add constraint FK_Relationship_7 foreign key (CustomerIDNumber)
      references Customer (CustomerIDNumber) on delete restrict on update restrict;

alter table Hold add constraint FK_Hold foreign key (AccountNumber)
      references Account (AccountNumber) on delete restrict on update restrict;

alter table Hold add constraint FK_Hold2 foreign key (CustomerIDNumber)
      references Customer (CustomerIDNumber) on delete restrict on update restrict;

alter table CheckingAccount add constraint FK_AccountType2 foreign key (AccountNumber)
      references Account (AccountNumber) on delete restrict on update restrict;

alter table Charge add constraint FK_Charge foreign key (SubBankName, DepartmentNumber, StaffIDNumber)
      references Staff (SubBankName, DepartmentNumber, StaffIDNumber) on delete restrict on update restrict;

alter table Charge add constraint FK_Charge2 foreign key (CustomerIDNumber)
      references Customer (CustomerIDNumber) on delete restrict on update restrict;

alter table Account add constraint FK_OpenAccount foreign key (SubBankName)
      references SubBank (SubBankName) on delete restrict on update restrict;

alter table Loan add constraint FK_Payment foreign key (SubBankName)
      references SubBank (SubBankName) on delete restrict on update restrict;

alter table LoanPayment add constraint FK_LoanHowToPay foreign key (LoanNumber)
      references Loan (LoanNumber) on delete restrict on update restrict;

alter table Department add constraint FK_in foreign key (SubBankName)
      references SubBank (SubBankName) on delete restrict on update restrict;

