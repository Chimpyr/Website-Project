use horizon_travels_test;

select * from users;
delete from users;
INSERT INTO users (first_name, last_name, password_hash, email, usertype) VALUES ('J','C', 'securePassword','jc@jc.com', 'admin');