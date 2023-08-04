import random
import sys
import requests
import json

# import pygame + pygame locals
import pygame
import pygame_menu
from pygame.locals import (
    RLEACCEL,
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    KEYDOWN,
    QUIT,
)
from pygame_menu import themes

# initialize pygame
pygame.mixer.init()
pygame.init()
pygame.font.init()

# ------------------------ constants ------------------------

# window
WIDTH = 500
HEIGHT = 400
WINDOW_SIZE = [WIDTH, HEIGHT]
GROUND_HEIGHT = int(HEIGHT / 4)
FLOOR = int(HEIGHT / 4 * 3)

# timing
FPS = 30
SPEED = 6

# events
ADDOBSTACLE = pygame.USEREVENT + 1
SCORECOUNT = ADDOBSTACLE + 1
ADDCLOUD = SCORECOUNT + 1
DURATION = ADDCLOUD + 1

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

OBJ_COLOR = DARK_GRAY
GROUND_COLOR = BLACK

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
volume = 10
high_score = 0

# background music (change later)
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# sound effects
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

playing_music = True
playing_sound_effects = True


# ------------------------ sprites ------------------------


# player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        if game_theme == "default":
            self.surf = pygame.image.load("jet.png").convert()
        else:
            self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.left = 50
        self.rect.bottom = FLOOR

    def update(self, pressed_keys):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 38:
            self.rect.top = 38
        if self.rect.bottom >= FLOOR:
            self.rect.bottom = FLOOR


# obstacle sprite class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()
        random_num = random.randint(0, 1)
        if game_theme == "default":
            if random_num == 0:
                self.surf = pygame.image.load("missile.png").convert()
            else:
                self.surf = pygame.image.load("missile.png").convert()
        else:
            if random_num == 0:
                self.surf = pygame.image.load("jet.png").convert()
            else:
                self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(center=(WIDTH + 20, FLOOR - 10))
        self.speed = SPEED

    # move obstacle based on its speed
    # remove when it passes off screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# cloud sprite class
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        if game_theme == "default":
            self.surf = pygame.image.load("cloud.png").convert()
        else:
            self.surf = pygame.image.load("cloud.png").convert()

        self.surf.set_colorkey(BLACK, RLEACCEL)
        
        # var = pygame.PixelArray(self.surf)
        # var.replace(WHITE, OBJ_COLOR)
        # del var

        self.rect = self.surf.get_rect(
            center=(
                random.randint(WIDTH + 20, WIDTH + 100),
                random.randint(
                    38, int(HEIGHT - GROUND_HEIGHT - (1 / 2) * self.surf.get_height())
                ),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# ------------------------ play ------------------------


def play_game():
    main_menu.disable()

    global high_score
    score = min = sec = 0

    obstacle_interval = random.randint(850, 1200)

    # set event timers
    pygame.time.set_timer(ADDOBSTACLE, obstacle_interval)
    pygame.time.set_timer(ADDCLOUD, 700)
    pygame.time.set_timer(SCORECOUNT, 250)
    pygame.time.set_timer(DURATION, 1000)

    ground = pygame.Surface((WIDTH, GROUND_HEIGHT))
    ground.fill((160,82,45))

    # jump physics
    v = SPEED  # velocity
    m = 1  # mass
    is_jumping = False

    # initialize player
    player = Player()

    # create sprite groups
    obstacles = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    # main game loop
    while running:
        # for every event in event queue
        for event in pygame.event.get():
            # quit game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # add new obstacle to screen
            elif event.type == ADDOBSTACLE:
                new_obstacle = Obstacle()
                obstacles.add(new_obstacle)
                all_sprites.add(new_obstacle)
                obstacle_interval = random.randint(790, 1600)
                pygame.time.set_timer(ADDOBSTACLE, obstacle_interval)
            # add cloud to screen
            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
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

        if pressed_keys[K_UP]:
            is_jumping = True

        if is_jumping == True:
            F = (1 / 2) * m * (v**2)
            player.rect.bottom -= F
            v -= 0.5

            if v < 0:
                m = -1
            if v <= -SPEED:
                is_jumping = False
                player.rect.bottom = FLOOR
                v = SPEED
                m = 1

        # update obstacle positions
        obstacles.update()
        clouds.update()

        screen.fill(bg_color)
        screen.blit(ground, (0, HEIGHT / 4 * 3))

        # draw all sprites
        for sprite in clouds:
            screen.blit(sprite.surf, sprite.rect)
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

            # turn off sounds
            move_up_sound.stop()
            move_down_sound.stop()
            collision_sound.play()

            # create and display game end menu
            end_menu = menu.create_end_menu(score, min, sec)
            end_menu.mainloop(screen)

            running = False

        # tick
        clock.tick(FPS)


# ------------------------ options ------------------------


def toggle_music(selected):
    if selected == False:
        pygame.mixer.music.stop()
        playing_music = False
    else:
        pygame.mixer.music.play(loops=-1)
        playing_music = True


def toggle_sound_effects(selected):
    if selected == False:
        move_up_sound.set_volume(0)
        move_down_sound.set_volume(0)
        collision_sound.set_volume(0)
        playing_sound_effects = False
    else:
        move_up_sound.set_volume(volume)
        move_down_sound.set_volume(volume)
        collision_sound.set_volume(volume)
        playing_sound_effects = True


def adjust_volume(selected):
    volume = selected
    pygame.mixer.music.set_volume(volume)
    move_up_sound.set_volume(volume)
    move_down_sound.set_volume(volume)
    collision_sound.set_volume(volume)


def change_window_theme(selected):
    window_theme = selected
    main_menu = menu.create_main_menu(window_theme)
    main_menu.mainloop(screen)


def change_game_theme(selected):
    game_theme = selected
    print(game_theme)


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

        # settings submenu
        settings_menu = pygame_menu.Menu(
            height=HEIGHT, theme=window_theme, title="Settings", width=WIDTH
        )
        settings_menu.add.button("Window theme", window_theme_menu)
        settings_menu.add.button("Game theme", game_theme_menu)
        settings_menu.add.toggle_switch(
            "Music",
            default=playing_music,
            state_text=("Off", "On"),
            onchange=toggle_music,
        )
        settings_menu.add.toggle_switch(
            "Sound effects",
            default=playing_sound_effects,
            state_text=("Off", "On"),
            onchange=toggle_sound_effects,
        )
        settings_menu.add.range_slider(
            "Volume",
            volume,
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            1,
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

def get_weather():
    p = {'key': '3864d0d26a9c4deab5a221512230308', 'q':'92620','aqi':'no'}
    r = requests.get('http://api.weatherapi.com/v1/current.json', params=p)
    
    # print(json.dumps(r.json(), indent = 4))
    
    global current_temp_f
    global bg_color
    bg_color = LIGHT_GRAY

    current_temp_f = int(r.json()["current"]["temp_f"])
    current_time = int(r.json()["location"]["localtime"][11:13])
    print(current_time)

    # change background color based on temp/time
    if current_temp_f > 70 and current_time > 7 and current_time < 18:
        bg_color = (135, 206, 250)
    elif current_time > 7 and current_time < 18:
        bg_color = (50,50,150)
    elif current_time > 4 and current_time < 7:
        bg_color = (255, 200, 200)
    else:
        bg_color = (20,20,85)

# ------------------------ main ------------------------


def main():
    global menu
    global main_menu
    global menu
    
    get_weather()
    # create and display menu
    menu = Menu()
    main_menu = menu.create_main_menu(window_theme)
    main_menu.mainloop(screen)


# -------------------------------------------------

if __name__ == "__main__":
    main()
