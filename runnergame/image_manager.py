# image_manager.py

import pygame
import sys
from pathlib import Path
from constants import WIDTH, GROUND_DIM, PLAYER_SCALE, OBSTACLE_SCALE, GLOW_SCALE

class ImageManager:
    """Manages loading, scaling, and storing images used in the game."""

    def __init__(self, paths_config):
        """
        Initializes the image manager by loading and configuring images.

        Args:
            paths_config (dict): Paths to image directories.
        """
        self.paths_config = paths_config
        self.initialize_images()
        self.len_bg = len(self.bg_imgs)
        self.len_obs = len(self.obs_imgs)
    
    def initialize_images(self):
        """
        Loads and scales all images.
        
        Raises:
            FileNotFoundError: If an image file could not be loaded.
        """
        try:
            self.run_imgs = self.load_images_from_directory(
                self.paths_config.get("run"), PLAYER_SCALE, True)
            self.jump_imgs = self.load_images_from_directory(
                self.paths_config.get("jump"), PLAYER_SCALE, True)
            self.obs_imgs = self.load_images_from_directory(
                self.paths_config.get("obstacle"), OBSTACLE_SCALE, True)
            self.ground_img = self.load_image(
                self.paths_config.get("ground"), (GROUND_DIM, GROUND_DIM))
            self.bg_imgs = self.load_images_from_directory(
                self.paths_config.get("background"))  
            self.scale_background_images()
            self.initialize_glow_img()
        except FileNotFoundError as e:
            print(f"Error loading image file: {e}")
            sys.exit(1)

    def scale_background_images(self):
        """Scales background images based on screen size."""
        bg_scale = (self.bg_imgs[0].get_width() / self.bg_imgs[0].get_height())
        self.bg_imgs = [
            pygame.transform.scale(layer, (WIDTH, int(WIDTH * bg_scale))) 
            for layer in self.bg_imgs]
        self.bg_width = [layer.get_width() for layer in self.bg_imgs]

    def initialize_glow_img(self):
        """Loads and scales glow image."""
        glow_scale = (
            int(GLOW_SCALE[0] * self.obs_imgs[10].get_width()), 
            int(GLOW_SCALE[1] * self.obs_imgs[10].get_width()))
        self.glow_img = self.load_image(self.paths_config.get("glow"),
                                        glow_scale)
        self.glow_img.set_alpha(65)
    
    def load_images_from_directory(self, directory, scale=None, factor=False):     
        """
        Loads all images from the specified directory.

        Args:
            directory (str): Path to directory containing images to load.
            scale (tuple[float, float], optional): Scale factors in the
                format of (x-scale, y-scale).
            factor (bool, optional): Indicates whether to scale by a 
                factor or to specific dimensions.

        Returns:
            list[pygame.Surface]: List of loaded and scaled images.
        """
        images = []
        for file in Path(directory).iterdir():
            image = self.load_image(str(file), scale, factor)
            images.append(image)
        return images
    
    def load_image(self, path, scale=None, factor=False):
        """
        Loads a single image.

        Args:
            path (str): Path to the image file.
            scale (tuple[float, float], optional): Scale factors in the
                format of (x-scale, y-scale). Defaults to None.
            factor (bool, optional): Indicates whether to scale by a 
                factor or by specific dimensions. Defaults to False.

        Returns:
            pygame.Surface: The loaded and scaled image.

        Raises:
            FileNotFoundError: If the image file cannot be loaded.
        """
        try:
            image = pygame.image.load(path).convert_alpha()
            return (self.scale_image(image, scale if not factor else (
                int(scale[0] * image.get_width()), 
                int(scale[1] * image.get_height()))) 
                if scale else image)
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            raise FileNotFoundError
    
    def scale_image(self, image, scale):
        """
        Scales given image to specific dimensions.
        
        Args:
            image (pygame.Surface): The image to be scaled.
            scale (tuple[float, float]): Scale factors in the format
                of (x-scale, y-scale).

        Returns:
            pygame.Surface: The scaled image.
        """
        return pygame.transform.scale(image, scale)