import requests
import json  # Import json to handle response conversion

def emotion_detector(text_to_analyze):
    """Analyzes sentiment of the given text using an external API.

    Args:
        text_to_analyze (str): The text to be analyzed for sentiment.

    Returns:
        dict: A dictionary containing the emotion scores and the dominant emotion.
    """
    # Define the URL for the sentiment analysis API
    url = 'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict'

    # Create the payload with the text to be analyzed
    payload = { "raw_document": { "text": text_to_analyze } }

    # Set the headers with the required model ID for the API
    headers = {
        "grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"
    }

    try:
        # Make the POST request to the API
        response = requests.post(url, json=payload, headers=headers)

        # Check if the response status is OK (200)
        if response.status_code == 200:
            # Convert the response text to a dictionary
            response_dict = response.json()
            print("API Response:", response_dict)  # Print the full response to inspect its structure

            # Try to extract emotions if available
            if 'emotionPredictions' in response_dict:
                emotions = response_dict['emotionPredictions']
                emotion_scores = {
                    'anger': emotions['anger'],
                    'disgust': emotions['disgust'],
                    'fear': emotions['fear'],
                    'joy': emotions['joy'],
                    'sadness': emotions['sadness']
                }

                # Find the dominant emotion
                dominant_emotion = max(emotion_scores, key=emotion_scores.get)
                emotion_scores['dominant_emotion'] = dominant_emotion

            else:
                # If the expected key is missing, return the whole response for debugging
                emotion_scores = {'error': 'emotionPredictions key not found', 'response': response_dict}

        else:
            # If the response is not successful, return an error message
            emotion_scores = {'error': 'API request failed with status code ' + str(response.status_code)}

    except requests.exceptions.RequestException as e:
        # Handle exceptions like network issues
        emotion_scores = {'error': str(e)}

    # Return the formatted dictionary with emotion scores and dominant emotion
    return emotion_scores
