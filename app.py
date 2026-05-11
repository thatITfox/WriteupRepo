from flask import Flask, render_template, send_from_directory, send_file
from werkzeug.exceptions import HTTPException
import markdown
import os

# check if the writeup folder exists
if not os.path.exists("writeups"): os.mkdir("writeups")

# path sanitation, stolen from my blog site code
def sanitize_filename(filename: str):
    safe_filename = filename.strip().replace("\n", "").replace("\r", "")
    safe_filename = os.path.normpath(f"/{safe_filename}")[1:]
    return safe_filename

# markdown renderer
def renderarticle(filepath) -> str:
    with open(filepath, "r") as f:
        articlemarkdown = f.read()
    html = markdown.markdown(articlemarkdown, extensions=["extra"])
    return html

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/writeups/")
def maindirectory():
    files = list()
    folders = list()

    filefolders = os.listdir("writeups")
    for item in filefolders:
        item_path = os.path.join("writeups", item)
        if os.path.isdir(item_path): folders.append(item)
        else: files.append(item)

    return render_template("structure.html", files=files, folders=folders)

@app.route("/writeups/<path:subpath>")
def routepath(subpath):
    # complex or dumbass logic here
    safe_subpath = sanitize_filename(subpath)
    real_path = os.path.join("writeups", safe_subpath)

    if not os.path.exists(real_path):
        return render_template("error.html", error="Path doesnt exist"), 404

    if os.path.isdir(real_path):
        # list available files and folders
        files = list()
        folders = list()

        for item in os.listdir(real_path):
            item_path = os.path.join(real_path, item)
            if os.path.isdir(item_path): folders.append(item)
            else: files.append(item)

        return render_template("structure.html", files=files, folders=folders)
    
    elif os.path.isfile(real_path) and real_path.endswith(".md"):
        article = renderarticle(real_path)
        return render_template("markdown.html", content=article)
    elif os.path.isfile(real_path):
        return send_file(real_path)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

# error handling, also stolen from my blog site
@app.errorhandler(Exception)
def page_not_found(e):
    if isinstance(e, HTTPException):
        return render_template('error.html', error=e), e.code
    return render_template("error.html", error="Something broke, max is on it"), 500

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)