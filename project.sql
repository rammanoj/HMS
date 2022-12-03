
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
    foreign key (address_id) references Address(id) on update cascade
);

create table Staff (
	id INT NOT NULL,
    hotel_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id) references User(id) on delete cascade,
    FOREIGN KEY (hotel_id) references Hotel(id) on delete cascade
);

create table Rooms (
	room_id INT NOT NULL AUTO_INCREMENT,
	room_no INT NOT NULL,
    floor INT NOT NULL,
    capacity INT NOT NULL,
    cost FLOAT NOT NULL,
    hotel_id INT NOT NULL,
    PRIMARY KEY (room_id),
    FOREIGN KEY (hotel_id) REFERENCES Hotel(id) on delete cascade
);

create table Booking (
	id int not null auto_increment,
    checkin_date Date,
    checkout_date Date,
    no_of_days Date,
    cancelled boolean,
    PRIMARY KEY (id)
);

create table UserClient (
	id int not null,
    dob date not null,
    primary key (id),
    foreign key (id) references User(id) on delete cascade
);

create table OnlineBooking (
	oid int not null,
    primary key (oid),
    user_id int not null,
    foreign key (user_id) references UserClient(id) on update cascade,
    foreign key (oid) references Booking(id) on update cascade
);

create table OfflineBooking (
	ofid int not null,
    primary key (ofid),
    foreign key (ofid) references Booking(id) on update cascade
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
    foreign key (room_id) references Rooms(room_id) on delete cascade
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

DROP procedure if exists createUser;
DELIMITER //
create procedure createUser(IN username varchar(100), IN user_email varchar(100), IN user_pass varchar(200), IN ddob date, IN address int)
BEGIN
start transaction;
if (user_pass is null) then
	insert into User(name, email, address_id) values (username, user_email, address);
else
	insert into User(name, user_password, email, address_id) values (username, user_pass, user_email, address);
end if;
insert into UserClient (id, dob) values (LAST_INSERT_ID(), ddob);
commit;
END //
DELIMITER ;

DROP procedure if exists searchUser;
DELIMITER //
create procedure searchUser(user_email varchar(100), pass varchar(200))
BEGIN
SELECT Uu.name, Staff.id, UserClient.id from (SELECT * FROM User where email=user_email and user_password=pass) as Uu left outer join Staff on Uu.id=Staff.id left outer join UserClient on Uu.id=UserClient.id;
END //
DELIMITER ;

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