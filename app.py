from flask import Flask, render_template, request
import re
from collections import Counter

app = Flask(__name__)

# Store past feedback to detect repetition
seen_feedback = set()

# Casual + real-world sentiment words
POSITIVE_WORDS = {
    "love", "loved", "awesome", "great", "good", "nice", "clean",
    "amazing", "cool", "slaps", "smooth", "fast", "excellent"
}

NEGATIVE_WORDS = {
    "hate", "slow", "lag", "laggy", "bug", "buggy", "bad", "worst",
    "annoying", "meh", "crash", "crashes", "issue", "issues"
}

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    confidence = None
    keywords = []
    warning = None

    if request.method == "POST":
        text = request.form.get("feedback", "")

        # 🛑 1. Empty / whitespace check
        if not text.strip():
            warning = "Please enter meaningful feedback (not empty input)."
            return render_template("index.html", warning=warning)

        clean_text = text.lower().strip()

        # 🔁 2. Repeated feedback detection
        if clean_text in seen_feedback:
            warning = "⚠ This feedback was already analyzed earlier."
        else:
            seen_feedback.add(clean_text)

        words = re.findall(r"\b[a-zA-Z]{2,}\b", clean_text)

        pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
        neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)

        total_signal = pos_count + neg_count

        # 🧠 3. Sentiment logic
        if total_signal == 0:
            sentiment = "Neutral"
            confidence = 40
        elif pos_count > neg_count:
            sentiment = "Positive"
            confidence = min(90, 50 + pos_count * 10)
        elif neg_count > pos_count:
            sentiment = "Negative"
            confidence = min(90, 50 + neg_count * 10)
        else:
            sentiment = "Neutral"
            confidence = 50

        # 🏷 4. Keyword extraction (top casual words)
        keywords = Counter(words).most_common(8)

    return render_template(
        "index.html",
        sentiment=sentiment,
        confidence=confidence,
        keywords=keywords,
        warning=warning
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
