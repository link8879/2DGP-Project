from pico2d import open_canvas, delay, close_canvas

from running100_mode import init, handle_events, update, draw, finish

open_canvas(800,600)
init()
playing = True
while playing:
    # image.clip_draw(8,661-33,11,32,100,100,50,80) # 달리기 처음 위치
    #image.clip_draw(6,661-150,31-6,150-131,100,100,50,80) #달리기 준비 모션
    #update_canvas()
    handle_events()
    update()
    draw()
    delay(0.01)
finish()
close_canvas()