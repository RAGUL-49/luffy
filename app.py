"""
Beatify - Transform words into music using AI
Main Flask Application
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from routes.music_routes import music_bp
from utils.logger import setup_logger

# Initialize Flask app
app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# Setup logger
logger = setup_logger()

# Register blueprints
app.register_blueprint(music_bp, url_prefix='/api')

# Serve frontend
@app.route('/')
def index():
    """Serve main page"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    try:
        return send_from_directory('frontend', path)
    except:
        return send_from_directory('frontend', 'index.html')

# Health check
@app.route('/health')
def health_check():
    """API health check"""
    return jsonify({
        'status': 'OK',
        'message': 'Beatify API is running',
        'version': '1.0.0'
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f'Internal error: {str(error)}')
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    
    print("\n" + "="*50)
    print("BEATIFY - AI Music Generator")
    print("="*50)
    print(f"Server starting on port {port}")
    print(f"Frontend: http://localhost:{port}")
    print(f"API: http://localhost:{port}/api")
    print(f"Health: http://localhost:{port}/health")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)