import pygame

DISPLAY_WIDTH = 1400
DISPLAY_HEIGHT = 700
COLOR_INFECTED = (220,20,60)
COLOR_GROUND = (0,0,0)
BLACK = (0,0,0)
ELEMENT_HEIGHT = 15

pygame.init()

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('Infected')

clock = pygame.timelist_of_molecules.Clock()

def draw_humans(list_of_molecules):
    ls = list_of_molecules
    for index in range (0,len(ls)):
        draw_human(ls[index].status, ls[index].pos_x, ls[index].pos_y, ELEMENT_HEIGHT+1, ELEMENT_HEIGHT+1)

def draw_human(x,y,w,h):
    pygame.draw.rect(gameDisplay, COLOR_INFECTED, [x, y, w, h], 0)
    pygame.draw.rect(gameDisplay, BLACK, [x, y, w, h], 1)

def draw_grid():
    index = 0
    while index <= DISPLAY_WIDTH:
        pygame.draw.line(gameDisplay, BLACK, (index,0),(index,DISPLAY_HEIGHT))
        pygame.draw.line(gameDisplay, BLACK, (0,index),(DISPLAY_WIDTH,index))
        index += ELEMENT_HEIGHT

def graphics_main(list_of_molecules):
    end = False

    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end=True

        gameDisplay.fill(COLOR_GROUND)
        draw_grid()
        draw_humans(list_of_molecules)

        pygame.display.update()
        clock.tick(30)