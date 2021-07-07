import pygame
import random

# Z turnleft X turnright C hold SPACE harddrop DOWN softdrop 
# LEFT RIGHT move ESC pause

# colors of diffrent type of pieces
piece_colors={
        'I':(178,34,34),
        'J':(255,215,0),
        'L':(128,0,128),
        'O':(0,0,139),
        'S':(50,205,50),
        'T':(139,69,19),
        'Z':(0,139,139)
        }

# diffrent type of bodies of pieces (in a 4x4 block)
piece_bodies={  
        'I':[[(1,0),(1,1),(1,2),(1,3)],[(0,1),(1,1),(2,1),(3,1)],[(2,0),(2,1),(2,2),(2,3)],[(0,2),(1,2),(2,2),(3,2)]],
        'J':[[(0,2),(1,0),(1,1),(1,2)],[(0,0),(0,1),(1,1),(2,1)],[(0,0),(0,1),(0,2),(1,0)],[(0,0),(1,0),(2,0),(2,1)]],
        'L':[[(0,0),(0,1),(0,2),(1,2)],[(0,0),(0,1),(1,0),(2,0)],[(0,0),(1,0),(1,1),(1,2)],[(0,1),(1,1),(2,0),(2,1)]],
        'O':[[(0,0),(0,1),(1,0),(1,1)]],
        'S':[[(0,0),(0,1),(1,1),(1,2)],[(0,1),(1,0),(1,1),(2,0)]],
        'T':[[(0,0),(0,1),(0,2),(1,1)],[(0,0),(1,0),(1,1),(2,0)],[(0,1),(1,0),(1,1),(1,2)],[(0,1),(1,0),(1,1),(2,1)]],
        'Z':[[(0,1),(0,2),(1,0),(1,1)],[(0,0),(1,0),(1,1),(2,1)]]
        }

def main():
    pygame.init()
    scr=pygame.display.set_mode((450,600))
    pygame.display.set_caption('tetris')
    fps=59
    fc=pygame.time.Clock()
    t=0  # time counting, will be added in every loop
    game=Tetris(scr)
    timetemp=0 # help recording time
    tq=True
    pygame.key.set_repeat(200,50)
    while tq:
        for event in pygame.event.get(): # check events
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_z:
                    game.current_piece.spin(1,game)
                elif event.key==pygame.K_x:
                    game.current_piece.spin(0,game)
                elif event.key==pygame.K_LEFT:
                    game.current_piece.move(-1,0,game)
                elif event.key==pygame.K_RIGHT:
                    game.current_piece.move(1,0,game)
                elif event.key==pygame.K_SPACE:
                    game.current_piece.hardDrop(game)
                elif event.key==pygame.K_DOWN:
                    game.current_piece.move(0,1,game)
                elif event.key==pygame.K_c and not game.pause and not game.lost:
                    game.holding()
                elif event.key==pygame.K_ESCAPE:
                    if game.current_piece.activated: # if haven't paused
                        game.current_piece.activated=False
                        game.pause=True
                    else:                            # if already paused
                        game.current_piece.activated=True
                        game.pause=False
                elif game.pause or game.lost:        # main menu
                    if event.key==pygame.K_c:        # continue
                        game.current_piece.activated=True
                        game.pause=False
                    elif event.key==pygame.K_r:      # retry
                        tq=False
                    elif event.key==pygame.K_q:      # quit
                        pygame.quit()
                    
        scr.fill((255,255,255))
        draw_ui(scr,game)                            # draw background
        drawText(scr,'time: '+str('{:.2f}'.format(t/fps)),10,10,15) # time
        #if game.timeset:        # to move the piece down every dropspeed
        #    timetemp=t
        #    game.timeset=False
        if t-timetemp==int(fps*game.dropspeed) and not game.lost:
            timetemp=t
            game.current_piece.move(0,1,game)            
        game.drawme()           # draw the blocks and the pieces
        if not game.lost:       # draw the current piece when is still alive
            game.current_piece.drawme()
        game.next.drawme()      # draw the next piece
        if game.hold!=None:     # draw the holded piece(if there is one)
            game.hold.drawme()  
        if game.lost:
            gameover(scr,game)  # draw 'GAMEOVER' when lost
        fc.tick(fps)
        if game.lost==False and game.pause==False:  # time past
            t+=1
        if game.pause or game.lost:           # draw menu when paused or lost      
            if game.pause: 
                drawText(scr,'PAUSED',130,140,40,(255,0,0))
                drawText(scr,'(C)ontinue',130,300,30,(255,255,255),(0,0,0))
            drawText(scr,'(R)etry',155,350,30,(255,255,255),(0,0,0))
            drawText(scr,'(Q)uit',165,400,30,(255,255,255),(0,0,0))
        pygame.display.flip()

def gameover(scr,game):     # draw game over and score
    drawText(scr,'GAME OVER',130,140,40,(255,0,0))
    drawText(scr,'SCORE: '+str(game.exp),130,200,30,(255,0,0))

def drawText(self,text,posx,posy,textHeight,fontColor=(0,0,0),backgroudColor=None):
    fontObj = pygame.font.Font('game.ttf', textHeight)
    textSurfaceObj = fontObj.render(text,True,fontColor,backgroudColor)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.left = posx
    textRectObj.top = posy
    self.blit(textSurfaceObj, textRectObj)

def draw_ui(scr,game):  # draw background
    pygame.draw.rect(scr,(0,0,0),((0,0),(300,50)))  # score&time box4
    pygame.draw.rect(scr,(255,255,255),((5,5),(295,40)))
    pygame.draw.rect(scr,(0,0,0),((300,0),(5,600))) # right frame of the well
    pygame.draw.rect(scr,(0,0,0),((305,2),(143,180)),5) # next piece box
    pygame.draw.rect(scr,(0,0,0),((305,182),(143,180)),5) # holding box
    drawText(scr,'score: '+str(game.exp),100,10,15)
    drawText(scr,'level: '+str(game.level),200,10,15)
    drawText(scr,'Next',350,5,30,(0,0,255))
    drawText(scr,'Hold',350,185,30,(0,0,255))
    for i in range(11):   # draw grid
        pygame.draw.rect(scr,(200,200,200),(((i+1)*25,50),(2,550)))
    for i in range(21):
        pygame.draw.rect(scr,(200,200,200),((0,(i+1)*25+50),(300,2)))
    if game.combo>=1:     # show combo when needed
        drawText(scr,str(game.combo)+' COMBO!!!',130,140,40,(255,0,0))
    
class Block():  # a single block
    def __init__(self,scr,color,x,y):
        self.scr=scr
        self.color=color
        self.x=x
        self.y=y
    def drawme(self):
        pygame.draw.rect(self.scr,self.color,((self.x*25,self.y*25+50),(25,25)))
        pygame.draw.rect(self.scr,(0,0,0),((self.x*25,self.y*25+50),(25,25)),1)
        
class Piece():  # one piece (((???)))
    def __init__(self,scr,pt,x=0,y=0):
        self.activated=False  # not 'dead' yet
        self.scr=scr
        self.x=x
        self.y=y
        self.type=pt
        self.spintype=random.randint(0,3)
        try: # if the number is too much (some pieces have only 2 or 1 spintypes)
            self.bodyxy=piece_bodies[pt][self.spintype]
        except:       # change it to the first spintype
            self.bodyxy=piece_bodies[pt][0]
            self.spintype=0
        self.color=piece_colors[pt]
        self.body=[]  # blocks which it contains
        for bp in self.bodyxy:
            self.body.append(Block(self.scr,self.color,bp[0]+self.x,bp[1]+self.y))
    def update(self):   # update its body after moved or spined
        self.body.clear()
        try:
            self.bodyxy=piece_bodies[self.type][self.spintype]
        except:
            self.bodyxy=piece_bodies[self.type][0]
            self.spintype=0
        for bp in self.bodyxy:
            self.body.append(Block(self.scr,self.color,bp[0]+self.x,bp[1]+self.y))
    def spin(self,dire,game): # 0 right 1 left
        if self.activated==False:
            return
        # make a same piece to check if it will collide after it spined
        coltest=Piece(game.scr,self.type,self.x,self.y) 
        coltest.spintype=self.spintype
        if dire:
            coltest.spintype-=1
        else:
            coltest.spintype+=1
        if coltest.spintype<0:
            coltest.spintype=len(piece_bodies[coltest.type])-1
        elif coltest.spintype>len(piece_bodies[coltest.type])-1:
            coltest.spintype=0
        coltest.update() 
        for part in coltest.body:   # check if it collided
            for block in game.body:
                if part.x==block.x and part.y==block.y:
                    del coltest    # if so, delete it and return
                    return
        if dire:
            self.spintype-=1 # spin right
        else:
            self.spintype+=1 # spin left
        if self.spintype<0:
            self.spintype=len(piece_bodies[self.type])-1
        elif self.spintype>len(piece_bodies[self.type])-1:
            self.spintype=0
        self.update()
        self.checkWallCollision(game)  # check if it's out of the wall
    def move(self,xp,yp,game,chk=True):
        if self.activated==False or game.lost:
            return
        for block in game.body:
            for part in self.body:
                if xp==1 and yp==0:   # if moved right,check collision
                    if part.x+1==block.x and part.y==block.y:
                        return
                elif xp==-1 and yp==0 and part.y==block.y: # if moved left
                    if part.x-1==block.x:
                        return
                if xp==0 and yp==1: # if moved down (you could never move up)
                    if part.x==block.x and part.y+1==block.y:
                        self.activated==False # if you can't move down
                        game.add_new_piece() # means change another piece
                        return
        self.x+=xp
        self.y+=yp
        self.update()
        if chk:  # prevent endless loop
            self.checkWallCollision(game)
    def drawme(self): 
        for part in self.body:
            part.drawme()
    def checkWallCollision(self,game): # check if it's out of the wall
        if self.activated==False:
            return
        for bxyp in self.body: # move it back
            if bxyp.x<0:
                self.move(0-bxyp.x,0,game,False)
            if bxyp.x>11:
                self.move(11-bxyp.x,0,game,False)
            if bxyp.y<0:
                self.move(0,0-bxyp.y,game,False)
            if bxyp.y>21:   # if collided the ground
                self.move(0,21-bxyp.y,game,False)
                game.add_new_piece()  # change to the next piece
    def hardDrop(self,game): # harddrop: to drop it immediately
        if not self.activated:
            return
        droprange=22
        if game.body==[]: # if there's nothing
            for part in self.body:  
                if droprange>21-part.y: # check which block is nearest to the ground
                    droprange=21-part.y
        for block in game.body: 
            for part in self.body:
                if block.x==part.x: # check if there's something in the same column
                    a=block.y-part.y-1 # and check which range is the smallest
                    if droprange>a and a>=0:
                        droprange=a
                else:               # if nothing's in that column
                    if droprange>21-part.y: # check which is nearest to the ground
                        droprange=21-part.y
        self.move(0,droprange,game) # move there
            
class Tetris(): # game
    def __init__(self,scr):
        self.scr=scr
        self.pause=False
        self.exp=0
        self.lost=False
        self.level=1
        self.current_piece=Piece(self.scr,random.choice(['I','J','L','O','S','Z','T']),5,0)
        self.current_piece.activated=True
        self.body=[] # all blocks (except current piece)
        self.next=Piece(self.scr,random.choice(['I','J','L','O','S','Z','T']),14,0)
        #self.timeset=False  # 
        self.dropspeed=1.0 # (sec)
        self.combo=False  
        self.holded=False  # (this round)
        self.hold=None
    def add_new_piece(self):  # when a block touches the floor, add a new piece
        if self.lost:
            return
        self.exp+=5  # jy+5 (?
        self.level=int(self.exp/1500)+1  # update level and speed
        self.dropspeed=1.0*(0.9)**self.level 
        self.current_piece.activated=False  # shut down current_piece
        for i in self.current_piece.body:  # add all blocks into game.body
            self.body.append(i)
        self.chkAndDeleteRow()      # remove full rows
        self.current_piece=Piece(self.scr,self.next.type,5,0) # add next piece
        for block in self.body:  # check if lost
            if block.x==self.current_piece.x and block.y==self.current_piece.y:
                self.lost=True
                self.current_piece==None
                return
        self.current_piece.activated=True  # activate current_piece,make next piece
        self.next=Piece(self.scr,random.choice(['I','J','L','O','S','Z','T']),14,0)
        #self.timeset=True
        self.holded=False  # now can hold another one
    def chkAndDeleteRow(self): # check if a row is full of blocks
        combo=False
        for i in range(22):  # check every row
            cnt,ta,newbody=0,[],[]
            for j in range(len(self.body)):  
                if self.body[j].y==i:
                    cnt+=1
                    ta.append(j)
            if cnt==12:         # if this row has 12 blocks,don't add them to the new body
                for k in range(len(self.body)):
                    if k not in ta:
                        newbody.append(self.body[k])
                for newblock in newbody:  # make other rows above this row drop
                    if newblock.y<i:
                        newblock.y+=1
                self.exp+=100  # jy+100 (da shui B ((((
                self.level=int(self.exp/1500)+1  # update level&speed
                self.dropspeed=1.0*(0.9)**self.level
                if self.combo>=1:  # get bonus if got combo
                    self.exp+=50*self.combo
                self.body=newbody
                self.combo+=1
                combo=True
        if not combo:  # nothing happend, shut down! (
            self.combo=-1
    def drawme(self):
        for block in self.body:
            block.drawme()
    def holding(self):
        if self.lost or self.holded:
            return
        p=self.hold  # temp
        self.hold=Piece(self.scr,self.current_piece.type,14,7)  # move current piece to holding piece
        self.hold.update() 
        self.hold.activated=False  # stop it(
        if p != None:  # if there was another piece holded
            self.current_piece=p  # move that to current piece
            self.current_piece.activated=True
            self.current_piece.x=5
            self.current_piece.y=0
            self.current_piece.update()
        else:          # haven't holded yet
            self.current_piece=Piece(self.scr,self.next.type,5,0) # put next
            for block in self.body:  # check lost
                if block.x==self.current_piece.x and block.y==self.current_piece.y:
                    self.lost=True
                    self.current_piece==None
                    return
            self.current_piece.activated=True
            self.next=Piece(self.scr,random.choice(['I','J','L','O','S','Z','T']),14,0)
            #self.timeset=True
        
        self.holded=True  # this round you cannot hold another piece.
        
if __name__=='__main__':
    while True:     # loop to retry
        main()