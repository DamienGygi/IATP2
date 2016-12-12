import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys



def ga_solve(file=None, gui=True, maxTime=0):
    if gui is True:
        initPoints(file)


def initPoints(file):
    SCREEN_X = 500
    SCREEN_Y = 500
    CITY_COLOR = [10, 10, 200]
    CITY_RADIUS = 7
    FONT_COLOR = [255, 255, 255]
    cities = []
    collecting = True

    pygame.init()
    window = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('GygSchaffo Perfekt Algorithm')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)

    def draw(positions):
        screen.fill(0)
        for pos in positions:
            pygame.draw.circle(screen, CITY_COLOR, pos, CITY_RADIUS)
        text = font.render("Nombre: %i" % len(positions), True, FONT_COLOR)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()


    if file is not None:
        collecting=False
        cities=readFile(file)
        draw(cities)

    while collecting:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False
            elif event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                cities.append(pygame.mouse.get_pos())
                draw(cities)


    screen.fill(0)
    pygame.draw.lines(screen, CITY_COLOR, True, cities)
    text = font.render("Un chemin, pas le meilleur!", True, FONT_COLOR)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN: break

def readFile(file):
    cities =[]
    with open(file,"r") as f:
        for lines in f:
            data= lines.split()
            cities.append((int(data[1]),int(data[2])))
    f.close()
    return cities


if __name__ == '__main__':
    ga_solve("pb005.txt", True, 20)
