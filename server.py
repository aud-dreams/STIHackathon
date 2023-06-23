from flask import Flask, request, jsonify
import pickle
import pandas as pd

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

@app.route('/')
def predict():
    data = request.get_json()  # Get JSON payload from the request
    # # Make predictions using the loaded model
    parsed_data = {
        "Region": data['region'],
        "Wealth": data['wealth'],
        "Age Category": data['age'],
        "Educational Level": data['education'],
        "Age at First Sex": data['age_of_first'],
        "Working Status": data['working_status'],
        "Marital Status": data['marital'],
        "Internet Access": data['internet'],
        "Alcohol Drinking": data['alcohol'],
        "Ethnicity": data['ethnicity'],
        "Sex": data['sex'],
    }

    data_df = pd.DataFrame(parsed_data)

    predictions = model.predict(data_df)
    return jsonify({'predictions': predictions.tolist()})

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=13311)