# config_handler.py

import sys
import toml

class ConfigHandler: 
    """Loads configuration data from a TOML file."""

    def __init__(self, config_file):
        """
        Handles initialization by loading configuration data from file.
        
        Args:
            config_file (str): Path to the TOML configuration file.
        """
        self.config = self.load_config(config_file)
    
    def load_config(self, file):
        """
        Loads the configuration from the given TOML file.
        
        Args:
            file (str): Path to the TOML file.

        Returns:
            dict: Configuration data.
        
        Raises:
            FileNotFoundError: If the TOML file does not exist.
            toml.TomlDecodeError: If the TOML file is malformed.
        """
        try:
            return toml.load(file)
        except toml.TomlDecodeError as e:
            print(f"Configuration file format error: {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            print(f"Configuration file not found: {e}")
            sys.exit(1)
    
    def get(self, section, key=None):
        """
        Retrieves a configuration value.
        
        Args:
            section (str): The section in the configuration.
            key (str): The key within the section.
        
        Returns:
            The configuration value if a key is provided, otherwise the
            full section as a dictionary.
        """
        section_config = self.config.get(section, {})
        return section_config.get(key) if key else section_config