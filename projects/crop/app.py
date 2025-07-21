from flask import Flask, render_template, request, redirect, url_for, flash, session
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'crop_recommendation_secret_key'

# Load the trained model
model = joblib.load('model.joblib')

# Crop mapping dictionary
crop_dict = {
    1: 'rice', 2: 'maize', 3: 'jute', 4: 'cotton', 5: 'coconut', 6: 'papaya',
    7: 'orange', 8: 'apple', 9: 'muskmelon', 10: 'watermelon', 11: 'grapes',
    12: 'mango', 13: 'banana', 14: 'pomegranate', 15: 'lentil', 16: 'blackgram',
    17: 'mungbean', 18: 'mothbeans', 19: 'pigeonpeas', 20: 'kidneybeans',
    21: 'chickpea', 22: 'coffee'
}

# Initialize history file
HISTORY_FILE = 'prediction_history.txt'

def save_prediction(input_data, prediction):
    """Save prediction to history file (without confidence)"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HISTORY_FILE, 'a') as f:
        f.write(f"{timestamp},{input_data},{prediction}\n")

def load_history():
    """Load prediction history (without confidence)"""
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    history.append({
                        'timestamp': parts[0],
                        'input_data': parts[1],
                        'prediction': parts[2]
                    })
    return history[-10:]  # Return last 10 predictions

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get form data
            n = float(request.form['nitrogen'])
            p = float(request.form['phosphorus'])
            k = float(request.form['potassium'])
            temperature = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            ph = float(request.form['ph'])
            rainfall = float(request.form['rainfall'])
            
            # Validate input ranges
            if not (0 <= n <= 140 and 0 <= p <= 145 and 0 <= k <= 205 and 
                   8 <= temperature <= 44 and 14 <= humidity <= 100 and 
                   3.5 <= ph <= 10 and 20 <= rainfall <= 300):
                flash('Please enter values within valid ranges!', 'error')
                return render_template('index.html')
            
            # Create feature array
            features = np.array([[n, p, k, temperature, humidity, ph, rainfall]])

            # Print input data to backend terminal
            print(f"Received input for prediction: N={n}, P={p}, K={k}, Temp={temperature}, Humidity={humidity}, pH={ph}, Rainfall={rainfall}")
            
            # Make prediction
            prediction = model.predict(features)[0]
            predicted_crop = crop_dict.get(int(prediction), 'Unknown')

            # Save prediction (remove confidence)
            input_data = f"N:{n}, P:{p}, K:{k}, Temp:{temperature}, Humidity:{humidity}, pH:{ph}, Rainfall:{rainfall}"
            save_prediction(input_data, predicted_crop)

            return render_template('index.html', 
                                prediction=predicted_crop, 
                                input_data={
                                    'nitrogen': n, 'phosphorus': p, 'potassium': k,
                                    'temperature': temperature, 'humidity': humidity,
                                    'ph': ph, 'rainfall': rainfall
                                })
        
        except ValueError:
            flash('Please enter valid numeric values!', 'error')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
    
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/history')
def history():
    predictions = load_history()
    return render_template('history.html', predictions=predictions)

@app.route('/project')
def project():
    return render_template('project.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
