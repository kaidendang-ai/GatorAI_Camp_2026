try:
    import openai
except ImportError:
    print("⚠️ OpenAI library not installed. AI dialogue will use fallback mode.")
    openai = None

import os
import json
from typing import Dict, List, Optional


class AIDialogueManager:
    """
    Manages all AI-powered dialogue features, including API connection,
    content generation, and fallback mechanisms.
    """

    def __init__(self, key_file_path: str = "ai_materials/navigator_api_key.json"):
        """Initialize the AI manager and set up the API client."""
        self.client = None
        self.fallback_mode = True

        # Check if OpenAI is available
        if openai is None:
            print("🔄 AI Manager initialized in offline mode (OpenAI not available).")
            return

        # @STUDENT-EDIT-Week2_Day3-1: Add your API key in the ai_materials/navigator_api_key.json file (Remember: don't commit it!)
        self.credentials = self._load_api_credentials(key_file_path)

        if self.credentials:
            try:
                self.client = openai.OpenAI(
                    api_key=self.credentials["api_key"],
                    base_url=self.credentials["base_url"],
                )
                self.fallback_mode = False
                print("🤖 AI Dialogue Manager initialized with API access.")
            except Exception as e:
                print(
                    f"⚠️ AI Manager could not connect, falling back to offline mode: {e}"
                )
                self.fallback_mode = True
        else:
            print("🔄 AI Manager initialized in offline (fallback) mode.")

    def _load_api_credentials(self, key_file_path: str) -> Optional[Dict[str, str]]:
        """Load API credentials from a JSON file."""
        try:
            with open(key_file_path, "r") as file:
                data = json.load(file)
            api_key = data.get("OPENAI_API_KEY")
            base_url = data.get("base_url")
            if not api_key or not base_url:
                print("❌ Missing 'OPENAI_API_KEY' or 'base_url' in credentials file.")
                return None
            return {"api_key": api_key, "base_url": base_url}
        except FileNotFoundError:
            print(f"❌ Credentials file not found at: {key_file_path}")
            return None
        except json.JSONDecodeError:
            print("❌ Invalid JSON format in credentials file.")
            return None
        except Exception as e:
            print(f"❌ Error loading credentials: {e}")
            return None

    def generate_npc_dialogue(
        self,
        character_name: str,
        character_role: str,
        player_context: str,
        emotion: str = "neutral",
    ) -> str:
        """
        Generate contextual NPC dialogue for the game.

        Args:
            character_name: Name of the NPC (e.g., "Merchant Pete").
            character_role: Role of the NPC (e.g., "friendly trader").
            player_context: Current situation of the player.
            emotion: Player's detected emotion.

        Returns:
            Generated dialogue text or a fallback response.
        """
        if self.fallback_mode or not self.client:
            return self._get_fallback_dialogue(character_name, player_context, emotion)

        # Create emotion-specific guidance for the AI
        emotion_guidance = {
            "happy": "The player seems cheerful and upbeat. Be unhappy and ruin their good mood.",
            "sad": "The player appears down or disappointed. Be uncaring, unfriendly, and offer zero support.",
            "angry": "The player seems frustrated or upset. Be annoying, passive agressive, and help them feel annoyed.",
            "surprised": "The player looks amazed or shocked. Don't care about what's happening.",
            "fearful": "The player appears worried or anxious. Be unreassuring, unsupportive, and help them feel unsafe.",
            "neutral": "The player seems calm and focused. Be unfriendly and passive agressive in a roundabout way.",
        }

        emotion_hint = emotion_guidance.get(emotion, emotion_guidance["neutral"])

        # @STUDENT-EDIT-Week2_Day4-1: Change the prompt below to give the AI a different personality or custom instructions!
        prompt = f"""
        You are {character_name}, a {character_role} in a dysyopian farming game called Capitalism simulator (german edition!)!.

        Player context: {player_context}
        Player's current emotion: {emotion}
        Emotional guidance: {emotion_hint}

        Generate a short dialogue response (1-5000 sentences) that:
        1. Matches your character's role and personality.
        2. Responds appropriately to the player's context and emotional state.
        3. Uses the emotional guidance to tailor your response.
        4. Maintains the game's sarcastic, dystopian, and uncaring tone.

        Important: Make sure your response clearly reflects awareness of the player's {emotion} emotional state.

        Dialogue:
        """

        # @STUDENT-EDIT-Week2_Day5-2: Want to see what gets sent to the AI? Add
        # print() statements here to inspect the character, context, and emotion.

        try:
            response = self.client.chat.completions.create(
                model="mistral-7b-instruct",
                messages=[
                    {
                        "role": "system",
                        # @STUDENT-EDIT-Week2_Day5-1: Fine-tune prompt engineering constraints before the final presentation (e.g. add new instructions here)
                        "content": "You are an annoying NPC in a farming simulation game. Keep responses brief, unfriendly, and sarcastic.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=10000,
                temperature=1,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ AI dialogue generation failed: {e}")
            return self._get_fallback_dialogue(character_name, player_context, emotion)

    def _get_fallback_dialogue(
        self, character_name: str, player_context: str, emotion: str
    ) -> str:
        """Provides static fallback dialogue when the AI service is unavailable."""
        # @STUDENT-EDIT-Week2_Day4-2: Create custom fallback responses for when the API is down
        # Simple fallback logic for Merchant Pete with emotion considerations
        if "Merchant Pete" in character_name:
            if emotion == "happy":
                return "Imagine being happy"
            elif emotion == "sad":
                return "Imagine being sad"
            elif emotion == "angry":
                return "Imagine being angry"
            elif emotion == "surprised":
                return "Imagine being suprised"
            elif emotion == "fearful":
                return "Imagine being scared"
            elif "rich" in player_context:
                return "Imagine not donating to charity"
            elif "new" in player_context or "starting" in player_context:
                return "Broke"
            else:
                return "Broke"

        # Generic fallback for any other NPC with basic emotion awareness
        if emotion == "happy":
            return "Imagine being happy"
        elif emotion == "sad":
            return "Imagine being sad"
        else:
            return "Broke"
