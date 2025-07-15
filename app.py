# app.py
from flask import Flask, render_template, request
from get_comments import get_comments
from sentiment_analysis import analyze_sentiment
import pandas as pd

app = Flask(__name__)

# Your API key here
API_KEY = "AIzaSyD_vPttiitar0aWuw551MTu3RPHgNJOkmY"

@app.route('/', methods=['GET', 'POST'])
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    video_url = request.form['video_url']
    comments = get_comments(video_url, API_KEY)
    result = [(c, analyze_sentiment(c)) for c in comments]
    summary = {'Positive': 0, 'Neutral': 0, 'Negative': 0}

    for _, sentiment in result:
        summary[sentiment] += 1

    comment_objs = [{'text': c, 'sentiment': s} for c, s in result]

    return render_template('result.html', comments=comment_objs, summary=summary)


if __name__ == '__main__':
    app.run(debug=True)
