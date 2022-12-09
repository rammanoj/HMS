# HMS

An App for the Hotel to help manage it's bookings.


## Setup

- Download the provided zip file to local directory.
- Download and Install MYSQL (version: 8.0.31) into the local system using [this][1]
- Extract the downloaded project zip. All the requirements of the project zip are present in requirements.txt file.
- This project uses Python-Flask for backend and Javascript, Bootstrap for frontend.
- Create a new virtual environment using this [link][2]
- Once installed, activate the virtual environment using the following command:
``` 
source <venv-name>/bin/activate
```
- Replace `<venv-name>` with the name provided at creation of virtual environment.
- Now install all the dependencies using the following command (from the root directory):
```
pip install -r requirements.txt
```
- Once all the dependencies are installed, Change file `<project-root>/globals.py` and configure the appropriate mysql host, username and password.
- Now run the app using the following command from project root directory.
```
cd <project-root>
python3 app.py

or 

python app.py (only if your virutalenv by default picks python3)
```




## Tech Stack:

- Database: [MySQL (Version: 8.0.31)][1]
- Backend: [Flask][3]
- Frontend: HTML5, CSS, Javascript, Bootstrap, Jquery


## Diagrams
- The project flow, logical, conceptual diagrams can be found at `<project-root>/diagrams` folder.
- It also contains the project proposal file with the detailed list of what comamnds being used at what places.


## Lessons Learned
- Flask Tempaltes
- Javascript AJAX
- A lot of knowledge on MYSQL functions, triggers, proceedures, error handling etc.


## Future Work:
- This could be used by any of the hotels that could help them manage their bookings and store the data.
- Update Booking can have more update options like changing rooms etc.
- Automatically providing the list of rooms by taking-in the capcity instead of manually asking users to select rooms according to capacity.
- Ability to update existing rooms cost/capacity for the Staff


## Commands Operations:

Procedures:
createUser: This procedure is a transaction that takes the user name, password, date of birth and address as input and inserts the values into the user table. It also inserts the id created into UserClient table.
searchUser: This procedure takes email and password as input and queries the user and user client table to check if a user exists.
searchUserBookings: This procedure takes email id as an argument and returns all the bookings done by the user by querying the database with multi-joins.
searchStaffUserBookings: This procedure returns all the bookings done by the all users and staff so far by querying the database with multi-joins.
Functions:
updateUser: This function takes a user’s userid,user name, password email id, street, city, pincode , type of user and updates the address and user table.
bookRoom: This function takes date, checkout date, no of days stay, user mail id, total amount, payment method as arguments and inserts into Booking table, OnlineBooking table, payment table.
bookOffRoom: This function takes checkin date, checkout date, no of days, user mail id, total amount, payment method, username, user id as arguments inserts into Booking table, OfflineBooking table, payment table.

Trigger
booking_validate_insert: This trigger validates booking information before inserting the information to booking table. 
booking_validate_update: This trigger validates booking information before updating the information to booking table. 
user_mail_validate_insert: This trigger validates email before inserting into user table.
room_add: This trigger checks if the room already exists before inserting a room into a room table.

Crud Operations:
checkUserEmailExist: Select user data from User table to check if user exists.
searchAddress: Select address from Address table to check if address exists.
createAddress: Inserts values into address table
getUserDetails: Selects user data from user table based on email.
updateUser: Updates the values of user based on mail id
getRooms: Selects all rooms data from Rooms table 
getBookings: Selects all bookings from bookings table
bookOnlineRoom: Selects data from bookRoom table based on arguments provided.





[1]: https://dev.mysql.com/downloads/mysql/
[2]: https://docs.python.org/3/library/venv.html#creating-virtual-environments
[3]: https://flask.palletsprojects.com/en/2.2.x/installation/