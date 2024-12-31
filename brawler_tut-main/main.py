import pygame
import math
import random
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BattleBot Game")

clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)  
LIGHT_RED = (255, 50, 50)  
YELLOW = (255, 255, 0)
FOREST_GREEN = (34, 139, 34) 


intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] 
round_over = False
ROUND_OVER_COOLDOWN = 2000

WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

pygame.mixer.music.load("brawler_tut-main/assets/audio/king.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("brawler_tut-main/assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("brawler_tut-main/assets/audio/magic.wav")
magic_fx.set_volume(0.75)

bg_image = pygame.image.load("brawler_tut-main/assets/images/background/forest.jpg").convert_alpha()

warrior_sheet = pygame.image.load("brawler_tut-main/assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("brawler_tut-main/assets/images/wizard/Sprites/wizard.png").convert_alpha()

victory_img = pygame.image.load("brawler_tut-main/assets/images/icons/victory.png").convert_alpha()

WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

count_font = pygame.font.Font("brawler_tut-main/assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("brawler_tut-main/assets/fonts/turok.ttf", 30)
loading_font = pygame.font.Font("brawler_tut-main/assets/fonts/turok.ttf", 100)
menu_font = pygame.font.Font("brawler_tut-main/assets/fonts/turok.ttf", 50)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg(is_loading_screen=False):
    if is_loading_screen:
        screen.fill(BLACK)

        for i in range(SCREEN_HEIGHT // 2, SCREEN_HEIGHT, 2): 
            glitter_color = (random.randint(150, 255), 0, 0)  
            pygame.draw.line(screen, glitter_color, (0, i), (SCREEN_WIDTH, i)) 

        if random.random() < 0.1:  
            intensity = random.randint(150, 255)
            pygame.draw.line(screen, (intensity, 0, 0), (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT - random.randint(0, 20)), 
                             (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT))
            
    else:
        scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))


def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, FOREST_GREEN, (x, y, 400 * ratio, 30))

def draw_loading_timer(seconds_left, show_countdown=True):
    bar_width = 400
    bar_height = 20
    bar_x = SCREEN_WIDTH / 2 - bar_width / 2
    bar_y = SCREEN_HEIGHT / 6 + 120  

    pygame.draw.rect(screen, (60, 60, 60), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))  
    pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height))  

    ratio = seconds_left / 3 
    pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width * ratio, bar_height))  

    if show_countdown:
        draw_text(str(seconds_left), loading_font, WHITE, SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 6 + 90)

def loading_screen():
    global intro_count
    last_count_update = pygame.time.get_ticks()
    loading_screen_active = True

    while loading_screen_active:
        draw_bg(is_loading_screen=True)

        pulse_size = 1 + math.sin(pygame.time.get_ticks() / 500) * 0.05
        glitter_color = RED
        title_x = SCREEN_WIDTH / 2 - count_font.size("BATTLEBOT GAME")[0] / 2
        title_y = SCREEN_HEIGHT / 6
        draw_text("BATTLEBOT GAME", count_font, glitter_color, title_x, title_y)

        draw_loading_timer(intro_count)

        fighter_1.draw(screen)
        fighter_2.draw(screen)

        if pygame.time.get_ticks() - last_count_update >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

        if intro_count <= 0:
            loading_screen_active = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(FPS)



def game_menu():
    menu_active = True
    while menu_active:
        draw_bg() 

        draw_text("DO U WANNA ????", menu_font, RED, SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 3)
        draw_text("1. Continue", menu_font, WHITE, SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 40)
        draw_text("2. Restart", menu_font, WHITE, SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2)
        draw_text("3. Exit", menu_font, WHITE, SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  
                    return "continue"
                if event.key == pygame.K_2: 
                    return "restart"
                    return "exit"

        pygame.display.update()
        clock.tick(FPS)

fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

run = True

loading_screen()

while run:
    clock.tick(FPS)

    draw_bg()

    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    if intro_count > 0:
        draw_loading_timer(intro_count, show_countdown=False)  

        if pygame.time.get_ticks() - last_count_update >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
    else:
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)

        fighter_1.update()
        fighter_2.update()

        fighter_1.draw(screen)
        fighter_2.draw(screen)

        if not round_over:
            if fighter_1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif fighter_2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                choice = game_menu()

                if choice == "continue":
                    round_over = False
                    intro_count = 3  
                    fighter_1.health = 100  
                    fighter_2.health = 100 
                    fighter_1.alive = True  
                    fighter_2.alive = True 
                elif choice == "restart":

                    score = [0, 0]
                    round_over = False
                    intro_count = 3
                    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
                elif choice == "exit":
                    run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
