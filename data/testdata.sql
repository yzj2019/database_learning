use db_lab3;

insert into `支行` values ('云银行中科大支行', 300000);

INSERT INTO `客户` VALUES (372301200000000000,'于子健',19912345678,'安徽省合肥市中国科学技术大学中校区','于子健',18887654321,'name@example.com','本人'),(372301200000000001,'张三',19912345678,'安徽省合肥市中国科学技术大学中校区','张三',18887654321,'name@example.com','本人'),(372301200000000002,'李四',19912345679,'安徽省合肥市中国科学技术大学中校区','李四',18887654321,'name@example.com','本人'),(372301200000000003,'王五',19912345678,'安徽省合肥市中国科学技术大学中校区','王五',18887654321,'name@example.com','本人'),(372301200000000004,'马六',19912345678,'安徽省合肥市中国科学技术大学中校区','马六',18887654321,'name@example.com','本人');

insert into `账户` values (0001, '云银行中科大支行', 1000, CURDATE(), 372301200000000000, CURDATE());
insert into `储蓄账户` values (0001, 0.025, '人民币');
insert into `客户在银行的账户` values ('云银行中科大支行', 372301200000000000, TRUE);

insert into `账户` values (0009, '云银行中科大支行', 1000, DATE_FORMAT('2020-01-01', '%Y-%m-%d'), 372301200000000004, CURDATE());
insert into `储蓄账户` values (0009, 0.025, '人民币');
insert into `客户在银行的账户` values ('云银行中科大支行', 372301200000000004, TRUE);

insert into `账户` values (0002, '云银行中科大支行', 0, CURDATE(), 372301200000000000, CURDATE());
insert into `支票账户` values (0002, 20000);
insert into `客户在银行的账户` values ('云银行中科大支行', 372301200000000000, FALSE);

insert into `账户` values (0003, '云银行中科大支行', 1000, CURDATE(), 372301200000000001, CURDATE());
insert into `储蓄账户` values (0003, 0.025, '人民币');
insert into `客户在银行的账户` values ('云银行中科大支行', 372301200000000001, TRUE);

insert into `账户` values (0004, '云银行中科大支行', 0, CURDATE(), 372301200000000002, CURDATE());
insert into `支票账户` values (0004, 20000);
insert into `客户在银行的账户` values ('云银行中科大支行', 372301200000000002, FALSE);


insert into `贷款` values (0001, '云银行中科大支行', 372301200000000000, 20000, 4);
insert into `贷款付款` values (0001, 0001, CURDATE(), 5000);

select * from `客户`;