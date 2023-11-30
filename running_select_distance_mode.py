from pico2d import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, load_music, SDLK_1,SDLK_2,SDLK_3

import game_framework
from pico2d import load_image, clear_canvas, update_canvas, get_events

import hurdle110_mode
import javelin_mode
import running_mode
import running_server
import select_running_difficulty_mode
import title_mode


def init():
    global image
    global running
    global bgm
    image = load_image('select_running_distance.png')
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
            game_framework.change_mode(title_mode)
        elif(event.type, event.key) == (SDL_KEYDOWN,SDLK_1):
            running_server.distance = 1       #100
            game_framework.change_mode(select_running_difficulty_mode)
        elif(event.type, event.key) == (SDL_KEYDOWN,SDLK_2):
            running_server.distance = 2       #200
            game_framework.change_mode(select_running_difficulty_mode)
        elif(event.type, event.key) == (SDL_KEYDOWN,SDLK_3):
            running_server.distance = 3       #300
            game_framework.change_mode(select_running_difficulty_mode)




def pause():
 pass

def resume():
 pass