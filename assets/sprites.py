import pygame
import math 
monitorWidth, monitorHeight = pygame.display.get_window_size()
radiusConst = monitorHeight * 0.45
summonRing = radiusConst * 1.7/6.3
center = (monitorWidth/2, monitorHeight/2)
positions = [
    (0.38268343236508984, 0.9238795325112867),
    (0.9238795325112867, 0.38268343236508984),
    (0.9238795325112867, -0.38268343236508984),
    (0.38268343236508984, -0.9238795325112867),
    (-0.38268343236508984, -0.9238795325112867),
    (-0.9238795325112867, -0.38268343236508984),  
    (-0.9238795325112867, 0.38268343236508984),
    (-0.38268343236508984, 0.9238795325112867),]
# Pre cauculated positions of buttons so dont need to run trig every time


def buttonpositions(pos):
    global positions
   
    if pos >= 0 or pos <= 7:
        x,y = positions[pos]
        return x,-y
    else:
        pass

singletap = pygame.image.load("assets/images/tap-note-single.png").convert_alpha()
singleholdhead = pygame.image.load("assets/images/hold.png").convert_alpha()
singleholdbody = pygame.image.load("assets/images/holdsegment.png").convert_alpha()
doubletap = pygame.image.load("assets/images/tap-note-double.png").convert_alpha()
doubleholdhead = pygame.image.load("assets/images/hold-double.png").convert_alpha()
doubleholdbody = pygame.image.load("assets/images/hold-double-segment.png").convert_alpha()

class TapNote:
    def __init__(self, button):
        self.image = singletap
        
        self.button = button
        self.x = summonRing * buttonpositions(self.button)[0]
        self.y = summonRing * buttonpositions(self.button)[1]
        self.angles = [22.5, 67.5, 112.5,157.5, 202.5, 247.5, 292.5, 337.5]
        self.image = pygame.transform.scale(self.image, (monitorHeight/7, monitorHeight/7))
        self.image = pygame.transform.rotate(self.image, self.angles[self.button] * -1)
        self.rect = self.image.get_rect()
        self.pos = [center[0] + self.x - self.rect.centerx , center[1] + self.y - self.rect.centery]
    def double(self):
        self.image = doubletap
        self.image = pygame.transform.scale(self.image, (monitorHeight/7, monitorHeight/7))
        self.image = pygame.transform.rotate(self.image, self.angles[self.button] * -1)

    def update(self, speed = 1):
        x = (speed) * buttonpositions(self.button)[0]
        y = (speed) * buttonpositions(self.button)[1]
        self.pos[0] += x
        self.pos[1] += y
        return self.image, self.pos

class HoldHead:
    def __init__(self, button):
        self.image = singleholdhead
        self.button = button

        self.x = summonRing * buttonpositions(self.button)[0]
        self.y = summonRing * buttonpositions(self.button)[1]
        self.angles = [22.5, 67.5, 112.5,157.5, 202.5, 247.5, 292.5, 337.5]
        self.image = pygame.transform.scale(self.image, (monitorHeight/14, monitorHeight/14))
        self.image = pygame.transform.rotate(self.image, self.angles[self.button] * -1)
        self.rect = self.image.get_rect()
        self.pos = [center[0] + self.x - self.rect.centerx , center[1] + self.y - self.rect.centery]

    def double(self):
        self.image = doubleholdhead
        self.image = pygame.transform.scale(self.image, (monitorHeight/14, monitorHeight/14))
        self.image = pygame.transform.rotate(self.image, self.angles[self.button] * -1)
    def update(self, speed = 1):
        x = (speed) * buttonpositions(self.button)[0]
        y = (speed) * buttonpositions(self.button)[1]
        self.pos[0] += x
        self.pos[1] += y
        return self.image, self.pos

class HoldTail:
    def __init__(self, button):

        self.image = singleholdhead
        self.button = button
        self.x = summonRing * buttonpositions(self.button)[0]
        self.y = summonRing * buttonpositions(self.button)[1]
        self.angles = [22.5, 67.5, 112.5,157.5, 202.5, 247.5, 292.5, 337.5]
        self.image = pygame.transform.scale(self.image, (monitorHeight/14, monitorHeight/14))
        self.image = pygame.transform.rotate(self.image, self.angles[self.button - 4] * -1)
        self.rect = self.image.get_rect()
        self.pos = [center[0] + self.x - self.rect.centerx , center[1] + self.y - self.rect.centery]
    def double(self):
        self.image = doubleholdhead
        self.image = pygame.transform.scale(self.image, (monitorHeight/14, monitorHeight/14))
        self.image = pygame.transform.rotate(self.image, self.angles[self.button -4] * -1)
    def update(self, speed):
        
        if not self.locked:
            x = (speed) * buttonpositions(self.button)[0]
            y = (speed) * buttonpositions(self.button)[1]
            self.pos[0] += x
            self.pos[1] += y
        return self.image, self.pos
class HoldBody:
    def __init__(self, button):

        self.locked = False
        self.image = singleholdbody
        self.button = button
        self.x = summonRing * buttonpositions(self.button)[0]
        self.y = summonRing * buttonpositions(self.button)[1]
        self.angles = [22.5, 67.5, 112.5,157.5, 202.5, 247.5, 292.5, 337.5]
        self.image = pygame.transform.scale(self.image, (monitorHeight/14, monitorHeight/14))
        self.image = pygame.transform.rotate(self.image, self.angles[self.button - 4] * -1)
        self.rect = self.image.get_rect()
        self.pos = [center[0] + self.x - self.rect.centerx , center[1] + self.y - self.rect.centery]
    def double(self):
        self.image = doubleholdbody
        self.image = pygame.transform.scale(self.image, (monitorHeight/14, monitorHeight/14))
        self.image = pygame.transform.rotate(self.image, self.angles[self.button] * -1)
    def update(self, speed):
        # if not self.locked:
        ############################
        # for hold body i think its better to only have one and update it's length by tranformations
        ############################

        x = (speed) * buttonpositions(self.button)[0]
        y = (speed) * buttonpositions(self.button)[1]
        self.pos[0] += x
        self.pos[1] += y
        return self.image, self.pos
