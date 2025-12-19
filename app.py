from flask import Flask, render_template, request
import hashlib
import re
from collections import Counter
import random

app = Flask(__name__)

# Store analyzed feedback (for demo purpose)
analyzed_feedback = set()

positive_words = {
    "good", "great", "love", "awesome", "nice", "amazing",
    "smooth", "fast", "cool", "perfect", "clean", "excellent"
}

negative_words = {
    "bad", "hate", "slow", "lag", "bug", "issue",
    "problem", "worst", "crash", "ruins", "delay", "annoying"
}


def analyze_sentiment(text):
    words = re.findall(r"\b[a-z]+\b", text.lower())

    pos = sum(1 for w in words if w in positive_words)
    neg = sum(1 for w in words if w in negative_words)

    if pos > neg:
        sentiment = "Positive"
    elif neg > pos:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    confidence = min(95, max(40, abs(pos - neg) * 20 + 40))
    return sentiment, confidence, words


def build_wordcloud(words):
    freq = Counter(words).most_common(12)
    colors = ["#7aa2f7", "#9ece6a", "#f7768e", "#e0af68", "#bb9af7"]

    cloud = []
    for word, count in freq:
        cloud.append({
            "word": word,
            "size": min(46, 14 + count * 6),
            "color": random.choice(colors)
        })
    return cloud


@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = confidence = None
    wordcloud = []
    repeated = False
    launched = False

    if request.method == "POST":
        launched = True
        feedback = request.form.get("feedback", "").strip()

        if feedback:
            hash_val = hashlib.md5(feedback.lower().encode()).hexdigest()

            if hash_val in analyzed_feedback:
                repeated = True
                sentiment = "Already Analyzed"
                confidence = 100
            else:
                analyzed_feedback.add(hash_val)
                sentiment, confidence, words = analyze_sentiment(feedback)
                wordcloud = build_wordcloud(words)

    return render_template(
        "index.html",
        sentiment=sentiment,
        confidence=confidence,
        wordcloud=wordcloud,
        repeated=repeated,
        launched=launched
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
