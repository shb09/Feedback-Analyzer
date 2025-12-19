from flask import Flask, render_template, request
import re
from collections import Counter
import os

app = Flask(__name__)

# Memory for repeated feedback detection
seen_feedback = set()

# Casual sentiment words
POSITIVE_WORDS = {
    "love", "loved", "awesome", "great", "good", "nice",
    "amazing", "cool", "slaps", "smooth", "fast", "clean"
}

NEGATIVE_WORDS = {
    "hate", "slow", "lag", "laggy", "bug", "buggy", "bad",
    "worst", "annoying", "meh", "crash", "crashes", "issue"
}

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    confidence = None
    wordcloud_data = []
    warning = None
    repeated = False

    if request.method == "POST":
        text = request.form.get("feedback", "")

        # 1️⃣ Empty input handling
        if not text.strip():
            warning = "⚠ Please enter meaningful feedback (not empty input)."
            return render_template("index.html", warning=warning)

        clean_text = text.lower().strip()

        # 2️⃣ Repeated feedback detection
        if clean_text in seen_feedback:
            repeated = True
        else:
            seen_feedback.add(clean_text)

        # Tokenization
        words = re.findall(r"\b[a-zA-Z]{2,}\b", clean_text)

        pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
        neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)
        signal = pos_count + neg_count

        # 3️⃣ Sentiment + confidence logic
        if signal == 0:
            sentiment = "Neutral 😐"
            confidence = 40
        elif pos_count > neg_count:
            sentiment = "Positive 😊"
            confidence = min(90, 50 + pos_count * 10)
        elif neg_count > pos_count:
            sentiment = "Negative 😠"
            confidence = min(90, 50 + neg_count * 10)
        else:
            sentiment = "Neutral 😐"
            confidence = 50

        # 4️⃣ Word cloud data
        wordcloud_data = Counter(words).most_common(12)

    return render_template(
        "index.html",
        sentiment=sentiment,
        confidence=confidence,
        wordcloud_data=wordcloud_data,
        warning=warning,
        repeated=repeated
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
