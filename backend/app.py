# app.py
from flask import Flask, request, jsonify, render_template
from scoring import RubricScorer
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# Load rubric
RUBRIC_PATH = os.environ.get("RUBRIC_PATH", "rubric.csv")
scorer = RubricScorer(rubric_path=RUBRIC_PATH)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/score", methods=["POST"])
def score():
    payload = request.json or {}
    transcript = payload.get("transcript", "")
    duration_sec = payload.get("duration_sec", None)
    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400

    result = scorer.score_transcript(transcript, duration_sec=duration_sec)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
