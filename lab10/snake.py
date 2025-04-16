import pygame
import sys
import random
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="PhoneBook",
    user="qurmanbek",
    password="yourpassword"
)
cur = conn.cursor()

player_name = input("Enter your name: ")
score = 0
FPS = 5

pygame.init()
HEIGHT = 600
WIDTH = 600
grid_SIZE = 20
grid_WIDTH = WIDTH // grid_SIZE
grid_HEIGHT = HEIGHT // grid_SIZE
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
FOOD_TIMEOUT = 5000

def drawGrid(surface):
    for y in range(grid_HEIGHT):
        for x in range(grid_WIDTH):
            r = pygame.Rect((x * grid_SIZE, y * grid_SIZE), (grid_SIZE, grid_SIZE))
            color = (93, 216, 228) if (x + y) % 2 == 0 else (84, 194, 205)
            pygame.draw.rect(surface, color, r)

class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17, 24, 47)

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * grid_SIZE)) % WIDTH), (cur[1] + (y * grid_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        global score, FPS
        cur.execute("INSERT INTO snake_results (player_name, score) VALUES (%s, %s)", (player_name, score))
        conn.commit()
        print(f"☠️ Game over! Score saved: {player_name} — {score}")
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        score = 0
        FPS = 5

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (grid_SIZE, grid_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def handle_keys(self):
        global score, FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: self.turn(UP)
                elif event.key == pygame.K_DOWN: self.turn(DOWN)
                elif event.key == pygame.K_LEFT: self.turn(LEFT)
                elif event.key == pygame.K_RIGHT: self.turn(RIGHT)
                elif event.key == pygame.K_p:
                    cur.execute("INSERT INTO snake_results (player_name, score) VALUES (%s, %s)", (player_name, score))
                    conn.commit()
                    print(f"💾 Saved manually: {player_name} — {score}")

class Food(object):
    def __init__(self):
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_WIDTH - 1) * grid_SIZE,
                         random.randint(0, grid_HEIGHT - 1) * grid_SIZE)
        self.weight = random.randint(1, 3)
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (grid_SIZE, grid_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)
        font = pygame.font.SysFont("monospace", 16)
        text = font.render(str(self.weight), True, (0, 0, 0))
        surface.blit(text, text.get_rect(center=r.center))

snake = Snake()
food = Food()
myfont = pygame.font.SysFont("monospace", 16)

while True:
    snake.handle_keys()
    drawGrid(surface)
    snake.move()

    if pygame.time.get_ticks() - food.spawn_time > FOOD_TIMEOUT:
        food.randomize_position()

    if snake.get_head_position() == food.position:
        snake.length += food.weight
        score += food.weight
        FPS += food.weight
        food.randomize_position()

    snake.draw(surface)
    food.draw(surface)

    screen.blit(surface, (0, 0))
    text = myfont.render("Score: {0}".format(score), 1, (0, 0, 0))
    screen.blit(text, (5, 10))

    pygame.display.flip()
    clock.tick(FPS)
