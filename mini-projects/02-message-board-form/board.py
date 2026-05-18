from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
messages = []

@app.route("/",methods = ["GET","POST"])
def board():
    if request.method == "POST":
        name = request.form["name"].strip()
        message = request.form["message"].strip()

        if name and message:
            messages.append({"name":name,"message":message})
            return redirect(url_for("board"))
    return render_template("board.html",messages = messages)

if __name__ == "__main__":
    app.run(debug=True)