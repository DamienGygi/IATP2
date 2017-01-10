import random
import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import operator
import sys
import math

class City:
    def __init__(self,name,x,y):
        self.name=name
        self.x=x
        self.y=y

    def __str__(self):
        return '%s' % (self.name)

    def __repr__(self):
        return self.name

    def __hash__(self):
        return str(self).__hash__()

class Individu:
    def __init__(self, cities,startCity):
        self.travelPath=cities
        self.startPathCity=startCity
        self.strTravelPath = "[" + '%s' % (self.startPathCity)
        self.distance= self.totalDistance()

    def totalDistance(self):
        distance=int(math.sqrt((int(self.travelPath[0].x)-int(self.startPathCity.x))**2+(int(self.travelPath[0].y)-int(self.startPathCity.y))**2))
        for i in range(0, len(self.travelPath)):
            city = self.travelPath[i]
            if (i == len(cities) - 1):
                city1 = self.travelPath[0]
            else:
                city1 = self.travelPath[i+1]
            distance+=int(math.sqrt((int(city1.x)-int(city.x))**2+(int(city1.y)-int(city.y))**2))
        return distance

    def __str__(self):
        for i in range(len(self.travelPath)):
            self.strTravelPath+=", "+'%s'%(self.travelPath[i])
        self.strTravelPath+="]"
        return "The total distance calculated using travel path is: " + '%s' % (self.distance) + " " +self.strTravelPath

cities = []
individues = []

def ga_solve(file=None, gui=True, maxTime=0):

    if gui is True:
        if file is not None:
            readFile(file)
        initPoints(file, cities)
    # else:
    #     if file is None:
    #         print("ERROR: Enter a file name please.")
    #     else:
    #         print("")


    POPULATION_SIZE = 10
    citiesToVisit=cities
    startCity= citiesToVisit.pop(0)
    for i in range(0, POPULATION_SIZE):
        newIndividus = Individu(random.sample(citiesToVisit,len(cities)),startCity)
        individues.append(newIndividus)

    for i in range(0, len(individues)):
        print(individues[i])



def readFile(file):
    with open(file,"r") as f:
        for lines in f:
            city_pos= lines.split()
            newCity=City(city_pos[0],city_pos[1],city_pos[2])
            cities.append(newCity)
    f.close()

def croisement(indiv1, indiv2):
    newParcours = []
    for i in range(0, 4):
        newParcours.append(indiv1.travelPath[i])

    for cityIndiv2 in indiv2.orderVisit:
        if cityIndiv2 not in newParcours:
            newParcours.append(cityIndiv2)

    return Individu(newParcours)

def mutation(individu):
    v1 = len(individu.orderVisit) - 2
    v2 = v1 + 1;
    tmp = individu.travelPath[v2]
    individu.orderVisit[v2] = individu.travelPath[v1]
    individu.orderVisit[v1] = tmp
    return individu

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
                draw(cities)


    screen.fill(0)
    for i in range(0,len(cities)):
        cityPos = (int(cities[i].x), int(cities[i].y))
        if(i==len(cities)-1):
            cityPos1 = (int(cities[0].x), int(cities[0].y))
        else:
            cityPos1 = (int(cities[i+1].x), int(cities[i+1].y))
        cityLine=(cityPos,cityPos1)

        pygame.draw.lines(screen, CITY_COLOR, True,cityLine)

    text = font.render("A good travelling path was found: ", True, FONT_COLOR)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN: break


if __name__ == '__main__':
    ga_solve("pb005.txt", True, 20)


