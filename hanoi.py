# -*- coding: cp1250 -*-
from visual import *
from config import config
import time, sys, os, argparse

DIST = 25
HEIGHT = 25
THICKNESS = 1
RADIUS = 10
SEL_TOWER = 'Z'
N = 0
# listy kolek aktualnie na danej wiezy - wpisujemy inty odp. indeksom w tab. rings
tA = 0
tB = 0
tC = 0
A = 0
B = 0
C = 0
rings = 0
scene = 0

# funkcja przesuwania kolek miedzy wiezami                    
def moveRing(t1,t2,d):
    global N
    i = 0
    global THICKNESS
    if t1[0] == -1 and t2[0] == -1: 
        return -1 # przesuwanie miedzy pustymi wiezami jest zabronione
    j = N-1
    while t2[j] == -1 and j > 0:
        j = j-1 # znajdywanie kolka do przeniesienia
    if t1[0] == -1:
        t1[0] = t2[j]
        t2[j] = -1
        rings[t1[0]].pos = (d,0,0)
    else:
        i = N-1
    while t1[i] == -1 and i > 0:
        i = i-1
    if t1[i] <  t2[j]:
        t1[i+1] = t2[j]
        t2[j] = -1
        rings[t1[i+1]].pos = (d,(i+1)*THICKNESS*1.7,0)

def checkWin(t):
    if t[N-1] != -1:
        txt = text(text='Gratulacje - ulozyles wieze',align='left',
                    depth=-0.3,height=3,
                    color=(1.0,0.0,0.5),pos=(-50,40,0))
        sleep(1)
        win() #so much win wow
                    
def win():
    print sys.argv
    print "-n "+str(N+1)
    txt = text(text='Nastepny level za: 3...',align='left',
                    depth=-0.3,height=3,
                    color=(1.0,0.0,0.5),pos=(-50,30,0))
    sleep(1) # 1-sekundowy delay
    txt.text='Nastepny level za: 2...'
    sleep(1) # 1-sekundowy delay
    txt.text='Nastepny level za: 1...'
    sleep(1) # 1-sekundowy delay
    python = sys.executable
    os.execl(python,python, * [sys.argv[0],"-n "+str(N+1)])

def keyInput(ev):
    global A
    global B
    global C
    global tA
    global tB
    global tC
    global SEL_TOWER
    if ev.key == '1':
        A.material = materials.emissive
        B.material = materials.wood
        C.material = materials.wood
        SEL_TOWER = 'A'
    elif ev.key == '2':
        A.material = materials.wood
        B.material = materials.emissive
        C.material = materials.wood
        SEL_TOWER = 'B'
    elif ev.key == '3':
        A.material = materials.wood
        B.material = materials.wood
        C.material = materials.emissive
        SEL_TOWER = 'C'
    elif ev.key == '0':
        A.material = materials.wood
        B.material = materials.wood
        C.material = materials.wood
        SEL_TOWER = 'Z'
    # A S D jako cele 'A' 'B' 'C'
    elif ev.key == 'a':
        if SEL_TOWER == 'B':
            moveRing(tA,tB,-DIST)
            B.material = materials.wood
            SEL_TOWER == 'Z'
        elif SEL_TOWER == 'C':
            moveRing(tA,tC,-DIST)
            C.material = materials.wood
            SEL_TOWER == 'Z'
    elif ev.key == 's':
        if SEL_TOWER == 'A':
            moveRing(tB,tA,0)
            A.material = materials.wood
            SEL_TOWER == 'Z'
        elif SEL_TOWER == 'C':
            moveRing(tB,tC,0)
            C.material = materials.wood
            SEL_TOWER == 'Z'
    elif ev.key == 'd':
        if SEL_TOWER == 'B':
            moveRing(tC,tB,DIST)
            B.material = materials.wood
            SEL_TOWER == 'Z'
        elif SEL_TOWER == 'A':
            moveRing(tC,tA,DIST)
            A.material = materials.wood
            SEL_TOWER == 'Z'
    
    checkWin(tC)

def main(argv):
    global N
    global A
    global B
    global C
    global tA
    global tB
    global tC
    global rings
    global THICKNESS
    global scene
    """
    Pobieranie ilosci kolek z pliku konfiguracyjnego
    Budowa pliku:
    config = {
            'N': 'X' - tutaj za 'X' podstawiamy wartosc. 
    }

    Jesli X > 10 to za N przyjmujemy 10, jesli X < 3 to za N przyjmujemy 3
    """
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument('-n', '--number')

        args = parser.parse_args()
        try:
            N = int(float(args.number))
        except TypeError:       
            N = int(float(config['N']))
        if N < 3:
            N = 3
        elif N > 10:
            N = 10
    else:      
        N = int(float(config['N']))
        if N < 3:
            N = 3
        elif N > 10:
            N = 10
        
    print "N = "+str(N)
    
    # listy kolek aktualnie na danej wiezy - wpisujemy inty odp. indeksom w tab. rings
    tA = [-1]*N
    tB = [-1]*N
    tC = [-1]*N
    
    THICKNESS = 2.5 - 1.5* (N-3) / 7

    scene = display(title='Hanoi',
         width=800, height=600,
         center=(0,15,10), background=(0,0,0))
    
    txt = text(text="Level "+str(N-2),align='left',
                depth=-0.3,height=3,
                color=(1.0,0.0,0.5),pos=(-50,50,0))
    
    A = cylinder(pos = (-DIST, 0, 0),
                 axis = (0, HEIGHT, 0),
                 material = materials.wood)
    B = cylinder(pos = (0, 0, 0),
                 axis = (0, HEIGHT, 0),
                 material = materials.wood)
    C = cylinder(pos = (DIST, 0, 0),
                 axis = (0, HEIGHT, 0),
                 material = materials.wood)

    colors = [None]*10
    colors[0] = (1,0,0)
    colors[1] = (0,1,0)
    colors[2] = (1,1,0)
    colors[3] = (0,0.5,0.5)
    colors[4] = (1,0,1)
    colors[5] = (0,1,1)
    colors[6] = (0,0,1)
    colors[7] = (1,0,0.5)
    colors[8] = (1,0.5,0)
    colors[9] = (0.5,0,0.5)
    rings = [None]*N

    for i in range(N):
        rings[i] = ring(pos=(-DIST, i*THICKNESS*1.7, 0),
                            axis=(0, 1, 0),
                            radius = RADIUS-(i*8.0)/N,
                            thickness = THICKNESS,
                            color=colors[i])
        tA[i] = i
        tB[i] = -1
        tC[i] = -1

    start = time.time()

    clock = text(text='czas: 0:00',align='right',
                    depth=-0.3,height=3,
                    color=(1.0,0.0,0.5),pos=(50,50,0))
    
    scene.bind('keydown', keyInput)
    while 1:
        sleep(0.01) # bez sleep jest szary ekran, 100 fps jest ok
        czas = time.time() - start
        seconds = int(czas%60)
        if seconds < 10:
            seconds = '0'+str(seconds)
        else:
            seconds = str(seconds)
        czas = str(int(czas/60))+':'+seconds
        clock.text = 'czas: '+czas

if __name__ == "__main__":
   main(sys.argv[1:])
