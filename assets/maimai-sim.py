import pygame, math, time
import loader

pygame.init()
pygame.mixer.init()
display = pygame.display.set_mode((0,0))
pygame.display.toggle_fullscreen()
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
slider = Slider(display, 0, 0, 400, 20, min=0, max=999, step=1)
output = TextBox(display, 475, 200, 50, 50, fontSize=30)    

output.disable()
from sprites import *



def getChart(songId):
    return loader.phrase_simai(simaichart)

class SongPlayer():
    def __init__(self, songId, display, speed = 5,):
        self.FRAMERATE = 60
        self.tick1 = pygame.mixer.Sound("./assets/sounds/tick1.wav") 
        self.tick2 = pygame.mixer.Sound("./assets/sounds/tick2.wav")
        self.speed = speed
        self.display = display
        monitorWidth, monitorHeight = pygame.display.get_window_size()
        self.radiusConst = monitorHeight * 0.45
        summonRing = self.radiusConst * 1.7/6.3
        self.center = (monitorWidth/2, monitorHeight/2)
        self.ticks = 0
        self.currentnote = 0
        self.fps = pygame.time.Clock()
        self.chart,self.bpm = getChart(songId)
        # buffer = [TapNote(1,0),TapNote(1,1),TapNote(1,2),TapNote(1,3),TapNote(1,4),TapNote(1,5),TapNote(1,6),TapNote(1,7)]
        self.buffer = []
        self.ticks = 0
        self.bar = 0
        self.barfraction = 0
        self.soundDelay = (self.radiusConst/((math.log(speed) + 1)* self.radiusConst * 0.1/20))
        self.tickBuffer = []
        self.tickCount = 0
        print((self.FRAMERATE * 60) / self.bpm)
        self.chartimg = pygame.image.load("assets/images/chart.png").convert()
        self.chartimg = pygame.transform.scale(self.chartimg,(monitorHeight,monitorHeight))
        self.chartpos = self.chartimg.get_rect(center = self.display.get_rect().center)
        #chartendimg is used to hide the note when it reaches outside
        self.chartendimg = pygame.image.load("assets/images/chart-end.png").convert_alpha()
        self.chartendimg = pygame.transform.scale(self.chartendimg,(monitorHeight,monitorHeight))
        self.timesig = 4
        self.phraser = chartPhraser(self.speed, self.timesig)

        pass
    def play(self,):
        pygame.mixer.music.load('./assets/sounds/track.mp3')
        pygame.mixer.music.play()
        while True:

            output.setText(slider.getValue())
            self.fps.tick(self.FRAMERATE)
            

            # update screen/delete object
            # if self.ticks == int(self.soundDelay) + 200:
                
            self.display.fill((0,0,0))
            print(int(self.ticks % ((self.FRAMERATE * 60) / self.bpm)))
            if int(self.ticks % ((self.FRAMERATE * 60) / self.bpm)) == int(0.0):
                self.barfraction += 1
                self.tickBuffer.append(self.ticks + self.soundDelay)
                if self.barfraction == self.timesig:
                    self.bar += 1
                    
                    self.barfraction = 0
                if self.bar == 0:
                    self.display.fill((20,20,20))
            print(self.bar, self.barfraction)
            # if ticks == tickBuffer[0]:
            #     tickCount += 1
            #     tickBuffer.remove(ticks)
            #     if tickCount == 1:
            #         pygame.mixer.Channel(0).play(tick1)
                    
            #     else:
            #         pygame.mixer.Channel(0).play(tick2)
            #     if tickCount == timesig:
            #         tickCount = 0
            self.buffer, self.chart = self.phraser.checkTime(self.chart, self.buffer, self.bar, self.barfraction)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key== pygame.K_ESCAPE:
                        pygame.quit()
            
            
            self.display.blit(self.chartimg, self.chartpos)
            for note in self.buffer:
                image, pos = note.update()
                self.display.blit(image, pos)
                if math.sqrt((pos[0] - self.center[0] + image.get_rect().centerx)**2 + (pos[1] - self.center[1] + image.get_rect().centery)**2) > self.radiusConst * 1.05:
                    self.buffer.remove(note)
            self.display.blit(self.chartendimg, self.chartpos)

            pygame.display.update()
            self.ticks += 1

        

class chartPhraser():
    def __init__(self, speed, timesig):
        self.holdbuffer = []
        self.holdbodylock = 0
        self.speed = speed
        self.timesig = timesig
        
    def phraseHold(self, buffer, duration, bar, barfraction, note):
        tail = None
        if note[0] == 'hold':
            if note[1] == bar and note[2] == barfraction:
                tail = HoldTail(self.speed, note[3])
                buffer.append(tail)
                self.holdbuffer.append([tail, duration, bar, barfraction])
        for hold in self.holdbuffer:
            baroffset = 0
            duration = hold[1]
            if duration > 3:
                duration = int(duration%self.timesig)
                baroffset = int(duration/self.timesig)
            
            if hold[2] + baroffset == bar and hold[3] + duration == barfraction:
                hold[0].locked = False
                self.holdbuffer.remove(hold)
            elif hold[2] + baroffset >= bar and hold[3] + duration >= barfraction:
                if tail == None and hold[0].locked == True:
                    self.buffer.append(HoldBody(self.speed, hold[0].button))

        
        return buffer


    def checkTime(self, chart, buffer, bar, barfraction):
        for note in chart:
            buffer = self.phraseHold(buffer, note[4], bar, barfraction, note)
            if note[1] == bar and note[2] == barfraction:
                if note[0] == 'tap':
                    buffer.append(TapNote(self.speed,note[3]))
                    chart.remove(note)
                    break
                if note[0] == 'hold':
                    buffer.append(HoldHead(self.speed, note[3]))
                    chart.remove(note)
                    break # for double notes just dont break
        return buffer, chart


simaichart = '''
(119){4},
{4}3,3,4,4,
{4}5,5,6,,
{4}7,7,8,8,
{4}1,1,2,,
{4}3,3/4,3,3/4,
{4}6,5/6,6,5/6,
{4}4/5,3/6,4/5,3/6,
{4}4/5,3/6,2b/7b,,
{4}5/6,5/6,3/4,3/4,
{4}5/6,3/4,5b/6b,,
{4}3/4,3/4,5/6,5/6,
{4}3/4,5/6,3b/4b,,
{4}6h[4:1],5,6h[4:1],5,
{4}3h[4:1],4,3h[4:1],4,
{4}6h[4:1],5,6h[4:1],5,
{4}3h[4:1],4,4/5,,
{4}7/8,7/8,1/2,1/2,
{4}7/8,1/2,7b/8b,,
{4}1/2,1/2,7/8,7/8,
{4}1/2,7/8,1b/2b,,
{4}7h[4:1],8,7h[4:1],8,
{4}2h[4:1],1,2h[4:1],1,
{4}7h[4:1],8,7h[4:1],8,
{4}2h[4:1],1,1/8,,
{4}3h[4:3],,4,4,
{4}6h[4:3],,5,5,
{4}7h[4:3],,8,8,
{4}2h[4:3],,1,1,
{4}8,8,7,7,
{4}6,6,5,5,
{4}4,4,3,3,
{4}2,2,1h[4:1],8b,
{4}1,2,3,4,
{4}5,6,7,1/8,
{4}8,7,6,5,
{4}4,3,2,1/8,
{4}8,1/7,8,1/7,
{4}1,2/8,1,2/8,
{4}8,1/7,1,2/8,
{4}1/8,2/7,3b/6b,,
{1}3-8[2:1]/4-7[2:1],
{4}1,1,2h[4:1],,
{1}1-6[2:1]/2-5[2:1],
{4}7,7,8h[4:1],,
{4}8,7,6,5,
{4}1,2,3,4,
{4}4/5,3/6,4/5,3/6,
{4}2/7,2/7,2b/7b,,
{4}7/8,1/6,1/2,3/8,
{4}7/8,1/2,7b/8b,,
{4}1/2,3/8,7/8,1/6,
{4}1/2,7/8,1b/2b,,
{4}7h[4:1],8,2h[4:1],1,
{4}7h[4:1],8,2h[4:1],1,
{4}1/8,1/8,2/7,2/7,
{4}1/8,2/7,3b/6b,,
{4}3/4,2/5,5/6,4/7,
{4}3/4,5/6,3b/4b,,
{4}5/6,4/7,3/4,2/5,
{4}5/6,3/4,5b/6b,,
{4}3h[4:1],4,6h[4:1],5,
{4}3h[4:1],4,6h[4:1],5,
{4}4/5,4/5,3/6,3/6,
{4}4/5,3/6,2b/7b,,
{4}8,8,1,1,
{4}2,2,3,,
{4}4,4,5,5,
{4}6,6,7,,
{4}2,1/2,2,1/2,
{4}7,7/8,7,7/8,
{4}1/8,2/7,1/8,2/7,
{4}1/8,2/7,3b/6b,,
{1},
{1},
{1},
E'''

# chart, bpm = loader.phrase_simai(simaichart)
# chart = [['hold', 1,0,1,8,False,False]]
# # buffer = [TapNote(1,0),TapNote(1,1),TapNote(1,2),TapNote(1,3),TapNote(1,4),TapNote(1,5),TapNote(1,6),TapNote(1,7)]
# buffer = []
# ticks = 0
# bar = 0
# barfraction = 0
# soundDelay = (radiusConst/((math.log(speed) + 1)* radiusConst * 0.1/20))
# tickBuffer = []
# tickCount = 0
# print((FRAMERATE * 60) / bpm)
# while True:
#     fps.tick(FRAMERATE)
    
#     # update screen/delete object
#     if ticks == int(soundDelay):
#         pygame.mixer.music.load('./assets/sounds/track.mp3')
#         pygame.mixer.music.play()
#     display.fill((0,0,0))
#     print(int(ticks % ((FRAMERATE * 60) / bpm)))
#     if int(ticks % ((FRAMERATE * 60) / bpm)) == int(0.0):
#         barfraction += 1
#         tickBuffer.append(ticks + soundDelay)
#         if barfraction == timesig:
#             bar += 1
            
#             barfraction = 0
#         if bar == 0:
#             display.fill((20,20,20))
#     print(bar, barfraction)
#     # if ticks == tickBuffer[0]:
#     #     tickCount += 1
#     #     tickBuffer.remove(ticks)
#     #     if tickCount == 1:
#     #         pygame.mixer.Channel(0).play(tick1)
            
#     #     else:
#     #         pygame.mixer.Channel(0).play(tick2)
#     #     if tickCount == timesig:
#     #         tickCount = 0
#     buffer, chart = checkTime(chart, buffer, bar, barfraction)
    

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#         if event.type == pygame.KEYDOWN:
#             if event.key== pygame.K_ESCAPE:
#                 pygame.quit()
    
    
#     display.blit(chartimg, chartpos)
#     for note in buffer:
#         image, pos = note.update()
#         display.blit(image, pos)
#         if math.sqrt((pos[0] - center[0] + image.get_rect().centerx)**2 + (pos[1] - center[1] + image.get_rect().centery)**2) > radiusConst * 1.05:
#             buffer.remove(note)
#     display.blit(chartendimg, chartpos)

#     pygame.display.update()
#     ticks += 1


c = SongPlayer(1, display, 10)

c.play()