import os

from flask import Flask, session, redirect, url_for

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    @app.route("/", methods=['GET'])
    def root_url_router():
        return redirect(url_for("auth_blueprint.login_router"))

    from . import auth
    app.register_blueprint(auth.auth_blueprint)

    from . import dashboard
    app.register_blueprint(dashboard.dashboard_blueprint)

    from . import filemanager
    app.register_blueprint(filemanager.filemanager_blueprint)

    return app