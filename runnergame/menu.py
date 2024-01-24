# menu.py

import pygame
import pygame_menu
from game import Game
from constants import (WIDTH, HEIGHT, DEFAULT, BLUE, DARK, GREEN, 
                       ORANGE, SOLARIZED)

class Menu:
    """Manages the game menu system."""

    def __init__(self, screen, sound_manager, image_manager, info):
        """
        Initializes the menu system.

        Args:
            screen (pygame.Surface): Used for rendering.
            sound_manager (SoundManager): Used for audio control.
            image_manager (ImageManager): Used for image control.
            info (list[str]): Information to display under Info menu.
        """
        self.screen = screen
        self.sound_manager = sound_manager
        self.image_manager = image_manager
        self.info = info
        self.high_score = 0
        self.window_theme = DARK
        self.main_menu = None
        self.end_menu = None
    
    def create_main_menu(self):
        """
        Creates the main menu with options to play the game, modify
        settings, view game information, or quit the application.
        """
        self.main_menu = pygame_menu.Menu(
            height=HEIGHT, theme=self.window_theme, 
            title="Welcome", width=WIDTH
        )
        settings_menu = self.create_settings_menu()
        info_menu = self.create_info_menu()
        self.main_menu.add.button("Play", self.start_game)
        self.main_menu.add.button("Settings", settings_menu)
        self.main_menu.add.button("Info", info_menu)
        self.main_menu.add.button("Quit", pygame.quit)

    def create_settings_menu(self):
        """
        Creates the Settings submenu to be included in the Main Menu; 
        includes settings to control theme, music, and sound effects.

        Returns:
            pygame_menu.Menu: The configured Settings submenu.
        """
        settings_menu = pygame_menu.Menu(
            height=HEIGHT, theme=self.window_theme, 
            title="Settings", width=WIDTH
        )
        window_theme_menu = self.create_window_theme_menu()
        settings_menu.add.button("Window theme", window_theme_menu)
        settings_menu.add.toggle_switch(
            title="Music",
            default=self.sound_manager.playing_music,
            state_text=("Off", "On"),
            onchange=self.sound_manager.toggle_music,
        )
        settings_menu.add.toggle_switch(
            title="Sound effects",
            default=self.sound_manager.playing_sound_effects,
            state_text=("Off", "On"),
            onchange=self.sound_manager.toggle_sound_effects,
        )
        settings_menu.add.range_slider(
            title="Volume",
            default=self.sound_manager.volume*10,
            range_values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            increment=1,
            width=275,
            range_box_single_slider=True,
            onchange=self.sound_manager.adjust_volume,
        )
        settings_menu.add.button("Back", pygame_menu.events.BACK)
        return settings_menu

    def create_info_menu(self):
        """
        Creates the Info submenu to be included in the Main Menu.

        Returns:
            pygame_menu.Menu: The configured Info submenu.
        """
        info_menu = pygame_menu.Menu(
            height=HEIGHT, theme=self.window_theme, title="Info", width=WIDTH
        )
        for item in self.info:
            info_menu.add.label(
                item, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
            info_menu.add.vertical_margin(30)
        info_menu.add.button("Back", pygame_menu.events.BACK)
        return info_menu

    def create_window_theme_menu(self):
        """
        Creates the Window Theme submenu to be included in the Settings
        Menu; selections include Default, Blue, Dark, Green, Orange,
        and Solarized.

        Returns:
            pygame_menu.Menu: The configured Window Theme submenu.
        """
        window_theme_menu = pygame_menu.Menu(
            height=HEIGHT, theme=self.window_theme, 
            title="Window theme", width=WIDTH
        )
        window_theme_menu.add.button(
            "Default", lambda: self.change_window_theme(DEFAULT))
        window_theme_menu.add.button(
            "Blue", lambda: self.change_window_theme(BLUE))
        window_theme_menu.add.button(
            "Dark", lambda: self.change_window_theme(DARK))
        window_theme_menu.add.button(
            "Green", lambda: self.change_window_theme(GREEN))
        window_theme_menu.add.button(
            "Orange", lambda: self.change_window_theme(ORANGE))
        window_theme_menu.add.button(
            "Solarized", lambda: self.change_window_theme(SOLARIZED)
        )
        window_theme_menu.add.button("Back", pygame_menu.events.BACK)
        return window_theme_menu
    
    def create_end_menu(self, score, min, sec):
        """
        Creates the End Menu displaying the user's score, duration of
        gameplay, and high score from the current session; provides
        options to restart the game, return to the Main Menu, or quit.

        Args:
            score (int): The player's score at the end of the game.
            min (int): The minutes part of the game duration.
            sec (int): The seconds part of the game duration.
        """
        self.end_menu = pygame_menu.Menu(
            height=HEIGHT, theme=self.window_theme, 
            title="Game Over", width=WIDTH
        )
        self.end_menu.add.label(f"Score: {score}")
        self.end_menu.add.label(f"Duration: {min}:{sec:02}")
        if self.high_score > 0:
            self.end_menu.add.label(f"High score: {self.high_score}")
        self.end_menu.add.button("Try again", self.restart_game)
        self.end_menu.add.button("Back to main menu", self.return_to_main_menu)
        self.end_menu.add.button("Quit", pygame.quit)
    
    def update_high_score(self, score):
        """
        Updates the high score if new score is higher than current value.
        
        Args:
            score (int): The score to compare against the high score.
        """
        if score > self.high_score:
            self.high_score = score
            
    def start_game(self):
        """Initializes and runs a new Game instance."""
        game = Game(self.screen, self)
        game.play_game()

    def restart_game(self):
        """Disables the End Menu and starts a new game."""
        self.end_menu.disable()
        self.start_game()

    def change_window_theme(self, selected):
        """
        Changes the theme of the game window.
        
        Args:
            selected (pygame_menu.themes.Theme): New theme to apply.
        """
        self.window_theme = selected
        self.create_main_menu()
        self.main_menu.mainloop(self.screen)

    def return_to_main_menu(self):
        """Returns to the Main Menu from the End Menu."""
        self.end_menu.disable()
        self.main_menu.enable()