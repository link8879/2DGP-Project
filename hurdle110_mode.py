from pico2d import *
import game_framework
import game_world
import title_mode
import you_lose_mode
import you_win_mode
from hurdle_player import HurdleRunner
from runningGround import RunningGround
from com_running_player import ComRunningPlayer
from camera import Camera
from finish_line import FinishLine
import running_server100
from hurdle import Hurdle

def init():
    global playing
    global bgm
    global second_sound
    global is_played
    global start_time
    global hurdles

    running_server100.background = RunningGround()
    running_server100.player = HurdleRunner()
    running_server100.com_player = ComRunningPlayer()
    running_server100.player_finishline = FinishLine()
    running_server100.com_finishline = FinishLine()
    hurdles = [Hurdle(i*200 + 200,86) for i in range(14)]

    game_world.add_object(running_server100.background,0)
    game_world.add_object(running_server100.player,1)
    game_world.add_object(running_server100.com_player,1)
    game_world.add_object(running_server100.com_finishline,0)
    game_world.add_object(running_server100.player_finishline,0)

    for hurdle in hurdles:
        game_world.add_object(hurdle, 0)

    game_world.add_collision_pairs(running_server100.player, hurdles,'player:hurdles')
    game_world.add_collision_pairs(running_server100.com_player, running_server100.com_finishline, 'com:finishline')

    # bgm = load_music('start_music.mp3')
    # bgm.set_volume(100)
    # bgm.play()

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

    if running_server100.player.x > 1440 and running_server100.com_player.x < 1440:
        game_world.clear()
        game_framework.change_mode(you_win_mode)
    elif running_server100.player.x < 1440 and running_server100.com_player.x > 1440:
        game_world.clear()
        game_framework.change_mode(you_lose_mode)

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