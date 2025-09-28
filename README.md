# Learn Sphere Setup

## Environment Configuration

Create a `.env` file in the root directory with the following configuration:

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

## Directory Structure Examples

### Course Structure
```
my-course/
├── module-1/
│   ├── lesson1.mp4
│   ├── lesson2.pdf
│   └── notes.txt
├── module-2/
│   ├── video1.mp4
│   └── slides.pptx
├── intro.mp4
└── cover.jpg (optional course image)
```

### Directory of Courses
```
courses/
├── web-development/     (course)
│   ├── html-basics/
│   ├── css-styling/
│   └── javascript/
├── data-science/        (course)
│   ├── python-intro/
│   └── statistics/
└── programming/         (directory)
    ├── beginner-courses/
    └── advanced-courses/
```

## Content Type Detection

The system automatically detects:
- **Course**: Contains modules (directories with only files) and/or lesson files
- **Module**: Contains only lesson files (no subdirectories)  
- **Directory**: Contains other directories or courses

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

The application will be available at `http://127.0.0.1:7000`
