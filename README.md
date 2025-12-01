# Genetic Algorithm for Travel Salesman Problem with Timw Windows
This is a project made for the **Mobility and Urban Logistics** course of the Industrial Engineering program at Technology University of Troyes (Université de Technologie de Troyes - UTT)

This project consists on :
- modeling the Travel Salesman Problem with Timw Windows (TSP-TW)
- applying a linear solver to find the optimal solution
- applying some well known TSP heuristics to the TSP-TW,
- Applying Genetic Algorithm
- Compare the results

Objective: Minimize the total time to visit all nodes

$$Obj = \min \sum_{i=1}^{n} (x_{ij} \cdot dist_{ij}) \;+\; \sum_{i=1}^{n} (\alpha_i \cdot r_i) $$
