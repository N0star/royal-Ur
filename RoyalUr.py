# FDC # Royal Game of Ur # 0.2.0

import random, time, math, os, sys, pygame
RX = 3; RY = 8

pygame.init()
ROZMIAR = 800,600
pygame.display.set_caption("The Royal Game of Ur")
ekran = pygame.display.set_mode(ROZMIAR)
zegar = pygame.time.Clock()

biały = pygame.color.THECOLORS['white']
czerwony = pygame.color.THECOLORS['red']
czarny = pygame.color.THECOLORS['black']
niebieski = pygame.color.THECOLORS['blue']
zielony = pygame.color.THECOLORS['green']
złoty = pygame.color.THECOLORS['gold']

eresh = pygame.color.Color(0xd9,0xc2,0x52)
ishta = pygame.color.Color(0xad,0x15,0x2e)
ivory = pygame.color.Color(0xf0,0xf0,0xef)
myfont = pygame.font.SysFont("monospace", 16)
mxfont = pygame.font.SysFont("monospace", 32)

tło = "tlo.jpg"; brak = "brak.png"
siat = 64 #siatka
borx = 368 #ramka x (od lewej)
bory = 32 #ramka y (od góry)
vol = 0.8; n=7

##############################################################DEF&CLASS####

def octogram(screen,color,x,y,a):
  pygame.draw.polygon(screen,color,((x-a,y-a),(x+a,y-a),(x+a,y+a),(x-a,y+a)))
  a=a*1.4142
  pygame.draw.polygon(screen,color,((x,y-a),(x-a,y),(x,y+a),(x+a,y)))

def impc(i,cxy,rad,v,t,rev=False): #i-number moving points on a circle!
  full=5000; t=int(v*t); t=t%full
  points = []
  cx=cxy[0]; cy=cxy[1];
  for _ in range(i):
    x = rad*math.cos(t) + cx;
    y = rad*math.sin(t) + cy;
    t=t+full//i; t=t%full
    points.append((x,y))
  return points

def board():
  ekran.fill(czarny)
  for i in range(8): #gameboard
    if(3<i<6): k=0;l=1;
    else: k=-1;l=2;
    for j in range(k,l):
      pygame.draw.rect(ekran,ivory,(borx+j*siat,bory+i*siat,siat-1,siat-1))
  for i in range(0,7,3):
    if(i==3): k=0;l=2;
    else: k=-1;l=2;
    for j in range(k,l,2):
      octogram(ekran,czarny,borx+j*siat+32,bory+i*siat+32,siat//4)

class Main():
  def __init__(self):
    self.run = 1
    self.mod = 'menu'

  def mcheck(self,x,y):
    self.mod = 'game_init'

  def maluj(self):
    board()

    label = myfont.render("Click anywhere to start", 7, biały)
    ekran.blit(label, (borx-siat-14, bory+siat*8+10))
    pygame.display.flip()

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
      delta = 0;
      if(self.ty<self.y):
          self.y=self.y-self.delta(self.y,self.ty,v)
          delta=1
      elif(self.ty>self.y):
          self.y=self.y+self.delta(self.ty,self.y,v)
          delta=1
      if(self.tx<self.x):
          self.x=self.x-self.delta(self.x,self.tx,v)
          delta=1
      elif(self.tx>self.x):
          self.x=self.x+self.delta(self.tx,self.x,v)
          delta=1
      return delta

  def delta(self,k,l,d):
        return (((k-l)//d)+((k-l)%10>0))

  def maluj(self):
    shft=10; bor = 32#20
    if self.gracz==1: kolor=ishta
    elif self.gracz==2: kolor=eresh
    #pygame.draw.rect(ekran,kolor,(self.x+bor,self.y,siat-bor,siat-bor))
    pygame.draw.circle(ekran, kolor, (self.x+bor+shft,self.y+bor), bor-shft)

class dice():
  def __init__(self):
    self.tetr = []
    self.d = -1
    for i in range(4):
      tetr = False
      self.tetr.append(tetr)

  def losuj(self):
    d=0
    for i in range(4):
      self.tetr[i]=random.choice((False,True))
      if(self.tetr[i] is True): d+=1;
    self.d=d
    return d

  def maluj(self,gracz): 
    y=bory+siat*8; delx=2*siat; centr=borx+siat//2
    if(self.d>=0):
      for i in range(4):
        if(i<2): j=1
        else: j=-1
        x=centr+(delx+i%2*siat)*j; kolor=biały;
        pygame.draw.polygon(ekran,kolor,((x,y),(x-10,y+20),(x+10,y+20)))
        if(self.tetr[i] is True):
          if(j>0): kolor=czarny#ishta
          else: kolor=czarny#eresh
          pygame.draw.polygon(ekran,kolor,((x,y),(x-3,y+20),(x+3,y+20)))

    y=bory+siat*5; gracz+=1; w=15 #player pointers
    if(gracz==1): kolor=ishta
    else: kolor = eresh; w=-w;
    for i in range(-1,3,2):
      x=centr+siat*i
      pygame.draw.polygon(ekran,kolor,((x+w,y+20),(x-w,y+30),(x+w,y+40)))

    if(self.d<0):
      if(gracz==1):
        label = myfont.render("Throw for Inanna", 5, ishta); er=-10
      else:
        label = myfont.render("Throw for Ereshkigal", 5, eresh); er=7
      #ekran.blit(label, (centr, bory+siat*8))
    else:
      label = myfont.render("Go for... "+str(int(self.d)), 5, biały); er=-24
    ekran.blit(label, (centr-siat-siat//2-er, bory+siat*8+10))
      
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
    self.pos()
    self.d=dice()
    self.tura=0
    self.win1=0
    self.win2=0
    self.efekty = []
    
    self.dice = Efekt('dice',0,0)
    self.efekty.append(self.dice)

  def pos(self):
    x=64*3; y=bory+64; centr=borx-siat//6
    for i in range(n):
      if(i<len(self.row1)):
        self.row1[i].tx=centr-x
        self.row1[i].ty=y+i*49
      if(i<len(self.row2)):
        self.row2[i].tx=centr+x
        self.row2[i].ty=y+i*49

  def col(self,mx):
    x=64*3; centr=borx-siat//6; mx=mx-20;
    if(mx>centr-x and mx<centr-x+siat-20): return 1
    elif(mx>centr+x and mx<centr+x+siat-20): return 2
    else: return 0

  def row(self,my):
    y=bory+64;
    for i in range(n):
      if(my>y+i*49 and my<y+(i+1)*49): return i
    return 99 #def beyond the list

  def field(self,mx,my):
    x=64*3; y=bory+64; centr=borx-siat//6; my=my-siat//2#mx=mx-20;
    if(mx>borx-siat and mx<centr+siat+siat):
      if(y>bory):
        if(mx<borx): x=-1
        elif(mx>borx+siat): x=1
        else: x=0
        
        for i in range(8):
          if(my<siat*(i+1)):
            y=i; break;
        if(y>64): return None

        if(x==0):
          pos=y+4
        else:
          pos=3-y
          if(pos<0):
            pos=19-y

        tok=[elem for i,elem in enumerate(self.tokeny) if elem.pos == pos]
        if len(tok) > 0:
          if(len(tok)>1):
             gracz=(x+3)//2
             if(x==0): return None #that shouldn't happen btw.!!
             tok=[elem for i,elem in enumerate(tok) if elem.gracz == gracz]
          return tok[0]
        else: pass
      return None       

  def koryguj(self,v=10):
    a=0
    for i in range(len(self.tokeny)):
      a+=self.tokeny[i].correct(v)
    for i in range(len(self.efekty)-1,-1,-1):
      if(self.efekty[i].timer<=0):
        if(self.efekty[i].gen!='dice'): del(self.efekty[i])
    return a

  def zwiad(self,token,d,inner=None):
    if(inner is not None):
      otok=[elem for i,elem in enumerate(self.tokeny) if elem.pos == 7]
      if(len(otok) == 0):
        return False
      else: return True
        
    pos = token.pos + d
    if pos > 14: return -1
    elif pos==14: return None
    else: pass

    otok=[elem for i,elem in enumerate(self.tokeny) if elem.pos == pos]
    if len(otok) == 0:
      otok = None
    elif otok[0].gracz==token.gracz or len(otok)>1:
      otok = -1
    elif pos!=7: otok=otok[0]
    else: otok=self.zwiad(token,d+1)
    
    return otok

  def widok(self,token,d,idt=None):
    print('widok',d,idt)
    pos = token.pos + d
    gen = ''

    if(pos==7 and self.zwiad(token,d,'inner') is True and idt!=-1): pos+=1;
    if(pos==14): gen='win'
    elif(idt is None or ((pos<4 or pos>11)and idt!=-1)):
      if(pos==3 or pos==13): gen='extr'
      elif(pos==7 and self.zwiad(token,d,'inner') is not True): gen='sankt'
      else: gen='move'
    elif(idt==-1):
      gen = 'stop'
      if(pos>14): pos=14
    else: gen='war'

    x,y=self.pos_pix(pos,token.gracz)
    print(x,y,gen)
    e = Efekt(gen,x,y)
    self.efekty.append(e)
    
  def pos_pix(self,pos,gracz):
    x=64*3; y=bory+64; centr=borx-siat//6
    print(pos)
    if (pos<4 or pos>11) :
      if gracz==1 : tx=-1
      elif gracz==2 : tx=1
      tx=centr+siat*tx
      if(pos<4): ty=y+siat*(2-pos)
      else: ty=y+siat*(18-pos)
    else:
      tx=centr
      ty=y+siat*(pos-5)
    return tx,ty

  def ruch(self,token,d):
    while(token.x!=token.tx or token.ty!=token.y):
      token.correct()
      #self.koryguj()
      self.maluj()
    if(d==0): return
    time.sleep(0.1)
    
    x=64*3; y=bory+64; centr=borx-siat//6
    pos = token.pos + 1
    print(pos)
    if (pos<4 or pos>11) :
      if token.gracz==1 : tx=-1
      elif token.gracz==2 : tx=1
      tx=centr+siat*tx
      if(pos<4): ty=y+siat*(2-pos)
      else: ty=y+siat*(18-pos)
    else:
      tx=centr
      ty=y+siat*(pos-5)
      
    token.tx=tx
    token.ty=ty
    token.pos=pos
    self.ruch(token,d-1)

  def init_ruch(self,token,d,otok=None,war=False):
    print(otok)
    npos=token.pos+d
    if(npos==7): #jump over the sactuary?
      if(self.zwiad(token,d,'yes')): d+=1;
    if(otok is not None):
      if(otok.pos==npos and 3<npos<12): war=True
    print(war)
    if(war==True and otok.gracz==1): self.zbij(otok)
    self.ruch(token,d)
    if(war==True and otok.gracz==2): self.zbij(otok)

  def zbij(self,token):
    token.pos=-1
    if(token.gracz==1): self.row1.append(token)
    if(token.gracz==2): self.row2.append(token)
    self.pos()

  def remove(self,token):
    if(token.gracz==1):
      inx=[i for i,elem in enumerate(self.row1) if elem.id == token.id]
      del self.row1[inx[0]]
    else:
      inx=[i for i,elem in enumerate(self.row2) if elem.id == token.id]
      del self.row2[inx[0]]
    self.pos()

  def end(self,token=None):
    self.d.d=-1
    if(token is not None):
      if(token.pos!=3 and token.pos!=7 and token.pos!=13):
        self.tura=(self.tura+1)%2
      elif(token==7):
        pass
    else: self.tura=(self.tura+1)%2
    self.dice.up=(self.dice.up+1)%2

  def losuj(self):
    d=self.d.losuj()
    return d

  def sign(self,case):
    if   case==0: pass #zero throw
    elif case==1: pass #no moves
    elif case==2: pass #extra turn
    elif case==3: pass #sanctuary
    elif case==4: pass #finish
    elif case==5: pass #fight

  def win(self,delta):
    if delta == 0:
      for i in range(len(self.tokeny)-1,-1,-1):
        if self.tokeny[i].pos==14:
          if(self.tokeny[i].gracz==1): self.win1+=1
          else: self.win2=self.win2+1
          del(self.tokeny[i])

    if(self.win2==n):
      b="Ereshkigal"; kolor=eresh; er=200; print(b)
    elif(self.win1==n):
      b="Inanna"; kolor=ishta; er=169; print(b)
    else: return 0;

    (x,y)=ROZMIAR
    ekran.fill(kolor)
    octogram(ekran,czarny,x//2,y//2,256)
    label = mxfont.render("Glory to "+b+"!!", 32, kolor)
    ekran.blit(label, (x//2-er,y//2))
    pygame.display.flip()
    time.sleep(3); return 1;

  def maluj(self): #graphics
    ekran.fill(czarny)
    for i in range(8): #gameboard
      if(3<i<6): k=0;l=1;
      else: k=-1;l=2;
      for j in range(k,l):
        pygame.draw.rect(ekran,ivory,(borx+j*siat,bory+i*siat,siat-1,siat-1))

    for i in range(0,7,3):
      if(i==3): k=0;l=2;
      else: k=-1;l=2;
      for j in range(k,l,2):
        octogram(ekran,czarny,borx+j*siat+32,bory+i*siat+32,siat//4)

    for i in range(len(self.tokeny)):
      self.tokeny[i].maluj() #tokens
    self.d.maluj(self.tura) #dices

    for i in range(len(self.efekty)):
      self.efekty[i].maluj() #effects
    pygame.display.flip()

class Efekt():
  def __init__(self,gen,x=ROZMIAR[0]//2,y=ROZMIAR[1]//2):
    self.id=id(self)
    self.x = x+siat//2+siat//8+2
    self.y = y+siat//2
    self.gen=gen
    self.up = 1
    self.flash = 0

    if(gen=='stop' or gen=='move'):
      self.timer=900; self.flash=200;
    elif(gen=='dice'): self.timer=3
    else: self.timer=900; self.flash=200;

  def maluj(self):
    x=self.x; y=self.y
    self.timer-=1
    if(self.flash>0):
      if(self.timer%self.flash==0): self.up+=1; self.up=self.up%2
    if(self.up):
      if(self.gen=='stop'):
        x+=3; pygame.draw.circle(ekran,czerwony,(x,y),13)
        pygame.draw.rect(ekran,biały,(x-10,y-4,19,7))
      elif(self.gen=='move'):
        pygame.draw.polygon(ekran,zielony,((x,y+3),(x+7,y-20),(x-7,y-20)))
      elif(self.gen=='extr'):
        octogram(ekran,niebieski,x,y,10)
        pygame.draw.polygon(ekran,zielony,((x,y),(x+7,y-20),(x-7,y-20)))
        #pygame.draw.polygon(ekran,zielony,((x,y),(x+10,y-20),(x-10,y-20)))
        #pygame.draw.polygon(ekran,niebieski,((x,y-10),(x+10,y-30),(x-10,y-30)))
      elif(self.gen=='war'):
        pygame.draw.polygon(ekran,czerwony,((x,y),(x+7,y-20),(x-7,y-20)))
        pygame.draw.polygon(ekran,czerwony,((x,y-10),(x+7,y-30),(x-7,y-30)))
      elif(self.gen=='sankt'):
        octogram(ekran,czerwony,x,y,13)
        pygame.draw.polygon(ekran,zielony,((x,y),(x+7,y-20),(x-7,y-20)))
        #pygame.draw.polygon(ekran,niebieski,((x,y-10),(x+10,y-30),(x-10,y-30)))
      elif(self.gen=='win'):
        octogram(ekran,czerwony,x,y,13)
      elif(self.gen=='dice'):
        self.timer+=2
        p0 = impc(4,(x,y),32,0.013,self.timer)
        for i in range(len(p0)):
          xys= impc(3,p0[i],14,0.02,self.timer)
          pygame.draw.polygon(ekran,czarny,xys)
          xys= impc(3,p0[i],12,0.02,self.timer)
          pygame.draw.polygon(ekran,biały,xys)

###################################################################MAIN#######

main = Main(); mbr=0;
while main.run:
  for zdarzenie in pygame.event.get():
      if zdarzenie.type == pygame.QUIT:
        pygame.display.quit()
        pygame.quit()
        sys.exit()
        
  (x,y)=pygame.mouse.get_pos()
  m=pygame.mouse.get_pressed()

  if main.mod=='menu':
    main.maluj()

    if(m==(0,0,0)): mbr=0;  
    if(mbr==0):
      if(m[0]==True):
        main.mcheck(x,y)
        mbr=1

  if main.mod=='game_init':      
    g=Gra(); d=-1
    main.mod='game'
  if main.mod=='game':
    
    g.maluj()
    a=g.koryguj()

    g.dice.x,g.dice.y=(x,y)
    if(m==(0,0,0)): mbr=0;  
    if(mbr==0):
        if(m[0]==True or m[2]==True):
          #print(x,y)
          if(d<0): #time to throw a dice!
            g.dice.up=(g.dice.up+1)%2
            d=g.losuj()
            print(d)
            if(d==0): d=-1; g.sign(0); g.end() #if 0 is rolled
            else:               #if there's no move to perform
              b=d; d=-1;
              for i in range(len(g.tokeny)):
                if(g.tokeny[i].gracz==g.tura+1):
                  a=g.zwiad(g.tokeny[i],b)
                  if(a!=-1): d=b; break;
              if(d<0): g.sign(1); g.end()
              
          else: #time to select a champion!
            if(g.col(x)==1 and g.tura==0): #from column 1
              tok=g.row(y)
              if(tok<len(g.row1)):
                print(tok," 1")
                tok=g.row1[tok]
                target=g.zwiad(tok,d)
                if(m[2]):
                    g.widok(tok,d,target)
                elif(target is not -1):
                  g.remove(tok)
                  g.init_ruch(tok,d)
                  d=-1
                  g.end(tok)

            elif(g.col(x)==2 and g.tura==1): #from column 2
              tok=g.row(y)
              if(tok<len(g.row2)):
                print(tok,"2")
                tok=g.row2[tok]
                target=g.zwiad(tok,d)
                if(m[2]):
                    g.widok(tok,d,target)
                elif(target is not -1):
                  g.remove(tok)
                  g.init_ruch(tok,d)
                  d=-1
                  g.end(tok)

            else:                           #from the board
              tok=g.field(x,y)
              if tok is not None:
                if(tok.gracz==g.tura+1):
                  target=g.zwiad(tok,d)
                  if(m[2]):
                    g.widok(tok,d,target)
                  elif(target is not -1):
                    g.init_ruch(tok,d,target)
                    d=-1
                    g.end(tok)
                    
          mbr=1
    if(g.win(a)): main.mod='menu';
        

#todo
#SOUND
#MESSAGES
#AI #OPT #EXT
