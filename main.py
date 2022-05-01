import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist


import warnings
warnings.filterwarnings("ignore")

# Converts string values from columns Zimmerzahl, Stockwerk, Alter and Kaution to Float
def convert_string_values(cases):
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

# Converts binary values from columns Hausmeister, Garage, Aufzug, Balkon, Terrasse, Kehrwoche and Moebliert into True and False
def convert_binary_values(cases):
    cases.replace("ja", 1, inplace=True, regex=True)
    cases.replace("nein", 0, inplace=True, regex=True)
    cases.replace("teilmoebliert", 1, inplace=True, regex=True)

# Applies one-hot-encoding on the columns Heizung, Kindergarten, Schule, S-Bahn, Lage, Kueche and Bad
def one_hot_encoding(cases):
    heizung_dummies = pd.get_dummies(cases['Heizung'])
    merged = pd.concat([cases, heizung_dummies], axis='columns')
    cases = merged
    kindergarten_dummies = pd.get_dummies(cases['Kindergarten'],prefix='kindergarten')
    merged = pd.concat([cases, kindergarten_dummies], axis='columns')
    cases = merged
    schule_dummies = pd.get_dummies(cases['Schule'],prefix='schule')
    merged = pd.concat([cases, schule_dummies], axis='columns')
    cases = merged
    sbahn_dummies = pd.get_dummies(cases['S-Bahn'],prefix='s-bahn')
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
    if 'Bewohner' in cases:
        df1 = cases.pop('Bewohner')
        df2 = cases.pop('Altersklasse')
        cases['Bewohner'] = df1
        cases['Altersklasse'] = df2
    return cases

# Builds the case base based on the given data
def build_case_base(case_base_copy, cases, case_base):

    for index, row in cases_copy.iterrows():
        if index < 66:
            row_distances = cdist(case_base_copy.values, np.array([cases_copy_ST.iloc[index+1]]), metric='euclidean')

            min_distance_idx = row_distances.argmin()

            # If false classified
            if cases['Bewohner'][index+1] != case_base['Bewohner'][min_distance_idx] or cases['Altersklasse'][index+1] != case_base['Altersklasse'][min_distance_idx]:
                case_base_copy = case_base_copy.append(cases_copy_ST.iloc[index+1])

                # add the case with "Bewohner" and "Altersklasse" to the case base for further classification of user input
                case_base = case_base.append(cases.iloc[index+1], ignore_index=True)

    return case_base_copy, case_base

# Takes and encodes user input
def allow_user_requests():
    user_input_df = pd.DataFrame(columns=['Zimmerzahl', 'Stockwerk', 'Heizung', 'Hausmeister', 'Kindergarten',
                                          'Schule', 'S-Bahn', 'Garage', 'Alter', 'Aufzug', 'Lage', 'Kaution',
                                          'Kueche', 'Bad', 'Balkon', 'Terrasse', 'Kehrwoche', 'Moebliert',
                                          'Miete', 'Nebenkosten', 'Quadratmeter'])

    print('Geben Sie bitte die Informationen zu der Wohnung ein.')
    Zimmerzahl = str(input("Zimmerzahl: ") or "0")
    Stockwerk = str(input("Stockwerk: ") or "0")
    Heizung = str(input("Heizung: ") or "Oel")
    Hausmeister = str(input("Hausmeister: ") or "0")
    Kindergarten = str(input("Kindergarten: ") or "fern")
    Schule = str(input("Schule: ") or "fern")
    SBahn = str(input("S-Bahn: ") or "erreichbar")
    Garage = str(input("Garage: ") or "0")
    Alter = str(input("Alter: ") or "0")
    Aufzug = str(input("Aufzug: ") or "0")
    Lage = str(input("Lage: ") or "Nebenstrasse")
    Kaution = str(input("Kaution: ") or "0")
    Kueche = str(input("Kueche: ") or "Kueche (alt)")
    Bad = str(input("Bad: ") or "Dusche")
    Balkon = str(input("Balkon: ") or "0")
    Terrasse = str(input("Terrasse: ") or "0")
    Kehrwoche = str(input("Kehrwoche: ") or "0")
    Moebliert = str(input("Moebliert: ") or "0")
    Miete = float(input("Miete: ") or 0)
    Nebenkosten = float(input("Nebenkosten: ") or 0)
    Quadratmeter = float(input("Quadratmeter: ") or 0)

    user_input = [Zimmerzahl, Stockwerk, Heizung, Hausmeister, Kindergarten, Schule, SBahn, Garage, Alter,
                  Aufzug, Lage, Kaution, Kueche, Bad, Balkon, Terrasse, Kehrwoche, Moebliert, Miete, Nebenkosten,
                  Quadratmeter]

    # save user_input as row in user_input dataframe
    user_input_df.loc[len(user_input_df)] = user_input

    convert_binary_values(user_input_df)
    convert_string_values(user_input_df)
    user_input_df = one_hot_encoding(user_input_df)

    user_input_ST = user_input_df.to_numpy().reshape(-1, 1)

    user_input_ST = np.append(user_input_ST, [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0],
                                              [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]])
    user_input_ST = user_input_ST.reshape(-1, 43)
    return user_input_ST, user_input_df

# Takes the scaled and original user inputs to classify it based on the built case base
def classify_user_input(user_input_ST, user_input_df):
    user_input_ST = np.multiply(user_input_ST, feature_importance_user_input)

    distance_for_user_input = cdist(case_base_copy.values, user_input_ST, metric='euclidean')

    min_distance_idx = distance_for_user_input.argmin()

    print(case_base['Bewohner'][min_distance_idx])
    print(case_base['Altersklasse'][min_distance_idx])

    korrekt_klassifiziert = str(input("War die Klassifizierung korrekt (Ja/Nein)? "))

    # If not classified correctly, the case needs to be saved in the case base
    if korrekt_klassifiziert == 'Nein':
        case_base_local, case_base_final = save_user_input_in_case_base(user_input_ST, user_input_df, case_base)
        return case_base_local, case_base_final

    # Otherwise, it doesn't need to be saved
    return case_base, case_base_copy



# Saves the given user input as case in the case base
def save_user_input_in_case_base(user_input_ST, user_input_df, case_base):
    bewohner = str(input("Bitte geben Sie die richtige Klassifierung für Bewohner an: "))
    altersklasse = str(input("Bitte geben Sie die richtige Klassifierung für Altersklasse an: "))
    user_input_df['Bewohner'] = bewohner
    user_input_df['Altersklasse'] = altersklasse
    pd.DataFrame(data=user_input_df).transpose()

    user_input_df_to_append = case_base[0:0]
    transformed_df = pd.concat([user_input_df_to_append, user_input_df], axis=0, ignore_index=True)
    parser = pd.io.parsers.base_parser.ParserBase({'usecols': None})
    transformed_df.columns = parser._maybe_dedup_names(transformed_df.columns)
    transformed_df = transformed_df.replace(np.nan, 0, regex=True)
    case_base_local = case_base.append(transformed_df)

    user_input_df_st = pd.DataFrame(user_input_ST, columns=case_base_copy.columns)
    case_base_final = case_base_copy.append(user_input_df_st, ignore_index=True)

    return case_base_local, case_base_final

# To show the full dataframe in the console
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


# Reading the data into a data frame
cases = pd.read_csv('A002.csv')

# Setting the importance value of features for given data
feature_importance = [200, 0.2, 10, 0.2, 0.3, 10, 10, 0.1, 0.1, 0.1, 50, 200, 200, 200, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                      0.3, 0.3, 0.3, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10,
                      10, 10, 10]

# Importance values for user input
feature_importance_user_input = [200, 0.2, 10, 0.2, 0.3, 10, 10, 0.1, 0.1, 0.1, 50, 200, 200, 200, 0.1, 0.3,
                                 50, 50, 50, 50, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# Converting values into float and integer, to be able to calculate distance later
convert_string_values(cases)
convert_binary_values(cases)
cases = one_hot_encoding(cases)


# Copy the columns names from cases to case_base
case_base = cases[0:0]

cases_copy = cases.drop(columns=['Bewohner', 'Altersklasse'])
case_base_copy = case_base.drop(columns=['Bewohner', 'Altersklasse'])

# Standardizing values
cases_copy_ST = cases_copy.to_numpy()
standard_scaler = StandardScaler()
cases_copy_ST = standard_scaler.fit_transform(cases_copy_ST)


cases_copy_ST = case_base_copy.append(pd.DataFrame(cases_copy_ST, columns=list(case_base_copy)), ignore_index=True)
case_base_copy = case_base_copy.append(cases_copy_ST.iloc[0])
case_base = case_base.append(cases.iloc[0])

cases_copy_ST = cases_copy_ST.multiply(feature_importance, axis='columns')

case_base_copy, case_base = build_case_base(case_base_copy, cases, case_base)
print("Fallbasis aufgebaut")
print(case_base)
case_base_copy = case_base_copy.reset_index(drop=True)
print("Fallbasis skaliert")
print(case_base_copy)

# User can give input as often as he likes
nochmal_eingeben = True
while nochmal_eingeben:
    user_input_ST, user_input_df = allow_user_requests()
    user_input_ST = standard_scaler.transform(user_input_ST)
    case_base_final, case_base_copy_final = classify_user_input(user_input_ST, user_input_df)
    nochmal_eingeben = str(input("Wollen Sie noch einmal eingeben? (Ja/Nein) "))
    if nochmal_eingeben == 'Nein' or nochmal_eingeben == 'nein':
        nochmal_eingeben = False
        print('Finale Fallbasis')
        print(case_base_final.reset_index(drop=True))
        # print('Skalierte Fallbasis')
        # print(case_base_copy_final)

