from pico2d import load_image, load_music, clamp, load_wav, load_font

import game_framework
import javelin_mode
import javelin_server
import javelin_you_lose_mode
import javelin_you_win_mode
import time

def land(e):
    return e[0] == 'LAND'

def calculate_all_distance():

    player_max_distance = 0
    com_player_max_distance = 0

    for i in javelin_server.flying_distance:
        if i > player_max_distance:
            player_max_distance = i

    for i in javelin_server.com_flying_distance:
        if i > com_player_max_distance:
            com_player_max_distance = i

    if player_max_distance > com_player_max_distance:
        game_framework.change_mode(javelin_you_win_mode)
    else:
        game_framework.change_mode(javelin_you_lose_mode)

class Flying:
    @staticmethod
    def enter(player,e):

        pass
    @staticmethod
    def exit(player,e):
        player.landing_sound.play()
        player.flying_sound.stop()
        pass

    @staticmethod
    def do(player):
        global distance
        pps = player.change_velocity_to_pps()
        player.y += player.strength * game_framework.frame_time
        player.strength -= 100 * game_framework.frame_time

        # 점프 중 수평 운동
        player.x += pps * game_framework.frame_time
        # 이동 범위 제한
        player.x = clamp(0, player.x, javelin_server.background.w - 1)
        player.y = clamp(0, player.y, javelin_server.background.h - 1)
        if player.y <= 130:
            player.velocity = 0
            pps = 0
            player.y = 130
            player.state_machine.handle_event(('LAND', 0))

        pass

    @staticmethod
    def draw(player):
        global distance
        sx, sy = player.x - javelin_server.background.window_left, player.y - javelin_server.background.window_bottom
        step = distance / 7
        if player.x - player.throwLocation < step:
            player.image.clip_draw(5, 661 - 346, 28, 28, sx, sy, 84, 84)
        elif player.x - player.throwLocation < 2 * step:
            player.image.clip_draw(40, 661 - 336, 40, 14, sx, sy, 120, 42)
        elif player.x - player.throwLocation < 3 * step:
            player.image.clip_draw(98, 661 - 324, 40, 2, sx, sy, 120, 6)
        elif player.x - player.throwLocation < 4 * step:
            player.image.clip_draw(157, 661 - 335, 40, 14, sx, sy, 120, 42)
        elif player.x - player.throwLocation < 5 * step:
            player.image.clip_draw(215, 661 - 336, 36, 18, sx, sy, 108, 54)
        elif player.x - player.throwLocation < 6 * step:
            player.image.clip_draw(273, 661 - 357, 28, 28, sx, sy, 84, 84)
        else:
            player.image.clip_draw(326, 661 - 358, 18, 36, sx, sy, 54, 108)


class Landing:
    @staticmethod
    def enter(player,e):
        pass
    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def do(player):
        player.timer += game_framework.frame_time

        if player.timer > 1.0 and not player.music_played:
            player.after_landing_music.play()
            player.music_played = True

        if player.timer > 7.0:
            if len(javelin_server.com_flying_distance) == 3:    #나중에 3으로 바꿔야 함
                calculate_all_distance()                    # 승패판정
            else:
                game_framework.change_mode(javelin_mode)
        pass

    @staticmethod
    def draw(player):
        sx, sy = player.x - javelin_server.background.window_left, player.y - javelin_server.background.window_bottom
        font = load_font('ENCR10B.TTF', 20)
        temp = ((player.init_x + distance) - javelin_server.foul_line.x) * 0.033
        print(temp)
        if distance+player.init_x < javelin_server.foul_line.x:
            temp = 0

        font.draw(100, 100, 'Distance: %.2fm' %temp,
                  (255, 255, 255))
        player.image.clip_draw(326, 661 - 358, 18, 36, sx, sy, 54, 108)

class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Flying
        self.transitions = {Flying: {land:Landing},
                           Landing: {}}
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

class ComJavelin:
    def __init__(self,velocity,x,y):

        self.x = x
        self.init_x = x
        self.y = y
        self.throwLocation = x
        self.image = load_image('player_animation.png')
        self.frame = 1
        self.action = 0
        self.velocity = velocity
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.strength = velocity * 10
        self.time = time.time()
        self.timer = 0
        self.music_played = False

        self.landing_sound = load_wav('javelin_landing_sound.wav')
        self.landing_sound.set_volume(100)

        self.flying_sound = load_music('flying_sound.wav')
        self.flying_sound.set_volume(100)
        self.flying_sound.repeat_play()

        self.after_landing_music = load_music('after_landing_music.mp3')
        self.after_landing_music.set_volume(100)

        global distance
        pps = self.change_velocity_to_pps()
        flight_time = 2 * self.strength / 100
        distance = flight_time * pps

        temp = 0

        if distance + self.x < javelin_server.foul_line.x:
            temp = 0
        else:
            temp = ((self.x + distance) - javelin_server.foul_line.x) * 0.033

        javelin_server.com_flying_distance.append(temp)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        current_time = time.time()
        if current_time - self.time < 5:
            return
        self.state_machine.handle_event(('INPUT',event))

    def draw(self):
        self.state_machine.draw()
        #draw_rectangle(* self.get_bb())

    def get_bb(self):
        return self.x -15, self.y -50, self.x +15, self.y +50

    def handle_collision(self, group, other):
       pass



    def change_velocity_to_pps(self):
        PIXEL_PER_METER = (10.0 / 0.33)
        RUN_SPEED_MPM = (self.velocity * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
        return RUN_SPEED_PPS
