#main.py

import pygame
import constants as constants
from menu import Menu
from image_manager import ImageManager
from sound_manager import SoundManager
from config_handler import ConfigHandler

def main():
    """
    The main entry point of the runner game. Initializes the
    environment and displays the main menu.
    """
    # Initialize Pygame modules.
    pygame.mixer.init()
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(constants.WINDOW_SIZE)
    pygame.display.set_caption(constants.TITLE)

    # Set up the main game screen.
    config_handler = ConfigHandler("config.toml")
    paths_config = config_handler.get("paths")
    
    # Initialize the sound and image managers.
    sound_manager = SoundManager(paths_config)
    image_manager = ImageManager(paths_config)

    # Create and display the main menu.
    menu = Menu(screen, sound_manager, image_manager, 
                config_handler.get("info"))
    menu.create_main_menu()
    menu.main_menu.mainloop(screen)

if __name__ == "__main__":
    main()