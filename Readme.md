🎵 Beatify (Python/Flask)
Transform any word or name into a unique musical experience using AI.

Tech Stack: Python + Flask + Perplexity AI + Freesound API

🚀 Features
Perplexity AI: Advanced music description generation
Freesound API: Real audio from 500,000+ sounds (FREE)
Simple Setup: Only 2 API keys needed (both free)
Python Flask: Clean, professional backend
RESTful API: Well-documented endpoints
Multi-Language: 12+ languages supported
📦 What You Need
Required:
Perplexity API Key (FREE - 5 requests/hour)
Get at: https://www.perplexity.ai/settings/api
Optional (Recommended):
Freesound API Key (FREE - 2000 requests/day)
Get at: https://freesound.org/apiv2/apply/
Without this: Uses placeholder audio (still works!)
With this: Real audio matching your descriptions
🏃 Quick Start (5 Minutes)
1. Install Python
bash
python --version  # Should be 3.9+
2. Clone & Setup
bash
# Clone repository
git clone <repo-url>
cd beatify

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
3. Configure API Keys
bash
# Copy example env file
cp .env.example .env

# Edit .env file and add your keys:
nano .env  # or use any text editor
Add your API keys:

env
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxx
FREESOUND_API_KEY=your-freesound-key  # Optional
4. Run
bash
python app.py
5. Open Browser
http://localhost:5000
✅ Done! Start generating music!

🔑 Getting API Keys
Step 1: Perplexity AI (REQUIRED - FREE)
Go to: https://www.perplexity.ai/
Click "Sign Up" (free account)
Go to: https://www.perplexity.ai/settings/api
Click "Generate API Key"
Copy key (starts with pplx-)
Paste in .env file
Free Tier:

✅ 5 requests per hour
✅ All models available
✅ No credit card needed
Step 2: Freesound API (OPTIONAL - FREE)
Why add this?

Without: Uses placeholder audio (generic music)
With: Real audio matching your descriptions
How to get:

Register
Go to: https://freesound.org/
Click "Sign Up"
Verify email
Apply for API Key
Visit: https://freesound.org/apiv2/apply/
Fill form:
Name: "Beatify"
Description: "AI music generation app"
Non-commercial use
Submit (usually approved instantly)
Get Your Key
Check email for approval
Visit: https://freesound.org/apiv2/credentials/
Copy your API key
Add to .env
env
   FREESOUND_API_KEY=your-key-here
Free Tier:

✅ 2000 requests per day
✅ Access to 500,000+ sounds
✅ High quality audio
✅ No credit card needed
📁 Project Structure
beatify/
│
├── app.py                      # Main Flask app
├── requirements.txt            # Dependencies
├── .env                        # API keys (create this)
│
├── routes/
│   └── music_routes.py         # API endpoints
│
├── controllers/
│   └── music_controller.py     # Business logic
│
├── services/
│   ├── perplexity_service.py   # Perplexity AI
│   └── audio_engine.py         # Freesound API
│
├── utils/
│   ├── validators.py           # Input validation
│   ├── json_formatter.py       # Data formatting
│   └── logger.py               # Logging
│
├── config/
│   └── settings.py             # Configuration
│
└── frontend/
    ├── index.html
    ├── styles.css
    └── script.js
🎯 API Endpoints
POST /api/generate
Generate music from a word

Request:

bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"word":"Happy","language":"English"}'
Response:

json
{
  "success": true,
  "trackId": "1701234567890",
  "data": {
    "track": {
      "title": "Happy Vibes",
      "genre": "Pop",
      "mood": "happy",
      "style": "upbeat acoustic guitar with cheerful melody",
      "lyrics": "Sunshine in my heart today...",
      "audio_url": "https://freesound.org/...",
      "audio_format": "mp3",
      "audio_engine": "freesound"
    },
    "metadata": {
      "keyword": "Happy",
      "timestamp": "2025-12-06T10:30:00Z",
      "model": "perplexity"
    }
  },
  "audioInfo": {
    "engine": "freesound",
    "format": "mp3",
    "note": "Audio from Freesound.org"
  }
}
GET /api/track/:id
Get track by ID

GET /api/tracks
List all generated tracks

GET /health
Health check

💰 Cost Breakdown
Service	Free Tier	Cost
Perplexity AI	5 requests/hour	$0
Freesound	2000 requests/day	$0
Total	-	$0/month
Upgrade Options (Optional):
Perplexity Pro: $20/month (unlimited requests)
Freesound is always free!
🛠️ Development
Run in Development Mode
bash
# Set environment
FLASK_ENV=development

# Run with auto-reload
python app.py
Run Tests
bash
pytest tests/
Code Formatting
bash
# Format code
black .

# Check style
flake8 .
🐛 Troubleshooting
"No module named 'flask'"
bash
pip install -r requirements.txt
"PERPLEXITY_API_KEY is required"
Check .env file exists
Verify API key starts with pplx-
No extra spaces in .env
"Freesound API failed"
Works without Freesound (uses placeholder)
Check API key is correct
Test at: https://freesound.org/apiv2/search/text/?query=test
Port Already in Use
bash
# Change port in .env
PORT=5001

# Or kill process
# Mac/Linux:
lsof -ti:5000 | xargs kill

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
📊 How It Works
User Input (Word)
      ↓
Perplexity AI → Generates music description
      ↓
{
  title: "...",
  genre: "Pop",
  mood: "happy",
  lyrics: "..."
}
      ↓
Freesound API → Finds matching audio
      ↓
Returns audio URL + metadata
      ↓
User plays audio
🚀 Deployment
Heroku
bash
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create beatify-app
git push heroku main
heroku config:set PERPLEXITY_API_KEY=your-key
heroku config:set FREESOUND_API_KEY=your-key
Railway
bash
railway init
railway up
railway variables set PERPLEXITY_API_KEY=your-key
railway variables set FREESOUND_API_KEY=your-key
Docker
dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
🎓 For AI Developers
Key Features:
Type hints throughout codebase
Error handling with try-except
Logging for debugging
Validation for security
Modular design for scalability
REST API best practices
Environment variables for config
Extend the Project:
Add more audio APIs (Jamendo, MusicGen)
Implement database (PostgreSQL, MongoDB)
Add user authentication
Create music playlists
Add audio processing (effects, mixing)
📝 Environment Variables
Variable	Required	Default	Description
PERPLEXITY_API_KEY	✅ Yes	-	Perplexity API key
FREESOUND_API_KEY	❌ No	-	Freesound API key
PORT	❌ No	5000	Server port
FLASK_ENV	❌ No	production	Environment mode
PERPLEXITY_MODEL	❌ No	llama-3.1-sonar-large-128k-online	AI model
MAX_TOKENS	❌ No	2000	Max response tokens
TEMPERATURE	❌ No	0.7	AI creativity (0-1)
📚 Resources
Flask Docs
Perplexity AI
Freesound API Docs
Python Best Practices
🤝 Contributing
Fork repository
Create feature branch
Commit changes
Push to branch
Open pull request
📝 License
MIT License - Free for personal and commercial use

💬 Support
Author: RAGUL N
Email: ragul.naa@gmail.com

GitHub: [@ragul-49](https://github.com/RAGUL-49)

LinkedIn:[@ragul-49]https://www.linkedin.com/in/ragul49/
Discord: Join community
Made with ❤️ and Python by AI Developers

🎉 100% FREE - No Credit Card Required!

