import pygame
from copy import deepcopy
from random import randint


#board initialise
w, h = 10, 20
set_board = [[0 for x in range(w)]for y in range(h)]
move_board = deepcopy(set_board)

#screen initialise - things to do with the output
pygame.init()
fps = 60
cell = 25 #how big one cell is in pixels
game_res = w * cell, h * cell #screen size in pixels
game_sc = pygame.display.set_mode(game_res)#initializing the screen
clock = pygame.time.Clock()
grid = [pygame.Rect(x * cell, y * cell, cell, cell)for x in range(w) for y in range(h)]


#drawing helpers
fig_shape = pygame.Rect(0,0,cell-2,cell-2)


#figures shape - coordinates:
figure_pos = [[(-1,0), (-2,0), (0,0), (1,0)], #line
        [(0,-1), (-1,-1), (-1,0), (0,0)], #square
        [(0,-1), (-1,-1), (0,0), (1,0)], #squiggly  
        [(0,0), (-1,0), (0,1), (-1,-1)], #reversed squiggly 
        [(0,0), (0,-1), (0,1), (-1,-1)], #L
        [(0,0), (0,-1), (0,1), (1,-1)], #Reversed L
        [(0,0), (0,-1), (0,1), (-1,0)]] #T
figure = figure_pos[randint(0,6)]

fig_coor = [[x + w//2, y] for x, y in figure]
drop_lim = 50
level = 1
drop_counter = 0
score = 0
rotate = False
landing_time = 0
landed = False
drop = False

def check_collision(fig_coor): ### Return True if collide, False if no collision
    global w, set_board
    for i in range(4):
        if fig_coor[i][0] >= w or fig_coor[i][0] < 0 or fig_coor[i][1] >= h:
            return True
        elif set_board[fig_coor[i][1]][fig_coor[i][0]] == 1:
            return True
    return False

while True:
    dx = 0
    dy = 0
    #saving the position before moving
    old_fig = deepcopy(fig_coor)
    old_board = move_board
    move_board = deepcopy(set_board)
    game_sc.fill("black")
    

    #rotating
    if rotate:
        rotate = False
        center = fig_coor[0]
        for i in range(4):
            y = fig_coor[i][1] - center[1]
            x = fig_coor[i][0] - center[0]
            fig_coor[i][0] = center[0] - y
            fig_coor[i][1] = center[1] + x
            if check_collision(fig_coor):
                fig_coor = deepcopy(old_fig)
                break
        continue

    if drop:
        drop = False
        while check_collision(fig_coor) == False:
            for i in range(4):
                fig_coor[i][1] += 1
        for i in range(4):
                fig_coor[i][1] -= 1


    #natural fall mechanism
    drop_counter += level
    if drop_counter >= drop_lim:
        drop_counter = 0
        dy += 1

    #getting input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                dx += 1
            elif event.key == pygame.K_LEFT:
                dx -= 1
            elif event.key == pygame.K_DOWN:
                dy += 1
            elif event.key == pygame.K_UP:
                rotate = True
            elif event.key == pygame.K_SPACE:
                drop = True

    # implementing change
    #changing coordinates of the figure in play
    for i in range(4):
        fig_coor[i][0] += dx
        fig_coor[i][1] += dy
    if check_collision(fig_coor):
        fig_coor = old_fig
        continue

    #putting the figure on the board
    for i in range(4):
        move_board[fig_coor[i][1]][fig_coor[i][0]] = 1 if fig_coor[i][1] >= 0 else 0
    #displaying the board and its contents

    #legal collision detection - landing
    for i in range(4):
        if fig_coor[i][1] == h - 1:
            landed = True
        elif set_board[fig_coor[i][1] + 1][fig_coor[i][0]] == 1:
            landed = True
    if landed:
        landing_time += 1
        if landing_time == 25:
            set_board = deepcopy(move_board)
            figure = figure_pos[randint(0,6)]
            fig_coor = [[x + w//2, y] for x, y in figure]
            landing_time = 0
            landed = False

    #check line complete
    for i in range(h):
        filled = True
        for x in range(w):
            if set_board[i][x] == 0:
                filled = False
                break
        if filled:
            for x in range(w):
                set_board[i][x] = 0
            for y in range(i, 0,-1):
                set_board[y] = set_board[y-1]
            break
    
    #level system
    if (score // 1000) > level:
        level += 0.5

    [pygame.draw.rect(game_sc, (40,40,40), line_rect, 1)for line_rect in grid]#draws grid lines
    # game_sc is the screen, (40, 40, 40) is the color of the lines, line_rect is the shape and 1 is the thickness

    for y in range(h):
        for x in range(w):
            if move_board[y][x] == 1:
                fig_shape.x = x * cell
                fig_shape.y = y * cell
                pygame.draw.rect(game_sc,pygame.Color('white'), fig_shape)

    pygame.display.flip() #shows the display
    clock.tick(fps) #in game time counter of sorts
