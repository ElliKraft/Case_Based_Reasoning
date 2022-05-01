# **Ähnlichkeit und Case Based Reasoning**

## Aufgabenstellung

Es soll eine Wohnungsempfehlung ausgesprochen werden. Dazu werden Daten der aktuell vermieteten Wohnungen zugrunde gelegt. Zu jeder Wohnung werden Attribute erhoben 
und gespeichert wer in dieser wohnt. Zu den Bewohnern ist gespeichert in welcher Altersgruppe diese sind (gemeint: bewohnende Erwachsene). Zudem ist eine Kategorie 
gespeichert, z.B. «Familie», «Single», «Paar», «Rentner» Eine Wohnungsbeschreibung umfasst Attribute wie S-Bahn-Anschluss, Garage, Miete, Nebenkosten, Alter, Aufzug, 
Lage, Entfernung zur Stadtmitte, Kaution, Küche, Bad, Balkon, Terrasse, Kehrwoche und Quadratmeter etc. Diese Angaben sind teils vage und teils wurden Kategorien 
gebildet, die es ggf. zu analysieren gilt. 
Die Fallbasis soll nach dem in der Vorlesung vorgestellten Verfahren geeignet gefüllt werden und dabei eine möglichst geringe Zahl an Fällen aufnehmen – und natürlich 
trotzdem korrekt klassifizieren. Die Klassifikation ermittelt sowohl die Altersklasse als auch die Kategorie. Dazu sind geeignete Ähnlichkeitsmaße zu entwickeln und 
zu implementieren. Ein Datensatz soll eingelesen werden und aus diesem wird die Fallbasis aufgebaut. Abschließend soll das System bei Eingabe von Wohnungsattributen 
(auch unvollständige Angaben möglich) auf die Mieterkategorie schließen.

## Lösungsansatz

Die Lösung wird nach dem Prinzip des fallbasierten Schließens aufgebaut und inkludiert vier Stufen:
- Retrieve: suche nach einem ausreichend ähnlichen Fall in der Fallbasis 
- Reuse: verwende die Lösung des gefundenen, ähnlichen Falles
- Revise: ist die Lösung gut? Der Benutzer überarbeitet die Lösung und gibt sie ans System zurück.
- Retain: trage die Situation und ihre Lösung als neuen Fall in die Fallbasis ein.

Der Programmentwurf wird in Python implementiert. 

### *Datenvorbereitung*

Bevor mit dem Durchlauf der genannten Stufen begonnen wird, wird eine Fallbasis aufgebaut. Dafür werden die Daten in dem gegebenen Datensatz "A002.csv" zunächst 
vorbereitet: 
- Zeichenketten und Zahlen in den Tabellenspalten werden unifiziert und kodiert
- die dadurch erhaltenen Werte werden für die einfachere Vergleichbarkeit skaliert. Dafür kommt der StandartScaler zum Einsatz, der den Mittelwert in einer Spalte 
entfernt und die Varianz auf eine Einheit skaliert. [1]

Bei der ersten, visuellen Untersuchung des Datensatzes wurden die Daten nach Spalten (Features) sortiert. Dabei wurde festegstellt, dass manche Features gut erkennbare Cluster
von Bewohnerkategorien lieferten. Aufgrund dessen wurde ein Vorschlag zu der Wichtigkeit der Features gegeben: die Features mit dem guten Clustering bekamen ein 
größeres Gewicht, diese mit dem schlechteren wurden weniger priorisiert. Die erhaltenen Koeffizienten wurden in der Vorbereitungsphase mit den in den Spalten enthaltenen
Werten (Datensatz nach der Skalierung) multipliziert, um die zu berechnende Distanz zu beeinflussen. 

### *Fallbasis aufbauen*

Es soll ein Ähnlichkeitsmaß definiert werden. In dem vorgeschlagenen Programmentwurf wird dazu die Euklidische Distanz (ED) verwendet, da sie intuitiv einsetzbar und 
gut für die gegebene Dimensionalität der Daten geeignet ist. [2] Für den Einsatz der ED ist die Datenskalierung notwendig, die in der Vorbereitungsstufe durchgeführt wird. [3]
Es werden nur die Fälle in die Fallbasis aufgenommen, bei denen der Bewohner und die Altersklasse falsch klassifiziert werden. Davon wurden 18 Fälle festgestellt. 

### *Retrieve - Reuse - Revise - Retain*

Es wird dem Benutzer oder der Benutzerin vorgeschlagen, eine Eingabe mit den Informationen zu einer Wohnung zu tätigen. Diese Eingabe wird mit den oben erwähnten
Methoden (s. Datenvorbereitung) kodiert und skaliert. 
Im nächsten Schritt wird die Euklidische Distanz von den eingegebenen Daten zu den in der Fallbasis enthaltenen Fällen berechnet, so wird der Fall gefunden, der 
dem eingegebenen am ähnlichsten ist. Dem Benutzer/der Benutzerin werden eine Bewohnerkategorie und eine Altersklasse als Lösung vorgeschlagen, die aus dem Datum 
stammen, das die kleinste Distanz zu der Benutzereingabe hat. Falls der Vorschlag inkorrekt ist, wird er vom Benutzer/von der Benutzerin korrigiert, und der Fall wird
in die Fallbasis aufgenommen.

### *Ergebnisbewertung*

![image](https://user-images.githubusercontent.com/58466497/166161665-dc68f775-4db2-4243-8d5e-4e69e900c71f.png)

Das Bild zeigt einen Ausschnitt der Spalten aus der Fallbasis mit den Informationen zu den dort enthaltenen Bewohnerkategorien und Altersklassen. Wie in dem Bild zu 
sehen ist, sind in der Fallbasis Fälle aus jeder Bewohnerkategorie präsent. Der Fakt, dass es am meisten Fälle aus der Kategorie "Familie" gibt, erklärt sich dadurch, 
dass diese Kategorie die meisten Einträge im Datensatz hat. Außerdem sind manche Werte von unterschiedlichen Kategorien innerhalb der Fallbasis sehr ähnlich, wodurch 
die Grenzen der Kategorien verschwimmen, und die gezeigten Fehlklassifizierungen verursacht werden.

## Literaturquellen
1. „sklearn.preprocessing.StandardScaler“, scikit learn Documentation, 2022. [Online]. Available: 
https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
3. Brosius F. “Kapitel 27 Distanz- und Ähnlichkeitsmaße” in *SPSS 8 Professionelle Statistik unter Windows*, Hamburg, Germany: mitp, 1998.
4. Maheshwari H. (2021, Oct. 13). How to decide the perfect distance metric for your machine learning model. [Online]. Available:  
https://towardsdatascience.com/how-to-decide-the-perfect-distance-metric-for-your-machine-learning-model-2fa6e5810f11








