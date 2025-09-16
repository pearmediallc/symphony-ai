# TikTok Symphony AI Studio

A professional web application for generating TikTok scripts and creating AI-powered digital avatar videos using the TikTok Business API.

## Features

### 📝 AI Script Generator
- Generate creative TikTok scripts using AI
- Custom prompts for any niche or industry
- Product-focused script generation
- Multiple tone and style options
- Generate up to 8 scripts at once
- Search and browse through generated scripts

### 🎭 Digital Avatar Videos
- Create videos with 80+ AI-powered digital avatars
- Text-to-speech video generation
- Use existing scripts or write new ones
- Batch video creation
- Professional avatars for various use cases

## Setup

### Prerequisites
- Python 3.8+
- TikTok Business API Access Token

### Installation

1. Clone the repository:
```bash
git clone https://github.com/pearmediallc/sym.git
cd sym
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Navigate to the home page at `http://localhost:5000`
2. Choose between Script Generator or Avatar Videos
3. Enter your TikTok Business API Access Token
4. Follow the step-by-step interface to generate content

## API Endpoints

### Script Generation
- `POST /api/create_task` - Create script generation task
- `GET /api/task_status` - Check task status
- `GET /api/list_scripts` - List generated scripts

### Avatar Videos
- `GET /api/get_avatars` - Get available avatars
- `POST /api/create_avatar_video_task` - Create avatar video
- `GET /api/get_avatar_video_task_status` - Check video status
- `GET /api/list_avatar_videos` - List generated videos
- `POST /api/update_avatar_video_name` - Update video name

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **API**: TikTok Business API v1.3
- **Styling**: Modern gradient design with TikTok brand colors

## Security

- Access tokens are only used locally and sent to TikTok's official API
- No tokens are stored on the server
- All API calls are made through your local server

## License

Private repository - All rights reserved

## Support

For issues and questions, please contact the development team.