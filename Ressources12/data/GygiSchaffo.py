import random
import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import operator
import sys
import math
from copy import deepcopy
import time

SCREEN_X = 500
SCREEN_Y = 500
CITY_COLOR = [10, 10, 200]
CITY_RADIUS = 7
FONT_COLOR = [255, 255, 255]

pygame.init()
window = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
pygame.display.set_caption('GygSchaffo Perfekt Algorithm')
screen = pygame.display.get_surface()
font = pygame.font.Font(None, 30)

cities = []
individues = []
POPULATION_SIZE = 100

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
        self.startCity=startCity
        self.distance= 0

    def totalDistance(self):
        for i in range(0, len(self.travelPath)):
            city = self.travelPath[i]
            if (i == len(cities) - 1):
                city1 = self.travelPath[0]
            else:
                city1 = self.travelPath[i + 1]
            self.distance += int(math.sqrt((int(city1.x) - int(city.x)) ** 2 + (int(city1.y) - int(city.y)) ** 2))
            
    def __str__(self):
        return "The total distance calculated using travel path is: " + '%s' % (self.distance) + " " + '%s' % (self.travelPath)

def ga_solve(file=None, gui=True, maxTime=0):

    if gui is True:
        if file is not None:
            readFile(file)
        initPoints(file)

    citiesToVisit=deepcopy(cities)
    startCity= citiesToVisit.pop(0)
    for i in range(0, POPULATION_SIZE):
        newIndividu = Individu(random.sample(citiesToVisit,len(citiesToVisit)),startCity)
        newIndividu.travelPath.insert(0,startCity)
        newIndividu.totalDistance();
        individuExist(newIndividu)

    individues.sort(key=lambda x: x.distance, reverse=False)
    numberOfIndividues=len(individues)

    startTime = time.time()

    while time.time()<startTime+maxTime:
        screen.fill(0)
        selection()
        mutation()
        individues.sort(key=lambda x: x.distance, reverse=False)
        while(len(individues)>numberOfIndividues):
            individues.pop()
        drawLine(individues[0].travelPath)

def selection():
    sampleSize=int(len(individues)*0.2)
    selectedIndividues=[]
    for i in range(0,sampleSize):
        selectedIndividues.append(individues[i])
        selectedIndividues.append(individues[random.randint(sampleSize, len(individues)-1)])

    for i in range(0,sampleSize):
        croisement(selectedIndividues[i],selectedIndividues[len(selectedIndividues)-i-1],len(selectedIndividues[0].travelPath))

def readFile(file):
    with open(file,"r") as f:
        for lines in f:
            city_pos= lines.split()
            newCity=City(city_pos[0],city_pos[1],city_pos[2])
            cities.append(newCity)
    f.close()

def initPoints(file):
    collecting = True
    if file is not None:
        collecting = False
        draw(cities)
    else:
        cities.clear()

    while collecting:
        for event in pygame.event.get():
            if event.type == QUIT:
                a=10
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False
            elif event.type == MOUSEBUTTONDOWN:
                newCity = City("v"+str(len(cities)), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                cities.append(newCity)
                draw(cities)
    screen.fill(0)
    drawLine(cities)


    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN: break

def croisement(indiv1, indiv2, numberOfCity):
    swapSize= int(numberOfCity*0.3)
    newCityTravelpath=[]
    newCityStartCity=indiv1.travelPath[0]

    for i in range(0,swapSize):
        newCityTravelpath.append(indiv1.travelPath[i])

    for cityIndiv2 in indiv2.travelPath:
        if cityIndiv2 not in newCityTravelpath:
            newCityTravelpath.append(cityIndiv2)
    newCityTravelpath.pop(0)
    newIndividu = Individu(newCityTravelpath, newCityStartCity)
    newIndividu.travelPath.insert(0, newCityStartCity)
    newIndividu.totalDistance();
    individuExist(newIndividu)

def mutation():
    for i in range(0,4):
        if (random.random() < 0.1):
            index = random.randint(0, len(individues) - 1)
            indiv = individues[index]
            listOrder = []
            listOrder.extend(indiv.travelPath)
            first = listOrder.pop(2)
            last = listOrder.pop(3)
            listOrder.insert(2, last)
            listOrder.insert(3, first)
            indiv.travelPath = listOrder

def draw(cityList):
    screen.fill(0)
    for city in cityList:
        cityPos = (int(city.x), int(city.y))
        pygame.draw.circle(screen, CITY_COLOR, cityPos, CITY_RADIUS)
    text = font.render("Nombre: %i" % len(cityList), True, FONT_COLOR)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()

def drawLine(cityList):
    text = font.render("Searching a good traveling path: ", True, FONT_COLOR)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()
    for i in range(0, len(cities)):
        cityPos = (int(cityList[i].x), int(cityList[i].y))
        if (i == len(cityList) - 1):
            cityPos1 = (int(cityList[0].x), int(cityList[0].y))
        else:
            cityPos1 = (int(cityList[i + 1].x), int(cityList[i + 1].y))
        cityLine = (cityPos, cityPos1)
        pygame.draw.lines(screen, CITY_COLOR, True, cityLine)
        pygame.display.flip()

def individuExist(indiv):
    pathExist = False
    for individu in individues:
        if (individu.travelPath == indiv.travelPath):
            pathExist = True
    if (pathExist is not True):
        individues.append(indiv)


if __name__ == '__main__':
    ga_solve("pb020.txt", True, 60)



