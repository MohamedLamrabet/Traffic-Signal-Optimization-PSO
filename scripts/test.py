import datetime
import time

import mysql.connector

myconn = mysql.connector.connect(host="localhost", user="root", passwd="", database="traffic")

# creating the cursor object
cur = myconn.cursor()
sql = "insert into `steps`(`avg_phase`, `waiting_time`, `travel_time`, `arrived_cars`, `departed_cars`, " \
      "`current_simulation_time`, `phases`, `fitness`, `created_at`, `updated_at`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# # The row values are provided in the form of tuple
ts = time.time()
created_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
updated_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

val = (10.11, 10.11, 10.11, 1, 1, 10.1, "[1, 2, 3]", 10.2, created_at, updated_at)

try:
    # inserting the values into the table
    cur.execute(sql, val)

    # commit the transaction
    myconn.commit()

except:
    myconn.rollback()

print(cur.rowcount, "record inserted!")
myconn.close()
