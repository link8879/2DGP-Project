from pico2d import load_image, clamp, get_canvas_width, get_canvas_height

import running_server
from camera import Camera


class RunningGround:
    def __init__(self):
        self.image = load_image('running_ground.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
    def draw(self):
        #self.image.clip_draw(0,0,800,600,400,300)
        self.image.clip_draw_to_origin(
            self.window_left, self.window_bottom,
            self.canvas_width, self.canvas_height,
            0, 0)
    def update(self):
        self.window_left = clamp(0,int(running_server.player.x) - self.canvas_width // 2,self.w - self.canvas_width - 1)
        self.window_bottom = clamp(0, int(running_server.player.y) - self.canvas_height // 2,self.h - self.canvas_height - 1)
        pass