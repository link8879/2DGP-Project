#달리기 게임 플레이어
import game_framework

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 0.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

import time

from pico2d import load_image, clamp, get_canvas_width, get_canvas_height, draw_rectangle, load_music
from sdl2 import SDL_KEYDOWN, SDLK_SPACE

import finish_line
import running_server100
from camera import Camera

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

class StartGame:
    @staticmethod
    def enter(player,e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def exit(player,e):

        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(6,661-150,31-6,150-131,30,100,75,57)

class Run:
    time_elapsed = 0
    @staticmethod
    def enter(player,e):
        global TIME_PER_ACTION
        global ACTION_PER_TIME
        global FRAMES_PER_ACTION
        global pps

        player.velocity += 0.5
        pps = player.change_velocity_to_pps()

        player.x = clamp(0, player.x, running_server100.background.w-1)
        player.y = clamp(0, player.y, running_server100.background.h-1)

        TIME_PER_ACTION -= 0.01
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 6

        if TIME_PER_ACTION <= 0.25:
            TIME_PER_ACTION += 0.01
    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def do(player):
        global pps
        global TIME_PER_ACTION
        if pps >= 0.0:
            player.velocity -= 0.01
        else:
            pass

        if TIME_PER_ACTION <= 0.5:
            TIME_PER_ACTION += 0.001

        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 6

        pps = player.change_velocity_to_pps()

        player.x += pps * game_framework.frame_time
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        print(pps)


    @staticmethod
    def draw(player):
        sx, sy = player.x - running_server100.background.window_left, player.y - running_server100.background.window_bottom
        if int(player.frame) == 0:
            player.image.clip_draw(28, 661 - 33, 12, 32, sx, sy, 36, 96)
        elif int(player.frame) == 1:
            player.image.clip_draw(46, 661 - 33, 14, 32,sx, sy, 42, 96)
        elif int(player.frame) == 2:
            player.image.clip_draw(62, 661 - 33, 16, 32, sx,sy, 48, 96)
        elif int(player.frame) == 3:
            player.image.clip_draw(81, 661 - 33, 26, 28, sx, sy, 78, 84)
        elif int(player.frame) == 4:
            player.image.clip_draw(115, 661 - 33, 21, 32, sx, sy, 63, 96)
        elif int(player.frame) == 5:
            player.image.clip_draw(143, 661 - 33, 15, 32, sx, sy, 45, 96)

class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = StartGame
        self.transitions = {StartGame: {space_down: Run},
                            Run:{space_down: Run}}

    def handle_event(self, e,player):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player,e)
                self.cur_state = next_state
                self.cur_state.enter(self.player,e)
                if running_server100.background.window_left == 0:
                    pass
                elif running_server100.background.window_left >= running_server100.background.w - running_server100.background.canvas_width - 1:
                    pass
                else:
                    running_server100.com_player.camera -= 50
                return True
        return False

    def start(self):
        self.cur_state.enter(self.player,('START',0))

    def update(self):
        self.cur_state.do(self.player)

    def draw(self):
        self.cur_state.draw(self.player)

class Runner:
    def __init__(self):
        self.x = 20
        self.y = 130
        self.image = load_image('player_animation.png')
        self.frame = 1
        self.action = 0
        self.velocity = 4.0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.space_down_count = 0
        self.time = time.time()
        self.sound = load_music('runningsound_effect.wav')
        self.sound.set_volume(50)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        current_time = time.time()
        if current_time - self.time < 5:
            return
        self.state_machine.handle_event(('INPUT',event),self)
        self.sound.play()

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(* self.get_bb())

    def get_bb(self):
        return self.x -13, self.y -16, self.x +13, self.y +16

    def handle_collision(self, other, group):
        pass

    def change_velocity_to_pps(self):
        PIXEL_PER_METER = (10.0 / 0.3)
        RUN_SPEED_MPM = (self.velocity * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
        return RUN_SPEED_PPS
