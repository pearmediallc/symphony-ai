# TikTok Symphony AI Studio

A secure web application for generating TikTok scripts and creating AI-powered digital avatar videos using the TikTok Business API.

## Features

### 🔐 Authentication System
- Secure login page with session management
- Environment-based authentication credentials
- Protected routes and API endpoints

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
- TikTok Advertiser ID

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

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. Update `.env` file with your values:
- `AUTH_USERNAME`: Login username (default: admin)
- `AUTH_PASSWORD`: Login password (default: password)
- `TIKTOK_ACCESS_TOKEN`: Your TikTok API access token
- `TIKTOK_ADVERTISER_ID`: Your TikTok advertiser ID
- `SECRET_KEY`: Flask session secret key (change in production)

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Navigate to `http://localhost:5000`
2. Login with your configured credentials
3. Choose between Script Generator or Avatar Videos
4. The application automatically uses TikTok credentials from environment variables
5. Follow the interface to generate content

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

- Login authentication required for all features
- API credentials stored securely in environment variables
- Session-based authentication with Flask sessions
- Access tokens never exposed in frontend code
- All API calls are made through your secure backend

## Recent Changes

- ✅ Added authentication system with login page
- ✅ Removed manual input fields for access token and advertiser ID
- ✅ Removed video/image upload functionality (use TikTok Ads Manager instead)
- ✅ All API credentials now loaded from environment variables
- ✅ Enhanced security with session management and protected routes

## License

Private repository - All rights reserved

## Support

For issues and questions, please contact the development team.