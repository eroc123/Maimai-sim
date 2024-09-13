import pygame
import time
from zipfile import ZipFile, Path
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
                        name = '_'.join(metadata[1].split('_')[1:])
                        img = file[:-11] + 'bg.png'
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
            zip.extract(song.track, path=f'./tmp')
            zip.extract(song.img, path=f'./tmp')
            zip.extract(song.path, path=f'./tmp')
        path=f'./tmp/'+song.path[:-11]
        # print(path)
        c = sim.SongPlayer(path,self.display,3,4)
        c.play()



    def run(self):
        pygame.init()
        self.display = pygame.display.set_mode((0,0))
        pygame.display.toggle_fullscreen()
        
        # test code
        self.play_chart('ゲームバラエティ', '734')


                        

class Chart:
    def __init__(self, genre, name, img, track,id, path):
        self.genre = genre
        self.name = name
        self.img = img
        self.track = track
        self.path = path
        self.id = id



c = MainGUI()
c.read_charts()
c.run()