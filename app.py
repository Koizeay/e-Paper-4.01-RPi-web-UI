from flask import Flask, render_template, request, redirect, url_for
import os
import time
import shutil

app = Flask(__name__)

IMAGE_DIR = "./images/"
DISPLAY_SCRIPT = "./display.py"

os.makedirs(IMAGE_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/manage")
def manage():
    images = [f for f in os.listdir(IMAGE_DIR) if f.endswith(".bmp")]
    images.sort(key=lambda x: x.lower())
    images = [x for x in images if x != "_.bmp"]
    return render_template("manage.html", images=images)

@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return "No file part", 400

    file = request.files["image"]
    if file.filename == "":
        return "No selected file", 400

    if not file.filename.endswith(".bmp"):
        return "Invalid file format", 400

    filename = os.path.splitext(file.filename)[0]

    if "/" in filename or "\\" in filename or "'" in filename or '"' in filename:
        return "Invalid filename", 400

    new_filename = f"{filename}-{int(time.time())}.bmp"
    file_path = os.path.join(IMAGE_DIR, new_filename)

    if os.path.exists(file_path):
        return "File already exists", 409

    file.save(file_path)
    return redirect(url_for("index"))

@app.route("/display")
def display():
    filename = request.args.get("filename")
    file_path = os.path.join(IMAGE_DIR, filename)

    if "/" in filename or "\\" in filename or "'" in filename or '"' in filename:
        return "Invalid filename", 400

    if not os.path.exists(file_path):
        return "File not found", 404

    if not filename.endswith(".bmp"):
        return "Invalid file format", 400

    if os.path.exists(os.path.join(IMAGE_DIR, "_.bmp")):
        os.remove(os.path.join(IMAGE_DIR, "_.bmp"))

    new_filename = "_.bmp"
    new_file_path = os.path.join(IMAGE_DIR, new_filename)
    shutil.copy(file_path, new_file_path)

    if os.name == "posix":
        try:
            os.system(f"python3 {DISPLAY_SCRIPT} &")
        except Exception as e:
            return str(e), 500
    else:
        print("Windows not supported")
        return "Windows not supported", 500

    return "Ok", 200

@app.route("/manage/delete", methods=["POST"])
def delete():
    filename = request.form.get("filename")
    file_path = os.path.join(IMAGE_DIR, filename)

    if filename == "_.bmp":
        return "Cannot delete currently displayed image", 400

    if "/" in filename or "\\" in filename or "'" in filename or '"' in filename:
        return "Invalid filename", 400

    if not os.path.exists(file_path):
        return "File not found", 404

    try:
        os.remove(file_path)
        return "Deleted", 200
    except Exception as e:
        return str(e), 500

@app.route("/manage/rename", methods=["POST"])
def rename():
    old_name = request.form.get("filename")
    new_name = request.form.get("newname")

    if "/" in new_name or "\\" in new_name or "'" in new_name or '"' in new_name:
        return "Invalid new name", 400

    old_path = os.path.join(IMAGE_DIR, old_name)
    new_path = os.path.join(IMAGE_DIR, new_name)

    if not os.path.exists(old_path):
        return "File not found", 404

    if os.path.exists(new_path):
        return "File with new name already exists", 409

    try:
        os.rename(old_path, new_path)
        return "Renamed", 200
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
