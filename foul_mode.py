from pico2d import *
import game_framework
import game_world
import javelin_mode
import title_mode

def init():
    global bgm
    global start_time

    bgm = load_music('start_music.mp3')
    bgm.set_volume(100)
    bgm.play()

    second_sound = load_music('startsound.wav')
    start_time = get_time()

def handle_events():
    global playing

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)


def render_world():
    clear_canvas()
    game_world.render()

    font = load_font('ENCR10B.TTF', 50)
    font.draw(200, 200, 'FOUL!', (255, 0, 0))

    current_time = get_time()
    print(current_time)
    print(start_time)
    if current_time - start_time > 5:
        game_framework.pop_mode()

    update_canvas()

def update():
    global bgm
    global is_played

def finish():
    pass


def draw():
    clear_canvas()
    render_world()
    update_canvas()

def pause():
    pass

def resume():
    print(5)
    game_framework.change_mode(javelin_mode)
