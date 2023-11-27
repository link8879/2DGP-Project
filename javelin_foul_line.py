import time

from pico2d import load_image, clamp, get_canvas_width, get_canvas_height, draw_rectangle, load_music, SDLK_t, \
    SDL_KEYDOWN, SDLK_SPACE, load_font

import finish_line
import foul_mode
import game_framework
import game_world
import javelin_mode
import javelin_server
import you_win_mode
from camera import Camera
from javelin import Javelin

class FoulLine:
    def __init__(self):
        self.x = 1000
        self.y = 130
        self.is_collision = False
    def update(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        draw_rectangle(* self.get_bb())

    def get_bb(self):
        return self.x -15, self.y -50, self.x +15, self.y +50

    def handle_collision(self, group, other):
        if group == 'foulLine:player':
            self.is_collision = True
            game_framework.push_mode(foul_mode)
            javelin_server.flying_distance.append(0)
            pass
