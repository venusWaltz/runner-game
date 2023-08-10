import random
import sys
import os

# import pygame + pygame locals
import pygame
import pygame_menu
from pygame.locals import (
    K_ESCAPE,
    K_UP,
    QUIT,
)
from pygame_menu import themes

# initialize pygame
pygame.mixer.init()
pygame.init()
pygame.font.init()

# ------------------------ constants ------------------------

# window
WIDTH = 750
HEIGHT = 500
WINDOW_SIZE = [WIDTH, HEIGHT]
GROUND_HEIGHT = int(HEIGHT / 4)
FLOOR = int(HEIGHT / 4 * 3)

# timing
FPS = 30
JUMP_SPEED = 6
DEFAULT_SPEED = 9
speed = DEFAULT_SPEED

# events
ADDOBSTACLE = pygame.USEREVENT + 1
SCORECOUNT = ADDOBSTACLE + 1
ADDCLOUD = SCORECOUNT + 1
DURATION = ADDCLOUD + 1
SPEEDUP = DURATION + 1
FRAMECHANGE = SPEEDUP + 1

# menu info
INFO = ["Developed by Fariah Saleh", "2023"]

# themes
DEFAULT = themes.THEME_DEFAULT.copy()
BLUE = themes.THEME_BLUE.copy()
DARK = themes.THEME_DARK.copy()
GREEN = themes.THEME_GREEN.copy()
ORANGE = themes.THEME_ORANGE.copy()
SOLARIZED = themes.THEME_SOLARIZED.copy()

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BROWN = (140,62,25)
LIGHT_BLUE = (135, 206, 250)
BLUE = (50,50,150)
DARK_BLUE = (20,20,85)
PINK = (255, 200, 200)

OBJ_COLOR = DARK_GRAY
BG_COLOR = BLACK

# ------------------------ setup ------------------------

# set screen size and title
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Runner game")
font = pygame.font.Font(None, 28)
clock = pygame.time.Clock() 

# defaults
window_theme = DARK
game_theme = "default"
sound = True
volume = 1
high_score = 0

# background music (change later)
pygame.mixer.music.load("main_title.mp3")

# sound effects
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

playing_music = True
playing_sound_effects = True


# ------------------------ images ------------------------

background_images = []
run_images = []
jump_images = []
obs_images = []
images = [background_images, run_images, jump_images, obs_images]
folder_path = ["images/background", "images/run", "images/jump", "images/obs"]

for (image_list, path) in zip(images, folder_path):
    for file in os.listdir(path):
        image = pygame.image.load(os.path.join(path,file)).convert_alpha()
        image_list.append(image)

bg_width = background_images[0].get_width()
bg_height = background_images[0].get_height()
bg_scale = bg_height / bg_width
background_images = [pygame.transform.scale(layer, (WIDTH, int(WIDTH*bg_scale))) for layer in background_images]

ground_img = pygame.image.load("images/ground.png").convert_alpha() #(24,20,37), (38,43,68), (58,68,102)
gr_width = ground_img.get_width()
gr_height = ground_img.get_height()
ground_img = pygame.transform.scale(ground_img, (GROUND_HEIGHT, GROUND_HEIGHT))
ground_width = ground_img.get_width()
ground_n = (WIDTH // ground_width) + 1

# ------------------------ sprites ------------------------


# player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        if game_theme == "default":
            self.surf = run_images[0]
        else:
            self.surf = pygame.image.load("jet.png").convert()
        self.rect = self.surf.get_rect()
        self.rect.left = int(WIDTH/7)
        self.rect.bottom = FLOOR
        self.wait = 0

    # animate walk cycle
    def change(self, num, img = run_images):
        bottom = self.rect.bottom
        if img:
            self.surf = img[num]
        self.rect = self.surf.get_rect()
        self.rect.left = int(WIDTH/7)
        self.rect.bottom = bottom

    def update(self, v, m, is_jumping):
        # while character is jumping
        if is_jumping == True:
            F = (1 / 2) * m * (v**2)
            self.rect.bottom -= F
            v -= 0.5

            if v > 0:
                self.change(0,jump_images)
            if v < 0:
                m = -1
                self.wait += 1
                if self.wait > 6:
                    self.change(1,jump_images)
            if v <= -JUMP_SPEED:
                is_jumping = False
                self.rect.bottom = FLOOR
                v = JUMP_SPEED
                m = 1
                self.wait = 0
        return v, m, is_jumping


# obstacle sprite class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()
        self.surf = pygame.image.load("images/obs/obs_6.png").convert_alpha()

        # self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(center=(WIDTH + 20, FLOOR - int(self.surf.get_height()/3*2)))
        self.speed = speed

        self.num = 1

    # move obstacle based on its speed
    # remove when it passes off screen
    def update(self):
        center = self.rect.center
        if self.num == 4:
            self.surf =  obs_images[8]
            self.rect = self.surf.get_rect(center=center)
        elif self.num == 8:
            self.surf =  obs_images[9]
            self.rect = self.surf.get_rect(center=center)
        elif self.num == 12:
            self.surf = obs_images[10]
            self.rect = self.surf.get_rect(center=center)
        elif self.num == 16:
            self.surf = obs_images[11]
            self.rect = self.surf.get_rect(center=center)
        elif self.num == 20:
            self.surf = obs_images[10]
            self.rect = self.surf.get_rect(center=center)
            self.num = -1
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        self.num += 1


# ------------------------ play ------------------------


def play_game():
    main_menu.disable()

    pygame.mixer.music.play(loops=-1)

    global high_score
    global speed 
    global images
    global bg_width
    speed = DEFAULT_SPEED
    score = min = sec = 0

    obstacle_interval = random.randint(850, 1200)

    # set event timers
    pygame.time.set_timer(ADDOBSTACLE, obstacle_interval)
    pygame.time.set_timer(ADDCLOUD, 700)
    pygame.time.set_timer(SCORECOUNT, 250)
    pygame.time.set_timer(DURATION, 1000)
    pygame.time.set_timer(SPEEDUP, 4000)
    pygame.time.set_timer(FRAMECHANGE, 75)

    ground_pos = []
    for i in range(ground_n):
        ground_pos.append(i*ground_width)

    layers = len(background_images)
    bg_pos = [0] * layers
    b = [WIDTH] * layers
    bg_pos = bg_pos + b
    bg_speed = [1,2,4,6]

    # jump physics
    v = JUMP_SPEED  # velocity
    m = 1  # mass
    is_jumping = False

    # initialize player
    player = Player()
    sp_num = 0

    # create sprite groups
    obstacles = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    # main game loop
    while running:

        clock.tick(FPS)

        # for every event in event queue
        for event in pygame.event.get():
            # quit game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # change player frame
            elif event.type == FRAMECHANGE:
                if is_jumping == False:
                    if sp_num >= len(run_images):
                        sp_num = 0
                    player.change(sp_num)
                    sp_num += 1
            # add new obstacle to screen
            elif event.type == ADDOBSTACLE:
                new_obstacle = Obstacle()
                obstacles.add(new_obstacle)
                all_sprites.add(new_obstacle)
                obstacle_interval = random.randint(790, 1600)
                pygame.time.set_timer(ADDOBSTACLE, obstacle_interval)
            # increase speed
            elif event.type == SPEEDUP:
                    speed += 0.25
            # update score count
            elif event.type == SCORECOUNT:
                score += 1
            # update duration count
            elif event.type == DURATION:
                if sec == 59:
                    sec = 0
                    min += 1
                else:
                    sec += 1

        # get pressed keys
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_ESCAPE]:
            # kill sprites
            for sp in all_sprites:
                sp.kill()

            # turn off sounds and music
            move_up_sound.stop()
            collision_sound.play()

            pygame.mixer.music.stop()
            playing_music = False

            # open main menu
            main_menu.enable()

            running = False

        # player jumps with up keypress
        if pressed_keys[K_UP]:
            is_jumping = True

        # update player
        v,m,is_jumping = player.update(v,m,is_jumping)

        # update obstacle positions
        obstacles.update()
        # clouds.update()

        # fill background
        screen.fill(BG_COLOR)


        # bg layer positions
        for i in range(layers):
            if bg_pos[i] <= -WIDTH:
                bg_pos[i] = WIDTH
            if bg_pos[i + layers] <= -WIDTH:
                bg_pos[i + layers] = WIDTH
            if bg_pos[i] < -background_images[i].get_width():
                bg_pos[i] = bg_pos[i + layers] + background_images[i].get_width()
            screen.blit(background_images[i], (bg_pos[i], 0))
            screen.blit(background_images[i], (bg_pos[i + layers], 0))
            bg_pos[i] -= bg_speed[i]
            bg_pos[i + layers] -= bg_speed[i]

        # ground
        for i in range(ground_n):
            screen.blit(ground_img, (ground_pos[i], FLOOR))
            ground_pos[i] -= speed
            if ground_pos[i] <= -ground_width:
                ground_pos[i] = WIDTH

        # draw all sprites
        for sprite in obstacles:
            screen.blit(sprite.surf, sprite.rect)
        screen.blit(player.surf, player.rect)

        # display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # display game duration
        duration_text = font.render(f"Time: {min}:{sec}", True, WHITE)
        d_text_width = font.size(f"Time: {min}:{sec}")[0]
        screen.blit(duration_text, (WIDTH - d_text_width - 10, 10))

        pygame.display.flip()

        # end game when player collides with an obstacle
        if pygame.sprite.spritecollideany(player, obstacles):
            # save score
            if score > high_score:
                high_score = score

            # kill sprites
            for sp in all_sprites:
                sp.kill()

            # turn off sounds and music
            move_up_sound.stop()
            collision_sound.play()

            pygame.mixer.music.stop()
            playing_music = False

            # create and display game end menu
            end_menu = menu.create_end_menu(score, min, sec)
            end_menu.mainloop(screen)

            running = False


# ------------------------ options ------------------------


def toggle_music(selected):
    if selected == False:
        pygame.mixer.music.set_volume(0)
        playing_music = False
    else:
        pygame.mixer.music.set_volume(volume)
        playing_music = True


def toggle_sound_effects(selected):
    if selected == False:
        move_up_sound.set_volume(0)
        collision_sound.set_volume(0)
        playing_sound_effects = False
    else:
        move_up_sound.set_volume(volume)
        collision_sound.set_volume(volume)
        playing_sound_effects = True


def adjust_volume(selected):
    global volume
    volume = selected/10
    pygame.mixer.music.set_volume(volume)
    move_up_sound.set_volume(volume)
    collision_sound.set_volume(volume)


def change_window_theme(selected):
    window_theme = selected
    main_menu = menu.create_main_menu(window_theme)
    main_menu.mainloop(screen)


def change_game_theme(selected):
    game_theme = selected


def return_to_main_menu():
    end_menu.disable()
    main_menu.enable()


def restart():
    end_menu.disable()
    play_game()


# ------------------------ menus ------------------------


class Menu:
    def __init__(self):
        pass

    # --------------------- game end menu ---------------------
    """
    score
    duration
    >try again
    >back to main menu
    >quit
    """

    def create_end_menu(self, score, min, sec):
        global end_menu

        # game end menu
        end_menu = pygame_menu.Menu(
            height=HEIGHT, theme=window_theme, title="Game Over", width=WIDTH
        )

        end_menu.add.label(f"Score: {score}")
        end_menu.add.label(f"Duration: {min}:{sec}")
        if high_score > 0:
            end_menu.add.label(f"High score: {high_score}")
        end_menu.add.button("Try again", restart)
        end_menu.add.button("Back to main menu", return_to_main_menu)
        end_menu.add.button("Quit", pygame.quit)
        return end_menu

    # --------------------- main menu ---------------------
    """
    >play
    >settings
        >window theme
            >default
            >blue
            >dark
            >green
            >orange
            >solarized
        >game theme
            >default
        >music toggle
        >sound effects toggle
        >volume
    >info
    >quit
    """

    def create_main_menu(self, window_theme):
        # game theme submenu
        game_theme_menu = pygame_menu.Menu(
            height=HEIGHT, theme=window_theme, title="Game theme", width=WIDTH
        )
        game_theme_menu.add.button("Default", lambda: change_game_theme("default"))
        game_theme_menu.add.button("Other", lambda: change_game_theme("other"))
        game_theme_menu.add.button("Back to main menu", return_to_main_menu)

        # window theme submenu
        window_theme_menu = pygame_menu.Menu(
            height=HEIGHT, theme=window_theme, title="Window theme", width=WIDTH
        )
        window_theme_menu.add.button("Default", lambda: change_window_theme(DEFAULT))
        window_theme_menu.add.button("Blue", lambda: change_window_theme(BLUE))
        window_theme_menu.add.button("Dark", lambda: change_window_theme(DARK))
        window_theme_menu.add.button("Green", lambda: change_window_theme(GREEN))
        window_theme_menu.add.button("Orange", lambda: change_window_theme(ORANGE))
        window_theme_menu.add.button(
            "Solarized", lambda: change_window_theme(SOLARIZED)
        )
        window_theme_menu.add.button("Back to main menu", return_to_main_menu)

        # settings submenu
        settings_menu = pygame_menu.Menu(
            height=HEIGHT, theme=window_theme, title="Settings", width=WIDTH
        )
        settings_menu.add.button("Window theme", window_theme_menu)
        settings_menu.add.button("Game theme", game_theme_menu)
        settings_menu.add.toggle_switch(
            title="Music",
            default=playing_music,
            state_text=("Off", "On"),
            onchange=toggle_music,
        )
        settings_menu.add.toggle_switch(
            title="Sound effects",
            default=playing_sound_effects,
            state_text=("Off", "On"),
            onchange=toggle_sound_effects,
        )
        settings_menu.add.range_slider(
            title="Volume",
            default=volume*10,
            range_values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            increment=1,
            width=275,
            range_box_single_slider=True,
            onchange=adjust_volume,
        )
        settings_menu.add.button("Return to main menu", pygame_menu.events.BACK)

        # info submenu
        info_menu = pygame_menu.Menu(
            height=HEIGHT, theme=window_theme, title="Info", width=WIDTH
        )

        for item in INFO:
            info_menu.add.label(item, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
            info_menu.add.vertical_margin(30)

        info_menu.add.button("Return to main menu", pygame_menu.events.BACK)

        # main menu
        main_menu = pygame_menu.Menu(
            height=HEIGHT, theme=window_theme, title="Welcome", width=WIDTH
        )

        # user_name = menu.add.text_input('Name: ', default='username', maxchar=10)
        main_menu.add.button("Play", play_game)
        main_menu.add.button("Settings", settings_menu)
        main_menu.add.button("Info", info_menu)
        main_menu.add.button("Quit", pygame.quit)
        return main_menu


# ------------------------ main ------------------------


def main():
    global menu
    global main_menu
    global menu
    
    # create and display menu
    menu = Menu()
    main_menu = menu.create_main_menu(window_theme)
    main_menu.mainloop(screen)


# -------------------------------------------------

if __name__ == "__main__":
    main()
