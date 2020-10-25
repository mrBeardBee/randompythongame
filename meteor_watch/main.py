import pygame
import math
import random
import os

current_dir = os.path.abspath(__file__)
new_dir = current_dir.rstrip('/main.py')
print('Directory path is [' + new_dir + ']')

os.chdir(new_dir)

screen_height = 500
screen_width = 500

pygame.init()

player_sprite_still = pygame.image.load('./images/player(1).png')
player_sprite_moving = pygame.image.load('./images/player(1).png')
background_image = pygame.image.load('./images/background.png')
life_point = pygame.image.load('./images/lives_emoji.png')
small_meteor = pygame.image.load('./images/small-meteor.png')
regular_meteor = pygame.image.load('./images/regular-meteor.png')
large_meteor = pygame.image.load('./images/large-meteor.png')

hit_sound = pygame.mixer.Sound("./sounds/hit.wav")
revive_sound = pygame.mixer.Sound("./sounds/revive.wav")
dead_sound = pygame.mixer.Sound("./sounds/dead.wav")


music = pygame.mixer.music.load("./sounds/Interplanetary-Odyssey.ogg")
pygame.mixer.music.play(-1)


def play_revive_sound():
    pygame.mixer.Sound.play(revive_sound)


def play_hit_sound():
    if alien.lives > 0:
        pygame.mixer.Sound.play(hit_sound)
    else:
        pygame.mixer.Sound.play(dead_sound)


player_sprite_moving_index = 1

pygame.display.set_caption("Meteor Watch")

screen = pygame.display.set_mode((screen_height, screen_width))

comic_sans = pygame.font.SysFont('Comic Sans MS', 15)
lives_font = pygame.font.SysFont('Comic Sans MS', 20)
game_over_font = pygame.font.SysFont('Comic Sans MS', 60)

wKey = pygame.K_w
aKey = pygame.K_a
sKey = pygame.K_s
dKey = pygame.K_d


#new meteor loop

initial_meteor_spawn_time = 1500
meteors = []
meteor_spawn_time = initial_meteor_spawn_time


def restartgame():
    global meteors
    global alien
    global meteor_spawn_time
    alien = player(250, 300, 22, 16, 8, 3)
    alien.lives = 3
    alien.alive = True
    meteor_spawn_time = initial_meteor_spawn_time
    meteors = []
    play_revive_sound()


def resetscreen():
    global meteors
    global meteor_spawn_time
    alien.x = 250
    alien.y = 300
    meteor_spawn_time = initial_meteor_spawn_time
    meteors = []


class player(object):
    def __init__(self, x, y, width, height, speed_per_frame, lives):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed_per_frame = speed_per_frame
        self.lives = lives
        self.alive = True
        self.hitbox = (self.x - (0.5 * self.width), self.y - (0.5 * self.height), self.width, self.height)
        self.is_moving = False

    def hit(self):
        self.lives -= 1
        if alien.alive:
            play_hit_sound()
            resetscreen()


class enemy(object):
    def __init__(self, x, y, level):
        self.x = x
        self.y = y

        if level > 7:
            self.width = 72
            self.height = 200
            self.sprite = large_meteor
            self.speed_per_frame = random.randint(4, 7)
        elif level > 4:
            self.width = 36
            self.height = 100
            self.sprite = regular_meteor
            self.speed_per_frame = random.randint(7, 11)
        else:
            self.width = 18
            self.height = 50
            self.sprite = small_meteor
            self.speed_per_frame = random.randint(10, 15)


        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self):
        global screen
        self.hitbox = (self.x - (0.5 * self.width), self.y - (0.5 * self.height), self.width, self.height)
        #pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)
        screen.blit(self.sprite, (self.x - (0.5 * self.width), self.y - (0.5 * self.height)))


restartgame()

clock = pygame.time.Clock()
global_time = 0
meteor_loop_time = 0

running = True
animation_loop = 0

#main loop

while running:
    pygame.time.delay(5)

    dt = clock.tick()
    meteor_loop_time += dt

    if alien.alive:
        global_time += dt

    if meteor_loop_time > meteor_spawn_time:
        meteors.append(enemy(random.randint(0, 500), -100, random.randint(1, 8)))
        meteor_spawn_time = random.randint(100, 600)
        meteor_loop_time = 0

    # Animation loop
    if animation_loop > 15:
        animation_loop = 0
        if player_sprite_moving_index == 1:
            player_sprite_moving_index = 2
            player_sprite_moving = pygame.image.load('./images/player(2).png')
        else:
            player_sprite_moving_index = 1
            player_sprite_moving = pygame.image.load('./images/player(1).png')

# Event Listeners

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for meteor in meteors:
        if meteor.y < screen_height + 50:
            meteor.y = meteor.y + meteor.speed_per_frame
        else:
            meteors.remove(meteor)
        if (meteor.y - (0.5 * meteor.height)) < alien.hitbox[1] + alien.hitbox[3] and (meteor.y + (0.5 * meteor.height)) > alien.hitbox[1]:
            if (meteor.x + (0.5 * meteor.width)) > alien.hitbox[0] and (meteor.x -(0.5 * meteor.width)) < alien.hitbox[0] + alien.hitbox[2]:
                alien.hit()
                # pass

# movement

    keys = pygame.key.get_pressed()

    if alien.alive:
        if keys[wKey] and not keys[aKey] and not keys[dKey]:
            alien.y -= alien.speed_per_frame
            alien.is_moving = True
        if keys[sKey] and not keys[aKey] and not keys[dKey]:
            alien.y += alien.speed_per_frame
            alien.is_moving = True
        if keys[aKey] and not keys[wKey] and not keys[sKey]:
            alien.x -= alien.speed_per_frame
            alien.is_moving = True
        if keys[dKey] and not keys[wKey] and not keys[sKey]:
            alien.x += alien.speed_per_frame
            alien.is_moving = True
        if keys[wKey] and keys[aKey] and not keys[dKey]:
            alien.x -= alien.speed_per_frame / math.sqrt(2)
            alien.y -= alien.speed_per_frame / math.sqrt(2)
            alien.is_moving = True
        if keys[wKey] and keys[dKey] and not keys[aKey]:
            alien.x += alien.speed_per_frame / math.sqrt(2)
            alien.y -= alien.speed_per_frame / math.sqrt(2)
            alien.is_moving = True
        if keys[sKey] and keys[aKey] and not keys[dKey]:
            alien.x -= alien.speed_per_frame / math.sqrt(2)
            alien.y += alien.speed_per_frame / math.sqrt(2)
            alien.is_moving = True
        if keys[sKey] and keys[dKey] and not keys[aKey]:
            alien.x += alien.speed_per_frame / math.sqrt(2)
            alien.y += alien.speed_per_frame / math.sqrt(2)
            alien.is_moving = True
        if keys[wKey] and keys[aKey] and keys[dKey]:
            alien.y -= alien.speed_per_frame
            alien.is_moving = True
        if keys[sKey] and keys[dKey] and keys[aKey]:
            alien.y += alien.speed_per_frame
            alien.is_moving = True
        if keys[aKey] and keys[wKey] and keys[sKey]:
            alien.x -= alien.speed_per_frame
            alien.is_moving = True
        if keys[dKey] and keys[wKey] and keys[sKey]:
            alien.x += alien.speed_per_frame
            alien.is_moving = True
        if not keys[wKey] and not keys[dKey] and not keys[sKey] and not keys[aKey]:
            alien.is_moving = False
        if keys[wKey] and keys[sKey] and not keys[aKey] and not keys[dKey]:
            alien.is_moving = False
        if keys[aKey] and keys[dKey] and not keys[wKey] and not keys[sKey]:
            alien.is_moving = False
    if not alien.alive:
        if keys[pygame.K_SPACE]:
            restartgame()
            global_time = 0

    if alien.x > screen_width:
        alien.x = 0
    elif alien.x < 0:
        alien.x = screen_width

    if alien.y > screen_height-50 - (alien.height/2):
        alien.y = screen_height-50 - (alien.height/2)
    elif alien.y < alien.height/2:
        alien.y = alien.height/2

    animation_loop = animation_loop + 1

    if alien.lives <= 0:
        alien.alive = False

# draw stuff here

#background
    screen.blit(background_image, (0, 0))

#meteors
    for meteor in meteors:
        meteor.draw()

#character sprite

    alien.hitbox = (alien.x - (0.5 * alien.width), alien.y - (0.5 * alien.height), alien.width,alien.height)
    #pygame.draw.rect(screen, (255,0,0), alien.hitbox, 2)

    if alien.alive:
        if not alien.is_moving:
            screen.blit(player_sprite_still, (alien.x - (0.5 * alien.width), alien.y - (0.5 * alien.height)))
        else:
            screen.blit(player_sprite_moving, (alien.x - (0.5 * alien.width), alien.y - (0.5 * alien.height)))

#shelf
    pygame.draw.rect(screen, (130, 130, 130), (0, screen_height-50, screen_width, 50))
    pygame.draw.rect(screen, (11, 25, 120), (0, screen_height-50, screen_width, 5))

#text
    WSAD = comic_sans.render('WSAD to move', False, (255, 255, 255))
    name_of_the_game = lives_font.render("Meteor Watch", False, (255,255,255))
    screen.blit(name_of_the_game, (10, 15))
    #Debug = comic_sans.render("# of meteors: " + str(len(meteors)), False, (255, 255, 255))
    seconds_survived = comic_sans.render((str(math.floor(global_time * 0.001)) + " seconds survived"), False, (255, 255, 255))
    screen.blit(WSAD, (screen_width-130, 10))
    #screen.blit(Debug,((screen_width - 150),50))
    screen.blit(seconds_survived, ((screen_width - 143), 30))

#lives
    if alien.lives > 0:
        lives_text_content = "Lives:"
    if alien.lives >= 1:
        screen.blit(life_point, (screen_width - 60, screen_height - 40))
    if alien.lives >= 2:
        screen.blit(life_point, (screen_width - 120, screen_height - 40))
    if alien.lives == 3:
        screen.blit(life_point, (screen_width - 180, screen_height - 40))
    if alien.lives <= 0:
        lives_text_content = "You Died!                           Press space to retry"
        screen.blit(game_over_font.render("GAME OVER", False, (255, 255, 255)), (75, 200))

    lives_text = lives_font.render(lives_text_content, False, (255, 255, 255))
    screen.blit(lives_text, (20, screen_height - 40))

#update
    pygame.display.update()

pygame.display.quit()
pygame.quit()
