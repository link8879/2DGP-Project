#게임월드 모듈

world = [[],[]]
collision_group = dict()

def add_object(o, depth = 0):
    world[depth].append(o)

# 게임월드 객체들을 몽땅 업데이트
def update():
    for layer in world:
        for o in layer:
            o.update()

# 게임 월드의 객체들을 몽땅 그리기
def render():
    for layer in world:
        for o in layer:
            o.draw()

def clear():
    for layer in world:
        layer.clear()

def add_collision_pairs(a,b, group):
    if group not in collision_group:
        collision_group[group] = [[],[]]
    if a:
        if type(b) is list:
            collision_group[group][1] += b
        else:
            collision_group[group][1].append(b)
    if b:
        if type(a) is list:
            collision_group[group][0] += a
        else:
            collision_group[group][0].append(a)

def all_collision_pairs():
    for group, pairs in collision_group.items():
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group


def all_objects():
    for layer in world:
        for o in layer:
            yield o
