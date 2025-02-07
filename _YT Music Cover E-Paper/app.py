from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import time
import requests

app = Flask(__name__)

# Change this to your display server (RPi) URL
DISPLAY_SERVER_URL = "http://X.X.X.X:8080/"

IMAGE_DIR = "./temp/"
LAST_ID = ""
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.route("/")
def index():
    if request.args.get("id"):
        current_id = request.args.get("id")
        global LAST_ID
        if current_id == LAST_ID:
            return "", 200
        else:
            LAST_ID = current_id
            downloadCoverImage(LAST_ID)
            convertCoverImageToEInk()
            displayCoverImage()
            return "", 200


def downloadCoverImage(youtube_id):
    url = f"https://img.youtube.com/vi/{youtube_id}/maxresdefault.jpg"
    response = requests.get(url)
    if response.status_code != 200:
        return
    with open(f"{IMAGE_DIR}source.jpg", "wb") as f:
        f.write(response.content)


def convertCoverImageToEInk():
    os.system(f"python ./convert.py")

def displayCoverImage():
    upload_url = f"{DISPLAY_SERVER_URL}upload"
    files = {"image": open(f"{IMAGE_DIR}output.bmp", "rb")}
    response = requests.post(upload_url, files=files)
    timestamp = int(time.time())
    if response.status_code != 200:
        print("Failed to upload image")
        return
    display_url = f"{DISPLAY_SERVER_URL}display?filename=output-{timestamp}.bmp"
    response = requests.get(display_url)
    if response.status_code != 200:
        print("Failed to display image")
        print(response.text + " <-> " + display_url)
        return
    delete_url = f"{DISPLAY_SERVER_URL}manage/delete"
    data = {"filename": f"output-{timestamp}.bmp"}
    response = requests.post(delete_url, data=data)
    if response.status_code != 200:
        print("Failed to delete image")
        return

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
