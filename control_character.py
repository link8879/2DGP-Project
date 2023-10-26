from pico2d import *
from runningGround import RunningGround

def handle_events():
    global playing

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            playing = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            playing = False
        #else:
            #boy.handle_event(event)



def reset_world():
    global playing
    global runningGround
    global world

    runningGround = RunningGround()
    world = []
    world.append(runningGround)
    playing = True

def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas(800,600)
reset_world()

while playing:
    # image = load_image('player_animation.png')
    # image.clip_draw(8,661-33,11,32,100,100,50,80)

    handle_events()
    update_world()
    render_world()
    update_canvas()
    
    delay(0.01)
close_canvas()
   #runningGround.draw()