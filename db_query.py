from db import server_connect

conn = server_connect()
cursor = conn.cursor()

def checkUserExist(email, password):
    cursor.callproc("searchUser", (email, password))
    o = []
    for res in cursor.stored_results():
        o.append(res.fetchall())
    o = o[0]
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

def getUserDetails(email):
    cursor.execute("SELECT * from (SELECT * FROM User where email=%s) as U left outer join Staff on U.id=Staff.id left outer join UserClient on U.id=UserClient.id left outer join Address on U.address_id = Address.id", (email,))
    return cursor.fetchall()[0]

def updateUser(id, username, password, email, street, city, pincode, type):
    cursor.execute("SELECT updateUser(%s, %s, %s, %s, %s, %s, %s, %s)", (int(id), username, password, email, street, city, pincode, type))
    cursor.fetchall()
    conn.commit()

