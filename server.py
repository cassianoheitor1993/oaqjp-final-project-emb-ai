"""
This module implements a Flask web application for sentiment analysis
using a specified API for text processing.
"""

from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

@app.route('/emotionDetector', methods=['GET'])
def sent_analyzer():
    """Analyze the sentiment of the text provided in the request."""
    text_to_analyze = request.args.get('textToAnalyze')
    if not text_to_analyze:
        return "Invalid input! Try again.", 400

    try:
        response = emotion_detector(text_to_analyze)
        anger = response['anger']
        disgust = response['disgust']
        fear = response['fear']
        joy = response['joy']
        sadness = response['sadness']
        dominant_emotion = response['dominant_emotion']

        formatted_response = (
            f"For the given statement, the system response is 'anger': {anger}, "
            f"'disgust': {disgust}, 'fear': {fear}, 'joy': {joy} and 'sadness': {sadness}. "
            f"The dominant emotion is {dominant_emotion}."
        )
        return formatted_response
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route("/")
def render_index_page():
    """Render the index HTML page."""
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)