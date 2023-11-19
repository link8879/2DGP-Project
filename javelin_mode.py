from pico2d import *
import game_framework
import game_world
import title_mode
from javelin_ground import JavelinGround
from javelin_player import Thrower
#from com_javelin_player import ComThrower
import running_server100

def init():
    global playing
    global bgm
    global second_sound
    global is_played
    global start_time

    running_server100.background = JavelinGround
    running_server100.player = Thrower()
    #running_server100.com_player = ComThrower()


    game_world.add_object(running_server100.background,0)
    game_world.add_object(running_server100.player,1)
    #game_world.add_object(running_server100.com_player,1)

    print(running_server100.player.x)
    print(running_server100.com_player.x)

    bgm = load_music('start_music.mp3')
    bgm.set_volume(100)
    bgm.play()

    second_sound = load_music('startsound.wav')
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
         #  running_sever100.player.handle_event(event)
            running_server100.player.handle_event(event)
            running_server100.com_player.handle_event(event)


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
    # if running_server100.player.x > 1440 and running_server100.com_player.x < 1440:
    #     game_world.clear()
    #     game_framework.change_mode(you_win_mode)
    # elif running_server100.player.x < 1440 and running_server100.com_player.x > 1440:
    #     game_world.clear()
    #     game_framework.change_mode(you_lose_mode)

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
 pass