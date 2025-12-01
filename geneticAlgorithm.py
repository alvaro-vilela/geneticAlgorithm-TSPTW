import random
import numpy as np
from random import randint
from copy import deepcopy
from utils import Calculate_cost
import matplotlib.pyplot as plt
from heuristics import route_Closest_Neighbour, route_Nearest_Insertion
import time

def Generate_random_route(n):
  route = list(range(1, n))
  random.shuffle(route)
  route.append(0)
  route = [0] + route
  return route

def Init_population(POP_SIZE, n, dist, a, b, pen, dmax):
  routes_NearestInsertion = 0
  routes_Closest_neighbour = 0
  routes_random = 0

  pop = []
  for i in range(POP_SIZE):
    prob = random.random()

    if prob < 0.15: # 15% of initial population is composed by the route generated with Nearest Insertion
      pop.append(route_Nearest_Insertion(n, dist, a, b, pen, dmax))
      routes_NearestInsertion+=1

    elif prob >= 0.15 and prob < 0.20: # 5% of initial population is composed by the route generated with Closest Neighbour
      pop.append(list(route_Closest_Neighbour(n, dist, a, b, dmax, pen, 0)[2]))
      routes_Closest_neighbour+=1

    elif prob >=  0.20: # 80% of initial population is composed by random routes
      individual = Generate_random_route(n)
      pop.append(individual)
      routes_random+=1

  print(f"Initial Population Proportion:\nNearest insertion: {round(routes_NearestInsertion/POP_SIZE, 2)}\nClosest Neighbour: {round(routes_Closest_neighbour/POP_SIZE, 2)}\nRandom routes: {round(routes_random/POP_SIZE, 2)}")
  print("-" * 60)
  return pop

def Fitness(pop, dist, a, b, pen):
  fitness = np.zeros(len(pop))
  for i in range(len(pop)):
    fitness[i] = Calculate_cost(dist, a, b, pen, pop[i])
  return fitness

def Selection(TOURNAMENT_SIZE, population, fitnesses): # select one individual using tournament selection
    tournament = [randint(0, len(population)-1) for i in range(TOURNAMENT_SIZE)]
    tournament_fitnesses = [fitnesses[tournament[i]] for i in range(TOURNAMENT_SIZE)]
    return deepcopy(population[tournament[tournament_fitnesses.index(min(tournament_fitnesses))]])

def Crossover(parent1, parent2):
  crossover_point = random.randint(1, len(parent1) - 2)

  child1 = parent1[:crossover_point]
  child2 = parent2[:crossover_point]

  def complete_child(child, parent):
      for node in parent:
          if node not in child:
              child.append(node)
      child.append(0)

  complete_child(child1, parent2)
  complete_child(child2, parent1)

  return child1, child2

def Mutate(route, PROB_MUTATION):
  if len(route) - 2 <= 1:
      return route  # No mutation possible if there's only one or no city

  if random.random() < PROB_MUTATION:
    node1, node2 = random.sample(range(1, len(route) - 1), 2)

    mutated_route = route[:]
    mutated_route[node1], mutated_route[node2] = mutated_route[node2], mutated_route[node1]
    return mutated_route

  else:
    return route
  
def Plot_fitness(GENERATIONS, solution_cumulated_best_cost):
  plt.plot(range(GENERATIONS), solution_cumulated_best_cost)
  plt.xlim(0, GENERATIONS)
  plt.xlabel("Generation")
  plt.ylabel("Best cost")
  plt.show()

def GA(POP_SIZE, GENERATIONS, TOURNAMENT_SIZE, PROB_MUTATION, n, dist, a, b, pen, dmax):
  start_time = time.time()
  pop = Init_population(POP_SIZE, n, dist, a, b, pen, dmax)
  generations = []
  generations.append(pop)

  generation_best_fitness = []
  cumulated_best_fitness = []

  fitnesses = np.zeros((GENERATIONS, POP_SIZE))
  fitnesses[0] = Fitness(pop, dist, a, b, pen)
  print()
  # print(f"Fitnessess: {fitnesses[0]}")

  best_fitness = min(fitnesses[0])
  generation_best_fitness.append(min(fitnesses[0]))
  cumulated_best_fitness.append(best_fitness)
  # print(f"Best fitness: {best_fitness}")
  best_individual = pop[np.where(fitnesses[0] == best_fitness)[0][0]]
  # print(f"Best individual index: {np.where(fitnesses[0] == best_fitness)[0][0]}")

  print(f"Generations: {GENERATIONS}\nPopulation size: {POP_SIZE}\nTournament size: {TOURNAMENT_SIZE}\nMutation probability: {PROB_MUTATION}")
  print("-"*60)
  print(f"Gen:    0 , Best of run: {round(min(fitnesses[0]), 2):<10} , Best so far: {round(best_fitness, 2)}")

  for gen in range(1, GENERATIONS):
    # print(f"GENERATION : {gen}")
    pop = []
    for i in range(POP_SIZE):
      parent1 = Selection(TOURNAMENT_SIZE, generations[gen-1], fitnesses[gen-1])
      parent2 = Selection(TOURNAMENT_SIZE, generations[gen-1], fitnesses[gen-1])
      child1, child2 = Crossover(parent1, parent2)
      child1 = Mutate(child1, PROB_MUTATION)
      child2 = Mutate(child2, PROB_MUTATION)

      competitors = [parent1, parent2, child1, child2]
      # competitors = [child1, child2]
      competitors_fitness = Fitness(competitors, dist, a, b, pen)
      best_fitness_competitors = min(competitors_fitness)
      best_competitor = competitors[np.where(competitors_fitness == best_fitness_competitors)[0][0]]

      pop.append(best_competitor)

    generations.append(pop)
    fitnesses[gen] = Fitness(pop, dist, a, b, pen)
    generation_best_fitness.append(min(fitnesses[gen]))
    # print(f"Fitnessess: {fitnesses[gen]}")

    if min(fitnesses[gen]) < best_fitness:
      # print(f"Atualizando a Fitness!")
      best_fitness = min(fitnesses[gen])
      # print(f"Best fitness: {best_fitness}")
      best_individual = pop[np.where(fitnesses[gen] == best_fitness)[0][0]]
      # print(f"Best individual index: {np.where(fitnesses[gen] == best_fitness)[0][0]}")
    cumulated_best_fitness.append(best_fitness)

    # print(f"Gen: {gen:4} , Best of run: {round(min(fitnesses[gen]), 2):<10} , Best so far: {round(best_fitness, 2)}")
    if gen%10 == 0:
      print(f"Gen: {gen:4} , Best of run: {round(min(fitnesses[gen]), 2):<10} , Best so far: {round(best_fitness, 2)}")


  print(f"Gen: {gen:4} , Best of run: {round(min(fitnesses[gen]), 2):<10} , Best so far: {round(best_fitness, 2)}")
  end_time = time.time()
  run_time = end_time - start_time
  print(f"Running time : {round(run_time, 3)} s")

  return best_fitness, best_individual, cumulated_best_fitness, generation_best_fitness, generations