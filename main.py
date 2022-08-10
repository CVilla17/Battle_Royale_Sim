# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 20:24:27 2021
@authors: Carlos Villa, Walter Truitt
"""

import random
import math
#from ps3_visualize import *
 
           
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.
        Does NOT test whether the returned position fits inside the room.
        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed
        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()

        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y

        return Position(new_x, new_y)

    def __str__(self):
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))
        
        
        
        
        
        
class Room(object):
    """
    A Room represents a rectangular region containing clean or dusty
    tiles.
    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dust. The tile is considered clean only when the amount
    of dust on this tile is 0.
    """
    def __init__(self, width, height, danger_zone_amount,num_weapons, heal_zones):
        """
        Initializes a rectangular room with the specified width, height, and
        dust_amount on each tile.
        width: an integer > 0
        height: an integer > 0
        dust_amount: an integer >= 0
        """
        self.width = width
        self.height = height
        self.position = {}
        for i in range(self.width):
            for j in range(self.height):
                self.position[(i, j)] = 0
        
        for _ in range(danger_zone_amount):
            randx = random.randint(0, self.width)
            randy = random.randint(0, self.height)           
            self.position[(randx, randy)] = 1.0
        for _ in range(num_weapons):
            randx = random.randint(0, self.width)
            randy = random.randint(0, self.height)           
            self.position[(randx, randy)] = 2.0
        for _ in range(heal_zones):
            randx = random.randint(0, self.width)
            randy = random.randint(0, self.height)           
            self.position[(randx, randy)] = 3.0

                
    def get_pos_dict(self):
        return self.position
    def in_danger(self, w, h):
        """
        Returns the amount of the tile (w, h)
        Assumes that (w, h) represents a valid tile inside the room.
        w: an integer
        h: an integer
        Returns: boolean. True is in danger.
        """
        if float(self.position[(w,h)]) == 1:
            return True
        else:
            return False 

    
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.
        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        return pos.get_x() >= 0 and pos.get_x() < self.width and pos.get_y() >= 0 and pos.get_y() < self.height

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        w = random.randint(0, self.width -1)
        h = random.randint(0, self.height -1)
        pos = Position(w, h)

        return pos
        
 
class Participant(object):
    def __init__(self, room, name, height, speed, strength, intelligence, creativity):
        """
        name - str - name of participant
        room - room object
        height - int - # of inches. Participant gets .1 points for every inch above 58 inches
        speed, strength, intelligence, creativity - float - attributes must add up to 10
        self.health - float - health is a multiplier of a participants stats
        """
        self.room=room
        self.position=self.room.get_random_position()
        self.direction=random.uniform(0.0,360.0)
        self.health= 1.0
        self.name = name
        if (height-58)>=0:
            self.height = (height-58)*.1
        else:
            self.height = 0
        if sum([self.height,speed,strength,intelligence,creativity])<=10:
            self.speed = speed
            self.strength = strength
            self.intelligence=intelligence
            self.creativity = creativity
        else:
            raise AssertionError('Adjust stats to be <= 10')
        
    def get_name(self):
           return self.name
    def get_strength(self):
           return self.strength
    def get_speed(self):
           return self.speed
    def get_intelligence(self):
           return self.intelligence
    def get_height(self):
           return self.height
    def get_health(self):
        return self.health
    def get_creativity(self):
        return self.creativity
        
           
    #update Participant class to mimic robot    
    def set_health(self, change):
        """updates a players health bar"""
        if self.health+change<=0:
            self.health=0
        else:
            self.health+=change
    def set_strength(self,change):
        """updates a players strength"""
        self.strength+=change
    def get_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.position

    def get_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_position(self, position):
        """
        Set the position of the robot to position.
        position: a Position object.
        """
        self.position=position
    def set_room(self,room):
        self.room=room

    def set_direction(self, direction):
        """
        Set the direction of the robot to direction.
        direction: float representing an angle in degrees
        """
        self.direction=direction

    def check_space(self, pos):
        """
        Checks for different items on a space and adjusts a character's stats accordingly
        pos: a Position object
        """
        w = math.floor(pos.get_x())
        h = math.floor(pos.get_y())
        dangerStatements=[f'{self.name} hit their head',f' {self.name} drowned a bit', f'Oops {self.name} has been burned', f'Yikes, {self.name} ate a mushroom that was poisonous',f'{self.name} fell out of a tree']
        weaponStatements=[f'{self.name} got the glock', f'{self.name} found a bow and arrow', f'{self.name} found a sword', f'{self.name} found a good rock for hitting', f'{self.name} looking strong rn, ngl']
        healStatements=[f'{self.name} found NeoSporin in this arena', f'{self.name}, you found a Band-aid in the bushes', f'{self.name} has an immune system on 100', f'{self.name} has recovered from injuries', f'{self.name} is so down bad a doctor came to help']
        if self.room.get_pos_dict()[(w,h)]==1.0:
            print(random.choice(dangerStatements))
            self.set_health(-1*random.random())
            self.room.get_pos_dict()[(w,h)] = 0

        elif self.room.get_pos_dict()[(w,h)]==2.0:
            print(random.choice(weaponStatements))
            self.set_strength(random.random())
            self.room.get_pos_dict()[(w,h)]=0

        elif self.room.get_pos_dict()[(w,h)]==3.0:
            print(random.choice(healStatements))
            self.set_health(random.random())
            self.room.get_pos_dict()[(w,h)]=0

    def update_position(self):
        """
        Simulates the passage of a single time-step.
        Moves player to new position and checks space for items
        """
        
        nextPos = Position.get_new_position(self.position,self.direction,self.speed)
        #checks if the new position is in the room. If it is it moves the player
        #to the new position and checks the space. If not it changes the player's direction.
        if self.room.is_position_in_room(nextPos):
            self.position=nextPos
            self.check_space(self.position)
        else:
            self.direction=random.uniform(0.0,360.0)    
            
def check_teams(pList):
    """Randomly creates teams if 3 participants are on the same tile"""
    primeList = pList
    if len(pList)>2:
        if (pList[0].get_intelligence() + pList[0].get_creativity()) >= 4.5   and  (pList[1].get_intelligence() + pList[1].get_creativity()) >= 4.5 and (pList[2].get_intelligence() + pList[2].get_creativity()) <  4.5:
          if random.random()>.3:
              print(f'Alliance formed between {pList[0].get_name()} and {pList[1].get_name()}')
              pList=[[primeList[0],primeList[1]],primeList[2]]
          else:
              print("No alliance formed")
              
        elif (pList[1].get_intelligence() + pList[1].get_creativity()) >= 4.5   and  (pList[2].get_intelligence() + pList[2].get_creativity()) >= 4.5 and (pList[0].get_intelligence() + pList[0].get_creativity()) <  4.5:
            if random.random()>.3:
                print(f'Alliance formed between {pList[0].get_name()} and {pList[1].get_name()}')
                pList=[[primeList[1],primeList[2]],primeList[0]]
            else:
                 print("No alliance formed")
            
        elif (pList[0].get_intelligence() + pList[0].get_creativity()) >= 4.5   and  (pList[2].get_intelligence() + pList[2].get_creativity()) >= 4.5 and (pList[1].get_intelligence() + pList[1].get_creativity()) <  4.5:
            if random.random()>.3:
                print(f'Alliance formed between {pList[0].get_name()} and {pList[2].get_name()}')
                pList=[[primeList[0],primeList[2]],primeList[1]] 
            else:
                print("No alliance formed")
            
        else:
            print("No Alliance formed")
    return pList
#Continue work
def checkFlee(pList):
    """Checks if a participant is able to escape the encounter without having to fight.
    If the participant has a combined speed and creativity better than other participant(s)
    in the encounter they can flee
    pList: list of participant objects
    return: list of participants still in encounter"""
    
    
    
    runner=random.choice(pList)
    
    pList.remove(runner)
    
    truthList=[]
    for p in pList:
        truthList.append( (runner.get_speed()+runner.get_creativity()) > (p.get_speed()+p.get_creativity()))
    
    if False in truthList:
        pList.append(runner)
        
        return pList
    else:
        print(f'{runner.get_name()} has fled the battle')
        return pList

def fight(fighter1, fighter2):
    """
    Runs through battle scenarios
    fighter1 and fighter2: participant objects, fighter 1 may be a list with two participant objects
    return: string that declares the fight is over and tells how much health is left for each participant
    """
    
    #battle for a participant getting jumped
    if type(fighter1)==list:
        
        tag1 = fighter1[0]
        tag2 = fighter1[1]
        attacker = random.choice([fighter1, fighter2])
        if attacker==fighter1:
            defender= fighter2
            print(f'{tag1.get_name()} and {tag2.get_name()} are attacking {defender.get_name()}')
            chance_to_hit = (tag1.get_speed()+tag1.get_height()+tag2.get_speed()+tag2.get_height())/8
            chance_to_evade = (defender.get_speed()+defender.get_intelligence())/8
            hit = (tag1.get_strength()+tag2.get_strength())/-10
            for i in range(2):
                if random.random()<= chance_to_hit: 
                    if random.random()<=chance_to_evade:
                        print("Missed hit")
                    else:
                        print("Hit landed!")
                        defender.set_health(hit)
                       
        else:
            defender = fighter1
            print(f'{tag1.get_name()} and {tag2.get_name()} are being attacked by {attacker.get_name()}')
            chance_to_hit = (fighter2.get_speed()+fighter2.get_height())/5
            chance_to_evade = (tag1.get_speed()+tag1.get_intelligence()+tag2.get_speed()+tag2.get_intelligence())/10
            hit = (fighter2.get_strength())/-10
            for i in range(2):
                if random.random()<= chance_to_hit: 
                    if random.random()<=chance_to_evade:
                        print("Missed hit")
                    else:
                        print("Hit landed!")
                        tag1.set_health(hit/2)
                        tag2.set_health(hit/2)
        print(f'Health of {tag1.get_name()} is {tag1.get_health()}\nHealth of {tag2.get_name()} is {tag2.get_health()}\
              \nHealth of {fighter2.get_name()} is {fighter2.get_health()}')
    
    #battle for 1v1    
    else:
       attacker = random.choice([fighter1,fighter2]) 
       if attacker==fighter1:
           defender=fighter2
       else:
           defender=fighter1
       chance_to_hit = (attacker.get_speed() + attacker.get_height())/5
       chance_to_evade = (defender.get_speed() + defender.get_intelligence())/10
       hit = (attacker.get_strength())/-10
       for i in range(2):
                if random.random()<= chance_to_hit: 
                    if random.random()<=chance_to_evade:
                        print("Missed hit")
                    else:
                        print("Hit landed!")
                        defender.set_health(hit)
       print(f'Health of {attacker.get_name()} is {attacker.get_health()}\nHealth of {defender.get_name()} is {defender.get_health()}')
    print("Fight is over")
    
def Encounter(pList):
    """
    pList - List of participant objects
    if Ps are on a team - make them together in a list - ex: pList could be [[p1, p2], p3]
    """
    print("Encounter!")
    #Checks for alliances
    new_pList = check_teams(pList) 
    #if no alliances, checks if someone flees
    if pList==new_pList:
        new_pList = checkFlee(pList)
    if len(new_pList)==1:
        print("Encounter over")
    else:
        fighter1=new_pList[0]
        fighter2=new_pList[1]
        fight(fighter1,fighter2)
           
            
def HungerGames( num_weapons, danger_zones_amount, room_width, room_height, heal_zones):
    """
    #participants - list - list of Participant instances
    num_weapons - int - number of weapons
    danger_zones_amount - int - number of danger zone amounts
    room_width - int - width of room
    room_height - int - height of room
    heal_zones - int - amount of zones that heal a participant
    """
    #similar to run_simulation
    
    #Initializes a new room and robots
    room = Room(room_width, room_height, danger_zones_amount, num_weapons, heal_zones)
    players=int(input("Type in the number of participants: "))
    
    participantList=[]
    
    for j in range(players):
        while True:
            try:
                print(f'Input stats for player {j+1}')
                print("Stats must add up to 10 or less. Categories are height, speed, strength, intelligence, and creativity. Height stat is (height-58)*.1. If height is less than 58, height stat is 0")
                name=str(input("Type participant name: "))
                height=float(input("Type participant height in inches: "))
                speed=float(input("Type number for speed: "))
                strength=float(input("Type number for strength: "))
                intelligence=float(input("Type number for intelligence: "))
                creativity=float(input("Type number for creativity: "))
                participant=Participant(room, name, height, speed, strength, intelligence, creativity)
                participantList.append(participant)
                break
            except AssertionError:
                print("Fix stats so they add up to 10 or less")
               
    print("Game starting, may the odds be ever in your favor!")
    #anim = RobotVisualization(len(participantList), room_width, room_height, delay = .1)
    while len(participantList)>1:
        positionDict={}
        matchUps=[]
        for participant in participantList:
            participant.update_position()
            #anim.update(room, participantList)
            if participant.get_health()==0:
                print(f'{participant.get_name()} has died')
                participantList.remove(participant)
        for p in participantList:
            x=math.floor(p.get_position().get_x())
            y=math.floor(p.get_position().get_y())
            positionDict[p]=(x,y)
        for p in participantList:
            position=positionDict[p]
            fighters=[]
            for key,value in positionDict.items():
                if value==position:
                    fighters.append(key)
            if len(fighters)<=3 and len(fighters)>1 and fighters not in matchUps:
                matchUps.append(fighters)
        for matches in matchUps:
            Encounter(matches)
        for p in participantList:
            if p.get_health()==0:
                print(f'{p.get_name()} has died')
                participantList.remove(p)
    #anim.done()  
    print(f'{participantList[0].get_name()} has won the Hunger Games!')
    
        

def FullGame():
    print("Welcome to the Hunger Games\nDesign your arena")
    room_width=int(input("Type in arena width(ex:5,10,25,etc): "))
    room_height=int(input("Type in room height(ex:5,10,25,etc): "))
    danger_zones_amount=int(input("Type in number of desired danger zones(ex:3,4,etc): "))
    num_weapons=int(input("Type in number of desired weapons for arena(ex:1,5,10): "))
    heal_zones=int(input("Type in number of healing areas(ex:1,5,10): "))
    HungerGames(num_weapons,danger_zones_amount,room_width,room_height,heal_zones)
    print("Thank you for playing!")
FullGame()