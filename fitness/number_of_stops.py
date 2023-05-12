"""
Objective 2: Minimize number of stops
The number of stops is the sum of the stops at each intersection. The stops at each intersection can be calculated using the following formula:
stop_count = (q * l) / (s * v)
where:

q: traffic flow rate (vehicles per hour)
s: speed (feet per second)
v: free-flow speed (feet per second)
l: effective green time (seconds)

 here is the code to optimize Function 2 with PSO using the pyswarms library:
"""
import numpy as np
import pyswarms as ps

# Define the objective function
def objective_function(x):
    q, s, v = 100, 50, 60  # Traffic flow rate, speed, free-flow speed
    l = x[0]  # Effective green time
    stop_count = (q * l) / (s * v)
    return stop_count

# Set the bounds for the variables
bounds = (np.array([10]), np.array([90]))

# Set the options for the PSO algorithm
options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}

# Create an instance of the PSO optimizer
optimizer = ps.single.GlobalBestPSO(n_particles=50, dimensions=1, options=options, bounds=bounds)

# Perform the optimization
best_position, best_fitness = optimizer.optimize(objective_function, iters=10)

# Print the results
print("Best effective green time:", best_position)
print("Minimum number of stops:", best_fitness)

"""

In this code, we first define the objective function as objective_function, which takes a vector x of length 1
 and returns the number of stops at the intersection calculated using the given formula. We also set the values for q, s, and v.

Next, we set the bounds for the variable l using a tuple bounds. In this case, we set the lower bound to 10 and the upper bound to 90.

We then set the options for the PSO algorithm in a dictionary options. Here, we set the cognitive and social parameters 
c1 and c2 to 0.5 and 0.3, respectively, and the inertia weight w to 0.9.

We create an instance of the PSO optimizer using ps.single.GlobalBestPSO, which takes the number of particles,
 the dimensionality of the problem, the options, and the bounds as input arguments.

Finally, we call the optimize method of the optimizer with the objective function and the number of iterations 
as input arguments. The optimize method returns the best position and best
 fitness found by the optimizer, which we print to the console as the best effective green time and minimum number of stops, respectively.


In this code, we first define the objective function as objective_function,
 which takes a vector x of length 3 and returns the sum of the floor of each element in the vector.

Next, we define the bounds for the variables using a tuple bounds. In this case, 
we set the lower bound to 0 and the upper bound to 10 for each variable.

We then set the options for the PSO algorithm in a dictionary options.
 Here, we set the cognitive and social parameters c1 and c2 to 0.5 and 0.3,
 respectively, and the inertia weight w to 0.9.

We create an instance of the PSO optimizer using ps.single.GlobalBestPSO, which takes the number of particles, 
the dimensionality of the problem, the options, and the bounds as input arguments.

Finally, we call the optimize method of the optimizer with the objective function and the number of iterations as input arguments.
 The optimize method returns the best position and best fitness found by the optimizer, which we print to the console.

"""