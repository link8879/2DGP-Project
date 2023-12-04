import time

from pico2d import draw_rectangle

import foul_mode
import game_framework
import javelin_server

class FoulLine:
    def __init__(self):
        self.x = 900
        self.y = 130
        self.is_collision = False
    def update(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        draw_rectangle(* self.get_bb())

    def get_bb(self):
        return self.x, self.y -50, self.x +15, self.y +50

    def handle_collision(self, group, other):
        if group == 'foulLine:player':
            self.is_collision = True
            game_framework.push_mode(foul_mode)
            javelin_server.flying_distance.append(0)
