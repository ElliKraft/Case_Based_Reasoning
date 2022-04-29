import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial.distance import pdist, squareform, cdist
import numpy
import sys


def convert_string_values():
    cases.replace("3-4 Zimmer", 3.5, inplace=True, regex=True)
    cases.replace("4-5 Zimmer", 4.5, inplace=True, regex=True)
    cases.replace("5-6 Zimmer", 5.5, inplace=True, regex=True)
    cases.replace("5 Zimmer", 5, inplace=True, regex=True)
    cases.replace("6 Zimmer", 6, inplace=True, regex=True)
    cases.replace("4 Zimmer", 4, inplace=True, regex=True)
    cases.replace("3 Zimmer", 3, inplace=True, regex=True)
    cases.replace("Ein Zimmer", 1, inplace=True, regex=True)
    cases.replace("1 Zimmer", 1, inplace=True, regex=True)
    cases.replace("Zwei Zimmer", 2, inplace=True, regex=True)
    cases.replace("2 Zimmer", 2, inplace=True, regex=True)

    cases.replace("EG", 0, inplace=True, regex=True)
    cases.replace("1.Stock", 1, inplace=True, regex=True)
    cases.replace("2.Stock", 2, inplace=True, regex=True)
    cases.replace("3.Stock", 3, inplace=True, regex=True)
    cases.replace("4.Stock", 4, inplace=True, regex=True)
    cases.replace("5.Stock", 5, inplace=True, regex=True)
    cases.replace("6.Stock", 6, inplace=True, regex=True)
    cases.replace("7.Stock", 7, inplace=True, regex=True)
    cases.replace("8.Stock", 8, inplace=True, regex=True)

    cases.replace("Neubau", 1, inplace=True, regex=True)
    cases.replace("1-3 Jahre", 2, inplace=True, regex=True)
    cases.replace("4-7 Jahre", 5.5, inplace=True, regex=True)
    cases.replace("7-10 Jahre", 8.5, inplace=True, regex=True)
    cases.replace("11-15 Jahre", 13, inplace=True, regex=True)
    cases.replace("16-20 Jahre", 18, inplace=True, regex=True)
    cases.replace("21-30 Jahre", 25.5, inplace=True, regex=True)
    cases.replace("31-50 Jahre", 40.75, inplace=True, regex=True)
    cases.replace("51-75 Jahre", 63, inplace=True, regex=True)
    cases.replace("76-100 Jahre", 88, inplace=True, regex=True)
    cases.replace("ueber 100", 112, inplace=True, regex=True)

    cases['Kaution'].replace("keine", 0, inplace=True, regex=True)
    cases.replace("1000-1500", 1250, inplace=True, regex=True)
    cases.replace("ueber 3000", 3000, inplace=True, regex=True)


def convert_binary_values():
    cases.replace("ja", 1, inplace=True, regex=True)
    cases.replace("nein", 0, inplace=True, regex=True)
    cases.replace("teilmoebliert", 1, inplace=True, regex=True)


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


def build_case_base(case_base_copy, cases):

    for index, row in cases_copy.iterrows():
        if index < 66:
            row_distances = cdist(case_base_copy.values, np.array([cases_copy_ST.iloc[index+1]]), metric='euclidean')

            print(index)
            print(row_distances)
            min_distance = row_distances.min()
            min_distance_idx = row_distances.argmin()

            print(min_distance_idx)
            if cases['Bewohner'][index+1] != cases['Bewohner'][min_distance_idx] or cases['Altersklasse'][index+1] != cases['Altersklasse'][min_distance_idx]:
                print('classified incorrect')
                print(cases['Bewohner'][index+1])
                print(cases['Bewohner'][min_distance_idx])
                print(cases['Altersklasse'][index+1])
                print(cases['Altersklasse'][min_distance_idx])
                # If false classified
                case_base_copy = case_base_copy.append(cases_copy_ST.iloc[index+1])

            if cases['Bewohner'][index+1] == cases['Bewohner'][min_distance_idx] and cases['Altersklasse'][index+1] == cases['Altersklasse'][min_distance_idx]:
                print('classified correct')
                print(cases['Bewohner'][index+1])
                print(cases['Bewohner'][min_distance_idx])
                print(cases['Altersklasse'][index+1])
                print(cases['Altersklasse'][min_distance_idx])

    print(case_base_copy.shape)

def allow_user_requests(build_case_base):
    print('Geben Sie bitte die Informationen zu der Wohnung ein.')
    Zimmerzahl = str(input("Zimmerzahl: ") or "0")
    Stockwerk = str(input("Stockwerk: ") or "0")
    Heizung = str(input("Heizung: ") or "0")
    Hausmeister = str(input("Hausmeister: ") or "0")
    Kindergarten = str(input("Kindergarten: ") or "0")
    Schule = str(input("Schule: ") or "0")
    SBahn = str(input("S-Bahn: ") or "0")
    Garage = str(input("Garage: ") or "0")
    Alter = str(input("Alter: ") or "0")
    Aufzug = str(input("Aufzug: ") or "0")
    Lage = str(input("Lage: ") or "0")
    Kaution = str(input("Kaution: ") or "0")
    Kueche = str(input("Kueche: ") or "0")
    Bad = str(input("Bad: ") or "0")
    Balkon = str(input("Balkon: ") or "0")
    Terrasse = str(input("Terrasse: ") or "0")
    Kehrwoche = str(input("Kehrwoche: ") or "0")
    Moebliert = str(input("Moebliert: ") or "0")
    Miete = float(input("Miete: ") or 0)
    Nebenkosten = float(input("Nebenkosten: ") or 0)
    Quadratmeter = float(input("Quadratmeter: ") or 0)

    user_input = [Zimmerzahl, Stockwerk, Heizung, Hausmeister,Kindergarten, Schule, SBahn, Garage, Alter, Aufzug, Lage, Kaution, Kueche, Bad, Balkon, Terrasse, Kehrwoche, Moebliert, Miete, Nebenkosten, Quadratmeter]
    print(user_input)


# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)


# Reading the data into a data frame
cases = pd.read_csv('A002.csv')
# print(cases.head(20))
# cases = cases.sample(frac=1).reset_index(drop=True)
# print(cases.head(20))

# Setting the importance value of features
feature_importance = [0.9, 0.2, 0.4, 0.2, 0.1, 0.4, 0.4, 0.1, 0.1, 0.1, 0.9, 0.8, 0.95, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                      0.3, 0.3, 0.3, 0.7, 0.7, 0.7, 0.65, 0.65, 0.65, 0.5, 0.5, 0.5, 0.5, 0.5, 0.2, 0.2, 0.2, 0.4, 0.4,
                      0.4, 0.4, 0.4, 1, 1]

convert_string_values()
convert_binary_values()
cases = one_hot_encoding(cases)


# Copy the columns names from cases to case_base
case_base = cases[0:0]

cases_copy = cases.drop(columns=['Bewohner', 'Altersklasse'])
case_base_copy = case_base.drop(columns=['Bewohner', 'Altersklasse'])

# Standardizing values
cases_copy_ST = cases_copy.to_numpy()
standard_scaler = StandardScaler()
# standard_scaler = MinMaxScaler()
cases_copy_ST = standard_scaler.fit_transform(cases_copy_ST)

# case_base_copy = case_base_copy.append(cases_copy_ST[0])
# case_base_copy = case_base_copy.append(pd.DataFrame(cases_copy_ST[0]))
cases_copy_ST = case_base_copy.append(pd.DataFrame(cases_copy_ST, columns=list(case_base_copy)), ignore_index=True)
case_base_copy = case_base_copy.append(cases_copy_ST.iloc[0])

cases_copy_ST = cases_copy_ST.multiply(feature_importance, axis='columns')

print("case base copy before method")
print('case_base_copy')
print(case_base_copy)
print('cases_copy')
print(cases_copy)
print('cases_copy_ST')
print(cases_copy_ST)

build_case_base(case_base_copy, cases)

allow_user_requests(build_case_base)

# for k in feature_importance.keys():
#    print(feature_importance[k])


# print(distance.euclidean())
