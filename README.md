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





[1]: https://dev.mysql.com/downloads/mysql/
[2]: https://docs.python.org/3/library/venv.html#creating-virtual-environments
[3]: https://flask.palletsprojects.com/en/2.2.x/installation/