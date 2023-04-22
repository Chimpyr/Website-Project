use horizon_travels_test;
use test_db;
select * from bookings;

select * from users;
select * from booking;
select * from journey;


delete from users;
delete from booking;

update users SET usertype = 'admin' WHERE email = "admin@admin.com";

INSERT INTO users (first_name, last_name, password_hash, email, usertype) VALUES ('J','C', 'securePassword','jc@jc.com', 'admin');