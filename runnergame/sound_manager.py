# sound_manager.py

import pygame

class SoundManager:
    """Manages music and sound effects in the game."""

    def __init__(self, paths_config):
        """
        Initializes the sound manager by loading sounds files.

        Args:
            paths_config (dict): Paths to sound files.
        """
        self.volume = 1
        self.playing_music = True
        self.playing_sound_effects = True
        self.paths_config = paths_config
        self.initialize_sounds()

    def initialize_sounds(self):
        """Loads all sound files."""
        self.jump_sound = pygame.mixer.Sound(
            self.paths_config.get("jump_sound"))
        self.collision_sound = pygame.mixer.Sound(
            self.paths_config.get("collision_sound"))
        pygame.mixer.music.load(
            self.paths_config.get("background_music"))

    def play_music(self):
        """Plays background music continuously when music is enabled."""
        if self.playing_music == True:
            pygame.mixer.music.play(loops=-1)
    
    def stop_music(self):
        """Stops the background music."""
        pygame.mixer.music.stop()

    def update_sound_effect_volume(self):
        """Adjusts the volume of sound effects."""
        volume = self.volume if self.playing_sound_effects else 0
        self.jump_sound.set_volume(volume)
        self.collision_sound.set_volume(volume)

    def play_collision(self):
        """
        Plays the collision sound effect and stops other sounds as the 
        game ends.
        """
        self.jump_sound.stop()
        self.collision_sound.play()
        self.stop_music()

    def toggle_music(self, selected):
        """
        Toggles the background music on or off.
        
        Args:
            selected (bool): True to play music, False to stop.
        """
        self.playing_music = selected
    
    def toggle_sound_effects(self, selected):
        """
        Toggles sound effects on or off.
        
        Args:
            selected (bool): True to enable sound effects, False to stop.
        """
        self.playing_sound_effects = selected
        self.update_sound_effect_volume()
    
    def adjust_volume(self, selected):
        """
        Adjusts the volume of the music and sound effects.
        
        Args:
            selected (int): Volume level, ranging from 0 to 10.
        """
        self.volume = selected/10
        pygame.mixer.music.set_volume(self.volume)
        self.update_sound_effect_volume()