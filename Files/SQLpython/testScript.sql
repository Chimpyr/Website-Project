use horizon_travels_test;

select * from users;
delete from users;

update users SET usertype = 'admin' WHERE user_id = 1005;

INSERT INTO users (first_name, last_name, password_hash, email, usertype) VALUES ('J','C', 'securePassword','jc@jc.com', 'admin');