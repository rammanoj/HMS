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



