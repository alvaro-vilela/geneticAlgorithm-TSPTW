
from pyscipopt import Model, quicksum,Expr
import numpy as np

def LinMod(n, pen, dist, dmax, a, b):
  model = Model("TSP_STW")

  # variables
  x = {}
  t = {}
  r = {}

  for i in range(n):
      t[i]=model.addVar(lb=0,name="t_%s"%i)
      r[i]=model.addVar(lb=0,name="r_%s"%i)
      for j in range(n):
          x[i,j]=model.addVar(vtype="B",name="x_%s_%s"%(i,j))

  myobj = Expr()
  for i in range(n):
    myobj += pen[i] * r[i]
    for j in range(n):
      myobj += x[i,j] * dist[i,j]

  model.setObjective(myobj,"minimize")

  # model.setObjective(quicksum(x[i,j] * dist[i,j] for i in range(n) for j in range(n)) + quicksum(pen[i] * r[i] for i in range(n)), "minimize")

  for i in range(n):
      model.addCons(x[i,i]==0)

  #Chaque sommet doit être visité une seule fois
  for j in range(n):
    model.addCons(quicksum(x[i,j] for i in range(n)) == 1)

  #Nb arcs entrants doit être égal au nb arcs sortants
  for j in range(n):
    model.addCons(quicksum(x[i,j] for i in range(n)) - quicksum(x[j,i] for i in range(n)) == 0)

  #Contraintes d'élimination des sous-tours
  for j in range(1, n):
    for i in range(n):
      if i != j:
        model.addCons(t[j] >= t[i] + dist[i, j] - 10*dmax * (1 - x[i, j]))

  for i in range(n):
    model.addCons(r[i] >= t[i] - b[i])

  for i in range(n):
    model.addCons(t[i] >= a[i])

  model.hideOutput()
  model.setParam("limits/time", 300)

  model.optimize()

  sol = model.getBestSol()
  succ = np.zeros(n, dtype=int)

  print("Solving time", model.getSolvingTime() )
  # print("sol", sol)
  print("Variables :")
  for i in range(n):
      # print(f"r[{i}] = {model.getSolVal(sol,r[i])}")
      # print(f"t[{i}] = {model.getSolVal(sol,t[i])}")
      for j in range(n):
          if model.getSolVal(sol,x[i,j])>0.99:
              succ[i]=j
              # print(i,"->",j)
  print(f'Cost of the route found with linear solver (time limit of 5 min): {model.getSolObjVal(sol):.2f}')

  route = np.zeros(n+1, dtype=int)
  current_node = succ[0]
  for i in range(1, n+1):
      route[i] = current_node
      current_node = succ[current_node]

  print("Optimal route : ", route)

  return model.getSolObjVal(sol), succ, route, model.getSolvingTime()