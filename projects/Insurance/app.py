from flask import Flask, render_template, request, redirect, url_for
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.joblib')
model = joblib.load(MODEL_PATH)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction = None
    if request.method == 'POST':
        try:
            # Print raw form values
            print('Raw form values:', dict(request.form))
            age_raw = request.form['age']
            sex_raw = request.form['sex']
            bmi_raw = request.form['bmi']
            children_raw = request.form['children']
            smoker_raw = request.form['smoker']
            # Convert values
            age = float(age_raw)
            sex = int(sex_raw)
            bmi = float(bmi_raw)
            children = int(children_raw)
            smoker = int(smoker_raw)
            region = 0  # Default to Southwest
            print(f"Converted values - Age: {age}, Sex: {sex}, BMI: {bmi}, Children: {children}, Smoker: {smoker}, Region: {region} (default)")
            features = np.array([[age, sex, bmi, children, smoker, region]])
            prediction = model.predict(features)[0]
            prediction = f"{prediction:.2f}"
        except Exception as e:
            prediction = f"Error: {e}"
    return render_template('predict.html', prediction=prediction)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
