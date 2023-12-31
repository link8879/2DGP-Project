from pico2d import load_image, draw_rectangle

import running_server


class Hurdle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = load_image('hurdle.png')
        self.state = 0

    def draw(self):
        if self.state == 0:
            self.image.clip_draw(0,0,75,77,self.x-running_server.background.window_left,self.y)
        elif self.state == 1:
            self.image.clip_draw(76,0,75,77,self.x-running_server.background.window_left,self.y)
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 36.5, self.y - 37.5, self.x -5, self.y + 32

    def update(self):
        pass

    def handle_collision(self, group,other):
        if group == 'player:hurdles':
            self.state = 1