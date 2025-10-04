from flask import Flask
from flask_assets import Environment, Bundle


def create_app():
    app = Flask(__name__)
    
    assets = Environment(app)
    scss = Bundle(
        'scss/main.scss',
        filters='libsass',
        output='css/main.css'
    )
    assets.register('scss_all', scss)

    # Import and register modular routes
    from app.routes import home_route, directory_route, course_details_route, lesson_route, media_route
    app.register_blueprint(home_route.bp)
    app.register_blueprint(directory_route.bp)
    app.register_blueprint(course_details_route.bp)
    app.register_blueprint(lesson_route.bp)
    app.register_blueprint(media_route.bp)

    # Import and register controllers
    from app.controllers.user_preferences_controller import user_preferences_blueprint
    app.register_blueprint(user_preferences_blueprint)

    return app
