import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.spatial import distance
import matplotlib.pyplot as plt
import seaborn as sn


def convert_string_values():
    cases.replace("3-4 Zimmer", "3.5", inplace=True, regex=True)
    cases.replace("4-5 Zimmer", "4.5", inplace=True, regex=True)
    cases.replace("5-6 Zimmer", "5.5", inplace=True, regex=True)
    cases.replace("5 Zimmer", "5", inplace=True, regex=True)
    cases.replace("6 Zimmer", "6", inplace=True, regex=True)
    cases.replace("4 Zimmer", "4", inplace=True, regex=True)
    cases.replace("3 Zimmer", "3", inplace=True, regex=True)
    cases.replace("Ein Zimmer", "1", inplace=True, regex=True)
    cases.replace("1 Zimmer", "1", inplace=True, regex=True)
    cases.replace("Zwei Zimmer", "2", inplace=True, regex=True)
    cases.replace("2 Zimmer", "2", inplace=True, regex=True)

    cases.replace("EG", "0", inplace=True, regex=True)
    cases.replace("1.Stock", "1", inplace=True, regex=True)
    cases.replace("2.Stock", "2", inplace=True, regex=True)
    cases.replace("3.Stock", "3", inplace=True, regex=True)
    cases.replace("4.Stock", "4", inplace=True, regex=True)
    cases.replace("5.Stock", "5", inplace=True, regex=True)
    cases.replace("6.Stock", "6", inplace=True, regex=True)
    cases.replace("7.Stock", "7", inplace=True, regex=True)
    cases.replace("8.Stock", "8", inplace=True, regex=True)

    cases.replace("Neubau", "1", inplace=True, regex=True)
    cases.replace("1-3 Jahre", "2", inplace=True, regex=True)
    cases.replace("4-7 Jahre", "5.5", inplace=True, regex=True)
    cases.replace("7-10 Jahre", "8.5", inplace=True, regex=True)
    cases.replace("11-15 Jahre", "13", inplace=True, regex=True)
    cases.replace("16-20 Jahre", "18", inplace=True, regex=True)
    cases.replace("21-30 Jahre", "25.5", inplace=True, regex=True)
    cases.replace("31-50 Jahre", "40.75", inplace=True, regex=True)
    cases.replace("51-75 Jahre", "63", inplace=True, regex=True)
    cases.replace("76-100 Jahre", "88", inplace=True, regex=True)
    cases.replace("ueber 100", "112", inplace=True, regex=True)

    cases['Kaution'].replace("keine", "0", inplace=True, regex=True)
    cases.replace("1000-1500", "1250", inplace=True, regex=True)
    cases.replace("ueber 3000", "3000", inplace=True, regex=True)


def convert_binary_values():
    cases.replace("ja", "1", inplace=True, regex=True)
    cases.replace("nein", "0", inplace=True, regex=True)
    cases.replace("teilmoebliert", "1", inplace=True, regex=True)


def one_hot_encoding(cases):
    heizung_dummies = pd.get_dummies(cases['Heizung'])
    merged = pd.concat([cases, heizung_dummies], axis='columns')
    cases = merged
    kindergarten_dummies = pd.get_dummies(cases['Kindergarten'])
    merged = pd.concat([cases, kindergarten_dummies], axis='columns')
    cases = merged
    schule_dummies = pd.get_dummies(cases['Schule'])
    merged = pd.concat([cases, schule_dummies], axis='columns')
    cases = merged
    sbahn_dummies = pd.get_dummies(cases['S-Bahn'])
    merged = pd.concat([cases, sbahn_dummies], axis='columns')
    cases = merged
    lage_dummies = pd.get_dummies(cases['Lage'])
    merged = pd.concat([cases, lage_dummies], axis='columns')
    cases = merged
    kueche_dummies = pd.get_dummies(cases['Kueche'])
    merged = pd.concat([cases, kueche_dummies], axis='columns')
    cases = merged
    bad_dummies = pd.get_dummies(cases['Bad'])
    merged = pd.concat([cases, bad_dummies], axis='columns')
    cases = merged
    cases.drop(columns=['Heizung', 'Kindergarten', 'Schule', 'S-Bahn', 'Lage', 'Kueche', 'Bad'], inplace=True)
    df1 = cases.pop('Bewohner')
    df2 = cases.pop('Altersklasse')
    cases['Bewohner'] = df1
    cases['Altersklasse'] = df2
    cases.to_csv('Nach Konvertierung.csv')
    return cases


# Reading the data into a data frame
cases = pd.read_csv('A002.csv')

convert_binary_values()
convert_string_values()
cases = one_hot_encoding(cases)

cases_ST = cases
cases_ST.drop(columns=['Bewohner', 'Altersklasse'], inplace=True)

standard_scaler = StandardScaler()
cases_ST = standard_scaler.fit(cases_ST)

# Setting the importance value of features
feature_importance = [0.9, 0.2, 0.4, 0.2, 0.1, 0.4, 0.4, 0.1, 0.1, 0.1, 0.9, 0.8, 0.95, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                      0.3, 0.3, 0.3, 0.7, 0.7, 0.7, 0.65, 0.65, 0.65, 0.5, 0.5, 0.5, 0.5, 0.5, 0.2, 0.2, 0.2, 0.4, 0.4,
                      0.4, 0.4, 0.4]

case_base = cases[0:0]

case_base = case_base.append(cases.iloc[[0]])
print(case_base.head(20))

# for k in feature_importance.keys():
#    print(feature_importance[k])


# print(distance.euclidean())
