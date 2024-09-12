import pygame, math, time, threading
FRAMERATE = 60

pygame.init()
pygame.mixer.init()
display = pygame.display.set_mode((0,0))
pygame.display.toggle_fullscreen()
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

slider = Slider(display, 0, 0, 400, 20, min=0, max=999, step=1)
output = TextBox(display, 475, 200, 50, 50, fontSize=30)    



output.disable()
from loader import phrase_simai



def getChart(songId):
    #return loader.phrase_simai(simaichart)
    
    simaichart = '''(119){1},
{2}4h[4:1],4h[4:1],
{2}5h[4:1],5h[4:1],
{2}4h[4:1],4h[4:1],
{2}5h[4:1],5h[4:1],
{4}4h[8:1]/5h[8:7],4h[8:1],4h[8:1],4h[8:1],
{4}4h[8:7]/5h[8:1],5h[8:1],5h[8:1],5h[8:1],
{4}4h[8:1]/5h[8:7],4h[8:1],4h[8:1],4h[8:1],
{4}4h[8:1]/5h[8:1],4h[8:1]/5h[8:1],3/6,,
{8}2h[4:1],,3h[4:1],,4,4,5h[4:1],,
{8}6h[4:1],,7h[4:1],,1,8,1b,,
{8}7h[4:1],,6h[4:1],,5,5,4h[4:1],,
{8}3h[4:1],,2h[4:1],,8,1,8b,,
{8}1/8h[4:1],,2h[4:1],,6,6,4h[4:1],,
{8}5h[4:1],,3,3,7h[4:1],,1b,,
{8}1h[4:1]/8,,7h[4:1],,3,3,5h[4:1],,
{8}4h[4:1],,6,6,2h[4:1],,8b,,
{2}1h[4:3]/8h[4:1],7h[4:3],
{8}2h[4:1],,,,3/6,3/6,3b/6h[2:1],,
{2}3h[4:3],5h[4:3],
{8}4h[2:1],,,,5,4,5b,,
{2}4h[4:1]/5h[4:3],3h[4:3],
{8}7h[4:1],,,,1/7,1/7,1h[2:1]/7b,,
{2}8h[4:3],2h[4:3],
{8}6h[2:1],,,,4,5,4b,,
{4}4h[2:1],5,5h[2:1],6,
{4}6h[2:1],7,7h[2:1],8,
{4}8h[2:1],1,1h[2:1],2,
{4}2h[2:1],3,3h[2:1],4,
{4}4h[2:1],8,3h[2:1],7,
{4}2h[2:1],6,1h[2:1],5,
{4}8h[2:1],4,7h[2:1],3,
{4}6h[2:1],2,5-8[32:3],1b,
{4}4h[8:1]/5h[8:5],4,4h[8:5],5,
{4}5h[8:5],4,4h[8:5],5b,
{4}5h[8:3],4h[8:3],5h[8:3],4h[8:3],
{4}5h[8:3],4h[8:3],5h[4:1],4b,
{4}4h[8:1]/5h[8:3],3h[8:3],6h[8:3],2h[8:3],
{4}7h[8:3],1h[8:3],8h[4:1],1b,
{4}1h[8:3]/8h[8:1],7h[8:3],2h[8:3],6h[8:3],
{4}3h[8:3],5h[4:1],4b,,
{8}2h[4:1],,3h[4:1],,1,1,4h[4:1],,
{8}8h[4:1],,5h[4:1],,7,7,6h[4:1],,
{8}5h[4:1],,8h[4:1],,4,4,1h[4:1],,
{8}3h[4:1],,2h[4:1],,1,8,1b,,
{8}1h[4:1],,7h[4:1],,3,3,5h[4:1],,
{8}8h[4:1],,2h[4:1],,6,6,4h[4:1],,
{4}1h[4:1],7h[4:1],8h[4:1],2h[4:1],
{16}1h[4:1],,,,8h[4:1],,,,2h[8:1],,7h[8:1],,1h[16:1],8h[16:1],1h[16:1],8h[16:1],
{4}1h[4:1],5h[4:1],2h[4:1],6h[4:1],
{8}3h[4:1],,7h[4:1],,4,4,8h[4:1],,
{4}5h[4:1],1h[4:1],6h[4:1],2h[4:1],
{8}7,7,3h[4:1],,8h[4:1],,4b,,
{4}1/5h[8:3],2h[8:3],4h[8:3],3h[8:3],
{8}2h[8:3],,4h[4:1],,1,2b/3b,2b/3b,,
{4}4/8h[8:3],6h[8:3],7h[8:3],8h[8:3],
{8}6h[8:3],,1h[4:1],,5,2b/6b,3b/7b,,
{8}3h[2:1],4,5,,6h[2:1],5,4,,
{8}2h[2:1],4,5,,7,4b/5b,4b/5b,,
{8}3h[2:1],1,8,,6h[2:1],8,1,,
{8}2h[2:1],1,8,,7,1b/8b,1b/8b,,
{8}1h[2:1],7,6,,2h[2:1],8,7,,
{8}3h[2:1],1,8,,4,2b/5b,2b/5b,,
{8}5h[2:1],3,2,,6h[2:1],4,3,,
{8}7h[2:1],5,4,,8,1b/6b,2b/5b,,
{4}4h[4:3]/5,3h[8:1],2h[8:1],1,
{4}4/8h[4:3],5h[8:1],6h[8:1],7,
{4}1h[4:3]/8,2h[8:1],4h[8:1],6,
{4}1/8h[4:3],7h[8:1],5h[8:1],3,
{4}1h[2:1]/8,2h[8:1],8h[2:1],7h[8:1],
{4}2h[2:1],3h[8:1],7h[2:1],6h[8:1],
{4}3h[2:1],2h[8:1],6h[2:1],7h[8:1],
{16}4h[2:1],,,,3h[8:1],,,,5,,4,5,4,,,,
{1},
{1},
{1},
E'''
    chart = phrase_simai(simaichart)
    return chart





class SongPlayer():
    def __init__(self, songId, display, speed = 5,):

        self.songId = 0 #integer for song id - determines the song to play
        self.difficultyId = 0 #0 is basic, 5 is remas (if it exists)

        
        #self.metronometick1 = pygame.mixer.Sound("./assets/sounds/tick1.wav") 
        #self.metronometick2 = pygame.mixer.Sound("./assets/sounds/tick2.wav")
        self.speed = speed #note speed
        self.display = display 
        monitorWidth, monitorHeight = pygame.display.get_window_size()
        self.radiusConst = monitorHeight * 0.45 #radius of judgement line
        summonRing = self.radiusConst * 1.7/6.3 #radius of summon ring
        self.center = (monitorWidth/2, monitorHeight/2) #center of judgement line
      
        self.fps = pygame.time.Clock()
        self.phrasedchart = getChart(songId)
        # print(self.phrasedchart)

        # self.buffer = []
        
        self.bar = 0
        self.barfraction = 0
        self.soundDelay = (self.radiusConst/((math.log(speed) + 1)* self.radiusConst * 0.1/20))
     
        # self.tickCount = 0
        # # print((self.FRAMERATE * 60) / self.bpm)
        self.chartimg = pygame.image.load("assets/images/chart.png").convert() #circle in the middle - judgement line
        self.chartimg = pygame.transform.scale(self.chartimg,(monitorHeight,monitorHeight)) 
        self.chartpos = self.chartimg.get_rect(center = self.display.get_rect().center) 
        #chartendimg is used to hide the note when it reaches outside
        self.chartendimg = pygame.image.load("assets/images/chart-end.png").convert_alpha()
        self.chartendimg = pygame.transform.scale(self.chartendimg,(monitorHeight,monitorHeight))
    
    def phrase_notes(self, chart):
        clock = pygame.time.Clock()
        currentbarfraction = 0
        bar = 0
        self.displaybuffer = []
        holdbuffer = []
        offset = 0
        # seperate loop that runs every 1/16th of a beat
        # higher accuracy may be needed later on 
        while True:
            currentbar = chart[bar]
            notes = currentbar['notes']
            # tpb : time per 1/16th beat in ms1000
            tpb = (240/currentbar['bpm'])/(currentbar['timesig'])*(1000/16)
            print(tpb)
            offset += tpb - int(tpb)
            tpb = int(tpb)
            if offset >= 1:
                tpb -= int(offset)
                offset -= int(offset)
            
            
            # print(tpb)
            while True:
                # Go through the current bar
                for note in notes:
                    # Check if the current 16th beat is the one to display the note for
                    if note.barFraction == currentbarfraction:
                        # Different note types
                        if note.name == 'TapNote':
                            self.displaybuffer.append(note.sprite)
                        if note.name == 'HoldNote':
                            self.displaybuffer.append(note.headSprite)
                            self.displaybuffer.append(note.tailSprite)
                            # Fix for note sprite so that they appear consistant to the offical game play
                            note.headSprite.update(25)
                            note.tailSprite.locked = False
                            note.tailSprite.update(-25)
                            note.tailSprite.locked = True
                            # Keep track of the current hold notes that are being displayed
                            holdbuffer.append(note)

                # Look through the hold buffer to find out when to allow the tail note to move
                for i in holdbuffer:
                    
                    endFraction = (1/i.divider)*i.duration*currentbar['timesig']+i.barFraction
                    endBar = int(i.barNumber)
                    while endFraction >= currentbar['timesig']:
                        endFraction -= currentbar['timesig']
                        endBar += 1
                    # print(endFraction,endBar, currentbarfraction, bar)
                    if endFraction <= currentbarfraction and endBar == bar:
                        # unlock the tail note so that it can move
                        i.tailSprite.locked = False
                        holdbuffer.remove(i)

                        # print('removed')
                    else:
                        # otherwise display a hold body note
                        # print(i.buttonNumber)
                        sprite = i.segment(i.buttonNumber)
                        if sprite:
                            self.displaybuffer.append(sprite)
                    # # print(int((1/i.divider)*i.duration*currentbar['timesig']))
                # # print(currentbarfraction, len(holdbuffer))
                        
                        # if note.__name__ == 'HoldNo':
                        #     note.tailSprite.locked = True

                # if game is inconsistant, check actualms to compare the actual milisecond time plaused and compare to the tpb
                actualms = pygame.time.delay(tpb)
                

                # since each loop cycle is 1/16th of the beat, incrument 1/16
                currentbarfraction += 1/16
                # print(currentbarfraction, currentbar['timesig'])
                # if end of the bar, incrument bar
                if int(currentbarfraction) >= currentbar['timesig']:
                    bar += 1
                    currentbarfraction = 0
                    break

    def load_music(self):
        # load the music, calculate time offset
        offset = 0.600
        time.sleep((300/self.radiusConst)+offset)
        pygame.mixer.music.play()

    def play(self,):
        
        
        
        

        #load bar to read
        pygame.mixer.music.load('./assets/sounds/track.mp3')
        threading.Thread(target=self.load_music,daemon=True).start()
        
        # here need finetune offset
        time.sleep(1)

        #main game engine
        threading.Thread(target=self.phrase_notes, args=(self.phrasedchart,), daemon=True).start()
                
        while True:
            # Tick FRAMERATE times per second
            self.fps.tick(FRAMERATE)

            self.display.blit(self.chartimg, self.chartpos)

            for note in self.displaybuffer:
                img, pos = note.update(self.speed/(FRAMERATE/60))
                self.display.blit(img, pos)
                if math.sqrt((pos[0] - self.center[0] + img.get_rect().centerx)**2 + (pos[1] - self.center[1] + img.get_rect().centery)**2) > self.radiusConst * 1.05:
                    self.displaybuffer.remove(note)
            # display notes in between
            self.display.blit(self.chartendimg, self.chartpos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key== pygame.K_ESCAPE:
                        pygame.quit()

            pygame.display.update()



        #while True:

            # output.setText(slider.getValue())
            # self.fps.tick(self.FRAMERATE)
            

            # # update screen/delete object
            # # if self.ticks == int(self.soundDelay) + 200:
                
            # self.display.fill((0,0,0))
            # # # print(int(self.ticks % ((self.FRAMERATE * 60) / self.bpm)))
            # if int(self.ticks % ((self.FRAMERATE * 60) / self.bpm)) == int(0.0):
            #     self.barfraction += 1
            #     self.tickBuffer.append(self.ticks + self.soundDelay)
            #     if self.barfraction == self.timesig:
            #         self.bar += 1
                    
            #         self.barfraction = 0
            #     if self.bar == 0:
            #         self.display.fill((20,20,20))
            # # print(self.bar, self.barfraction)
            # # if ticks == tickBuffer[0]:
            # #     tickCount += 1
            # #     tickBuffer.remove(ticks)
            # #     if tickCount == 1:
            # #         pygame.mixer.Channel(0).play(tick1)
                    
            # #     else:
            # #         pygame.mixer.Channel(0).play(tick2)
            # #     if tickCount == timesig:
            # #         tickCount = 0
            # #self.buffer, self.chart = self.phraser.checkTime(self.chart, self.buffer, self.bar, self.barfraction)
            

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #     if event.type == pygame.KEYDOWN:
            #         if event.key== pygame.K_ESCAPE:
            #             pygame.quit()
            
            
            # self.display.blit(self.chartimg, self.chartpos)
            # for note in self.buffer:
            #     image, pos = note.update()
            #     self.display.blit(image, pos)
            #     if math.sqrt((pos[0] - self.center[0] + image.get_rect().centerx)**2 + (pos[1] - self.center[1] + image.get_rect().centery)**2) > self.radiusConst * 1.05:
            #         self.buffer.remove(note)
            # self.display.blit(self.chartendimg, self.chartpos)

            # pygame.display.update()
            # self.ticks += 1

        

# class chartPhraser():
#     def __init__(self, speed, timesig):
#         self.holdbuffer = []
#         self.holdbodylock = 0
#         self.speed = speed
#         self.timesig = timesig
        
#     def phraseHold(self, buffer, duration, bar, barfraction, note):
#         tail = None
#         if note[0] == 'hold':
#             if note[1] == bar and note[2] == barfraction:
#                 tail = HoldTail(self.speed, note[3])
#                 buffer.append(tail)
#                 self.holdbuffer.append([tail, duration, bar, barfraction])
#         for hold in self.holdbuffer:
#             baroffset = 0
#             duration = hold[1]
#             if duration > 3:
#                 duration = int(duration%self.timesig)
#                 baroffset = int(duration/self.timesig)
            
#             if hold[2] + baroffset == bar and hold[3] + duration == barfraction:
#                 hold[0].locked = False
#                 self.holdbuffer.remove(hold)
#             elif hold[2] + baroffset >= bar and hold[3] + duration >= barfraction:
#                 if tail == None and hold[0].locked == True:
#                     self.buffer.append(HoldBody(self.speed, hold[0].button))

        
#         return buffer


#     def checkTime(self, chart, buffer, bar, barfraction):
#         for note in chart:
#             buffer = self.phraseHold(buffer, note[4], bar, barfraction, note)
#             if note[1] == bar and note[2] == barfraction:
#                 if note[0] == 'tap':
#                     if note[4]:
#                         tapnote = TapNote(self.speed,note[3])
#                         tapnote.double()
#                         buffer.append(tapnote)

#                         chart.remove(note)
#                     else:
#                         buffer.append(TapNote(self.speed,note[3]))
#                         chart.remove(note)
#                     break
#                 if note[0] == 'hold':
#                     buffer.append(HoldHead(self.speed, note[3]))
#                     chart.remove(note)
#                     break # for double notes just dont break
#         return buffer, chart



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
# # print((FRAMERATE * 60) / bpm)
# while True:
#     fps.tick(FRAMERATE)
    
#     # update screen/delete object
#     if ticks == int(soundDelay):
#         pygame.mixer.music.load('./assets/sounds/track.mp3')
#         pygame.mixer.music.play()
#     display.fill((0,0,0))
#     # print(int(ticks % ((FRAMERATE * 60) / bpm)))
#     if int(ticks % ((FRAMERATE * 60) / bpm)) == int(0.0):
#         barfraction += 1
#         tickBuffer.append(ticks + soundDelay)
#         if barfraction == timesig:
#             bar += 1
            
#             barfraction = 0
#         if bar == 0:
#             display.fill((20,20,20))
#     # print(bar, barfraction)
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


#play the whole thing
c.play()