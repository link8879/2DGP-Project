from pico2d import load_image
from camera import Camera


class RunningGround:
    def __init__(self):
        self.image = load_image('running_ground.png')
    def draw(self):
        self.image.clip_draw(0,0,800,600,400,300)

    def update(self):
        pass