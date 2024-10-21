import requests
import json

def emotion_detector(text_to_analyze):
    """Analyzes sentiment of the given text using an external API.
    Args: text_to_analyze (str): The text to be analyzed for sentiment.
    Returns: a tuple containing a dictionary with emotion scores and the dominant emotion, and the status code
    """
    if not text_to_analyze:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }, 400

    # Define the URL for the sentiment analysis API
    url = 'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict'

    # Create the payload with the text to be analyzed
    payload = { "raw_document": { "text": text_to_analyze } }

    # Set the headers with the required model for the API
    headers = {
        "grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Convert the response text into a dictionary
    response_dict = json.loads(response.text)

    # Extract the required set of emotions and their scores
    sentiment_mentions = response_dict.get('documentSentiment', {}).get('sentimentMentions', [])
    if sentiment_mentions:
        emotions = sentiment_mentions[0].get('sentimentprob', {})
        anger_score = emotions.get('negative', 0)
        disgust_score = emotions.get('negative', 0)  # Assuming disgust is part of negative
        fear_score = emotions.get('negative', 0)  # Assuming fear is part of negative
        joy_score = emotions.get('positive', 0)
        sadness_score = emotions.get('negative', 0)  # Assuming sadness is part of negative
    else:
        anger_score = disgust_score = fear_score = joy_score = sadness_score = 0

    # Find the dominant emotion
    emotion_scores = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    # Return the formatted output
    return {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }, 200