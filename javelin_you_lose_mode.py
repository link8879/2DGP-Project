import time

from pico2d import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_RETURN, load_music, load_font
from sdl2 import SDLK_1

import game_framework
from pico2d import load_image, clear_canvas, update_canvas, get_events

import javelin_server
import running100_mode
import running_server
import title_mode


def init():
    global image
    global running
    global bgm
    global font

    font = load_font('ENCR10B.TTF', 20)
    
    image = load_image('you_lose.png')
    bgm = load_music('lose_music.mp3')
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

    for i in range(len(javelin_server.flying_distance)):
        font.draw(100+ 100 * i, 100 ,'Distance: %.2f m' % javelin_server.flying_distance[i], (255, 255, 255))


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
