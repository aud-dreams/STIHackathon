# Libraries
import pandas as pd
import pickle

# Base
from sklearn.model_selection import train_test_split

# Models
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from collections import Counter
from imblearn.over_sampling import SMOTE
from numpy import where

# Performance
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV 
from sklearn.metrics import classification_report

# WOMEN DATASET
eth_women = pd.read_csv("eth_women.csv")

# drop all rows with num of sex partners = 0
eth_women.dropna(subset=["V836"], inplace=True)


# replace all nulls with 0
eth_women.fillna(0, inplace=True)

eth_women_df = eth_women[["CASEID", "V024", "V190", "V013", "V106", "V525", "V714", "V501", "V171A", "S1107D", "V131", "V763A"]]

eth_women_df.rename(columns = {"CASEID": "ID", "V024": "Region", "V190": "Wealth", "V013": "Age Category", "V106": "Educational Level", "V525": "Age at First Sex", "V714": "Working Status", "V501": "Marital Status", "V171A": "Internet Access", "S1107D": "Alcohol Drinking", "V131": "Ethnicity", "V763A": "STI"}, inplace = True)

# add column for sex (gender)
eth_women_df["Sex"] = 0


# MEN DATASET
eth_men = pd.read_csv("eth_men.csv")

# drop all rows with num of sex partners = 0
eth_men.dropna(subset=["MV836"], inplace=True)

# replace all nulls with 0
eth_men.fillna(0, inplace=True)

eth_men_df = eth_men[["MCASEID", "MV024", "MV190", "MV013", "MV106", "MV525", "MV714", "MV501", "MV171A", "SM815DD", "MV131", "MV763A"]]

eth_men_df.rename(columns = {"MCASEID": "ID", "MV024": "Region", "MV190": "Wealth", "MV013": "Age Category", "MV106": "Educational Level", "MV525": "Age at First Sex", "MV714": "Working Status", "MV501": "Marital Status", "MV171A": "Internet Access", "SM815DD": "Alcohol Drinking", "MV131": "Ethnicity", "MV763A": "STI"}, inplace = True)

# add column for sex (gender)
eth_men_df["Sex"] = 1


# combine men & women dataframes
merged_df = pd.concat([eth_men_df, eth_women_df])

# remove missing/don't know data
merged_df = merged_df[merged_df["Alcohol Drinking"] != 98]
merged_df = merged_df[merged_df["Ethnicity"] != 98]
merged_df = merged_df[merged_df["Ethnicity"] != 99]
merged_df = merged_df[merged_df["Ethnicity"] != 96]
merged_df = merged_df[merged_df["STI"] != 8]

X = merged_df[["Region", "Wealth", "Age Category", "Educational Level", "Age at First Sex", "Working Status", "Marital Status", "Internet Access", "Alcohol Drinking", "Ethnicity", "Sex"]]
y = merged_df['STI']

# Oversampling
counter = Counter(y)

oversample = SMOTE()
X_train_os, y_train_os = oversample.fit_resample(X, y)

counter = Counter(y_train_os)

oversampled_df = pd.DataFrame(X_train_os, columns=X.columns)
oversampled_df['STI'] = y_train_os
oversampled_df

# SUPPORT VECTOR MACHINE
X_train, X_test, y_train , y_test = train_test_split(X_train_os, y_train_os, test_size=0.2, random_state=42)

svm = LinearSVC(C=10, dual=False, fit_intercept=False, random_state=42)
clf = CalibratedClassifierCV(svm)
clf.fit(X_train, y_train)

y_pred_clf = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred_clf)
print("Accuracy:", accuracy)

y_proba_clf = clf.predict_proba(X_test)
y_proba_clf = pd.DataFrame(y_proba_clf)
print(y_proba_clf)



with open('model.pkl', 'wb') as file:
    pickle.dump(svm, file)