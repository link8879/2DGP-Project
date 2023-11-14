from pico2d import load_image, get_time, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE

import game_framework
import game_world
import running_server100
import you_lose_mode

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 100.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'

class StartGame:
    @staticmethod
    def enter(player,e):
        player.wait_time = get_time()
        pass

    @staticmethod
    def do(player):
        if get_time() - player.wait_time > 5:
            player.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(6, 661 - 150, 31 - 6, 150 - 131, 20, 250, 75, 57)

class Run:
    @staticmethod
    def enter(player,e):
        pass
    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def do(player):
        # global last_update_time
        #
        # current_time = get_time()
        # if current_time - last_update_time > 0.3:  # 0.2초(200 밀리초)마다 로직 실행
        #     player.frame += 1
        #     player.x += 10
        #     last_update_time = current_time

        player.x += RUN_SPEED_PPS * game_framework.frame_time
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6


    @staticmethod
    def draw(player):
        # if player.frame == 0:
        #     player.image.clip_draw(8,661-33,11,32,player.x+100,player.y+50,50,90)
        if int(player.frame) == 0:
            player.image.clip_draw(28, 661 - 33, 12, 32, player.x- running_server100.background.window_left, player.y + 30, 36, 96)
        elif int(player.frame) == 1:
            player.image.clip_draw(46, 661 - 33, 14, 32, player.x- running_server100.background.window_left, player.y + 30, 42, 96)
        elif int(player.frame) == 2:
            player.image.clip_draw(62, 661 - 33, 16, 32, player.x- running_server100.background.window_left, player.y + 30, 48, 96)
        elif int(player.frame) == 3:
            player.image.clip_draw(81, 661 - 33, 26, 28, player.x- running_server100.background.window_left, player.y + 30, 78, 84)
        elif int(player.frame) == 4:
            player.image.clip_draw(115, 661 - 33, 21, 32, player.x- running_server100.background.window_left, player.y + 30, 63, 96)
        elif int(player.frame) == 5:
            player.image.clip_draw(143, 661 - 33, 15, 32, player.x- running_server100.background.window_left, player.y + 30, 45, 96)

class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = StartGame
        self.transitions = {StartGame: {time_out: Run},
                            Run:{}}

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player,e)
                self.cur_state = next_state
                self.cur_state.enter(self.player,e)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.player,('START',0))

    def update(self):
        self.cur_state.do(self.player)

    def draw(self):
        self.cur_state.draw(self.player)

class ComRunningPlayer:
    def __init__(self):
        self.x = 20
        self.y = 250
        self.frame = 1
        self.image = load_image('complayer_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.camera = 0
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x -15, self.y -50, self.x +15, self.y +50

    def handle_collision(self, group, other):
        if group == 'com_player:finishline':
            game_framework.change_mode(you_lose_mode)
            print(group)
