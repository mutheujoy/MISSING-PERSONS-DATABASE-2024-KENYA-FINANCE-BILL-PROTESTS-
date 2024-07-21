from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="Templates/templates")
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from . import views, models

        db.create_all()
        # views.app = app

        return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
