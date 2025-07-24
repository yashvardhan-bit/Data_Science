from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session
model = joblib.load('model.joblib')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/history')
def history():
    history = session.get('history', [])
    return render_template('history.html', history=history)

@app.route('/predict', methods=['POST'])
def predict():
    features = [float(x) for x in request.form.values()]
    prediction = model.predict([features])[0]
    # Save to session history
    history = session.get('history', [])
    history.append({'input': features, 'prediction': int(prediction)})
    session['history'] = history
    return render_template('index.html', prediction_text=f'Prediction: {prediction}')

if __name__ == '__main__':
    app.run(debug=True)