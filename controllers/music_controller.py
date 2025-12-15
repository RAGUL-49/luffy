"""
Music Controller - Business logic for music generation
"""
import time
from services.perplexity_service import PerplexityService
from services.audio_engine import AudioEngine
from utils.validators import validate_input
from utils.json_formatter import prepare_json
from utils.logger import setup_logger

logger = setup_logger()

class MusicController:
    """Controller for handling music generation requests"""
    
    def __init__(self):
        """Initialize services and storage"""
        self.perplexity_service = PerplexityService()
        self.audio_engine = AudioEngine()
        self.track_store = {}  # In-memory storage
        self.playlist_store = {}  # In-memory playlist storage
        logger.info("MusicController initialized")
    
    def generate_music(self, word, language='English', custom_settings=None):
        """
        Generate music from a word
        
        Args:
            word (str): The input word/name
            language (str): Target language
            custom_settings (dict): Optional custom settings
            
        Returns:
            dict: Generation result
        """
        try:
            logger.info(f'Generating music for: "{word}"')
            
            # Step 1: Validate input
            is_valid, error_message = validate_input(word)
            if not is_valid:
                logger.warning(f"Validation failed: {error_message}")
                return {
                    'success': False,
                    'error': error_message
                }
            
            # Step 2: Get music description from Perplexity AI
            logger.info("Requesting description from Perplexity AI...")
            perplexity_response = self.perplexity_service.generate_music_description(
                word, 
                language, 
                custom_settings or {}
            )
            
            # Step 3: Prepare and validate JSON
            logger.info("Preparing JSON response...")
            prepared_data = prepare_json(perplexity_response, word)
            
            # Step 4: Generate audio from description
            logger.info("Generating audio...")
            audio_data = self.audio_engine.generate_audio(prepared_data['track'])
            
            # Step 5: Add audio info to response
            prepared_data['track']['audio_url'] = audio_data['url']
            prepared_data['track']['audio_format'] = audio_data['format']
            prepared_data['track']['audio_engine'] = audio_data['engine']
            
            # Step 6: Store track
            track_id = str(int(time.time() * 1000))
            self.track_store[track_id] = prepared_data
            
            logger.info(f'Successfully generated track: {track_id}')
            
            return {
                'success': True,
                'trackId': track_id,
                'data': prepared_data,
                'audioInfo': {
                    'engine': audio_data['engine'],
                    'format': audio_data['format'],
                    'note': audio_data.get('note', '')
                }
            }
            
        except Exception as e:
            logger.error(f'Error generating music: {str(e)}', exc_info=True)
            return {
                'success': False,
                'error': 'Failed to generate music',
                'message': str(e)
            }
    
    def get_track(self, track_id):
        """
        Retrieve a track by ID
        
        Args:
            track_id (str): Track identifier
            
        Returns:
            dict: Track data or None
        """
        return self.track_store.get(track_id)
    
    def list_tracks(self):
        """
        List all generated tracks

        Returns:
            list: List of track summaries
        """
        return [
            {
                'id': track_id,
                'title': data['track']['title'],
                'keyword': data['metadata']['keyword'],
                'timestamp': data['metadata']['timestamp']
            }
            for track_id, data in self.track_store.items()
        ]

    def create_playlist(self, name, track_ids):
        """
        Create a new playlist

        Args:
            name (str): Playlist name
            track_ids (list): List of track IDs to include

        Returns:
            dict: Playlist creation result
        """
        try:
            # Validate tracks exist
            valid_tracks = []
            for track_id in track_ids:
                if track_id in self.track_store:
                    valid_tracks.append(track_id)
                else:
                    logger.warning(f"Track {track_id} not found, skipping")

            if not valid_tracks:
                return {
                    'success': False,
                    'error': 'No valid tracks provided'
                }

            # Create playlist
            playlist_id = str(int(time.time() * 1000))
            self.playlist_store[playlist_id] = {
                'id': playlist_id,
                'name': name,
                'tracks': valid_tracks,
                'created_at': time.time(),
                'updated_at': time.time()
            }

            logger.info(f"Created playlist '{name}' with {len(valid_tracks)} tracks")
            return {
                'success': True,
                'playlist_id': playlist_id,
                'data': self.playlist_store[playlist_id]
            }

        except Exception as e:
            logger.error(f"Error creating playlist: {str(e)}")
            return {
                'success': False,
                'error': 'Failed to create playlist',
                'message': str(e)
            }

    def get_playlist(self, playlist_id):
        """
        Get a playlist by ID

        Args:
            playlist_id (str): Playlist identifier

        Returns:
            dict: Playlist data or None
        """
        return self.playlist_store.get(playlist_id)

    def list_playlists(self):
        """
        List all playlists

        Returns:
            list: List of playlist summaries
        """
        return [
            {
                'id': playlist_id,
                'name': data['name'],
                'track_count': len(data['tracks']),
                'created_at': data['created_at']
            }
            for playlist_id, data in self.playlist_store.items()
        ]

    def add_to_playlist(self, playlist_id, track_ids):
        """
        Add tracks to an existing playlist

        Args:
            playlist_id (str): Playlist identifier
            track_ids (list): List of track IDs to add

        Returns:
            dict: Update result
        """
        try:
            if playlist_id not in self.playlist_store:
                return {
                    'success': False,
                    'error': 'Playlist not found'
                }

            playlist = self.playlist_store[playlist_id]
            added_count = 0

            for track_id in track_ids:
                if track_id in self.track_store and track_id not in playlist['tracks']:
                    playlist['tracks'].append(track_id)
                    added_count += 1

            if added_count > 0:
                playlist['updated_at'] = time.time()
                logger.info(f"Added {added_count} tracks to playlist '{playlist['name']}'")

            return {
                'success': True,
                'added_count': added_count,
                'data': playlist
            }

        except Exception as e:
            logger.error(f"Error adding to playlist: {str(e)}")
            return {
                'success': False,
                'error': 'Failed to add tracks to playlist',
                'message': str(e)
            }

    def remove_from_playlist(self, playlist_id, track_ids):
        """
        Remove tracks from a playlist

        Args:
            playlist_id (str): Playlist identifier
            track_ids (list): List of track IDs to remove

        Returns:
            dict: Update result
        """
        try:
            if playlist_id not in self.playlist_store:
                return {
                    'success': False,
                    'error': 'Playlist not found'
                }

            playlist = self.playlist_store[playlist_id]
            removed_count = 0

            for track_id in track_ids:
                if track_id in playlist['tracks']:
                    playlist['tracks'].remove(track_id)
                    removed_count += 1

            if removed_count > 0:
                playlist['updated_at'] = time.time()
                logger.info(f"Removed {removed_count} tracks from playlist '{playlist['name']}'")

            return {
                'success': True,
                'removed_count': removed_count,
                'data': playlist
            }

        except Exception as e:
            logger.error(f"Error removing from playlist: {str(e)}")
            return {
                'success': False,
                'error': 'Failed to remove tracks from playlist',
                'message': str(e)
            }

    def rename_playlist(self, playlist_id, new_name):
        """
        Rename an existing playlist

        Args:
            playlist_id (str): Playlist identifier
            new_name (str): The new name for the playlist

        Returns:
            dict: Update result
        """
        try:
            if playlist_id not in self.playlist_store:
                return {
                    'success': False,
                    'error': 'Playlist not found'
                }

            if not new_name or not new_name.strip():
                return {
                    'success': False,
                    'error': 'Playlist name cannot be empty'
                }

            playlist = self.playlist_store[playlist_id]
            old_name = playlist['name']
            playlist['name'] = new_name.strip()
            playlist['updated_at'] = time.time()

            logger.info(f"Renamed playlist '{old_name}' to '{new_name.strip()}'")

            return {'success': True, 'data': playlist}

        except Exception as e:
            logger.error(f"Error renaming playlist: {str(e)}", exc_info=True)
            return {'success': False, 'error': 'Failed to rename playlist', 'message': str(e)}

    def reorder_playlist_tracks(self, playlist_id, ordered_track_ids):
        """
        Reorder tracks in a playlist.

        Args:
            playlist_id (str): The ID of the playlist to update.
            ordered_track_ids (list): A list of track IDs in the new desired order.

        Returns:
            dict: The result of the operation.
        """
        try:
            if playlist_id not in self.playlist_store:
                return {'success': False, 'error': 'Playlist not found'}

            playlist = self.playlist_store[playlist_id]

            # Validate that the new list of IDs matches the existing one, just reordered
            if sorted(playlist['tracks']) != sorted(ordered_track_ids):
                logger.warning(f"Track reorder mismatch for playlist {playlist_id}")
                return {
                    'success': False,
                    'error': 'Track list mismatch. Reorder failed.'
                }

            # Update the track order
            playlist['tracks'] = ordered_track_ids
            playlist['updated_at'] = time.time()

            logger.info(f"Reordered tracks for playlist '{playlist['name']}'")
            return {
                'success': True,
                'data': playlist
            }

        except Exception as e:
            logger.error(f"Error reordering playlist tracks: {str(e)}", exc_info=True)
            return {'success': False, 'error': 'Failed to reorder tracks', 'message': str(e)}


    def delete_playlist(self, playlist_id):
        """
        Delete a playlist

        Args:
            playlist_id (str): Playlist identifier

        Returns:
            dict: Deletion result
        """
        try:
            if playlist_id not in self.playlist_store:
                return {
                    'success': False,
                    'error': 'Playlist not found'
                }

            deleted_playlist = self.playlist_store.pop(playlist_id)
            logger.info(f"Deleted playlist '{deleted_playlist['name']}'")

            return {
                'success': True,
                'deleted_playlist': deleted_playlist
            }

        except Exception as e:
            logger.error(f"Error deleting playlist: {str(e)}")
            return {
                'success': False,
                'error': 'Failed to delete playlist',
                'message': str(e)
            }