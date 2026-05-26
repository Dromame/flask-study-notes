from flask import Blueprint, redirect, render_template, request, url_for
from extensions import db
from models import Post


bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts)


@bp.route("/post/<int:post_id>")
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("detail.html", post=post)


@bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"].strip()
        summary = request.form["summary"].strip()
        body = request.form["body"].strip()

        if title and summary and body:
            post = Post(title=title, summary=summary, body=body)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("blog.index"))

    return render_template("form.html", post=None)


@bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
def edit(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == "POST":
        title = request.form["title"].strip()
        summary = request.form["summary"].strip()
        body = request.form["body"].strip()

        if title and summary and body:
            post.title = title
            post.summary = summary
            post.body = body
            db.session.commit()
            return redirect(url_for("blog.detail", post_id=post.id))

    return render_template("form.html", post=post)


@bp.post("/post/<int:post_id>/delete")
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("blog.index"))