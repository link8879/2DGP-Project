#달리기 게임 플레이어
from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_SPACE


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

class StartGame:
    @staticmethod
    def enter(player,e):
        pass

    @staticmethod
    def do(player):
        print("준비")
        pass

    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(6,661-150,31-6,150-131,100,100,50,80)


class Run:
    @staticmethod
    def enter(player,e):

        player.x += 50
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
        if player.frame == 0:
            player.image.clip_draw(8,661-33,11,32,player.x+100,player.y+50,50,90)
        elif player.frame == 1:
            player.image.clip_draw(8, 661 - 33, 11, 32, player.x + 100, player.y + 50, 50, 90)

class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = StartGame
        self.transitions = {StartGame: {space_down: Run},
                            Run:{space_down: Run}}

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

class RunningPlayer:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.image = load_image('player_animation.png')
        self.frame = 0
        self.action = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT',event))

    def draw(self):
        self.state_machine.draw()

