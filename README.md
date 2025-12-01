# Genetic Algorithm for Travel Salesman Problem with Time Windows
This is a project made for the **Mobility and Urban Logistics** course of the Industrial Engineering program at Technology University of Troyes (Université de Technologie de Troyes - UTT)

This project consists on :
- modeling the Travel Salesman Problem with Time Windows (TSP-TW)
- applying a linear solver to find the optimal solution
- applying some well known TSP heuristics to the TSP-TW,
- Applying Genetic Algorithm
- Compare the results
  
In the present work, we study a relaxed version of the TSP with time windows. This means that arriving outside the time window is allowed. If the vehicle arrives early, it must wait until the window opens. However, if it arrives late, a penalty is applied for the delay. The objective is to determine the optimal route that minimizes both travel costs and lateness penalties.

# Mathematical formulation for the TSP with relaxed Time Windows

## Parameters

- $N$ : Number of vertices  
- $\alpha_i$ : Penalty coefficient associated with lateness at the point $i$ 
- $a_i$ : Lower bound of the time window at the point $i$
- $b_i$ : Upper bound of the time window at the point $i$ 
- $dist_{ij}$ : Distance between the points $i$ and $j$

## Decision variables

- $x_{ij}$ : Equals 1 if the vehicle travels from vertex $i$ to vertex $j$ in the route; 0 otherwise
- $t{i}$ : Departure time at client $i$ 
- $r{i}$ : Delay associated with client $i$

## Objective function

The objective function of the project aims to minimize the total cost, which consists of two elements:
- the cost related to the distance traveled by the vehicle
- the cost associated with penalties, if these are applied

$$Obj = \min \sum_{i=1}^{n} (x_{ij} \cdot dist_{ij}) \;+\; \sum_{i=1}^{n} (\alpha_i \cdot r_i) $$

## Constraints

**Constraint 1** states that all clients must be visited exactly once:

$$\sum_{i=1}^{n} x_{ij} = 1 \quad \forall j \in 1..N$$

**Constraint 2** states that if the truck visits a client, it must also leave it:

$$\sum_{i=1}^{n} x_{ij} - \sum_{i=1}^{n} x_{ji} = 0 \quad \forall j \in 1..N$$

**Constraint 3** requires that if a vehicle visits client $j$ immediately after client $i$, then the departure time at client $j$ must be greater than the departure time at client $i$ plus the travel duration of arc $(i, j)$. This constraint is essential to eliminate subtours and guarantee a coherent route. Additionally, $t_j$ must be strictly greater than 0.

$$t_j \ge t_i + d_{ij} - M(1 - x_{ij}) \quad \forall i \in 1..N, \forall j \in 1..N, i \ne j$$

To compute the delay time for each client $i$, we can use $\max(0, t_i - b_i)$ To keep the model linear, we use **Constraints 4 and 5**:

$$r_i \ge t_i - b_i \quad \forall i \in 1..N$$

$$r_i \ge 0 \quad \forall i \in 1..N$$

In our problem, it is possible to arrive at a client before the start of their time window. In this case, it is necessary to wait until the start time before departing for the next client. **Constraint 6** prevents departing from a client before the moment they are available to be served.

$$t_i \ge a_i \quad \forall i \in 1..N$$

Finally, we present the **Constraints 7 and 8**, which indicate, respectively, that $x$ is a Boolean variable and that $t$ is a non-negative variable.

$$x_{ij} = \{0, 1\} \quad \forall i \in 1..N, \forall j \in 1..N$$

$$t_i \ge 0 \quad \forall i \in 1..N$$

## Instance Parameters:

The instances for this study consist on excel files containing the x and y coordinates for each vertice, their time window's lower and upper bounds and their latenesse penalty.
 
 - The warehouse is indexed by 0, i.e. Row 0 represents the warehouse, not a client. 

##### Example:
vertice | coord_x | coord_y | a | b | lateness penalty |
--- | --- | --- | --- |--- |--- |
0 | 35 | 35 | 0 | 10000 | 0 | 
1 | 41 | 49 | 161 | 171 | 1 | 
2 | 35 | 17 | 50 | 60 | 1 | 
3 | 55 | 45 | 116 | 126 | 1 | 
4 | 40 | 20 | 149 | 159 | 1 | 
5 | 15 | 30 | 34 | 44 | 1 |