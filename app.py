from flask import Flask, render_template, request, session, redirect, url_for
from db_query import createAddress, searchAddress, createUser, checkUserEmailExist, checkUserExist, getUserDetails, updateUser, getRooms, getBookings, bookOnlineRoom, bookRoom, getRoomIDs
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'test_secret_key'


def isLoggedIn():
    return "email" in session and session.get("email") is not None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if isLoggedIn():
        return redirect(url_for('home'))
    if request.method == "GET":
        return render_template("register.html", username="", email="", dob="", city="", pincode="", street="")
    else:
        f = request.form
        username, password, repass, email, dob, street, city, pincode = f.get("username"), f.get("psw"), f.get("psw-repeat"), f.get("email"), f.get("dob"), f.get("street"), f.get("city"), f.get("pincode")
        if checkUserEmailExist(email):
            return render_template("register.html", message="User already exist in db!", color="red", username=username, email=email, dob=dob, city=city, pincode=pincode, street=street)
        if len(password) < 8:
            return render_template("register.html", message="Password length cannot be less than 8!", color="red", username=username, email=email, dob=dob, city=city, pincode=pincode, street=street)
        if password != repass:
            return render_template("register.html", message="Passwords do not match", color="red", username=username, email=email, dob=dob, city=city, pincode=pincode, street=street)
        if datetime.now() < datetime.strptime(dob, "%Y-%m-%d"):
            return render_template("register.html", message="Date of Birth cannot be in future", color="red", username=username, email=email, dob=dob, city=city, pincode=pincode, street=street)
        
        add_id = searchAddress(street, city, pincode)
        if add_id == -1:
            add_id = createAddress(street, city, pincode)
        
        createUser(username, password, email, dob, add_id)
        return render_template("register.html", message="User Successfully created. Please login to continue", color="green")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if isLoggedIn():
        return redirect(url_for('home'))
    if request.method == "GET":
        return render_template("login.html")
    else:
        f = request.form
        email, password = f.get("email"), f.get("psw")
        check = checkUserExist(email, password)
        if check:
            session['username'] = check[0]
            session['email'] = email
            session['type'] = check[1]
            return redirect(url_for('home'))
        else:
            return render_template("login.html", message="User credentials mismatch!", color="red")

 
@app.route("/", methods=['GET'])
def home():
    sess = None
    if isLoggedIn():
        sess=session

    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)

    if (start_date is None or end_date is None) and not (start_date is None and end_date is None):
        return render_template("home.html", user=sess, message="Please select both start and end date")
    elif start_date is not None and end_date is not None:
        start_date, end_date = datetime.strptime(start_date, "%Y-%m-%d"), datetime.strptime(end_date, "%Y-%m-%d")
        if datetime.now() >= start_date or datetime.now() >= end_date:
            return render_template("home.html", user=sess, message="Booking cannot be in the past!", start_date=start_date.strftime("%Y-%m-%d"), end_date=end_date.strftime("%Y-%m-%d"))
        if start_date >= end_date:
            return render_template("home.html", user=sess, message="End date must be greater than Start Date", start_date=start_date.strftime("%Y-%m-%d"), end_date=end_date.strftime("%Y-%m-%d"))
        rooms, bookings, tmp = getRooms(), getBookings(), {}
        for i in bookings:
            if i[2] < start_date.date() or end_date.date() < i[1]:
                pass
            else:
                tmp[i[6]] = True
        return render_template("home.html", user=sess, rooms=[i for i in rooms if i[0] not in tmp], start_date=start_date.strftime("%Y-%m-%d"), end_date=end_date.strftime("%Y-%m-%d"))

    return render_template("home.html", user=sess)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not isLoggedIn():
        return render_template("error.html", message="You do not have permission to access the page!")
    else:
        if request.method == "GET":
            return render_template("profile.html", data=getUserDetails(session['email']))
        else:
            f, data = request.form, getUserDetails(session['email'])
            username, password, repass, email, dob, street, city, pincode = f.get("username"), f.get("psw"), f.get("psw-repeat"), f.get("email"), f.get("dob"), f.get("street"), f.get("city"), f.get("pincode")
            if password != repass:
                return render_template("profile.html", data=data, message="Passwords does not match!", color="red")
            if len(password) < 8:
                return render_template("profile.html", data=data, message="Passwords length cannot be less than 8!", color="red")
            if email != data[3] and checkUserEmailExist(email):
                return render_template("profile.html", data=data, message="Email already registered by another user", color="red")
            
            if username != data[1] or password != data[2] or email != session['email'] or street != data[9] or city != data[10] or pincode != data[11] or (dob is None or dob != data[8]):
                updateUser(data[0], username, password, email, street, city, pincode, session['type'])
                if email != session['email']:
                    session['email'] = email
                if username != session['username']:
                    session['username'] = username

                return render_template("profile.html", data=getUserDetails(session['email']), message="Profile Successfully Updated", color="green")
            else:
                return render_template("profile.html", data=data, message="No changes made to the profile", color="red")


@app.route("/logout", methods=['GET'])
def logout():
    if isLoggedIn():
        session.clear()
        return render_template("login.html", message="Sucessfully Logged out", color="green")
    else:
        return render_template("login.html", message="You need to first login to logout!", color="red")


def check_available(start, end, rooms):
    bookings = getBookings()
    rooms_len = len(rooms)
    print(rooms)
    for i in bookings:
        if not (i[2] < start.date() or end.date() < i[1]):
            if i[6] in rooms:
                rooms.remove(i[6])
    return rooms_len == len(rooms)

@app.route("/book", methods=['POST'])
def bookRoomView():
    if not isLoggedIn():
        return render_template("error.html", message="You do not have permission to perform the action!")

    # book the rooms
    d = request.json
    rooms = [getRoomIDs(i)[0][0] for i in d['room']]
    if not check_available(datetime.strptime(d['start_date'], "%Y-%m-%d"), datetime.strptime(d['end_date'], "%Y-%m-%d"), rooms):
        return {"message": "Rooms are not available on selected dates!", "error": 1}
    no_days = (datetime.strptime(d['end_date'], "%Y-%m-%d") - datetime.strptime(d['start_date'], "%Y-%m-%d")).days
    id = bookOnlineRoom(d['start_date'], d['end_date'], no_days, session.get("email"), d.get("cost").replace("$", ""), d['payment_type'])
    for i in rooms:
        bookRoom(i, id[0][0])
    return {"message": "Successfully Booked Rooms", "error": 0}
    

if __name__ == '__main__':
    app.run(debug=True, port=3000)