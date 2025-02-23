from flask import Flask, render_template, request, url_for
from flask import send_from_directory
from gtts import gTTS
import os
import time

app = Flask(__name__)

# Ensure static directory exists for storing audio files
if not os.path.exists("static"):
    os.makedirs("static")

def text_to_speech(text, lang):
    """Convert text to speech and save the file inside the static directory."""
    tts = gTTS(text=text, lang=lang)
    filename = "speech.mp3"  # Fixed filename to overwrite old audio
    filepath = os.path.join("static", filename)
    tts.save(filepath)
    return filename

@app.route("/", methods=["GET", "POST"])
def index():
    """Handle the home page and text-to-speech conversion."""
    if request.method == "POST":
        text = request.form["text"]
        lang = request.form["lang"]
        speech_file = text_to_speech(text, lang)

        # Serve the audio file correctly from /static/
        audio_url = url_for('static', filename=speech_file, _external=True) + "?t=" + str(int(time.time()))
        return render_template("index.html", audio_url=audio_url)

    return render_template("index.html", audio_url=None)

if __name__ == "__main__":
    app.run(debug=True)
