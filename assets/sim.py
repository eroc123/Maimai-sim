import pygame, math, time, threading
FRAMERATE = 60

pygame.init()
pygame.mixer.init()


 

from loader import phrase_simai




def getChart(path, diffcuilty, speed):
    #return loader.phrase_simai(simaichart)
    with open(path+'/maidata.txt', 'rb') as f:
        simaichart = f.read()
    simaichart = simaichart.decode('utf-8')
    chartlist = simaichart.split('\n')
    for line in chartlist:
        if f'&inote_{diffcuilty}' in line:
            simaichart = chartlist[chartlist.index(line)+1:]
            # print(simaichart)
            for line in simaichart:
                print(line)
                if line == '':
                    simaichart = simaichart[:simaichart.index(line)]
                    break
    # print(simaichart)
    simaichart = '\n'.join(simaichart)
    print(simaichart)
    chart = phrase_simai(simaichart, diffcuilty, speed)
    musicpath = path+'/track.mp3'
    return chart, musicpath






class SongPlayer():

    def __init__(self, path, display, speed, diffcuilty ):


        self.songId = 0 #integer for song id - determines the song to play
        self.difficultyId = 0 #0 is basic, 5 is remas (if it exists)

        self.baseTime = 60 #in ticks. 60 ticks in a second. Time taken for note to go from summon ring to judgement line with a speed of one
        self.baseTimeMs = 1000 #base time in miliseconds
        speedMultiplerFactor = (speed-1)/3 + 1
        timeTicks = int(self.baseTime/speedMultiplerFactor)
        timeMs = int(self.baseTimeMs/speedMultiplerFactor)
        #self.metronometick1 = pygame.mixer.Sound("./assets/sounds/tick1.wav") 
        #self.metronometick2 = pygame.mixer.Sound("./assets/sounds/tick2.wav")
        
        self.display = display 
        monitorWidth, monitorHeight = pygame.display.get_window_size()
        self.radiusConst = monitorHeight * 0.45 #radius of judgement line
        self.summonRing = self.radiusConst * 1.7/6.3 #radius of summon ring
        self.center = (monitorWidth/2, monitorHeight/2) #center of judgement line
        print((self.radiusConst - self.summonRing))
        self.speed = int((self.radiusConst - self.summonRing) / timeTicks)    #this is in pixels per tick.

        self.speedMs = int((self.radiusConst - self.summonRing) / timeMs)
        print(self.speed)
        self.fps = pygame.time.Clock()
        self.phrasedchart, self.musicpath = getChart(path, diffcuilty, self.speed)

        # print(self.phrasedchart)

        # self.buffer = []
        
        self.bar = 0
        self.barfraction = 0
   
     
        # self.tickCount = 0
        # # print((self.FRAMERATE * 60) / self.bpm)
        self.chartimg = pygame.image.load("assets/images/chart.png").convert() #circle in the middle - judgement line
        self.chartimg = pygame.transform.scale(self.chartimg,(monitorHeight,monitorHeight)) 
        self.chartpos = self.chartimg.get_rect(center = self.display.get_rect().center) 
        #chartendimg is used to hide the note when it reaches outside
        self.chartendimg = pygame.image.load("assets/images/chart-end.png").convert_alpha()
        self.chartendimg = pygame.transform.scale(self.chartendimg,(monitorHeight,monitorHeight))
    def updateHolds(self):
        for note in self.activebuffer:
            if note.name ==  'HoldNote':
                note.elapsedDuration += 1 
                note.sprite[2].elapsedDuration += 1 
                if int(note.elapsedDuration) == int(note.holdDuration):

                    
                    note.sprite[1].locked = False
                

                    
        
    def phrase_notes(self, chart):
        clock = pygame.time.Clock()
        currentbarfraction = 0
        bar = 0
        self.activebuffer = []
        holdbuffer = []
        offset = 0
        # seperate loop that runs every 1/16th of a beat
        # higher accuracy may be needed later on 

        while self.running:

            currentbar = chart[bar]
            notes = currentbar['notes']
            # tpb : time per 1/16th beat in ms1000
            tpb = (240/currentbar['bpm'])/(currentbar['timesig'])*(1000/16)
            print(tpb)
            offset += tpb - int(tpb)
            tpb = int(tpb)
            if offset >= 1:
                tpb += int(offset)
                offset -= int(offset)
            
            
            # print(tpb)
            while self.running:

                self.updateHolds()
                # Go through the current bar
                for note in notes:
                    

                    # Check if the current 16th beat is the one to display the note for
                    if note.barFraction == currentbarfraction:
                        # Different note types
                        if note.name == 'TapNote':
                            self.activebuffer.append(note)
                        if note.name == 'HoldNote':
                            self.activebuffer.append(note)
                            
                            # Fix for note sprite so that they appear consistant to the offical game play
                            note.sprite[0].update(25)
                            note.sprite[1].locked = False
                            note.sprite[1].update(-25)
                            note.sprite[1].locked = True
                            
                            # Keep track of the current hold notes that are being displayed
                            

                # Look through the hold buffer to find out when to allow the tail note to move
                # for i in holdbuffer:
                    
                #     endFraction = (1/i.divider)*i.duration*currentbar['timesig']+i.barFraction
                #     endBar = int(i.barNumber)
                #     while endFraction >= currentbar['timesig']:
                #         endFraction -= currentbar['timesig']
                #         endBar += 1
                #     # print(endFraction,endBar, currentbarfraction, bar)
                #     if endFraction <= currentbarfraction and endBar == bar:
                #         # unlock the tail note so that it can move
                #         i.tailSprite.locked = False
                #         holdbuffer.remove(i)

                #         # print('removed')
                #     else:
                #         # otherwise display a hold body note
                #         # print(i.buttonNumber)
                #         sprite = i.segment(i.buttonNumber)
                #         if sprite:
                #             self.displaybuffer.append(sprite)
                    # # print(int((1/i.divider)*i.duration*currentbar['timesig']))
                # # print(currentbarfraction, len(holdbuffer))
                        
                        # if note.__name__ == 'HoldNo':
                        #     note.tailSprite.locked = True

                # if game is inconsistant, check actualms to compare the actual milisecond time plaused and compare to the tpb
                actualms = pygame.time.delay(tpb)
                

                # since each loop cycle is 1/16th of the beat, incrument 1/16
                currentbarfraction += 1/16

                #update hold notes

                

                # if end of the bar, incrument bar
                if int(currentbarfraction) >= currentbar['timesig']:
                    bar += 1
                    currentbarfraction = 0
                    break

    def load_music(self):
        # load the music, calculate time offset

        offset = 0.450

        time.sleep((300/self.radiusConst)+offset)
        pygame.mixer.music.play()

    def play(self,):
        
        
        
        

        self.running = True
        #load bar to read
        pygame.mixer.music.load(self.musicpath)
        threading.Thread(target=self.load_music).start()
        
        # here need finetune offset
        # time.sleep(1)

        #main game engine
        threading.Thread(target=self.phrase_notes, args=(self.phrasedchart,)).start()

        while self.running:
            # Tick FRAMERATE times per second
            FRAMERATE = 1/(self.fps.tick()/1000)

            
            self.display.blit(self.chartimg, self.chartpos)

            for note in self.activebuffer:

                for spriteindex, sprites in enumerate(note.sprite):
                   
                    img, pos = sprites.update(self.speed/(FRAMERATE/60))
                    
                    if note.name == 'TapNote':

                        
                        if math.sqrt((pos[0] - self.center[0] + img.get_rect().centerx)**2 + (pos[1] - self.center[1] + img.get_rect().centery)**2) > self.radiusConst * 1.05:
                            
                            self.activebuffer.remove(note)
                        else:
                            self.display.blit(img, pos)
                    elif note.name == 'HoldNote' and spriteindex == 2:
                        for segment in img:
                            if not math.sqrt((pos[0] - self.center[0] + segment[0].get_rect().centerx)**2 + (pos[1] - self.center[1] + segment[0].get_rect().centery)**2) > self.radiusConst * 1.05:
                            
                                self.display.blit(segment[0], segment[1])
                                print(segment[1], "segment coordinates")
                                print(len(img), "segment length")

                            pass
                    # elif note.name == "HoldNote":
                                # if note.elapsedDuration > note.holdDuration + 50:
                                #     self.activebuffer.remove(note)
                    elif note.name == 'HoldNote':
                        if not math.sqrt((pos[0] - self.center[0] + img.get_rect().centerx)**2 + (pos[1] - self.center[1] + img.get_rect().centery)**2) > self.radiusConst * 1.05:
                            
                            self.display.blit(img, pos)
                        elif note.elapsedDuration > note.holdDuration + 50:
                            pass
                            
                       
                  
                        
                    
                  
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key== pygame.K_ESCAPE:

                        self.running = False
                        pygame.mixer.music.stop()
                        

            pygame.display.update()
        return



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
            # # print(self.bar, self.barf   raction)
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



