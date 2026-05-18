from vpython import *
# 팅커비스가 만든 테스트 프로젝트
ball = sphere(pos=vector(0, 0, 0), radius=0.5, color=color.cyan)
ball.velocity = vector(1, 0, 0)
dt = 0.01
while True:
    rate(100)
    ball.pos = ball.pos + ball.velocity * dt
    if abs(ball.pos.x) > 5:
        ball.velocity.x = -ball.velocity.x
