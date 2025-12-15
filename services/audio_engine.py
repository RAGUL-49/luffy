"""
Audio Engine - Audio generation using Freesound API
"""
import requests
from config.settings import AUDIO_CONFIG
from utils.logger import setup_logger

logger = setup_logger()

class AudioEngine:
    """Audio generation service using Freesound.org API"""
    
    def __init__(self):
        """Initialize audio engine"""
        self.api_key = AUDIO_CONFIG.get('freesound_api_key', '')
        self.use_api = bool(self.api_key)
        
        # Placeholder tracks by mood
        self.placeholder_tracks = {
            'energetic': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
            'happy': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
            'sad': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3',
            'relaxed': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3',
            'emotional': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3',
            'intense': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3',
            'peaceful': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3',
            'uplifting': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3',
            'dark': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3',
            'romantic': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3',
            'chill': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3',
            'aggressive': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3',
            'default': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
        }
        
        if self.use_api:
            logger.info("AudioEngine initialized with Freesound API")
        else:
            logger.info("AudioEngine initialized with placeholder audio (no API key)")
    
    def generate_audio(self, track_data):
        """
        Generate audio based on track description
        
        Args:
            track_data (dict): Track information (genre, mood, style)
            
        Returns:
            dict: Audio information (url, format, engine)
        """
        try:
            logger.info(f"Generating audio for: {track_data.get('title', 'Unknown')}")
            
            # Try Freesound API if available
            if self.use_api:
                try:
                    return self._generate_with_freesound(track_data)
                except Exception as e:
                    logger.warning(f"Freesound API failed: {str(e)}, using placeholder")
                    return self._generate_placeholder(track_data)
            else:
                return self._generate_placeholder(track_data)
                
        except Exception as e:
            logger.error(f'Audio generation error: {str(e)}')
            return self._generate_placeholder(track_data)
    
    def _generate_with_freesound(self, track_data):
        """
        Generate audio using Freesound.org API
        
        Args:
            track_data (dict): Track information
            
        Returns:
            dict: Audio information
        """
        try:
            # Build search query
            genre = track_data.get('genre', 'music')
            mood = track_data.get('mood', 'ambient')
            search_query = f"{genre} {mood}".lower()
            
            logger.info(f"Searching Freesound for: {search_query}")
            
            # API headers
            headers = {
                'Authorization': f"Token {self.api_key}"
            }
            
            # API parameters
            params = {
                'query': search_query,
                'filter': 'duration:[30 TO 180]',  # 30s to 3min
                'fields': 'id,name,previews,duration,username',
                'page_size': 10,
                'sort': 'rating_desc'
            }
            
            # Make request
            response = requests.get(
                'https://freesound.org/apiv2/search/text/',
                headers=headers,
                params=params,
                timeout=10
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Check results
            if data.get('results') and len(data['results']) > 0:
                sound = data['results'][0]
                
                # Get audio URL
                audio_url = (
                    sound['previews'].get('preview-hq-mp3') or 
                    sound['previews'].get('preview-lq-mp3')
                )
                
                logger.info(f"Found audio: {sound['name']}")
                
                return {
                    'url': audio_url,
                    'format': 'mp3',
                    'engine': 'freesound',
                    'sound_id': sound['id'],
                    'sound_name': sound['name'],
                    'duration': int(sound.get('duration', 0)),
                    'username': sound.get('username', 'unknown'),
                    'note': f'Audio from Freesound.org by {sound.get("username", "unknown")}'
                }
            
            logger.warning('No results from Freesound')
            raise Exception('No suitable sounds found')
            
        except requests.exceptions.RequestException as e:
            logger.error(f'Freesound API error: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Freesound error: {str(e)}')
            raise
    
    def _generate_placeholder(self, track_data):
        """
        Generate placeholder audio (no API needed)
        
        Args:
            track_data (dict): Track information
            
        Returns:
            dict: Placeholder audio information
        """
        mood = track_data.get('mood', '').lower()
        audio_url = self.placeholder_tracks.get(mood, self.placeholder_tracks['default'])
        
        logger.info(f"Using placeholder audio for mood: {mood}")
        
        return {
            'url': audio_url,
            'format': 'mp3',
            'engine': 'placeholder',
            'note': 'Free music from SoundHelix. Add Freesound API key for real audio.'
        }