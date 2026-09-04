import pygame
import math

pygame.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Fighting Game")

clock = pygame.time.Clock()

# =========================
# COLORS
# =========================
SKY = (80, 160, 220)
GROUND = (65, 155, 75)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (220, 40, 40)
DARK_RED = (90, 0, 0)
GRAY = (70, 70, 70)
YELLOW = (255, 220, 40)
ORANGE = (255, 130, 20)

# =========================
# LOAD PLAYER 1
# =========================
player1 = pygame.image.load(
    "/storage/emulated/0/Download/player1.png"
).convert_alpha()

player1 = pygame.transform.scale(
    player1, (180, 270)
)

# =========================
# LOAD PLAYER 2
# =========================
player2 = pygame.image.load(
    "/storage/emulated/0/Download/player2.png"
).convert_alpha()

player2 = pygame.transform.scale(
    player2, (180, 270)
)

# Face Player 1
player2 = pygame.transform.flip(
    player2, True, False
)

# =========================
# POSITIONS
# =========================
p1_x = 100
p1_y = 180

p2_x = 620
p2_y = 180

# =========================
# HEALTH
# =========================
p1_health = 100
p2_health = 100

# =========================
# PLAYER 1 JUMP
# =========================
p1_velocity_y = 0
gravity = 1
jump_power = -18

# =========================
# PLAYER 1 ATTACK
# =========================
p1_attack = None
p1_attack_timer = 0
p1_attack_cooldown = 0

# =========================
# PLAYER 2 ATTACK
# =========================
p2_attack = None
p2_attack_timer = 0
p2_attack_cooldown = 0

# =========================
# HIT EFFECT
# =========================
hit_timer = 0
hit_x = 0
hit_y = 0

# =========================
# GAME
# =========================
game_over = False
winner = ""

# =========================
# TOUCH BUTTONS
# =========================
left_button = pygame.Rect(25, 485, 90, 80)
right_button = pygame.Rect(125, 485, 90, 80)

jump_button = pygame.Rect(600, 485, 90, 80)

punch_button = pygame.Rect(700, 390, 90, 80)
kick_button = pygame.Rect(800, 485, 90, 80)


# =========================
# BUTTON
# =========================
def draw_button(rect, text):

    pygame.draw.rect(
        screen,
        GRAY,
        rect,
        border_radius=18
    )

    pygame.draw.rect(
        screen,
        WHITE,
        rect,
        3,
        border_radius=18
    )

    font = pygame.font.Font(None, 28)

    text_image = font.render(
        text,
        True,
        WHITE
    )

    screen.blit(
        text_image,
        text_image.get_rect(center=rect.center)
    )


# =========================
# PLAYER 1 ATTACK
# =========================
def player1_attack(kind):

    global p1_attack
    global p1_attack_timer
    global p1_attack_cooldown
    global p2_health
    global hit_timer
    global hit_x
    global hit_y

    if p1_attack_cooldown > 0:
        return

    p1_attack = kind

    if kind == "punch":

        p1_attack_timer = 18
        p1_attack_cooldown = 30
        damage = 10

        attack_box = pygame.Rect(
            p1_x + 100,
            p1_y + 65,
            110,
            90
        )

    else:

        p1_attack_timer = 24
        p1_attack_cooldown = 40
        damage = 15

        attack_box = pygame.Rect(
            p1_x + 80,
            p1_y + 145,
            140,
            100
        )

    enemy_box = pygame.Rect(
        p2_x + 25,
        p2_y + 25,
        130,
        240
    )

    if attack_box.colliderect(enemy_box):

        p2_health -= damage

        hit_timer = 12
        hit_x = p2_x + 80
        hit_y = p2_y + 120


# =========================
# RESET
# =========================
def reset_game():

    global p1_x, p1_y
    global p2_x, p2_y
    global p1_health, p2_health
    global p1_velocity_y
    global game_over, winner
    global p1_attack, p1_attack_timer
    global p1_attack_cooldown
    global p2_attack, p2_attack_timer
    global p2_attack_cooldown

    p1_x = 100
    p1_y = 180

    p2_x = 620
    p2_y = 180

    p1_health = 100
    p2_health = 100

    p1_velocity_y = 0

    p1_attack = None
    p1_attack_timer = 0
    p1_attack_cooldown = 0

    p2_attack = None
    p2_attack_timer = 0
    p2_attack_cooldown = 0

    game_over = False
    winner = ""


# =========================
# MAIN LOOP
# =========================
running = True

while running:

    # =========================
    # EVENTS
    # =========================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = event.pos

            if not game_over:

                if left_button.collidepoint(pos):
                    p1_x -= 25

                elif right_button.collidepoint(pos):
                    p1_x += 25

                elif jump_button.collidepoint(pos):

                    if p1_y >= 180:
                        p1_velocity_y = jump_power

                elif punch_button.collidepoint(pos):

                    player1_attack("punch")

                elif kick_button.collidepoint(pos):

                    player1_attack("kick")

            else:

                restart_button = pygame.Rect(
                    330, 350, 240, 70
                )

                if restart_button.collidepoint(pos):
                    reset_game()

    # =========================
    # GAME
    # =========================
    if not game_over:

        # =========================
        # PLAYER 1 MOVEMENT
        # =========================
        p1_x = max(
            0,
            min(p1_x, WIDTH - 180)
        )

        # =========================
        # PLAYER 1 JUMP
        # =========================
        p1_velocity_y += gravity
        p1_y += p1_velocity_y

        if p1_y >= 180:

            p1_y = 180
            p1_velocity_y = 0

        # =========================
        # PLAYER 1 ATTACK TIMER
        # =========================
        if p1_attack_cooldown > 0:
            p1_attack_cooldown -= 1

        if p1_attack_timer > 0:

            p1_attack_timer -= 1

        else:

            p1_attack = None

        # =========================
        # ENEMY MOVEMENT
        # =========================

        distance = p1_x - p2_x

        if p2_attack is None:

            if distance > 130:
                p2_x += 2

            elif distance < -130:
                p2_x -= 2

        p2_x = max(
            0,
            min(p2_x, WIDTH - 180)
        )

        # =========================
        # ENEMY ATTACK AI
        # =========================

        if p2_attack_cooldown > 0:
            p2_attack_cooldown -= 1

        # Enemy starts attack when close
        if (
            abs(p1_x - p2_x) < 145
            and p2_attack is None
            and p2_attack_cooldown == 0
        ):

            # Alternate punch and kick
            if pygame.time.get_ticks() // 1000 % 2 == 0:

                p2_attack = "punch"
                p2_attack_timer = 18
                p2_attack_cooldown = 50

            else:

                p2_attack = "kick"
                p2_attack_timer = 24
                p2_attack_cooldown = 60

        # =========================
        # ENEMY ATTACK ANIMATION
        # =========================

        if p2_attack is not None:

            p2_attack_timer -= 1

            # Hit near middle of animation
            if p2_attack_timer == 9:

                if abs(p1_x - p2_x) < 160:

                    if p2_attack == "punch":

                        p1_health -= 10

                    else:

                        p1_health -= 15

                    hit_timer = 12
                    hit_x = p1_x + 70
                    hit_y = p1_y + 120

            if p2_attack_timer <= 0:

                p2_attack = None

        # =========================
        # HIT EFFECT
        # =========================

        if hit_timer > 0:
            hit_timer -= 1

        # =========================
        # WIN / LOSE
        # =========================

        if p2_health <= 0:

            p2_health = 0
            game_over = True
            winner = "YOU WIN!"

        if p1_health <= 0:

            p1_health = 0
            game_over = True
            winner = "YOU LOSE!"

    # =========================
    # BACKGROUND
    # =========================

    screen.fill(SKY)

    pygame.draw.rect(
        screen,
        GROUND,
        (0, 450, WIDTH, 150)
    )

    pygame.draw.line(
        screen,
        BLACK,
        (0, 450),
        (WIDTH, 450),
        5
    )

    # =========================
    # HEALTH BARS
    # =========================

    pygame.draw.rect(
        screen,
        DARK_RED,
        (30, 25, 350, 30)
    )

    pygame.draw.rect(
        screen,
        RED,
        (30, 25, int(p1_health * 3.5), 30)
    )

    pygame.draw.rect(
        screen,
        DARK_RED,
        (520, 25, 350, 30)
    )

    pygame.draw.rect(
        screen,
        RED,
        (520, 25, int(p2_health * 3.5), 30)
    )

    font = pygame.font.Font(None, 28)

    screen.blit(
        font.render("PLAYER 1", True, WHITE),
        (30, 65)
    )

    screen.blit(
        font.render("PLAYER 2", True, WHITE),
        (520, 65)
    )

    # ==================================================
    # PLAYER 1 ANIMATION
    # ==================================================

    p1_image = player1
    p1_draw_x = p1_x

    if p1_attack == "punch":

        progress = p1_attack_timer / 18

        movement = int(
            20 * math.sin(progress * math.pi)
        )

        p1_draw_x += movement

        angle = -10 * math.sin(
            progress * math.pi
        )

        p1_image = pygame.transform.rotate(
            player1,
            angle
        )

    elif p1_attack == "kick":

        progress = p1_attack_timer / 24

        movement = int(
            28 * math.sin(progress * math.pi)
        )

        p1_draw_x += movement

        angle = 12 * math.sin(
            progress * math.pi
        )

        p1_image = pygame.transform.rotate(
            player1,
            angle
        )

    screen.blit(
        p1_image,
        (p1_draw_x, p1_y)
    )

    # ==================================================
    # PLAYER 2 ANIMATION
    # ==================================================

    p2_image = player2
    p2_draw_x = p2_x

    if p2_attack == "punch":

        progress = p2_attack_timer / 18

        movement = int(
            25 * math.sin(progress * math.pi)
        )

        # Enemy lunges toward Player 1
        p2_draw_x -= movement

        # Enemy leans forward
        angle = 10 * math.sin(
            progress * math.pi
        )

        p2_image = pygame.transform.rotate(
            player2,
            angle
        )

    elif p2_attack == "kick":

        progress = p2_attack_timer / 24

        movement = int(
            32 * math.sin(progress * math.pi)
        )

        # Enemy lunges forward
        p2_draw_x -= movement

        # Bigger kick movement
        angle = -15 * math.sin(
            progress * math.pi
        )

        p2_image = pygame.transform.rotate(
            player2,
            angle
        )

    screen.blit(
        p2_image,
        (p2_draw_x, p2_y)
    )

    # ==================================================
    # PLAYER 1 ATTACK EFFECT
    # ==================================================

    if p1_attack == "punch":

        progress = p1_attack_timer / 18

        if progress < 0.75:

            fist_x = int(p1_x + 185)
            fist_y = int(p1_y + 105)

            pygame.draw.circle(
                screen,
                YELLOW,
                (fist_x, fist_y),
                15
            )

            pygame.draw.circle(
                screen,
                ORANGE,
                (fist_x, fist_y),
                23,
                3
            )

    if p1_attack == "kick":

        progress = p1_attack_timer / 24

        if progress < 0.75:

            foot_x = int(p1_x + 190)
            foot_y = int(p1_y + 200)

            pygame.draw.circle(
                screen,
                YELLOW,
                (foot_x, foot_y),
                18
            )

            pygame.draw.circle(
                screen,
                ORANGE,
                (foot_x, foot_y),
                28,
                3
            )

    # ==================================================
    # ENEMY ATTACK EFFECT
    # ==================================================

    if p2_attack == "punch":

        progress = p2_attack_timer / 18

        if progress < 0.75:

            fist_x = int(p2_x - 5)
            fist_y = int(p2_y + 105)

            pygame.draw.circle(
                screen,
                YELLOW,
                (fist_x, fist_y),
                15
            )

            pygame.draw.circle(
                screen,
                ORANGE,
                (fist_x, fist_y),
                23,
                3
            )

    if p2_attack == "kick":

        progress = p2_attack_timer / 24

        if progress < 0.75:

            foot_x = int(p2_x + 5)
            foot_y = int(p2_y + 200)

            pygame.draw.circle(
                screen,
                YELLOW,
                (foot_x, foot_y),
                18
            )

            pygame.draw.circle(
                screen,
                ORANGE,
                (foot_x, foot_y),
                28,
                3
            )

    # ==================================================
    # HIT EFFECT
    # ==================================================

    if hit_timer > 0:

        size = 30 + (12 - hit_timer) * 3

        pygame.draw.circle(
            screen,
            YELLOW,
            (hit_x, hit_y),
            size,
            5
        )

        pygame.draw.line(
            screen,
            WHITE,
            (
                hit_x - size,
                hit_y - size
            ),
            (
                hit_x + size,
                hit_y + size
            ),
            5
        )

        pygame.draw.line(
            screen,
            WHITE,
            (
                hit_x + size,
                hit_y - size
            ),
            (
                hit_x - size,
                hit_y + size
            ),
            5
        )

    # ==================================================
    # TOUCH CONTROLS
    # ==================================================

    draw_button(left_button, "<")
    draw_button(right_button, ">")
    draw_button(jump_button, "JUMP")
    draw_button(punch_button, "PUNCH")
    draw_button(kick_button, "KICK")

    # ==================================================
    # GAME OVER
    # ==================================================

    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 170)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        big_font = pygame.font.Font(
            None,
            90
        )

        result = big_font.render(
            winner,
            True,
            WHITE
        )

        screen.blit(
            result,
            result.get_rect(
                center=(WIDTH // 2, 220)
            )
        )

        restart_button = pygame.Rect(
            330,
            350,
            240,
            70
        )

        draw_button(
            restart_button,
            "RESTART"
        )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()