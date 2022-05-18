create database Contacts
go
use Contacts

go
create table Member(
	ID char(8),
	FULLNAME nvarchar(30),
	PHONENUM varchar(10),
	EMAIL varchar(50),
	BIGAVT varchar(50),		--file path
	SMALLAVT varchar(50)	--file path
)

insert into Member values ('20120600',N'Lê Minh Trí','0585081598','20120600@student.hcmus.edu.vn','Avatar/BigAvatar/lmtri.png','Avatar/SmallAvatar/lmtri.png')
insert into Member values ('20120607',N'Lê Hữu Trọng','0378140742','20120607@student.hcmus.edu.vn','Avatar/BigAvatar/lhtrong.png','Avatar/SmallAvatar/lhtrong.png')
insert into Member values ('20120059',N'Lê Ngọc Đức','0378871736','20120059@student.hcmus.edu.vn','Avatar/BigAvatar/lnduc.png','Avatar/SmallAvatar/lnduc.png')