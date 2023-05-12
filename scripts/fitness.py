import traci
import sys

# Total delay
def calculate_delay(lane_id, vehicle_id):
    # Retrieve necessary data from SUMO and TraCI
    v = traci.lane.getMaxSpeed(lane_id)  # Free-flow speed of the lane
    u = traci.vehicle.getSpeed(vehicle_id)  # Actual speed of the vehicle
    t = traci.vehicle.getAccumulatedWaitingTime(vehicle_id)  # Time spent by the vehicle on the lane
    n = 4 # Random between 3 and 5

    # Check for division by zero
    if v == u:
        return sys.maxsize #float('inf')  # Return a maximum delay value or any appropriate default value

    # Calculate delay using the HCM equation with the retrieved parameters
    delay = (1 / (v - u)) * (1 - (1 / (1 + ((u * t) / (v - u)) ** n)))
    return delay

