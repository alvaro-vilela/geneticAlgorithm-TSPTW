import random
import numpy as np
from utils import Calculate_cost


# Closest Neighbour

def closest_neighbour(n, dist, dmax, v, visited)    : #retourne le plus proche sommet non visité à 'v'
    delta=dmax
    iref=-1
    for i in range(n):
        if dist[v][i]<delta and not (visited[i]):
           iref=i
           delta=dist[v][iref]
    return iref

def route_Closest_Neighbour(n, dist, a, b, dmax, pen, root):
    distance=0
    cost=0
    tour=np.zeros(n+1,dtype=int)
    visited = np.zeros(n, dtype=bool)

    tour[0] = root
    visited[root]=True
    t_a = 0
    t_d = 0

    for i in range (1, n):
      tour[i] = closest_neighbour(n, dist, dmax, root, visited)
      distance += dist[root][tour[i]]
      cost += dist[root][tour[i]]
      t_a = t_d + dist[root][tour[i]]
      # print(f"dist {tour[i-1]} -> {tour[i]} : {round(dist[root][tour[i]], 2)}")
      # print(f"t_a = {round(t_a, 2)}")

      if t_a < a[tour[i]]:
        t_d = a[tour[i]]
        # print(f"w = {round(t_d - t_a, 2)}")
      elif t_a > b[tour[i]]:
        t_d = t_a
        cost += pen[tour[i]] * (t_d - b[tour[i]])
        # print(f"r = {round(t_d - b[tour[i]], 2)}, cout pen = {round(pen[tour[i]] * (t_d - b[tour[i]]), 2)}")
      else:
        t_d = t_a

      # print(f"t_d = {round(t_d, 2)}\n-----------------")
      root = tour[i]
      visited[root]=True

    tour[n] = tour[0]
    distance += dist[root][tour[0]]
    cost += dist[root][tour[0]]

    # print(f"Cout de la tournée avec PPV: {cost}")
    # print(f"Tournée avec PPV : {tour}")
    return distance,cost,tour

"""### Clarke & Wright"""

def route_Clarke_Wright(n, dist, root=0):
  tours = {i: [i] for i in range(n) if i != root}
  distance = sum(dist[root][i] * 2 for i in range(n) if i != root)

  visited = set()
  excluded_nodes = set()

  savings = []
  for i in range(n):
      for j in range(i + 1, n):
          if i != root and j != root:
              saving = dist[root][i] + dist[root][j] - dist[i][j]
              savings.append((saving, i, j))

  savings.sort(reverse=True, key=lambda x: x[0])

  for saving, i, j in savings:
      if i in visited or j in visited:
          continue

      tour_i = next((key for key, tour in tours.items() if i in tour), None)
      tour_j = next((key for key, tour in tours.items() if j in tour), None)

      if tour_i is not None and tour_j is not None and tour_i != tour_j:
          new_tour = tours[tour_i] + tours[tour_j]

          tours[tour_i] = new_tour
          del tours[tour_j]
          visited.update(new_tour)
          distance -= saving

  final_tour = [root]
  for tour in tours.values():
      final_tour.extend(tour)
  final_tour.append(root)
  distance += dist[final_tour[-2]][root]

  remaining_clients = set(range(n)) - visited - excluded_nodes - {root}
  for cliente in remaining_clients:
      excluded_nodes.add(cliente)

  return distance, final_tour

"""### Meilleur insertion"""

def route_Nearest_Insertion(n, dist, a, b, pen, dmax):
    route = []
    visited = np.zeros(n+1, dtype = bool)
    route.append(0)
    route.append(0)
    visited[0] = visited[n] = True
    valeurs = dist[:][0]
    root = np.where((valeurs == min(i for i in valeurs if i>0)))[0]
    visited[root[0]] = True
    route.insert(1,root[0])

    for i in range(1,n-1):
        non_visited = np.where(~visited)
        i_ = random.choice(non_visited[0])
        delta = dmax + n*b[0]
        for j in range(1,len(np.where(visited)[0])):
            pseudo_route = route.copy()
            pseudo_route.insert(j,i_)
            gain = Calculate_cost(dist, a, b, pen, pseudo_route)
            if gain < delta:
                delta = gain
                jref = j
        route.insert(jref,i_)
        visited[i_] = True
    return route

"""### 2-Opt optimization"""

def reverseArray(arr,start, end):
  while start < end:
    arr[start], arr[end] = arr[end], arr[start]
    start += 1
    end -= 1
  return arr

def two_opt(route):
  Best = True
  while (Best == True):
    Best = False
    for i in range(len(route)-1):
      for j in range(len(route)-1):
        if j != i and j != i+1 and j != i-1:
          temp_route = route.copy()
          reverseArray(temp_route,i+1,j)
          if Calculate_cost(temp_route) < Calculate_cost(route):
            route = temp_route.copy()
            Best = False
    return route