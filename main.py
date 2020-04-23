import pygame
from buttons import Button
from node import node
import dijkstra
pygame.init()

#Set up the display
win_height = 700
win_width = 1000
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Eliminate')

#Create lists for the grid/graph, start node location, walls, and pins
nodes = []
for row in range(30):
    curr_row = []
    for col in range(50):
        curr_row.append(node(row, col))
    nodes.append(curr_row)
#Start node initialized at row 15 column 10
start = [15, 10]

#Walls and pins list used for redrawing existing pins and walls when needed. See draw_window()
walls = []
pins = []

#Calculates the row and column on the graph based on mouse location
def get_row_col(x, y):
    offset_x = x % 20
    adj_x = x - offset_x
    new_x = adj_x // 20

    offset_y = y % 20
    adj_y = y - offset_y
    new_y = adj_y // 20
    return new_y, new_x

#Simply redraws all the buttons
def draw_buttons():
    draw_btn.draw(win)
    erase_btn.draw(win)
    run_btn.draw(win)
    pin_btn.draw(win)
    clr_btn.draw(win)

#Redraws all of the current walls and pins
def draw_walls_pins():
    for j in range(len(walls)):
        pygame.draw.rect(win, (0, 0, 0), (1 + 20 * walls[j].col, 101 + (20 * walls[j].row), 18, 18))
    for k in range(len(pins)):
        win.blit(target_image, (pins[k].col * 20 + 1, pins[k].row * 20 + 101))

#Draws the entire window from scratch. Used to animate drag-and-drop mechanisms, and to clear the whole board
def draw_window():
    win.fill((255, 255, 255))
    for j in range(100, win_height + 20, 20):
        pygame.draw.line(win, (224, 224, 224), (0, j), (1000, j))
    for k in range(0, win_width + 20, 20):
        pygame.draw.line(win, (224, 224, 224), (k, 100), (k, 700))
    draw_buttons()
    draw_walls_pins()
    win.blit(arrow_images[curr_direction], (arrow_rect.x + 1, arrow_rect.y + 1))
    pygame.display.update()

#Create all of the buttons for user options
draw_rect = pygame.rect.Rect((100, 30, 100, 40))
draw_btn = Button(draw_rect, 'Draw Wall')

erase_rect = pygame.rect.Rect((250, 30, 100, 40))
erase_btn = Button(erase_rect, 'Erase Wall')

run_rect = pygame.rect.Rect((450, 30, 100, 40))
run_btn = Button(run_rect, 'Eliminate!')

pin_rect = pygame.rect.Rect((650, 30, 100, 40))
pin_btn = Button(pin_rect, 'Draw Pin')

clr_rect = pygame.rect.Rect((800, 30, 100, 40))
clr_btn = Button(clr_rect, 'Clear Pin')

#Designate the start node, create the start rectangle so the start node can be clicked, and
#draw the start node arrow image in the appropriate direction
nodes[start[0]][start[1]].isStart = True
arrow_rect = pygame.rect.Rect(nodes[start[0]][start[1]].col * 20, 100 + nodes[start[0]][start[1]].row * 20, 20, 20)
curr_direction = 2
arrow_images = [pygame.image.load('Images/Attacker_Left.png'), pygame.image.load('Images/Attacker_Up.png'), pygame.image.load('Images/Attacker_Right.png'), pygame.image.load('Images/Attacker_Down.png')]

target_image = pygame.image.load('Images/Target.png')

running = True          #Main game loop boolean
drawing = False         #Active when user is drawing walls
erasing = False         #Active when user is erasing walls
moveStart = False       #Active when user to dragging the start node
display_path = False    #Active when the shortest path is displayed to prevent updating
draw_window()
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Event handlers for hovering over the buttons and drawing/erasing walls
        elif event.type == pygame.MOUSEMOTION:
            #User doesn't click on the grid, used to highlight buttons on mouse hover
            if event.pos[1] < 100:
                if draw_rect.collidepoint(event.pos):
                    draw_btn.active = True

                elif erase_rect.collidepoint(event.pos):
                    erase_btn.active = True

                elif run_rect.collidepoint(event.pos):
                    run_btn.active = True

                elif pin_rect.collidepoint(event.pos):
                    pin_btn.active = True

                elif clr_rect.collidepoint(event.pos):
                    clr_btn.active = True

                else:
                    draw_btn.active = False
                    erase_btn.active = False
                    run_btn.active = False
                    pin_btn.active = False
                    clr_btn.active = False
                draw_buttons()
                pygame.display.update(pygame.Rect(0, 0, 1000, 100))

            else:
                #User is moving mouse with the left button down, with the draw wall option selected
                if drawing:
                    target_row, target_col = get_row_col(event.pos[0], event.pos[1] - 100)
                    #Ensure the desired wall is not a wall already
                    if not nodes[target_row][target_col].isWall:
                        nodes[target_row][target_col].isWall = True
                        walls.append(nodes[target_row][target_col])
                        #Draw the black rectangle representing a wall and update the grid
                        pygame.draw.rect(win, (0, 0, 0), (target_col * 20 + 1, target_row * 20 + 101, 18, 18))
                        pygame.display.update(pygame.Rect(0, 100, 1000, 600))

                #User is moving mouse with the left button down, with the erase wall option selected
                if erasing:
                    target_row, target_col = get_row_col(event.pos[0], event.pos[1] - 100)
                    #Ensure the desired node is a wall
                    if nodes[target_row][target_col].isWall:
                        nodes[target_row][target_col].isWall = False
                        walls.remove(nodes[target_row][target_col])
                        pygame.draw.rect(win, (255, 255, 255), (target_col * 20 + 1, target_row * 20 + 101, 18, 18))
                        pygame.display.update(pygame.Rect(0, 100, 1000, 600))

                #User has left mouse button down while on the start node and is moving the start node
                if moveStart:
                    pygame.draw.rect(win, (255, 255, 255), (arrow_rect.x + 1, arrow_rect.y + 1, 18, 18))
                    mx, my = event.pos
                    arrow_rect.x = mx + ox
                    arrow_rect.y = my + oy
                    draw_window()

        #Event handlers for clicking on the buttons
        elif event.type == pygame.MOUSEBUTTONUP:
            #Ensure the button moused up if the left mouse button
            if event.button == 1:
                #Make sure user clicked on the draw wall button
                if draw_rect.collidepoint(event.pos):
                    if not draw_btn.clicked:
                        #If a previous path is displayed, clear the board
                        if display_path:
                            draw_window()
                            display_path = False
                        #Show that draw wall button was clicked and make sure no others are clicked
                        draw_btn.clicked = True
                        erase_btn.clicked = False
                        pin_btn.clicked = False
                        clr_btn.clicked = False
                    #If the button was already clicked, unclick it/deselect the draw wall option
                    else:
                        draw_btn.clicked = False

                #Same idea for the other buttons
                elif erase_rect.collidepoint(event.pos):
                    if not erase_btn.clicked:
                        if display_path:
                            draw_window()
                            display_path = False
                        draw_btn.clicked = False
                        erase_btn.clicked = True
                        pin_btn.clicked = False
                        clr_btn.clicked = False
                    else:
                        erase_btn.clicked = False

                elif pin_rect.collidepoint(event.pos):
                    if not pin_btn.clicked:
                        if display_path:
                            draw_window()
                            display_path = False
                        draw_btn.clicked = False
                        erase_btn.clicked = False
                        pin_btn.clicked = True
                        clr_btn.clicked = False
                    else:
                        pin_btn.clicked = False

                elif clr_rect.collidepoint(event.pos):
                    if not clr_btn.clicked:
                        if display_path:
                            draw_window()
                            display_path = False
                        draw_btn.clicked = False
                        erase_btn.clicked = False
                        pin_btn.clicked = False
                        clr_btn.clicked = True
                    else:
                        clr_btn.clicked = False

                #When the eliminate button is clicked
                elif run_rect.collidepoint(event.pos):
                    #Clear the board if a previous path is displayed and clear all buttons
                    if display_path:
                        draw_window()
                        display_path = False
                    draw_btn.clicked = False
                    erase_btn.clicked = False
                    pin_btn.clicked = False
                    clr_btn.clicked = False
                    #Ensure that the user has placed at least one pin, else do nothing else
                    if len(pins) > 0:
                        #Calculate and draw out the shortest path to all pins. curr_direction used to keep the
                        #start arrow facing the right direction when moved around
                        curr_direction = dijkstra.eliminate(nodes, start, len(pins), win, arrow_images)
                        #Indicate that there is now a path being shown on screen
                        display_path = True
                        #Remove the last pin from list of pins, as it is now the new start
                        pins.remove(nodes[start[0]][start[1]])
                        arrow_rect.x = start[1] * 20
                        arrow_rect.y = start[0] * 20 + 100
                        #Since the pathfinding algorithm clears all pins of their pin status, all but the last pin
                        #must be "reinstated" as pins
                        for i in range(len(pins)):
                            nodes[pins[i].row][pins[i].col].isEnd = True

                #If the user mouses up while on the grid, they no longer are drawing or erasing walls    
                if event.pos[1] >= 100:
                    drawing = False
                    erasing = False
                
                #Same as above but they are no longer moving the start node
                if moveStart:
                    pygame.draw.rect(win, (255, 255, 255), (arrow_rect.x + 1, arrow_rect.y + 1, 18, 18))
                    arrow_rect.x = event.pos[0]
                    arrow_rect.y = event.pos[1]
                    node.adjust_start(arrow_rect, nodes, start, moveStart)
                    draw_window()
                    moveStart = False

        #Mouse downing will draw pins, clear pins, and start the process of drawing/erasing walls
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #User is drawing a pin
                if pin_btn.clicked:
                    #Make sure they are drawing it on the grid
                    if event.pos[1] >= 100:
                        #Get the node they clicked on
                        target_row, target_col = get_row_col(event.pos[0], event.pos[1] - 100)
                        curr_node = nodes[target_row][target_col]
                        #Make sure the node clicked on is not a wall, the start node, or a pin already
                        if not curr_node.isWall and not curr_node.isStart and not curr_node.isEnd:
                            #Set its status as a pin and draw the target image
                            nodes[target_row][target_col].isEnd = True
                            pins.append(nodes[target_row][target_col])
                            win.blit(target_image, (target_col * 20 + 1, target_row * 20 + 101))
                            pygame.display.update(pygame.Rect(0, 100, 1000, 600))

                #Same process as drawing a pin, but clearing its pin status and cleaing the image
                elif clr_btn.clicked:
                    if event.pos[1] >= 100:
                        target_row, target_col = get_row_col(event.pos[0], event.pos[1] - 100)
                        #Only needs to be done if the current node if a pin
                        if nodes[target_row][target_col].isEnd:
                            nodes[target_row][target_col].isEnd = False
                            pins.remove(nodes[target_row][target_col])
                            pygame.draw.rect(win, (255, 255, 255), (target_col * 20 + 1, target_row * 20 + 101, 18, 18))
                            pygame.display.update(pygame.Rect(0, 100, 1000, 600))

                elif draw_btn.clicked:
                    #The user has begun drawing walls
                    if event.pos[1] >= 100:
                        drawing = True
                        target_row, target_col = get_row_col(event.pos[0], event.pos[1] - 100)
                        curr_node = nodes[target_row][target_col]
                        #Make the current node a wall if it is not already one, not a pin, and not the start node
                        if not curr_node.isWall and not curr_node.isEnd and not curr_node.isStart:
                            nodes[target_row][target_col].isWall = True
                            walls.append(nodes[target_row][target_col])
                            pygame.draw.rect(win, (0, 0, 0), (target_col * 20 + 1, target_row * 20 + 101, 18, 18))
                            pygame.display.update(pygame.Rect(0, 100, 1000, 600))

                #Same as above but for erasing walls
                elif erase_btn.clicked:
                    if event.pos[1] >= 100:
                        erasing = True
                        target_row, target_col = get_row_col(event.pos[0], event.pos[1] - 100)
                        if nodes[target_row][target_col].isWall:
                            nodes[target_row][target_col].isWall = False
                            pygame.draw.rect(win, (255, 255, 255), (target_col * 20 + 1, target_row * 20 + 101, 18, 18))
                            pygame.display.update(pygame.Rect(0, 100, 1000, 600))

                #The user has mouse downed on the start node while none of the buttons are clicked
                elif arrow_rect.collidepoint(event.pos) and not draw_btn.clicked and not erase_btn.clicked:
                    if not run_btn.clicked and not pin_btn.clicked and not clr_btn.clicked:
                        moveStart = True
                        mx, my = event.pos
                        ox = arrow_rect.x - mx
                        oy = arrow_rect.y - my