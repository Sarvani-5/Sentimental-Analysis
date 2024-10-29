from flask import Flask, request, jsonify
import joblib

# Load the trained model and vectorizer
model = joblib.load('model_lr.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Sentiment mapping dictionary
sentiment_mapping = {0: "Negative", 2: "Positive"}

# Initialize Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text', '')
    
    # Transform text input to vector
    text_vector = vectorizer.transform([text])
    
    # Predict probabilities
    probabilities = model.predict_proba(text_vector)[0]
    
    # Determine sentiment based on probabilities
    if abs(probabilities[1] - probabilities[0]) < 0.15:  # Threshold for Neutral
        sentiment = "Neutral"
    else:
        sentiment = sentiment_mapping[model.predict(text_vector)[0]]
    
    # Prepare output
    result = {
        'sentiment': sentiment,
        'positive_probability': probabilities[1],
        'negative_probability': probabilities[0],
        'neutral_threshold_applied': abs(probabilities[1] - probabilities[0]) < 0.15
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
