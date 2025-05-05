import pygame, sys, random, time

pygame.init()

WIDTH, HEIGHT = 1280, 800

FONT = pygame.font.SysFont("Console", int(WIDTH/20))
SMALL_FONT = pygame.font.SysFont("Console", 40)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")
CLOCK = pygame.time.Clock()

# Game objects
player = pygame.Rect(0, 0, 10, 100)
player.center = (WIDTH - 100, HEIGHT / 2)

opponent = pygame.Rect(0, 0, 10, 100)
opponent.center = (100, HEIGHT / 2)

ball = pygame.Rect(0, 0, 20, 20)
ball.center = (WIDTH / 2, HEIGHT / 2)

# Initial values
player_score, opponent_score = 0, 0
x_speed, y_speed = 1, 1
ball_speed = 1.2
opponent_speed = 1

# Game time
GAME_DURATION = 119  # seconds
start_time = None

# Text input state
username = ""
age = ""
entering_username = True
entering_age = False
game_started = False
game_over = False

def draw_text_input_screen():
    SCREEN.fill("black")
    title = FONT.render("Enter your name and age to start", True, "white")
    SCREEN.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT / 4))

    if entering_username:
        input_text = SMALL_FONT.render("Name: " + username + "|", True, "green")
    else:
        input_text = SMALL_FONT.render("Name: " + username, True, "white")
    SCREEN.blit(input_text, (WIDTH / 2 - 200, HEIGHT / 2 - 50))

    if entering_age:
        input_age = SMALL_FONT.render("Age: " + age + "|", True, "green")
    else:
        input_age = SMALL_FONT.render("Age: " + age, True, "white")
    SCREEN.blit(input_age, (WIDTH / 2 - 200, HEIGHT / 2 + 10))

    pygame.display.update()

def draw_game_over():
    SCREEN.fill("black")
    over_text = FONT.render("⏱ Time's up!", True, "white")
    SCREEN.blit(over_text, (WIDTH/2 - over_text.get_width()/2, HEIGHT/4))

    result_text = ""
    if player_score > opponent_score:
        result_text = f"{username} Wins! 🎉"
    elif opponent_score > player_score:
        result_text = "Opponent Wins! 🏆"
    else:
        result_text = "It's a Draw!"

    result_render = FONT.render(result_text, True, "yellow")
    SCREEN.blit(result_render, (WIDTH/2 - result_render.get_width()/2, HEIGHT/2))

    score_text = SMALL_FONT.render(f"Final Score - {username}: {player_score} | Opponent: {opponent_score}", True, "lightblue")
    SCREEN.blit(score_text, (WIDTH/2 - score_text.get_width()/2, HEIGHT/2 + 80))

    pygame.display.update()

# Main loop
while True:
    if not game_started:
        draw_text_input_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if entering_username:
                    if event.key == pygame.K_RETURN:
                        entering_username = False
                        entering_age = True
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif entering_age:
                    if event.key == pygame.K_RETURN and age.isdigit():
                        game_started = True
                        start_time = time.time()  # Start the timer
                    elif event.key == pygame.K_BACKSPACE:
                        age = age[:-1]
                    elif event.unicode.isdigit():
                        age += event.unicode
        continue

    if game_over:
        draw_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        continue

    # Check time left
    elapsed_time = time.time() - start_time
    remaining_time = GAME_DURATION - int(elapsed_time)
    if elapsed_time >= GAME_DURATION:
        game_over = True
        continue

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Ball movement
    if ball.y >= HEIGHT:
        y_speed = -1
    if ball.y <= 0:
        y_speed = 1

    if ball.x <= 0:
        player_score += 1
        ball.center = (WIDTH / 2, HEIGHT / 2)
        x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])
        opponent_speed += 0.2
        ball_speed = 1.2

    if ball.x >= WIDTH:
        opponent_score += 1
        ball.center = (WIDTH / 2, HEIGHT / 2)
        x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])
        ball_speed = 1.2

    if player.x - ball.width <= ball.x <= player.right and ball.y in range(player.top - ball.width, player.bottom + ball.width):
        x_speed = -1
    if opponent.x - ball.width <= ball.x <= opponent.right and ball.y in range(opponent.top - ball.width, opponent.bottom + ball.width):
        x_speed = 1

    # Gradually increase ball speed
    ball_speed += 0.001
    ball.x += x_speed * ball_speed
    ball.y += y_speed * ball_speed

    # Opponent AI with mistakes
    if random.randint(0, 20) != 0:
        if opponent.y < ball.y:
            opponent.top += opponent_speed
        if opponent.bottom > ball.y:
            opponent.bottom -= opponent_speed

    # Move player with mouse
    mouse_y = pygame.mouse.get_pos()[1]
    player.centery = mouse_y

    # Draw game screen
    SCREEN.fill("black")
    pygame.draw.rect(SCREEN, "red", player)
    pygame.draw.rect(SCREEN, "white", opponent)
    pygame.draw.circle(SCREEN, "yellow", ball.center, 10)

    player_score_text = FONT.render(str(player_score), True, "white")
    opponent_score_text = FONT.render(str(opponent_score), True, "white")
    SCREEN.blit(player_score_text, (WIDTH / 2 + 50, 50))
    SCREEN.blit(opponent_score_text, (WIDTH / 2 - 100, 50))

    # Timer display
    timer_text = SMALL_FONT.render(f"Time left: {remaining_time} sec", True, "orange")
    SCREEN.blit(timer_text, (WIDTH / 2 - timer_text.get_width() / 2, 10))

    # Player info
    user_info = SMALL_FONT.render(f"{username} (Age {age})", True, "lightblue")
    SCREEN.blit(user_info, (WIDTH / 2 - user_info.get_width() / 2, HEIGHT - 60))

    pygame.display.update()
    CLOCK.tick(300)
