import pandas as pd
from flask import Flask, render_template, request
import joblib
import os

app = Flask(__name__)
model = joblib.load(os.path.join(os.path.dirname(__file__), 'model.joblib'))

# Dictionaries for feature encoding
brand_dict = {'ASUS': 1, 'Lenovo': 2, 'acer': 3, 'Avita': 4, 'HP': 5, 'DELL': 6, 'MSI': 7, 'APPLE': 8}
processor_brand_dict = {'Intel': 1, 'AMD': 2, 'M1': 3}
processor_name_dict = {'Core i3': 1, 'Core i5': 2, 'Celeron Dual': 3, 'Ryzen 5': 4, 'Core i7': 5, 'Core i9': 6, 'M1': 7, 'Pentium Quad': 8, 'Ryzen 3': 9, 'Ryzen 7': 10, 'Ryzen 9': 11}
processor_gnrtn_dict = {'10th': 5, 'Not Available': 0, '11th': 6, '7th': 2, '8th': 3, '9th': 4, '4th': 1, '12th': 7}
ram_type_dict = {'DDR4': 3, 'LPDDR4': 4, 'LPDDR4X': 5, 'DDR5': 6, 'DDR3': 1, 'LPDDR3': 2}
os_dict = {'Windows': 1, 'DOS': 2, 'Mac': 3}
os_bit_dict = {'64': 1, '32': 2}
touchscreen_dict = {'Yes': 1, 'No': 0}
msoffice_dict = {'Yes': 1, 'No': 0}
warranty_dict = {'1 Year': 1, '2 Year': 2, '3 Year': 3, 'No Warranty': 0}

search_history = []

def extract_number(val):
    """Extract numeric value from storage strings"""
    if isinstance(val, str):
        val = val.replace('GB', '').replace('gb', '').replace('TB', '').replace('tb', '').replace(' ', '').replace('MB', '').replace('mb', '')
    return float(val) if val else 0

def log_prediction(data, prediction):
    """Log prediction details to terminal"""
    print(f"\n{'='*60}")
    print("💻 LAPTOP PREDICTION REQUEST")
    print(f"{'='*60}")
    print(f"🏷️  Brand: {data['brand']}")
    print(f"🔧 Processor: {data['processor_brand']} {data['processor_name']} ({data['processor_gnrtn']})")
    print(f"💾 RAM: {data['ram_gb']} {data['ram_type']}")
    print(f"💿 Storage: SSD {data['ssd']}, HDD {data['hdd']}")
    print(f"🖥️  OS: {data['os']} {data['os_bit']}-bit")
    print(f"🎮 Graphics: {data['graphic_card_gb']}")
    print(f"👆 Touchscreen: {data['Touchscreen']}")
    print(f"📄 MS Office: {data['msoffice']}")
    print(f"🛡️  Warranty: {data['warranty']}")
    print(f"{'-'*60}")
    print(f"💰 Predicted Price: ₹{prediction:,.2f}")
    print(f"{'='*60}")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/project', methods=["POST", "GET"])
def predict():
    if request.method == 'POST':
        try:
            # Get form data
            data = {
                'brand': request.form['brand'],
                'processor_brand': request.form['processor_brand'],
                'processor_name': request.form['processor_name'],
                'processor_gnrtn': request.form['processor_gnrtn'],
                'ram_gb': request.form['ram_gb'],
                'ram_type': request.form['ram_type'],
                'ssd': request.form['ssd'],
                'hdd': request.form['hdd'],
                'os': request.form['os'],
                'os_bit': request.form['os_bit'],
                'graphic_card_gb': request.form['graphic_card_gb'],
                'Touchscreen': request.form['Touchscreen'],
                'msoffice': request.form['msoffice'],
                'warranty': request.form['warranty']
            }

            # Encode categorical features
            features = [
                brand_dict.get(data['brand'], 0),
                processor_brand_dict.get(data['processor_brand'], 0),
                processor_name_dict.get(data['processor_name'], 0),
                processor_gnrtn_dict.get(data['processor_gnrtn'], 0),
                extract_number(data['ram_gb']),
                extract_number(data['ssd']),
                extract_number(data['hdd']),
                os_dict.get(data['os'], 0),
                extract_number(data['graphic_card_gb']),
                touchscreen_dict.get(data['Touchscreen'], 0),
                warranty_dict.get(data['warranty'], 0)
            ]

            # Make prediction
            prediction = model.predict([features])[0]
            rounded_prediction = round(prediction, 2)

            # Log to terminal
            log_prediction(data, rounded_prediction)

            # Add to search history
            search_history.append({
                **data,
                'prediction': rounded_prediction
            })

            return render_template('project.html', 
                                 prediction=rounded_prediction,
                                 **data)

        except Exception as e:
            print(f"❌ Error during prediction: {str(e)}")
            return render_template('project.html', error="An error occurred during prediction")

    return render_template('project.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"📧 Contact Form - Name: {name}, Email: {email}, Message: {message}")
    return render_template('contact.html')

@app.route('/history')
def history():
    return render_template('history.html', history=search_history)

if __name__ == '__main__':
    print("💻 Starting Laptop Price Predictor...")
    print("📱 Web interface: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)