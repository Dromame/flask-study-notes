from flask import Flask, render_template
from extensions import db


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev"

    db.init_app(app)

    from models import Post
    from blog import bp as blog_bp

    app.register_blueprint(blog_bp)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)