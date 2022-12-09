
-- DDL

drop database if exists hotels;
create database hotels;

use hotels;

create table Hotel (
	id INT NOT NULL AUTO_INCREMENT,
    name varchar(100),
    PRIMARY KEY (id)
);

create table Address(
	id INT NOT NULL AUTO_INCREMENT,
    street varchar(200) NOT NULL,
    city varchar(100) NOT NULL,
    pincode varchar(6) NOT NULL,
    primary key (id)
);

create table User(
    id int not null AUTO_INCREMENT,
    name varchar(100) NOT NULL,
    user_password varchar(200) NOT NULL,
    email varchar(100) NOT NULL,
    address_id INT NOT NULL,
    primary key (id),
    foreign key (address_id) references Address(id) on update cascade on delete restrict
);

create table Staff (
	id INT NOT NULL,
    hotel_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id) references User(id) on delete restrict on update cascade,
    FOREIGN KEY (hotel_id) references Hotel(id) on update cascade on delete restrict
);

create table Rooms (
	room_id INT NOT NULL AUTO_INCREMENT,
	room_no INT NOT NULL,
    floor INT NOT NULL,
    capacity INT NOT NULL,
    cost FLOAT NOT NULL,
    hotel_id INT NOT NULL,
    PRIMARY KEY (room_id),
    FOREIGN KEY (hotel_id) REFERENCES Hotel(id) on delete cascade on update cascade
);

create table UserClient (
	id int not null,
    dob date not null,
    primary key (id),
    foreign key (id) references User(id) on delete cascade on update cascade
);

create table Booking (
	id int not null auto_increment,
    checkin_date Date,
    checkout_date Date,
    no_of_days int,
    cancelled boolean,
    user_id int,
    PRIMARY KEY (id),
    foreign key (user_id) references UserClient(id) on update cascade on delete restrict
);

create table OnlineBooking (
	oid int not null,
    primary key (oid),
    foreign key (oid) references Booking(id) on update cascade on delete restrict
);

create table OfflineBooking (
	ofid int not null,
    primary key (ofid),
    foreign key (ofid) references Booking(id) on update cascade on delete restrict
);

create table payment (
	pay_reference INT NOT NULL AUTO_INCREMENT,
    amount float,
    payment_method ENUM('CREDIT', 'DEBIT', 'UPI', 'MOBILE WALLET', 'CASH'),
	booking_id int not null,
    PRIMARY KEY (pay_reference),
    FOREIGN KEY (booking_id) references Booking(id) on update cascade on delete cascade
);



create table BookRooms (
	booking_id int not null,
    room_id int not null,
    primary key (booking_id, room_id),
    foreign key (booking_id) references Booking(id) on update cascade on delete cascade,
    foreign key (room_id) references Rooms(room_id) on delete cascade on update cascade
);

create table StaffBookRoom (
	staff_id int not null,
    user_id int not null,
    booking_id int not null,
    primary key (staff_id, user_id, booking_id),
    foreign key (staff_id) references Staff(id) on delete cascade,
    foreign key (user_id) references UserClient(id) on update cascade,
    foreign key (booking_id) references OfflineBooking(ofid) on update cascade
);

-- End of DDL


-- Proceedures

DROP procedure if exists createUser;
DELIMITER //
create procedure createUser(IN username varchar(100), IN user_email varchar(100), IN user_pass varchar(200), IN ddob date, IN address int)
BEGIN
declare temp int default 0;
if (user_pass = "na") then
    select count(*) into temp from User where email=user_email;
    if temp = 0 then
    	insert into User(name, user_password, email, address_id) values (username, user_pass, user_email, address);
        insert into UserClient (id, dob) values (LAST_INSERT_ID(), ddob);
    end if;
else
	insert into User(name, user_password, email, address_id) values (username, user_pass, user_email, address);
    insert into UserClient (id, dob) values (LAST_INSERT_ID(), ddob);
end if;
END //
DELIMITER ;

DROP procedure if exists searchUser;
DELIMITER //
create procedure searchUser(user_email varchar(100), pass varchar(200))
BEGIN
SELECT Uu.name, Staff.id, UserClient.id from (SELECT * FROM User where email=user_email and user_password=pass) as Uu left outer join Staff on Uu.id=Staff.id left outer join UserClient on Uu.id=UserClient.id;
END //
DELIMITER ;


DROP procedure if exists searchUserBookings;
DELIMITER //
create procedure searchUserBookings(user_email varchar(100))
BEGIN
SELECT b.*, h.*, r.*, p.*, ob.*, offf.*, u.* FROM Booking b
LEFT OUTER JOIN OnlineBooking ob ON ob.oid = b.id
LEFT OUTER JOIN OfflineBooking offf ON offf.ofid = b.id
LEFT OUTER JOIN BookRooms br ON br.booking_id = b.id
LEFT OUTER JOIN Rooms r ON r.room_id = br.room_id
LEFT OUTER JOIN Hotel h ON r.hotel_id = h.id
LEFT OUTER JOIN payment p ON p.booking_id = b.id 
LEFT OUTER JOIN User u on u.id = b.user_id
WHERE u.email = user_email;
END //
DELIMITER ; 

DROP procedure if exists searchStaffUserBookings;
DELIMITER //
create procedure searchStaffUserBookings()
BEGIN
SELECT b.*, h.*, r.*, p.*, ob.*, offf.*, u.* FROM Booking b
LEFT OUTER JOIN OnlineBooking ob ON ob.oid = b.id
LEFT OUTER JOIN OfflineBooking offf ON offf.ofid = b.id
LEFT OUTER JOIN BookRooms br ON br.booking_id = b.id
LEFT OUTER JOIN Rooms r ON r.room_id = br.room_id
LEFT OUTER JOIN Hotel h ON r.hotel_id = h.id
LEFT OUTER JOIN payment p ON p.booking_id = b.id 
LEFT OUTER JOIN User u on u.id = b.user_id; 
END //
DELIMITER ; 

-- End of Proceedures


-- Functions

DROP function if exists updateUser;
DELIMITER //
create function updateUser(userid int, user_name varchar(100), pass varchar(200), user_email varchar(100), st varchar(100), ci varchar(100), pi varchar(6), type varchar(10))
RETURNS INT
DETERMINISTIC MODIFIES SQL DATA
begin
declare temp int default -1;
select id into temp from Address where street=st and city=ci and pincode=pi;
if (temp = -1) then
	INSERT INTO Address (street, city, pincode) values (st, ci, pi);
    set temp = LAST_INSERT_ID();
end if;
update User set name=user_name, user_password=pass, email=user_email, address_id=temp where id=userid;
return null;
END //
DELIMITER ;

DROP function if exists bookRoom;
DELIMITER //
create function bookRoom(checkin_d date, checkout_d date, nof_days int, usermail varchar(100), amm float, pay_method varchar(30))
RETURNS INT
DETERMINISTIC MODIFIES SQL DATA
begin
declare temp int;
declare userid int;
select id into userid from User where email=usermail;
INSERT INTO Booking (checkin_date, checkout_date, no_of_days, cancelled, user_id) values (checkin_d, checkout_d, nof_days, 0, userid);
set temp = LAST_INSERT_ID();
INSERT INTO OnlineBooking (oid) values (temp);
INSERT INTO payment (amount, payment_method, booking_id) values (amm, pay_method, temp);
return temp;
END //
DELIMITER ; 

DROP function if exists bookOffRoom;
DELIMITER //
create function bookOffRoom(checkin_d date, checkout_d date, nof_days int, amm float, pay_method varchar(30), username varchar(100), mmail varchar(100), addd int, dob date, eemail varchar(100))
RETURNS INT
DETERMINISTIC MODIFIES SQL DATA
begin
declare temp int;
declare user__id int default 0;
declare staff__id int default 0;
declare off_id int default 0;
call createUser(username, mmail, "na", dob, addd);
select id into user__id from User where email=mmail;
select id into staff__id from User where email=eemail;
INSERT INTO Booking (checkin_date, checkout_date, no_of_days, cancelled, user_id) values (checkin_d, checkout_d, nof_days, 0, user__id);
set temp = LAST_INSERT_ID();
INSERT INTO OfflineBooking (ofid) values (temp);
INSERT INTO StaffBookRoom (staff_id, user_id, booking_id) values (staff__id, user__id, temp);
INSERT INTO payment (amount, payment_method, booking_id) values (amm, pay_method, temp);
return temp;
END //
DELIMITER ; 

DROP function if exists updateBookings;
DELIMITER //
create function updateBookings(checkin_d date, checkout_d date, nof_days int, payment float, bid int)
RETURNS INT
DETERMINISTIC MODIFIES SQL DATA
begin
UPDATE Booking SET checkin_date=checkin_d, checkout_date=checkout_d, no_of_days=nof_days where Booking.id = bid;
UPDATE payment SET amount = payment where booking_id = bid;
return null;
END //
DELIMITER ; 

-- End of Functions


-- Triggers

DROP TRIGGER if exists booking_validate_insert;
DELIMITER //
CREATE TRIGGER `booking_validate_insert`
	BEFORE INSERT
	ON `Booking`
	FOR EACH ROW
BEGIN
	IF NEW.`checkin_date` > NEW. `checkout_date` THEN
		SIGNAL SQLSTATE VALUE '45000'
			SET MESSAGE_TEXT = 'Checkin date has to be less than Checkout date';
	END IF;
END //
DELIMITER ;

DROP TRIGGER if exists booking_validate_update;
DELIMITER //
CREATE TRIGGER `booking_validate_update`
	BEFORE UPDATE
	ON `Booking`
	FOR EACH ROW
BEGIN
	IF NEW.`checkin_date` > NEW. `checkout_date` THEN
		SIGNAL SQLSTATE VALUE '45000'
			SET MESSAGE_TEXT = 'Checkin date has to be less than Checkout date';
	END IF;
END //
DELIMITER ;

DROP TRIGGER if exists booking_validate_insert_past;
DELIMITER //
CREATE TRIGGER `booking_validate_insert_past`
	BEFORE UPDATE
	ON `Booking`
	FOR EACH ROW
BEGIN
	IF NEW.`checkin_date` < CURDATE() THEN
		SIGNAL SQLSTATE VALUE '45000'
			SET MESSAGE_TEXT = 'Checkin date cannot be in past!';
	END IF;
END //
DELIMITER ;


DROP TRIGGER if exists user_mail_validate_insert;
DELIMITER //
CREATE TRIGGER `user_mail_validate_insert`
	BEFORE INSERT
	ON `User`
	FOR EACH ROW
BEGIN
	IF EXISTS (select email from User where email=NEW.`email`) THEN
		SIGNAL SQLSTATE VALUE '45000'
			SET MESSAGE_TEXT = 'User email already exists in DB!';
	END IF;
END //
DELIMITER ;

DROP TRIGGER if exists room_add;
DELIMITER //
CREATE TRIGGER `room_add`
	BEFORE INSERT
	ON `Rooms`
	FOR EACH ROW
BEGIN
	IF EXISTS (select room_no from Rooms where room_no=NEW.`room_no`) THEN
		SIGNAL SQLSTATE VALUE '45000'
			SET MESSAGE_TEXT = 'Room already exists in DB!';
	END IF;
END //
DELIMITER ;

-- End of Triggers


-- DML for Staff & Hotel

INSERT INTO Hotel (name) values ('The Royal Suite');
INSERT INTO Address (street, city, pincode) values ('444 Huntington Ave', 'Boston', '02115');
INSERT INTO Address (street, city, pincode) values ('1022 Huntington Ave', 'Boston', '02115');
INSERT INTO Address (street, city, pincode) values ('56 Huntington Ave', 'Boston', '02115');


INSERT INTO User (name, user_password, email, address_id) values ('John', 'johnpass', 'john@gmail.com', 1);
INSERT INTO User (name, user_password, email, address_id) values ('Michael', 'michaelpass', 'mike@gmail.com', 2);
INSERT INTO User (name, user_password, email, address_id) values ('Michille', 'michillepass', 'michille@gmail.com', 2);
INSERT INTO User (name, user_password, email, address_id) values ('Taylor', 'taylorpass', 'taylor@gmail.com', 3);

INSERT INTO Staff (id, hotel_id) values (1, 1);
INSERT INTO Staff (id, hotel_id) values (2, 1);
INSERT INTO Staff (id, hotel_id) values (3, 1);
INSERT INTO Staff (id, hotel_id) values (4, 1);

INSERT INTO Rooms(room_no, floor, capacity, cost, hotel_id) values (101, 1, 4, 300, 1);
INSERT INTO Rooms(room_no, floor, capacity, cost, hotel_id) values (102, 1, 2, 150, 1);
INSERT INTO Rooms(room_no, floor, capacity, cost, hotel_id) values (103, 1, 5, 400, 1);
INSERT INTO Rooms(room_no, floor, capacity, cost, hotel_id) values (201, 2, 6, 500, 1);
INSERT INTO Rooms(room_no, floor, capacity, cost, hotel_id) values (202, 2, 2, 150, 1);
INSERT INTO Rooms(room_no, floor, capacity, cost, hotel_id) values (203, 2, 3, 250, 1);
INSERT INTO Rooms(room_no, floor, capacity, cost, hotel_id) values (301, 3, 2, 125, 1);
INSERT INTO Rooms(room_no, floor, capacity, cost, hotel_id) values (302, 3, 3, 300, 1);
INSERT INTO Rooms(room_no, floor, capacity, cost, hotel_id) values (303, 3, 3, 275, 1);
INSERT INTO Rooms(room_no, floor, capacity, cost, hotel_id) values (401, 4, 1, 95, 1);

-- End of DML for Staff & Hotel
