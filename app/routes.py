from flask import Blueprint, render_template
from config import Config
from app.services.directory_service import DirectoryService

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    # Get courses from the configured directory
    courses = DirectoryService.scan_directory(Config.COURSES_ROOT_DIRECTORY_ABS_PATH)
    
    return render_template("home.html", courses=courses)
