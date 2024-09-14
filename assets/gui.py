import pygame
import time
from zipfile import ZipFile, Path
import io
import os
import threading
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
        pygame.font.init()
        pygame.init()
        self.display = pygame.display.set_mode((0,0))
        pygame.display.toggle_fullscreen()
        windowcaption = 'Python MaiMai Sim'
        pygame.display.set_caption(windowcaption)
        self.clock = pygame.time.Clock()

    

    def read_charts(self):
        self.songlist = []
        self.genrelist = {}
        f = []
        # background = pygame.Surface((pygame.display.Info().current_w , pygame.display.Info().current_h))
        self.loading = 0
        self.total = 0
        
        for (dirpath, dirnames, filenames) in walk(self.path):
            f.extend(filenames)
            break
        for file_name in f:
            with ZipFile(self.path+file_name, 'r') as zip: 
                self.total += len(zip.namelist())/3
        
        for file_name in f:
            
            with ZipFile(self.path+file_name, 'r') as zip: 
                for file in zip.namelist():
                    if 'maidata' in file:
                        self.clock.tick()

                        metadata = file.split('/')
                        genre = metadata[0]
                        data = zip.read(name = file).decode('utf-8')
                        data = data.split('\n')
                        name = data[0].split('=')[1]
                        
                        img = file[:-11] + 'bg.png'
                        
                        
                        
                        track = file[:-11] + 'track.mp3'
                        id = metadata[1].split('_')[0]
                        self.genrelist[genre] = file_name
                        self.songlist.append(Chart(genre, name, img, track, id, file))
                        
                        # print(f'loading {int((self.loading/self.total)*100)}%, {file_name}')
                        self.loading += 1
                        self.clock.tick()
                        self.display.fill((int((self.loading/self.total)*255),int((self.loading/self.total)*255),int((self.loading/self.total)*255)))
                        pygame.display.flip()
                        
                        # time.sleep(0.01)
    
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
        c = sim.SongPlayer(path,self.display,6,4)
        c.play()
    def animate_in(self, img):
        display_size = pygame.display.Info().current_w , pygame.display.Info().current_h
        w, h = display_size
        for i in range (0,255,8): 
            img.set_alpha(i)         
            time.sleep(0.001)
            self.display.blit(img, (0.5*w - img.get_rect().centerx,0.5*h-img.get_rect().centery))

            pygame.display.update()

    def animate_out(self, img):
        display_size = pygame.display.Info().current_w , pygame.display.Info().current_h
        w, h = display_size
        for i in range (225,0,-8): 
            img.set_alpha(i)         
            time.sleep(0.001)
            self.display.blit(img, (0.5*w - img.get_rect().centerx,0.5*h-img.get_rect().centery))

            pygame.display.update()
    def animate_in_chart(self, img):
        display_size = pygame.display.Info().current_w , pygame.display.Info().current_h
        w, h = display_size
        for i in range (0,255,8): 
            img.set_alpha(i)         
            time.sleep(0.001)
            
            background_surface = pygame.Surface(display_size)
            background_surface.fill(pygame.Color("#626262"))
            background_surface2 = pygame.Surface((img.get_rect().width, img.get_rect().height))
            background_surface2.fill(pygame.Color('#000000'))
            
            self.display.blit(background_surface, (0, 0))
            self.display.blit(self.chartimg, self.chartpos)
            self.display.blit(background_surface2, (0.5*w - img.get_rect().centerx,0.5*h-img.get_rect().centery))
            self.display.blit(img, (0.5*w - img.get_rect().centerx,0.5*h-img.get_rect().centery))

            pygame.display.update()
        self.oldselection = self.currentselection
    def animate_out_chart(self,img):
        for i in range (255, 0, -8): 
            img.set_alpha(i)         
            time.sleep(0.001)
            display_size = pygame.display.Info().current_w , pygame.display.Info().current_h
            w, h = display_size
            background_surface = pygame.Surface(display_size)
            background_surface.fill(pygame.Color("#626262"))
            background_surface2 = pygame.Surface((img.get_rect().width, img.get_rect().height))
            background_surface2.fill(pygame.Color('#000000'))
            self.display.blit(background_surface, (0, 0))
            self.display.blit(self.chartimg, self.chartpos)
            self.display.blit(background_surface2, (0.5*w - img.get_rect().centerx,0.5*h-img.get_rect().centery))
            self.display.blit(img, (0.5*w - img.get_rect().centerx,0.5*h-img.get_rect().centery))
            pygame.display.update()
    def run(self):
        
        display_size = pygame.display.Info().current_w , pygame.display.Info().current_h
        

        
        

        clock = pygame.time.Clock()
        font = pygame.font.Font("./assets/fonts/japanese.ttf",20)
        titlefont = pygame.font.Font("./assets/fonts/japanese.ttf",40)
        titletext = titlefont.render('Python MaiMai Simulator', True, (0,0,0))
        self.animate_in(titletext)
        self.animate_out(titletext)
        
        w,h = display_size
        
        y = 0
        genre = 'niconicoボーカロイド'

        self.chartimg = pygame.image.load("assets/images/chart.png").convert() #circle in the middle - judgement line
        self.chartimg = pygame.transform.scale(self.chartimg,(h,h)) 
        self.chartpos = self.chartimg.get_rect(center = self.display.get_rect().center) 

        background_surface = pygame.Surface(display_size)
        background_surface.fill(pygame.Color("#626262"))
        
        
        textsurface = font.render(genre, True, (255, 255, 255))
        
        self.currentselection = 0
        
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
        self.currentselectionflock = Lock()
        self.currentselectionblock = Lock()
        self.oldselection = 0
        background_surface.blit(background_surface, (0, 0))
        background_surface.blit(self.chartimg, self.chartpos)
        background_surface.blit(textsurface, ((0.5*w )- (textsurface.get_rect().centerx), 0.2*h - textsurface.get_rect().centery))
        for song in self.songlist:
            if song.genre == genre:
                # print(self.path+self.genrelist[genre])
                with ZipFile(self.path+self.genrelist[genre], 'r') as zip: 
                    songimg = pygame.image.load(io.BytesIO(zip.read(self.songlist[self.songlist.index(song)+self.currentselection].img)))
                break
        songsurface = pygame.Surface((0.5*h, 0.5*h))
        
        songsurface.blit(pygame.transform.scale(songimg, (0.45*h,0.45*h)), (0.025*h,0.025*h))
        text = font.render(song.name, True, (255,255,255))
        songsurface.blit(text, (songsurface.get_rect().centerx-text.get_rect().centerx, 0.95*songsurface.get_rect().height))
        background_surface.blit(songsurface, (0.5*w - songsurface.get_rect().centerx,0.5*h-songsurface.get_rect().centery))
        self.animate_in(background_surface)


        while True:
            clock.tick(60)
            
            
            
            self.display.blit(background_surface, (0, 0))
            self.display.blit(self.chartimg, self.chartpos)
            self.display.blit(textsurface, ((0.5*w )- (textsurface.get_rect().centerx), 0.2*h - textsurface.get_rect().centery))
            
            if self.oldselection != self.currentselection:
                self.animate_out_chart(songsurface)
                song = self.songlist[self.currentselection]
                songsurface = pygame.Surface((0.5*h, 0.5*h))
                
                for song in self.songlist:
                    if song.genre == genre:
                        # print(self.path+self.genrelist[genre])
                        with ZipFile(self.path+self.genrelist[genre], 'r') as zip: 
                            songimg = pygame.image.load(io.BytesIO(zip.read(self.songlist[self.songlist.index(song)+self.currentselection].img)))               
                        break
                songsurface.blit(pygame.transform.scale(songimg, (0.45*h,0.45*h)), (0.025*h,0.025*h))
                text = font.render(song.name, True, (255,255,255))
                songsurface.blit(text, (songsurface.get_rect().centerx-text.get_rect().centerx, 0.95*songsurface.get_rect().height))
                self.animate_in_chart(songsurface)
            else:
                song = self.songlist[self.currentselection]
                songsurface = pygame.Surface((0.5*h, 0.5*h))
                for song in self.songlist:
                    if song.genre == genre:
                        # print(self.path+self.genrelist[genre])
                        with ZipFile(self.path+self.genrelist[genre], 'r') as zip: 
                            songimg = pygame.image.load(io.BytesIO(zip.read(self.songlist[self.songlist.index(song)+self.currentselection].img)))  
                        break              
                songsurface.blit(pygame.transform.scale(songimg, (0.45*h,0.45*h)), (0.025*h,0.025*h))
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
                if self.currentselectionflock.counter == 0:
                    self.currentselection += 1
                    print(self.currentselection)
                self.currentselectionflock.counter += 1
            elif self.currentselectionflock.counter >= 5:
                self.currentselectionflock.counter = 0

            if 5 in pressedlist:
                if self.currentselectionblock.counter == 0:
                    self.currentselection -= 1
                    print(self.currentselection)
                self.currentselectionblock.counter += 1
            elif self.currentselectionblock.counter >= 5:
                self.currentselectionblock.counter = 0

            if 3 in pressedlist:
                if self.currentselectionblock.counter == 0:
                    self.play_chart(song.genre, song.id)
                self.currentselectionblock.counter += 1
            elif self.currentselectionblock.counter >= 5:
                self.currentselectionblock.counter = 0

            
                
                
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