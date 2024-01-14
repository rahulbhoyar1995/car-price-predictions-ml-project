from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    fuel_type_diesel = 0
    if request.method == 'POST':
        year = int(request.form['Year'])
        present_price = float(request.form['Present_Price'])
        kms_driven = int(request.form['Kms_Driven'])
        kms_driven_2 = np.log(kms_driven)
        owner = int(request.form['Owner'])
        fuel_type_petrol = request.form['Fuel_Type_Petrol']
        
        if fuel_type_petrol == 'Petrol':
            fuel_type_petrol = 1
            fuel_type_diesel = 0
        else:
            fuel_type_petrol = 0
            fuel_type_diesel = 1
        
        year = 2020 - year
        seller_type_individual = request.form['Seller_Type_Individual']
        
        if seller_type_individual == 'Individual':
            seller_type_individual = 1
        else:
            seller_type_individual = 0
        
        transmission_manual = request.form['Transmission_Mannual']
        
        if transmission_manual == 'Mannual':
            transmission_manual = 1
        else:
            transmission_manual = 0
        
        prediction = model.predict([[present_price, kms_driven_2, owner, year, fuel_type_diesel,
                                     fuel_type_petrol, seller_type_individual, transmission_manual]])
        
        output = round(prediction[0], 2)
        
        if output < 0:
            return render_template('index.html', prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html', prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
