from flask import Flask, render_template, request, session, redirect, url_for
from db_query import createAddress, searchAddress, createUser, checkUserEmailExist, checkUserExist, getUserDetails, updateUser
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'test_secret_key'


def isLoggedIn():
    return "email" in session and session.get("email") is not None

@app.route('/register', methods=['GET', 'POST'])
def register():
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
    if isLoggedIn():
        return render_template("home.html", user=session.get('username'), logged=True)
    else:
        return render_template("home.html", logged=False)


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



if __name__ == '__main__':
    app.run(debug=True, port=3000)