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

    # Register template filters
    from app.services.registry_service import RegistryService

    @app.template_filter('course_color')
    def course_color_filter(course):
        """Template filter to get course color."""
        registry_service = RegistryService()
        return registry_service.get_color(course.title, course.path or "", course.node_type)

    # Import and register routes
    from . import routes
    app.register_blueprint(routes.bp)

    # Import and register controllers
    from app.controllers.user_preferences_controller import user_preferences_blueprint
    app.register_blueprint(user_preferences_blueprint)

    return app
