import time

from pico2d import load_image, clamp, get_canvas_width, get_canvas_height, draw_rectangle, load_music, SDLK_j, \
    SDL_KEYDOWN, SDLK_SPACE, get_time

import finish_line
import game_framework
import game_world
import running_server
import you_lose_mode
import you_win_mode
from camera import Camera

PIXEL_PER_METER = (10/0.33)
RUN_SPEED_KMPH = 17.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

def turn_jump(e):
    return e[0] == 'JUMP'

def land(e):
    return e[0] == 'LAND'

class Ready:
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
    time_elapsed = 0
    @staticmethod
    def enter(player,e):
        global TIME_PER_ACTION
        global ACTION_PER_TIME
        global FRAMES_PER_ACTION
        global pps

        player.velocity += 1.0
        pps = player.change_velocity_to_pps()

        player.x = clamp(0, player.x, running_server.background.w-1)
        player.y = clamp(0, player.y, running_server.background.h-1)
    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def do(player):
        player.x += RUN_SPEED_PPS * game_framework.frame_time
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

    @staticmethod
    def draw(player):
        if int(player.frame) == 0:
            player.image.clip_draw(28, 661 - 33, 12, 32, player.x - running_server.background.window_left,
                                   player.y + 30, 36, 96)
        elif int(player.frame) == 1:
            player.image.clip_draw(46, 661 - 33, 14, 32, player.x - running_server.background.window_left,
                                   player.y + 30, 42, 96)
        elif int(player.frame) == 2:
            player.image.clip_draw(62, 661 - 33, 16, 32, player.x - running_server.background.window_left,
                                   player.y + 30, 48, 96)
        elif int(player.frame) == 3:
            player.image.clip_draw(81, 661 - 33, 26, 28, player.x - running_server.background.window_left,
                                   player.y + 30, 78, 84)
        elif int(player.frame) == 4:
            player.image.clip_draw(115, 661 - 33, 21, 32, player.x - running_server.background.window_left,
                                   player.y + 30, 63, 96)
        elif int(player.frame) == 5:
            player.image.clip_draw(143, 661 - 33, 15, 32, player.x - running_server.background.window_left,
                                   player.y + 30, 45, 96)


class Jump:
    @staticmethod
    def enter(player,e):
            player.x = clamp(0, player.x, running_server.background.w-1)
            player.y = clamp(0, player.y, running_server.background.h-1)
            player.strength = 150
            player.is_jumping = True
    @staticmethod
    def exit(player,e):
        player.is_jumping = False
        pass

    @staticmethod
    def do(player):
        global pps
        player.y += player.strength * game_framework.frame_time
        player.strength -= 320 * game_framework.frame_time

        # 점프 중 수평 운동
        player.x += RUN_SPEED_PPS * game_framework.frame_time
        if player.y <= 250:
            player.state_machine.handle_event(('LAND',0))


    @staticmethod
    def draw(player):
        sx, sy = player.x - running_server.background.window_left, player.y - running_server.background.window_bottom
        player.image.clip_draw(191, 661 - 72, 31, 19, sx, sy, 93, 57)

class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Ready
        self.transitions = {Ready: {time_out: Run},
                            Run:{turn_jump: Jump},
                            Jump:{land: Run}}

    def handle_event(self, e):

        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player,e)
                self.cur_state = next_state
                self.cur_state.enter(self.player,e)
                if running_server.background.window_left == 0:
                    pass
                elif running_server.background.window_left >= running_server.background.w - running_server.background.canvas_width - 1:
                    pass
                else:
                    running_server.com_player.camera -= 50


                return True
        return False

    def start(self):
        self.cur_state.enter(self.player,('START',0))

    def update(self):
        self.cur_state.do(self.player)

    def draw(self):
        self.cur_state.draw(self.player)

class ComHardHurdleRunner:
    def __init__(self):
        self.x = 20
        self.y = 250
        self.image = load_image('complayer_animation.png')
        self.frame = 1
        self.action = 0
        self.velocity = 10.0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.jump_force = 0
        self.is_jumping = False
        self.camera = 0

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT',event))

    def draw(self):
        self.state_machine.draw()
        #draw_rectangle(* self.get_bb())

    def get_bb(self):
        if self.is_jumping:
            return self.x - 45, self.y - 30, self.x + 45, self.y + 30
        else:
            return self.x -35, self.y -50, self.x +35, self.y +50

    def handle_collision(self, group, other):
        if group == 'com_player:hurdles':
             self.state_machine.handle_event(('JUMP',0))
        elif group == 'com_player:finishline':
            game_framework.change_mode(you_lose_mode)

    def change_velocity_to_pps(self):
        PIXEL_PER_METER = 10/0.33
        RUN_SPEED_MPM = (self.velocity * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
        return RUN_SPEED_PPS


