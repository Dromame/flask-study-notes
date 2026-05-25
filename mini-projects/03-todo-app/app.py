from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#database
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///tasks.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#bind database object
db = SQLAlchemy(app)

# define task
class Task(db.Model):
    #default table name "task"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120),nullable=False)

# create data table
with app.app_context():
    db.create_all()

# route
@app.route("/",methods=["GET","POST"])
def tasks():
    # New posted task
    if request.method == "POST":
        title = request.form["title"].strip()
        if title:
            task = Task(title=title)
            db.session.add(task)
            db.session.commit() #?
        return redirect(url_for("tasks"))

    # get page
    task_list = Task.query.order_by(Task.id.desc()).all()
    return render_template("tasks.html",tasks=task_list)

if __name__ == "__main__":
    app.run(debug=True)