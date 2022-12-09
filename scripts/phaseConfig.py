import os, sys
import copy
if 'SUMO_HOME' in os.environ:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)
else:   
	sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

def setJunctionPhase(junction, setAllRed):
	if setAllRed == True:
		traci.trafficlight.setRedYellowGreenState(junction._id, "rrrrrrrrrrrrrrrrrrrrrrrrrrrr")
	elif junction.phaseMap[junction.green] == 1:
		traci.trafficlight.setRedYellowGreenState(junction._id, "rrrrrrrrrrrrrrrrrrrrrggggggg")
	elif junction.phaseMap[junction.green] == 2:
		traci.trafficlight.setRedYellowGreenState(junction._id, "gggggggrrrrrrrrrrrrrrrrrrrrr")
	elif junction.phaseMap[junction.green] == 3:
		traci.trafficlight.setRedYellowGreenState(junction._id, "rrrrrrrrrrrrrrgggggggrrrrrrr")
	elif junction.phaseMap[junction.green] == 4:
		traci.trafficlight.setRedYellowGreenState(junction._id, "rrrrrrrgggggggrrrrrrrrrrrrrr")
	else:
		traci.trafficlight.setRedYellowGreenState(junction._id, "rrrrrrrrrrrrrrrrrrrrrrrrrrrr")
	return
