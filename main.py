from vpython import *
import math, random

# 반딧불 은하 오르골 v2 — 인터랙티브 밤하늘
# 석리송님의 조명 변경(local_light y=15)을 살리고,
# 문서 기능(sphere/ring/helix/label/local_light/attach_trail/rate/keysdown/scene.mouse)을 더 섞었습니다.

scene_background(color.black)
local_light(pos=vector(0, 15, 4), color=color.white)
local_light(pos=vector(-4, -2, 3), color=vector(0.2, 0.5, 1.0))
local_light(pos=vector(4, 2, -3), color=vector(1.0, 0.45, 0.2))

label(pos=vector(0, 3.55, 0), text="반딧불 은하 오르골 v2", height=18, color=color.cyan)
label(pos=vector(0, 3.16, 0), text="방향키/WASD: 은하 바람 · Space: 반짝임 모드 · 마우스 위치: 오로라 지휘", height=8, color=color.white)

# 중심 별과 은하 원반
sun = sphere(pos=vector(0, 0, 0), radius=0.45, color=color.yellow)
ring(pos=vector(0, 0, 0), axis=vector(0, 1, 0), radius=1.15, thickness=0.015, color=color.orange)
ring(pos=vector(0, 0, 0), axis=vector(0, 1, 0), radius=2.05, thickness=0.015, color=color.cyan)
ring(pos=vector(0, 0, 0), axis=vector(0, 1, 0), radius=2.95, thickness=0.015, color=color.magenta)
helix(pos=vector(0, -0.18, 0), axis=vector(0, 0.36, 0), radius=3.2, coils=4, thickness=0.02, color=vector(0.4, 0.25, 1.0))

# 배경 별
stars = []
for i in range(120):
    p = vector(random.uniform(-7, 7), random.uniform(-4, 4), random.uniform(-5, 5))
    r = random.uniform(0.018, 0.05)
    c = vector(random.uniform(0.45, 1.0), random.uniform(0.45, 1.0), 1.0)
    stars.append((sphere(pos=p, radius=r, color=c), random.uniform(0, 6.28), r))

# 별자리 — 점들을 curve로 연결
constellation_points = [
    vector(-5.2, 2.7, -2.4), vector(-4.4, 2.95, -2.2), vector(-3.7, 2.55, -2.5),
    vector(-3.05, 2.85, -2.25), vector(-2.35, 2.45, -2.55)
]
for p in constellation_points:
    sphere(pos=p, radius=0.07, color=color.white)
constellation = curve(color=vector(0.55, 0.85, 1.0), radius=0.012)
for p in constellation_points:
    constellation.append(p)
label(pos=vector(-3.7, 3.25, -2.3), text="작은 요정자리", height=8, color=vector(0.55, 0.85, 1.0))

# 행성들: 반지름, 크기, 색, 속도
planet_specs = [
    (1.15, 0.10, color.cyan, 1.9),
    (2.05, 0.15, color.green, 1.15),
    (2.95, 0.20, color.magenta, 0.72),
    (3.55, 0.12, vector(1, 0.55, 0.15), 0.48),
]
planets = []
for idx, (orbit, size, col, speed) in enumerate(planet_specs):
    angle = idx * 2.1
    body = sphere(pos=vector(math.cos(angle) * orbit, 0, math.sin(angle) * orbit), radius=size, color=col)
    body.attach_trail(color=col, retain=110)
    planets.append((body, orbit, speed, angle))

# 반딧불이 — 각각 다른 위상으로 깜빡이며 위아래로 움직임
fireflies = []
for i in range(34):
    angle = 2 * math.pi * i / 34
    radius = random.uniform(3.5, 5.9)
    y = random.uniform(-1.4, 1.8)
    bug = sphere(pos=vector(math.cos(angle) * radius, y, math.sin(angle) * radius), radius=0.055, color=vector(1, 0.9, 0.25))
    fireflies.append((bug, angle, radius, y, random.uniform(0.5, 1.7)))

# 유성 3개
comets = []
for i in range(3):
    comet = sphere(pos=vector(-4, 2, i - 1), radius=0.09 + 0.02 * i, color=color.white)
    comet.attach_trail(color=[color.cyan, color.magenta, color.orange][i], retain=55)
    comets.append((comet, i * 2.3))

# 오로라 리본: 작은 구슬 줄로 구성해서 파도처럼 흔들기
ribbons = []
for row, base_y in enumerate([2.0, 2.25, 2.5, 2.75]):
    beads = []
    for i in range(38):
        x = -5.9 + i * 0.32
        col = [color.cyan, color.green, color.magenta, vector(1, 0.8, 0.25)][row]
        beads.append(sphere(pos=vector(x, base_y, -3.3), radius=0.032, color=col))
    ribbons.append((beads, base_y, row))

# 조작 상태
clock = 0
wind = vector(0, 0, 0)
speed_boost = 1.0
sparkle_mode = False
last_space = False

while True:
    rate(60)
    clock += 0.025 * speed_boost

    # 키 입력: 은하 바람과 속도 조절
    keys = keysdown()
    wind = vector(0, 0, 0)
    if 'ArrowLeft' in keys or 'left' in keys or 'a' in keys:
        wind.x -= 0.18
    if 'ArrowRight' in keys or 'right' in keys or 'd' in keys:
        wind.x += 0.18
    if 'ArrowUp' in keys or 'up' in keys or 'w' in keys:
        wind.y += 0.10
        speed_boost = 1.65
    else:
        speed_boost = 1.0
    if 'ArrowDown' in keys or 'down' in keys or 's' in keys:
        wind.y -= 0.10
    space_now = ' ' in keys or 'Space' in keys or 'space' in keys
    if space_now and not last_space:
        sparkle_mode = not sparkle_mode
    last_space = space_now

    # 마우스 위치로 오로라 강도 살짝 지휘
    mouse_x = scene.mouse.pos.x if scene.mouse else 0
    conductor = max(-1, min(1, mouse_x / 5))

    # 태양 숨쉬기
    sun.radius = 0.45 + 0.06 * math.sin(clock * 3)
    sun.color = vector(1, 0.75 + 0.2 * math.sin(clock * 2), 0.1)

    # 별 반짝임
    for st, phase, base_r in stars:
        glow = 0.55 + 0.45 * math.sin(clock * (3.8 if sparkle_mode else 2.2) + phase)
        st.radius = base_r * (0.8 + 1.2 * glow)

    # 행성 공전
    for i in range(len(planets)):
        body, orbit, speed, angle0 = planets[i]
        a = angle0 + clock * speed
        body.pos = vector(math.cos(a) * orbit, 0.25 * math.sin(a * 1.7), math.sin(a) * orbit) + wind

    # 반딧불이 군무
    for bug, angle0, radius, base_y, speed in fireflies:
        a = angle0 + clock * speed * 0.45
        pulse = 0.5 + 0.5 * math.sin(clock * 5 * speed + angle0)
        spiral = radius + 0.15 * math.sin(clock * 1.3 + angle0)
        bug.pos = vector(math.cos(a) * spiral, base_y + 0.35 * math.sin(clock * speed + angle0), math.sin(a) * spiral) + wind
        bug.radius = 0.035 + 0.055 * pulse
        bug.color = vector(0.35 + 0.65 * pulse, 0.75 + 0.25 * pulse, 0.18 + (0.35 if sparkle_mode else 0))

    # 유성 왕복
    for comet, phase in comets:
        comet.pos = vector(-4.8 + ((clock * 1.15 + phase) % 9.6), 1.9 - 0.45 * math.sin(clock * 1.2 + phase), 1.8 * math.sin(clock * 0.8 + phase))

    # 오로라 흔들림
    for beads, base_y, row in ribbons:
        for i, bead in enumerate(beads):
            wave = math.sin(clock * (1.6 + row * 0.35) + i * 0.38 + conductor)
            bead.pos.y = base_y + 0.28 * wave + 0.08 * conductor
            bead.radius = 0.025 + 0.04 * (0.5 + 0.5 * wave)
