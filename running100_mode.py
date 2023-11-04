from pico2d import *
import game_framework
import game_world
import running_player
import title_mode
from runningGround import RunningGround
from running_player import RunningPlayer
from com_running_player import ComRunningPlayer
from camera import Camera
from finish_line import FinishLine
import running_server100

def init():
    global playing
    running_server100.background = RunningGround()
    running_server100.player = RunningPlayer()
    running_server100.com_player = ComRunningPlayer()
    running_server100.player_finishline = FinishLine(100,100)
    running_server100.com_finishline = FinishLine(100,100)


    game_world.add_object(running_server100.background,0)
    game_world.add_object(running_server100.player,1)
    game_world.add_object(running_server100.com_player,1)
    game_world.add_object(running_server100.com_finishline,0)
    game_world.add_object(running_server100.player_finishline,0)

    playing = True

def handle_events():
    global playing

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
         #  running_sever100.player.handle_event(event)
            running_server100.player.handle_event(event)
            running_server100.com_player.handle_event(event)



def update_world():
    game_world.update()
    delay(0.01)

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


def update():
    update_world()

def finish():
    game_world.clear()
    pass


def draw():
    clear_canvas()
    render_world()
    update_canvas()

