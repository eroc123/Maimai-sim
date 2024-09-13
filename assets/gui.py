import pygame
import time
from zipfile import ZipFile, Path
import io
import os
from os import walk

def fade_image(image_path):
    display_size = pygame.display.Info().current_w , pygame.display.Info().current_h - 50
    screen = pygame.display.set_mode(display_size)
    image = pygame.image.load(image_path)
    image_size = image.get_rect().size

    centered_image = [(display_size[0] - image_size[0])/2, (display_size[1] - image_size[1])/2]

    time.sleep(1)

    for i in range (255):
        screen.fill((0,0,0))    
        image.set_alpha(i)    
        screen.blit(image, centered_image)    
        pygame.display.update()    
        time.sleep(0.001)

    time.sleep(1.5)

    for i in range (255, 0, -1):
        screen.fill((0,0,0))       
        image.set_alpha(i)    
        screen.blit(image, centered_image)    
        pygame.display.update()    
        time.sleep(0.001)



class MainGUI:
    def __init__(self):
        self.songlist = []
        self.path = './assets/charts/'

    def read_charts(self):
        self.songlist = []
        self.genrelist = {}
        f = []
        
        for (dirpath, dirnames, filenames) in walk(self.path):
            f.extend(filenames)
            break
        for file_name in f:

            with ZipFile(self.path+file_name, 'r') as zip: 
                for file in zip.namelist():
                    if 'maidata' in file:
                        metadata = file.split('/')
                        genre = metadata[0]
                        data = zip.read(name = file).decode('utf-8')
                        data = data.split('\n')
                        name = data[0].split('=')[1]
                        
                        img = file[:-11] + 'bg.png'
                        
                        
                        img = pygame.image.load(io.BytesIO(zip.read(img)))
                        track = file[:-11] + 'track.mp3'
                        id = metadata[1].split('_')[0]
                        self.genrelist[genre] = file_name
                        self.songlist.append(Chart(genre, name, img, track, id, file))
    
    def play_chart(self, genre, id):
        import sim

        for song in self.songlist:
            if song.genre == genre and song.id == id:
                break
        with ZipFile(self.path+self.genrelist[genre], 'r') as zip: 
            if not os.path.exists(f'./tmp/'+song.path[:-11]):
                zip.extract(song.track, path=f'./tmp')
                zip.extract(song.path, path=f'./tmp')
        path=f'./tmp/'+song.path[:-11]
        # print(path)
        c = sim.SongPlayer(path,self.display,3,4)
        c.play()



    def run(self):
        pygame.font.init()
        pygame.init()
        self.display = pygame.display.set_mode((0,0))
        pygame.display.toggle_fullscreen()
        windowcaption = 'Python MaiMai Sim'
        pygame.display.set_caption(windowcaption)
        display_size = pygame.display.Info().current_w , pygame.display.Info().current_h
        

        
        

        clock = pygame.time.Clock()
        w,h = display_size
        
        y = 0
        genre = 'ゲームバラエティ'

        self.chartimg = pygame.image.load("assets/images/chart.png").convert() #circle in the middle - judgement line
        self.chartimg = pygame.transform.scale(self.chartimg,(h,h)) 
        self.chartpos = self.chartimg.get_rect(center = self.display.get_rect().center) 

        background_surface = pygame.Surface(display_size)
        background_surface.fill(pygame.Color("#626262"))
        font = pygame.font.Font("./assets/fonts/japanese.ttf",20)
        textsurface = font.render(genre, True, (255, 255, 255))
        
        currentselection = 0
        
        buttonpositions = [
            (-0.38268343236508984, 0.9238795325112867),
            (-0.9238795325112867, 0.38268343236508984),
            (-0.9238795325112867, -0.38268343236508984), 
            (-0.38268343236508984, -0.9238795325112867), 
            (0.38268343236508984, -0.9238795325112867),
            (0.9238795325112867, -0.38268343236508984),
            (0.9238795325112867, 0.38268343236508984),
            (0.38268343236508984, 0.9238795325112867),
            
            
        ]
        for x,y in buttonpositions:
            buttonpositions[buttonpositions.index((x,y))] = ((0.5-(h * 0.45 * x)/w),0.5-(0.45 * y))

        
        pressedlist = []
        currentselectionflock = Lock()
        currentselectionblock = Lock()
        while True:
            clock.tick(60)
            
            
            
            self.display.blit(background_surface, (0, 0))
            self.display.blit(self.chartimg, self.chartpos)
            self.display.blit(textsurface, ((0.5*w )- (textsurface.get_rect().centerx), 0.2*h - textsurface.get_rect().centery))
            song = self.songlist[currentselection]
            songsurface = pygame.Surface((0.5*h, 0.5*h))
            
            songsurface.blit(pygame.transform.scale(song.img, (0.45*h,0.45*h)), (0.025*h,0.025*h))
            text = font.render(song.name, True, (255,255,255))
            songsurface.blit(text, (songsurface.get_rect().centerx-text.get_rect().centerx, 0.95*songsurface.get_rect().height))
            self.display.blit(songsurface, (0.5*w - songsurface.get_rect().centerx,0.5*h-songsurface.get_rect().centery))
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    event.x,event.y = event.pos
                    event.x = event.x/w
                    event.y = event.y/h
                    for x,y in buttonpositions:
                        if event.x >= x - 0.1 and event.x <= x + 0.1 and event.y >= y - 0.1 and event.y <= y + 0.1:
                            touch = buttonpositions.index((x,y))
                            # print(f'Button {touch} down')
                            pressedlist.append(touch)
                    print(event.x, event.y)
                if event.type == pygame.MOUSEBUTTONUP:
                    event.x,event.y = event.pos
                    event.x = event.x/w
                    event.y = event.y/h
                    for x,y in buttonpositions:
                        if event.x >= x - 0.1 and event.x <= x + 0.1 and event.y >= y - 0.1 and event.y <= y + 0.1:
                            touch = buttonpositions.index((x,y))
                            # print(f'Button {touch} up')
                            pressedlist.remove(touch)
                    
                if event.type == pygame.FINGERDOWN:
                    
                    for x,y in buttonpositions:
                        if event.x >= x - 0.1 and event.x <= x + 0.1 and event.y >= y - 0.1 and event.y <= y + 0.1:
                            touch = buttonpositions.index((x,y))
                            # print(f'Button {touch} down')
                            pressedlist.append(touch)
                if event.type == pygame.FINGERUP:
                    
                    for x,y in buttonpositions:
                        if event.x >= x - 0.1 and event.x <= x + 0.1 and event.y >= y - 0.1 and event.y <= y + 0.1:
                            touch = buttonpositions.index((x,y))
                            # print(f'Button {touch} up')
                            pressedlist.remove(touch)

            
                
            if 2 in pressedlist:
                if currentselectionflock.counter == 0:
                    currentselection += 1
                    print(currentselection)
                currentselectionflock.counter += 1
            elif currentselectionflock.counter >= 5:
                currentselectionflock.counter = 0

            if 5 in pressedlist:
                if currentselectionblock.counter == 0:
                    currentselection -= 1
                    print(currentselection)
                currentselectionblock.counter += 1
            elif currentselectionblock.counter >= 5:
                currentselectionblock.counter = 0

            if 3 in pressedlist:
                if currentselectionblock.counter == 0:
                    self.play_chart(song.genre, song.id)
                currentselectionblock.counter += 1
            elif currentselectionblock.counter >= 5:
                currentselectionblock.counter = 0

            
                
                
            pygame.display.update()

        # test code
        # self.play_chart('ゲームバラエティ', '734')

class Lock:
    def __init__(self,):
        self.counter = 0
                        

class Chart:
    def __init__(self, genre, name, img, track,id, path):
        self.genre = genre
        self.name = name
        self.img = img
        self.track = track
        self.path = path
        self.id = id
        self.button = None



c = MainGUI()
c.read_charts()
c.run()