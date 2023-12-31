import time

from pico2d import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_RETURN, load_music, load_font

import game_framework
from pico2d import load_image, clear_canvas, update_canvas, get_events

import running_server
import title_mode


def init():
    global image
    global running
    global bgm
    global total_time
    global font

    font = load_font('ENCR10B.TTF', 20)
    total_time = time.time() - running_server.player.time - 5 # 끝날 때 시간으로 바꿀 필요 있음
    image = load_image('you_win.png')
    bgm = load_music('win_music.mp3')
    bgm.set_volume(100)
    bgm.play()
    running = True

def finish():
    global image
    del image

def update():
    pass

def draw():
    clear_canvas()
    image.draw(400,300)
    font.draw(100, 100, 'Time: %.2f sec' % total_time, (255, 255, 255))
    font.draw(400, 100, 'Velocity: %.2f m/s' % (100/total_time), (255, 255, 255))
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif(event.type, event.key) == (SDL_KEYDOWN,SDLK_RETURN):
            game_framework.change_mode(title_mode)

def pause():
 pass

def resume():
 pass