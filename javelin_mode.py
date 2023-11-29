from pico2d import *

import com_javelin_mode
import game_framework
import game_world
import title_mode
from javelin_ground import JavelinGround
from javelin_player import Thrower
from javelin_foul_line import FoulLine
#from com_javelin_player import ComThrower
import javelin_server

def init():
    global playing
    global bgm
    global second_sound
    global is_played
    global start_time

    javelin_server.background = JavelinGround()
    javelin_server.player = Thrower()
    javelin_server.foul_line = FoulLine()

    game_world.add_object(javelin_server.background,0)
    game_world.add_object(javelin_server.player,1)
    game_world.add_object(javelin_server.foul_line,1)
    game_world.add_collision_pair('foulLine:player',javelin_server.player,None)
    game_world.add_collision_pair('foulLine:player',None,javelin_server.foul_line)

    bgm = load_music('start_music.mp3')
    bgm.set_volume(100)
    bgm.play()

    second_sound = load_music('javelin_startsound.wav')
    is_played = False

    start_time = get_time()
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
            javelin_server.player.handle_event(event)
            #javelin_server.com_player.handle_event(event)


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

def update():
    global bgm
    global is_played

    for game_object in game_world.all_objects():
        game_object.update()

    game_world.handle_collisions()
    current_time = get_time()

    if current_time - start_time >= 5 and is_played == False:
        second_sound.set_volume(300)
        second_sound.play()
        is_played = True


def finish():
    game_world.clear()
    pass


def draw():
    clear_canvas()
    render_world()
    update_canvas()

def pause():

    pass

def resume():
    game_framework.change_mode(com_javelin_mode)

