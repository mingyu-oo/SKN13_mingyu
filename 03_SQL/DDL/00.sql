create user playdata@localhost identified by '1111'; # 문자열은 다 '' 해줘야하지만 숫자는 꼭해줘야함
create user playdata@'%' identified by '1111'; # 문자열은 다 '' 해줘야하지만 숫자는 꼭해줘야함

-- 00_ddl.sql
-- 생성된 계정 확인
select user, host from mysql.user;

-- SQL문 작성 시 한 명령문이 끝나면 ;(구분자)으로 종료를 해줘야 함. 
-- 실행 : control + enter
-- 주석 : control + / 
-- 한줄 주석 
# 한줄 주석 
/* block 주석 */

-- 계정에 권한을 부여
-- grant 부여할 권한 on 대상 테이블 to 권한부여할 계정
grant all privileges on *.* to 'playdata'@'localhost';
grant all privileges on *.* to 'playdata'@'%';
-- *:DB.*:table



##################################################
# DB 생성
##################################################
create database test_db;
create database hr;

show databases;
-- grant all privileges on test_db.* to playdata@'%'; # test_db에 있는 모든 권한을 'playdata'@'%'에 주겠다. 

drop database hr; # 삭제

use test_db; # 이제부터 이 DB 쓸거야~
-- table이름 -> test_db (DB의 테이블)
use sys;
-- sys.sys_config -> 다른 DB의 테이블 호출, DB이름.테이블이름



##################################################
# Table 생성
##################################################
-- create table test.db.member();
use test_db; -- DB이름을 명시하지 않으면 test_db다.
create table member(
	id varchar(10) primary key, -- 최대 10글자
    password varchar(10) not null, -- not null : 필수 입력
    name varchar(50) not null,
    point int default 1000, -- 값을 넣지 않으면 1000을 default값.
    email varchar(100) not null unique, -- unique : 중복값 허용X
    age int check(age > 20),
    join_date timestamp not null default current_timestamp
    -- default current_timestamp : 값이 insert되는 시점을 저장.
);

-- 테이블들 조회
show tables;
-- 데이블의 cloumn 정보 조회
desc member;
-- 테이블 삭제
drop table if exists member;


##################################################
# insert
##################################################
use test_db;
-- 모든 column에 값을 다 넣을 경우 column명 생략
insert into member 
values('id-100', '1111', '이순신', 5000, 'woo@a.com', 30, '2023-12-10 11:22:33');

insert into member(id, password, name, email)  -- point, join_date : default값, age : null
values('id-200', '2222', '유관순', 'min@b.com');

insert into member(id, password, name, point, email) 
values('id-300', '3333', '강감찬', null, 'gyu@c.com'); -- table 만들 때 point의 default값을 1000으로 해놨으니 null을 넣어주면 들어감

insert into member(id, password, name, point, email, age) 
values('id-400', '4', '한석봉', null, 'rox@c.com', 5); -- Error Code: 3819. Check constraint 'member_chk_1' is violated.	0.000 sec check(age > 20) 조건을 줬으니 error

select * from member;

desc member;