from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from gtts import gTTS

import os
import time

app = Flask(__name__)

def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    filename = "speech.mp3"
    tts.save(filename)
    return filename

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        lang = request.form["lang"]
        speech_file = text_to_speech(text, lang)
        audio_url = url_for('download_file', filename=speech_file) + "?t=" + str(int(time.time()))
        return render_template("index.html", audio_url=audio_url)
    return render_template("index.html", audio_url=None)

@app.route("/<filename>")
def download_file(filename):
    return send_from_directory(".", filename)

if __name__ == "__main__":
    app.run(debug=True)