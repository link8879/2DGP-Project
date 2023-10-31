from pico2d import load_image
from camera import Camera


class RunningGround:
    def __init__(self, camera):
        self.image = load_image('running_ground.png')
        self.camera = camera
    def draw(self):
        self.image.clip_draw(0+self.camera.x,0+self.camera.y,800,600,400,300)

    def update(self):
        pass