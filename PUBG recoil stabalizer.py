from pynput.mouse import Listener,Button
import pyautogui as pag
import time
from timeloop import Timeloop
from datetime import timedelta
import datetime
import pynput.keyboard as keyboard
from pynput.keyboard import Key

import win32api
import datetime, threading

from threading import Thread 

speed=280

def AK(x):
    v=0
    if x<190:
        v=250
    else:
        v=220
    return v*1e-5


def M4(x):
    v=0
    if x<200:
        v=280
    else:
        v=200
    return v*1e-5
  
def SCAR(x):
    v=0
    if x<200:
        v=220
    elif x<300:
        v=135
    elif x<400:
        v=100
    else:
        v=101
    return v*1e-5

def UMP(x):
    v=0
    if x<110:
        v=315
    elif x<180:
        v=300
    elif x<360:
        v=250
    else:
        v=200
    return v*1e-5



class Mover(Thread):
    def __init__(self):
        super().__init__()
        self.keep_run=False
        self.t=2.6021280019157032e-05
        self.alpha=0.0005
        self.beta=0.005
        self.c=0

    def reset(self):
        self.t=1e-5
        # self.t=2.6e-03
        self.alpha=0.0005
        self.beta=0.7
        self.c=0


    def my_move(self):
        c=0
        pos=win32api.GetCursorPos()

        t=self.t
        
        while True:
            
            self.c=c
            win32api.mouse_event(1,0,3,0,0)
            
            time.sleep(t)
            
            if aim_state=="ak":
                t=AK(c)
            elif aim_state=="m4":
                t=M4(c)
            elif aim_state=="scar":
                t=SCAR(c)
            elif aim_state=="ump":
                t=UMP(c)
            
            if not self.keep_run:
                break
            c+=1
    def start(self):
        self.reset()
        self.keep_run=True
        self.my_move()
    
    def stop(self):
        self.keep_run=False
    
    
mover=Mover()

state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128
f1=win32api.GetKeyState(112)
f2=win32api.GetKeyState(113)

f5=win32api.GetKeyState(116)
f6=win32api.GetKeyState(117)
f7=win32api.GetKeyState(118)
f8=win32api.GetKeyState(119)

ctl=win32api.GetKeyState(17)
l_shift=win32api.GetKeyState(160)
r=win32api.GetKeyState(0x52)

flag=False
aim_state="ak"

while True:
    a = win32api.GetKeyState(0x01)
    b = win32api.GetKeyState(0x02)
    cur_f1=win32api.GetKeyState(112)
    cur_f2=win32api.GetKeyState(113)
    
    cur_f5=win32api.GetKeyState(116)
    cur_f6=win32api.GetKeyState(117)
    cur_f7=win32api.GetKeyState(118)
    cur_f8=win32api.GetKeyState(119)
    
    
    cur_ctl=win32api.GetKeyState(17)
    cur_lshift=win32api.GetKeyState(160)
    cur_r=win32api.GetKeyState(0x52)


    if f5 != cur_f5:  # Button state changed
        f5 = cur_f5
        if f5<0:
            aim_state="ak"
            print("ak state.")

    if f6 != cur_f6:  # Button state changed
        f6 = cur_f6
        if f6<0:
            aim_state="m4"
            print("m4 gun state.")

    if f7 != cur_f7:  # Button state changed
        f7 = cur_f7
        if f7<0:
            aim_state="scar"
            print("scar gun state.")

    if f8 != cur_f8:  # Button state changed
        f8 = cur_f8
        if f8<0:
            aim_state="ump"
            print("ump gun state.")



    if cur_f1 != f1:  # Button state changed
        f1 = cur_f1

        if f1 < 0:
            speed-=5
            print("cur speed:",speed)
        else:
            pass
            
    if cur_f2 != f2:  # Button state changed
        f2 = cur_f2

        if f2 < 0:
            speed+=5
            print("cur speed:",speed)
        else:
            pass
            
    if b != state_right:  # Button state changed
        state_right = b
        if state_right < 0:
            flag=not flag


            
            
    if flag:
        if a != state_left:  # Button state changed
            state_left = a

            if a < 0:
                Thread(target = mover.start).start()
                print(win32api.GetCursorPos(),"in t",mover.t)  
            else:
                mover.stop()
                print("counter:",mover.c,"out t",mover.t)
  


        if l_shift != cur_lshift:  # Button state changed
            l_shift = cur_lshift
            if l_shift < 0:
                flag=False

        if cur_r != r:  # Button state changed
            r = cur_r
            if r < 0:
                flag=False

     

    else:
        mover.stop()
            
            
            
    time.sleep(0.00005)
    


