import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.spatial import distance
import matplotlib.pyplot as plt
import seaborn as sn


def convert_zimmerzahl(cases, column_number):
    for index, zimmer in cases['Zimmerzahl'].iteritems():
        if zimmer == "Ein Zimmer":
            cases.iloc[index, column_number] = 1
        elif zimmer == "Zwei Zimmer":
            cases.iloc[index, column_number] = 2
        elif zimmer == "3 Zimmer":
            cases.iloc[index, column_number] = 3
        elif zimmer == "3-4 Zimmer":
            cases.iloc[index, column_number] = 3.5
        elif zimmer == "4 Zimmer":
            cases.iloc[index, column_number] = 4
        elif zimmer == "4-5 Zimmer":
            cases.iloc[index, column_number] = 4.5
        elif zimmer == "5 Zimmer":
            cases.iloc[index, column_number] = 5
        elif zimmer == "5-6 Zimmer":
            cases.iloc[index, column_number] = 5.5
    print(cases)

def convert_binary_values(cases, column_number):
    for index, value in cases['Hausmeister'].iteritems():
        if value == "ja":
            cases.loc[index, column_number] = 1
        elif value == "nein":
            cases.loc[index, column_number] = 0
    cases.to_csv('Hausmeister.csv')

# Reading the data into a data frame
cases = pd.read_csv('A002.csv')

convert_binary_values(cases, 3)
print(cases['Hausmeister'])


standard_scaler = StandardScaler()
cases_ST = standard_scaler.fit(cases)
print(cases_ST)

# Setting the importance value of features
feature_importance = {
    "Zimmerzahl": 0.9,
    "Stockwerk": 0.2,
    "Heizung": 0.1,
    "Hausmeister": 0.4,
    "Kindergarten": 0.3,
    "Schule": 0.7,
    "S-Bahn": 0.65,
    "Garage": 0.2,
    "Alter": 0.1,
    "Aufzug": 0.4,
    "Lage": 0.5,
    "Kaution": 0.6,
    "Kueche": 0.2,
    "Bad": 0.4,
    "Balkon": 0.4,
    "Terrasse": 0.1,
    "Kehrwoche": 0.1,
    "Moebliert": 0.1,
    "Miete": 0.9,
    "Nebenkosten": 0.8,
    "Quadratmeter": 0.95
}

case_base = pd.DataFrame(columns=feature_importance.keys())
# print(case_base, sep='\n')

case_base = case_base.append(cases.iloc[[0]])
# print(case_base)












# for k in feature_importance.keys():
#    print(feature_importance[k])


# print(distance.euclidean())
