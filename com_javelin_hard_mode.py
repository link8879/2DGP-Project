from pico2d import *
import game_framework
import game_world
import title_mode
from com_hard_javelin_player import ComHardThrower
from javelin_ground import JavelinGround
from javelin_foul_line import FoulLine
import javelin_server

def init():
    global playing
    global bgm
    global second_sound
    global is_played
    global start_time

    javelin_server.background = JavelinGround()
    javelin_server.player = ComHardThrower()
    javelin_server.foul_line = FoulLine()

    game_world.add_object(javelin_server.background,0)
    game_world.add_object(javelin_server.player,1)
    game_world.add_object(javelin_server.foul_line,1)

    game_world.add_collision_pair('foulLine:Complayer',javelin_server.player,None)
    game_world.add_collision_pair('foulLine:Complayer',None,javelin_server.foul_line)

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

    if current_time - start_time >= 5 and not is_played:
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
    pass

