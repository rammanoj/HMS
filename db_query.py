from db import server_connect

conn = server_connect()
cursor = conn.cursor()

def checkUserExist(email, password):
    cursor.execute("SELECT Uu.name, Staff.id, UserClient.id from (SELECT * FROM User where email=%s and user_password=%s) as Uu left outer join Staff on Uu.id=Staff.id left outer join UserClient on Uu.id=UserClient.id", (email, password))
    o = cursor.fetchall()
    if len(o) > 0:
        if o[0][1] == None:
            return [o[0][0], "Client"]
        else:
            return [o[0][0], "Staff"]
    else:
        return False
    

def checkUserEmailExist(mailAdd):
    cursor.execute("SELECT * FROM User where email=%s", (mailAdd,))
    o = cursor.fetchall()
    return len(o) > 0

def createUser(username, password, email, dob, addressId):
    cursor.callproc("createUser", [username, email, password, dob, addressId])
    conn.commit()


def searchAddress(street, city, pincode):
    cursor.execute("SELECT * from Address where street=%s and city=%s and pincode=%s", (street, city, pincode))
    o = cursor.fetchall()
    if len(o) > 0:
        return o[0][0]
    else:
        return -1


def createAddress(street, city, pincode):
    cursor.execute("INSERT INTO Address (street, city, pincode) values (%s, %s, %s)", (street, city, pincode))
    conn.commit()
    return cursor.lastrowid

