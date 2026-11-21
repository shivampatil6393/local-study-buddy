
from flask import Flask, request, jsonify, render_template
from pathlib import Path
import requests
import io

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:3b"

syllabus = ""

buddy_state = {
    "face": "happy",
    "message": "Ready to study!",
    "progress": 0,
    "vibrate": False
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/status")
def status():
    return jsonify({
        "server": "online",
        "model": MODEL,
        "buddy": buddy_state
    })


@app.route("/api/esp32/status")
def esp32_status():
    global buddy_state

    data = dict(buddy_state)
    buddy_state["vibrate"] = False

    return jsonify(data)


@app.route("/api/syllabus", methods=["POST"])
def upload_syllabus():
    global syllabus

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = file.filename.lower()

    try:
        if filename.endswith(".txt"):
            syllabus = file.read().decode("utf-8")

        elif filename.endswith(".pdf"):
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file.read()))
            syllabus = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

        else:
            return jsonify({
                "error": "Upload PDF or TXT only"
            }), 400

        buddy_state.update({
            "face": "happy",
            "message": "Syllabus loaded!",
            "vibrate": True
        })

        return jsonify({
            "message": "Syllabus uploaded successfully",
            "characters": len(syllabus)
        })

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}

    question = data.get("message", "").strip()
    topic = data.get("topic", "General Study")

    if not question:
        return jsonify({"error": "Enter a question"}), 400

    buddy_state.update({
        "face": "thinking",
        "message": "Thinking..."
    })

    prompt = f"""
You are a friendly AI study buddy.

Teach the student step by step.
Use simple language.
Explain difficult concepts with examples.
Help solve programming and mathematics problems.

Student syllabus:
{syllabus[:30000]}

Current topic: {topic}

Student question:
{question}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False
            },
            timeout=180
        )

        response.raise_for_status()

        answer = response.json()["message"]["content"]

        buddy_state.update({
            "face": "happy",
            "message": "Here's your answer!",
            "vibrate": True
        })

        return jsonify({
            "answer": answer,
            "model": MODEL
        })

    except requests.RequestException as error:
        buddy_state.update({
            "face": "sad",
            "message": "AI connection failed"
        })

        return jsonify({
            "error": str(error)
        }), 503


@app.route("/api/progress", methods=["POST"])
def update_progress():
    data = request.get_json(silent=True) or {}

    try:
        progress = max(
            0,
            min(100, int(data.get("progress", 0)))
        )
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid progress"}), 400

    buddy_state["progress"] = progress

    return jsonify({
        "progress": progress
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
