from flask import Flask, render_template, request
import re
from collections import Counter

app = Flask(__name__)

# Simple in-memory cache (faculty idea)
processed_feedback = {}

positive_words = [
    "good", "excellent", "nice", "helpful", "clean", "great", "easy", "useful"
]

negative_words = [
    "bad", "poor", "declined", "dirty", "slow", "worst", "problem", "issue"
]

def analyze_sentiment(text):
    score = 0
    for w in positive_words:
        if w in text:
            score += 1
    for w in negative_words:
        if w in text:
            score -= 1

    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stopwords = {"this", "that", "with", "from", "have", "has", "been", "very"}
    words = [w for w in words if w not in stopwords]
    return Counter(words).most_common(8)

def suggest_action(keywords):
    topics = [word for word, _ in keywords]

    if any(w in topics for w in ["food", "cafeteria", "canteen"]):
        return "Recommend cafeteria quality inspection."
    elif any(w in topics for w in ["library", "books", "study"]):
        return "Consider upgrading library resources."
    elif any(w in topics for w in ["wifi", "internet", "network"]):
        return "IT infrastructure review suggested."
    elif any(w in topics for w in ["faculty", "teacher", "lecture"]):
        return "Academic quality review recommended."
    else:
        return "General feedback detected. Monitor trends."

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    keywords = []
    action = None
    confidence = None
    reused = False

    if request.method == "POST":
        feedback = request.form.get("feedback", "").strip().lower()

        if feedback in processed_feedback:
            # reuse previous analysis
            reused = True
            sentiment, keywords, action, confidence = processed_feedback[feedback]
        else:
            sentiment = analyze_sentiment(feedback)
            keywords = extract_keywords(feedback)
            action = suggest_action(keywords)
            confidence = min(95, 50 + len(keywords) * 5)

            processed_feedback[feedback] = (
                sentiment, keywords, action, confidence
            )

    return render_template(
        "index.html",
        sentiment=sentiment,
        keywords=keywords,
        action=action,
        confidence=confidence,
        reused=reused
    )

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="127.0.0.1", port=5000, debug=True)
