from pico2d import load_image


class FinishLine:
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.image = load_image('finish_line.png')
        self.state = 0 # 0이면 끊어지기 전
    def draw(self):
        if self.state == 0:
            self.image.clip_draw(0,0,44,81,1480,88)
        elif self.state == 1:
            self.image.clip_draw(48, 0, 44, 81, 1480, 88)
            pass

    def update(self):
        pass