#

import random, time, os, sys, pygame
RX = 3
RY = 8

pygame.init()
ROZMIAR = 800,600
pygame.display.set_caption("The Royal Game of Ur")
ekran = pygame.display.set_mode(ROZMIAR)
zegar = pygame.time.Clock()
biały = pygame.color.THECOLORS['white']
czerwony = pygame.color.THECOLORS['red']
czarny = pygame.color.THECOLORS['black']
złoty = pygame.color.THECOLORS['gold']
myfont = pygame.font.SysFont("monospace", 27)

tło = "tlo.jpg"
cel =  "cel.png"
wla = "zapal.png"
wyl = "zgas.png" #wyl = "zgasz.png"
brak = "brak.png"
blok = "blok.png"
siat = 64 #siatka
borx = 368 #ramka x (od lewej)
bory = 32 #ramka y (od góry)
vol = 0.8

n=7

class Token(): # żetony
  def __init__(self,gracz):
    self.id = id(self)
    self.x = 0
    self.y = 0
    self.tx = 0
    self.ty = 0
    self.pos = -1
    self.gracz = gracz

class Gra():
  def __init__(self):

    self.row1 = []
    self.row2 = []
    self.tokeny=[]
    for i in range(n):
      t = Token(1)
      self.row1.append(t)
      self.tokeny.append(t)
      t = Token(2)
      self.tokeny.append(t)
      self.row2.append(t)
    self.f = 0

  def zwiad(self,token,d):
    pos = token.pos + d

    otok=[elem for i,elem in enumerate(self.tokeny) if elem.pos == pos]
    if len(otok) == 0:
      otok = None
    else: otok=otok[0]
    
    return otok

  def widok(self,d,idt=None):
    pos = token.pos + d

  def ruch(self):
    pass

  def maluj(self): #graphics
    for i in range(8):
      if(3<i<6): k=0;l=1;
      else: k=-1;l=2;
      for j in range(k,l):
        pygame.draw.rect(ekran,biały,(borx+j*siat,bory+i*siat,siat-1,siat-1))


    pygame.display.flip()
    
    




g=Gra()
g.maluj()

#todo
#MENU

#DUEL
#AI
#OPT
#EXT
