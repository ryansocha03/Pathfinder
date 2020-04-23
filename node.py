'''Class file for the graph nodes'''
import sys
import pygame
pygame.init()

class node(object):
    def __init__(self, row, col):
        self.row = row                  #Contains the row of the node in the grid
        self.col = col                  #Contains the column of the row in the grid
        self.isWall = False             #True when the node is a wall, false otherwise
        self.visited = False            #True if the node has been visited in the current iteration of dijkstra
        self.distance = sys.maxsize     #Distance from the start node
        self.isStart = False            #True when the node is the start node
        self.isEnd = False              #True when the node is a pin
        self.prev_node = None           #Contains this nodes predecessor

    #Draw new arrow image and color last node yellow. 0 is left, 1 is up, 2 is right, 3 is down in start_images
    def trace_node(self, win, start_images):
        pygame.draw.rect(win, (255, 255, 0), (20 * self.prev_node.col + 1, 20 * self.prev_node.row + 101, 18, 18))
        #Moved to the left
        curr_direction = 0
        if self.col < self.prev_node.col:
            pygame.draw.rect(win, (255, 255, 255), (20 * self.col + 1, 20 * self.row + 101, 18, 18))
        #Moved up
        elif self.row < self.prev_node.row:
            pygame.draw.rect(win, (255, 255, 255), (20 * self.col + 1, 20 * self.row + 101, 18, 18))
            curr_direction = 1
        #Moved to the right
        elif self.col > self.prev_node.col:
            pygame.draw.rect(win, (255, 255, 255), (20 * self.col + 1, 20 * self.row + 101, 18, 18))
            curr_direction = 2
        #Else moved down
        else:
            pygame.draw.rect(win, (255, 255, 255), (20 * self.col + 1, 20 * self.row + 101, 18, 18))
            curr_direction = 3
        win.blit(start_images[curr_direction], (20 * self.col + 1, 20 * self.row + 101))
        return curr_direction

    #This method performs the necessary updates when the start node is dragged and dropped
    @staticmethod
    def adjust_start(s_rect, nodes, start, moveStart):
        if moveStart:
            if s_rect.y < 100:
                s_rect.x = nodes[start[0]][start[1]].col * 20
                s_rect.y = 100 + (nodes[start[0]][start[1]].row * 20)
            else:
                offset_x = s_rect.x % 20
                offset_y = s_rect.y % 20

                prev_start_row = start[0]
                prev_start_col = start[1]

                nodes[start[0]][start[1]].isStart = False
                s_rect.x = s_rect.x - offset_x
                start[1] = (s_rect.x - offset_x) // 20 + 1
                s_rect.y = s_rect.y - offset_y
                start[0] = (s_rect.y - offset_y) // 20 - 4
                if nodes[start[0]][start[1]].isWall or nodes[start[0]][start[1]].isEnd:
                    start[0] = prev_start_row
                    start[1] = prev_start_col
                    s_rect.x = nodes[start[0]][start[1]].col * 20
                    s_rect.y = 100 + (nodes[start[0]][start[1]].row * 20)

                nodes[start[0]][start[1]].isStart = True
