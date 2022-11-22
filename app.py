from flask import Flask, render_template, request, session, redirect, url_for
from db_query import createAddress, searchAddress, createUser, checkUserEmailExist, checkUserExist
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
            print(check)
            session['username'] = check[0]
            session['email'] = email
            session['type'] = check[1]
            return redirect(url_for('home'))
        else:
            return render_template("login.html", message="User credentials mismatch!", color="red")


@app.route("/", methods=['GET'])
def home():
    if isLoggedIn():
        print(session.get("username"))
        return render_template("home.html", user=session.get('username'), logged=True)
    else:
        return render_template("home.html", logged=False)

@app.route("/logout", methods=['GET'])
def logout():
    if isLoggedIn():
        session.clear()
        return render_template("login.html", message="Sucessfully Logged out", color="green")
    else:
        return render_template("login.html", message="You need to first login to logout!", color="red")



if __name__ == '__main__':
    app.run(debug=True, port=3000)