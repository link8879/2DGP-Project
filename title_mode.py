from pico2d import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, load_music, SDLK_1,SDLK_2,SDLK_3

import game_framework
from pico2d import load_image, clear_canvas, update_canvas, get_events

import hurdle110_mode
import javelin_mode
import running100_mode
import hurdle_select_distance_mode
import running_select_distance_mode

def init():
    global image
    global running
    global bgm
    image = load_image('title.png')
    bgm = load_music('titlemusic.mp3')
    bgm.set_volume(100)
    bgm.repeat_play()
    running = True

def finish():
    global image
    del image

def update():
    pass

def draw():
    clear_canvas()
    image.draw(400,300)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif(event.type, event.key) == (SDL_KEYDOWN,SDLK_1):
            game_framework.change_mode(running_select_distance_mode)
        elif(event.type, event.key) == (SDL_KEYDOWN,SDLK_2):
            game_framework.change_mode(hurdle_select_distance_mode)
        elif(event.type, event.key) == (SDL_KEYDOWN,SDLK_3):
            game_framework.change_mode(javelin_mode)


def pause():
 pass

def resume():
 pass