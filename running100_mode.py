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
    global runningGround
    global running_player
    global com_running_player
    global camera
    global player_finish_line
    global com_finish_line

    camera = Camera()
    runningGround = RunningGround(camera)
    running_player = RunningPlayer(camera)
    com_running_player = ComRunningPlayer(camera)
    player_finish_line = FinishLine(100,100,camera,running_player)
    com_finish_line = FinishLine(100,100,camera,running_player)


    game_world.add_object(runningGround,0)
    game_world.add_object(running_player,1)
    game_world.add_object(com_running_player,1)
    game_world.add_object(player_finish_line,0)
    game_world.add_object(com_finish_line,0)

    playing = True

def update_world():
    game_world.update()

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

