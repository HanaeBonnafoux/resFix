from tkinter import *
from random import *
from math import*

# Global variables 
CANVAS_HEIGHT, CANVAS_WIDTH = 500, 700

canvasHeight=500
canvasWidth=750

listParticles=[]
Ek=0
numberParticle=0
P=0
#nrT --- Need to figure what nrt is
flag=1

nbrLabel = None
EcLabel = None
reservoir = None

# FONCTIONS

def distanceSquared(xA,yA,xB,yB):
    d=(xA-xB)**2+(yA-yB)**2
    return d

def calculateKineticEnergy():
    global Ek
    if flag==1:
        Ek=0
        for p in listParticles :
            Ek+=0.5*p[4]*(p[2]**2+p[3]**2)
    if flag==0 :
        Ek=0
    return Ek
#There is probably a problem here because the kinetic energy returns a strange result

def createValidParticle():
    
# Creating a particle
    
    global numberParticle,flag
    flag=1
    size=1.*randint(15,55)
    mass=size
    dX,dY=1.*randint(-3,3),1.*randint(-3,3)
    coordx=1.*randint(0+size,canvasWidth-size)
    coordy=1.*randint(0+size,canvasHeight-size)
    color=choice(['Red','Orange','Yellow','Green','Cyan','Blue','Purple','Magenta'])
    index=reservoir.create_oval(coordx,coordy,coordx+size,coordy+size,fill=color)
    particle=[coordx,coordy,dX,dY,mass,index]
    listParticles.append(particle)
    numberParticle+=1

# Test overlap

    for p in listParticles:  
        if p!=particle and distanceSquared(p[0],p[1],particle[0],particle[1])<=(p[4]+particle[4])**2 :
            reservoir.delete(particle[5])
            l=len(listParticles)-1
            del listParticles[l]
            createValidParticle()
            break
    return numberParticle

def plusOne():
    global numberParticle
    numberParticle+=1
    

def fcombine():
    createValidParticle()
    #plusOne(),
    #Not working as it should
        
def move ():
    nbrLabel.config(text='Number of particles =' + str(numberParticle))
    Ek = int(calculateKineticEnergy())
    EcLabel.config(text='Ek=' + str(Ek))
    if flag==1:
        for particle in listParticles:
            posX=particle[0]
            posY=particle[1]
            particle[0] += particle[2]
            particle[1] += particle[3]
            if particle[0]-particle[4]<=0 or particle[0]+particle[4]>=canvasWidth :
                particle[2]*=-1
                particle[0]=posX
                particle[1]=posY
            if particle[1]-particle[4]<=0 or particle[1]+particle[4]>=canvasHeight :
                particle[3]*=-1
                particle[0]=posX
                particle[1]=posY
            for otherParticule in listParticles :
                if otherParticule != particle and distanceSquared(particle[0],particle[1],otherParticule[0],otherParticule[1])<=(particle[4]+otherParticule[4])**2 :
                    particle[0]=posX
                    particle[1]=posY
                    nx=(particle[0]-otherParticule[0])/sqrt((particle[0]-otherParticule[0])**2+(particle[1]-otherParticule[1])**2)
                    ny=(particle[1]-otherParticule[1])/sqrt((particle[0]-otherParticule[0])**2+(particle[1]-otherParticule[1])**2)
                    tx=-ny
                    ty=nx
                    m1=particle[4]
                    m2=otherParticule[4]
                    v1x=particle[2]
                    v1y=particle[3]
                    v2x=otherParticule[2]
                    v2y=otherParticule[3]
                    v1n=v1x*nx + v1y*ny
                    v1t=v1x*tx + v1y*ty  
                    v2n=v2x*nx + v2y*ny
                    v2t=v2x*tx + v2y*ty
                    v1nn=((m1-m2)/(m1+m2))*v1n + ((2*m2)/(m1+m2))*v2n
                    v2nn=((2*m1)/(m1+m2))*v1n + ((m2-m1)/(m1+m2))*v2n
                    particle[2]=v1nn*nx - v1t*ny
                    otherParticule[2]=v2nn*nx - v2t*ny
                    otherParticule[3]=v2t*nx + v2nn*ny
                    particle[3]=v1t*nx + v1nn*ny
            reservoir.coords(particle[5],particle[0]-particle[4],particle[1]-particle[4],particle[0]+particle[4],particle[1]+particle[4])
    reservoir.after(10,move)


    
def stop_it():
    global flag
    flag=0

def reset():
    global flag, numberParticle,listParticles, Ek
    flag=0
    numberParticle=0
    for particle in listParticles :
        reservoir.delete(particle[5])
    del listParticles[:]

    
def main():
    # MAIN

    global nbrLabel, EcLabel, reservoir

    mainWindow=Tk()
    mainWindow.geometry('1000x545')
    mainWindow.title('PARTICLE RESERVOIR')

    reservoir=Canvas(mainWindow,bg='light grey',height=canvasHeight,width=canvasWidth)
    reservoir.place(x=0,y=0)

    createButton=Button(mainWindow,text='+1 Particle ',command= fcombine)
    createButton.place(x=150,y=510)

    rapportButton=Button(mainWindow,text=' Stop ', command=stop_it)
    rapportButton.place(x=345,y=510)

    razButton=Button(mainWindow,text='Reset ', command=reset)
    razButton.place(x=550,y=510)

    # data and labels

    nbrLabel=Label(mainWindow,text='Number of particles = ' + str(numberParticle))
    nbrLabel.place(x=canvasWidth+25,y=25)

    EcLabel=Label(mainWindow,text='Kinetic Energy = ' + str(Ek))
    EcLabel.place(x=canvasWidth+25,y=50)

    print(Ek)

    move()
    mainWindow.mainloop()

if __name__ == '__main__':
    main()
