# game.py

import sys
import pygame
from pygame.locals import K_ESCAPE, K_UP, QUIT
import random
from entities import Player, Obstacle
from constants import *

class Game:
    """Manages the main game logic and loop."""

    def __init__(self, screen, menu):
        """
        Initializes the game.
        
        Args:
            screen (pygame.Surface): Used for rendering.
            menu (Menu): The central game menu system.
        """
        self.screen = screen
        self.menu = menu
        self.clock = pygame.time.Clock() 
        self.font = pygame.font.Font(None, FONTPT)
        self.initialize_sprites()
        self.initialize_background()
        self.initialize_game_parameters()
        self.running = True

    def initialize_sprites(self):
        """Initializes player and sprite groups."""
        self.player = Player(self.menu)
        self.sprite_num = 0
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def initialize_background(self):
        """Initializes background layers and their positions."""
        self.layers = self.menu.image_manager.len_bg
        self.bg_speed = [1 if i == 0 else i * 2 for i in range(self.layers)]
        self.bg_pos = [0] * self.layers
        b = [WIDTH] * self.layers
        self.bg_pos = self.bg_pos + b

    def initialize_game_parameters(self):
        """Initializes game parameters and jump physics."""
        self.ground_pos = [x*GROUND_DIM for x in range(0, WIDTH//GROUND_DIM + 1)]
        self.speed = DEFAULT_SPEED
        self.score = 0
        self.min = 0
        self.sec = 0
        self.v = JUMP_SPEED  # velocity
        self.m = 1  # mass
        self.is_jumping = False

    def play_game(self): 
        """Starts the main game loop, continuing until the game ends.""" 
        self.initialize_game()

        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update_game_state()
            self.render()

            if self.check_collisions():
                self.handle_game_end()
                break

    def initialize_game(self):
        """Initializes game elements."""
        self.menu.main_menu.disable()
        self.menu.sound_manager.play_music()
        self.set_event_timers()

    def set_event_timers(self):
        """Sets timers for game events."""
        pygame.time.set_timer(ADDOBSTACLE, random.randint(TIMER_MIN, TIMER_MAX))
        pygame.time.set_timer(SCORECOUNT, SCORECOUNT_OFFSET)
        pygame.time.set_timer(DURATION, DURATION_OFFSET)
        pygame.time.set_timer(SPEEDUP, SPEEDUP_OFFSET)
        pygame.time.set_timer(FRAMECHANGE, FRAMECHANGE_OFFSET)

    def handle_events(self):
        """
        Handles all events in game including quitting, updating player
        and obstacle animation, increasing game speed, and updating 
        time and score count.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit_game()
            elif event.type == FRAMECHANGE and not self.is_jumping:
                self.handle_frame_change()
            elif event.type == ADDOBSTACLE:
                self.add_obstacle()
            elif event.type == SPEEDUP:
                self.speed += SPEED_INCREMENT
            elif event.type == SCORECOUNT:
                self.score += 1
            elif event.type == DURATION:
                self.update_time()
                    
        self.handle_player_input()

    def quit_game(self):
        """Handles quitting the game."""
        pygame.quit()
        sys.exit()

    def handle_frame_change(self):
        """Handles player sprite animation."""
        if self.sprite_num >= len(self.menu.image_manager.run_imgs):
            self.sprite_num = 0
        self.player.animate(self.sprite_num, 
                            self.menu.image_manager.run_imgs)
        self.sprite_num += 1

    def add_obstacle(self):
        """Adds a new obstacle to the game at a random time interval."""
        new_obstacle = Obstacle(self.menu)
        self.obstacles.add(new_obstacle)
        self.all_sprites.add(new_obstacle)
        obstacle_interval = random.randint(TIMER_MIN, TIMER_MAX)
        pygame.time.set_timer(ADDOBSTACLE, obstacle_interval)

    def update_time(self):
        """Updates duration of current game progress."""
        if self.sec == 59:
            self.sec = 0
            self.min += 1
        else:
            self.sec += 1
    
    def handle_player_input(self):
        """Handles keyboard input from user."""
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.is_jumping = True
        if pressed_keys[K_ESCAPE]:
            for sp in self.all_sprites:
                sp.kill()
            self.menu.sound_manager.play_collision()
            self.menu.main_menu.enable()
            self.running = False

    def update_game_state(self):
        """Updates player and obstacle positions."""
        self.v, self.m, self.is_jumping = self.player.update(
            self.v, self.m, self.is_jumping)
        self.obstacles.update(self.speed)

    def render(self):
        """Renders all objects to screen."""
        self.screen.fill(BLACK)
        self.draw_parallax_background()
        self.draw_ground()
        self.draw_player()
        self.draw_obstacles()
        self.draw_score()
        self.draw_duration()
        pygame.display.flip()

    def draw_parallax_background(self):
        """Manages movement of and draws the parallaxing background."""
        for i in range(self.layers):
            self.bg_pos[i] -= self.bg_speed[i]
            self.bg_pos[i + self.layers] -= self.bg_speed[i]
            if self.bg_pos[i] <= -WIDTH:
                self.bg_pos[i] = WIDTH
            if self.bg_pos[i + self.layers] <= -WIDTH:
                self.bg_pos[i + self.layers] = WIDTH
            if self.bg_pos[i] < -self.menu.image_manager.bg_width[i]:
                self.bg_pos[i] = (self.bg_pos[i + self.layers] + 
                                  self.menu.image_manager.bg_width[i])
            self.screen.blit(self.menu.image_manager.bg_imgs[i], 
                             (self.bg_pos[i], 0))
            self.screen.blit(self.menu.image_manager.bg_imgs[i], 
                             (self.bg_pos[i + self.layers], 0))

    def draw_ground(self):
        """Handles movement of and draws the ground tiles."""
        self.ground_pos = [x - self.speed for x in self.ground_pos]
        if self.ground_pos[0] < -GROUND_DIM:
            self.ground_pos.pop(0)
            self.ground_pos.append(self.ground_pos[-1] + GROUND_DIM)
        for pos in self.ground_pos:
            self.screen.blit(self.menu.image_manager.ground_img, (pos, FLOOR))

    def draw_player(self):
        """Draws player to screen."""
        self.screen.blit(self.player.surf, self.player.rect)

    def draw_obstacles(self):
        """Draws obstacles to screen."""
        for sprite in self.obstacles:
            self.screen.blit(sprite.glow_surf, sprite.glow_rect)
            self.screen.blit(sprite.surf, sprite.rect)

    def draw_score(self):
        """Draws score to screen."""
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def draw_duration(self):
        """Draws current game duration to screen."""
        duration_text = self.font.render(
            f"Time: {self.min}:{self.sec:02}", True, WHITE)
        d_text_width = self.font.size(f"Time: {self.min}:{self.sec:02}")[0]
        self.screen.blit(duration_text, (WIDTH - d_text_width - 10, 10))

    def check_collisions(self):
        """
        Checks for collisions between the player and obstacles.

        Returns:
            bool: True if a collision is detected, False otherwise.
        """
        return pygame.sprite.spritecollideany(self.player, self.obstacles)

    def handle_game_end(self):
        """
        Handles the end of the game by updating the high score, 
        destroying all sprites, turning off all sounds, and displaying
        the game end menu.
        """
        self.menu.update_high_score(self.score)
        for sprite in self.all_sprites:
            sprite.kill()
        self.menu.sound_manager.play_collision()
        self.menu.create_end_menu(self.score, self.min, self.sec)
        self.menu.end_menu.mainloop(self.screen)

        self.running = False