#https://realpython.com/pygame-a-primer/
import random
import sys

# import pygame + pygame locals
import pygame
import pygame_menu
from pygame.locals import (
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    KEYDOWN,
    QUIT,
)
from pygame_menu import sound, themes
from pygame_menu.examples import create_example_window

# initialize pygame
pygame.init()

# constants
WIDTH = 500
HEIGHT = 400
WINDOW_SIZE = [WIDTH, HEIGHT]
FPS = 30
ADDOBSTACLE = pygame.USEREVENT + 1
INFO = ['Developed by Fariah Saleh', '2023']
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ------------------------ sprites ------------------------


# player sprite class
class Player(pygame.sprite.Sprite):

  def __init__(self):
    super(Player, self).__init__()
    self.surf = pygame.Surface((10, 10))
    self.surf.fill((0, 0, 0))
    self.rect = self.surf.get_rect()

  def update(self, pressed_keys):
    if pressed_keys[K_UP]:
      self.rect.move_ip(0, -5)
    if pressed_keys[K_DOWN]:
      self.rect.move_ip(0, 5)
    if pressed_keys[K_LEFT]:
      self.rect.move_ip(-5, 0)
    if pressed_keys[K_RIGHT]:
      self.rect.move_ip(5, 0)

    # Keep player on screen
    if self.rect.left < 0:
      self.rect.left = 0
    if self.rect.right > WIDTH:
      self.rect.right = WIDTH
    if self.rect.top <= 0:
      self.rect.top = 0
    if self.rect.bottom >= HEIGHT:
      self.rect.bottom = HEIGHT


# obstacle sprite class
class Obstacle(pygame.sprite.Sprite):

  def __init__(self):
    super(Obstacle, self).__init__()
    self.surf = pygame.Surface((10, 10))
    self.surf.fill((255, 255, 255))
    self.rect = self.surf.get_rect(center=(
        random.randint(WIDTH + 20, WIDTH + 100),
        random.randint(0, HEIGHT),
    ))
    self.speed = random.randint(5, 10)

  # move obstacle based on its speed
  # remove when it passes off screen
  def update(self):
    self.rect.move_ip(-self.speed, 0)
    if self.rect.right < 0:
      self.kill()


# ------------------------ play ------------------------


def play_game():
  menu.disable()
  # set obstacle event index and set timer
  pygame.time.set_timer(ADDOBSTACLE, 250)

  # initialize player
  player = Player()

  # create sprite groups
  obstacles = pygame.sprite.Group()
  all_sprites = pygame.sprite.Group()
  all_sprites.add(player)

  score = 0

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

    # get pressed keys
    pressed_keys = pygame.key.get_pressed()

    # update player position
    player.update(pressed_keys)

    # update obstacle positions
    obstacles.update()

    screen.fill((100, 100, 100))

    # draw all sprites
    for sprite in all_sprites:
      screen.blit(sprite.surf, sprite.rect)

    pygame.display.flip()
    
    # end game when player collides with an obstacle
    if pygame.sprite.spritecollideany(player, obstacles):
      for sp in all_sprites:
        sp.kill()
      running = False
      menu.enable()

    # tick
    clock.tick(FPS)


# ------------------------ switch options ------------------------


def toggle_music():
  pass


def toggle_sound_effects():
  pass


def adjust_volume():
  pass


def toggle_window_theme():
  pass


def toggle_game_theme():
  pass


# ------------------------ create menu ------------------------


def create_menu(window_theme):

  # game theme menu
  game_theme_menu = pygame_menu.Menu(height=HEIGHT,
                                     theme=window_theme,
                                     title='Info',
                                     width=WIDTH)
  game_theme_menu.add.button('Window theme')

  # window theme menu
  window_theme_menu = pygame_menu.Menu(height=HEIGHT,
                                       theme=window_theme,
                                       title='Info',
                                       width=WIDTH)
  window_theme_menu.add.button('Window theme')

  # settings menu
  settings_menu = pygame_menu.Menu(height=HEIGHT,
                                   theme=window_theme,
                                   title='Info',
                                   width=WIDTH)
  # settings_menu.add.button('Window theme', window_theme_menu)
  # settings_menu.add.button('Game theme', game_theme_menu)
  settings_menu.add.toggle_switch('Music',
                                  default=1,
                                  state_text=('Off', 'On'))
  settings_menu.add.toggle_switch('Sound effects',
                                  default=1,
                                  state_text=('Off', 'On'))
  settings_menu.add.range_slider('Volume',10,[0,1,2,3,4,5,6,7,8,9,10],1,width=275)
  settings_menu.add.button('Return to menu', pygame_menu.events.BACK)

  # info menu
  info_menu = pygame_menu.Menu(height=HEIGHT,
                               theme=window_theme,
                               title='Info',
                               width=WIDTH)

  for item in INFO:
    info_menu.add.label(item,
                        align=pygame_menu.locals.ALIGN_LEFT,
                        font_size=20)
    info_menu.add.vertical_margin(30)

  info_menu.add.button('Return to main menu', pygame_menu.events.BACK)

  # main menu
  menu = pygame_menu.Menu(height=HEIGHT,
                          theme=window_theme,
                          title='Welcome',
                          width=WIDTH)

  # user_name = menu.add.text_input('Name: ', default='username', maxchar=10)
  menu.add.button('Play', play_game)
  menu.add.button('Settings', settings_menu)
  menu.add.button('Info', info_menu)
  menu.add.button('Quit', pygame.quit)

  return menu


# ------------------------ main ------------------------


def main():

  # add music + sound effects + score tracking

  global screen
  global clock
  global menu
  global window_theme
  global game_theme
  global sound
  global volume
  
  # set screen size and title
  screen = pygame.display.set_mode(WINDOW_SIZE)
  pygame.display.set_caption('Hello World!')

  clock = pygame.time.Clock() 

  window_theme = pygame_menu.themes.THEME_DARK
  game_theme = 'default'
  sound = True
  volume = 10

  # create and display menu
  menu = create_menu(window_theme)
  menu.mainloop(screen)


# -------------------------------------------------

if __name__ == '__main__':
  main()
