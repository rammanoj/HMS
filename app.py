from flask import Flask, render_template, request, session, redirect, url_for

from db_query import createAddress, searchAddress, createUser, checkUserEmailExist, checkUserExist, getUserDetails, updateUser, getRooms, getBookings, bookOnlineRoom, bookRoom, getRoomIDs, bookOfflineRoom, createRoom, deleteRoom,getBookingsForUser, deleteRoomBooking, updateBookings, get_stats
from datetime import datetime, timedelta
from mysql.connector import DatabaseError

app = Flask(__name__)
app.secret_key = 'test_secret_key'


def isLoggedIn():
    return "email" in session and session.get("email") is not None


def date(d):
     d =  datetime.strptime(d,"%y-%m-%d %H:%M")
     d.strftime("%d-%m-%y %H:%M")
     return d

app.add_template_filter(date)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if isLoggedIn():
        return redirect(url_for('home'))
    if request.method == "GET":
        return render_template("register.html", username="", email="", dob="", city="", pincode="", street="")
    else:
        f = request.form
        username, password, repass, email, dob, street, city, pincode = f.get("username"), f.get("psw"), f.get("psw-repeat"), f.get("email"), f.get("dob"), f.get("street"), f.get("city"), f.get("pincode")
        if len(password) < 8:
            return render_template("register.html", message="Password length cannot be less than 8!", color="red", username=username, email=email, dob=dob, city=city, pincode=pincode, street=street)
        if password != repass:
            return render_template("register.html", message="Passwords do not match", color="red", username=username, email=email, dob=dob, city=city, pincode=pincode, street=street)
        if datetime.now() < datetime.strptime(dob, "%Y-%m-%d"):
            return render_template("register.html", message="Date of Birth cannot be in future", color="red", username=username, email=email, dob=dob, city=city, pincode=pincode, street=street)
        
        add_id = searchAddress(street, city, pincode)
        if add_id == -1:
            add_id = createAddress(street, city, pincode)
        
        try:
            dat = getUserDetails(email)
            if len(dat) > 0 and dat[2] == "na":
                updateUser(dat[0], username, password, email, dob, street, city, pincode)
            else:
                createUser(username, password, email, dob, add_id)
        except DatabaseError as e:
            print(str(e))
            return render_template("register.html", message=str(e).split(":")[1], color="red", username=username, email=email, dob=dob, city=city, pincode=pincode, street=street)

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
        check = checkUserExist(email, password) if len(password) >= 8 else False
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
                tmp[i[8]] = True
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
    for i in bookings:
        if not (i[2] < start.date() or end.date() < i[1]):
            if i[8] in rooms:
                rooms.remove(i[8])
    return rooms_len == len(rooms)

@app.route("/book", methods=['POST'])
def bookRoomView():
    if not isLoggedIn():
        return render_template("error.html", message="You do not have permission to perform the action!")

    # book the rooms
    d = request.json
    if session.get("type").lower() == "staff":
        if d['user'] == "":
            return {"message": "Username cannot be empty!", "error": 1}


    rooms = [getRoomIDs(i)[0][0] for i in d['room']]
    if not check_available(datetime.strptime(d['start_date'], "%Y-%m-%d"), datetime.strptime(d['end_date'], "%Y-%m-%d"), rooms):
        return {"message": "Rooms are not available on selected dates!", "error": 1}
        
    no_days = (datetime.strptime(d['end_date'], "%Y-%m-%d") - datetime.strptime(d['start_date'], "%Y-%m-%d")).days

    try:
        if session.get("type").lower() == "staff":
            if datetime.now() < datetime.strptime(d['dob'], "%Y-%m-%d"):
                return {"message": "DOB cannot be in future!", "error": 1}
            add_id = searchAddress(d['street'], d['city'], d['pincode'])
            if add_id == -1:
                add_id = createAddress(d['street'], d['city'], d['pincode'])
            id = bookOfflineRoom(d['start_date'], d['end_date'], no_days, d.get("cost").replace("$", ""), d['payment_type'], d['user'], d['email'], add_id, datetime.strptime(d['dob'], "%Y-%m-%d"))
        else:
            id = bookOnlineRoom(d['start_date'], d['end_date'], no_days, session.get("email"), d.get("cost").replace("$", ""), d['payment_type'])
    except DatabaseError as e:
        print(str(e))
        return {"message": str(e).split(":")[1], "error": 1}

    for i in rooms:
        bookRoom(i, id[0][0])
    return {"message": "Successfully Booked Rooms", "error": 0}

@app.route('/history', methods=['GET', 'POST'])
def history():
    if not isLoggedIn():
        return render_template("error.html", message="You do not have permission to access the page!")
    else:
        bookings, data = getBookingsForUser(session['email'], session['type']), {}
        for booking in bookings:
            today, operation = datetime.today().strftime("%Y-%m-%d"), None
            if booking[2].strftime("%Y-%m-%d") < today:
                operation = "past"
            elif booking[1].strftime("%Y-%m-%d") <= today and today <= booking[2].strftime("%Y-%m-%d"):
                operation = "present"
            else:
                operation = "future"

            if session['type'].lower() != "staff":
                if booking[0] not in data:
                    data[booking[0]] = {"data": {
                        "start_date": datetime.strftime(booking[1], "%Y-%m-%d"),
                        "end_date": datetime.strftime(booking[2], "%Y-%m-%d"),
                        "rooms": [[booking[9], booking[10]]],
                        "cost": "$" + str(booking[15]),
                        "payment_type": booking[16],
                        "days": booking[3],
                        "op": operation,
                        "cancelled": 0 if booking[4] == True else 1,
                        "id": booking[0]
                    }, "op": operation }
                else:
                    data[booking[0]]['data']['rooms'].append([booking[9], booking[10]])
            else:
                if booking[0] not in data:
                    data[booking[0]] = {"data": {
                        "start_date": datetime.strftime(booking[1], "%Y-%m-%d"),
                        "end_date": datetime.strftime(booking[2], "%Y-%m-%d"),
                        "rooms": [[booking[9], booking[10]]],
                        "cost": "$" + str(booking[15]),
                        "payment_type": booking[16],
                        "type": "offline" if booking[21] != None else "online",
                        "user": booking[21],
                        "days": booking[3],
                        "op": operation,
                        "cancelled": 0 if booking[4] == True else 1,
                        "id": booking[0]
                    }, "op": operation }
                else:
                    data[booking[0]]['data']['rooms'].append([booking[9], booking[10]])

        if request.method == "GET":
            return render_template("history.html", data = data)
        else:
            deleteRoomBooking(request.json.get("id"))
            return {"message": "Cancelled the booking", "error": 0}

@app.route("/rooms", methods=["GET", "POST"])
def RoomsView():
    if not isLoggedIn():
        render_template("error.html", message="You do not have permission to perform this action!")

    if session.get("type").lower() != "staff":
        render_template("error.html", message="You do not have permission to access this page!")

    if request.method == "GET":
        return render_template("rooms.html", rooms=getRooms())
    else:
        # create newly added room
        d = request.json
        if d['operation'] == "create":
            if d['room'] == "" or d['cost'] == "" or d['floor'] == "" or d['capacity'] == "":
                return {"message": "Please fill all the values", "error": 1}

            try:
                if int(d['room']) < 0 or int(d['cost']) < 0 or int(d['floor']) < 0 or int(d['capacity']) < 0:
                    return {"message": "Values cannot be negative", "error": 1}
            except Exception as e:
                return {"message": "Enter a valid integer!", "error": 1}

            try:
                id = createRoom(d['room'], d['cost'], d['floor'], d['capacity'])
                return {"message": "Room create successfully", "error": 0, "id": id}
            except DatabaseError as e:
                return {"message": str(e).split(":")[1], "error": 1}
        else:
            deleteRoom(d['room'])
            return {"message": "Room successfully deleted", "error": 0}


@app.route("/update_booking", methods=["POST"])
def updateBooking():
    if not isLoggedIn():
        render_template("error.html", message="You do not have permission to perform this action!")

    d = request.json
    start, end = datetime.strptime(d['start_date'],  "%Y-%m-%d"), datetime.strptime(d['end_date'],  "%Y-%m-%d")
    bookings = getBookings()
    for i in bookings:
        if i[0] == d['id']:
            continue
        if not (i[2] < start.date() or end.date() < i[1]):
            if i[9] in d['rooms']:
                return {"message": "Rooms not available on specified dates!", "error": 1}
        
    cost = 0
    no_days = (end-start).days
    for i in getRooms():
        if i[1] in d['rooms']:
            cost += no_days * i[4]

    try:
        updateBookings(start, end, no_days, cost, d['id'])
    except DatabaseError as e:
        print(str(e))
        return {"message": str(e).split(":")[1], "error": 1}

    return {"message": "Successfully updated bookings", "error": 0, "cost": cost, "no_days": no_days}


@app.route("/stats", methods=["GET"])
def stats():
    if not isLoggedIn():
        return render_template("error.html", message="You do not have permission to perform this action!")

    if session.get("type") != "Staff":
        return render_template("error.html", message="You do not have permission to perform this action!")

    if "start_date" not in request.args and "end_date" not in request.args:
        return render_template("stats.html")

    if "start_date" not in request.args or "end_date" not in request.args:
        return render_template("stats.html", message="Both dates need to be specified", error=1)


    start_date = datetime.strptime(request.args['start_date'],  "%Y-%m-%d")
    end_date = datetime.strptime(request.args['end_date'],  "%Y-%m-%d")

    if (end_date - start_date).days > 365:
        return render_template("stats.html", message="Time span cannot me more than 1 year!", error=1, start=request.args['start_date'], end=request.args['end_date'])

    if (end_date - start_date).days < 60:
        return render_template("stats.html", message="Time span cannot me less than 60 days!", error=1, start=request.args['start_date'], end=request.args['end_date'])

    out = {}
    iter = start_date
    while iter < end_date:
        out[iter.month] = 0
        iter += timedelta(days=30)
    for i in get_stats(start_date, end_date):
        out[i[1].month] += 1
    return render_template("stats.html", stats={"data": out}, disp=True, start=request.args['start_date'], end=request.args['end_date'])

if __name__ == '__main__':
    app.run(debug=True, port=3000)