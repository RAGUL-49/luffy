"""
Music Routes - API endpoints for music generation
"""
from flask import Blueprint, request, jsonify
from controllers.music_controller import MusicController
from utils.logger import setup_logger

music_bp = Blueprint('music', __name__)
controller = MusicController()
logger = setup_logger()

@music_bp.route('/generate', methods=['POST'])
def generate_music():
    """
    Generate music from a word/name
    
    Request body:
    {
        "word": "string",
        "language": "string" (optional, default: "English")
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Extract parameters
        word = data.get('word', '').strip()
        language = data.get('language', 'English')
        custom_settings = data.get('customSettings', {})
        
        # Validate word
        if not word:
            return jsonify({
                'success': False,
                'error': 'Word is required'
            }), 400
        
        # Generate music
        logger.info(f"Received request for word: '{word}' in {language}")
        result = controller.generate_music(word, language, custom_settings)
        
        # Return result
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 500
        
    except Exception as e:
        logger.error(f"Error in generate_music endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to generate music',
            'message': str(e)
        }), 500

@music_bp.route('/track/<track_id>', methods=['GET'])
def get_track(track_id):
    """
    Retrieve a generated track by ID
    """
    try:
        result = controller.get_track(track_id)
        
        if result:
            return jsonify({
                'success': True,
                'data': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Track not found'
            }), 404
            
    except Exception as e:
        logger.error(f"Error retrieving track: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve track',
            'message': str(e)
        }), 500

@music_bp.route('/tracks', methods=['GET'])
def list_tracks():
    """
    List all generated tracks
    """
    try:
        tracks = controller.list_tracks()
        return jsonify({
            'success': True,
            'tracks': tracks,
            'count': len(tracks)
        }), 200
    except Exception as e:
        logger.error(f"Error listing tracks: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@music_bp.route('/playlists', methods=['POST'])
def create_playlist():
    """
    Create a new playlist

    Request body:
    {
        "name": "string",
        "track_ids": ["string"]
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400

        name = data.get('name', '').strip()
        track_ids = data.get('track_ids', [])

        if not name:
            return jsonify({
                'success': False,
                'error': 'Playlist name is required'
            }), 400

        if not isinstance(track_ids, list):
            return jsonify({
                'success': False,
                'error': 'track_ids must be a list'
            }), 400

        logger.info(f"Creating playlist '{name}' with {len(track_ids)} tracks")
        result = controller.create_playlist(name, track_ids)

        if result.get('success'):
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Error creating playlist: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to create playlist',
            'message': str(e)
        }), 500

@music_bp.route('/playlists', methods=['GET'])
def list_playlists():
    """
    List all playlists
    """
    try:
        playlists = controller.list_playlists()
        return jsonify({
            'success': True,
            'playlists': playlists,
            'count': len(playlists)
        }), 200
    except Exception as e:
        logger.error(f"Error listing playlists: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@music_bp.route('/playlist/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    """
    Get a playlist by ID
    """
    try:
        playlist = controller.get_playlist(playlist_id)

        if playlist:
            # Include full track data
            tracks_data = []
            for track_id in playlist['tracks']:
                track = controller.get_track(track_id)
                if track:
                    tracks_data.append({
                        'id': track_id,
                        **track
                    })

            playlist_with_tracks = {
                **playlist,
                'tracks_data': tracks_data
            }

            return jsonify({
                'success': True,
                'data': playlist_with_tracks
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Playlist not found'
            }), 404

    except Exception as e:
        logger.error(f"Error retrieving playlist: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve playlist',
            'message': str(e)
        }), 500

@music_bp.route('/playlist/<playlist_id>', methods=['PUT'])
def update_playlist(playlist_id):
    """
    Update a playlist (add/remove tracks)

    Request body:
    {
        "action": "add" | "remove" | "rename" | "reorder",
        "track_ids": ["string"] (for add/remove),
        "ordered_track_ids": ["string"] (for reorder),
        "name": "string" (for rename)
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400

        action = data.get('action')
        track_ids = data.get('track_ids', [])
        new_name = data.get('name', '').strip()
        ordered_track_ids = data.get('ordered_track_ids', [])

        if action == 'add':
            if not isinstance(track_ids, list):
                return jsonify({'success': False, 'error': 'track_ids must be a list'}), 400
            result = controller.add_to_playlist(playlist_id, track_ids)
        elif action == 'remove':
            if not isinstance(track_ids, list):
                return jsonify({'success': False, 'error': 'track_ids must be a list'}), 400
            result = controller.remove_from_playlist(playlist_id, track_ids)
        elif action == 'rename':
            if not new_name:
                return jsonify({
                    'success': False,
                    'error': 'New name is required for rename action'
                }), 400
            result = controller.rename_playlist(playlist_id, new_name)
        elif action == 'reorder':
            if not isinstance(ordered_track_ids, list) or not ordered_track_ids:
                return jsonify({
                    'success': False,
                    'error': 'ordered_track_ids list is required for reorder action'
                }), 400
            result = controller.reorder_playlist_tracks(playlist_id, ordered_track_ids)
        else:
            return jsonify({
                'success': False,
                'error': 'Action must be "add", "remove", "rename", or "reorder"'
            }), 400

        if result.get('success'):
            return jsonify(result), 200
        else:
            # Use 404 for 'not found' errors, otherwise 400
            status_code = 404 if 'not found' in result.get('error', '').lower() else 400
            return jsonify(result), status_code

    except Exception as e:
        logger.error(f"Error updating playlist: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to update playlist',
            'message': str(e)
        }), 500

@music_bp.route('/playlist/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    """
    Delete a playlist
    """
    try:
        result = controller.delete_playlist(playlist_id)

        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        logger.error(f"Error deleting playlist: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to delete playlist',
            'message': str(e)
        }), 500