from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev-change-this",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(app.instance_path) / 'study_journal.sqlite3'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=str(Path(app.root_path) / "static" / "uploads"),
    )

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    from . import models
    from .auth import bp as auth_bp
    from .journal import bp as journal_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(journal_bp)

    with app.app_context():
        db.create_all()

    return app