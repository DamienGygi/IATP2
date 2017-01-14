import random
import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import operator
import sys
import math
from copy import deepcopy
import time

'''Global variable'''
SCREEN_X = 500
SCREEN_Y = 500
CITY_COLOR = [248, 255, 11]
CITY_RADIUS = 7
FONT_COLOR = [255, 255, 255]
POPULATION_SIZE = 100

''' Graphic part initialisation'''
pygame.init()
window = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
pygame.display.set_caption('GygSchaffo Perfekt Algorithm')
screen = pygame.display.get_surface()
font = pygame.font.Font(None, 20)

''' City list  and individu list initialisation'''
cities = []
individues = []


''' City class '''
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

''' Invididu class'''
class Individu:
    def __init__(self, cities):
        self.travelPath=cities
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
        return "Distance of found path: " + '%s' % (self.distance)

''' City import from file '''
def readFile(file):
    with open(file,"r") as f:
        for lines in f:
            city_pos= lines.split()
            newCity=City(city_pos[0],city_pos[1],city_pos[2])
            cities.append(newCity)
    f.close()

''' City initilisation with GUI'''
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


''' ga_solve function, this function returns the best found travel path and the distance using the individu class'''
def ga_solve(file=None, gui=True, maxTime=0):
    if gui is True:
        if file is not None:
            readFile(file)
        initPoints(file)

    '''Creation of a Population of individues, all are different (have a different travel path)'''
    citiesToVisit=cities[:]
    startCity= citiesToVisit.pop(0)
    for i in range(0, POPULATION_SIZE):
        newIndividu = Individu(random.sample(citiesToVisit,len(citiesToVisit)))
        newIndividu.travelPath.insert(0,startCity)
        newIndividu.totalDistance();
        individuExist(newIndividu)

    '''Sorting of the population to find the Elite individues'''
    individues.sort(key=lambda x: x.distance, reverse=False)
    numberOfIndividues=len(individues)

    startTime = time.time()

    '''Muting of the population to find a optimal solution'''
    while time.time()<startTime+maxTime:
        screen.fill(0)
        selection()
        mutation()
        individues.sort(key=lambda x: x.distance, reverse=False)
        while(len(individues)>numberOfIndividues):
            individues.pop()
        drawLine(individues[0].travelPath)

    '''Drawing of the best solution and wait on keypress'''
    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN: break

    '''Console print of the travel path and the distance '''
    print(individues[0].distance)
    print(individues[0].travelPath)

    '''return of the best found individu in max time'''
    return individues[0]

'''Personal selection: This function select a part of individu to mute them. We select the 2 first individues after the ordering of the list
    using the distance and then we select 40% of the rest population randomly'''
def selection():
    sampleSize=int(len(individues)*0.4)
    selectedIndividues=[]
    selectedIndividues.append(individues[0])
    selectedIndividues.append(individues[1])
    for i in range(0,sampleSize):
        selectedIndividues.append(individues[random.randint(sampleSize, len(individues)-1)])

    '''For each selected individu we transform him using the croisement function, swaping of the travel path list between 2 individues'''
    for i in range(0,sampleSize):
        croisement(selectedIndividues[i],selectedIndividues[len(selectedIndividues)-i-1],len(selectedIndividues[0].travelPath))
        croisement(selectedIndividues[len(selectedIndividues) - i - 1], selectedIndividues[i],len(selectedIndividues[0].travelPath))

'''Swaping of a specific part of the travel path between 2 individues. We use the start part of the travel path
    of individu 1 and add the rest of the path of individu 2
'''
def croisement(indiv1, indiv2, numberOfCity):
    swapSize= int(numberOfCity*0.2)
    newCityTravelpath=[]
    newCityStartCity=indiv1.travelPath[0]
    for i in range(0,swapSize):
        newCityTravelpath.append(indiv1.travelPath[i])

    for cityIndiv2 in indiv2.travelPath:
        if cityIndiv2 not in newCityTravelpath:
            newCityTravelpath.append(cityIndiv2)
    newCityTravelpath.pop(0)
    newIndividu = Individu(newCityTravelpath)
    newIndividu.travelPath.insert(0, newCityStartCity)
    newIndividu.totalDistance();
    individuExist(newIndividu)

'''The mutation function modifying, swaping the order of the travel path and create a new individu if the distance is lower '''
def mutation():
    if (random.random() < 0.1):
        index = random.randint(0,len(individues)-1)
        indiv =deepcopy(individues[index])
        listOrder = []
        listOrder.extend(indiv.travelPath)
        for l in range(0,10):
            res = lambda i: (i[l], i[l+1])
            res(listOrder)
            indiv.travelPath = listOrder
            indiv.totalDistance();
            if( indiv.distance < individues[index].distance):
                individues.pop(index)
                individuExist(indiv)

'''This function verify if the new individu already exist'''
def individuExist(indiv):
    pathExist = False
    for individu in individues:
        if (individu.travelPath == indiv.travelPath):
            pathExist = True
    if (pathExist is not True):
        individues.append(indiv)

'''This draws all the city points using the city list'''
def draw(cityList):
    screen.fill(0)
    for city in cityList:
        cityPos = (int(city.x), int(city.y))
        pygame.draw.circle(screen, CITY_COLOR, cityPos, CITY_RADIUS)
    text = font.render("Nombre: %i" % len(cityList), True, FONT_COLOR)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()

'''This function draws each line of the travel path, it use the individu list'''
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

'''Main point of the app '''

if __name__ == '__main__':
    ga_solve("pb050.txt", True, 60)



