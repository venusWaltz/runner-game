# entities.py

import pygame
import random
from constants import WIDTH, FLOOR, JUMP_SPEED

class Player(pygame.sprite.Sprite):
    """Manages the player sprite, extending the Pygame sprite class."""

    def __init__(self, menu):
        """
        Initializes player with the first image and sets its position.

        Args:
            menu (Menu): The central game menu system.
        """
        super(Player, self).__init__()
        self.menu = menu
        self.surf = menu.image_manager.run_imgs[0]
        self.rect = self.surf.get_rect()
        self.rect.left = int(WIDTH/7)
        self.rect.bottom = FLOOR
        self.run_imgs = menu.image_manager.run_imgs
        self.float_frames = 6
        self.wait = 0

    def animate(self, num, img):
        """
        Animates walk or jump cycle by moving to next image in sequence.

        Args:
            num (int): The index of the next image to swap to.
            img (list[pygame.Surface]): Images in the animation sequence
                to iterate through.
        """
        bottom = self.rect.bottom
        if img:
            self.surf = img[num]
        self.rect = self.surf.get_rect()
        self.rect.left = int(WIDTH/7)
        self.rect.bottom = bottom

    def update(self, v, m, is_jumping):
        """
        Handles the jump animation of the player sprite.

        Args:
            v (float): Current velocity of the player.
            m (float): Mass of the player.
            is_jumping (boolean): Indicates whether player is jumping.
    
        Returns:
            tuple[float, float, bool]: Updated input paramters.
        """
        if is_jumping == True:
            # Calculate jump force using the formula: F = 1/2 * m * v^2.
            F = (1 / 2) * m * (v**2)

            # Update player position using calculated force.
            self.rect.bottom -= F
            
            # Decrease velocity over time to simulate gravity.
            v -= 0.5

            # Handle upward movement animation.
            if v > 0:
                self.animate(0, self.menu.image_manager.jump_imgs)

            # Handle downward movement animation.
            if v < 0:
                # Invert mass to simulate downward arc of jump.
                m = -1
                self.wait += 1
                # Pause animation for a few frames at the top of the jump arc.
                if self.wait > self.float_frames:
                    self.animate(1, self.menu.image_manager.jump_imgs)

            # Reset jump parameters when the player reaches the ground.
            if v <= -JUMP_SPEED:
                is_jumping = False
                self.rect.bottom = FLOOR
                v = JUMP_SPEED
                m = 1
                self.wait = 0

        return v, m, is_jumping


class Obstacle(pygame.sprite.Sprite):
    """Manages obstacle sprites, extending the Pygame Sprite class."""

    def __init__(self, menu):
        """
        Initializes obstacle with the first image and sets its position.

        Args:
            menu (Menu): The central game menu system.
        """
        super(Obstacle, self).__init__()
        self.menu = menu
        self.len_obs = menu.image_manager.len_obs

        self.frame = random.randint(0, self.len_obs - 1)
        self.num_frames = 4
        self.max_frames = (self.len_obs - 1) * self.num_frames

        self.surf = menu.image_manager.obs_imgs[self.frame]
        self.glow_surf = menu.image_manager.glow_img
        self.rect = self.surf.get_rect(center=(
            WIDTH + 20, 
            FLOOR - int(1.5 * self.menu.image_manager.obs_imgs
                        [int(self.len_obs/2)].get_height())))
        self.glow_rect = self.glow_surf.get_rect(center=self.rect.center)

    def update(self, speed):
        """
        Handles the animation and movement of the obstacle sprite.

        Args:
            speed (float): The speed at which the obstacle should move.
        """
        self.animate(self.rect.center)
        self.update_position(speed)
        self.frame += 1

        # Remove the obstacle when it moves off screen.
        if self.rect.right < 0:
            self.kill()
    
    def animate(self, center):
        """
        Updates the next frame to be animated.

        Args:
            center (tuple): The current position of the obstacle.
            frame (int): The specific frame number to display next.
        """
        if self.frame % self.num_frames == 0:
            self.surf = self.menu.image_manager.obs_imgs[
                int(self.frame / self.num_frames) % self.len_obs]
            self.rect = self.surf.get_rect(center=center)
            self.frame = self.frame % self.max_frames

    def update_position(self, speed):
        """
        Updates the positions of the glow and obstacle sprites.

        Args:
            speed (float): The speed at which the obstacle should move.
        """
        self.glow_rect.center = self.rect.center
        self.rect.move_ip(-speed, 0)
        self.glow_rect.move_ip(-speed, 0)