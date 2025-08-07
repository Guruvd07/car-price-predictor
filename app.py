from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import pandas as pd
import pickle
import json
import os
from datetime import datetime
import numpy as np
import joblib
from catboost import Pool

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Load the dataset (your original Cars.csv structure)
try:
    df = pd.read_csv('Cars.csv')
    print("✅ Dataset loaded successfully")
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
except:
    print("⚠️ Cars.csv not found, creating sample data")
    df = pd.DataFrame()

# Load ML model
def load_model_files():
    global model, cat_features
    try:
        # Load your trained CatBoost model
        model = joblib.load('car_price_model.pkl')
        print("✅ CatBoost model loaded successfully")
        
        # Define categorical features as per your training
        cat_features = ['Brand_Model', 'Fuel Type', 'Transmission', 'Location']
        print(f"✅ Categorical features: {cat_features}")
        
        return True
    except Exception as e:
        print(f"ERROR loading model: {str(e)}")
        model = None
        cat_features = []
        return False

# Initialize model loading
model_loaded = load_model_files()

# Initialize users.json if it doesn't exist
if not os.path.exists('users.json'):
    with open('users.json', 'w') as f:
        json.dump([], f)

def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listings')
def listings():
    if df.empty:
        return render_template('listings.html', cars=[], brands=[], 
                             search_brand='', search_model='')
    
    search_brand = request.args.get('brand', '').lower()
    search_model = request.args.get('model', '').lower()
    
    filtered_df = df.copy()
    
    if search_brand:
        filtered_df = filtered_df[filtered_df['Brand'].str.lower().str.contains(search_brand, na=False)]
    
    if search_model:
        filtered_df = filtered_df[filtered_df['Model'].str.lower().str.contains(search_model, na=False)]
    
    cars = []
    for _, row in filtered_df.iterrows():
        car = {
            'title': f"{row['Brand']} {row['Model']}",
            'brand': row['Brand'],
            'year': row['Year'],
            'km_driven': row['KM Driven'],
            'fuel_type': row['Fuel Type'],
            'transmission': row['Transmission'],
            'location': row['Location'],
            'price': f"₹{row['Price (INR)']:,}"
        }
        cars.append(car)
    
    brands = sorted(df['Brand'].unique()) if not df.empty else []
    
    return render_template('listings.html', cars=cars, brands=brands, 
                         search_brand=search_brand, search_model=search_model)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user' not in session:
        flash('Please login to access the prediction feature.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if not model_loaded or model is None:
            flash('Model not available. Please contact administrator.')
            return render_template('predict.html', show_form=True, **get_dropdown_data())
            
        try:
            # Get form data exactly as your model expects
            brand_model = request.form['brand_model']
            fuel_type = request.form['fuel_type']
            transmission = request.form['transmission']
            location = request.form['location']
            km_driven = float(request.form['km_driven'])
            car_age = float(request.form['car_age'])
            
            print(f"Input data:")
            print(f"Brand_Model: {brand_model}")
            print(f"Fuel Type: {fuel_type}")
            print(f"Transmission: {transmission}")
            print(f"Location: {location}")
            print(f"KM Driven: {km_driven}")
            print(f"Car Age: {car_age}")
            
            # Prepare input data exactly as your model was trained
            sample_data = pd.DataFrame([{
                "Brand_Model": brand_model,
                "Fuel Type": fuel_type,
                "Transmission": transmission,
                "Location": location,
                "KM Driven": km_driven,
                "Car Age": car_age
            }])
            
            print(f"Sample data prepared: {sample_data.to_dict('records')[0]}")
            
            # Create CatBoost Pool with categorical features (as per your training)
            sample_pool = Pool(data=sample_data, cat_features=cat_features)
            
            # Make prediction (model returns log-transformed price)
            log_pred = model.predict(sample_pool)
            
            # Convert back from log scale (as per your training)
            predicted_price = np.expm1(log_pred[0])
            
            print(f"Log prediction: {log_pred[0]}")
            print(f"Final price prediction: ₹{predicted_price:,.2f}")
            
            # Format price for display
            if predicted_price > 100000:
                formatted_price = f"₹{predicted_price/100000:.1f} Lakh"
            else:
                formatted_price = f"₹{predicted_price:,.0f}"
            
            # Car details for display
            car_details = {
                'Brand_Model': brand_model,
                'Car_Age': int(car_age),
                'KM Driven': int(km_driven),
                'Fuel Type': fuel_type,
                'Transmission': transmission,
                'Location': location
            }
            
            return render_template('predict.html', 
                                 prediction=formatted_price,
                                 raw_prediction=f"₹{predicted_price:,.0f}",
                                 car_details=car_details,
                                 show_form=True,
                                 **get_dropdown_data())
                                 
        except Exception as e:
            flash(f'Error making prediction: {str(e)}')
            print(f"Prediction error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    return render_template('predict.html', show_form=True, **get_dropdown_data())

def get_dropdown_data():
    if df.empty:
        return {
            'fuel_types': ['Petrol', 'Diesel', 'CNG', 'Electric'],
            'transmissions': ['Manual', 'Automatic'],
            'locations': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune'],
            'brand_models': ['Honda City GXi', 'Maruti Swift VDi', 'Hyundai i20 Magna', 'Toyota Innova 2.5 VX', 'Mahindra XUV500 W8', 'Tata Nexon XM'] # Default if df is empty
        }
    
    # Ensure 'Brand_Model' column exists in df for suggestions
    if 'Brand_Model' not in df.columns:
        df['Brand_Model'] = df['Brand'] + ' ' + df['Model']

    return {
        'fuel_types': sorted(df['Fuel Type'].unique()),
        'transmissions': sorted(df['Transmission'].unique()),
        'locations': sorted(df['Location'].unique()),
        'brand_models': sorted(df['Brand_Model'].unique()) # Get unique Brand_Model combinations
    }

# Test route to verify model works exactly as trained
@app.route('/test-model')
def test_model():
    if model:
        try:
            # Test with exact same data as your training example
            sample = pd.DataFrame([{
                "Brand_Model": "Honda City GXi",
                "Fuel Type": "Petrol",
                "Transmission": "Manual",
                "Location": "Mumbai",
                "KM Driven": 44000,
                "Car Age": 18
            }])
            
            print(f"Test sample: {sample.to_dict('records')[0]}")
            
            # Create Pool exactly as in your training
            sample_pool = Pool(data=sample, cat_features=cat_features)
            log_pred = model.predict(sample_pool)
            price_inr = np.expm1(log_pred[0])
            
            return f"""
            <h2>Model Test Results</h2>
            <p><strong>Input:</strong> Honda City GXi, Petrol, Manual, Mumbai, 44000 KM, 18 years old</p>
            <p><strong>Log Prediction:</strong> {log_pred[0]:.4f}</p>
            <p><strong>Final Price:</strong> ₹{price_inr:,.2f}</p>
            <p><strong>Expected:</strong> ~₹173,849 (as per your training)</p>
            <p><strong>Status:</strong> {'✅ Match!' if abs(price_inr - 173849) < 10000 else '⚠️ Different'}</p>
            """
            
        except Exception as e:
            return f"Model test failed: {str(e)}<br><br>Traceback:<br>{traceback.format_exc()}"
    return "Model not loaded"

@app.route('/model-info')
def model_info():
    """Display model information"""
    if model:
        try:
            info = f"""
            <h2>Model Information</h2>
            <p><strong>Model Type:</strong> CatBoost Regressor</p>
            <p><strong>Categorical Features:</strong> {cat_features}</p>
            <p><strong>Expected Features:</strong> Brand_Model, Fuel Type, Transmission, Location, KM Driven, Car Age</p>
            <p><strong>Output:</strong> Log-transformed price (converted back with np.expm1)</p>
            <p><strong>Training Info:</strong> Iterations=1500, Learning Rate=0.05, Depth=7</p>
            """
            return info
        except Exception as e:
            return f"Error getting model info: {str(e)}"
    return "Model not loaded"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        users = load_users()
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        
        if user:
            session['user'] = user['name']
            flash('Login successful!')
            return redirect(url_for('predict'))
        else:
            flash('Invalid email or password.')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        password = request.form['password']
        
        users = load_users()
        
        if any(u['email'] == email for u in users):
            flash('Email already registered.')
            return render_template('register.html')
        
        new_user = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'password': password,
            'registered_at': datetime.now().isoformat()
        }
        
        users.append(new_user)
        save_users(users)
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
