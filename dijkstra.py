'''File for all things dijkstra. Please note that the feature for dealing with a pin that is
inaccesible from the start node (by surrounding either the start node or pin/pins with walls)
is not yet implemented so the function behavior is undefined. Please make sure that all pins
are accesible from the start node :). The path is found by using dijkstras algorithm iteratively
to first find the closest pin node, and then tracing the path to it. This is done repeatedly
until no pin nodes remain'''
import operator
import sys
import pygame
import time
pygame.init()

def eliminate(nodes, start, num_pins, win, start_images):
    #Loop until all nodes have been eliminated
    while num_pins > 0:
        #Get the visited nodes
        visited_nodes = dijkstra(nodes, start)
        #The old start node is no longer the start
        nodes[start[0]][start[1]].isStart = False
        #The current end node is now the new start node
        current_end = visited_nodes[len(visited_nodes) - 1]
        start[0] = current_end.row
        start[1] = current_end.col
        nodes[start[0]][start[1]].isEnd = False
        nodes[start[0]][start[1]].isStart = True
        #Trace out the path and get the direction the start arrow should face
        curr_direction = trace_path(visited_nodes, win, start_images)
        num_pins = num_pins - 1
    return curr_direction

#This function builds the path from the start to end node and traces it out on screen
def trace_path(visited_nodes, win, start_images):
    path = []
    curr_node = visited_nodes[len(visited_nodes) - 1]
    while not curr_node.prev_node is None:
        path.insert(0, curr_node)
        curr_node = curr_node.prev_node

    for i in range(len(path)):
        curr_direction = path[i].trace_node(win, start_images)
        time.sleep(0.05)
        pygame.display.update()
    return curr_direction

#This function performs dijkstra's using the current start node
def dijkstra(nodes, start):
    #First, all nodes must have their distance, visited, and prev_node attributes reset
    for row in range(30):
        for col in range(50):
            nodes[row][col].distance = sys.maxsize
            nodes[row][col].visited = False
            nodes[row][col].prev_node = None
    #The start nodes distance is set to zero
    nodes[start[0]][start[1]].distance = 0

    #The 2d list of nodes is compressed into a 1d list
    unvisited = compress_nodes(nodes)
    visited = []
    
    #We will loop until we have gone through all available nodes
    while len(unvisited) >= 0:
        #Unvisited nodes are sorted by distance, allowing us to remove the node with smallest distance
        unvisited.sort(key=operator.attrgetter('distance')) 
        curr_node = unvisited.pop(0)

        #If the node removed is a wall, we go to the next iteration
        if curr_node.isWall:
            continue
    
        #If the node with smallest distance has an 'infinite' distance, we have been trapped, and we should return
        if curr_node.distance == sys.maxsize:
            return visited
    
        #Say that we have visited the node and add it to the end of the list of visited nodes
        curr_node.visited = True
        visited.append(curr_node)

        #If the current node is a pin, we step execution and return the list of visited nodes
        if curr_node.isEnd:
            return visited

        #Update distance of the node above (if applicable)
        if curr_node.row > 0 and nodes[curr_node.row - 1][curr_node.col].visited == False:    
            nodes[curr_node.row - 1][curr_node.col].distance = curr_node.distance + 1
            nodes[curr_node.row - 1][curr_node.col].prev_node = curr_node
      
        #Update distance of the node to the left (if applicable)
        if curr_node.col > 0 and nodes[curr_node.row][curr_node.col - 1].visited == False:
            nodes[curr_node.row][curr_node.col - 1].distance = curr_node.distance + 1
            nodes[curr_node.row][curr_node.col - 1].prev_node = curr_node

        #Update distance of the node below (if applicable)
        if curr_node.row < len(nodes) - 1 and nodes[curr_node.row + 1][curr_node.col].visited == False:
            nodes[curr_node.row + 1][curr_node.col].distance = curr_node.distance + 1
            nodes[curr_node.row + 1][curr_node.col].prev_node = curr_node

        #Update distance of the node to the right (if applicable)
        if curr_node.col < len(nodes[0]) - 1 and nodes[curr_node.row][curr_node.col + 1].visited == False:
            nodes[curr_node.row][curr_node.col + 1].distance = curr_node.distance + 1
            nodes[curr_node.row][curr_node.col + 1].prev_node = curr_node


def compress_nodes(nodes):
    unvisited = []
    for row in range(30):
        for col in range(50):
            unvisited.append(nodes[row][col])
    return unvisited