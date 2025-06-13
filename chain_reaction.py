import pygame
import random
import math

# Screen dimensions
WIDTH, HEIGHT = 800, 600
FPS = 60

# Ball settings
START_RADIUS = 30
MIN_RADIUS = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Ball:
    def __init__(self, pos, radius, velocity=None, color=None):
        self.x, self.y = pos
        self.radius = radius
        if velocity is None:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 4)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
        else:
            self.vx, self.vy = velocity
        self.color = color or [random.randint(50, 255) for _ in range(3)]

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx *= -1
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vy *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def collide(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        return distance <= self.radius + other.radius

    def split(self):
        if self.radius // 2 < MIN_RADIUS:
            return []
        new_radius = self.radius // 2
        children = []
        for _ in range(2):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 4)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            child = Ball((self.x, self.y), new_radius, (vx, vy), self.color)
            children.append(child)
        return children


balls = [Ball((random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100)), START_RADIUS) for _ in range(5)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(Ball(event.pos, START_RADIUS))

    screen.fill((30, 30, 30))

    new_balls = []
    removed = set()
    for i in range(len(balls)):
        if i in removed:
            continue
        for j in range(i + 1, len(balls)):
            if j in removed:
                continue
            if balls[i].collide(balls[j]):
                new_balls.extend(balls[i].split())
                new_balls.extend(balls[j].split())
                removed.update([i, j])
                break

    balls = [b for idx, b in enumerate(balls) if idx not in removed]
    balls.extend(new_balls)

    for ball in balls:
        ball.move()
        ball.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
