import os
import yaml
from typing import Optional, Dict, Any, List
import toml

class AlacrittyClient:
    def __init__(self):
        self.config_path: Optional[str] = None
        self._initialized: bool = False

    def initialize(self, config_path: str):
        """Initialize the Alacritty client with the config file path."""
        self.config_path = config_path
        self._initialized = True

    def is_initialized(self) -> bool:
        """Check if the client has been initialized with a config path."""
        return self._initialized


    def load_config(self) -> Dict[str, Any]:
        if not self.config_path or not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Alacritty config file not found: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            if self.config_path.endswith(".toml"):
                return toml.load(f)
            return yaml.safe_load(f)

    def save_config(self, config: Dict[str, Any]):
        if not self.config_path:
            raise ValueError("Config path not set.")
        with open(self.config_path, "w", encoding="utf-8") as f:
            if self.config_path.endswith(".toml"):
                toml.dump(config, f)
            else:
                yaml.safe_dump(config, f, sort_keys=False)

    def get_section(self, section: str) -> Any:
        """Get a specific section (e.g., 'font', 'colors') from the config."""
        config = self.load_config()
        return config.get(section, {})

    def set_section(self, section: str, value: Any):
        """Set a specific section in the config and save."""
        config = self.load_config()
        config[section] = value
        self.save_config(config)

    def get_keybindings(self) -> List[Dict[str, Any]]:
        """Get the keybindings section from the config."""
        config = self.load_config()
        return config.get("key_bindings", [])

    def set_keybindings(self, keybindings: List[Dict[str, Any]]):
        """Set the keybindings section in the config and save."""
        config = self.load_config()
        config["key_bindings"] = keybindings
        self.save_config(config)

    def get_theme(self) -> Dict[str, Any]:
        """Get the colors (theme) section from the config."""
        return self.get_section("colors")

    def set_theme(self, theme: Dict[str, Any]):
        """Set the colors (theme) section in the config and save."""
        self.set_section("colors", theme)

    def get_font(self) -> Dict[str, Any]:
        """Get the font section from the config."""
        return self.get_section("font")

    def set_font(self, font: Dict[str, Any]):
        """Set the font section in the config and save."""
        self.set_section("font", font)

    def get_window(self) -> Dict[str, Any]:
        """Get the window section from the config."""
        return self.get_section("window")

    def set_window(self, window: Dict[str, Any]):
        """Set the window section in the config and save."""
        self.set_section("window", window)

    def get_performance(self) -> Dict[str, Any]:
        """Get the performance section from the config."""
        return self.get_section("performance")

    def set_performance(self, performance: Dict[str, Any]):
        """Set the performance section in the config and save."""
        self.set_section("performance", performance)

    def export_config(self, export_path: str):
        """Export the current config to another file."""
        config = self.load_config()
        with open(export_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(config, f, sort_keys=False)

# Global instance
alacritty_client = AlacrittyClient()