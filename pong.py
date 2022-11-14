import pygame as pg
import os

pg.init()
WIDTH, HEIGHT = 1024, 768
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
BALL_RADIUS = 7
SCORE_FONT = pg.font.SysFont('comicsans', 50)
WINNING_SCORE = 10
pg.display.set_caption("Pong")


class Ball:
    MAX_VEL = 10
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.starting_x = x
        self.y = self.starting_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pg.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.starting_x
        self.y = self.starting_y
        self.y_vel = 0
        self.x_vel *= -1


class Player:
    VEL = 10

    def __init__(self, x, y, width, height):
        self.x = self.starting_x = x
        self.y = self.starting_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pg.draw.rect(win, WHITE, (self.x, self.y, self.width, self.height))

    def movement(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.starting_x
        self.y = self.starting_y


def handle_player_movement(keys, player1, player2):
    if keys[pg.K_w] and player1.y - player1.VEL >= 0:
        player1.movement(up=True)
    if keys[pg.K_s] and player1.y + player1.VEL + player1.height <= HEIGHT:
        player1.movement(up=False)
    if keys[pg.K_UP] and player2.y - player2.VEL >= 0:
        player2.movement(up=True)
    if keys[pg.K_DOWN] and player2.y + player2.VEL + player2.height <= HEIGHT:
        player2.movement(up=False)


def handle_collision(player1, player2, ball):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= player1.y and ball.y <= player1.y + player1.height:
            if ball.x + ball.radius <= player1.x + player1.width:
                ball.x_vel *= -1
                middle_player1_y = player1.y + player1.height / 2
                difference_in_y = middle_player1_y - ball.y
                reduction_factor = (player1.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= player2.y and ball.y <= player2.y + player2.height:
            if ball.x + ball.radius >= player2.x:
                ball.x_vel *= -1
                middle_player2_y = player2.y + player2.height / 2
                difference_in_y = middle_player2_y - ball.y
                reduction_factor = (player2.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def draw(win, ball, paddles, player1_score, player2_score):
    win.fill(BLACK)
    ball.draw(win)
    player1_score = SCORE_FONT.render(f"1 PLAYER: {player1_score}", 1, WHITE)
    player2_score = SCORE_FONT.render(f'2 PLAYER: {player2_score}', 1, WHITE)
    win.blit(player1_score, (WIDTH // 4 - player1_score.get_width()//2, 20))
    win.blit(player2_score, (WIDTH * (3/4) - player2_score.get_width()//2, 20))
    for paddle in paddles:
        paddle.draw(win)
    pg.display.update()


def playerWin(win, player):
    playerwon = SCORE_FONT.render(f"PLAYER {player} WIN", 1, WHITE)
    win.blit(playerwon, (WIDTH // 2 - playerwon.get_width() //
             2, HEIGHT // 2 - playerwon.get_height()//2))
    pg.display.update()


def main():
    # INIT SETTINGS FOR GAME
    pg.mouse.set_visible(False)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    left_player = Player(20, HEIGHT//2 - 50, 20, 100)
    right_player = Player(WIDTH - 40, HEIGHT//2 - 50, 20, 100)
    player1_score = 0
    player2_score = 0

    going = True
    clock = pg.time.Clock()
    while going:
        clock.tick(FPS)
        # DRAWING OBJECT TO SCREEN
        draw(WINDOW, ball, [left_player, right_player],
             player1_score, player2_score)
        # GAME MECHANINCS
        keys = pg.key.get_pressed()
        handle_player_movement(keys, left_player, right_player)
        ball.move()
        handle_collision(left_player, right_player, ball)

        # SCORING MECHANICS
        if ball.x >= WIDTH:
            player1_score += 1
            if player1_score == WINNING_SCORE:
                ball.reset()
                right_player.reset()
                left_player.reset()
                playerWin(WINDOW, 1)
                pg.time.delay(5000)
                player1_score = 0
            ball.reset()
        if ball.x <= 0:
            player2_score += 1
            if player2_score == WINNING_SCORE:
                ball.reset()
                playerWin(WINDOW, 2)
                pg.time.delay(5000)
                player2_score = 0
                right_player.reset()
                left_player.reset()
            ball.reset()

        # ENDING GAME
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False


if __name__ == "__main__":
    main()
