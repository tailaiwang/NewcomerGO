#Hack the Barriers 18
#Elham Islam, Eric Wei, Jim Wu, Samuel Sun, Tailai Wang 
from pygame import*
from pygame.locals import*
from math import*
from math import radians, cos, sin, asin, sqrt
from random import*
import tkinter as tk
from tkinter import filedialog
import pygame
import urllib.request
import json
import re



pygame.init()
pygame.mixer.init()
pygame.mixer.pre_init(22050,-16,2,2048) #sound 

#SCREEN STUFF AND CONSTANTS
#####################################################################
radius = 6371
screenWidth = 640
screenHeight = 640
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
GREY = (111,111,111)
TEAL = (0, 128, 128)
screen = display.set_mode((screenWidth,screenHeight))#screen size (16:9 iOS ratios)
#####################################################################
#FONTS
font.init()
ralewayBold60 = font.Font("raleway/Raleway-Bold.ttf",60)
ralewayRegular48 = font.Font("raleway/Raleway-Regular.ttf", 48)
ralewayMedium36 = font.Font("raleway/Raleway-Medium.ttf", 36)
ralewayRegular24 = font.Font("raleway/Raleway-Regular.ttf", 24)
ralewayRegular12 = font.Font("raleway/Raleway-Regular.ttf", 12)
####################################################################
logo = image.load("2000px-Pokémon_GO_logo.png")
logo = transform.scale(logo, (640, 384))
startRect = Rect(screenWidth/2 - 160, 450, 320, 80)
startText = ralewayRegular48.render("Start", True, BLACK)
####################################################################
maps = image.load("map.png")
maps = transform.scale(maps, (640, 291))
ad = image.load("ad.png")
ad = transform.scale(ad, (630, 78))
####################################################################
scrollRect = Rect(0,640 - 80, screenWidth/3, 80)
mapRect = Rect(screenWidth/3, 640 - 80, screenWidth/3, 80)
profileRect = Rect(screenWidth - screenWidth/3, 640 - 80, screenWidth/3, 80)
scrollText = ralewayMedium36.render("List", True, BLACK)
mapText = ralewayMedium36.render("Map", True, BLACK)
profileText = ralewayMedium36.render("Profile", True, BLACK)
titleText = ralewayMedium36.render("Landmark", True, BLACK)
titleText2 = ralewayMedium36.render("KM", True, BLACK)
####################################################################
profileHeadlines = open("profile.txt")
profileData = profileHeadlines.readlines()
profileHeadlines.close()
profilePic = transform.scale(image.load("lye.png"),(150,150))
mostText = ralewayRegular24.render("Your Watchlist", True, BLACK)

####################################################################
def screenFill(c):
    draw.rect(screen, (c), (0, 0, screenWidth, screenHeight))
    
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
lat1 = 53.32055555555556
lat2 = 53.31861111111111
lon1 = -1.7297222222222221
lon2 = -1.6997222222222223
print(haversine(lon1,lat1,lon2,lat2))

def drawMenu():
    screen.blit(logo, (0,0))
    draw.rect(screen, BLACK, startRect, 2)
    screen.blit(startText, (screenWidth/2 - startText.get_width()/2, 460))
    
def drawScroll():
    count = 0
    screen.blit(titleText, (5, 20))
    screen.blit(titleText2, (585,20))
    for i in range(12):
        tempText = ralewayRegular24.render(spotData[count*2], True, BLACK)
        tempText2 = ralewayRegular24.render(str(round(distances[i],2)), True, GREY)
        screen.blit(tempText, (5,80 + count*40))
        screen.blit(tempText2, (590,80 + count*40))
        count += 1
    
def drawMap():
    screen.blit(maps, (0,150))
    screen.blit(ad, (0,50))
    screen.blit(userText, (screenWidth/2 - userText.get_width()/2, 460))
    screen.blit(userText2, (screenWidth/2 - userText2.get_width()/2, 500))

def drawBars():
    draw.rect(screen, BLACK, scrollRect, 2)
    draw.rect(screen,BLACK, mapRect, 2)
    draw.rect(screen, BLACK, profileRect, 2)
    screen.blit(scrollText, (scrollRect[0] + scrollRect[2]/2 - scrollText.get_width()/2, scrollRect[1] + 20))
    screen.blit(mapText, (mapRect[0] + scrollRect[2]/2 - mapText.get_width()/2, mapRect[1] + 20))
    screen.blit(profileText, (profileRect[0] + scrollRect[2]/2 - profileText.get_width()/2, profileRect[1] + 20))
    
def drawProfile():
    screen.blit(profileText, (screenWidth/2 - profileText.get_width()/2, 75/2 - profileText.get_height()/2))
    screen.blit(profilePic, (screenWidth/2 - profilePic.get_width()/2, 100))
    count = 0
    for i in range (3):
        if (i == 0):
            temp = ralewayMedium36.render(profileData[i], True, BLACK)
            screen.blit(temp, (screenWidth/2 - temp.get_width()/2, 250 + count*40))
            
        elif (i == 1):
            temp = ralewayRegular24.render(profileData[i], True, BLACK)
            screen.blit(temp, (screenWidth/2 - temp.get_width()/2, 250 + count*40))

        else:
            temp = ralewayRegular24.render(profileData[i], True, GREY)
            screen.blit(temp, (screenWidth/2 - temp.get_width()/2, 320))

        count += 1
    tempText = ralewayRegular24.render("Your Favorite Location", True, BLACK)
    tempText2 = ralewayRegular24.render("85 Location Points", True, GREY)
    screen.blit(tempText, (screenWidth/2 - tempText.get_width()/2, 400))
    screen.blit(tempText2, (screenWidth/2 - tempText2.get_width()/2, 360))
    screen.blit(image.load("Annesley Hall.jpg"), (screenWidth/2 -70, 440))
def coor():
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'

    ipa = "https://www.iplocation.net/find-ip-address"

    req = urllib.request.Request(ipa, headers = headers)
    f = urllib.request.urlopen(req)
    x = f.read().decode("utf-8")
    ip = re.findall(r'\d{3}\.\d{3}\.\d{3}\.\d{2,3}', x)

    baseurl = "http://api.ipstack.com/%s?access_key=760628d5decbc2753ef07b989107005a" % ip[0]
    # info
    f = urllib.request.urlopen(baseurl)
    json_string = json.loads(f.read())
    lat = json_string['latitude']
    lon = json_string['longitude']
    f.close()

    return [lat, lon]

userCoor = coor()
userText = ralewayMedium36.render("Your Coordinates", True, BLACK)
userText2 = ralewayMedium36.render(str(round(userCoor[0],3)) + "," + str(round(userCoor[1],3)), True, GREY)

spotFile = open("AUAU.txt")
spotData = spotFile.readlines()
distances = []
for i in range(1, 72, 2):
    x,y = spotData[i].split(",")
    distance = haversine(float(x),float(y),float(userCoor[0]),float(userCoor[1]))
    distances.append(distance)
#####################################################################
running = True
section = "Menu"
while running:
    leftClick = False #leftClick and rightClick are used to prevent accidental drag
    enter = False
    for evt in event.get():
        if evt.type == QUIT:
            running=False
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                running = False #shuts program on ESC
            if evt.key == K_RETURN:
                enter = True
        if evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:
                leftClick = True
     
#---------------------------------------------------------------------
    mx,my = mouse.get_pos() #Mouse position
#---------------------------------------------------------------------
    if section == "Menu":
         screenFill(WHITE)
         drawMenu()
         if (startRect.collidepoint(mx,my) and leftClick):
             section = "Map"

    if section == "Map":
        screenFill(WHITE)
        drawMap()
        drawBars()
        draw.rect(screen, RED, mapRect, 2)
        if (scrollRect.collidepoint(mx,my) and leftClick):
            section = "Scroll"
        if (mapRect.collidepoint(mx,my) and leftClick):
            section = "Map"
        if (profileRect.collidepoint(mx,my) and leftClick):
            section = "Profile"
    if section == "Scroll":
        screenFill(WHITE)
        drawScroll()
        drawBars()
        draw.rect(screen, RED, scrollRect, 2)
        if (scrollRect.collidepoint(mx,my) and leftClick):
            section = "Scroll"
        if (mapRect.collidepoint(mx,my) and leftClick):
            section = "Map"
        if (profileRect.collidepoint(mx,my) and leftClick):
            section = "Profile"
    if section == "Profile":
        screenFill(WHITE)
        drawBars()
        drawProfile()
        draw.rect(screen, RED, profileRect, 2)
        if (scrollRect.collidepoint(mx,my) and leftClick):
            section = "Scroll"
        if (mapRect.collidepoint(mx,my) and leftClick):
            section = "Map"
        if (profileRect.collidepoint(mx,my) and leftClick):
            section = "Profile"
    display.flip()
    
quit() #<---the worst thing ever
