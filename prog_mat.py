from pulp import *

# Função que define o valor custo do agente em determinada task
def taskValue(agent,task):
  return (agent+task)

n = 3
funcOptimization = LpMaximize

problem = LpProblem("O problema de designacao", funcOptimization)

agentsRange = range(n)
tasksRange = range(n)

# Cria as varíaveis binárias da execução dos agente em determinada tarefa
agentsExectution = LpVariable.dicts("aegnts",(agentsRange,tasksRange),0,1,LpInteger)

# Maximizar a experienca dado que um agente está habilitado a executar a tarefa
problem += lpSum([taskValue(agent,task) * agentsExectution[agent][task] for agent in agentsRange for task in tasksRange])

# Um agente apenas executa uma tarefa
for agent in agentsRange:
  problem += (lpSum([agentsExectution[agent][task] for task in tasksRange]) == 1, f"Agente_Limite_{agent}")

# Uma tarefa apenas pode ser executado por um agente
for task in tasksRange:
  problem += (lpSum([agentsExectution[agent][task] for agent in agentsRange]) == 1, f"Tarefa_Limite_{task}")

problem.solve()
total_sum = 0
for agent in agentsRange:
  for task in tasksRange:
    if agentsExectution[agent][task].value() == 1:
      print(f"Agente {agent} executou a tarefa {task}")
      total_sum += taskValue(agent,task)

print(f"A soma total foi {total_sum}")