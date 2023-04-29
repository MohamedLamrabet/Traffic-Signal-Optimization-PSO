import datetime
import json
import time

import mysql.connector


def insertInDB(i, optimization_id, steps, phase, waiting_time, travel_time, total_delay, num_stops, sum_arrived,
               sum_departed, total_co2_emission,
               total_co_emission, total_fuel_consumption, total_noise_emission, current_simulation_time,
               current_phase, fitness):
    # Create the connection object
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="", database="traffic")

    # creating the cursor object
    cur = myconn.cursor()
    sql = "insert into `iterations`(`iterations`,`optimization_id`, `steps`,`avg_phase`, `waiting_time`, `travel_time`, `total_delay`, `num_stops`, `arrived_cars`, `departed_cars`, " \
          "`co2_emission`,`co_emission`,`fuel_consumption`,`noise_emission`, `current_simulation_time`, `phases`, `fitness`, `created_at`, `updated_at`)" \
          " values (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    ts = time.time()
    created_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    updated_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    val = (
        i, optimization_id, steps, phase, waiting_time, travel_time, total_delay, num_stops, sum_arrived, sum_departed,
        total_co2_emission,
        total_co_emission, current_simulation_time, total_fuel_consumption, total_noise_emission,
        current_phase, fitness, created_at, updated_at)

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


def getSimulationTimeFromDB():
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="", database="traffic")
    cur = myconn.cursor()
    try:
        cur.execute("SELECT simulation_period FROM optimizations ORDER BY id DESC LIMIT 1;")
        result = cur.fetchone()

        return result[0]
    except:
        myconn.rollback()
    myconn.close()


def getNumberOfGenerationFromDB():
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="", database="traffic")
    cur = myconn.cursor()
    try:
        cur.execute("SELECT number_of_generation FROM optimizations ORDER BY id DESC LIMIT 1;")
        result = cur.fetchone()

        return result[0]
    except:
        myconn.rollback()
    myconn.close()


def insertBestPhases(optimization_id, iteration, phase, fitness):
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="", database="traffic")

    # creating the cursor object
    cur = myconn.cursor()
    sql = "insert into `best_results`(`optimization_id`,`iterations`,`phases`,`fitness`, `created_at`, `updated_at`)" \
          " values (%s,%s, %s, %s, %s, %s)"

    ts = time.time()
    created_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    updated_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    phase = json.dumps(phase)

    val = (optimization_id, iteration, phase, fitness, created_at, updated_at)

    try:
        # inserting the values into the table
        cur.execute(sql, val)

        # commit the transaction
        myconn.commit()

    except BaseException as e:
        print(e)
        myconn.rollback()

    print(cur.rowcount, "record inserted!")
    myconn.close()
