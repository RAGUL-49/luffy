"""
Perplexity Service - Integration with Perplexity AI API
"""
import requests
import json
from config.settings import PERPLEXITY_CONFIG, MODEL_SETTINGS
from utils.logger import setup_logger

logger = setup_logger()


def get_system_prompt(language='English'):
    """Generate system prompt for the specified language"""
    return f"""You are an AI music generator for the project "Beatify".

Task: Generate a music description inspired by the user's word in {language}.

Output Format - MUST be valid JSON only:
{{
  "track": {{
    "title": "Generated track title in {language}",
    "language": "{language}",
    "genre": "Electronic/Pop/Rock/etc",
    "mood": "energetic/happy/sad/relaxed/emotional",
    "style": "Detailed music style description with instruments",
    "lyrics": "Creative lyrics in {language} or null",
    "duration": "1-2 minutes",
    "audio_url": "placeholder"
  }},
  "metadata": {{
    "keyword": "USER_WORD",
    "timestamp": "ISO 8601 timestamp",
    "model": "perplexity"
  }}
}}

Rules:
- Output ONLY JSON, no explanations
- Generate content in {language}
- Make lyrics catchy and relevant in {language}
- Choose genre/mood based on word meaning
- Be creative and unique"""


class PerplexityService:
    """Service for interacting with Perplexity AI API"""

    VALID_MODELS = [
        "sonar", 
        "sonar-pro",
        "sonar-reasoning"
    ]

    def __init__(self):
        """Initialize Perplexity service"""
        self.api_key = PERPLEXITY_CONFIG['api_key']
        self.api_url = PERPLEXITY_CONFIG['api_url']

        # FIX: Replace invalid model automatically
        configured_model = MODEL_SETTINGS['perplexity_model']
        if configured_model not in self.VALID_MODELS:
            logger.warning(
                f"Invalid Perplexity model '{configured_model}'. "
                f"Switching to 'sonar-pro'."
            )
            configured_model = "sonar-pro"

        self.model = configured_model
        self.max_tokens = MODEL_SETTINGS['max_tokens']
        self.temperature = MODEL_SETTINGS['temperature']

        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY is required")

        logger.info(f"PerplexityService initialized with model: {self.model}")

    def generate_music_description(self, word, language='English', custom_settings=None):
        """Generate music description using Perplexity AI"""
        try:
            logger.info(f'Generating music description for "{word}" in {language}')

            # Prompt building
            system_prompt = get_system_prompt(language)
            user_prompt = f"Generate a unique music track inspired by the word: {word}"

            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            payload = {
                'model': self.model,
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                'max_tokens': self.max_tokens,
                'temperature': self.temperature
            }

            logger.info("Calling Perplexity API...")
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)

            if response.status_code != 200:
                logger.error(f"Perplexity API error {response.status_code}: {response.text}")
                raise Exception(f"API request failed ({response.status_code})")

            api_response = response.json()
            content = api_response["choices"][0]["message"]["content"].strip()

            # Strip ```json ``` wrapper
            if content.startswith("```"):
                content = content.split("```")[1]  # Removes first ```
            if content.startswith("json"):
                content = content[4:]
            content = content.strip().rstrip("`").strip()

            # Parse JSON
            try:
                result = json.loads(content)
                logger.info("Successfully parsed Perplexity JSON response")
                return result
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON from API: {content}")
                raise Exception("Perplexity returned invalid JSON")

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error calling Perplexity API: {str(e)}")
            raise Exception(f"Failed to connect to Perplexity API: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
