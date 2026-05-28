"""
Display manager for handling logical resolution scaling with dynamic window resizing.

All game rendering happens on a base surface at the logical resolution,
which is then scaled to fit the actual window size while maintaining aspect ratio.
"""

from typing import Optional, Tuple

import pygame

from classes.constants import (
    LOGICAL_WIDTH, LOGICAL_HEIGHT,
    MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT,
    MAX_WINDOW_SCALE, DEFAULT_WINDOW_SCALE
)


class DisplayManager:
    """Manages the resizable window and logical resolution scaling."""

    def __init__(self):
        self.logical_width = LOGICAL_WIDTH
        self.logical_height = LOGICAL_HEIGHT
        self.logical_aspect_ratio = LOGICAL_WIDTH / LOGICAL_HEIGHT

        # Detect monitor size and calculate initial window size
        display_info = pygame.display.Info()
        self.monitor_width = display_info.current_w
        self.monitor_height = display_info.current_h

        # Calculate initial window size (percentage of monitor, maintaining aspect ratio)
        initial_width, initial_height = self._calculate_initial_size()
        self.window_width = initial_width
        self.window_height = initial_height

        self._fullscreen = False
        self._windowed_size = (initial_width, initial_height)

        # Create resizable window
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height),
            pygame.RESIZABLE
        )

        # Create the logical surface where all game rendering happens
        self.game_surface = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))

        # Cached scaled surface (only recreate on resize)
        self._cached_scaled_surface: Optional[pygame.Surface] = None
        self._needs_rescale = True

        # Scaling state
        self._update_scaling()

    def _calculate_initial_size(self) -> Tuple[int, int]:
        """Calculate initial window size based on monitor dimensions."""
        # Target size is a percentage of the monitor
        target_width = int(self.monitor_width * DEFAULT_WINDOW_SCALE)
        target_height = int(self.monitor_height * DEFAULT_WINDOW_SCALE)

        # Adjust to maintain logical aspect ratio
        if target_width / target_height > self.logical_aspect_ratio:
            # Too wide, constrain by height
            width = int(target_height * self.logical_aspect_ratio)
            height = target_height
        else:
            # Too tall, constrain by width
            width = target_width
            height = int(target_width / self.logical_aspect_ratio)

        # Ensure minimum size
        width = max(width, MIN_WINDOW_WIDTH)
        height = max(height, MIN_WINDOW_HEIGHT)

        return width, height

    def _update_scaling(self):
        """Calculate scaling factors and letterbox offsets."""
        window_aspect = self.window_width / self.window_height

        if window_aspect > self.logical_aspect_ratio:
            # Window is wider than logical - letterbox on sides
            self.scaled_height = self.window_height
            self.scaled_width = int(self.window_height * self.logical_aspect_ratio)
        else:
            # Window is taller than logical - letterbox on top/bottom
            self.scaled_width = self.window_width
            self.scaled_height = int(self.window_width / self.logical_aspect_ratio)

        # Calculate letterbox offsets to center the game surface
        self.offset_x = (self.window_width - self.scaled_width) // 2
        self.offset_y = (self.window_height - self.scaled_height) // 2

        # Scale factors for converting window coords to logical coords
        self.scale_x = self.logical_width / self.scaled_width
        self.scale_y = self.logical_height / self.scaled_height

        # Mark for rescale
        self._needs_rescale = True
        self._cached_scaled_surface = None

    def handle_resize(self, new_width: int, new_height: int):
        """Handle window resize event."""
        # Enforce minimum size
        new_width = max(new_width, MIN_WINDOW_WIDTH)
        new_height = max(new_height, MIN_WINDOW_HEIGHT)

        # Enforce maximum size (monitor bounds)
        max_width = int(self.monitor_width * MAX_WINDOW_SCALE)
        max_height = int(self.monitor_height * MAX_WINDOW_SCALE)
        new_width = min(new_width, max_width)
        new_height = min(new_height, max_height)

        # Only update if size actually changed
        if new_width == self.window_width and new_height == self.window_height:
            return

        self.window_width = new_width
        self.window_height = new_height

        if not self._fullscreen:
            self._windowed_size = (new_width, new_height)

        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height),
            pygame.RESIZABLE if not self._fullscreen else pygame.FULLSCREEN
        )
        self._update_scaling()

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode (F11)."""
        self._fullscreen = not self._fullscreen

        if self._fullscreen:
            # Store current windowed size before going fullscreen
            self._windowed_size = (self.window_width, self.window_height)

            # Go fullscreen at monitor resolution
            self.window_width = self.monitor_width
            self.window_height = self.monitor_height
            self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height),
                pygame.FULLSCREEN
            )
        else:
            # Restore windowed size
            self.window_width, self.window_height = self._windowed_size
            self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height),
                pygame.RESIZABLE
            )

        self._update_scaling()

    def is_fullscreen(self) -> bool:
        """Check if currently in fullscreen mode."""
        return self._fullscreen

    def window_to_logical(self, window_x: int, window_y: int) -> Tuple[int, int]:
        """Convert window coordinates to logical game coordinates."""
        logical_x = int((window_x - self.offset_x) * self.scale_x)
        logical_y = int((window_y - self.offset_y) * self.scale_y)

        # Clamp to logical bounds
        logical_x = max(0, min(logical_x, self.logical_width - 1))
        logical_y = max(0, min(logical_y, self.logical_height - 1))

        return logical_x, logical_y

    def is_point_in_game_area(self, window_x: int, window_y: int) -> bool:
        """Check if a window coordinate is within the game rendering area."""
        return (
            self.offset_x <= window_x < self.offset_x + self.scaled_width and
            self.offset_y <= window_y < self.offset_y + self.scaled_height
        )

    def get_game_surface(self) -> pygame.Surface:
        """Get the logical game surface for rendering."""
        return self.game_surface

    def present(self):
        """Scale and blit the game surface to the window, then flip."""
        # Clear screen with black (for letterboxing)
        self.screen.fill((0, 0, 0))

        # Only rescale if needed (window size changed)
        if self._needs_rescale or self._cached_scaled_surface is None:
            self._cached_scaled_surface = pygame.transform.smoothscale(
                self.game_surface,
                (self.scaled_width, self.scaled_height)
            )
            self._needs_rescale = False
        else:
            # Update the cached surface with new game content
            pygame.transform.smoothscale(
                self.game_surface,
                (self.scaled_width, self.scaled_height),
                self._cached_scaled_surface
            )

        # Blit centered
        self.screen.blit(self._cached_scaled_surface, (self.offset_x, self.offset_y))
        pygame.display.flip()

    def get_logical_size(self) -> Tuple[int, int]:
        """Get the logical resolution."""
        return self.logical_width, self.logical_height

    def get_window_size(self) -> Tuple[int, int]:
        """Get the current window size."""
        return self.window_width, self.window_height

    def get_scale_factor(self) -> float:
        """Get the current scale factor (useful for UI sizing decisions)."""
        return self.scaled_width / self.logical_width


# Global display manager instance
_display_manager: Optional[DisplayManager] = None


def init_display() -> DisplayManager:
    """Initialize and return the global display manager."""
    global _display_manager
    _display_manager = DisplayManager()
    return _display_manager


def get_display() -> DisplayManager:
    """Get the global display manager instance."""
    if _display_manager is None:
        raise RuntimeError("Display manager not initialized. Call init_display() first.")
    return _display_manager