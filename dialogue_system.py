"""
Capitalism simulator! - Dialogue System
=============================
This module manages character dialogue in the game, providing a flexible
framework for conversations with NPCs (Non-Player Characters).

Educational Concepts Covered:
- Data structures (dictionaries, lists)
- Text rendering and display
- User interface design
- State management
- Event handling and input processing
- Modular code organization

This system can be easily extended to support:
- Multiple characters with unique dialogue
- Branching conversations
- Character mood/emotion responses
- Quest-related dialogue
- Dynamic dialogue based on game state
"""

import os
import subprocess
import sys

import pygame
from settings import *
from timer import Timer
import game_settings

# Try to import AI dialogue manager, fall back gracefully if it fails
try:
    from ai_dialogue_manager import AIDialogueManager

    AI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ AI Dialogue Manager not available: {e}")
    AI_AVAILABLE = False


class DialogueSystem:
    """
    Manages displaying NPC dialogue in a text box on screen, with support for
    AI-generated dynamic content.
    """

    def __init__(self):
        """Initialize the dialogue system and its components."""
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font("font/LycheeSoda.ttf", 30)
        self.active = False
        self.current_dialogue = []
        self.dialogue_index = 0
        self.on_finish_callback = None
        self.choice_mode = False
        self.choice_buttons = []
        self.character_id = None

        # AI Dialogue Manager
        self.ai_enabled = game_settings.get("enable_ai_dialogue", True) and AI_AVAILABLE
        self.ai_manager = None
        if self.ai_enabled:
            try:
                self.ai_manager = AIDialogueManager()
            except Exception as e:
                print(f"⚠️ Failed to initialize AI manager: {e}")
                self.ai_enabled = False

        # Dialogue box setup
        self.box_height = 180  # Increased height for multiple lines
        self.text_box_rect = pygame.Rect(
            (SCREEN_WIDTH - 1200) // 2,
            SCREEN_HEIGHT - self.box_height - 30,
            1200,
            self.box_height,
        )

    def start_dialogue(self, character_id: str, player_context: dict = None, dialogue_lines: list = None, on_finish=None):
        """Begin a dialogue session with an NPC."""
        self.active = True
        self.dialogue_index = 0
        self.on_finish_callback = on_finish
        self.character_id = character_id
        self.choice_mode = False
        self.choice_buttons = []
        # @STUDENT-EDIT-Day4-1: Insert print() statements here to debug which dialogue branch is executing

        if dialogue_lines:
            # If explicit dialogue lines are passed (e.g. from custom NPCs), use them
            self.current_dialogue = []
            for paragraph in dialogue_lines:
                pages = self._wrap_text(paragraph, self.text_box_rect.width - 40)
                self.current_dialogue.extend(pages)
        elif self.ai_enabled and self.ai_manager and player_context:
            # Generate dialogue using AI
            dialogue_line = self.ai_manager.generate_npc_dialogue(
                character_name=player_context.get("npc_name", "NPC"),
                character_role=player_context.get("npc_role", "character"),
                player_context=player_context.get("situation", "meeting you"),
                emotion=player_context.get("emotion", "neutral"),
            )
            self.current_dialogue = self._wrap_text(
                dialogue_line, self.text_box_rect.width - 40
            )
        else:
            # Use fallback dialogue
            fallback_dialogue = self._get_static_fallback(character_id)
            self.current_dialogue = self._wrap_text(
                fallback_dialogue, self.text_box_rect.width - 40
            )

        if not self.current_dialogue:
            self.end_dialogue()

    def _get_static_fallback(self, character_id: str) -> str:
        """Provides a simple, static fallback dialogue for NPCs."""
        # @STUDENT-EDIT-Day5-3: Try loading custom dialogue from a text file here instead of hardcoding it
        # @STUDENT-EDIT-Day3-1: Add a new greeting string to this dialogue dictionary
        fallbacks = {
            "trader": "Welcome, friend! I have many fine goods for a hardworking capitalist like you. Let's see what you need."
        }
        # @STUDENT-EDIT-Day3-2: Create a branching dialogue option using nested lists/dictionaries
        # @STUDENT-EDIT-Day3-3: Add a dialogue choice that ends the conversation early (self.active = False)
        return fallbacks.get(character_id, "Hello there! Nice day for farming.")

    def _wrap_text(self, text, max_width):
        """Wraps text to fit within a given width and returns lines that fit in the dialogue box."""
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                if current_line.strip():  # Only add non-empty lines
                    lines.append(current_line.strip())
                current_line = word + " "

        if current_line.strip():  # Add the last line if it's not empty
            lines.append(current_line.strip())

        # Group lines into pages that fit in the dialogue box
        lines_per_page = 4  # Number of lines that fit in the larger dialogue box
        pages = []
        for i in range(0, len(lines), lines_per_page):
            page_lines = lines[i : i + lines_per_page]
            pages.append(page_lines)

        # Ensure we always have at least one page
        return pages if pages else [["No dialogue available."]]

    def _build_choice_buttons(self):
        """Create on-screen buttons for the poker choice prompt."""
        button_width = 150
        button_height = 44
        button_y = self.text_box_rect.bottom - 72
        x_center = self.text_box_rect.centerx
        x_left = x_center - button_width - 20
        x_right = x_center + 20

        return [
            {"rect": pygame.Rect(x_left, button_y, button_width, button_height), "label": "Play Poker", "action": "play_poker"},
            {"rect": pygame.Rect(x_right, button_y, button_width, button_height), "label": "Have a bad time", "action": "end_dialogue_sans"},
        ]

    def _show_choice_buttons(self):
        """Reveal the poker choice buttons after the intro dialogue finishes."""
        if self.character_id == "Poker person":
            self.choice_buttons = self._build_choice_buttons()
            self.choice_mode = True

    def _handle_choice_action(self, action):
        """Respond to a poker-choice button press."""
        if action == "play_poker":
            self.active = False
            self.choice_mode = False
            self.choice_buttons = []
            poker_script = os.path.join(os.path.dirname(__file__), "poker.py")
            if os.path.exists(poker_script):
                subprocess.Popen([sys.executable, poker_script], cwd=os.path.dirname(__file__))
            else:
                print("Poker script not found.")
            pygame.quit()
            raise SystemExit(0)
        else:
            self.end_dialogue()

    def next_line(self):
        """Advance to the next page of dialogue or end the session."""
        if self.choice_mode:
            self.end_dialogue()
            return

        if self.dialogue_index >= len(self.current_dialogue) - 1:
            if self.character_id == "Poker person":
                self._show_choice_buttons()
            else:
                self.end_dialogue()
        else:
            self.dialogue_index += 1

    def end_dialogue(self):
        """End the current dialogue session and trigger the callback."""
        self.active = False
        self.current_dialogue = []
        self.dialogue_index = 0
        self.choice_mode = False
        self.choice_buttons = []
        if self.on_finish_callback:
            self.on_finish_callback()
            self.on_finish_callback = None

    def input(self, events):
        """Handle player input for advancing dialogue using events to prevent conflicts."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.choice_mode and event.button == 1:
                for button in self.choice_buttons:
                    if button["rect"].collidepoint(event.pos):
                        self._handle_choice_action(button["action"])
                        return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # @STUDENT-EDIT-Day4-2: Link a dialogue choice to a sprite action here if implementing branching
                    if self.choice_mode:
                        self._handle_choice_action("end_dialogue")
                    else:
                        self.next_line()
                    return True  # Indicate that we consumed the input
        return False  # No input consumed

    def draw(self):
        """Draw the dialogue box and text to the screen."""
        if self.active:
            # Draw the dialogue box
            pygame.draw.rect(self.display_surface, "White", self.text_box_rect, 0, 10)
            pygame.draw.rect(self.display_surface, "Black", self.text_box_rect, 4, 10)

            # Draw the current page of dialogue (multiple lines)
            if self.dialogue_index < len(self.current_dialogue):
                current_page = self.current_dialogue[self.dialogue_index]
                line_height = 35
                start_y = self.text_box_rect.y + 20

                for i, line in enumerate(current_page):
                    if line.strip():  # Only render non-empty lines
                        line_surface = self.font.render(line, True, "Black")
                        self.display_surface.blit(
                            line_surface,
                            (self.text_box_rect.x + 20, start_y + i * line_height),
                        )

            if self.choice_mode:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.choice_buttons:
                    hovered = button["rect"].collidepoint(mouse_pos)
                    color = (80, 140, 220) if hovered else (60, 90, 160)
                    pygame.draw.rect(self.display_surface, color, button["rect"], border_radius=8)
                    pygame.draw.rect(self.display_surface, "White", button["rect"], 2, border_radius=8)
                    label_surface = self.font.render(button["label"], True, "White")
                    label_rect = label_surface.get_rect(center=button["rect"].center)
                    self.display_surface.blit(label_surface, label_rect)

                prompt_text = "Choose an option..."
            elif self.dialogue_index < len(self.current_dialogue) - 1:
                prompt_text = "Press ENTER to continue..."
            else:
                prompt_text = "Press ENTER to finish..."

            prompt_surface = self.font.render(prompt_text, True, "darkgray")
            self.display_surface.blit(
                prompt_surface,
                (
                    self.text_box_rect.right - prompt_surface.get_width() - 20,
                    self.text_box_rect.bottom - prompt_surface.get_height() - 10,
                ),
            )

    def update(self, events=None):
        """Update the dialogue system, handling input and drawing."""
        if self.active:
            if events:
                self.input(events)
            self.draw()
