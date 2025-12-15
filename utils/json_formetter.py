"""
JSON Formatter - Format and validate JSON responses
"""
from datetime import datetime

def prepare_json(perplexity_response, user_word):
    """
    Prepare and validate JSON response from Perplexity
    
    Args:
        perplexity_response (dict): Response from Perplexity AI
        user_word (str): Original user input word
        
    Returns:
        dict: Formatted and validated JSON
    """
    try:
        # Ensure response has correct structure
        if not isinstance(perplexity_response, dict):
            raise ValueError('Response must be a dictionary')
        
        if 'track' not in perplexity_response or 'metadata' not in perplexity_response:
            raise ValueError('Invalid response structure - missing track or metadata')
        
        track = perplexity_response['track']
        metadata = perplexity_response['metadata']
        
        # Validate track is a dictionary
        if not isinstance(track, dict):
            raise ValueError('Track must be a dictionary')
        
        # Add/update timestamp if missing
        if 'timestamp' not in metadata or not metadata['timestamp']:
            metadata['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        
        # Ensure keyword matches user input
        metadata['keyword'] = user_word
        
        # Prepare track with defaults
        prepared_track = {
            'title': track.get('title') or f"{user_word} - Generated Track",
            'language': track.get('language') or 'English',
            'genre': track.get('genre') or 'Electronic',
            'mood': track.get('mood') or 'energetic',
            'style': track.get('style') or 'modern electronic production',
            'lyrics': track.get('lyrics'),  # Can be None
            'duration': track.get('duration') or '1-2 minutes',
            'audio_url': track.get('audio_url') or 'placeholder'
        }
        
        # Prepare metadata
        prepared_metadata = {
            'keyword': metadata.get('keyword') or user_word,
            'timestamp': metadata['timestamp'],
            'model': metadata.get('model') or 'perplexity'
        }
        
        return {
            'track': prepared_track,
            'metadata': prepared_metadata
        }
        
    except KeyError as e:
        raise Exception(f'Missing required field: {str(e)}')
    except Exception as e:
        raise Exception(f'JSON preparation failed: {str(e)}')