from mysql.connector import connect
from globals import MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_CHARSET


def server_connect():
    try: 
        conf = {
            'host': MYSQL_HOST,
            "port": MYSQL_PORT,
            "database": MYSQL_DB,
            "user": MYSQL_USERNAME,
            "password": MYSQL_PASSWORD,
            "charset": MYSQL_CHARSET
        }
        conn = connect(**conf)
        return conn
    except Exception as e:
        print("Unable to connect to database!")
        exit(1)


# conn = server_connect()
# cur = conn.cursor()
# cur.execute("SELECT * FROM township")
# towns = cur.fetchall()
# for i in towns:
#     print(str(i[1]) + ", " + str(i[2]))
# print("Enter any of the above town, states")
# town = validate_db(towns, 1, "town")

# while True:
#     tmp = False
#     state = validate_db(towns, 2, "State")
#     for i in towns:
#         if i[2] == state and i[1] == town:
#             tmp = True
#             break
#     if tmp:
#         break
#     print("Entered State is not associated with the given town!")
    


# cur.callproc("allReceivers", [town, state])
# out = cur.stored_results()
# o_data = []
# for i in out:
#         o_data += i.fetchall()


# if len(o_data) == 0:
#     print("No data found for the given inputs!")

# print("\nAllReceivers Data: ")
# print("rid, location, sponsor, area, deployed, hauled, detections, individual_sharks_detected, bayside, town, state")
    
# for i in o_data:
#     print(", ".join(str(v) for v in i))

# cur.close()
# conn.close()


