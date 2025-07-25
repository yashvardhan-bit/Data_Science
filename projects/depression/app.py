from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session
model = joblib.load('model.joblib')

# Feature order for the model
FEATURES = [
    'Age', 'Marital Status', 'Education Level', 'Number of Children',
    'Smoking Status', 'Physical Activity Level', 'Employment Status', 'Income',
    'Alcohol Consumption', 'History of Substance Abuse',
    'Family History of Depression', 'Chronic Medical Conditions'
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Contact Form - Name: {name}, Email: {email}, Message: {message}")
    return render_template('contact.html')

@app.route('/project', methods=['GET', 'POST'])
def project():
    prediction = None
    if request.method == 'POST':
        try:
            features = []
            feature_values = {}
            for feat in FEATURES:
                val = request.form.get(feat)
                if val is None or val == '':
                    raise ValueError(f'Missing value for {feat}')
                features.append(float(val))
                feature_values[feat] = val
            print('User submitted values for prediction:')
            for k, v in feature_values.items():
                print(f'  {k}: {v}')
            pred = model.predict([features])[0]
            prediction = 'Yes' if int(pred) == 1 else 'No'
            # Save to session history
            history = session.get('history', [])
            history.append({'input': features, 'prediction': prediction})
            session['history'] = history
        except Exception as e:
            prediction = f'Error: {e}'
    return render_template('project.html', prediction=prediction)

@app.route('/history')
def history():
    history = session.get('history', [])
    return render_template('history.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)