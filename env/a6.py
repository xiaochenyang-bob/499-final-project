from flask import Flask, render_template, request
app = Flask(__name__)
names = []

@app.route("/")
def index():
    name = request.args.get("newname")
    if name is not None:
        names.append(name)
    return render_template("index.html", names=names)

@app.route("/add")
def add():
    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)