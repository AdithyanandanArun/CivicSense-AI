from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

from db import init_db
from memory import save_message, get_recent_messages
from rag import build_index, query_schemes

load_dotenv()
apikey = os.getenv("groqapi")
client = Groq(api_key=apikey)
app = Flask(__name__)

init_db()
build_index()
@app.route ("/")
def index():
    return render_template("index.html")
@app.route ("/groq", methods=["post"])
def groq():
    user_message = request.json.get("message")
    response = client.chat.completions.create(model="llama-3.3-70b-versatile",messages=[{"role": "system", "content": "You are a assistant."},{"role": "user", "content": user_message}])
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

