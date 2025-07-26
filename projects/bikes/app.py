from flask import Flask, render_template, request
import joblib
import os

app = Flask(__name__)
model = joblib.load(os.path.join(os.path.dirname(__file__), 'model.joblib'))

brand_dict = {
    'TVS': 1, 'Royal Enfield': 2, 'Triumph': 3, 'Yamaha': 4, 'Honda': 5,
    'Hero': 6, 'Bajaj': 7, 'Suzuki': 8, 'Benelli': 9, 'KTM': 10,
    'Mahindra': 11, 'Kawasaki': 12, 'Ducati': 13, 'Hyosung': 14,
    'Harley-Davidson': 15, 'Jawa': 16, 'BMW': 17, 'Indian': 18,
    'Rajdoot': 19, 'LML': 20, 'Yezdi': 21, 'MV': 22, 'Ideal': 23
}

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/project', methods=["POST", "GET"])
def predict():
    if request.method == 'POST':
        try:
            brand_name = request.form['brand_name']
            owner = int(request.form['owner'])
            age = int(request.form['age'])
            power = int(request.form['power'])
            kms_driven = int(request.form['kms_driven'])
            
            if brand_name not in brand_dict:
                return render_template('project.html', error="Invalid brand selected")
            
            brand_code = brand_dict[brand_name]
            print(f"Input Data: Brand={brand_name}({brand_code}), Owner={owner}, Age={age}, Power={power}, KMs={kms_driven}")
            
            features = [[brand_code, owner, age, power, kms_driven]]
            prediction = model.predict(features)
            rounded_prediction = round(prediction[0], 2)
            
            print(f"Predicted Price: ₹{rounded_prediction}")
            
            return render_template('project.html', 
                                 prediction=rounded_prediction,
                                 brand_name=brand_name,
                                 owner=owner,
                                 age=age,
                                 power=power,
                                 kms_driven=kms_driven)
        except ValueError:
            return render_template('project.html', error="Please enter valid numbers")
        except Exception as e:
            print(f"Error: {str(e)}")
            return render_template('project.html', error="An error occurred during prediction")
    
    return render_template('project.html')

if __name__ == "__main__":
    print("🚲 Starting Bike Price Predictor...")
    print("📱 Web interface: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)