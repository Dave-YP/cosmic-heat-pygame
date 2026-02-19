"""
Game Settings Module for Cosmic Heat

This module provides a centralized settings management system for the game,
handling persistent storage of user preferences and high scores.

Classes:
    GameSettings: Singleton class managing all game configuration.

Module-level instances:
    game_settings: Pre-instantiated GameSettings singleton for global access.

Files created:
    game_settings.json: Stores user preferences (audio, display, difficulty)
    high_scores.json: Stores top 10 player scores

Example usage:
    from settings import game_settings
    
    # Check if music is enabled
    if game_settings.get("music_enabled"):
        play_music()
    
    # Toggle a setting
    game_settings.toggle("sfx_enabled")
    
    # Add a high score
    game_settings.add_high_score(5000, "Player1")
"""

import json
import os
import pygame

SETTINGS_FILE = "game_settings.json"
HIGH_SCORES_FILE = "high_scores.json"

DEFAULT_SETTINGS = {
    "music_enabled": True,
    "sfx_enabled": True,
    "fullscreen": False,
    "music_volume": 0.25,
    "sfx_volume": 0.4,
    "difficulty": "normal"
}

DIFFICULTY_MODIFIERS = {
    "easy": {"enemy_spawn_rate": 180, "damage_multiplier": 0.5, "score_multiplier": 0.75},
    "normal": {"enemy_spawn_rate": 120, "damage_multiplier": 1.0, "score_multiplier": 1.0},
    "hard": {"enemy_spawn_rate": 80, "damage_multiplier": 1.5, "score_multiplier": 1.5}
}


class GameSettings:
    """
    Singleton class for managing game settings and high scores.
    
    This class provides a centralized way to manage all game configuration
    including audio settings, display preferences, difficulty levels, and
    high score tracking. Settings are automatically persisted to JSON files.
    
    The singleton pattern ensures only one instance exists throughout the
    game, providing consistent settings access from any module.
    
    Attributes:
        settings (dict): Current game settings dictionary.
        high_scores (list): List of high score entries, each containing
            'name' and 'score' keys.
    
    Settings Keys:
        music_enabled (bool): Whether background music is enabled.
        sfx_enabled (bool): Whether sound effects are enabled.
        fullscreen (bool): Whether the game runs in fullscreen mode.
        music_volume (float): Background music volume (0.0 to 1.0).
        sfx_volume (float): Sound effects volume (0.0 to 1.0).
        difficulty (str): Game difficulty ('easy', 'normal', or 'hard').
    
    Difficulty Modifiers:
        easy: 50% damage taken, 75% score earned, slower enemy spawns
        normal: 100% damage taken, 100% score earned, standard spawns
        hard: 150% damage taken, 150% score earned, faster enemy spawns
    
    Example:
        >>> from settings import game_settings
        >>> game_settings.get("music_enabled")
        True
        >>> game_settings.toggle("music_enabled")
        False
        >>> game_settings.get_difficulty_modifier("damage_multiplier")
        1.0
    """
    
    _instance = None
    
    def __new__(cls):
        """Create singleton instance if it doesn't exist."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """
        Initialize the settings manager.
        
        Loads existing settings from disk if available, otherwise uses
        defaults. This method is safe to call multiple times due to the
        singleton pattern - subsequent calls are no-ops.
        """
        if self._initialized:
            return
        self._initialized = True
        self.settings = DEFAULT_SETTINGS.copy()
        self.high_scores = []
        self._load_settings()
        self._load_high_scores()
    
    def _load_settings(self):
        """Load settings from JSON file, falling back to defaults on error."""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    loaded = json.load(f)
                    for key in DEFAULT_SETTINGS:
                        if key in loaded:
                            self.settings[key] = loaded[key]
            except (json.JSONDecodeError, IOError):
                self.settings = DEFAULT_SETTINGS.copy()
    
    def _save_settings(self):
        """Persist current settings to JSON file."""
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except IOError:
            pass
    
    def _load_high_scores(self):
        """Load high scores from JSON file."""
        if os.path.exists(HIGH_SCORES_FILE):
            try:
                with open(HIGH_SCORES_FILE, 'r') as f:
                    self.high_scores = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.high_scores = []
    
    def _save_high_scores(self):
        """Persist high scores to JSON file."""
        try:
            with open(HIGH_SCORES_FILE, 'w') as f:
                json.dump(self.high_scores, f, indent=2)
        except IOError:
            pass
    
    def get(self, key):
        """
        Retrieve a setting value.
        
        Args:
            key (str): The setting key to retrieve.
        
        Returns:
            The setting value, or the default value if key doesn't exist.
        
        Example:
            >>> game_settings.get("music_enabled")
            True
        """
        return self.settings.get(key, DEFAULT_SETTINGS.get(key))
    
    def set(self, key, value):
        """
        Set a setting value and persist to disk.
        
        Args:
            key (str): The setting key to set.
            value: The value to assign.
        
        Example:
            >>> game_settings.set("music_volume", 0.5)
        """
        self.settings[key] = value
        self._save_settings()
    
    def toggle(self, key):
        """
        Toggle a boolean setting and persist to disk.
        
        Args:
            key (str): The setting key to toggle. Must be a boolean setting.
        
        Returns:
            bool: The new value after toggling, or None if key is not boolean.
        
        Example:
            >>> game_settings.get("music_enabled")
            True
            >>> game_settings.toggle("music_enabled")
            False
        """
        if key in self.settings and isinstance(self.settings[key], bool):
            self.settings[key] = not self.settings[key]
            self._save_settings()
            return self.settings[key]
        return None
    
    def add_high_score(self, score, name="Player"):
        """
        Add a new high score entry.
        
        The score is inserted in sorted order and the list is trimmed to
        keep only the top 10 scores. Persists immediately to disk.
        
        Args:
            score (int): The score value to add.
            name (str, optional): Player name. Defaults to "Player".
        
        Example:
            >>> game_settings.add_high_score(5000, "Alice")
            >>> game_settings.add_high_score(3000)  # Uses "Player" as name
        """
        entry = {"name": name, "score": score}
        self.high_scores.append(entry)
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]
        self._save_high_scores()
    
    def get_high_scores(self):
        """
        Retrieve the top 10 high scores.
        
        Returns:
            list: List of score entries, each a dict with 'name' and 'score'.
                  Sorted by score in descending order.
        
        Example:
            >>> scores = game_settings.get_high_scores()
            >>> for entry in scores:
            ...     print(f"{entry['name']}: {entry['score']}")
        """
        return self.high_scores[:10]
    
    def get_difficulty_modifier(self, key):
        """
        Get a difficulty-based gameplay modifier.
        
        Args:
            key (str): The modifier to retrieve. Valid keys are:
                - 'enemy_spawn_rate': Frame interval for enemy spawning
                - 'damage_multiplier': Multiplier for damage taken
                - 'score_multiplier': Multiplier for score earned
        
        Returns:
            float: The modifier value for the current difficulty setting.
        
        Example:
            >>> game_settings.set("difficulty", "hard")
            >>> game_settings.get_difficulty_modifier("damage_multiplier")
            1.5
        """
        diff = self.settings.get("difficulty", "normal")
        return DIFFICULTY_MODIFIERS.get(diff, DIFFICULTY_MODIFIERS["normal"]).get(key, 1.0)
    
    def cycle_difficulty(self):
        """
        Cycle to the next difficulty level.
        
        Cycles through: easy -> normal -> hard -> easy
        
        Returns:
            str: The new difficulty setting.
        
        Example:
            >>> game_settings.get("difficulty")
            'normal'
            >>> game_settings.cycle_difficulty()
            'hard'
            >>> game_settings.cycle_difficulty()
            'easy'
        """
        difficulties = ["easy", "normal", "hard"]
        current = self.settings.get("difficulty", "normal")
        idx = difficulties.index(current) if current in difficulties else 1
        next_idx = (idx + 1) % len(difficulties)
        self.settings["difficulty"] = difficulties[next_idx]
        self._save_settings()
        return self.settings["difficulty"]
    
    def apply_audio_settings(self):
        """
        Apply current audio settings to pygame mixer.
        
        Sets the music volume based on music_enabled and music_volume settings.
        Call this after changing audio settings to apply them immediately.
        
        Example:
            >>> game_settings.toggle("music_enabled")
            >>> game_settings.apply_audio_settings()
        """
        if self.settings["music_enabled"]:
            pygame.mixer.music.set_volume(self.settings["music_volume"])
        else:
            pygame.mixer.music.set_volume(0)
    
    def should_play_sfx(self):
        """
        Check if sound effects should be played.
        
        Returns:
            bool: True if sfx_enabled setting is True.
        
        Example:
            >>> if game_settings.should_play_sfx():
            ...     explosion_sound.play()
        """
        return self.settings["sfx_enabled"]
    
    def get_sfx_volume(self):
        """
        Get the current sound effects volume.
        
        Returns:
            float: The sfx_volume if sfx is enabled, otherwise 0.
        
        Example:
            >>> sound = pygame.mixer.Sound("effect.wav")
            >>> sound.set_volume(game_settings.get_sfx_volume())
        """
        if self.settings["sfx_enabled"]:
            return self.settings["sfx_volume"]
        return 0
    
    def play_sound(self, sound):
        """
        Play a sound effect if sfx is enabled.
        
        Convenience method that checks sfx_enabled before playing.
        Also updates the sound's volume to current settings.
        
        Args:
            sound (pygame.mixer.Sound): The sound to play.
        
        Example:
            >>> explosion = pygame.mixer.Sound("explosion.wav")
            >>> game_settings.play_sound(explosion)
        """
        if self.settings["sfx_enabled"]:
            sound.set_volume(self.settings["sfx_volume"])
            sound.play()


game_settings = GameSettings()
