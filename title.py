from pico2d import load_image


def init():
    global image
    global running

    image = load_image('title.png')
    running = True

def finish():
    global image
    del image

def update():
    global running
    