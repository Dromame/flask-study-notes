from functools import wraps
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id else None

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please login。", "warning")
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        error = None

        if not username:
            error = "user name is empty"
        elif len(password) < 6:
            error = "6 digits"
        elif User.query.filter_by(username=username).first():
            error = "username existed"

        if error is None:
            user = User(
                username=username,
                password_hash=generate_password_hash(password),
            )
            db.session.add(user)
            db.session.commit()
            flash("success, please login", "success")
            return redirect(url_for("auth.login"))

        flash(error, "error")

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password_hash, password):
            flash("failed user name", "error")
        else:
            session.clear()
            session["user_id"] = user.id
            flash("login successful", "success")
            return redirect(url_for("journal.my_entries"))
    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    session.clear()
    flash("logout successful", "success")
    return redirect(url_for("journal.index"))