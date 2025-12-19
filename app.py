import os
import re
from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    score = 0
    keywords = []

    if request.method == "POST":
        text = request.form.get("feedback", "").lower()

        # Casual + real-world words (NOT academic)
        positive_words = [
            "good", "nice", "love", "awesome", "great", "fun", "cool",
            "fast", "smooth", "easy", "happy", "amazing", "enjoyed"
        ]
        negative_words = [
            "bad", "hate", "worst", "boring", "slow", "buggy", "confusing",
            "annoying", "terrible", "lag", "crash", "problem"
        ]

        for word in positive_words:
            if word in text:
                score += 1

        for word in negative_words:
            if word in text:
                score -= 1

        if score > 0:
            sentiment = "Positive 😊"
        elif score < 0:
            sentiment = "Negative 😠"
        else:
            sentiment = "Neutral 😐"

        # Extract meaningful keywords (unstructured)
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text)
        keywords = Counter(words).most_common(8)

    return render_template(
        "index.html",
        sentiment=sentiment,
        score=score,
        keywords=keywords
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
