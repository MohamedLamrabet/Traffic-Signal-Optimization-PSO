# ====================================Import Modules====================================
from __future__ import absolute_import
from __future__ import print_function

import json
import os
import sys
import optparse
import random
import numpy as np
import inquirer

from mysqlDb import insertInDB, insertBestPhases, getSimulationTimeFromDB, getNumberOfGenerationFromDB

try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path
                    .join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of \
        your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci
from junction import Junction
from device import Device
from phaseConfig import setJunctionPhase

# ===============================Generate Route File====================================

# put code to generate route file here, or better make it in some other python file, import and then run here!

# ====================================Make Junctions====================================
junction_U = Junction(_id='U',
                      dev_a_dets=['0', '1', '2', '3', '4', '5'],
                      dev_b_dets=['6', '7', '8', '9', '10', '11'],
                      dev_c_dets=['54', '55', '56', '57', '58', '59'],
                      dev_d_dets=['60', '61', '62', '63', '64', '65'],
                      phaseMap={1: 1, 2: 2, 3: 4, 4: 3})

junction_L = Junction(_id='L',
                      dev_a_dets=['18', '19', '20', '21', '22', '23'],
                      dev_b_dets=['12', '13', '14', '15', '16', '17'],
                      dev_c_dets=['66', '67', '68', '69', '70', '71'],
                      dev_d_dets=['24', '25', '26', '27', '28', '29'],
                      phaseMap={1: 1, 2: 2, 3: 4, 4: 3})

junction_R = Junction(_id='R',
                      dev_a_dets=['30', '31', '32', '33', '34', '35'],
                      dev_b_dets=['48', '49', '50', '51', '52', '53'],
                      dev_c_dets=['36', '37', '38', '39', '40', '41'],
                      dev_d_dets=['42', '43', '44', '45', '46', '47'],
                      phaseMap={1: 3, 2: 1, 3: 2, 4: 4})

# set neighbours
junction_U.neighbours = [{'junction': junction_L, 'connection': ('d', 'b'), 'data': 0},
                         {'junction': junction_R, 'connection': ('c', 'b'), 'data': 0}]
junction_L.neighbours = [{'junction': junction_R, 'connection': ('c', 'a'), 'data': 0},
                         {'junction': junction_U, 'connection': ('b', 'd'), 'data': 0}]
junction_R.neighbours = [{'junction': junction_L, 'connection': ('a', 'c'), 'data': 0},
                         {'junction': junction_U, 'connection': ('b', 'c'), 'data': 0}]


# ========================================run()=========================================

def run(i, fitnessID, optID):
    global steps
    steps = 0

    endSimTIme = 30
    global allWaitingTime
    allWaitingTime = []
    global allTravelTime
    allTravelTime = []

    global allEmissionCO2
    allEmissionCO2 = []

    global allarrived
    allarrived = []
    global alldeparted
    alldeparted = []
    fitnessParticle = []
    phaseParticle = []

    fitnessFunctionID = fitnessID
    optimizationID = optID

    initial = [[[50, 23, 59], 0], [[23, 50, 45], 1], [[52, 7, 49], 1], [[22, 59, 38], 0], [[25, 7, 44], 0],
               [[32, 56, 59], 0], [[15, 46, 9], 1], [[10, 8, 44], 0], [[6, 57, 27], 0], [[40, 10, 33], 1],
               [[45, 44, 14], 0], [[59, 19, 56], 0], [[22, 12, 28], 1], [[8, 23, 26], 0], [[45, 16, 39], 1],
               [[56, 48, 57], 0], [[46, 51, 47], 0], [[17, 54, 51], 1], [[54, 30, 11], 0], [[36, 25, 30], 1],
               [[24, 41, 56], 0], [[47, 48, 39], 1], [[60, 28, 39], 0], [[52, 44, 18], 0], [[50, 58, 55], 0],
               [[8, 21, 9], 0], [[50, 24, 47], 1], [[32, 30, 19], 0], [[29, 38, 23], 0], [[13, 44, 45], 0]]

    x = 0
    print("iteration :", i)
    if i == 0:
        while steps < endSimTIme:

            num_stops = {}
            total_num_stops = 0
            total_delay = 0

            # traci.simulationStep()
            # PSOphase = individual(3)
            PSOphase = initial[x]
            x += 1
            phaseParticle.append(PSOphase)
            travelTime = []
            waitingTime = []

            co2_emission_edge = []
            co_emission_edge = []
            fuel_consumption = []
            noise_emission = []

            phase = (PSOphase[0][0] + PSOphase[0][1] + PSOphase[0][2]) / 3
            runDeviceDetect(phase)
            """
            gets data from devices for
            junctions for "time" number of simulation steps
            """
            edgeIDs = traci.edge.getIDList()
            for j in edgeIDs:
                travelTime.append(traci.edge.getTraveltime(j))
                waitingTime.append(traci.edge.getWaitingTime(j))
                co2_emission_edge.append(traci.edge.getCO2Emission(j))
                co_emission_edge.append(traci.edge.getCOEmission(j))
                fuel_consumption.append(traci.edge.getFuelConsumption(j))
                noise_emission.append(traci.edge.getNoiseEmission(j))

            if (sum(alldeparted) == 0):
                allWaitingTime.append(sum(waitingTime))
            else:
                allWaitingTime.append(sum(waitingTime) / sum(alldeparted))

            allTravelTime.append(sum(travelTime))

            total_co2_emission = sum(co2_emission_edge)
            total_co_emission = sum(co_emission_edge)
            total_fuel_consumption = sum(fuel_consumption)
            total_noise_emission = sum(noise_emission)

            allEmissionCO2.append(total_co2_emission)

            # Get a list of all vehicles in the simulation
            vehicles = traci.vehicle.getIDList()
            num_vehicles = len(vehicles)

            # Check each vehicle's current edge and speed to determine if it's stopped
            for vehicle_id in vehicles:
                current_edge = traci.vehicle.getRoadID(vehicle_id)
                current_speed = traci.vehicle.getSpeed(vehicle_id)
                total_delay += traci.vehicle.getAccumulatedWaitingTime(vehicle_id)

                # If the vehicle is stopped, increment the stop count for the current edge
                if current_speed < 0.1:
                    if current_edge in num_stops:
                        num_stops[current_edge] += 1
                    else:
                        num_stops[current_edge] = 1
            for edge in num_stops:
                total_num_stops += num_stops[edge]

            print()
            print("----------------------------------------------------------------------")
            print()
            print("Step : ", steps)
            print(f"There are {num_vehicles} vehicles in the network.")
            print("Avg phase ", phase)
            print("Waiting time: ")
            print(allWaitingTime)
            print("Travel time: ")
            print(allTravelTime)
            print("Arrived cars: ", sum(allarrived))
            print("Departed cars: ", sum(alldeparted))
            print("CO2 Emission in mg: ", total_co2_emission)
            print("Total CO emission in mg : ", total_co_emission)
            print("Total fuel consumption in ml : ", total_fuel_consumption)
            print("Total Emission in db : ", total_noise_emission)
            print("Total Number of stops : ", total_num_stops)
            print("Total delay in s: ", total_delay)
            print("Current Simulation time in s: ", traci.simulation.getTime())

            if fitnessFunctionID == 1:
                # Fitness number of stops
                fitness = total_num_stops

            elif fitnessFunctionID == 2:
                # Fitness co2 emission
                fitness = total_co2_emission

            elif fitnessFunctionID == 3:
                # Fitness total delay
                fitness = total_delay

            else:
                # Fitness Travel time

                Cr = phase * (7 / 21)
                if sum(allarrived) == 0:
                    fitness = (sum(waitingTime) + sum(travelTime) + (
                            sum(alldeparted) - sum(allarrived)) * traci.simulation.getTime()) / 1 + Cr
                else:
                    fitness = (sum(waitingTime) + sum(travelTime) + (
                            sum(alldeparted) - sum(allarrived)) * traci.simulation.getTime()) / (
                                  sum(allarrived)) ** 2 + Cr


            fitnessParticle.append(fitness)
            print("Phases: ", PSOphase[0], "Its fitness: ", fitness)

            if (sum(alldeparted) == 0):
                waiting_time = sum(waitingTime)
            else:
                waiting_time = sum(waitingTime) / sum(alldeparted)

            travel_time = sum(travelTime)
            current_simulation_time = traci.simulation.getTime()

            sum_arrived = sum(allarrived)
            sum_departed = sum(alldeparted)
            current_phase = json.dumps(PSOphase[0])

            insertInDB(i, optimizationID, steps, phase, waiting_time, travel_time, total_delay, total_num_stops,
                       sum_arrived, sum_departed, total_co2_emission,
                       total_co_emission, current_simulation_time, total_fuel_consumption, total_noise_emission,
                       current_phase, fitness)

            useAlgoAndSetPhase()
            """	
            use an algorithm to set the phase for the junctions
            """
            prepareJunctionVectArrs()
            '''
            prepare the vehicleVectarr for junctions
            '''

            setJunctionPhasesInSUMO()
            '''
            set the junction's phases in the SUMO simulator
            '''

            steps += 1

        value = min(fitnessParticle)
        idxg = fitnessParticle.index(value)
        pg.append(phaseParticle[idxg])
        pgf.append(value)
        allFitness.append(fitnessParticle)
        AllPSOphase.append(phaseParticle)

    else:
        steps = 0
        allWaitingTime = []
        allTravelTime = []
        allarrived = []
        alldeparted = []

        fitnessParticle = []

        updated = PSO(AllPSOphase[-1], allFitness[-1], pg, pgf)

        AllPSOphase.append(updated)
        h = 0

        while steps < endSimTIme:
            # traci.simulationStep()
            travelTime = []
            waitingTime = []
            co2_emission_edge = []
            co_emission_edge = []
            fuel_consumption = []
            noise_emission = []
            num_stops = {}
            total_num_stops = 0
            total_delay = 0

            particle = updated[h]
            # print ("len of updated",len(updated))
            h += 1
            phase = (particle[0][0] + particle[0][1] + particle[0][2]) / 3
            runDeviceDetect(phase)
            """
                gets data from devices for
                junctions for "time" number of simulation steps
            """

            edgeIDs = traci.edge.getIDList()

            for j in edgeIDs:
                travelTime.append(traci.edge.getTraveltime(j))
                waitingTime.append(traci.edge.getWaitingTime(j))
                co2_emission_edge.append(traci.edge.getCO2Emission(j))
                co_emission_edge.append(traci.edge.getCOEmission(j))
                fuel_consumption.append(traci.edge.getFuelConsumption(j))
                noise_emission.append(traci.edge.getNoiseEmission(j))

            if (sum(alldeparted) == 0):
                allWaitingTime.append(sum(waitingTime))
            else:
                allWaitingTime.append(sum(waitingTime) / sum(alldeparted))

            allTravelTime.append(sum(travelTime))

            total_co2_emission = sum(co2_emission_edge)
            total_co_emission = sum(co_emission_edge)
            total_fuel_consumption = sum(fuel_consumption)
            total_noise_emission = sum(noise_emission)

            allEmissionCO2.append(total_co2_emission)

            # Get a list of all vehicles in the simulation
            vehicles = traci.vehicle.getIDList()
            num_vehicles = len(vehicles)

            # Check each vehicle's current edge and speed to determine if it's stopped
            for vehicle_id in vehicles:
                current_edge = traci.vehicle.getRoadID(vehicle_id)
                current_speed = traci.vehicle.getSpeed(vehicle_id)
                total_delay += traci.vehicle.getAccumulatedWaitingTime(vehicle_id)

                # If the vehicle is stopped, increment the stop count for the current edge
                if current_speed < 0.1:
                    if current_edge in num_stops:
                        num_stops[current_edge] += 1
                    else:
                        num_stops[current_edge] = 1

            for edge in num_stops:
                total_num_stops += num_stops[edge]

            print()
            print("-----------------------------------------------------------------")
            print()
            print("Step : ", steps)
            print(f"There are {num_vehicles} vehicles in the network.")
            print("Avg phase : ", phase)
            print("Waiting time : ")
            print(allWaitingTime)
            print("Travel time : ")
            print(allTravelTime)
            print("Arrived cars : ", sum(allarrived))
            print("Departed cars : ", sum(alldeparted))
            print("CO2 Emission in mg: ", total_co2_emission)
            print("Total CO emission in mg : ", total_co_emission)
            print("Total fuel consumption in ml : ", total_fuel_consumption)
            print("Total Emission in db : ", total_noise_emission)
            print("Total Number of stops : ", total_num_stops)
            print("Total delay in s: ", total_delay)
            print("Current Simulation time in s: ", traci.simulation.getTime())

            if fitnessFunctionID == 1:
                # Fitness number of stops
                fitness = total_num_stops

            elif fitnessFunctionID == 2:
                # Fitness co2 emission
                fitness = total_co2_emission

            elif fitnessFunctionID == 3:
                # Fitness total delay
                fitness = total_delay

            else:
                # Fitness Travel time
                Cr = phase * (7 / 21)
                if sum(allarrived) == 0:
                    fitness = (sum(waitingTime) + sum(travelTime) + (
                            sum(alldeparted) - sum(allarrived)) * traci.simulation.getTime()) / 1 + Cr
                else:
                    fitness = (sum(waitingTime) + sum(travelTime) + (
                            sum(alldeparted) - sum(allarrived)) * traci.simulation.getTime()) / (
                                  sum(allarrived)) ** 2 + Cr

            fitnessParticle.append(fitness)

            print("Phases: ", particle[0], "Its fitness: ", fitness)

            if (sum(alldeparted) == 0):
                waiting_time = sum(waitingTime)
            else:
                waiting_time = sum(waitingTime) / sum(alldeparted)

            travel_time = sum(travelTime)
            current_simulation_time = traci.simulation.getTime()
            sum_arrived = sum(allarrived)
            sum_departed = sum(alldeparted)
            current_phase = json.dumps(particle[0])

            insertInDB(i, optimizationID, steps, phase, waiting_time, travel_time, total_delay, total_num_stops,
                       sum_arrived, sum_departed, total_co2_emission,
                       total_co_emission, current_simulation_time, total_fuel_consumption, total_noise_emission,
                       current_phase, fitness)

            useAlgoAndSetPhase()
            """
            use an algorithm to set the phase for the junctions
            """
            prepareJunctionVectArrs()
            '''
               prepare the vehicleVectarr for junctions
            '''

            setJunctionPhasesInSUMO()
            '''
             set the junction's phases in the SUMO simulator
            '''

            steps += 1

        allFitness.append(fitnessParticle)
        value = min(fitnessParticle)
        idx = fitnessParticle.index(value)
        pg.append(updated[idx])
        pgf.append(value)

    return pg, pgf


# =========================Supplimentary functions for run()===========================
def setJunctionPhasesInSUMO():
    setJunctionPhase(junction_U, setAllRed=False)
    setJunctionPhase(junction_L, setAllRed=False)
    setJunctionPhase(junction_R, setAllRed=False)

    return


def useAlgoAndSetPhase():
    junction_U.update()
    junction_L.update()
    junction_R.update()

    return


def runDeviceDetect(phase):
    for _ in np.arange(phase):
        junction_U.checkDevices()
        junction_L.checkDevices()
        junction_R.checkDevices()
        allarrived.append(traci.simulation.getArrivedNumber())
        alldeparted.append(traci.simulation.getDepartedNumber())
        traci.simulationStep()
        phase += 1

    return


def prepareJunctionVectArrs():
    junction_U.prepareVehVectarr()
    junction_L.prepareVehVectarr()
    junction_R.prepareVehVectarr()

    return


def PSO(particles, fitness, pg, pgf):
    updated = []
    minLFit = min(fitness)
    idxL = fitness.index(minLFit)
    pB = particles[idxL]

    bestfit = min(pgf)
    index = pgf.index(bestfit)
    pG = pg[index]

    for i in range(len(particles)):
        updated.append(updateParticle(particles[i], pB, pG))

    return updated


def updateParticle(particles, pB, pG):
    randRou1 = random.uniform(0, 1)
    randRou2 = random.uniform(0, 1)
    w = random.uniform(0.5, 1.0)

    vPlus1 = w * particles[1] \
             + randRou1 * ((pB[0][0] - particles[0][0]) + (pB[0][1] - particles[0][1]) + (pB[0][2] - particles[0][2])) \
             + randRou2 * ((pG[0][0] - particles[0][0]) + (pG[0][1] - particles[0][1]) + (pG[0][2] - particles[0][2]))

    particles[0][0] = abs(int(particles[0][0] + vPlus1))
    particles[0][1] = abs(int(particles[0][1] + vPlus1))
    particles[0][2] = abs(int(particles[0][2] + vPlus1))
    particles[1] = vPlus1
    for i in range(3):
        while particles[0][i] > 60:
            particles[0][i] = penalty(particles[0][i])
    return particles


def penalty(phase):
    phase = abs(phase - random.randint(30, 60))
    return phase


def individual(indSize):
    indv = []
    x = []
    for i in range(indSize):
        x.append(random.randint(5, 60))
    indv.append(x)
    rand = random.uniform(0, 1)
    v = 0
    if rand < 0.5:
        v = 0
    else:
        v = 1
    indv.append(v)
    return indv


# ===============================Start SUMO and call run()==============================
def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    # generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    global AllPSOphase
    AllPSOphase = []
    global allFitness
    allFitness = []
    global pg
    pg = []
    global pgf
    pgf = []
    BestResults = []
    bestFitnessResults = []

    questions = [
        inquirer.List('fitness',
                      message="Choose the fitness do you want?",
                      choices=['Number of stops', 'CO2 emission', 'Total delay', 'Travel time'],
                      ),
    ]
    answers = inquirer.prompt(questions)

    print("*****************************")
    print("Fitness: ", answers["fitness"])
    print("*****************************")

    # number of stops = 1, co2 emission = 2, total delay = 3, else travel time

    if answers["fitness"] == 'Number of stops':
        fitnessFunctionID = 1
    elif answers["fitness"] == 'CO2 emission':
        fitnessFunctionID = 2
    elif answers["fitness"] == 'Total delay':
        fitnessFunctionID = 3
    else:
        fitnessFunctionID = 4

    iterations =  int(input('Enter the number of iterations:'))
    print("*****************************")
    print("Nbr of iterations: ", iterations)
    print("*****************************")

    num_vehicles = int(input('Enter the max number of vehicles:'))
    print("*****************************")
    print("Max nbr of vehicles: ", num_vehicles)
    print("*****************************")

    optimizationID = 1

    sumoCmd = [sumoBinary, "-c", "../city.sumocfg", "-n",
               "../city.net.xml", "-r", "../trips.trips.xml",
               "--max-num-vehicles={}".format(num_vehicles)
               ]

    traci.start(sumoCmd)

    # simulation_time = getSimulationTimeFromDB()
    # number_of_generation = getNumberOfGenerationFromDB()

    for i in range(iterations):
        resultsOfi = run(i, fitnessFunctionID, optimizationID)

        bestphase = resultsOfi[0]
        bestFitness = resultsOfi[1]
        print("End of iteration: ", i)
        print("Best phases :")
        print(bestphase[-1][0])
        print("Best fitness :")
        print(bestFitness[i])
        print("----------------------------------------------------------------")
        BestResults.append(bestphase[-1][0])
        bestFitnessResults.append(bestFitness[i])

        insertBestPhases(optimizationID, i, bestphase[-1][0], bestFitness[i])

    print("Best fitness of all iterations: ")
    print(bestFitnessResults)
    print("Best phases of all iterations: ")
    print(BestResults)

    traci.close()
