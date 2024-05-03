from Tkinter import *
from random import *
from math import*

# Variable globales 
CANVAS_HEIGHT, CANVAS_WIDTH = 500, 700

canvasHeight=500
canvasWidth=750

listeParticules=[]
Ec=0
nbrParticules=0
P=0#nrT
flag=1

nbrLabel = None
EcLabel = None
reservoir = None

# FONCTIONS

def distanceAuCarre(xA,yA,xB,yB):
    d=(xA-xB)**2+(yA-yB)**2
    return d

def calculerEnergieCinetique():
    global Ec
    if flag==1:
        Ec=0
        for p in listeParticules :
            Ec+=0.5*p[4]*(p[2]**2+p[3]**2)
    if flag==0 :
        Ec=0
    return Ec

def creerParticuleValide():
    
# Creation
    
    global nbrParticules,flag
    flag=1
    size=1.*randint(15,55)
    mass=size
    dX,dY=1.*randint(-3,3),1.*randint(-3,3)
    coordx=1.*randint(0+size,canvasWidth-size)
    coordy=1.*randint(0+size,canvasHeight-size)
    color=choice(['Red','Orange','Yellow','Green','Cyan','Blue','Purple','Magenta'])
    index=reservoir.create_oval(coordx,coordy,coordx+size,coordy+size,fill=color)
    particule=[coordx,coordy,dX,dY,mass,index]
    listeParticules.append(particule)
    nbrParticules+=1

# Test overlap

    for p in listeParticules:  
        if p!=particule and distanceAuCarre(p[0],p[1],particule[0],particule[1])<=(p[4]+particule[4])**2 :
            reservoir.delete(particule[5])
            l=len(listeParticules)-1
            del listeParticules[l]
            creerParticuleValide()
            break
    return nbrParticules

def plusUn():
    global nbrParticules
    nbrParticules+=1
    

def fcombine():
    creerParticuleValide()
    #plusUn()
    #lol en fait ca marche pas
        
def move ():
    nbrLabel.config(text='Nombre de particules=' + str(nbrParticules))
    Ec = int(calculerEnergieCinetique())
    EcLabel.config(text='Ec=' + str(Ec))
    if flag==1:
        for particule in listeParticules:
            posX=particule[0]
            posY=particule[1]
            particule[0] += particule[2]
            particule[1] += particule[3]
            if particule[0]-particule[4]<=0 or particule[0]+particule[4]>=canvasWidth :
                particule[2]*=-1
                particule[0]=posX
                particule[1]=posY
            if particule[1]-particule[4]<=0 or particule[1]+particule[4]>=canvasHeight :
                particule[3]*=-1
                particule[0]=posX
                particule[1]=posY
            for otherParticule in listeParticules :
                if otherParticule != particule and distanceAuCarre(particule[0],particule[1],otherParticule[0],otherParticule[1])<=(particule[4]+otherParticule[4])**2 :
                    particule[0]=posX
                    particule[1]=posY
                    nx=(particule[0]-otherParticule[0])/sqrt((particule[0]-otherParticule[0])**2+(particule[1]-otherParticule[1])**2)
                    ny=(particule[1]-otherParticule[1])/sqrt((particule[0]-otherParticule[0])**2+(particule[1]-otherParticule[1])**2)
                    tx=-ny
                    ty=nx
                    m1=particule[4]
                    m2=otherParticule[4]
                    v1x=particule[2]
                    v1y=particule[3]
                    v2x=otherParticule[2]
                    v2y=otherParticule[3]
                    v1n=v1x*nx + v1y*ny
                    v1t=v1x*tx + v1y*ty  
                    v2n=v2x*nx + v2y*ny
                    v2t=v2x*tx + v2y*ty
                    v1nn=((m1-m2)/(m1+m2))*v1n + ((2*m2)/(m1+m2))*v2n
                    v2nn=((2*m1)/(m1+m2))*v1n + ((m2-m1)/(m1+m2))*v2n
                    particule[2]=v1nn*nx - v1t*ny
                    otherParticule[2]=v2nn*nx - v2t*ny
                    otherParticule[3]=v2t*nx + v2nn*ny
                    particule[3]=v1t*nx + v1nn*ny
            reservoir.coords(particule[5],particule[0]-particule[4],particule[1]-particule[4],particule[0]+particule[4],particule[1]+particule[4])
    reservoir.after(10,move)


    
def stop_it():
    global flag
    flag=0

def raz():
    global flag, nbrParticules,listeParticules, Ec
    flag=0
    nbrParticules=0
    for particule in listeParticules :
        reservoir.delete(particule[5])
    del listeParticules[:]

    
def main():
    # MAIN

    global nbrLabel, EcLabel, reservoir

    mainWindow=Tk()
    mainWindow.geometry('1000x545')
    mainWindow.title('RESERVOIR DE PARTICULES')

    reservoir=Canvas(mainWindow,bg='light grey',height=canvasHeight,width=canvasWidth)
    reservoir.place(x=0,y=0)

    createButton=Button(mainWindow,text='+1 Particules ',command= fcombine)
    createButton.place(x=150,y=510)

    rapportButton=Button(mainWindow,text=' Arret ', command=stop_it)
    rapportButton.place(x=345,y=510)

    razButton=Button(mainWindow,text='Remise a zero ', command=raz)
    razButton.place(x=550,y=510)

    # data et labels


    nbrLabel=Label(mainWindow,text='Nbr particules = ' + str(nbrParticules))
    nbrLabel.place(x=canvasWidth+25,y=25)

    EcLabel=Label(mainWindow,text='Ec = ' + str(Ec))
    EcLabel.place(x=canvasWidth+25,y=50)

    print(Ec)

    move()
    mainWindow.mainloop()

if __name__ == '__main__':
    main()
