import pygame 
import math
from bs4 import BeautifulSoup #for webscrapping
import requests #for webscrapping (acquiring the request of the website)

pygame.init() #initialise module

#setting up pygame window
WIDTH, HEIGHT = 1500, 1000
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) #give us a pygame surface (need access to it to add something to the window)
pygame.display.set_caption("Planet Simulation")

#RGB value for the colours
BLACK = (0,0,0)
WHITE = (250,235,215) #antinquewhite 
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
GREY = (80, 78, 81)

FONT = pygame.font.SysFont("arial", 16, True, False)

def print_planet_info(MD, ML, VD, VL, ED, EL, MSD, MSL): #M = Mercury and MS = Mars
    #Earth
    font = pygame.font.SysFont("arial", 20, True, False) #last two arguments are for boldness and italics respectively 
    surface1 = font.render(f"                The current real distance from the Earth to the Sun is {ED} km.", True, WHITE) #text which will appear on screen
    surface2 = font.render(f"The time it takes for light to reach Earth from the Sun is {EL}.", True, WHITE)
    WIN.blit(surface1, (0,0))
    WIN.blit(surface2, (0,25))
    
    #Mars
    font = pygame.font.SysFont("arial", 20, True, False) #last two arguments are for boldness and italics respectively 
    surface3 = font.render(f"                The current real distance from the Earth to Mars is {MSD} km.", True, WHITE) #text which will appear on screen
    surface4 = font.render(f"The time it takes for light to reach Earth from Mars is {MSL}.", True, WHITE)
    WIN.blit(surface3, (830,0))
    WIN.blit(surface4, (830,25))
    
    
    #Venus
    font = pygame.font.SysFont("arial", 20, True, False) #last two arguments are for boldness and italics respectively 
    surface3 = font.render(f"                The current real distance from the Earth to Mars is {VD} km.", True, WHITE) #text which will appear on screen
    surface4 = font.render(f"The time it takes for light to reach Earth from Mars is {VL}.", True, WHITE)
    WIN.blit(surface3, (0,930))
    WIN.blit(surface4, (0,955))
    
    #Mercury
    font = pygame.font.SysFont("arial", 20, True, False) #last two arguments are for boldness and italics respectively 
    surface3 = font.render(f"                The current real distance from the Earth to Mars is {MD} km.", True, WHITE) #text which will appear on screen
    surface4 = font.render(f"The time it takes for light to reach Earth from Mars is {ML}.", True, WHITE)
    WIN.blit(surface3, (820,930))
    WIN.blit(surface4, (820,955))
    

def NASA_webscrape():
    
    #Mercury - distance from Mercury to Earth and the time it takes light to reach Earth from Mercury
    html_text4 = requests.get('https://theskylive.com/mercury-info').text
    soup4 = BeautifulSoup(html_text4, 'lxml')
    Mercury_distance_km = soup4.find_all('ar')
    for i, tag in enumerate(Mercury_distance_km):
        if i == 4:
            mercury_distance = tag.text #in km
        if i == 6:
            mercury_light = tag.text #in minutes
            
    #Venus - distance from Venus to Earth and the time it takes light to reach Earth from Venus       
    html_text3 = requests.get('https://theskylive.com/venus-info').text
    soup3 = BeautifulSoup(html_text3, 'lxml')
    Venus_distance_km = soup3.find_all('ar')
    for i, tag in enumerate(Venus_distance_km):
        if i == 4:
            venus_distance = tag.text #in km
        if i == 6:
            venus_light = tag.text #in minutes
    
    #Earth - distance from the Sun to Earth and the time it takes light to reach Earth from the Sun
    html_text1 = requests.get('https://theskylive.com/how-far-is-sun').text #to get the full html code in text form (bringing html text of that page)
    soup1 = BeautifulSoup(html_text1, 'lxml') #parser is lxml
    Earth_distance_km = soup1.find_all('ar')
    for i, tag in enumerate(Earth_distance_km):
        if i == 0:
            earth_distance = tag.text #in km
        if i == 2:
            earth_light = tag.text #in minutes
            
    #Mars - distance from Mars to Earth and the time it takes light to reach Earth from Mars
    html_text2 = requests.get('https://theskylive.com/mars-info').text
    soup2 = BeautifulSoup(html_text2, 'lxml')
    Mars_distance_km = soup2.find_all('ar')
    for i, tag in enumerate(Mars_distance_km):
        if i == 4:
            mars_distance = tag.text #in km
        if i == 6:
            mars_light = tag.text #in minutes
            
    return mercury_distance, mercury_light, venus_distance, venus_light, earth_distance, earth_light, mars_distance, mars_light
    

class Planet:
    Astrom_unit = 149.6e6*1000 #1 astronomical unit which is the mean distance from sun to earth (in m)
    Gravitational_constant = 6.67428e-11 #used in finding the force of attraction between objects 
    Scale = 250/Astrom_unit #represents what 1m is in pixels in the pygame scale - 1 AU is approx. 100 pixels 
    Timestep = 3600*24 #represents the time we want to represent in the simulation (everytime we update the frame, we pass this timestep). The position of the planet will be updated one day at a time
    
    def __init__(self, x, y, radius, colour, mass):
        self.x = x #in m
        self.y = y #in m
        self.radius = radius 
        self.colour = colour
        self.mass = mass #in kg 
        
        #tells us if planet is sun - we don't want to draw the orbit for the sun (this variable will tell us)
        self.orbit = [] #keeps track of points that the planet travels along in order to draw circular orbit 
        self.sun = False
        self.distance_to_sun = 0 #update this value for each planet (to draw on screen)
        
        #vertical and horizontal axis of the planets for moving in circles (moving in both directions generates a circular motion of movement)
        self.x_vel = 0
        self.y_vel = 0
        
        #draws planets on the screen 
    def draw_planet(self, win): #window we draw planet on
        x = self.x * self.Scale + WIDTH/2
        y = self.y * self.Scale + HEIGHT/2
        
        if len(self.orbit) > 2:
            updated_points = [] #getting list of updated points (x and y coordinates to scale)
            for point in self.orbit:
                x, y = point
                x = x * self.Scale + WIDTH/2
                y = y * self.Scale + HEIGHT/2
                updated_points.append((x,y)) 
        
            pygame.draw.lines(win, self.colour, False, updated_points, 2) #takes list of points and will draw lines between the points. It does not enclose (due to False as the argument)
        
        pygame.draw.circle(win, self.colour, (x,y), self.radius) #draw the x and y on the screen
        
        #Adding text to each celestial body (not sun) related to each planet's distance from the sun (in km)
        if not self.sun: 
            distance_text = FONT.render(f"{self.distance_to_sun/1000} km", 1, WHITE) #rounding to 1 decimal place
            win.blit(distance_text, (x - distance_text.get_width()/2,y - distance_text.get_width()/2))
        
        
    def force_of_attraction(self, other): #other is another planet
        #getting the distance between the 2 celestial bodies 
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2) #pythagerous theorem

        if other.sun: #if the other object is the sun, we just calculate the distance to the sun 
            self.distance_to_sun = distance #will use this when drawing distance of the sun on top of the planet 
        
        FOA = self.Gravitational_constant*self.mass*other.mass/distance**2 #force of attraction (straight line force between two celestial bodies - still need to break down in x and y component) - FOA = (G*(m1*m2))/d^2
        THETA = math.atan2(distance_y, distance_x) #gives us theta -> theta = tan-1(o/a)
        #x force and y force of attraction
        x_force = math.cos(THETA)*FOA
        y_force = math.sin(THETA)*FOA 
        
        return x_force, y_force 
        
    #function will loop through the planets, caculate the FOA of the current planets and the other planets, we will also
    #caculate the velocity of the planets and they will orbit in that speed 
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue #as distance would be 0 and thus we could not calculate the FOA
            
            fx, fy = self.force_of_attraction(planet)
            total_fx += fx
            total_fy += fy
                
            # f = m*a -> a = f/m. Now, v = a*t
        self.x_vel += total_fx/self.mass*self.Timestep #simulating over a period of time (1 day -> multiplying that by the acceleration of the planet's orbit)
        self.y_vel += total_fy/self.mass*self.Timestep 
            
            #displacement -> s = d/t -> d = s*t
        self.x += self.x_vel*self.Timestep
        self.y += self.y_vel*self.Timestep
        self.orbit.append((self.x, self.y)) #appending the x and y position we are at so we can draw the orbit of the planet 
            

#pygame event loop - infinite loop wwhich runs the entire time the simulation is going 
def main():
    run = True
    clock = pygame.time.Clock() #synchronise the game to a clock (not the speed of the computer)
    
    mercury_distance, mercury_light, venus_distance, venus_light, earth_distance, earth_light, mars_distance, mars_light = NASA_webscrape()
    
    #creating the planets
    Sun = Planet(0, 0, 30, YELLOW, 1.98892*10**30)
    Sun.sun = True 
    
    Earth = Planet(-1*Planet.Astrom_unit, 0, 16, BLUE, 5.9742*10**24) #name of class can be used to access object (Planet.Astrom_unit)
    Earth.y_vel = 29.783*1000 #initial velocity (otherwise the only force being applied is x (as we are going straight down towards the sun)) -> in metres per second (*1000)
    
    Mars = Planet(-1.524*Planet.Astrom_unit, 0, 12, RED, 6.39*10**23)
    Mars.y_vel = 24.077*1000 
    
    Mercury = Planet(0.387*Planet.Astrom_unit, 0, 8, GREY, 3.30*10**23)
    Mercury.y_vel = -47.4*1000 
    
    Venus = Planet(0.723*Planet.Astrom_unit, 0, 14, WHITE, 4.8685*10**24)
    Venus.y_vel = -35.02*1000

    celestial_bodies = [Sun, Mercury, Venus, Earth, Mars] #in order from closest to the sun 
    
    background = pygame.image.load('Space-background.jpg')
    music = pygame.mixer.music.load('Cornfield-Chase-HansZimmer-Interstellar.wav')
    pygame.mixer.music.play(-1)

    while run:
        clock.tick(60) #updates maximum at 60 frames per seek (runs loop at 60 times per second)
        WIN.fill(BLACK) #fills the window with colour black
        WIN.blit(background, (0,0))
        print_planet_info(mercury_distance, mercury_light, venus_distance, venus_light, earth_distance, earth_light, mars_distance, mars_light)
        
        for event in pygame.event.get(): #list of different events that occur (keypresses, mouse movements etc)
            if event.type == pygame.QUIT: #event which is user clicking on x (exit the program)
                run = False
        for celestial in celestial_bodies:
            celestial.update_position(celestial_bodies)
            celestial.draw_planet(WIN)
        
        pygame.display.update() #updating the display 
        
    pygame.quit() #quit pygame 

main()