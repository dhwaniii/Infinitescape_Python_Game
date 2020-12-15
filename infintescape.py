import pygame
import sys

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 20
BLACK = (0,0,0)
RED = (255, 0, 0)
ADD_NEW_BULLET_RATE = 25
knifes_img = pygame.image.load('knifes_bricks.png')
knifes_img_rect = knifes_img.get_rect()
knifes_img_rect.left = 0
knifesD_img = pygame.image.load('knifesD_bricks.png')
knifesD_img_rect = knifesD_img.get_rect()
knifesD_img_rect.left = 0
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont('Sprocket', 30)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


pygame.display.set_caption('InfinitEscape')


class Topscore:
    def __init__(self):
        self.high_score = 0
    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score

topscore = Topscore()


class HoodWinker:
    hoodwinker_velocity = 10

    def __init__(self):
      
        self.hoodwinker_img = pygame.image.load('hoodwinker.png')
        self.hoodwinker_img_rect = self.hoodwinker_img.get_rect()
        self.hoodwinker_img_rect.width -= 5
        self.hoodwinker_img_rect.height -= 10           
        self.hoodwinker_img_rect.top = WINDOW_HEIGHT/2
        self.hoodwinker_img_rect.right = WINDOW_WIDTH
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.hoodwinker_img, self.hoodwinker_img_rect)
        if self.hoodwinker_img_rect.top <= knifes_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.hoodwinker_img_rect.bottom >= knifesD_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.hoodwinker_img_rect.top -= self.hoodwinker_velocity
        elif self.down:
            self.hoodwinker_img_rect.top += self.hoodwinker_velocity


class Bullets:
    bullets_velocity = 10

    def __init__(self):
        self.bullets = pygame.image.load('bullet.png')
        self.bullets_img = pygame.transform.scale(self.bullets, (40,40))
        self.bullets_img_rect = self.bullets_img.get_rect()
        self.bullets_img_rect.right = hoodwinker.hoodwinker_img_rect.left
        self.bullets_img_rect.top = hoodwinker.hoodwinker_img_rect.top + 20


    def update(self):
        canvas.blit(self.bullets_img, self.bullets_img_rect)

        if self.bullets_img_rect.left > 0:
            self.bullets_img_rect.left -= self.bullets_velocity


class WhizzKid:
    whizzkid_velocity = 10

    def __init__(self):
        
        self.whizzkid_img = pygame.image.load('whizzkid.png')
        self.whizzkid_img_rect = self.whizzkid_img.get_rect()
        self.whizzkid_img_rect.left = 20
        self.whizzkid_img_rect.top = WINDOW_HEIGHT/2 - 100
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.whizzkid_img, self.whizzkid_img_rect)
        if self.whizzkid_img_rect.top <= knifes_img_rect.bottom:
            game_over()
            if SCORE > self.whizzkid_score:
                self.whizzkid_score = SCORE
        if self.whizzkid_img_rect.bottom >= knifesD_img_rect.top:
            game_over()
            if SCORE > self.whizzkid_score:
                self.whizzkid_score = SCORE
        if self.up:
            self.whizzkid_img_rect.top -= 10
        if self.down:
            self.whizzkid_img_rect.bottom += 10


def game_over():
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound('among_us_kill.wav')
    music.play()
    topscore.top_score(SCORE)
    game_over_img = pygame.image.load('end.png')
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(game_over_img, game_over_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                music.stop()
                game_loop()
        pygame.display.update()


def start_game():
    background_image = pygame.image.load("bg.jpg").convert()
    canvas.blit(background_image, [0, 0])

    music = pygame.mixer.Sound('among_us_start.wav')
    music.play()
    start_img = pygame.image.load('start.png')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                music.stop()
                game_loop()
        pygame.display.update()


def check_level(SCORE):
    global LEVEL
    if SCORE in range(0, 10):
        knifes_img_rect.bottom = 50
        knifesD_img_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 1
    elif SCORE in range(10, 20):
        knifes_img_rect.bottom = 100
        knifesD_img_rect.top = WINDOW_HEIGHT - 100
        LEVEL = 2
    elif SCORE in range(20, 30):
        knifes_img_rect.bottom = 150
        knifesD_img_rect.top = WINDOW_HEIGHT - 150
        LEVEL = 3
    elif SCORE > 30:
        knifes_img_rect.bottom = 200
        knifesD_img_rect.top = WINDOW_HEIGHT - 200
        LEVEL = 4





def game_loop():
    while True:
        global hoodwinker
        hoodwinker = HoodWinker()
        bullets = Bullets()
        whizzkid = WhizzKid()
        add_new_bullet_counter = 0
        global SCORE
        SCORE = 0
        global  HIGH_SCORE
        bullets_list = []
        pygame.mixer.music.stop()
        pygame.mixer.music.load('among_us.mp3')
        pygame.mixer.music.play(-1, 0.0)
        while True:
            background_image = pygame.image.load("bg.jpg").convert()
            canvas.blit(background_image, [0, 0])
           
            check_level(SCORE)
            hoodwinker.update()
            add_new_bullet_counter += 1

            if add_new_bullet_counter == ADD_NEW_BULLET_RATE:
                add_new_bullet_counter = 0
                new_flame = Bullets()
                bullets_list.append(new_flame)
            for f in bullets_list:
                if f.bullets_img_rect.left <= 0:
                    bullets_list.remove(f)
                    SCORE += 1
                f.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        whizzkid.up = True
                        whizzkid.down = False
                    elif event.key == pygame.K_DOWN:
                        whizzkid.down = True
                        whizzkid.up = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        whizzkid.up = False
                        whizzkid.down = True
                    elif event.key == pygame.K_DOWN:
                        whizzkid.down = True
                        whizzkid.up = False

            score_font = font.render('Score:'+str(SCORE), True, RED)
            score_font_rect = score_font.get_rect()
            score_font_rect.center = (200, knifes_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(score_font, score_font_rect)

            level_font = font.render('Level:'+str(LEVEL), True, RED)
            level_font_rect = level_font.get_rect()
            level_font_rect.center = (500, knifes_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(level_font, level_font_rect)

            top_score_font = font.render('Top Score:'+str(topscore.high_score),True,RED)
            top_score_font_rect = top_score_font.get_rect()
            top_score_font_rect.center = (800, knifes_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(top_score_font, top_score_font_rect)

            canvas.blit(knifes_img, knifes_img_rect)
            canvas.blit(knifesD_img, knifesD_img_rect)
            whizzkid.update()
            for f in bullets_list:
                if f.bullets_img_rect.colliderect(whizzkid.whizzkid_img_rect):
                    game_over()
                    if SCORE > whizzkid.whizzkid_score:
                        whizzkid.whizzkid_score = SCORE
            pygame.display.update()
            CLOCK.tick(FPS)


start_game()


