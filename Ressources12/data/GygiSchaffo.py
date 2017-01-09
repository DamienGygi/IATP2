import random
import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys
import math

class City:
    def __init__(self,name,x,y):
        self.name=name
        self.x=x
        self.y=y

class Individu:
    def __init__(self, cities):
        self.travelPath=cities
        self.distance= self.totalDistance()

    def totalDistance(self):
        distance=0
        for i in range(0, len(self.travelPath)):
            city = self.travelPath[i]
            if (i == len(cities) - 1):
                city1 = self.travelPath[0]
            else:
                city1 = self.travelPath[i+1]
            distance+=math.sqrt((city1.x-city.x)**2+(city1.y-city.y)**2)
        return distance


cities = []
individues = []

def ga_solve(file=None, gui=True, maxTime=0):

    if gui is True:
        if file is not None:
            readFile(file)
        initPoints(file, cities)
    else:
        if file is None:
            print("ERROR: Enter a file name please.")
        else:
            print("")

def readFile(file):
    with open(file,"r") as f:
        for lines in f:
            city_pos= lines.split()
            newCity=City(city_pos[0],city_pos[1],city_pos[2])
            cities.append(newCity)
    f.close()

def initPoints(file, cities):

    SCREEN_X = 500
    SCREEN_Y = 500
    CITY_COLOR = [10, 10, 200]
    CITY_RADIUS = 7
    FONT_COLOR = [255, 255, 255]
    collecting = True

    pygame.init()
    window = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('GygSchaffo Perfekt Algorithm')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)

    def draw(cityList):
        screen.fill(0)
        for city in cityList:
            cityPos=(int(city.x),int(city.y))
            pygame.draw.circle(screen, CITY_COLOR, cityPos, CITY_RADIUS)
        text = font.render("Nombre: %i" % len(cityList), True, FONT_COLOR)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()

    if file is not None:
        collecting=False
        random.shuffle(cities)
        draw(cities)
    else:
        cities=[]

    while collecting:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False
            elif event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                cities.append(pygame.mouse.get_pos())
                #random.shuffle(cities)
                draw(cities)

    POPULATION_SIZE = 10
    for i in range(0, POPULATION_SIZE):
        newIndividus= Individu(random.sample(cities,len(cities)))
        individues.append(newIndividus)

    screen.fill(0)
    for i in range(0,len(cities)):
        cityPos = (int(cities[i].x), int(cities[i].y))
        if(i==len(cities)-1):
            cityPos1 = (int(cities[0].x), int(cities[0].y))
        else:
            cityPos1 = (int(cities[i+1].x), int(cities[i+1].y))
        cityLine=(cityPos,cityPos1)

        pygame.draw.lines(screen, CITY_COLOR, True,cityLine)

    text = font.render("Chemin trouvé: ", True, FONT_COLOR)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN: break


if __name__ == '__main__':
    ga_solve("pb005.txt", True, 20)


