from pathlib import Path
from uuid import uuid4

from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from . import db
from .auth import login_required
from .models import Entry


bp = Blueprint("journal", __name__)


def get_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)

    if entry.user_id != g.user.id:
        abort(403)

    return entry


@bp.route("/")
def index():
    entries = Entry.query.order_by(Entry.created_at.desc()).all()
    return render_template("index.html", entries=entries)


@bp.route("/entries")
@login_required
def my_entries():
    entries = Entry.query.filter_by(user_id=g.user.id).order_by(Entry.created_at.desc()).all()
    return render_template("journal/list.html", entries=entries)


@bp.route("/entries/create", methods=("GET", "POST"))
@login_required
def create_entry():
    if request.method == "POST":
        title = request.form["title"].strip()
        body = request.form["body"].strip()
        cover = request.files.get("cover")
        error = None

        if not title:
            error = "标题不能为空。"
        elif not body:
            error = "正文不能为空。"

        filename = None

        if error is None and cover and cover.filename:
            safe_name = secure_filename(cover.filename)
            filename = f"{uuid4().hex}_{safe_name}"
            save_path = Path(current_app.config["UPLOAD_FOLDER"]) / filename
            cover.save(save_path)

        if error is None:
            entry = Entry(
                title=title,
                body=body,
                cover_filename=filename,
                author=g.user,
            )
            db.session.add(entry)
            db.session.commit()
            flash("record success", "success")
            return redirect(url_for("journal.my_entries"))

        flash(error, "error")

    return render_template("journal/form.html", entry=None)


@bp.route("/entries/<int:entry_id>/edit", methods=("GET", "POST"))
@login_required
def edit_entry(entry_id):
    entry = get_entry(entry_id)

    if request.method == "POST":
        title = request.form["title"].strip()
        body = request.form["body"].strip()

        if not title or not body:
            flash("title and body cannot be empty.", "error")
        else:
            entry.title = title
            entry.body = body
            db.session.commit()
            flash("updated", "success")
            return redirect(url_for("journal.my_entries"))

    return render_template("journal/form.html", entry=entry)


@bp.post("/entries/<int:entry_id>/delete")
@login_required
def delete_entry(entry_id):
    entry = get_entry(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash("delete", "success")
    return redirect(url_for("journal.my_entries"))
