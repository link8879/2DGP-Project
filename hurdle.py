from pico2d import load_image


class Hurdle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = load_image('hurdle.png')
        self.state = 0

    def draw(self):
        self.image.clip_draw(0,0,75,77,self.x,self.y)
        pass

    def get_bb(self):
        return self.x - 36.5, self.y - 37.5, self.x + 36.5, self.y + 37.5

    def update(self):
        pass

    def handle_collision(self, other, group):
        self.state = 0