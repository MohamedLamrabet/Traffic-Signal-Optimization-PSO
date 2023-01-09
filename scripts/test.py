import datetime
import time

import mysql.connector

myconn = mysql.connector.connect(host="localhost", user="root", passwd="", database="traffic")

# creating the cursor object
cur = myconn.cursor()
sql = "insert into `steps`(`steps`,`avg_phase`, `waiting_time`, `travel_time`, `arrived_cars`, `departed_cars`,`current_simulation_time`, `phases`, `fitness`, `created_at`, `updated_at`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# # The row values are provided in the form of tuple
ts = time.time()
created_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
updated_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

val = (0, 44.0, 24, 10.0, 0, 43, 44.0, "[50, 23, 59]", 2984.635455416006,
           created_at, updated_at)

try:
    # inserting the values into the table
    cur.execute(sql, val)

    # commit the transaction
    myconn.commit()

except TypeError as e:
    print(e)
    myconn.rollback()

print(cur.rowcount, "record inserted!")
myconn.close()
