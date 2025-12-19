from flask import Flask, render_template, request
import re
from collections import Counter

app = Flask(__name__)

POSITIVE_WORDS = {
    "good", "great", "awesome", "nice", "love", "excellent",
    "amazing", "cool", "smooth", "perfect", "happy", "fast"
}

NEGATIVE_WORDS = {
    "bad", "worst", "slow", "boring", "hate", "confusing",
    "buggy", "lag", "crash", "poor", "terrible", "annoying"
}

STOPWORDS = {
    "the", "is", "and", "it", "this", "that", "to", "for",
    "of", "on", "in", "just", "very", "really"
}


@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    confidence = None
    words = []

    if request.method == "POST":
        text = request.form.get("feedback", "").lower()

        tokens = re.findall(r"[a-zA-Z]{3,}", text)
        tokens = [w for w in tokens if w not in STOPWORDS]

        score = 0
        matched = 0

        for w in tokens:
            if w in POSITIVE_WORDS:
                score += 1
                matched += 1
            elif w in NEGATIVE_WORDS:
                score -= 1
                matched += 1

        # 🔥 FIXED SENTIMENT LOGIC
        if matched == 1:
            sentiment = "Positive" if score > 0 else "Negative"
            confidence = 70
        elif matched > 1:
            if score > 0:
                sentiment = "Positive"
            elif score < 0:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
            confidence = min(95, 50 + matched * 10)
        else:
            sentiment = "Neutral"
            confidence = 40

        words = Counter(tokens).most_common(15)

    return render_template(
        "index.html",
        sentiment=sentiment,
        confidence=confidence,
        words=words
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
