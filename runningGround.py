from pico2d import load_image

class RunningGround:
    def __init__(self):
        self.image = load_image('running_ground.png')

    def draw(self):
        self.image.draw(750,300)

    def update(self):
        pass