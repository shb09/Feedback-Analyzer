from flask import Flask, render_template, request, jsonify
import re
from collections import Counter

app = Flask(__name__)

# Expanded casual sentiment words
POSITIVE = {
    "good","great","love","awesome","nice","cool","helpful","amazing",
    "fine","ok","okay","useful","liked","smooth","works","fun"
}

NEGATIVE = {
    "bad","hate","slow","buggy","confusing","empty","meh","boring",
    "annoying","issue","problem","lag","weird","broken","frustrating"
}

STOPWORDS = {
    "the","is","it","this","that","to","and","a","of","for","in","on",
    "but","sometimes","just","feels","idk","why"
}

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def analyze():
    text = request.form.get("text", "").lower()

    if not text.strip():
        return jsonify({
            "sentiment": "Neutral",
            "confidence": 0,
            "wordcloud": []
        })

    words = re.findall(r"[a-z']+", text)

    score = 0
    matched = 0

    for w in words:
        if w in POSITIVE:
            score += 1
            matched += 1
        elif w in NEGATIVE:
            score -= 1
            matched += 1

    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    confidence = min(100, max(30, int((abs(score) / max(1, matched)) * 100)))

    filtered = [w for w in words if w not in STOPWORDS and len(w) > 3]
    counts = Counter(filtered).most_common(20)

    return jsonify({
        "sentiment": sentiment,
        "confidence": confidence,
        "wordcloud": counts
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
