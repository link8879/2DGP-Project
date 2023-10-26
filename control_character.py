from pico2d import *
from runningGround import RunningGround

def reset_world():
    global playing
    global runningGround

    runningGround = RunningGround()
    playing = True

open_canvas(800,600)
reset_world()

while playing:
    update_canvas()

clear_canvas()
   #runningGround.draw()