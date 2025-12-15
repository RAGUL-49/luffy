"""
Configuration Settings - Load and validate configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Perplexity Configuration (Required)
PERPLEXITY_CONFIG = {
    'api_key': os.getenv('PERPLEXITY_API_KEY', ''),
    'api_url': 'https://api.perplexity.ai/chat/completions'
}

# Model Settings
MODEL_SETTINGS = {
    'perplexity_model': os.getenv('PERPLEXITY_MODEL', 'llama-3.1-sonar-large-128k-online'),
    'max_tokens': int(os.getenv('MAX_TOKENS', '2000')),
    'temperature': float(os.getenv('TEMPERATURE', '0.7'))
}

# Audio Configuration (Optional)
AUDIO_CONFIG = {
    'freesound_api_key': os.getenv('FREESOUND_API_KEY', '')
}

# Music Settings
MUSIC_SETTINGS = {
    'genres': [
        'Electronic', 'Pop', 'Hip Hop', 'Rock', 'Classical',
        'Jazz', 'EDM', 'R&B', 'Country', 'Folk',
        'Ambient', 'Lo-fi', 'Indie', 'Trap', 'House'
    ],
    'moods': [
        'energetic', 'happy', 'sad', 'relaxed', 'emotional',
        'intense', 'peaceful', 'uplifting', 'dark', 'romantic',
        'chill', 'aggressive'
    ],
    'languages': [
        'English', 'Spanish', 'French', 'German', 'Italian',
        'Japanese', 'Korean', 'Chinese', 'Hindi', 'Tamil',
        'Portuguese', 'Arabic'
    ]
}

# App Settings
APP_CONFIG = {
    'port': int(os.getenv('PORT', '5000')),
    'host': os.getenv('HOST', '0.0.0.0'),
    'debug': os.getenv('FLASK_ENV', 'production') == 'development',
    'cors_origins': os.getenv('CORS_ORIGINS', '*').split(',')
}

def validate_config():
    """Validate required configuration"""
    errors = []
    warnings = []
    
    # Check Perplexity API key
    if not PERPLEXITY_CONFIG['api_key']:
        errors.append('PERPLEXITY_API_KEY is required')
        errors.append('Get it from: https://www.perplexity.ai/settings/api')
    elif not PERPLEXITY_CONFIG['api_key'].startswith('pplx-'):
        warnings.append('PERPLEXITY_API_KEY should start with "pplx-"')
    
    # Check Freesound API key (optional)
    if not AUDIO_CONFIG['freesound_api_key']:
        warnings.append('FREESOUND_API_KEY not set - using placeholder audio')
        warnings.append('Get free key at: https://freesound.org/apiv2/apply/')
    
    # Print errors
    if errors:
        print("\n" + "="*60)
        print("CONFIGURATION ERRORS:")
        for error in errors:
            print(f"   {error}")
        print("="*60 + "\n")
        raise ValueError("Configuration validation failed")

    # Print warnings
    if warnings:
        print("\n" + "="*60)
        print("CONFIGURATION WARNINGS:")
        for warning in warnings:
            print(f"   {warning}")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("Configuration validated successfully")
        if AUDIO_CONFIG['freesound_api_key']:
            print("Freesound API key found - real audio enabled")
        else:
            print("Using placeholder audio")
        print("="*60 + "\n")

# Validate configuration on import
try:
    validate_config()
except ValueError as e:
    print(f"\n{e}\n")
    print("Please update your .env file with required API keys")
    print("See README.md for instructions\n")