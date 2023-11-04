#달리기 게임 플레이어
from pico2d import load_image, clamp, get_canvas_width, get_canvas_height, draw_rectangle
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
    @staticmethod
    def enter(player,e):
        #if player.x <= 500 or player.space_down_count >= 84:
        player.x += 10
        player.x = clamp(0, player.x, running_server100.background.w-1)
        player.y = clamp(0, player.y, running_server100.background.h-1)
    @staticmethod
    def exit(player,e):
        player.frame += 1
        pass

    @staticmethod
    def do(player):
        pass
        #player.frame = (player.frame + 1) % 8

    @staticmethod
    def draw(player):
        sx, sy = player.x - running_server100.background.window_left, player.y - running_server100.background.window_bottom

        # if player.frame == 0:
        #     player.image.clip_draw(8,661-33,11,32,player.x+100,player.y+50,50,90)
        if player.frame == 1:
            player.image.clip_draw(28, 661 - 33, 12, 32, sx, sy, 36, 96)
        elif player.frame == 2:
            player.image.clip_draw(46, 661 - 33, 14, 32,sx, sy, 42, 96)
        elif player.frame == 3:
            player.image.clip_draw(62, 661 - 33, 16, 32, sx,sy, 48, 96)
        elif player.frame == 4:
            player.image.clip_draw(81, 661 - 33, 26, 28, sx, sy, 78, 84)
        elif player.frame == 5:
            player.image.clip_draw(115, 661 - 33, 21, 32, sx, sy, 63, 96)
        elif player.frame == 6:
            player.image.clip_draw(143, 661 - 33, 15, 32, sx, sy, 45, 96)
            player.frame = 1

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
                player.space_down_count += 1
                if running_server100.background.window_left == 0:
                    print("스크롤이 왼쪽 끝에 도달했습니다.")
                elif running_server100.background.window_left >= running_server100.background.w - running_server100.background.canvas_width - 1:
                    print("스크롤이 오른쪽 끝에 도달했습니다.")
                else:
                    running_server100.com_player.x -= 10

                print(player.space_down_count)
                print(player.x)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.player,('START',0))

    def update(self):
        self.cur_state.do(self.player)

    def draw(self):
        self.cur_state.draw(self.player)

class RunningPlayer:
    def __init__(self):
        self.x = 20
        self.y = 130
        self.image = load_image('player_animation.png')
        self.frame = 1
        self.action = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.space_down_count = 0

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT',event),self)

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(* self.get_bb())

    def get_bb(self):
        return self.x -13, self.y -16, self.x +13, self.y +16

    def handle_collision(self, other, group):
        pass