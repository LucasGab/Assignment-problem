agentsSatisfaction = []

n = 50

file = open('1.txt')

for line in file:
    line = line.split()
    numbers_float = [int(x) for x in line]
    agentsSatisfaction.append(numbers_float)
    

for i in range(n):
  print(f"\nExperiencias Agente {i}:")
  sum = 0
  for j in range(n):
    sum +=  agentsSatisfaction[i][j]
  print(sum)