from flask import Flask, render_template, request, session
import joblib
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
model = joblib.load(os.path.join(os.path.dirname(__file__), 'model.joblib'))

def validate_input(age, sex, bmi, children, smoker):
    errors = []
    if not age or age < 18 or age > 100: errors.append("Age must be between 18 and 100 years")
    if sex not in [0, 1]: errors.append("Please select a valid gender")
    if not bmi or bmi < 10 or bmi > 50: errors.append("BMI must be between 10 and 50")
    if children is None or children < 0 or children > 10: errors.append("Number of children must be between 0 and 10")
    if smoker not in [0, 1]: errors.append("Please select a valid smoking status")
    return errors

def log_prediction(source, age, sex, bmi, children, smoker, prediction_inr, prediction_usd):
    print(f"\n{'='*60}\n📊 {source} PREDICTION REQUEST\n{'='*60}")
    print(f"👤 Age: {age}\n👥 Gender: {'Male' if sex == 1 else 'Female'}\n⚖️  BMI: {bmi}\n👶 Children: {children}")
    print(f"🚬 Smoking: {'Yes' if smoker == 1 else 'No'}\n🌍 Region: Southwest (default)\n{'-'*60}")
    print(f"💰 Prediction: ₹{prediction_inr:.2f} (${prediction_usd:.2f})\n{'='*60}")

def log_error(source, message):
    print(f"\n{'='*60}\n❌ {source} ERROR\n{'='*60}\n{message}\n{'='*60}")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction = None
    error_message = None
    form_data = {}
    
    if request.method == 'POST':
        try:
            data = {k: request.form.get(k, '').strip() for k in ['age', 'sex', 'bmi', 'children', 'smoker']}
            form_data = data.copy()
            
            if not all(data.values()):
                error_message = "Please fill in all fields"
                log_error("WEB PREDICTION", "Missing required fields")
            else:
                try:
                    age, sex, bmi, children, smoker = float(data['age']), int(data['sex']), float(data['bmi']), int(data['children']), int(data['smoker'])
                    errors = validate_input(age, sex, bmi, children, smoker)
                    
                    if errors:
                        error_message = "; ".join(errors)
                        log_error("WEB PREDICTION", f"Validation errors:\n" + "\n".join(f"  • {e}" for e in errors))
                    else:
                        features = np.array([[age, sex, bmi, children, smoker, 0]])
                        prediction_usd = model.predict(features)[0]
                        prediction_inr = prediction_usd * 83
                        prediction = f"{prediction_inr:.2f}"
                        
                        log_prediction("WEB", age, sex, bmi, children, smoker, prediction_inr, prediction_usd)
                        session['last_prediction'] = prediction
                        session['last_form_data'] = form_data
                        
                except ValueError:
                    error_message = "Please enter valid numbers for age, BMI, and children"
                    log_error("WEB PREDICTION", "Invalid number format")
                    
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            log_error("WEB PREDICTION", f"Exception: {str(e)}")
    
    return render_template('predict.html', prediction=prediction, error=error_message, form_data=form_data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json()
        if not data: return {'error': 'No data provided'}, 400
        
        age, sex, bmi, children, smoker = data.get('age'), data.get('sex'), data.get('bmi'), data.get('children'), data.get('smoker')
        
        if any(v is None for v in [age, sex, bmi, children, smoker]): return {'error': 'Missing required fields'}, 400
        
        errors = validate_input(age, sex, bmi, children, smoker)
        if errors: return {'error': '; '.join(errors)}, 400
        
        features = np.array([[age, sex, bmi, children, smoker, 0]])
        prediction_usd = model.predict(features)[0]
        prediction_inr = prediction_usd * 83
        
        log_prediction("API", age, sex, bmi, children, smoker, prediction_inr, prediction_usd)
        return {'prediction': round(prediction_inr, 2), 'currency': 'INR', 'confidence': 'high'}
        
    except Exception as e:
        return {'error': f'Prediction failed: {str(e)}'}, 500

def terminal_predict():
    print(f"\n{'='*50}\n🏥 INSURANCE COST PREDICTOR - TERMINAL MODE\n{'='*50}")
    
    try:
        print("\n📋 Please enter your details:")
        age = float(input("Age (18-100): "))
        print("Gender: 0 for Female, 1 for Male")
        sex = int(input("Gender (0/1): "))
        bmi = float(input("BMI (10-50): "))
        children = int(input("Number of children (0-10): "))
        print("Smoking: 0 for Non-smoker, 1 for Smoker")
        smoker = int(input("Smoking status (0/1): "))
        
        errors = validate_input(age, sex, bmi, children, smoker)
        if errors:
            log_error("TERMINAL PREDICTION", f"Validation errors:\n" + "\n".join(f"  • {e}" for e in errors))
            return
        
        features = np.array([[age, sex, bmi, children, smoker, 0]])
        prediction_usd = model.predict(features)[0]
        prediction_inr = prediction_usd * 83
        
        log_prediction("TERMINAL", age, sex, bmi, children, smoker, prediction_inr, prediction_usd)
        
    except ValueError:
        log_error("TERMINAL PREDICTION", "Please enter valid numbers")
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        log_error("TERMINAL PREDICTION", f"Error: {str(e)}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--terminal':
        terminal_predict()
    else:
        print("🌐 Starting web server...\n📱 Web interface: http://127.0.0.1:5000\n💻 Terminal mode: python app.py --terminal")
        app.run(debug=True, host='0.0.0.0', port=5000)
