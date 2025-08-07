🚗 Used Car Price Prediction Engine
Welcome to the Used Car Price Prediction Engine! This web application, built with Flask and a CatBoost Machine Learning model, allows users to get accurate price predictions for used cars based on various features. It also includes features for browsing car listings and user authentication.

✨ Features
AI-Powered Price Prediction: Get instant price estimates for used cars using a pre-trained CatBoost Regressor model.
Car Listings: Browse a comprehensive list of used cars with search and filter capabilities.
User Authentication: Secure login and registration system to access prediction features.
Responsive Design: A clean and intuitive user interface that works well on various devices.
Autocomplete Suggestions: Smart suggestions for car models in the prediction form to enhance usability.
🚀 Live Demo
Experience the application live here: https://car-price-predictor-s3ha.onrender.com/

🛠️ Technologies Used
Backend: Python, Flask
Machine Learning: Pandas, NumPy, Scikit-learn, CatBoost, Joblib
Frontend: HTML, CSS, JavaScript (Jinja2 templating)
Deployment: Render.com
Version Control: Git, GitHub
📊 Project Structure
car-price-predictor/
├── app.py                  # Main Flask application
├── Cars.csv                # Dataset used for training and dropdowns
├── car_price_model.pkl     # Pre-trained CatBoost ML model
├── users.json              # Simple JSON file for user data (can be replaced by DB)
├── Procfile                # Render.com process file for Gunicorn
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates (Jinja2)
│   ├── base.html
│   ├── index.html          # Landing page
│   ├── listings.html       # Car listings page
│   ├── login.html          # User login form
│   ├── predict.html        # Price prediction form and results
│   └── register.html       # User registration form
└── static/                 # Static assets (CSS, JS)
    ├── css/
    │   └── style.css       # Custom CSS styles
    └── js/
        └── script.js       # Frontend JavaScript
⚙️ Setup and Local Development
To run this project locally, follow these steps:

Clone the repository:

git clone https://github.com/Guruvd07/car-price-predictor.git
cd car-price-predictor
Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`
Install dependencies:

pip install -r requirements.txt
Ensure model and data files are present: Make sure Cars.csv and car_price_model.pkl are in the root directory of your project. If you trained your model separately, place your .pkl file here.

Run the Flask application:

python app.py
The application will typically run on http://127.0.0.1:5000.

☁️ Deployment
This project is designed for easy deployment on platforms like Render.com.

Deployment Steps:

Push your code to GitHub: Ensure all your project files, including Procfile and requirements.txt, are pushed to your GitHub repository.
Create a Web Service on Render.com:
Log in to Render.com and create a new "Web Service".
Connect your GitHub repository.
Configure the service with:
Runtime: Python 3
Build Command: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
Start Command: gunicorn app:app
Environment Variable: Add PYTHON_VERSION with a specific value like 3.11.8 (or 3.12.x).
Instance Type: Free
Monitor Deployment: Render will automatically build and deploy your application. Check the logs for any issues.
Access Live App: Once deployed, your application will be available at the URL provided by Render.
🤝 Contributing
Feel free to fork this repository, make improvements, and submit pull requests.

📄 License
This project is open-source and available under the MIT License.