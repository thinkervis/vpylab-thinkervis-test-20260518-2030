from vpython import *
import math, random

# 반딧불 은하 오르골
# VPyLab 문서에서 확인한 sphere, ring, helix, curve, label, local_light, rate를 섞어 만든 작은 우주 풍경입니다.

scene_background(color.black)
local_light(pos=vector(0, 5, 4), color=color.white)
local_light(pos=vector(-4, -2, 3), color=vector(0.2, 0.5, 1.0))

label(pos=vector(0, 3.4, 0), text="반딧불 은하 오르골", height=18, color=color.cyan)
label(pos=vector(0, 3.0, 0), text="행성은 돌고, 별은 깜빡이고, 반딧불은 리듬처럼 숨을 쉽니다", height=9, color=color.white)

# 중심 별과 은하 원반
sun = sphere(pos=vector(0, 0, 0), radius=0.45, color=color.yellow)
ring(pos=vector(0, 0, 0), axis=vector(0, 1, 0), radius=1.15, thickness=0.015, color=color.orange)
ring(pos=vector(0, 0, 0), axis=vector(0, 1, 0), radius=2.05, thickness=0.015, color=color.cyan)
ring(pos=vector(0, 0, 0), axis=vector(0, 1, 0), radius=2.95, thickness=0.015, color=color.magenta)
helix(pos=vector(0, -0.18, 0), axis=vector(0, 0.36, 0), radius=3.2, coils=4, thickness=0.02, color=vector(0.4, 0.25, 1.0))

# 배경 별
stars = []
for i in range(95):
    p = vector(random.uniform(-7, 7), random.uniform(-4, 4), random.uniform(-5, 5))
    r = random.uniform(0.018, 0.05)
    c = vector(random.uniform(0.45, 1.0), random.uniform(0.45, 1.0), 1.0)
    stars.append((sphere(pos=p, radius=r, color=c), random.uniform(0, 6.28)))

# 행성들: 반지름, 크기, 색, 속도
planet_specs = [
    (1.15, 0.10, color.cyan, 1.9),
    (2.05, 0.15, color.green, 1.15),
    (2.95, 0.20, color.magenta, 0.72),
]
planets = []
for idx, (orbit, size, col, speed) in enumerate(planet_specs):
    angle = idx * 2.1
    body = sphere(pos=vector(math.cos(angle) * orbit, 0, math.sin(angle) * orbit), radius=size, color=col)
    body.attach_trail(color=col, radius=size * 0.18, retain=90)
    planets.append((body, orbit, speed, angle))

# 반딧불이 — 각각 다른 위상으로 깜빡이며 위아래로 움직임
fireflies = []
for i in range(26):
    angle = 2 * math.pi * i / 26
    radius = random.uniform(3.5, 5.7)
    y = random.uniform(-1.4, 1.8)
    bug = sphere(pos=vector(math.cos(angle) * radius, y, math.sin(angle) * radius), radius=0.055, color=vector(1, 0.9, 0.25))
    fireflies.append((bug, angle, radius, y, random.uniform(0.5, 1.7)))

# 유성
comet = sphere(pos=vector(-4, 2, 0), radius=0.11, color=color.white)
comet.attach_trail(color=color.cyan, radius=0.025, retain=60)

# 오로라 리본: 작은 구슬 줄로 구성해서 파도처럼 흔들기
ribbons = []
for row, base_y in enumerate([2.0, 2.25, 2.5]):
    beads = []
    for i in range(34):
        x = -5.5 + i * 0.33
        col = [color.cyan, color.green, color.magenta][row]
        beads.append(sphere(pos=vector(x, base_y, -3.3), radius=0.035, color=col))
    ribbons.append((beads, base_y, row))

clock = 0
while True:
    rate(60)
    clock += 0.025

    # 태양 숨쉬기
    sun.radius = 0.45 + 0.05 * math.sin(clock * 3)

    # 별 반짝임
    for st, phase in stars:
        glow = 0.55 + 0.45 * math.sin(clock * 2.2 + phase)
        st.radius = 0.018 + 0.025 * glow

    # 행성 공전
    for i in range(len(planets)):
        body, orbit, speed, angle0 = planets[i]
        a = angle0 + clock * speed
        body.pos = vector(math.cos(a) * orbit, 0.25 * math.sin(a * 1.7), math.sin(a) * orbit)

    # 반딧불이 군무
    for bug, angle0, radius, base_y, speed in fireflies:
        a = angle0 + clock * speed * 0.45
        pulse = 0.5 + 0.5 * math.sin(clock * 5 * speed + angle0)
        bug.pos = vector(math.cos(a) * radius, base_y + 0.35 * math.sin(clock * speed + angle0), math.sin(a) * radius)
        bug.radius = 0.035 + 0.055 * pulse
        bug.color = vector(0.35 + 0.65 * pulse, 0.75 + 0.25 * pulse, 0.18)

    # 유성 왕복
    comet.pos = vector(-4.8 + (clock * 1.2 % 9.6), 1.9 - 0.45 * math.sin(clock * 1.2), 1.8 * math.sin(clock * 0.8))

    # 오로라 흔들림
    for beads, base_y, row in ribbons:
        for i, bead in enumerate(beads):
            wave = math.sin(clock * (1.6 + row * 0.35) + i * 0.38)
            bead.pos.y = base_y + 0.28 * wave
            bead.radius = 0.025 + 0.035 * (0.5 + 0.5 * wave)
