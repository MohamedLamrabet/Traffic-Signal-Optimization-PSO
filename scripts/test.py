import datetime
import time

import mysql.connector
import json
#
# myconn = mysql.connector.connect(host="localhost", user="root", passwd="", database="traffic")
# cur = myconn.cursor()
# try:
#     cur.execute("SELECT simulation_period FROM optimizations ORDER BY id DESC LIMIT 1;")
#     result = cur.fetchone()
#     # for x in result:
#     print("%d"%(result[0]))
# except:
#     myconn.rollback()
# myconn.close()


myconn = mysql.connector.connect(host="localhost", user="root", passwd="", database="traffic")

# creating the cursor object
cur = myconn.cursor()
sql = "insert into `best_phases`(`phases`, `created_at`, `updated_at`)" \
      " values (%s, %s, %s)"

ts = time.time()
created_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
updated_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

phase = json.dumps([1,0,1])

val = (phase, created_at, updated_at)

try:
    # inserting the values into the table
    cur.execute(sql, val)

    # commit the transaction
    myconn.commit()

except BaseException as e :
    print(e)
    myconn.rollback()

print(cur.rowcount, "record inserted!")
myconn.close()