import os
import logging
from pythonjsonlogger import jsonlogger
from flask import Flask, request, render_template
import joblib
import json
from datetime import datetime

# Logging Configuration
LOG_DIR = '/app/prediction_logs'
APP_LOG_DIR = '/app/logs'
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(APP_LOG_DIR, exist_ok=True)

# Ensure directories have proper permissions
os.chmod(LOG_DIR, 0o777)
os.chmod(APP_LOG_DIR, 0o777)

# Logging Setup
logger = logging.getLogger('sentiment_logger')
logger.setLevel(logging.INFO)

# JSON Formatter that works well with Loggly
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s %(data)s'
)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Application log file - use a fixed filename for easier monitoring
app_log_file = os.path.join(APP_LOG_DIR, 'sentiment.log')
app_file_handler = logging.FileHandler(app_log_file)
app_file_handler.setFormatter(formatter)
logger.addHandler(app_file_handler)

# Prediction log file - use a fixed filename for easier monitoring
prediction_log_file = os.path.join(LOG_DIR, 'sentiment_prediction.jsonl')
prediction_file_handler = logging.FileHandler(prediction_log_file)
prediction_file_handler.setFormatter(formatter)
logger.addHandler(prediction_file_handler)

# Make sure log files exist and have proper permissions
for log_file in [app_log_file, prediction_log_file]:
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write('')
    os.chmod(log_file, 0o666)

# Load the trained model and vectorizer
model = joblib.load('model_lr.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Sentiment mapping dictionary
sentiment_mapping = {0: "Negative", 2: "Positive"}

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    # Log home page access with empty data object for consistent JSON format
    logger.info('Home page accessed', extra={'data': {}})
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the text input from the form
        text = request.form['text']
        
        # Log input text for tracking
        log_data = {
            'input_text': text,
            'input_length': len(text)
        }
        logger.info('Sentiment Prediction Request', extra={'data': log_data})
        
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
            'positive_probability': float(probabilities[1]),
            'negative_probability': float(probabilities[0]),
            'neutral_threshold_applied': str(abs(probabilities[1] - probabilities[0]) < 0.15)
        }
        
        # Log prediction result with comprehensive details
        result_log = {
            'input_text': text,
            'sentiment': sentiment,
            'probabilities': {
                'positive': float(probabilities[1]),
                'negative': float(probabilities[0])
            },
            'full_result': result
        }
        logger.info('Sentiment Prediction Result', extra={'data': result_log})
        
        return render_template('index.html', result=result)

if __name__ == '__main__':
    # Log application startup
    logger.info('Sentiment Analysis Application Started', extra={'data': {}})
    app.run(host='0.0.0.0', port=5000)