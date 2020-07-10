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

  def correct(self,v=10): #KORYGOWANIE (XY)
      if(self.ty<self.y):
          self.y=self.y-self.delta(self.y,self.ty,v)
      elif(self.ty>self.y):
          self.y=self.y+self.delta(self.ty,self.y,v)
      if(self.tx<self.x):
          self.x=self.x-self.delta(self.x,self.tx,v)
      if(self.tx>self.x):
          self.x=self.x+self.delta(self.tx,self.x,v)

  def delta(self,k,l,d):
        return (((k-l)//d)+((k-l)%10>0))

  def maluj(self):
    bor = 20
    if self.gracz==1: kolor=czerwony
    elif self.gracz==2: kolor=złoty
    pygame.draw.rect(ekran,kolor,(self.x+bor,self.y,siat-bor,siat-bor))
    

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

    x=64*3; y=bory+64; centr=borx-siat//6
    for i in range(n):
      self.row1[i].tx=centr-x
      self.row1[i].ty=y+i*49
      self.row2[i].tx=centr+x
      self.row2[i].ty=y+i*49

  def col(self,mx):
    x=64*3; y=bory+64; centr=borx-siat//6; mx=mx-20;
    if(mx>centr-x and mx<centr-x+siat-20): return 1
    elif(mx>centr+x and mx<centr+x+siat-20): return 2
    else: return 0

  def row(self,my):
    y=bory+64;
    for i in range(n):
      if(my>y+i*49 and my<y+(i+1)*49): return i
    return 99 #def beyond the list

  def koryguj(self):
    for i in range(len(self.tokeny)):
      self.tokeny[i].correct()

  def zwiad(self,token,d):
    pos = token.pos + d
    if pos > 14: return -1
    elif pos==14: return None
    else: pass

    otok=[elem for i,elem in enumerate(self.tokeny) if elem.pos == pos]
    if len(otok) == 0:
      otok = None
    elif orok[0].gracz==token.gracz:
      otok = -1
    else: otok=otok[0]
    
    return otok

  def widok(self,d,idt=None):
    pos = token.pos + d

  def ruch(self,d):
    pass

  def maluj(self): #graphics
    ekran.fill(czarny)
    for i in range(8):
      if(3<i<6): k=0;l=1;
      else: k=-1;l=2;
      for j in range(k,l):
        pygame.draw.rect(ekran,biały,(borx+j*siat,bory+i*siat,siat-1,siat-1))

    for i in range(len(self.tokeny)):
      self.tokeny[i].maluj()

    pygame.display.flip()
    
    


mbr=0
g=Gra()
while True:
  for zdarzenie in pygame.event.get():
      if zdarzenie.type == pygame.QUIT:
        pygame.display.quit()
        pygame.quit()
        sys.exit()
  
  g.maluj()
  g.koryguj()
  
  m=pygame.mouse.get_pressed()
  if(m==(0,0,0)): mbr=0;  
  if(mbr==0):
      (x,y)=pygame.mouse.get_pos()
      if(m[0]==True or m[1]==True):
        #print(x,y)
        if(g.col(x)==1):
          tok=g.row(y)
          if(tok<len(g.row1)):
            print(tok," 1")
            tok=g.row1[tok]
            g.zwiad(tok,1)

        elif(g.col(x)==2):
          tok=g.row(y)
          if(tok<len(g.row2)):
            print(tok,"2")
            tok=g.row2[tok]
            g.zwiad(tok,1)
        
        mbr=1
        

#todo
#MENU

#DUEL
#AI
#OPT
#EXT