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

    # Import and register routes
    from . import routes
    app.register_blueprint(routes.bp)

    return app
