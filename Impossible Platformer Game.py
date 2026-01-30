#Impossible Platformer Game
#Nishchay Bhudia
#08/10/2024 - 21/01/2025
#Course Work
#Computer Science


#Imports
import time
import csv
import os
import random
import math
import pygame
import sys
from os import listdir
from os.path import isfile, join

#Initialising Pygame
pygame.init()
pygame.mixer.init()

#sound effects
def load_sounds():
    sounds = {
        'background': pygame.mixer.Sound('assets/Sound Effects/background.mp3'),
        'die': pygame.mixer.Sound('assets/Sound Effects/die.mp3'),
        'checkpoint': pygame.mixer.Sound('assets/Sound Effects/checkpoint.mp3'), # need to fix 
        'start': pygame.mixer.Sound('assets/Sound Effects/start.mp3')
    }
    
    # Set background music volume lower than effects
    sounds['background'].set_volume(0.2)
    
    return sounds

# Load all sounds
game_sounds = load_sounds()

# Start playing background music on loop
def play_background_music():
    game_sounds['background'].play(-1)  # -1 means loop forever

def stop_background_music():
    game_sounds['background'].stop()

# Play sound effects
def play_sound(sound_name):
    game_sounds[sound_name].play()


#Display Settings
pygame.display.set_caption("Impossible Game")

#Basic Variables
WIDTH, HEIGHT = 1000, 800 #Screen
FPS = 60
PLAYER_VEL = 5
death_count = 0



#Pygame Window Setup
window = pygame.display.set_mode((WIDTH, HEIGHT))



#Loading Screen
def draw_loading_screen(window):
    window.fill((64, 224, 208 ))  #Light Blue background

    # Initialize font
    pygame.font.init()
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)

    #  text
    title_text = font.render("Impossible Game", True, (255, 255, 255))  # Game Title
    instruction_text = small_font.render("Press Any Key to Start", True, (255, 255, 255))  # Instruction text

    # Position text in the center
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() // 2 - 50))
    window.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 - instruction_text.get_height() // 2 + 50))

    pygame.display.update()

def wait_for_key_press():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False  # Exit the loop when any key is pressed



def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]



# Menu and Pause game (Esc key) 
def show_menu(window, player):
    menu_font = pygame.font.Font(None, 36)
    menu_options = ["Resume", "Reset Character", "Reset Game"]
    selected_option = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Resume Button
                        return "resume"
                    elif selected_option == 1:  # Reset Character Button
                        return "reset_character"
                    elif selected_option == 2:  # Reset Game Button
                        return "reset_game"
                elif event.key == pygame.K_ESCAPE:
                    return "resume"

        window.fill((64, 224, 208 , 128))  

        for i, option in enumerate(menu_options):
            color = (255, 255, 255) if i == selected_option else (128, 128, 128)
            text = menu_font.render(option, True, color)
            window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50 + i * 50))

        pygame.display.update()

#Sign Up and Log in system
def draw_auth_screen(window, mode):
    window.fill((255, 182, 193))#pink  # Light Blue ish background pink: 255,182,193 light blue: 64, 224, 208
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)

    title_text = font.render(f"{'Sign Up' if mode == 'signup' else 'Log In'}", True, (255, 255, 255))
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    username_text = small_font.render("Username:", True, (255, 255, 255))
    window.blit(username_text, (WIDTH // 4, HEIGHT // 2 - 50))

    password_text = small_font.render("Password:", True, (255, 255, 255))
    window.blit(password_text, (WIDTH // 4, HEIGHT // 2 + 50))

    pygame.display.update()

def get_input(prompt):
    input_text = ""
    input_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2 + (50 if prompt == "Password:" else -50), 200, 32)
    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        pygame.draw.rect(window, (255, 255, 255), input_rect)
        text_surface = pygame.font.Font(None, 32).render(input_text, True, (0, 0, 0))
        window.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.display.flip()
#Authenticate User
def authenticate_user(mode):
    draw_auth_screen(window, mode)
    username = get_input("Username:")
    password = get_input("Password:")

    if mode == "signup":
        with open("users.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, password])
        return True
    else:
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == password:
                    return True
    return False

def auth_menu():
    while True:
        window.fill((64, 224, 208))  # Light Blue background
        font = pygame.font.Font(None, 74)
        small_font = pygame.font.Font(None, 50)

        title_text = font.render("Login/Sign up", True, (255, 255, 255))
        window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        signup_text = small_font.render("1. Sign Up", True, (255, 255, 255))
        window.blit(signup_text, (WIDTH // 2 - signup_text.get_width() // 2, HEIGHT // 2))

        login_text = small_font.render("2. Log In", True, (255, 255, 255))
        window.blit(login_text, (WIDTH // 2 - login_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if authenticate_user("signup"):
                        return
                elif event.key == pygame.K_2:
                    if authenticate_user("login"):
                        return




# Authentication system
if not os.path.exists("users.csv"):
    with open("users.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password"])

auth_menu()

#Splitting Sprite Images
def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        #Flipping Image Depending On The Movement 

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

# Getting Block Size
def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

#The Player
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "VirtualGuy", 32, 32, True)
    ANIMATION_DELAY = 3

    #Player Gravity
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.health = 100
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

        
    #Jumping
    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
    #Getting Hit
    def make_hit(self):
        self.hit = True
        
        
        
        
    #Player Move Left
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
            
    #Player Move Right
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()
        
    #Landing On A Block
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1
        
    #Updating The Sprite (Animation)
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
    def respawn(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.health = 100  # Reset health
        self.jump_count = 0
        # Reset any other necessary states
        
#Adding Blocks
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

#Creating The Block
class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

# Getting Small Block Size
def get_small_block(size):
    path = join("assets", "small.block")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return surface

#Fire Trap
class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

#Saw Trap
class Saw(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "saw")
        self.saw = load_sprite_sheets("Traps", "Saw", width, height)
        self.image = self.saw["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.saw[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

#Checkpoint
class Checkpoint(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "checkpoint")
        self.checkpoint = pygame.image.load(join("assets","checkpoint123.png")).convert_alpha()
        self.image = pygame.transform.scale(self.checkpoint, (width, height))
        self.mask = pygame.mask.from_surface(self.image)
        self.activated = False  # To track if the checkpoint is activated
        self.respawn_pos = (x + width // 2, y + height)  # Default respawn position at the checkpoint

    def activate(self):
        self.activated = True

    def check_activation(self, player):
        if self.rect.colliderect(player.rect):
            if not self.activated:  # Only activate if it's not already activated
                self.activate()
            return self.respawn_pos  # Always return the current respawn position
        return None


#Spike Trap
class Spike(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "spike")
        self.spike = pygame.image.load(join("assets", "Traps", "Spikes", "idle.png")).convert_alpha()
        self.image = pygame.transform.scale(self.spike, (width, height))
        self.mask = pygame.mask.from_surface(self.image)

#Block Trap
class Blk(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "blk")
        self.blk = pygame.image.load(join("assets", "Traps", "Spike Head", "Idle.png")).convert_alpha()
        self.image = pygame.transform.scale(self.blk, (width, height))
        self.mask = pygame.mask.from_surface(self.image)

#Block 2 trap
class Blk2(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "blk2")
        self.blk2 = pygame.image.load(join("assets","op 4.png")).convert_alpha()
        self.image = pygame.transform.scale(self.blk2, (width, height))
        self.mask = pygame.mask.from_surface(self.image)



# Trampoline Trap
class Trampoline(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "trampoline")
        self.trampoline = load_sprite_sheets("Traps", "Trampoline", width, height)
        self.image = self.trampoline["idle"][0]  # Default to idle image
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "idle"
        self.launched = False

    def launch(self):
        self.animation_name = "Jump"
        self.launched = True
        self.animation_count = 0  # Reset animation count to start the jump animation

    def reset(self):
        self.animation_name = "idle"
        self.launched = False

    def loop(self):
        sprites = self.trampoline[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        # Reset animation after the jump finishes
        if self.animation_name == "Jump" and self.animation_count // self.ANIMATION_DELAY >= len(sprites):
            self.reset()




        

#The Background (Function)
def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

#Background Drawing
def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()

#Verticle Collision Defining
def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
        

    player.move(-dx, 0)
    player.update()
    return collided_object

#Player Movement With Keys
def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj:
            if obj.name == "fire" or obj.name == "saw" or obj.name == "spike" or obj.name == "blk":
                player.make_hit()
            elif obj.name == "trampoline":
                trampoline = obj
                if not trampoline.launched:
                    trampoline.launch()
                    player.y_vel = -12  # Ajust Launch player into the air

                    

#Defining The Window (Function)
def main(window):
    clock = pygame.time.Clock()
    global checkpoint_pos  # Use global variable to track checkpoint position
    
    #Loading Screen Variables
    draw_loading_screen(window)
    wait_for_key_press()
    # Start background music when game starts
    play_background_music()
    play_sound('start')
    background, bg_image = get_background("Green.png")

    block_size = 96
    # Smaller block size
    small_block_size = 48

    # Define the checkpoint position
    checkpoint_pos = None
    default_respawn_pos = (0, HEIGHT - block_size)  # Default respawn position
    
    #Defining The Player
    player = Player(100, 100, 50, 50)
    
    # Fire traps configuration (x_position, y_offset)
    fire_positions = [
        (350, -352), (100, -64), (4330, -64), (4360, -64), (4530, -64),
        (4560, -64), (4700, -64), (4730, -64), (4880, -64), (4900, -64),
        (5040, -64), (5070, -64), (6350, -255)
    ]
    fires = [Fire(x, HEIGHT - block_size + y_offset, 16, 32) for x, y_offset in fire_positions]
    for fire in fires:
        fire.on()

    # Saw traps configuration (x_position, y_offset)
    saw_positions = [
        (300, -75), (400, -75), (3850, -170)
    ]
    saws = [Saw(x, HEIGHT - block_size + y_offset, 38, 38) for x, y_offset in saw_positions]
    for saw in saws:
        saw.on()

    # Trampolines configuration (x_position, y_offset)
    trampoline_positions = [
        (2510, -100), (2790, -250), (3050, -150), (4440, -343),
        (4835, -373), (5920, -373)
    ]
    trampolines = [Trampoline(x, HEIGHT - block_size + y_offset, 28, 28) for x, y_offset in trampoline_positions]

    # Spike traps configuration (x_position, y_offset)
    spike_positions = [
        (600, -64), (500, -64), (700, -64), (800, -64), (600, -544),
        (400, -352), (900, -64), (1100, -64), (1250, -64), (1940, -160),
        (2120, -350), (2301, -64), (2371, -64), (2441, -64), (2511, -64),
        (2581, -64), (2651, -64), (2721, -64), (2791, -64), (2861, -64),
        (2931, -64), (3001, -64), (3071, -64), (3141, -64), (3211, -64),
        (5200, -64), (5400, -64), (5600, -64), (5800, -64), (4370, -350),
        (4510, -350), (4730, -350), (4870, -350), (4940, -350), (5010, -350),
        (5080, -350), (5150, -350), (5220, -350), (5290, -350), (5360, -350),
        (5430, -350), (5500, -350), (5570, -350), (5640, -350), (5710, -350),
        (5780, -350), (5850, -350), (5920, -350), (5990, -350), (6010, -350),
        (6080, -350), (6150, -350), (6220, -350), (6600, -64), (6670, -64),
        (6740, -64), (6810, -64), (6880, -64)
    ]
    spikes = [Spike(x, HEIGHT - block_size + y_offset, 70, 64) for x, y_offset in spike_positions]

    # Block traps
    blk = Blk(1700, HEIGHT - block_size - 64, 70, 64)
    blk2 = Blk2(1600, HEIGHT - block_size - 400, 70, 64)

    # Checkpoints configuration (x_position, y_offset)
    checkpoint_positions = [
        (1400, -168), (3500, -168), (6500, -550)
    ]
    checkpoints = [Checkpoint(x, HEIGHT - block_size + y_offset, 200, 200) for x, y_offset in checkpoint_positions]

    # Floor blocks
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 8) // block_size)]

    # Platform blocks configuration (x_multiplier, y_multiplier)
    platform_positions = [
        (0, 2), (4, 4), (3, 4), (-1, 3), (-1, 4), (-1, 5), (-1, 6),
        (-1, 7), (-1, 8), (-1, 9), (-1, 2), (6, 6), (5, 6), (5, 5),
        (20, 2), (21, 2), (22, 2), (23, 2), (23, 5), (21, 3), (22, 3),
        (23, 3), (23, 4), (22, 4), (40, 2), (41, 3), (42, 2)
    ]
    platforms = [Block(x_mult * block_size, HEIGHT - y_mult * block_size, block_size) 
                 for x_mult, y_mult in platform_positions]

    #Long horizontal platform (blocks 45-66)
    long_platform = [Block(i * block_size, HEIGHT - block_size * 4, block_size) 
                     for i in range(45, 67)]
    
    # Additional platforms at block 65-66 level 3
    long_platform.extend([Block(65 * block_size, HEIGHT - block_size * 3, block_size),
                         Block(66 * block_size, HEIGHT - block_size * 3, block_size)])

    # Vertical pillars at x=48 and x=57
    pillar_heights = [5, 6, 7, 8.75, 9.75, 10.75, 11.75]
    pillars = []
    for height in pillar_heights:
        pillars.append(Block(48 * block_size, HEIGHT - block_size * height, block_size))
        pillars.append(Block(57 * block_size, HEIGHT - block_size * height, block_size))
    
    # Additional blocks
    pillars.extend([
        Block(68 * block_size, HEIGHT - block_size * 5, block_size),
        Block(58 * block_size, HEIGHT - block_size * 11.75, block_size)
    ])

    # Small block
    small_block = Block(block_size * 6, HEIGHT - block_size * 3, small_block_size)

    # Combine all objects
    objects = [
        *floor,
        *platforms,
        *long_platform,
        *pillars,
        small_block,
        *fires,
        *saws,
        *spikes,
        *trampolines,
        *checkpoints,
        blk,
        blk2
    ]

    offset_x = 0
    scroll_area_width = 200

    #Creating A While Loop Allowing You To Exit The Game
    run = True
    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            menu_action = show_menu(window, player)
            if menu_action is not None:
                if menu_action == "reset_character":
                    player.make_hit()
                    play_sound('die')
                elif menu_action == "reset_game":
                    player.respawn(100, 100)
                    play_sound('start')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            #Double Jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()

        #Loops for animation
        player.loop(FPS)
        
        for fire in fires:
            fire.loop()
        for saw in saws:
            saw.loop()
        for tramp in trampolines:
            tramp.loop()
            
        handle_move(player, objects)

        draw(window, background, bg_image, player, objects, offset_x)
        
        #check for checkpoint collision
        for checkpoint in checkpoints:
            if pygame.sprite.collide_mask(player, checkpoint):
                if not checkpoint.activated:
                    play_sound('checkpoint')
                checkpoint_pos = (player.rect.x, player.rect.y)
                checkpoint.activated = True

        #Respawn player if hit
        if player.hit:
            play_sound('die')
            if checkpoint_pos:
                player.rect.x, player.rect.y = checkpoint_pos
            else:
                player.rect.x, player.rect.y = default_respawn_pos
            player.hit = False
            offset_x = player.rect.x - WIDTH // 2

        #checkpoint activation check
        respawn_pos = None
        for checkpoint in checkpoints:
            pos = checkpoint.check_activation(player)
            if pos:
                respawn_pos = pos
                break
                
        if respawn_pos:
            checkpoint_pos = respawn_pos

        #Handle player death and respawn
        if player.health <= 0:
            player.respawn(*default_respawn_pos)
            offset_x = 0

        #moving Background so it doesnt look static
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    #stop background music when quitting
    stop_background_music()
    pygame.quit()
    quit()

#END GAME
if __name__ == "__main__":
    main(window)     # defining the window function

