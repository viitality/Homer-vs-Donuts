import os
import time
import math

import pygame as py
import numpy as np

import MarkovProcess as mp


resolutionEcran = (1200,700)
FPS = 100
greenColor = (0,255,0)
blackColor = (0, 0, 0)
blueColor = (80, 150, 255)
whiteColor = (230,230,230)
purpleColor = (140, 50, 160)

py.init()
clock = py.time.Clock()
arialFontFPS = py.font.SysFont("arial", 15)
arial10Font = py.font.SysFont("arial", 10)
py.display.set_caption("Homer VS Donuts")



class Background(py.sprite.Sprite):
    def __init__(self,grid_size):
        super(Background, self).__init__()
        self.grid_size = grid_size
        self.leftmargin = 30
        self.rightmargin = 20
        self.topmargin = 200
        self.bottommargin = 20
        self.reload()

    def reload(self):
        img_background = py.image.load("img/fond.png") # ou pour l'original : "img/donut_earth.png"
        self.img_background = py.transform.scale(img_background,resolutionEcran)
        self.size_node = min((resolutionEcran[0]-self.leftmargin-self.rightmargin)/self.grid_size[0],
                             (resolutionEcran[1]-self.topmargin-self.bottommargin)/self.grid_size[1])
        self.size_white = int(self.size_node*0.8)
        self.horizon_center = (resolutionEcran[0]-self.size_node*self.grid_size[0]-self.leftmargin-self.rightmargin)//2
        self.vertical_center = (resolutionEcran[1]-self.size_node*self.grid_size[1]-self.topmargin-self.bottommargin)//2

    def draw(self, surface):
        surface.blit(self.img_background, [0,0])
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                py.draw.rect(surface, whiteColor, py.Rect(self.leftmargin +self.horizon_center+ x*self.size_node,
                    self.topmargin +self.vertical_center+ y*self.size_node,
                    self.size_white,self.size_white))

class Display_Qvalues():
    def __init__(self, background, homer_agent):
        self.background = background
        self.homer_agent = homer_agent
        self.font = py.font.SysFont("arial",10)
        self.color = (130,130,130)

    def draw(self,surface):
        for x in range(self.background.grid_size[0]):
            for y in range(self.background.grid_size[1]):
                xx = self.background.leftmargin +self.background.horizon_center+ x*self.background.size_node
                yy = self.background.topmargin +self.background.vertical_center+ y*self.background.size_node
                width , height = self.font.size(str("%.1f"%self.homer_agent.Q_values[x,y]["up"]))
                surface.blit(self.font.render(str("%.1f"%self.homer_agent.Q_values[x,y]["up"]), True, self.color), [xx+self.background.size_white//2-width//2, yy])
                width , height = self.font.size(str("%.1f"%self.homer_agent.Q_values[x,y]["down"]))
                surface.blit(self.font.render(str("%.1f"%self.homer_agent.Q_values[x,y]["down"]), True, self.color), [xx+self.background.size_white//2-width//2, yy+self.background.size_white-height])
                width , height = self.font.size(str("%.1f"%self.homer_agent.Q_values[x,y]["left"]))
                surface.blit(self.font.render(str("%.1f"%self.homer_agent.Q_values[x,y]["left"]), True, self.color), [xx+2, yy+self.background.size_white//2-height//2])
                width , height = self.font.size(str("%.1f"%self.homer_agent.Q_values[x,y]["right"]))
                surface.blit(self.font.render(str("%.1f"%self.homer_agent.Q_values[x,y]["right"]), True, self.color), [xx+self.background.size_white-width-2, yy+self.background.size_white//2-height//2])

class Display_images():
    def __init__(self, background, homer_agent):
        self.background = background
        self.homer_agent = homer_agent
        self.homer_grid = homer_agent.grid
        self.reload()

    def reload(self):
        self.homer_img = self.load_img(name="homer.png")
        self.donut_img = self.load_img(name="donut.png")
        self.characters_img = self.load_img(nb=len(self.homer_grid.lose_states))
    

    def load_img(self,nb=1,name=""):
        if name != "":
            img = py.image.load("img/"+name)
            img = self.scale_img(img)
            return img
        list_characters = os.listdir(os.path.join("img","characters"))
        list_img = []
        for i in range(nb):
            list_img.append(self.scale_img(py.image.load("img/characters/"+list_characters[i%len(list_characters)])))
        return list_img

    def scale_img(self, img):
        ix,iy=img.get_size()
        size_max = self.background.size_white*1.15
        if ix>iy:
            scale = float(size_max)/float(ix)
            sx = size_max
            sy = scale*iy
        else:
            scale = float(size_max)/float(iy)
            sx = scale*ix
            sy = size_max
        return py.transform.scale(img,(sx,sy))
            
    def draw(self,surface):
        coords = self.homer_agent.current_state
        xx = self.background.leftmargin +self.background.horizon_center+ coords[0]*self.background.size_node
        yy = self.background.topmargin +self.background.vertical_center+ coords[1]*self.background.size_node
        surface.blit(self.homer_img, [xx,yy])
        for i,coords in enumerate(self.homer_grid.lose_states):
            xx = self.background.leftmargin +self.background.horizon_center+ coords[0]*self.background.size_node
            yy = self.background.topmargin +self.background.vertical_center+ coords[1]*self.background.size_node
            surface.blit(self.characters_img[i], [xx,yy])
        for i,coords in enumerate(self.homer_grid.win_states):
            xx = self.background.leftmargin +self.background.horizon_center+ coords[0]*self.background.size_node
            yy = self.background.topmargin +self.background.vertical_center+ coords[1]*self.background.size_node
            surface.blit(self.donut_img, [xx,yy])


def draw_text(surf, text, size, x, y, color=blackColor):
    """
    Petite fonction pour la représentation graphique avec pygame
    :param surf: surface sur laquelle écrire
    :param text: texte à écrire
    :param size: taille de police
    :param x: coordonnée x de l'emplacement du texte
    :param y: coordonnée y de l'emplacement du texte
    :param color: couleur du texte
    """
    """
    police = py.font.SysFont("monospace" ,15)
    image_texte = police.render (text, 1 , color)
    surface.blit(image_texte, (320,240))
    py.display.flip()
    """
    font = py.font.Font(py.font.match_font('arial'), size)
    text_surface = font.render(text, True, color) # white for color true for anti aliased
    text_rect = text_surface.get_rect() 
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)  # le text surface est sur le text rectangle


#########################################################################################

grid_size = (8,5)
win_states = [(5,0)]
lose_states = [(0,1),(2,2),(3,1),(4,0),(5,4),(6,2)]
obstacle_states = []
start = (0,4)
#homer_success_rate = [0.8, 0.1, 0.1]

available_actions = ['up', 'down', 'left', 'right']
#======= Initialisation des probabilités de transition (probabilité pour Homer de se tromper):
    # /!\ Varie entre chaque exécution du code, mais pas entre chaque partie lors d'une même exécution
probasDirectory = {}
for line in range(grid_size[1]):
    for column in range(grid_size[0]):
        spot_id = str(line)+'_'+str(column)
        probasDirectory[spot_id] = {}
        for action in available_actions:
            probas = np.random.rand(4)
            probas = probas / np.sum(probas)
            i  = np.argmax(probas)
            probas[i] += 0.5 # permet d'assurer que la probabilité de prendre la bonne action est >= 0.5
            probas = list(probas / np.sum(probas)) # normalisation
            probasDirectory[spot_id][action] = {}
            probasDirectory[spot_id][action][action] = max(probas)
            probas.remove(max(probas))
            for x in available_actions:
                if x != action:
                    proba = np.random.choice(probas)
                    probasDirectory[spot_id][action][x] = proba
                    probas.remove(proba)
            #print(spot_id, action, probasDirectory[spot_id][action])


homer_grid = mp.Grid(grid_size, win_states, lose_states, obstacle_states, probasDirectory)
homer_agent = mp.Agent(start, homer_grid)

#########################################################################################

windowSurface = py.display.set_mode(resolutionEcran, py.RESIZABLE)
background = Background(grid_size)
display_Qvalues = Display_Qvalues(background,homer_agent)
display_images = Display_images(background,homer_agent)

learning = False
learning2 = False
running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        elif event.type == py.VIDEORESIZE:
            resolutionEcran = event.size

            background.reload()
            display_images.reload()
        elif event.type == py.KEYDOWN:
            if event.key == py.K_a:
                print("you pressed a")
                homer_agent.play_to_learn()
            elif event.key == py.K_z:
                print("you pressed z")
                homer_agent.play_to_learn_step()
            elif event.key == py.K_e:
                print("you pressed e")
                homer_agent.play_to_learn_step2()
            elif event.key == py.K_l:
                print("you pressed l")
                learning = True
            elif event.key == py.K_m:
                print("you pressed m")
                learning2 = True
            elif event.key == py.K_s:
                print("you pressed s")
                learning = False
                learning2 = False
            elif event.key == py.K_COLON:
                homer_agent.lr /= 2
                print(f"learning rate :{homer_agent.lr}")
            elif event.key == py.K_ASTERISK:
                homer_agent.lr *= 2
                print(f"learning rate :{homer_agent.lr}")
            elif event.key == py.K_RETURN:
                homer_agent.play_to_win()
            elif event.key == py.K_ESCAPE:
                running = False
                
    if learning:
        homer_agent.play_to_learn()
    elif learning2:
        homer_agent.play_to_learn_step2()
    background.draw(windowSurface)
    display_Qvalues.draw(windowSurface)
    display_images.draw(windowSurface)
    #affichage du titre
    draw_text(windowSurface, "EAT DONUTS & AVOID ENEMIES!", 60, resolutionEcran[0] // 2, 10, blackColor)  # 18 est pour la taille
    #py.display.flip() 

    #affichage du score
    draw_text(windowSurface, "Score :", 50, resolutionEcran[0] -130, resolutionEcran[1]//2 - 180, purpleColor) 
    score=156
    draw_text(windowSurface, str(score), 50, resolutionEcran[0] -130, resolutionEcran[1]//2 - 100, purpleColor) 

    #affichage des touches
    draw_text(windowSurface, "Controls :", 40, 70, 150, blackColor)  # taille, x, y
    draw_text(windowSurface, "- enter : play_to_win", 20, 85, 210, blackColor)  
    draw_text(windowSurface, "- a : play_to_learn", 20, 76, 250, blackColor)  
    draw_text(windowSurface, "- z : play_to_learn_step", 20, 95, 290, blackColor)  
    draw_text(windowSurface, "- e : play_to_learn_step2", 20, 100, 330, blackColor)
    draw_text(windowSurface, "- l : apprentissage", 20, 75, 370, blackColor)
    draw_text(windowSurface, "- s : arrêt d'apprentissage", 20, 102, 410, blackColor)
    draw_text(windowSurface, "- * : learning_rate *2", 20, 85, 450, blackColor)
    draw_text(windowSurface, "- / : learning_rate /2", 20, 85, 490, blackColor)

    """
    font2 = py.font.SysFont('Keys : ', 50)
    img2 = font2.render('Keys : ', True, blackColor)
    windowSurface.blit(img2, (12, 160))
    font3 = py.font.SysFont('a : play_to_learn', 25)
    img3 = font3.render('a : play_to_learn', True, blackColor)
    windowSurface.blit(img3, (12, 210))
    font4 = py.font.SysFont('z : play_to_learn by step', 25)
    img4 = font4.render('z : play_to_learn by step', True, blackColor)
    windowSurface.blit(img4, (12, 260))
    font5 = py.font.SysFont('e : play_to_learn by step2', 25)
    img5 = font5.render('e : play_to_learn by step2', True, blackColor)
    windowSurface.blit(img5, (12, 310)) 
    """

    windowSurface.blit(arialFontFPS.render(f"{int(clock.get_fps())} FPS", True, blueColor), [5, 5])
    py.display.flip()

    clock.tick(FPS)