# Learn Sphere

A Flask-based learning management system for organizing and managing course content from your local filesystem.

## Features

- 📚 **Automatic Course Detection** - Scans directories and automatically organizes courses, modules, and lessons
- 🖼️ **Smart Image Handling** - Automatically displays course thumbnails (supports: cover, thumbnail, image, logo, icon)
- 🎨 **Theme Support** - Light/dark theme toggle with persistent user preferences
- 📊 **Progress Tracking** - Track learning progress across courses and modules
- 🗂️ **Hierarchical Navigation** - Browse nested directories with breadcrumb navigation
- 🔒 **Security** - Path traversal protection and input validation
- 💾 **Registry Caching** - Efficient scanning with registry-based caching

## Architecture

Learn Sphere follows a clean layered architecture:

- **Routes** - Deliver frontend templates
- **Controllers** - Expose API endpoints
- **Services** - Business logic and heavy lifting
- **Repositories** - Data access layer (JSON files)
- **Models** - Data structures and types
- **Utils** - Shared utilities and helpers

## Environment Configuration

Create a `.env` file in the root directory:

```env
# Environment Configuration
ENV=DEV
DEBUG=true
HOST=127.0.0.1
PORT=7000

# Courses Configuration
# Set this to the absolute path of your courses directory
COURSES_ROOT_DIRECTORY_ABS_PATH=/path/to/your/courses/directory
```

## Course Directory Structure

### Course with Modules
```
my-course/
├── thumbnail.jpg          # Course thumbnail (auto-detected)
├── module-1/
│   ├── 01-lesson1.mp4
│   ├── 02-lesson2.pdf
│   └── 03-notes.txt
├── module-2/
│   ├── 01-video1.mp4
│   └── 02-slides.pptx
└── intro.mp4             # Root-level lesson
```

### Nested Directory Structure
```
courses/
├── web-development/       # Course
│   ├── cover.jpg
│   ├── html-basics/       # Module
│   ├── css-styling/       # Module
│   └── javascript/        # Module
├── data-science/          # Course
│   ├── thumbnail.png
│   ├── python-intro/
│   └── statistics/
└── programming/           # Directory (contains other courses)
    ├── beginner-courses/
    └── advanced-courses/
```

## Supported File Types

### Images (Thumbnails)
`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`

**Priority order:** cover → thumbnail → image → logo → icon

### Lessons
- **Video**: `.mp4`, `.webm`, `.mov`, `.m4v`
- **Audio**: `.mp3`, `.wav`, `.m4a`, `.flac`
- **Text/Documents**: `.txt`, `.md`, `.rst`, `.doc`, `.html`, `.htm`, `.pdf`

**Note:** Files with unsupported extensions will display a download option instead of preview.

## Installation & Setup

### 1. Install Dependencies

```bash
# Create and activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Install test dependencies (optional)
pip install -r requirements-test.txt
```

### 2. Configure Environment

Create a `.env` file with your courses directory path (see Environment Configuration above).

### 3. Run the Application

```bash
python3 run.py
```

The application will be available at `http://127.0.0.1:7000`

## Development

### Project Structure

```
learn-sphere/
├── app/
│   ├── controllers/          # API endpoints
│   ├── models/              # Data models
│   ├── repositories/        # Data access layer
│   ├── routes/              # Template routes
│   ├── services/            # Business logic
│   ├── static/              # CSS, JS, images
│   ├── templates/           # Jinja2 templates
│   └── utils/               # Shared utilities
├── tests/                   # Test suite
├── config.py                # Configuration
├── run.py                   # Application entry point
└── requirements.txt         # Python dependencies
```

### Running Tests

```bash
# Run all tests
python3 -m pytest

# Run with coverage
python3 -m pytest --cov=app --cov-report=html

# Run specific test file
python3 -m pytest tests/services/test_user_preferences_service.py
```

### Code Quality

The project follows strict architectural guidelines:
- Repository pattern for data access
- Service layer for business logic
- DRY (Don't Repeat Yourself) principle
- Input validation and security best practices
- Target: 85%+ code coverage

## Registry Management

Learn Sphere maintains a registry of scanned courses for performance. Manage it using:

```bash
# Show all registry entries
python3 manage_registry.py show

# Clean up old entries (default: 30 days)
python3 manage_registry.py cleanup [days]

# Clear entire registry
python3 manage_registry.py clear

# Force re-scan all directories
python3 manage_registry.py force-analyze
```

## How It Works

### Content Detection
1. **First scan**: Deep analysis determines if directory is a Course, Module, or Directory
2. **Registry caching**: Results stored in `app/data/registry.json` for fast subsequent loads
3. **Image discovery**: Automatically finds and serves course thumbnails
4. **Progress calculation**: Tracks completion status (placeholder implementation)

### Image Handling
- Course images are auto-detected with priority: `cover.*` > `thumbnail.*` > `image.*` > `logo.*` > `icon.*`
- If no image found, displays 2-character initials from course title
- Images served securely through `/media/course/<course_id>/<filename>` route
- Path traversal protection prevents unauthorized file access

### User Preferences
Stored in `app/data/user_preferences.json`:
- Theme preference (light/dark)
- Last accessed course
- Playback speeds (video/audio)

## API Endpoints

### User Preferences
- `GET /api/user-preferences/theme` - Get theme preference
- `POST /api/user-preferences/theme` - Update theme
- `GET /api/user-preferences/playback-speed` - Get playback speeds
- `POST /api/user-preferences/playback-speed` - Update speeds
- `GET /api/user-preferences/` - Get all preferences

## Troubleshooting

### Images not displaying
- Ensure images are named `thumbnail.*`, `cover.*`, `image.*`, `logo.*`, or `icon.*`
- Supported formats: jpg, jpeg, png, gif, bmp, svg, webp
- Check browser console for 404 errors

### Courses not appearing
- Verify `COURSES_ROOT_DIRECTORY_ABS_PATH` in `.env`
- Run `python3 manage_registry.py force-analyze` to re-scan
- Check directory permissions

### Application won't start
- Ensure Python 3.10+ is installed
- Activate virtual environment
- Install all dependencies: `pip install -r requirements.txt`

## License

[Add your license here]
