create database SocketAccount
go 
use SocketAccount

go 
create table Account(
	username varchar(20) NOT NULL,
	pass varchar(10) NOT NULL,
)

go
insert into Account values ('lmtri','1')
insert into Account values ('lhtrong','1')
insert into Account values ('lnduc','1')