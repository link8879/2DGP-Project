from pico2d import *
import game_framework
import game_world
import title_mode
from runningGround import RunningGround
from running_player import Runner
from com_running_player import ComRunningPlayer
from finish_line import FinishLine
from com_finish_line import ComFinishLine
import running_server
from com_hard_running_player import ComHardRunningPlayer

def init():
    global playing
    global bgm
    global second_sound
    global is_played
    global start_time

    if running_server.distance == 1:
        running_server.background = RunningGround('running_ground.png')
        running_server.player_finishline = FinishLine(5000)
        running_server.com_finishline = ComFinishLine(5000)
        pass
    elif running_server.distance == 2:
        running_server.background = RunningGround('running_ground200.png')
        running_server.player_finishline = FinishLine(10000)
        running_server.com_finishline = ComFinishLine(10000)
        pass
    elif running_server.distance == 3:
        running_server.background = RunningGround('running_ground300.png')
        running_server.player_finishline = FinishLine(15000)
        running_server.com_finishline = ComFinishLine(15000)
        pass

    running_server.player = Runner()
    running_server.com_player = ComRunningPlayer()
    running_server.player = Runner()
    running_server.com_player = ComHardRunningPlayer()

    game_world.add_object(running_server.background,0)
    game_world.add_object(running_server.player,1)
    game_world.add_object(running_server.com_player,1)
    game_world.add_object(running_server.com_finishline,0)
    game_world.add_object(running_server.player_finishline,0)

    game_world.add_collision_pair('player:finishline',running_server.player, None)
    game_world.add_collision_pair('player:finishline',None,running_server.player_finishline)

    game_world.add_collision_pair('com_player:finishline', running_server.com_player, None)
    game_world.add_collision_pair('com_player:finishline', None, running_server.com_finishline)


    print(running_server.player.x)
    print(running_server.com_player.x)

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