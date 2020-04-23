# Pathfinder

This program is a pathfinding visualizer. 
It takes a grid of 30 rows and 50 columns to act as an undirected graph.
The user can then mark nodes as either pins or walls. The algorithm will then find the shortest path to all pins while avoiding the wall
nodes. 
Note that this is not a Hamiltonian path, as the algorithm does not need to visit each node in the graph once (again the graph is made of entire grid), it needs to find and visit each specially marked pin node once.
