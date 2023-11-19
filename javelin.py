from pico2d import load_image, load_music

import game_framework
import javelin_server
import you_win_mode
import time

class Flying:
    @staticmethod
    def enter(player,e):
        pass
    @staticmethod
    def exit(player,e):
        player.is_jumping = False
        pass

    @staticmethod
    def do(player):
        # global pps
        # player.y += player.jump_force * game_framework.frame_time
        # player.jump_force -= 200 * game_framework.frame_time
        #
        # # 점프 중 수평 운동
        # player.x += pps * game_framework.frame_time
        # # 이동 범위 제한
        # player.x = clamp(0, player.x, javelin_server.background.w - 1)
        # player.y = clamp(0, player.y, javelin_server.background.h - 1)
        # if player.y <= 130:
        #     player.state_machine.handle_event(('LAND',0))
        pass

    @staticmethod
    def draw(player):
        sx, sy = player.x - javelin_server.background.window_left, player.y - javelin_server.background.window_bottom
        # player.image.clip_draw(191, 661 - 72, 31, 19, sx, sy, 93, 57)
        player.image.clip_draw(5,661-346,28,28,sx,sy,84,84)
        pass

class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Flying

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

class Javelin:
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
