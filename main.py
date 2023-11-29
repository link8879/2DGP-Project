from pico2d import open_canvas, delay, close_canvas
import game_framework
import hurdle110_mode
import javelin_mode
import running100_mode
import title_mode
import you_win_mode

open_canvas(800,600)
game_framework.run(title_mode) #테스트 타임 줄이기 위함
close_canvas()
# open_canvas(800,600)
# title_mode.init()
# playing = True
# while playing:
#     # image.clip_draw(8,661-33,11,32,100,100,50,80) # 달리기 처음 위치
#     #image.clip_draw(6,661-150,31-6,150-131,100,100,50,80) #달리기 준비 모션
#     #update_canvas()
#     title_mode.handle_events()
#     title_mode.update()
#     title_mode.draw()
#     delay(0.01)
# title_mode.finish()
# close_canvas()

