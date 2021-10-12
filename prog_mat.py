from pulp import *
from sys import argv, stderr
import time
import random

# Getting CBC solver
cbcSolver = getSolver('PULP_CBC_CMD',msg=False)

# Getting GUROBI solver (you have to install and have a license)
# https://www.gurobi.com/documentation/7.0/quickstart_linux/software_installation_guid.html
# Download Gurobi on: https://www.gurobi.com/downloads/gurobi-software/
# download the readme, to follow instruction on how to install
# Get a license: https://www.gurobi.com/academia/academic-program-and-licenses/
# Use the license with 'grbgetkey'
# Run /opt/gurobi912/linux64/ sudo python3 setup.py install
# export GUROBI_HOME="/opt/gurobi912/linux64"
# export PATH="${PATH}:${GUROBI_HOME}/bin"
# export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${GUROBI_HOME}/lib"
gurobiSolver = getSolver('GUROBI')

# The number n of agents and tasks
n = 5

# Checking argument usage
if len(argv) < 2:
  if len(argv) == 0:
    argv.append('script_name')
  print('Usage: python3 ' + argv[0] + ' [solver]', file=stderr)
  exit(1)

# Setting the resolve solver
if argv[1] == 'cbc':
  resolveSolver = cbcSolver
  solverName = 'cbc'
elif argv[1] == 'gurobi':
  resolveSolver = gurobiSolver
  solverName= 'Gurobi'
else:
  print('Invalid solver. Available solvers: cbc, gurobi')
  exit(2)

agentsSatisfaction = []
for i in range(n):
  randomList = []
  for j in range(n):
    randomList.append(random.randint(0,10))
  agentsSatisfaction.append(randomList)

for i in range(n):
  print(f"\nExperiencias Agente {i}:")
  for j in range(n):
    print(f"Tarefa {j}: {agentsSatisfaction[i][j]}")

# Returns the satisfactionValue of an agent execunting a task
def satisfactionValue(agent,task):
  return agentsSatisfaction[agent][task]

# The optimization function (Maximize)
funcOptimization = LpMaximize

# Defines the problem to resolve
problem = LpProblem("O_problema_de_designacao", funcOptimization)

# Creates the array of agents and tasks numbers
# Example for n = 3:
# agentsRange = [0,1,2]
# tasksRange = [0,1,2]
agentsRange = range(n)
tasksRange = range(n)

# Creates the binary variables xij, that defines if an "i" agent execute a "j" task
# with:
# xij E {0,1} for i = 1,2,...,n; j = 1,2,...,n
# In the practice creates n*n = n^2 binary variables
agentsExectution = LpVariable.dicts("agents",(agentsRange,tasksRange),0,1,LpInteger)

# Defines the satisfaction function that will be using the function optimization 
# (in this case Maximization defined on line 11).
# So the funtion is:
# The summation of Xij*Cij, where
# Cij is the satisfaction value of "i" agent executing "j" task
problem += lpSum([satisfactionValue(agent,task) * agentsExectution[agent][task] for agent in agentsRange for task in tasksRange])

# Defines the restriction for agent
# One agent can execute just one task
# The summation of Xij for j=,1,2,...,n must be equal 1
for agent in agentsRange:
  problem += (lpSum([agentsExectution[agent][task] for task in tasksRange]) == 1, f"Agent_Limit_{agent}")

# Defines the restriction for task
# One task can be executed by just one agent
# The summation of Xij for i=,1,2,...,n must be equal 1
for task in tasksRange:
  problem += (lpSum([agentsExectution[agent][task] for agent in agentsRange]) == 1, f"Task_Limit_{task}")


print(f"\nSolver: {solverName}:\n")
start = time.time()

# Solve the problem using CBC
problem.solve(resolveSolver)

total_sum = 0

# Calculates the total sum
for agent in agentsRange:
  for task in tasksRange:
    if agentsExectution[agent][task].value() == 1:
      print(f"Agent: {agent} executed the task: {task}")
      total_sum += satisfactionValue(agent,task)

print(f"\nThe maximization returned a summation of: {total_sum}")
end = time.time()
print(f"Time Elapsed: {end-start}")
