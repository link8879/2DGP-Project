from pico2d import *
import game_framework
import game_world
import running_player
import title_mode
from runningGround import RunningGround
from running_player import RunningPlayer
from com_running_player import ComRunningPlayer
from camera import Camera

def handle_events():
    global playing

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            running_player.handle_event(event)
            com_running_player.handle_event(event)

def init():
    global playing
    global runningGround
    global world
    global running_player
    global com_running_player
    global camera

    camera = Camera()
    runningGround = RunningGround(camera)
    running_player = RunningPlayer(camera)
    com_running_player = ComRunningPlayer(camera)

    world = []
    world.append(runningGround)
    world.append(running_player)
    world.append(com_running_player)
    playing = True

def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
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

