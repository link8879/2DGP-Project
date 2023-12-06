#달리기 게임 플레이어
import game_framework
import you_win_mode
import time
from pico2d import load_image, clamp, load_wav
from sdl2 import SDL_KEYDOWN, SDLK_SPACE
import running_server

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

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
        global pps
        player.sound.play()
        if player.velocity < 40:
            player.velocity += 1.0
        pps = player.change_velocity_to_pps()

        player.x = clamp(0, player.x, running_server.background.w-1)
        player.y = clamp(0, player.y, running_server.background.h-1)

        player.TIME_PER_ACTION -= 0.1
        player.ACTION_PER_TIME = 1.0 / player.TIME_PER_ACTION
        player.FRAMES_PER_ACTION = 6

        if player.TIME_PER_ACTION <= 0.25:
            player.TIME_PER_ACTION = 0.25
    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def do(player):
        global pps
        if pps >= 0.01:
            player.velocity -= 0.01
        else:
            pass
        player.TIME_PER_ACTION += 0.001
        player.ACTION_PER_TIME = 1.0 / player.TIME_PER_ACTION
        player.FRAMES_PER_ACTION = 6

        pps = player.change_velocity_to_pps()

        player.x += pps * game_framework.frame_time
        player.frame = (player.frame + player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * game_framework.frame_time) % 6

    @staticmethod
    def draw(player):
        sx, sy = player.x - running_server.background.window_left, player.y - running_server.background.window_bottom
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
        self.cur_state = Ready
        self.transitions = {Ready: {space_down: Run},
                            Run:{space_down: Run}}

    def handle_event(self, e,player):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player,e)
                self.cur_state = next_state
                self.cur_state.enter(self.player,e)
                if running_server.background.window_left == 0:
                    pass
                elif running_server.background.window_left >= running_server.background.w - running_server.background.canvas_width - 1:
                    pass
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
        self.sound = load_wav('runningsound_effect.wav')
        self.sound.set_volume(50)
        self.PIXEL_PER_METER = (10 / 0.33)

        self.RUN_SPEED_MPM = (self.velocity * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 6


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        current_time = time.time()
        if current_time - self.time < 5:
            return
        self.state_machine.handle_event(('INPUT',event),self)

    def draw(self):
        self.state_machine.draw()
        #draw_rectangle(* self.get_bb())

    def get_bb(self):
        return self.x -15, self.y -50, self.x +15, self.y +50

    def handle_collision(self, group, other):
        if group == 'player:finishline':
            game_framework.change_mode(you_win_mode)


    def change_velocity_to_pps(self):
        PIXEL_PER_METER = (10/0.33)
        self.PIXEL_PER_METER = (10 / 0.33)
        self.RUN_SPEED_MPM = (self.velocity * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)
        return self.RUN_SPEED_PPS
