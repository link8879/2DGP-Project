from pico2d import load_image, draw_rectangle

import running_server


class ComFinishLine:
    def __init__(self,x):
        self.x, self.y = x,230
        self.image = load_image('finish_line.png')
        self.state = 0 # 0이면 끊어지기 전
    def draw(self):
        if self.state == 0:
            self.image.clip_draw(0,0,44,81,self.x,self.y)
        elif self.state == 1:
            self.image.clip_draw(48, 0, 44, 81, self.x - running_server100.background.window_left,self.y)

        #draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x -22, self.y - 40.5, self.x + 22, self.y + 40.5
    def update(self):
        pass
    def handle_collision(self,group, other):
        pass