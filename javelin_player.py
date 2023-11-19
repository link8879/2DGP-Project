import time

from pico2d import load_image, clamp, get_canvas_width, get_canvas_height, draw_rectangle, load_music, SDLK_j,SDL_KEYDOWN, SDLK_SPACE

import finish_line
import game_framework
import game_world
import javelin_server
import you_win_mode
from camera import Camera

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 4.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def j_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_j
def land(e):
    return e[0] == 'LAND'

class Ready:
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

        player.velocity += 1.0
        pps = player.change_velocity_to_pps()

        player.x = clamp(0, player.x, javelin_server.background.w-1)
        player.y = clamp(0, player.y, javelin_server.background.h-1)

        TIME_PER_ACTION -= 0.1
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 6

        if TIME_PER_ACTION <= 0.25:
            TIME_PER_ACTION = 0.25
    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def do(player):
        global pps
        global TIME_PER_ACTION
        if pps >= 0.01:
            player.velocity -= 0.01
        else:
            pass


        TIME_PER_ACTION += 0.001

        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 6

        pps = player.change_velocity_to_pps()
        print(pps)
        player.x += pps * game_framework.frame_time
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

    @staticmethod
    def draw(player):
        sx, sy = player.x - javelin_server.background.window_left, player.y - javelin_server.background.window_bottom
        if int(player.frame) == 0:
            player.image.clip_draw(0, 661 - 303, 40, 34, sx, sy, 120, 102)
        elif int(player.frame) == 1:
            player.image.clip_draw(41, 661 - 304, 40, 34,sx, sy, 120, 102)
        elif int(player.frame) == 2:
            player.image.clip_draw(82, 661 - 304, 40, 34, sx,sy, 120, 102)
        elif int(player.frame) == 3:
            player.image.clip_draw(123, 661 - 304, 40, 30, sx, sy, 120, 90)
        elif int(player.frame) == 4:
            player.image.clip_draw(164, 661 - 304, 40, 34, sx, sy, 120, 102)
        elif int(player.frame) == 5:
            player.image.clip_draw(205, 661 - 304, 40, 34, sx, sy, 120, 102)


class Jump:
    @staticmethod
    def enter(player,e):
        # if not player.is_jump:
            #player.x += 10
            player.x = clamp(0, player.x, javelin_server.background.w-1)
            player.y = clamp(0, player.y, javelin_server.background.h-1)
            player.jump_force = 150
            player.is_jumping = True
    @staticmethod
    def exit(player,e):
        player.is_jumping = False
        pass

    @staticmethod
    def do(player):
        global pps
        player.y += player.jump_force * game_framework.frame_time
        player.jump_force -= 200 * game_framework.frame_time

        # 점프 중 수평 운동
        player.x += pps * game_framework.frame_time
        # 이동 범위 제한
        player.x = clamp(0, player.x, javelin_server.background.w - 1)
        player.y = clamp(0, player.y, javelin_server.background.h - 1)
        if player.y <= 130:
            player.state_machine.handle_event(('LAND',0))


    @staticmethod
    def draw(player):
        sx, sy = player.x - javelin_server.background.window_left, player.y - javelin_server.background.window_bottom
        player.image.clip_draw(191, 661 - 72, 31, 19, sx, sy, 93, 57)

class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Ready
        self.transitions = {Ready: {space_down: Run},
                            Run:{space_down: Run,j_down: Jump},
                            Jump:{land: Run}}

    def handle_event(self, e):

        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player,e)
                self.cur_state = next_state
                self.cur_state.enter(self.player,e)
                if javelin_server.background.window_left == 0:
                    pass
                elif javelin_server.background.window_left >= javelin_server.background.w - javelin_server.background.canvas_width - 1:
                    pass
                return True
        return False

    def start(self):
        self.cur_state.enter(self.player,('START',0))

    def update(self):
        self.cur_state.do(self.player)

    def draw(self):
        self.cur_state.draw(self.player)

class Thrower:
    def __init__(self):
        self.x = 20
        self.y = 130
        self.image = load_image('player_animation.png')
        self.frame = 1
        self.action = 0
        self.velocity = 4.0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.jump_force = 0
        self.is_jumping = False
        self.time = time.time()
        self.collision = False
        self.sound = load_music('runningsound_effect.wav')
        self.sound.set_volume(50)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        current_time = time.time()
        if current_time - self.time < 5:
            return
        self.state_machine.handle_event(('INPUT',event))
        self.sound.play()

    def draw(self):
        self.state_machine.draw()
        #draw_rectangle(* self.get_bb())

    def get_bb(self):
        if self.is_jumping:
            return self.x - 45, self.y - 30, self.x + 45, self.y + 30
        else:
            return self.x -15, self.y -50, self.x +15, self.y +50

    def handle_collision(self, group, other):
        if group == 'player:hurdles':
            self.velocity -=0.01
        elif group == 'player:finishline':
            game_framework.change_mode(you_win_mode)



    def change_velocity_to_pps(self):
        PIXEL_PER_METER = (10.0 / 0.3)
        RUN_SPEED_MPM = (self.velocity * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
        return RUN_SPEED_PPS