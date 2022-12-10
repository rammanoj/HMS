# HMS

An App for the Hotel to help manage it's bookings.


## Setup

- Download the provided zip file to local directory.
- Download and Install MYSQL (version: 8.0.31) into the local system using [this][1].
- Extract the downloaded project zip. All the requirements of the project zip are present in requirements.txt file.
- Download Python3 from [here][4]. It on windows, add python path to the PATH variable to access it via terminal.
- Create a new virtual environment using this [link][2]
- Once installed, activate the virtual environment using the following command:
``` 
source <venv-path>/bin/activate (for linux/mac)
call <venv-path>\Scripts\activate (for windowss)
```
- Replace `<venv-path>` with the name provided at creation of virtual environment.
- Now install all the dependencies using the following command (from the root directory):
```
source <path-to-virtualenv>/bin/activate (for mac/linux)
call <path-to-virtualenv>\Scripts\activate (for windows)

python -m pip (only if pip is not installed)
pip install -r requirements.txt
```
- Once all the dependencies are installed, Change file `<project-root>/globals.py` and configure the appropriate mysql host, username and password.
- Now run the files `<project-root>/project_dump.sql` or `<project-root>/project.sql` to create the database and run pre-defined DDL, DML statements.
- Finally, run the app using the following command from project root directory.
```
cd <project-root>
python3 app.py

or 

python app.py (only if your virutalenv by default picks python3)
```

- Visit http://127.0.0.1:3000/ to see the running instance of the app.

## Structure
- There are two types of users:
    - Staff: Admins to the site who can perform offline bookings, view / update rooms, get stats etc.
    - Users: clients who book rooms at the hotel.
- You can login to the app with email `john@gmail.com` and password `johnpass`. John is of type Staff.
    - Staff can:
        - Book offline rooms
        - View statistics of bookings
        - Add / delete rooms from hotel
        - View all the bookings.
        - Update / delete any booking.
        - Update his/her profile

- Now, to book a room as a user. Register to the app providing name, email, address. Once registered, you can login with the same credentials. 
    - User can:
        - Book a room online.
        - View his/her bookings.
        - Update his/her profile
        - Update his/her future booking
        - Cancel his/her booking.


## Tech Stack:

- Database: [MySQL (Version: 8.0.31)][1]
- Backend: [Flask][3]
- Frontend: HTML5, CSS, Javascript, Bootstrap, Jquery


## Diagrams
- The project flow, logical, conceptual diagrams can be found at `<project-root>/diagrams` folder.
- It also contains the project proposal file with the detailed list of what comamnds being used at what places.


## Lessons Learned
#### Technical expertise gained
- Flask Tempaltes
- Javascript AJAX
- A lot of knowledge on MYSQL functions, triggers, proceedures, error handling etc.

#### Time management
We understood how to manage time equally between different parts of the project. Since the backend included dealing with SQL
and and querying the database from flask application. Though frontend was taking more time, we tried to dedicate more time to the backend rather than frontend as backend was more important in this project. 

#### Alternative design


## Future Work:
- This could be used by any of the hotels that could help them manage their bookings and store the data.
- Update Booking can have more update options like changing rooms etc.
- Automatically providing the list of rooms by taking-in the capcity instead of manually asking users to select rooms according to capacity.
- Ability to update existing rooms cost/capacity for the Staff


## Commands Operations:


### Procedures:

- **createUser:** This procedure is a transaction that takes the user name, password, date of birth and address as input and inserts the values into the user table. It also inserts the id created into UserClient table.
- **searchUser:** This procedure takes email and password as input and queries the user and user client table to check if a user exists.
searchUserBookings: This procedure takes email id as an argument and returns all the bookings done by the user by querying the database with multi-joins.
- **searchUserBookings:** This proceedure returns all the bookings done by a specific user.
- **searchStaffUserBookings:** This procedure returns all the bookings done by the all users and staff so far by querying the database with multi-joins.


### Functions:

- **updateUser:** This function takes a user’s userid,user name, password email id, street, city, pincode , type of user and updates the address and user table.
- **bookRoom:** This function takes date, checkout date, no of days stay, user mail id, total amount, payment method as arguments and inserts into Booking table, OnlineBooking table, payment table.
- **bookOffRoom:** This function takes checkin date, checkout date, no of days, user mail id, total amount, payment method, username, user id as arguments inserts into Booking table, OfflineBooking table, payment table.
- **updateBookings:** Updates the bookings.


### Triggers:

- **booking_validate_insert:** This trigger validates booking information before inserting the information to booking table. 
- **booking_validate_update:** This trigger validates booking information before updating the information to booking table. 
- **user_mail_validate_insert:** This trigger validates email before inserting into user table.
- **room_add:** This trigger checks if the room already exists before inserting a room into a room table.


## CRUD Operations:

- **checkUserEmailExist:** Select user data from User table to check if user exists.
- **searchAddress:** Select address from Address table to check if address exists.
- **createAddress:** Inserts values into address table
- **getUserDetails:** Selects user data from user table based on email.
- **updateUser:** Updates the values of user based on mail id
- **getRooms:** Selects all rooms data from Rooms table 
- **getBookings:** Selects all bookings from bookings table
- **bookOnlineRoom:** Selects data from bookRoom table based on arguments provided.
- **UpdateOnlineBooking:** updates the booking.
- **getRooms:** get the list of available rooms.
- **AddRooms:** Adds a room to the hotel.
- **DeleteRooms:** Delete a speciifed room from the hotel.





[1]: https://dev.mysql.com/downloads/mysql/
[2]: https://docs.python.org/3/library/venv.html#creating-virtual-environments
[3]: https://flask.palletsprojects.com/en/2.2.x/installation/
[4]: https://www.python.org/downloads/
