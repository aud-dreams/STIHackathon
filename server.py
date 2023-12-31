from flask import Flask, request, jsonify
import pickle
import pandas as pd

model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def predict():
    data = request.get_json()  # Get JSON payload from the request

    # Make predictions using the loaded model
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

    data_df = pd.DataFrame(parsed_data, index=[0])

    predictions = model.predict(data_df)
    y_proba_clf = model.predict_proba(data_df)
    y_proba_clf = pd.DataFrame(y_proba_clf)

    return jsonify({'predictions': predictions.tolist(), 'probability': y_proba_clf.to_dict()})

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=13311)
