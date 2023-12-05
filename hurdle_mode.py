from pico2d import *
import game_framework
import game_world
import title_mode
from hurdle_player import HurdleRunner
from runningGround import RunningGround
from com_hurdle_player import ComHurdleRunner
from finish_line import FinishLine
from com_finish_line import ComFinishLine
import running_server
from hurdle import Hurdle

def init():
    global playing
    global bgm
    global second_sound
    global is_played
    global start_time
    global hurdles

    if running_server.distance == 4:
        running_server.background = RunningGround('hurdle_ground110.png')
        running_server.player_finishline = FinishLine(3320)
        running_server.com_finishline = ComFinishLine(3320)

        hurdles = [Hurdle(i * 300 + 320, 86) for i in range(10)]
        com_hurdles = [Hurdle(i * 300 + 320, 228) for i in range(10)]
        pass
    elif running_server.distance == 5:
        running_server.background = RunningGround('hurdle_ground400.png')
        running_server.player_finishline = FinishLine(12020)
        running_server.com_finishline = ComFinishLine(12020)

        hurdles = [Hurdle(i * 1200 + 1220, 86) for i in range(10)]
        com_hurdles = [Hurdle(i * 1200 + 1220, 228) for i in range(10)]
        pass

    running_server.player = HurdleRunner()
    running_server.com_player = ComHurdleRunner()



    game_world.add_object(running_server.background,0)
    game_world.add_object(running_server.player,1)
    game_world.add_object(running_server.com_player,1)
    game_world.add_object(running_server.com_finishline,0)
    game_world.add_object(running_server.player_finishline,0)

    for hurdle in hurdles:
        game_world.add_object(hurdle, 0)

    for com_hurdle in com_hurdles:
        game_world.add_object(com_hurdle, 0)

    game_world.add_collision_pair('com_player:hurdles',running_server.com_player,None)
    for com_hurdle in com_hurdles:
        game_world.add_collision_pair('com_player:hurdles',None,com_hurdle)

    game_world.add_collision_pair('player:hurdles',running_server.player,None)
    for hurdle in hurdles:
        game_world.add_collision_pair('player:hurdles',None,hurdle)

    game_world.add_collision_pair('player:finishline', running_server.player, None)
    game_world.add_collision_pair('player:finishline', None, running_server.player_finishline)

    game_world.add_collision_pair('com_player:finishline', running_server.com_player, None)
    game_world.add_collision_pair('com_player:finishline', None, running_server.com_finishline)

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
            running_server.player.handle_event(event)
            running_server.com_player.handle_event(event)


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
 pass