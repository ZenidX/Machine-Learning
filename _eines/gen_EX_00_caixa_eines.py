# -*- coding: utf-8 -*-
"""Genera el quadern EX_00_caixa_eines.ipynb.

Es la referencia d'eines que els alumnes tenen oberta al costat mentre fan
EX_01..EX_05. Per aixo, dues regles governen tot aquest fitxer:

1) No hi surt cap dels conjunts dels exercicis (Wine, breast cancer, digits,
   make_classification, vins_bruts.csv). Tots els exemples van sobre taules
   de joguina inventades a ma, de 6 a 10 files, que es llegeixen senceres a
   pantalla. Aixi l'alumne veu que fa cada funcio sense que se li reveli cap
   resultat que li tocava descobrir.

2) Cada seccio es autonoma: torna a construir les seves dades de joguina, de
   manera que es pugui obrir el quadern per la seccio que faci falta.

Els numeros que apareixen al text son els reals que surten en executar el
quadern amb numpy 2.3, pandas 2.3 i scikit-learn 1.8 (comprovar-ho amb
_eines/executa_nb.py).
"""
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code, escriu

DESTI = "Machine Learning/02_practica/EX_00_caixa_eines.ipynb"

cells = []

# ================================================================= portada
cells.append(md(r"""
# Caixa d'eines

**Optativa d'Aprenentatge automàtic — DAM/DAW 2n**

Els exercicis `EX_01`..`EX_05` et demanen fer servir eines que la teoria no va
arribar a explicar: matrius de confusió, imputadors, codificadors de text,
pipelines. Aquest quadern les explica totes. No és un exercici: aquí totes les
cel·les estan plenes i funcionen, i el pots tenir obert en una altra pestanya
mentre treballes.

**No resol cap exercici.** Tots els exemples van sobre taules inventades de sis a
deu files: quatre alumnes amb una nota, vuit fruites amb un pes, deu correus
classificats. Cap dels conjunts dels exercicis apareix aquí. Això és a posta: has
de poder comptar amb el dit el que fa cada funció, i cap número d'aquest quadern
et pot estalviar el descobriment que et toca fer al teu.

No el llegeixis de dalt a baix. Obre'l per la secció que necessitis: cada secció
torna a construir les seves pròpies dades i no depèn de cap altra.

## Índex

| | Secció | Eines |
|---|---|---|
| **1** | [Partir les dades](#1) | `train_test_split` |
| **2** | [Preparar columnes numèriques](#2) | `StandardScaler`, `fit_transform` contra `transform` |
| **3** | [Valors que falten](#3) | `isna`, `dropna`, `fillna`, `SimpleImputer` |
| **4** | [Columnes de text](#4) | `OneHotEncoder`, `pd.get_dummies` |
| **5** | [Duplicats](#5) | `duplicated`, `drop_duplicates` |
| **6** | [Encadenar-ho tot](#6) | `Pipeline`, `make_pipeline`, `ColumnTransformer` |
| **7** | [Mesurar un model](#7) | `accuracy_score`, `confusion_matrix`, `precision_score`, `recall_score`, `f1_score`, `classification_report`, `DummyClassifier` |
| **8** | [Escollir columnes](#8) | `SelectKBest`, `f_classif`, `feature_importances_` |
| **9** | [Provar configuracions](#9) | `cross_val_score`, `GridSearchCV` |
| **10** | [Dibuixar](#10) | `plt.scatter`, `plot_tree`, `meshgrid` + `contourf` |
| **11** | [Com saber si ho has fet bé](#11) | les quatre comprovacions |

Cada eina va explicada sempre igual: **què fa**, **què li has de donar i què et
torna**, **un exemple mínim** i **el parany**, si en té. La part del parany és la
que més et servirà: hi ha escrit l'error real que et sortirà a pantalla.

Tot funciona a Google Colab sense instal·lar res.
"""))

cells.append(code(r"""
# Tot el que fa servir aquest quadern. Cap fitxer local, cap instal.lacio.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# la llavor fixada, perque els numeros del text siguin els que et surten a tu
np.random.seed(0)

pd.set_option("display.width", 120)
print("numpy", np.__version__, "| pandas", pd.__version__)
"""))

# ======================================================= 1. train_test_split
cells.append(md(r"""
<a id="1"></a>

---

## 1. Partir les dades

### `train_test_split`

**Què fa.** Parteix les dades en dos trossos a l'atzar: un per entrenar el model i
un per examinar-lo.

**Què li has de donar i què et torna.** Li dones `X` (les columnes de mesures) i
`y` (l'etiqueta). Et torna **una tupla de quatre coses**, sempre en aquest ordre:
`X_entrena, X_examen, y_entrena, y_examen`. Si li has donat DataFrames, et torna
DataFrames; si li has donat arrays, arrays.

Tres arguments que has de conèixer:

- `test_size=0.4` — la fracció de files que van a l'examen. Amb 10 files, 4.
- `random_state=42` — fixa l'atzar. Amb el mateix número, la mateixa partició cada
  vegada. Sense això no pots comparar dos models: no sabries si la diferència és
  del model o de la partició.
- `stratify=y` — obliga que la proporció de cada classe sigui la mateixa als dos
  costats.

Mirem-ho amb deu alumnes. La columna `beca` és l'etiqueta i està **desequilibrada**:
només dos dels deu en tenen.
"""))

cells.append(code(r"""
from sklearn.model_selection import train_test_split

alumnes = pd.DataFrame({
    "nom":   ["Aina", "Bernat", "Clara", "David", "Elena",
              "Ferran", "Gemma", "Hug", "Irina", "Jordi"],
    "hores": [    2,       8,       5,       1,       9,
                  3,       7,       4,       6,       2],
    "nota":  [  4.0,     7.5,     6.0,     3.0,     9.0,
                4.5,     7.0,     5.0,     6.5,     3.5],
    "beca":  [    0,       0,       0,       0,       1,
                  0,       0,       0,       1,       0],
})

X = alumnes[["hores", "nota"]]
y = alumnes["beca"]

print("Files:", len(alumnes), "| amb beca:", int(y.sum()))
alumnes
"""))

cells.append(code(r"""
X_entrena, X_examen, y_entrena, y_examen = train_test_split(
    X, y, test_size=0.4, random_state=13)

print("entrenament:", len(X_entrena), "files | examen:", len(X_examen), "files")
print("beques a l'entrenament:", int(y_entrena.sum()))
print("beques a l'examen:     ", int(y_examen.sum()))
print("alumnes que han anat a l'examen:", list(alumnes.loc[X_examen.index, "nom"]))
"""))

cells.append(md(r"""
### El parany

Mira l'última línia: **l'examen ha sortit amb zero beques**. Les dues alumnes amb
beca (Elena i Irina) han caigut totes dues a l'entrenament.

Això no és un error del codi, és l'atzar fent el que fa: amb només dos casos
positius de deu, hi ha una probabilitat alta que tots dos acabin al mateix costat.
I el dany és greu: un examen sense cap beca **no pot dir res** sobre si el model
sap detectar beques. Podries tenir un 100 % de precisió i no haver mesurat res.

`stratify=y` ho impedeix: reparteix cada classe proporcionalment entre els dos
costats.
"""))

cells.append(code(r"""
X_entrena, X_examen, y_entrena, y_examen = train_test_split(
    X, y, test_size=0.4, random_state=13, stratify=y)

print("beques a l'entrenament:", int(y_entrena.sum()))
print("beques a l'examen:     ", int(y_examen.sum()))
print("alumnes que han anat a l'examen:", list(alumnes.loc[X_examen.index, "nom"]))
"""))

cells.append(md(r"""
Amb `stratify=y`, els dos casos positius es reparteixen: un a cada costat. Ara
l'examen sí que examina alguna cosa.

Dues coses més sobre `stratify`:

- Sempre es passa **l'etiqueta** (`stratify=y`), no `X`.
- Si una classe té **menys mostres que trossos** demanats, peta amb
  `ValueError: The least populated class in y has only 1 member`. Vol dir que no hi
  ha prou casos d'aquella classe per repartir-los; el problema són les dades, no
  l'argument.

**Quan fer-ho servir:** sempre que classifiques. No costa res i tanca un forat.
"""))

# ==================================================== 2. StandardScaler
cells.append(md(r"""
<a id="2"></a>

---

## 2. Preparar columnes numèriques

### `StandardScaler`

**Què fa.** Posa totes les columnes a la mateixa escala: a cada columna li resta la
seva mitjana i la divideix per la seva desviació típica. El resultat és una columna
amb mitjana 0 i desviació 1.

**Per què.** Els models que mesuren distàncies (k-NN, SVM) i els que ajusten
coeficients (regressió logística) comparen columnes entre elles. Si una columna va
per centenars i una altra no arriba a 10, la primera manda del tot i la segona no
compta. L'arbre i el bosc no ho necessiten: parteixen columna a columna i l'escala
els és indiferent.

**Què li has de donar i què et torna.** Li dones una matriu numèrica (array o
DataFrame, sense text ni `NaN`). Et torna **sempre un array de numpy**, no un
DataFrame: perds els noms de les columnes.

Vuit fruites, amb un pes en grams (de 8 a 1300) i un preu en euros (d'1,20 a 6,80).
Dues escales que no tenen res a veure.
"""))

cells.append(code(r"""
from sklearn.preprocessing import StandardScaler

fruites = pd.DataFrame({
    "fruita":   ["poma", "plàtan", "cirera", "meló", "maduixa", "pera", "kiwi", "raïm"],
    "pes_g":    [  180,     120,        8,    1300,       15,     200,     95,    450],
    "preu_eur": [ 1.20,    1.50,     6.80,    3.50,     4.90,    1.40,   2.10,   2.80],
})

X = fruites[["pes_g", "preu_eur"]]

print("mitjana per columna:", X.mean().to_numpy().round(3))
print("desviació per columna:", X.std(ddof=0).to_numpy().round(3))
fruites
"""))

cells.append(code(r"""
escalador = StandardScaler()
X_escalat = escalador.fit_transform(X)

print("tipus del resultat:", type(X_escalat).__name__)   # array, no DataFrame
print("\nel que ha apres l'escalador:")
print("  mitjanes (escalador.mean_): ", escalador.mean_.round(3))
print("  desviacions (escalador.scale_):", escalador.scale_.round(3))

print("\ndades escalades:")
print(np.round(X_escalat, 2))
"""))

cells.append(md(r"""
El meló, que pesava 1300 g, ha passat a valer 2,5: és el que està més lluny de la
mitjana. La cirera, de 8 g, ha passat a −0,72. Les dues columnes ja són comparables.

### La comprovació que faràs servir als exercicis

Un escalat correcte deixa cada columna amb **mitjana ≈ 0 i desviació ≈ 1**. Això es
comprova en dues línies, i és el primer que has de mirar quan un exercici et demana
escalar.
"""))

cells.append(code(r"""
print("mitjana per columna: ", X_escalat.mean(axis=0).round(9))
print("desviació per columna:", X_escalat.std(axis=0).round(9))
"""))

cells.append(md(r"""
`axis=0` vol dir *per columna* (recorre les files cap avall). Si t'oblides l'`axis`,
`X_escalat.mean()` et dona un sol número: la mitjana de tota la taula, que no és el
que vols comprovar.

Si en comptes de 0 i 1 et surt qualsevol altra cosa, l'escalat no s'ha aplicat on et
pensaves.

### El parany central de tot el curs: `fit_transform` contra `transform`

`StandardScaler` té dos verbs, i confondre'ls és l'error més car que pots cometre.

- **`fit`** — *aprèn* la mitjana i la desviació de les dades que li dones.
- **`transform`** — *aplica* el que ja ha apres. No torna a aprendre res.
- **`fit_transform`** — fa les dues coses de cop.

La regla és una sola frase: **`fit` només amb l'entrenament, mai amb l'examen.**

Dues línies de codi, i tota la diferència està en quin verb fa servir cada una:

```python
X_entrena_esc = escalador.fit_transform(X_entrena)   # aprèn AQUÍ
X_examen_esc  = escalador.transform(X_examen)        # només aplica
```

**Per què.** La mitjana de l'examen és informació de l'examen. Si l'escalador la
calcula, el teu entrenament ja ha vist alguna cosa de les dades amb què l'anaves a
examinar, i el número que et sortirà serà millor del que el model es mereix. Això té
nom: **fuita d'informació** (*data leakage*). Un model amb fuita sembla bo al quadern
i falla el dia que el fas servir amb dades noves de veritat.

Mirem-ho amb les fruites: sis per entrenar, dues per examinar.
"""))

cells.append(code(r"""
X_entrena = X.iloc[:6]     # poma, platan, cirera, melo, maduixa, pera
X_examen  = X.iloc[6:]     # kiwi, raim

escalador = StandardScaler()
X_entrena_esc = escalador.fit_transform(X_entrena)   # apren AQUI
X_examen_esc  = escalador.transform(X_examen)        # nomes aplica

print("mitjanes apreses (nomes de les 6 d'entrenament):", escalador.mean_.round(3))
print("mitjana de les 8 fruites senceres:              ", X.mean().to_numpy().round(3))
print()
print("entrenament escalat, mitjana per columna:", X_entrena_esc.mean(axis=0).round(9))
print("examen escalat, mitjana per columna:     ", X_examen_esc.mean(axis=0).round(3))
"""))

cells.append(md(r"""
Fixa-t'hi bé, perquè això sorprèn: **la mitjana de l'examen escalat no dona 0**, dona
−0,069 i −0,368. I està bé que sigui així.

L'escalador ha restat les mitjanes de l'entrenament (303,833 i 3,217), no les de
l'examen. El kiwi i el raïm han quedat una mica per sota del centre de l'entrenament,
i això és exactament el que ha de passar: l'examen es mesura amb la regla de
l'entrenament, no amb la seva pròpia.

Per tant, la comprovació «mitjana ≈ 0» s'aplica **al conjunt sobre el qual has fet
`fit`**. Si l'examen et dona exactament 0, sospita: vol dir que li has fet `fit` al
damunt.

L'error contrari, el que has d'evitar, s'escriu així:

```python
X_tot_esc = escalador.fit_transform(X)                 # MAL: fit amb tot
X_entrena_esc, X_examen_esc = ... # partir despres ja no arregla res
```

No peta. No avisa. Et dona un número que no val, i res no t'ho diu.

**La manera de no equivocar-se mai** és no escriure aquestes dues línies a mà i fer
servir un `Pipeline`, que és la secció 6.
"""))

# ==================================================== 3. valors que falten
cells.append(md(r"""
<a id="3"></a>

---

## 3. Valors que falten

Un valor que falta és un `NaN` (*not a number*). Els models de scikit-learn no els
accepten: `fit()` peta amb `ValueError: Input contains NaN`. Abans d'entrenar, els
has de comptar i decidir què en fas.

Sis alumnes, amb forats a posta en tres columnes.
"""))

cells.append(code(r"""
taula = pd.DataFrame({
    "nom":    ["Aina",     "Bernat", "Clara",  "David",    "Elena",    "Ferran"],
    "hores":  [   2.0,      np.nan,     5.0,      1.0,        9.0,        3.0],
    "nota":   [   4.0,         7.5,  np.nan,      3.0,        9.0,     np.nan],
    "ciutat": ["Badalona",  np.nan, "Girona", "Badalona", "Badalona", "Girona"],
})
taula
"""))

cells.append(md(r"""
### `isna().sum()` — l'inventari

**Què fa.** `isna()` torna una taula de la mateixa forma, plena de `True`/`False`.
`sum()` compta els `True` de cada columna (perquè `True` val 1).

**Què et torna.** Una Series de pandas: l'índex són els noms de les columnes i el
valor és quants nuls té cada una.

És sempre la primera línia que escrius davant d'unes dades que no coneixes.
"""))

cells.append(code(r"""
print(taula.isna().sum())
print()
print("nuls en total:", int(taula.isna().sum().sum()))
"""))

cells.append(md(r"""
Un nul a `hores`, dos a `nota`, un a `ciutat`: quatre en total. Els dos `sum()` de
la segona línia no són un error: el primer compta per columna i el segon suma
aquestes tres xifres.

### `dropna` — esborrar

**Què fa.** Treu les files (o les columnes) que tenen algun nul.

**Què li has de donar i què et torna.** Un DataFrame nou; **no modifica l'original**.
L'argument que decideix què s'esborra és `axis`:

- `axis=0` (el de sèrie) — esborra **files**.
- `axis=1` — esborra **columnes**.
"""))

cells.append(code(r"""
print("files originals:", len(taula))
print("amb dropna(axis=0):", len(taula.dropna(axis=0)), "files")
print()
print(taula.dropna(axis=0))
print()
print("amb dropna(axis=1) queden aquestes columnes:", list(taula.dropna(axis=1).columns))
"""))

cells.append(md(r"""
### El parany de `dropna`

Els dos resultats són un desastre, cadascun a la seva manera:

- `axis=0` t'ha deixat **3 files de 6**. Has perdut la meitat de les dades per quatre
  valors. En un dataset amb nuls repartits per moltes columnes, `dropna()` pot
  esborrar-ne el 80 % sense que t'adonis: no peta, no avisa, només et queda una taula
  petita.
- `axis=1` t'ha deixat **una sola columna**, `nom`, que és precisament la que no
  serveix per predir res.

Per això `dropna()` sempre va seguit de comptar les files que queden. Si el cost és
alt, cal imputar en comptes d'esborrar.

### `fillna` — omplir a mà

**Què fa.** Substitueix els nuls pel valor que li diguis.

**Què et torna.** Una còpia amb els forats plens. Serveix per a una exploració
ràpida.
"""))

cells.append(code(r"""
copia = taula.copy()
copia["hores"] = copia["hores"].fillna(taula["hores"].mean())
copia["nota"]  = copia["nota"].fillna(taula["nota"].median())

print("mitjana d'hores:", taula["hores"].mean(), "| mediana de nota:", taula["nota"].median())
print("nuls que queden:", int(copia[["hores", "nota"]].isna().sum().sum()))
copia[["nom", "hores", "nota"]]
"""))

cells.append(md(r"""
### `SimpleImputer` — omplir amb memòria

**Què fa.** El mateix que `fillna`, però és un objecte de scikit-learn: **aprèn** el
valor de reemplaçament amb `fit` i el **recorda** per aplicar-lo després amb
`transform`.

**Què li has de donar i què et torna.** Li dones una matriu (DataFrame o array). Et
torna **un array de numpy**, no un DataFrame. El valor que ha après queda a
`.statistics_`, un per columna.

Tres estratègies, i quan va cada una:

- `strategy="mean"` — la mitjana. Per a columnes numèriques sense valors extrems.
- `strategy="median"` — la mediana. Per a columnes numèriques **amb** valors
  extrems: un sol valor absurd et desplaça la mitjana i no la mediana.
- `strategy="most_frequent"` — el valor més repetit. És l'única que funciona amb
  **columnes de text**.
"""))

cells.append(code(r"""
from sklearn.impute import SimpleImputer

for estrategia in ["mean", "median"]:
    imputador = SimpleImputer(strategy=estrategia)
    resultat = imputador.fit_transform(taula[["hores", "nota"]])
    print(f"strategy={estrategia!r}")
    print("  statistics_ (el que omplira):", imputador.statistics_.round(3))
    print("  columna hores:", resultat[:, 0])
    print("  columna nota: ", resultat[:, 1].round(3))
"""))

cells.append(code(r"""
# most_frequent es l'unica que va amb text
imputador_text = SimpleImputer(strategy="most_frequent")
ciutats_plenes = imputador_text.fit_transform(taula[["ciutat"]])

print("valor mes frequent:", imputador_text.statistics_)
print("resultat:", list(ciutats_plenes.ravel()))
"""))

cells.append(md(r"""
`Badalona` surt tres vegades i `Girona` dues, així que el forat del Bernat s'ha omplert
amb `Badalona`.

### Per què un imputador és millor que un `fillna` a mà

Perquè en un exercici hi ha un examen pel mig, i **la mitjana també és informació**.

Si omples els forats amb `taula["hores"].mean()`, aquesta mitjana s'ha calculat amb
**totes** les files, incloses les de l'examen. Has tornat a filtrar informació, igual
que a la secció 2. L'imputador ho evita perquè fa `fit` un cop, amb l'entrenament, i
després `transform` a l'examen amb el valor que ja tenia guardat.

Mira la diferència de números:
"""))

cells.append(code(r"""
entrena = taula[["hores"]].iloc[:4]    # Aina, Bernat, Clara, David
examen  = taula[["hores"]].iloc[4:]    # Elena, Ferran

imputador = SimpleImputer(strategy="mean").fit(entrena)   # fit NOMES amb l'entrenament

print("mitjana apresa (nomes 4 files):", imputador.statistics_.round(4))
print("mitjana de les 6 files senceres:", round(taula['hores'].mean(), 4))
print()
print("entrenament imputat:", imputador.transform(entrena).ravel())
print("examen transformat: ", imputador.transform(examen).ravel())
"""))

cells.append(md(r"""
2,667 contra 4,0. Són dos números diferents, i el correcte és el primer: el forat del
Bernat s'ha d'omplir amb el que sabíem **abans** de mirar l'examen.

**Regla pràctica:** exploració i diagnòstic, `fillna` i `isna` de pandas. Dades que
aniran a un model amb examen, `SimpleImputer` dins d'un `Pipeline` (secció 6).
"""))

# ==================================================== 4. columnes de text
cells.append(md(r"""
<a id="4"></a>

---

## 4. Columnes de text

Un model no sap què és `"Girona"`. Si li passes una columna de text, peta amb
`ValueError: could not convert string to float: 'Girona'`. El text s'ha de convertir
en números, i **com el converteixes canvia el que el model n'entén**.

### Primer, l'error de fer-ho mal

La temptació és òbvia: assignar un número a cada categoria. Badalona 1, Barcelona 2,
Girona 3. És una línia de codi i funciona sense petar. Vegem què aprèn el model.
"""))

cells.append(code(r"""
from sklearn.linear_model import LinearRegression

lloguers = pd.DataFrame({
    "ciutat":  ["Badalona", "Barcelona", "Girona", "Badalona", "Barcelona", "Girona"],
    "lloguer": [      900,        1400,      800,        950,        1500,      780],
})

# LA MANERA MALA: un numero per categoria
codi = {"Badalona": 1, "Barcelona": 2, "Girona": 3}
X_mal = lloguers["ciutat"].map(codi).to_frame("codi_ciutat")

model = LinearRegression().fit(X_mal, lloguers["lloguer"])
print("pendent que ha apres:", round(float(model.coef_[0]), 2), "euros per unitat de codi")
print()
print("el que prediu el model:")
for ciutat, c in codi.items():
    una_fila = pd.DataFrame({"codi_ciutat": [c]})
    print(f"  {ciutat:<10} (codi {c}): {float(model.predict(una_fila)[0]):7.1f} €")
print()
print("el que diuen les dades de veritat:")
print(lloguers.groupby("ciutat")["lloguer"].mean().round(1).to_string())
"""))

cells.append(md(r"""
**La conclusió falsa que n'ha tret el model:** «cada unitat de codi baixa el lloguer
67,5 €». Com que Barcelona porta el codi 2 i Girona el 3, el model conclou que el
lloguer baixa en anar de Badalona a Barcelona a Girona, en línia recta.

I les dades diuen el contrari: Barcelona és la més cara de les tres (1450 € de
mitjana), i el model li assigna 1055 €, **per sota de Badalona**. Ha entès una
tendència que no existeix.

El problema no és el model, és el codi numèric. En posar 1, 2, 3 li has dit tres
coses que no eren certes: que hi ha un ordre, que Barcelona està entre les altres
dues, i que la distància de Badalona a Barcelona és la mateixa que de Barcelona a
Girona. Cap de les tres és veritat: **són tres ciutats, no tres nivells**.

Compte amb el matís: si la categoria **sí** que té ordre (`baix` < `mitjà` < `alt`),
codificar-la 1, 2, 3 és correcte i és el que has de fer. El que no es pot fer és
inventar un ordre on no n'hi ha.

### `OneHotEncoder` — la manera bona

**Què fa.** Converteix una columna amb $k$ categories en **$k$ columnes de zeros i
uns**. Cada fila té un 1 a la columna de la seva categoria i 0 a la resta. Cap
categoria queda més amunt o més avall que cap altra.

**Què li has de donar i què et torna.** Li dones una columna en forma de taula de dues
dimensions (`df[["ciutat"]]`, amb dos claudàtors). Et torna una matriu de $n$ files ×
$k$ columnes. Per defecte és una matriu dispersa (*sparse*); amb
`sparse_output=False` et dona un array normal, que és el que vols per mirar-lo.
`get_feature_names_out()` et dona els noms de les columnes noves.
"""))

cells.append(code(r"""
from sklearn.preprocessing import OneHotEncoder

ciutats = pd.DataFrame({
    "ciutat": ["Badalona", "Barcelona", "Girona", "Barcelona", "Badalona", "Girona"],
})

codificador = OneHotEncoder(sparse_output=False)
M = codificador.fit_transform(ciutats)

print("categories que ha trobat:", list(codificador.categories_[0]))
print("noms de les columnes noves:", list(codificador.get_feature_names_out()))
print("forma: una columna ha passat a ser", M.shape[1], "columnes")
print()
print(pd.DataFrame(M.astype(int), columns=codificador.get_feature_names_out()))
"""))

cells.append(md(r"""
Tres categories, tres columnes, un sol 1 per fila. Cap ciutat és més gran que cap
altra: la distància entre dues qualssevol és la mateixa. Això és el que volies dir des
del principi.

**Comprovació:** el nombre de columnes noves ha de ser igual al nombre de categories
diferents. Si `df["ciutat"].nunique()` dona 3 i t'han sortit 5 columnes, alguna cosa
s'ha codificat dues vegades.

### El parany: una categoria que no havies vist mai

El codificador aprèn les categories amb `fit`. Si a l'examen apareix una que no hi
era, peta.
"""))

cells.append(code(r"""
ciutats_noves = pd.DataFrame({"ciutat": ["Lleida", "Girona"]})

try:
    codificador.transform(ciutats_noves)
except ValueError as e:
    print("ValueError:", str(e).strip().splitlines()[0])
"""))

cells.append(md(r"""
`Found unknown categories ['Lleida'] in column 0 during transform`.

Petar és el comportament per defecte, i té sentit: t'avisa que les dades noves
contenen alguna cosa que el model no sap interpretar. Però amb dades reals això passa
constantment, i aturar tot el programa perquè ha aparegut una ciutat nova no sol ser
el que vols.

`handle_unknown="ignore"` diu: si no la conec, posa tot zeros en aquella fila.
"""))

cells.append(code(r"""
codificador_ok = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
codificador_ok.fit(ciutats)

resultat = codificador_ok.transform(ciutats_noves)
print("columnes:", list(codificador_ok.get_feature_names_out()))
print(resultat.astype(int))
print()
print("Lleida -> tot zeros (desconeguda) | Girona -> el seu 1 al lloc corresponent")
"""))

cells.append(md(r"""
La fila de `Lleida` queda `[0, 0, 0]`: el model no en sap res i no s'inventa res. La de
`Girona` funciona amb normalitat. El programa continua.

**Fes-lo servir sempre que codifiquis text dins d'un `Pipeline`**: és la línia que
evita que el teu codi peti amb dades que encara no has vist.

### `pd.get_dummies` i quan no serveix

**Què fa.** El mateix, però des de pandas, i et torna un **DataFrame amb els noms de
les columnes ja posats**. Per mirar les dades és més còmode.

**Per què no serveix per entrenar.** Perquè **no recorda res**. És una funció, no un
objecte amb `fit`: cada vegada que la crides mira les categories que hi ha en aquell
moment i fa les columnes que toquen. Amb entrenament i examen per separat, et surten
taules amb columnes diferents.
"""))

cells.append(code(r"""
print("get_dummies sobre l'entrenament:", list(pd.get_dummies(ciutats["ciutat"]).columns))
print("get_dummies sobre l'examen:     ", list(pd.get_dummies(ciutats_noves["ciutat"]).columns))
"""))

cells.append(md(r"""
Tres columnes a l'entrenament, dues a l'examen, i **cap de les dues no coincideix amb
l'altra**: l'examen ha inventat `Lleida` i ha perdut `Badalona` i `Barcelona`. Si
passes això a un model entrenat amb tres columnes, peta o —pitjor— li dones columnes
que volen dir una altra cosa.

**Regla:** `pd.get_dummies` per mirar; `OneHotEncoder` per entrenar.
"""))

# ==================================================== 5. duplicats
cells.append(md(r"""
<a id="5"></a>

---

## 5. Duplicats

Una fila repetida no és un error inofensiu. Si la mateixa fila acaba una vegada a
l'entrenament i una altra a l'examen, l'examen li està preguntant al model una cosa
que ja ha vist, amb la resposta inclosa. Deixa de ser un examen.

Set files, amb dues repetides.
"""))

cells.append(code(r"""
taula = pd.DataFrame({
    "nom":   ["Aina", "Bernat", "Clara", "Bernat", "David", "Aina", "Elena"],
    "hores": [    2,       8,       5,       8,       1,      2,       9],
    "nota":  [  4.0,     7.5,     6.0,     7.5,     3.0,    4.0,     9.0],
})
taula
"""))

cells.append(md(r"""
### `duplicated()` — comptar abans d'esborrar

**Què fa.** Marca amb `True` les files que ja havien aparegut abans.

**Què et torna.** Una Series de booleans, una per fila. `.sum()` te'ls compta.

**El detall important:** la **primera** aparició no es marca. Amb dues còpies d'una
fila, `duplicated()` dona un sol `True`. Per això el número que et surt és *quantes
files sobren*, no *quantes files estan implicades*.
"""))

cells.append(code(r"""
print("marca per fila:", list(taula.duplicated()))
print("files que sobren:", int(taula.duplicated().sum()))
print()
print("files implicades (keep=False marca TOTES les copies):",
      int(taula.duplicated(keep=False).sum()))
print()
print("les files repetides:")
print(taula[taula.duplicated(keep=False)])
"""))

cells.append(md(r"""
Dues files sobren (la segona del Bernat i la segona de l'Aina), però **quatre files
estan implicades**: les dues còpies de cada una. `keep=False` és el que fa servir
quan vols veure-les totes.

### `drop_duplicates()` — esborrar

**Què fa.** Torna la taula sense les files repetides.

**Què et torna.** Un DataFrame nou, **amb l'índex original ple de forats**. Per això
gairebé sempre va seguit de `.reset_index(drop=True)`.

Dos arguments:

- `keep` — quina còpia es queda: `"first"` (el de sèrie), `"last"`, o `False` per
  **treure-les totes**, inclosa la primera.
- `subset=["columna"]` — mira només aquestes columnes per decidir si dues files són
  iguals, en comptes de totes.
"""))

cells.append(code(r"""
net = taula.drop_duplicates().reset_index(drop=True)

print("abans:", len(taula), "files | despres:", len(net), "files")
print("comprovacio:", int(net.duplicated().sum()), "duplicats")
print()
print(net)
"""))

cells.append(code(r"""
print("keep='first' (el de serie):", len(taula.drop_duplicates(keep="first")), "files")
print("keep='last':               ", len(taula.drop_duplicates(keep="last")), "files")
print("keep=False (fora totes):   ", len(taula.drop_duplicates(keep=False)), "files")
print()
print("subset=['nom'] (una fila per nom):", len(taula.drop_duplicates(subset=["nom"])), "files")
"""))

cells.append(md(r"""
### El parany

Tres coses:

- **`keep=False` esborra més del que penses.** Tres files en lloc de cinc: ha tret les
  dues còpies del Bernat i les dues de l'Aina, i només han quedat Clara, David i
  Elena. Fes-lo servir quan un duplicat vol dir que la fila és sospitosa; no per
  netejar.
- **`subset` canvia la pregunta.** Amb `subset=["nom"]` dues files són «iguals» si
  comparteixen el nom, encara que la resta sigui diferent. Aquí dona el mateix, però
  amb dades reals pot esborrar files legítimes.
- **Esborra els duplicats abans de `train_test_split`.** Si ho fas després, ja hauràs
  repartit les còpies i el mal està fet.

L'ordre correcte és sempre: `drop_duplicates` → `train_test_split` → model.
"""))

# ==================================================== 6. Pipeline
cells.append(md(r"""
<a id="6"></a>

---

## 6. Encadenar-ho tot

### `Pipeline`

**Què fa.** Enganxa diversos passos en un sol objecte que es comporta com un model:
té `fit`, `predict` i `score`.

**Què resol.** A les seccions 2 i 3 has vist dues maneres de filtrar informació de
l'examen cap a l'entrenament, i les dues eren silencioses. El consell «recorda de fer
`fit` només amb l'entrenament» depèn de la teva disciplina, i la disciplina falla.

Un `Pipeline` **fa que l'error sigui impossible d'escriure**. Quan crides
`pipe.fit(X_entrena, y_entrena)`, cada pas fa `fit_transform` amb l'entrenament; quan
crides `pipe.predict(X_examen)`, cada pas fa només `transform`. No hi ha manera que
un `fit` toqui l'examen, perquè tu ja no escrius els `fit` un per un.

Això és el que val la pena entendre: no és comoditat, és una **garantia
estructural**.

**Què li has de donar i què et torna.** Li dones una llista de parelles
`("nom", objecte)`. Tots els passos menys l'últim han de tenir `transform`; l'últim és
el model. Et torna un objecte amb la mateixa interfície que un model.

### `ColumnTransformer`

**Què fa.** Aplica transformacions **diferents a columnes diferents**, i enganxa els
resultats de costat.

**Per què el necessites.** `StandardScaler` no pot tocar una columna de text i
`OneHotEncoder` no té sentit sobre una numèrica. `ColumnTransformer` és el que et
permet dir «escalador per a aquestes, codificador per a aquella».

**Què li has de donar i què et torna.** Una llista de triplets
`("nom", transformador, [llista de columnes])`. Et torna un array amb totes les
columnes resultants una al costat de l'altra.

Vuit pisos: dues columnes numèriques (`m2`, `planta`), una de text (`barri`), i
l'etiqueta `car`.
"""))

cells.append(code(r"""
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

pisos = pd.DataFrame({
    "m2":     [        45,          80,      95,         50,       70,         85,      55,      60],
    "planta": [         1,           4,       5,          1,        3,          4,       2,       2],
    "barri":  ["Gràcia", "Eixample", "Eixample", "Sants", "Gràcia", "Eixample", "Sants", "Sants"],
    "car":    [         0,           1,       1,          0,        0,          1,       0,       0],
})
pisos
"""))

cells.append(code(r"""
X = pisos[["m2", "planta", "barri"]]
y = pisos["car"]

# 1. partir PRIMER, abans de tocar res
X_entrena, X_examen, y_entrena, y_examen = train_test_split(
    X, y, test_size=0.25, random_state=0, stratify=y)

# 2. una cosa per a les numeriques, una altra per a la de text
preparacio = ColumnTransformer([
    ("num", StandardScaler(),                        ["m2", "planta"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"),  ["barri"]),
])

# 3. preparacio + model en un sol objecte
pipe = Pipeline([("preparacio", preparacio), ("model", LogisticRegression())])

# 4. un sol fit, nomes amb l'entrenament
pipe.fit(X_entrena, y_entrena)

print("prediu:", pipe.predict(X_examen), "| de veritat era:", y_examen.to_numpy())
print("score:", pipe.score(X_examen, y_examen))
"""))

cells.append(md(r"""
Sis línies de codi útil, un sol `fit`, i cap manera d'equivocar-se amb l'ordre.

Si vols veure què li arriba al model, el pas de preparació és consultable pel nom que
li has posat:
"""))

cells.append(code(r"""
prep = pipe.named_steps["preparacio"]

print("columnes que rep el model:", list(prep.get_feature_names_out()))
print("forma de l'entrenament transformat:", prep.transform(X_entrena).shape)
"""))

cells.append(md(r"""
Dues columnes numèriques escalades més tres columnes del barri: cinc columnes on
n'entraven tres. Els prefixos `num__` i `cat__` són el nom que li has donat a cada
branca del `ColumnTransformer`.

### `make_pipeline` — la versió curta

**Què fa.** El mateix que `Pipeline`, però li passes els objectes sense noms i els hi
posa sols, en minúscules.

**Quan fer-lo servir.** Quan no necessites consultar els passos pel nom. Als
exercicis apareix així: `make_pipeline(StandardScaler(), KNeighborsClassifier())`.
"""))

cells.append(code(r"""
from sklearn.neighbors import KNeighborsClassifier

curt = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))
print("noms que ha posat sols:", list(curt.named_steps.keys()))

curt.fit(X_entrena[["m2", "planta"]], y_entrena)
print("score:", curt.score(X_examen[["m2", "planta"]], y_examen))
"""))

cells.append(md(r"""
### El parany

- **Parteix abans de construir el pipeline**, no després. El pipeline et protegeix
  del `fit` sobre l'examen, però no pot endevinar quines files volies examinar.
- **L'últim pas és el model**; els altres han de tenir `transform`. Si poses dos
  models, peta amb `TypeError: All intermediate steps should be transformers`.
- **Un `Pipeline` dins d'un `ColumnTransformer` és normal**: si una columna necessita
  imputar-se *i* escalar-se, la branca és
  `Pipeline([("imp", SimpleImputer()), ("esc", StandardScaler())])`.
"""))

# ==================================================== 7. metriques
cells.append(md(r"""
<a id="7"></a>

---

## 7. Mesurar un model, i no només amb la precisió

Aquesta és la secció que més et farà falta, i la que no surt a cap quadern de teoria.

Fins ara has mesurat els models amb un sol número: el percentatge d'encerts. Aquest
número amaga una cosa que gairebé sempre importa: **quins** errors comet el model. I
en molts problemes els dos errors possibles no valen el mateix.

Farem tota la secció amb **deu correus** ja classificats, perquè els puguis comptar
amb el dit i quadrar-los amb el que diu cada funció. La classe positiva (l'1) és
«brossa».
"""))

cells.append(code(r"""
# 10 correus. real = el que era de veritat, predit = el que ha dit el model.
# 1 = brossa (la classe positiva), 0 = legitim
real   = np.array([1, 1, 1, 1, 0, 0, 0, 0, 0, 0])
predit = np.array([1, 1, 0, 0, 1, 0, 0, 0, 0, 0])

comparacio = pd.DataFrame({
    "correu": range(1, 11),
    "real":   ["brossa" if v else "legítim" for v in real],
    "predit": ["brossa" if v else "legítim" for v in predit],
})
comparacio["encert"] = np.where(real == predit, "sí", "NO")
comparacio
"""))

cells.append(md(r"""
Compta-ho tu abans de continuar. Dels deu correus:

- **2** eren brossa i el model ha dit brossa. Encerts sobre la classe positiva.
- **2** eren brossa i el model ha dit legítim. **Brossa que s'ha colat.**
- **1** era legítim i el model ha dit brossa. **Un correu bo a la paperera.**
- **5** eren legítims i el model ho ha dit. Encerts sobre la classe negativa.

Set encerts i tres errors. Ara veurem com cada funció diu una part d'aquests números.

### `accuracy_score` — la precisió

**Què fa.** Compta quina fracció de les prediccions són correctes.

$$\text{precisió} = \frac{\text{encerts}}{\text{total}}$$

**Què li has de donar i què et torna.** `accuracy_score(y_real, y_predit)`, en aquest
ordre. Et torna **un sol número** entre 0 i 1.

**Què compta.** Tots els encerts, siguin de la classe que siguin.
**Què no compta.** Res sobre com es reparteixen els errors. Els tres errors d'aquest
model no són intercanviables, i la precisió els tracta com si ho fossin.
"""))

cells.append(code(r"""
from sklearn.metrics import accuracy_score

print("accuracy_score:", accuracy_score(real, predit))
print("a ma: 7 encerts / 10 correus =", 7 / 10)
"""))

cells.append(md(r"""
### `confusion_matrix` — els quatre números

**Què fa.** Compta les quatre combinacions possibles de (què era, què ha dit).

**Què li has de donar i què et torna.** `confusion_matrix(y_real, y_predit)`. Et torna
**un array de numpy** de $k \times k$, amb $k$ el nombre de classes.

**Com es llegeix, que és tot el que importa aquí.** En `sklearn`:

> **les files són el que era de veritat, les columnes són el que ha dit el model.**

I les classes van ordenades de petit a gran: primer la 0, després la 1. Així que per a
un problema binari la matriu és:

| | **predit: 0 (legítim)** | **predit: 1 (brossa)** |
|---|---|---|
| **real: 0 (legítim)** | encerts negatius | **falsos positius** |
| **real: 1 (brossa)** | **falsos negatius** | encerts positius |

- **La diagonal** (de dalt a l'esquerra a baix a la dreta) són els **encerts**: el que
  era i el que ha dit coincideixen.
- **Fora de la diagonal**, els errors. I són de dos tipus, amb nom propi:
  - **Fals positiu** — no era, i el model ha dit que sí. Aquí: un correu bo a la
    paperera. Casella de dalt a la dreta.
  - **Fals negatiu** — era, i el model ha dit que no. Aquí: brossa que arriba a la
    safata. Casella de baix a l'esquerra.

Les paraules «positiu» i «negatiu» es refereixen sempre a **el que ha dit el model**,
i «fals» vol dir que s'ha equivocat. Un fals negatiu és un «ha dit que no i s'ha
equivocat».
"""))

cells.append(code(r"""
from sklearn.metrics import confusion_matrix

matriu = confusion_matrix(real, predit)
print(matriu)
print()

# la mateixa matriu, amb les etiquetes posades
print(pd.DataFrame(matriu,
                   index=["real: legítim", "real: brossa"],
                   columns=["predit: legítim", "predit: brossa"]))
"""))

cells.append(code(r"""
# quadrem cada casella amb el que has comptat a ma
vn, fp = matriu[0]
fn, vp = matriu[1]

print("encerts negatius (era legitim, ha dit legitim):", vn, " -> n'havies comptat 5")
print("falsos positius  (era legitim, ha dit brossa): ", fp, " -> n'havies comptat 1")
print("falsos negatius  (era brossa, ha dit legitim): ", fn, " -> n'havies comptat 2")
print("encerts positius (era brossa, ha dit brossa): ", vp, " -> n'havies comptat 2")
print()
print("la diagonal son els encerts:", vn + vp, "=", int(matriu.trace()))
print("i la precisio es la diagonal dividida pel total:", matriu.trace() / matriu.sum())
"""))

cells.append(md(r"""
### El parany de la matriu

- **L'ordre dels arguments.** `confusion_matrix(predit, real)` també funciona i no
  peta: et dona la matriu transposada, amb els falsos positius i els falsos negatius
  intercanviats. Primer sempre el real.
- **L'ordre de les classes.** Si la teva classe important és la 0 i no la 1, la
  casella que has de mirar canvia de lloc. `labels=[1, 0]` et deixa posar l'ordre que
  vulguis, i és recomanable escriure-ho explícitament perquè quedi clar al codi.
"""))

cells.append(code(r"""
print("per defecte, classes ordenades [0, 1]:")
print(confusion_matrix(real, predit))
print()
print("amb labels=[1, 0], la brossa primer:")
print(confusion_matrix(real, predit, labels=[1, 0]))
"""))

cells.append(md(r"""
És la mateixa informació amb les caselles canviades de lloc. Si llegeixes la segona
com si fos la primera, dius que hi ha 2 falsos positius quan n'hi ha 1.

### `precision_score` i `recall_score` — la decisió, no les fórmules

Les dues surten de la matriu, i cada una es fixa en un dels dos errors.

**Precisió de la classe positiva** (*precision*): de tots els que el model ha dit que
eren brossa, quants n'eren.

$$\text{precision} = \frac{VP}{VP + FP} = \frac{2}{2 + 1} = 0{,}667$$

**Sensibilitat** (*recall*): de tots els que eren brossa de veritat, quants n'ha
trobat.

$$\text{recall} = \frac{VP}{VP + FN} = \frac{2}{2 + 2} = 0{,}5$$

La fórmula és el de menys. **El que has de decidir és quin dels dos errors no et pots
permetre**, i això no ho diu la matemàtica, ho diu el problema:

- **Un diagnòstic mèdic.** El que no et pots permetre és un **fals negatiu**: dir-li a
  algú que està bé quan no ho està. Se'n va a casa sense tractament. Una falsa alarma
  és desagradable i porta a fer més proves, però no mata ningú. Aquí vols **recall
  alt**, i estàs disposat a pagar-ho amb falses alarmes.
- **Un filtre de correu brossa.** El que no et pots permetre és un **fals positiu**:
  enviar a la paperera un correu de veritat. Ningú no la mira, i has perdut informació
  que et feia falta. Que es coli una mica de brossa és molest i no més. Aquí vols
  **precision alta**, i estàs disposat a pagar-ho deixant passar brossa.

Són el mateix model i les mateixes dues fórmules: el que canvia és **què costa
equivocar-se**. Per això no hi ha una mètrica bona en general, i per això has de saber
de què va el problema abans de triar-la.

**Què li has de donar i què et torna.** `precision_score(y_real, y_predit)` i
`recall_score(y_real, y_predit)`. Un número cada una. `pos_label=0` canvia quina
classe es considera la positiva, i és l'argument que faràs servir quan la classe que
t'importa sigui la 0.
"""))

cells.append(code(r"""
from sklearn.metrics import precision_score, recall_score, f1_score

print("precision (classe 1, brossa):", round(precision_score(real, predit), 4))
print("  a ma: VP / (VP + FP) =", vp, "/", vp + fp, "=", round(vp / (vp + fp), 4))
print()
print("recall (classe 1, brossa):   ", round(recall_score(real, predit), 4))
print("  a ma: VP / (VP + FN) =", vp, "/", vp + fn, "=", round(vp / (vp + fn), 4))
print()
print("les mateixes mesures per a la classe 0 (legitim), amb pos_label=0:")
print("  precision:", round(precision_score(real, predit, pos_label=0), 4))
print("  recall:   ", round(recall_score(real, predit, pos_label=0), 4))
"""))

cells.append(md(r"""
Fixa-t'hi: la mateixa predicció té `recall` 0,5 per a la brossa i 0,833 per als
legítims. **Una mètrica sense dir de quina classe parla no vol dir res.**

### `f1_score`

**Què fa.** Combina precision i recall en un sol número (la seva mitjana harmònica),
per quan vols comparar models sense decidir quin error pesa més. Baixa si qualsevol de
les dues és baixa.

$$F_1 = 2 \cdot \frac{\text{precision} \cdot \text{recall}}{\text{precision} + \text{recall}}$$
"""))

cells.append(code(r"""
print("f1_score:", round(f1_score(real, predit), 4))
"""))

cells.append(md(r"""
### `classification_report` — tot de cop

**Què fa.** Calcula precision, recall i F1 **per a cada classe**, i els imprimeix en
una taula.

**Què li has de donar i què et torna.** `classification_report(y_real, y_predit)`. Et
torna **un text** per imprimir, no números per fer servir en un càlcul (per a això
tens les funcions d'abans). `target_names=[...]` posa noms a les classes en comptes de
0 i 1.

La columna `support` és quantes mostres reals té cada classe. Val la pena mirar-la
sempre: t'avisa si la partició t'ha deixat una classe amb quatre casos.
"""))

cells.append(code(r"""
from sklearn.metrics import classification_report

print(classification_report(real, predit, target_names=["legítim", "brossa"]))
"""))

cells.append(md(r"""
Tot el que has comptat a mà, en una taula: `brossa` té precision 0,67, recall 0,50 i
support 4 (els quatre correus de brossa que hi havia).

Un avís sobre les tres últimes línies: `accuracy` és la precisió global; `macro avg`
és la mitjana simple de les classes (tracta totes les classes igual, encara que una
tingui quatre casos i l'altra mil); `weighted avg` les pondera pel `support`. Si el
conjunt està desequilibrat, `macro avg` i `weighted avg` diuen coses molt diferents, i
el que sol interessar és el `macro`.

### `ConfusionMatrixDisplay` — la matriu dibuixada

**Què fa.** Pinta una matriu de confusió, útil quan hi ha moltes classes i llegir
l'array és incòmode.

**Què li has de donar.** La matriu ja calculada i, si vols, els noms de les classes.
`.plot()` la dibuixa.
"""))

cells.append(code(r"""
from sklearn.metrics import ConfusionMatrixDisplay

dibuix = ConfusionMatrixDisplay(confusion_matrix(real, predit),
                                display_labels=["legítim", "brossa"])
dibuix.plot(cmap="Blues", colorbar=False)
plt.title("Files: el que era. Columnes: el que ha dit el model")
plt.show()
"""))

cells.append(md(r"""
### `DummyClassifier` — la referència honesta

**Què fa.** Un «model» que no mira les dades. Amb `strategy="most_frequent"` respon
sempre la classe més freqüent de l'entrenament, sigui quina sigui l'entrada.

**Per què existeix.** Perquè un número sol no vol dir res. Un 85 % de precisió pot ser
excel·lent o pot ser vergonyós, i l'única manera de saber-ho és comparar-lo amb el que
s'aconsegueix sense fer res.

**Aquesta és l'eina que et permet avaluar-te sol**, sense que ningú et digui quin
número havies de treure. No necessites el resultat del professor: necessites el del
model tonto.

**Què li has de donar i què et torna.** S'usa exactament com qualsevol model: `fit`,
`predict`, `score`. Sempre amb les **mateixes** dades i la **mateixa** partició que el
model que vols jutjar; si no, la comparació no val.

Deu files amb una classe molt majoritària: vuit de classe 0, dues de classe 1.
"""))

cells.append(code(r"""
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier

desequilibrat = pd.DataFrame({
    "x1": [1, 2, 3, 4, 5, 6, 7, 8,  9, 10],
    "x2": [2, 1, 4, 3, 6, 5, 8, 7, 10,  9],
    "y":  [0, 0, 0, 0, 0, 0, 0, 0,  1,  1],
})
X = desequilibrat[["x1", "x2"]]
y = desequilibrat["y"]

X_entrena, X_examen, y_entrena, y_examen = train_test_split(
    X, y, test_size=0.4, random_state=0, stratify=y)

tonto = DummyClassifier(strategy="most_frequent").fit(X_entrena, y_entrena)

print("el que hi havia a l'examen:", y_examen.to_numpy())
print("el que respon el model tonto:", tonto.predict(X_examen))
print()
print("precisio del model tonto:", tonto.score(X_examen, y_examen))
print("recall del model tonto sobre la classe 1:",
      recall_score(y_examen, tonto.predict(X_examen), zero_division=0))
"""))

cells.append(md(r"""
Aquí està tot el problema en dos números: **un 75 % de precisió i un recall de 0**.

El model tonto no ha encertat ni un sol cas de la classe 1 —no en pot encertar cap, no
mira les dades— i tot i així treu un 75 %, perquè tres de les quatre files de l'examen
eren de la classe 0.

Conclusió pràctica: **si el teu model treu un 75 % en aquestes dades, no ha après
res.** I no ho hauries sabut mirant només el 75 %.

Per això, davant de qualsevol resultat, la primera pregunta és sempre la mateixa: **què
treu el `DummyClassifier` amb aquestes mateixes dades?** Si no el guanyes, el problema
no és afinar el model, és que encara no has fet res.

Una nota sobre `zero_division=0`: quan el model no prediu cap positiu, el
denominador de la fórmula és 0. Sense aquest argument, `sklearn` t'avisa amb un
`UndefinedMetricWarning` i et torna 0 igualment.
"""))

# ==================================================== 8. escollir columnes
cells.append(md(r"""
<a id="8"></a>

---

## 8. Escollir columnes

Quan una taula té moltes columnes, no totes serveixen. N'hi ha que no tenen cap relació
amb l'etiqueta i només afegeixen soroll. Dues maneres de veure-ho.

Vuit alumnes, tres columnes: `hores` d'estudi, `faltes` d'assistència i `atzar`, que
són números inventats sense cap relació amb res. L'etiqueta és `aprovat`.
"""))

cells.append(code(r"""
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

t = pd.DataFrame({
    "hores":   [1, 2, 3, 4, 7, 8, 9, 10],
    "faltes":  [9, 8, 7, 2, 4, 2, 1,  0],
    "atzar":   [5, 1, 9, 2, 6, 3, 8,  4],
    "aprovat": [0, 0, 0, 0, 1, 1, 1,  1],
})
X = t[["hores", "faltes", "atzar"]]
y = t["aprovat"]
t
"""))

cells.append(md(r"""
### `SelectKBest` amb `f_classif`

**Què fa.** Puntua cada columna per separat segons com de bé separa les classes ella
sola, i es queda amb les `k` millors. `f_classif` és la puntuació: mira si la mitjana
de la columna és diferent en cada classe.

**Què li has de donar i què et torna.** `SelectKBest(f_classif, k=2)` i després `fit`
amb `X` i `y` (necessita l'etiqueta). `transform` et torna un array amb només les `k`
columnes triades. Les puntuacions queden a `.scores_` i `.get_support()` et diu quines
ha triat.
"""))

cells.append(code(r"""
selector = SelectKBest(f_classif, k=2).fit(X, y)

print("puntuacio de cada columna:", np.round(selector.scores_, 2))
print("p-valor de cada columna:  ", np.round(selector.pvalues_, 4))
print()
print("mascara de triades:", selector.get_support())
print("columnes triades:", list(selector.get_feature_names_out()))
print("forma: de", X.shape, "a", selector.transform(X).shape)
"""))

cells.append(md(r"""
`hores` treu 43,2, `faltes` 7,17 i `atzar` 0,22. La columna inventada queda fora, que
és el que volies.

**El parany:** `f_classif` mira cada columna **tota sola**. Dues columnes que no diuen
res per separat poden dir-ho tot juntes, i `SelectKBest` no ho veurà mai.

### `feature_importances_`

**Què fa.** Un arbre o un bosc ja entrenat et diu quant ha fet servir cada columna per
decidir. No és una funció que cridis: és un **atribut que apareix després del `fit`**.

**Què et torna.** Un array amb un número per columna, **que sumen 1**. L'ordre és el
de les columnes de `X`.
"""))

cells.append(code(r"""
bosc = RandomForestClassifier(n_estimators=100, random_state=0).fit(X, y)

print("importancies:", np.round(bosc.feature_importances_, 3), "| suma:",
      round(bosc.feature_importances_.sum(), 6))
print()
for nom, imp in sorted(zip(X.columns, bosc.feature_importances_),
                       key=lambda p: -p[1]):
    print(f"  {nom:<8} {imp:.3f}")
"""))

cells.append(code(r"""
arbre = DecisionTreeClassifier(random_state=0).fit(X, y)
print("un arbre sol:", np.round(arbre.feature_importances_, 3))
"""))

cells.append(md(r"""
**El parany:** l'arbre sol dona `[1.0, 0.0, 0.0]` — tota la importància a `hores` i zero
a la resta. No vol dir que `faltes` no serveixi; vol dir que amb `hores` ja n'hi havia
prou per separar aquestes vuit files i l'arbre no ha necessitat mirar res més.

El bosc reparteix millor (0,44 / 0,37 / 0,19) perquè són cent arbres i cada un veu
columnes diferents. Per llegir importàncies, fes servir el bosc, no un arbre sol.

I fixa-t'hi: `atzar` treu 0,19. Una columna d'inventada pura no baixa a zero, perquè el
bosc l'acaba fent servir per desempatar. Amb poques files, una importància petita no
prova que la columna serveixi de res.
"""))

# ==================================================== 9. configuracions
cells.append(md(r"""
<a id="9"></a>

---

## 9. Provar diverses configuracions

Aquesta secció és per anar més enllà del que demanen els exercicis.

### `cross_val_score`

**Què fa.** Parteix les dades en `cv` trossos, i entrena `cv` vegades: cada vegada un
tros fa d'examen i la resta d'entrenament. Així cada fila fa d'examen exactament un
cop.

**Per què.** Perquè **una sola partició pot enganyar**. Amb un `train_test_split` i un
`random_state`, el número que et surt depèn de quines files han caigut a l'examen.

**Què li has de donar i què et torna.** `cross_val_score(model, X, y, cv=5)`, amb el
model **sense entrenar**. Et torna **un array amb `cv` números**, un per tros. El que
es reporta és la mitjana, i la desviació diu com de fiable és.

Dotze punts en dues columnes, amb dues classes que se solapen una mica.
"""))

cells.append(code(r"""
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

t = pd.DataFrame({
    "x1": [1.0, 2.0, 1.5, 2.5, 3.0, 5.5, 4.5, 7.0, 6.5, 7.5, 8.0, 3.5],
    "x2": [1.0, 2.0, 2.5, 1.5, 2.0, 6.0, 1.5, 7.0, 7.5, 6.5, 7.0, 6.5],
    "y":  [  0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1],
})
X = t[["x1", "x2"]]
y = t["y"]

# el mateix model, vuit particions simples diferents
for llavor in range(8):
    Xe, Xx, ye, yx = train_test_split(X, y, test_size=1/3,
                                      random_state=llavor, stratify=y)
    model = KNeighborsClassifier(n_neighbors=3).fit(Xe, ye)
    print(f"  random_state={llavor}: score {model.score(Xx, yx):.3f}")
"""))

cells.append(md(r"""
El mateix model i les mateixes dades donen **des de 0,5 fins a 1,0** segons la llavor.
Si informes del 1,0 has triat la partició que t'afavoria; si informes del 0,5 has
tingut mala sort. Cap dels dos números descriu el model.
"""))

cells.append(code(r"""
puntuacions = cross_val_score(KNeighborsClassifier(n_neighbors=3), X, y, cv=3)

print("un score per tros:", np.round(puntuacions, 3))
print("mitjana:", round(puntuacions.mean(), 3), "| desviacio:", round(puntuacions.std(), 3))
"""))

cells.append(md(r"""
`[0.75, 1.0, 0.75]`, mitjana 0,833. Aquest número ja no depèn d'una llavor afortunada,
i la desviació de 0,118 t'avisa que amb tan poques dades hi ha molta variabilitat.

**El parany:** `cv=5` amb una classe que té 4 mostres peta (`n_splits=5 cannot be
greater than the number of members in each class`). Baixa el `cv`, o mira't el
desequilibri.

### `GridSearchCV`

**Què fa.** Prova totes les combinacions de paràmetres que li dones, cada una amb
validació creuada, i es queda amb la millor.

**Què et torna.** L'objecte ja entrenat amb la millor combinació, i tres atributs:
`best_params_`, `best_score_` i `cv_results_`.
"""))

cells.append(code(r"""
graella = GridSearchCV(KNeighborsClassifier(), {"n_neighbors": [1, 3, 5]}, cv=3)
graella.fit(X, y)

print("millor combinacio:", graella.best_params_)
print("el seu score:", round(graella.best_score_, 3))
print("score de cada combinacio:", np.round(graella.cv_results_["mean_test_score"], 3))
"""))

cells.append(md(r"""
Les tres combinacions empaten a 0,833, i en cas d'empat es queda la primera. **Aquest
empat és el resultat**, no un error: amb dotze files, canviar `n_neighbors` no canvia
res, i la graella no té prou dades per distingir res. Val la pena mirar sempre
`cv_results_` i no només `best_params_`, per saber si la tria vol dir alguna cosa.

**El parany:** `GridSearchCV` multiplica. Tres valors × tres valors × `cv=5` són 45
entrenaments. Amb dades de veritat i una graella generosa, es pot passar molt de
temps.
"""))

# ==================================================== 10. dibuixar
cells.append(md(r"""
<a id="10"></a>

---

## 10. Dibuixar

### `plt.scatter` amb colors per classe

**Què fa.** Pinta punts. Per veure les classes de colors diferents, es pinta **una
crida per classe**, amb una màscara booleana que tria les files d'aquella classe.

És el patró que faràs servir sempre, i és aquest bucle:

```python
for classe in np.unique(y):
    mascara = (y == classe)
    plt.scatter(X[mascara, 0], X[mascara, 1], label=f"classe {classe}")
```
"""))

cells.append(code(r"""
from sklearn.tree import DecisionTreeClassifier, plot_tree

t = pd.DataFrame({
    "x1": [1.0, 2.0, 1.5, 2.5, 3.0, 5.5, 4.5, 7.0, 6.5, 7.5, 8.0, 3.5],
    "x2": [1.0, 2.0, 2.5, 1.5, 2.0, 6.0, 1.5, 7.0, 7.5, 6.5, 7.0, 6.5],
    "y":  [  0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1],
})
X = t[["x1", "x2"]].to_numpy()     # a numpy: les mascares hi son mes comodes
y = t["y"].to_numpy()

plt.figure(figsize=(6, 5))
for classe in np.unique(y):
    mascara = (y == classe)
    plt.scatter(X[mascara, 0], X[mascara, 1], s=70, label=f"classe {classe}")

plt.xlabel("x1")
plt.ylabel("x2")
plt.title("Dotze punts, dues classes")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""))

cells.append(md(r"""
Es veuen els dos punts que es colen al costat contrari: el de la classe 1 a baix a
l'esquerra i el de la classe 0 a dalt. Són els que fan que cap model no arribi al 100 %.

**El parany:** si passes `c=y` en comptes de fer el bucle, tens colors però no tens
llegenda, i no saps quin color és quina classe.

### `plot_tree`

**Què fa.** Dibuixa un arbre de decisió entrenat: cada nus mostra la pregunta que fa,
quantes mostres hi arriben i com estan repartides.

**Què li has de donar.** L'arbre ja entrenat. `feature_names` i `class_names` posen
noms en comptes de `X[0]` i `y[0]`; `filled=True` acoloreix els nusos per classe
majoritària. Necessita una figura gran per llegir-se: `figsize=(10, 6)` com a mínim.
"""))

cells.append(code(r"""
arbre = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X, y)

plt.figure(figsize=(10, 6))
plot_tree(arbre, feature_names=["x1", "x2"], class_names=["classe 0", "classe 1"],
          filled=True, fontsize=10)
plt.title("L'arbre sencer, llegible")
plt.show()
"""))

cells.append(md(r"""
Es llegeix de dalt a baix: a cada nus, si la condició es compleix vas a l'esquerra i si
no, a la dreta. `samples` són les mostres que hi arriben i `value` com es reparteixen
entre classes.

**El parany:** sense `max_depth`, un arbre entrenat amb dades reals surt amb desenes
de nusos i el dibuix és una taca il·legible. Per ensenyar-lo, entrena'l amb
`max_depth=3` o menys.

### La recepta de la frontera de decisió

Això és fontaneria: **no és el tema, i no l'has d'entendre línia per línia**. Copia la
funció i fes-la servir. Va amb qualsevol model de dues columnes.

La idea en tres passos: fabriques una quadrícula de punts que cobreix tot el dibuix
(`meshgrid`), demanes al model què prediu a cada punt de la quadrícula (`predict`), i
pintes la quadrícula de colors segons la resposta (`contourf`). El resultat és el mapa
de com el model ha repartit el pla.

El detall que embolica és `ravel()` i `reshape()`: `meshgrid` et dona dues matrius,
`predict` vol una llista de parelles, i `contourf` torna a voler una matriu. `ravel()`
aplana i `reshape()` recompon.
"""))

cells.append(code(r"""
def pinta_frontera(model, X, y, titol="", passa=0.05):
    '''Pinta la frontera de decisio d'un model entrenat amb DUES columnes.

    model: ja entrenat, amb .predict
    X: array (n, 2)      y: array (n,)
    '''
    # 1. una quadricula que cobreix el dibuix amb un marge
    marge = 0.5
    x_min, x_max = X[:, 0].min() - marge, X[:, 0].max() + marge
    y_min, y_max = X[:, 1].min() - marge, X[:, 1].max() + marge
    xx, yy = np.meshgrid(np.arange(x_min, x_max, passa),
                         np.arange(y_min, y_max, passa))

    # 2. que prediu el model a cada punt de la quadricula
    punts = np.c_[xx.ravel(), yy.ravel()]      # aplanar a llista de parelles
    Z = model.predict(punts).reshape(xx.shape)  # i recompondre la matriu

    # 3. pintar el fons i els punts a sobre
    plt.contourf(xx, yy, Z, alpha=0.25, cmap="coolwarm")
    for classe in np.unique(y):
        mascara = (y == classe)
        plt.scatter(X[mascara, 0], X[mascara, 1], s=70,
                    edgecolor="black", label=f"classe {classe}")
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title(titol)
    plt.legend()


plt.figure(figsize=(6, 5))
pinta_frontera(arbre, X, y, "Arbre amb max_depth=2: fronteres rectes")
plt.show()
"""))

cells.append(md(r"""
Les fronteres de l'arbre són horitzontals i verticals, perquè cada pregunta seva és
sobre una sola columna. Canvia el model i canvia la forma:
"""))

cells.append(code(r"""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

plt.figure(figsize=(11, 4.5))

plt.subplot(1, 2, 1)
pinta_frontera(KNeighborsClassifier(n_neighbors=3).fit(X, y), X, y, "k-NN amb k=3")

plt.subplot(1, 2, 2)
pinta_frontera(LogisticRegression().fit(X, y), X, y, "Regressió logística")

plt.tight_layout()
plt.show()
"""))

cells.append(md(r"""
El k-NN fa una frontera irregular que envolta els punts; la regressió logística només
sap fer una recta. La mateixa funció, tres models, tres formes.

**El parany:** la `passa` de la quadrícula. Amb `passa=0.05` i un dibuix gran, això és
`predict` sobre desenes de milers de punts, i amb k-NN pot tardar. Si va lent, puja-la
a `0.1`. I la funció només va amb **dues** columnes: amb tres o més no hi ha pla on
dibuixar.
"""))

# ==================================================== 11. autocomprovacio
cells.append(md(r"""
<a id="11"></a>

---

## 11. Com saber si ho has fet bé sense que ningú t'ho digui

Els enunciats dels exercicis porten una línia de «com saps que ho has fet bé» amb un
número aproximat. Aquesta línia és una crossa, i no la tindràs sempre: a la feina no hi
ha ningú que tingui el resultat apuntat. El que sí que tindràs sempre són aquestes
quatre comprovacions.

### 1. Comprova el mecanisme, no el resultat

No comprovis que el número final coincideix. Comprova que **cada pas ha fet el que
havia de fer**. Cada transformació deixa una empremta que es pot verificar en una
línia:

| Si has fet això | Comprova això | Ha de donar |
|---|---|---|
| escalar | `X_esc.mean(axis=0)` i `X_esc.std(axis=0)` | ≈ 0 i ≈ 1 (al conjunt del `fit`) |
| imputar | `df.isna().sum().sum()` | 0 |
| codificar text | nombre de columnes noves | tantes com categories |
| treure duplicats | `df.duplicated().sum()` | 0 |
| partir | `len(X_entrena) + len(X_examen)` | el total de files |
"""))

cells.append(code(r"""
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# una taula de joguina amb els quatre desperfectes alhora
brut = pd.DataFrame({
    "pes":    [ 180.0,  120.0, np.nan,  1300.0,  15.0,  180.0],
    "preu":   [  1.20,   1.50,   6.80,    3.50,  4.90,   1.20],
    "origen": ["local", "importat", "local", "importat", "local", "local"],
})

net = brut.drop_duplicates().reset_index(drop=True)
num = SimpleImputer(strategy="median").fit_transform(net[["pes", "preu"]])
num_esc = StandardScaler().fit_transform(num)
cat = OneHotEncoder(sparse_output=False).fit_transform(net[["origen"]])

print("duplicats que queden:", int(net.duplicated().sum()), "        -> ha de ser 0")
print("nuls que queden:", int(np.isnan(num).sum()), "              -> ha de ser 0")
print("mitjana escalada:", num_esc.mean(axis=0).round(9), "-> ha de ser ~0")
print("desviacio escalada:", num_esc.std(axis=0).round(9), "-> ha de ser ~1")
print("categories a 'origen':", net["origen"].nunique(),
      "| columnes creades:", cat.shape[1], "  -> han de coincidir")
"""))

cells.append(md(r"""
Cinc línies, cinc comprovacions, cap d'elles necessita saber el resultat final. Si una
falla, ja saps **quin** pas revisar.

### 2. Compara sempre contra el `DummyClassifier`

El teu número no vol dir res tot sol. El que vol dir alguna cosa és la **diferència**
entre el teu model i un que no mira les dades.
"""))

cells.append(code(r"""
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

joguina = pd.DataFrame({
    "x1": [1, 2, 3, 4, 5, 6, 7, 8,  9, 10],
    "x2": [2, 1, 4, 3, 6, 5, 8, 7, 10,  9],
    "y":  [0, 0, 0, 0, 0, 0, 0, 0,  1,  1],
})
X = joguina[["x1", "x2"]]
y = joguina["y"]

Xe, Xx, ye, yx = train_test_split(X, y, test_size=0.4, random_state=2, stratify=y)

tonto = DummyClassifier(strategy="most_frequent").fit(Xe, ye)
meu   = DecisionTreeClassifier(random_state=0).fit(Xe, ye)

print(f"model tonto:  {tonto.score(Xx, yx):.3f}")
print(f"el teu model: {meu.score(Xx, yx):.3f}")
print(f"diferencia:   {meu.score(Xx, yx) - tonto.score(Xx, yx):+.3f}")
"""))

cells.append(md(r"""
0,750 contra 1,000: l'arbre guanya el model tonto per 25 punts. **Això** és el que vol
dir que el model ha après alguna cosa, i no el 1,000 tot sol.

Si la diferència hagués sortit 0 o negativa, el problema **no és el model**: o les dades
no tenen la informació que li demanes, o el preprocessat l'ha destruït, o hi ha un
error al codi. Afinar paràmetres no ho arreglarà.

### 3. Mira si el número que et surt té sentit

Una precisió és **una fracció d'enters**: encerts partit per mostres de l'examen. Amb
$n$ mostres, els únics valors possibles són $0/n, 1/n, \dots, n/n$. No n'hi ha cap
entremig.

Per tant, davant de qualsevol número, la pregunta és: **quantes mostres té el test?**
"""))

cells.append(code(r"""
def valors_possibles(n):
    '''Els unics valors que pot prendre una precisio amb n mostres d'examen.'''
    return np.arange(n + 1) / n


n = 38
possibles = valors_possibles(n)

print(f"amb {n} mostres d'examen, la precisio puja de {1/n:.4f} en {1/n:.4f}")
print("els valors mes alts possibles:", np.round(possibles[-4:], 4))
print()
for candidat in [0.9500, 0.9474, 0.9737, 0.8000]:
    encerts = candidat * n
    # el candidat ve arrodonit a 4 decimals, aixi que admetem una centesima
    # d'encert de marge; un numero de veritat impossible falla per molt mes
    possible = abs(encerts - round(encerts)) < 0.01
    print(f"  {candidat:.4f} -> {encerts:7.2f} encerts ->",
          "possible" if possible else "IMPOSSIBLE amb 38 mostres")
"""))

cells.append(md(r"""
Un 0,9500 amb 38 mostres voldria dir 36,1 encerts, i els encerts són enters: **aquest
número no pot venir d'un examen de 38 mostres**. Els veïns que sí que existeixen són
36/38 = 0,9474 i 37/38 = 0,9737.

Quan un número no encaixa en la graella, sempre és una d'aquestes tres coses: has
mesurat sobre un conjunt diferent del que et pensaves, has barrejat les prediccions
d'un model amb les etiquetes d'un altre, o el número que estàs comparant no és una
precisió.

El cas extrem d'això és un examen petit. Amb 10 mostres, l'única cosa que pots dir és
la precisió en salts del 10 %, i un model que en encerta 9 i un que n'encerta 8 no es
poden distingir. **Un examen petit no mesura**, i mirar-ne la mida és el primer que has
de fer abans de creure't una diferència.

### 4. Compara l'entrenament amb l'examen

Sempre calcula les dues coses. El model ha vist les dades d'entrenament, així que hi
anirà millor; el que has de mirar és **quant** millor.

Aquí canviem de taula: les dades d'abans eren massa netes per ensenyar-ho. Aquesta té
deu files on l'etiqueta segueix `x1` **amb dues excepcions** (les files 4 i 7), que és
el que passa sempre amb dades de veritat.
"""))

cells.append(code(r"""
amb_soroll = pd.DataFrame({
    "x1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "x2": [3, 7, 1, 9, 4, 8, 2, 10, 5,  6],
    "y":  [0, 0, 0, 1, 0, 1, 0, 1, 1,  1],   # les files 4 i 7 son excepcions
})
Xs = amb_soroll[["x1", "x2"]]
ys = amb_soroll["y"]

Xe, Xx, ye, yx = train_test_split(Xs, ys, test_size=0.4, random_state=3, stratify=ys)

sense_limit = DecisionTreeClassifier(random_state=0).fit(Xe, ye)
amb_limit   = DecisionTreeClassifier(max_depth=1, random_state=0).fit(Xe, ye)

for nom, model in [("arbre sense limit", sense_limit), ("arbre max_depth=1", amb_limit)]:
    e = model.score(Xe, ye)
    x = model.score(Xx, yx)
    print(f"{nom:<20} entrenament {e:.3f} | examen {x:.3f} | forat {e - x:+.3f}")
"""))

cells.append(md(r"""
Compara les dues files de la sortida, perquè diuen una cosa que sorprèn:

- L'arbre **sense límit** treu **1,000 a l'entrenament i 0,750 a l'examen**.
- L'arbre amb **`max_depth=1`** treu **0,833 a l'entrenament i 1,000 a l'examen**.

El pitjor dels dos a l'entrenament és el millor a l'examen. L'arbre sense límit ha
crescut fins a encertar totes les files que li has donat, excepcions incloses: ha
construït una regla per a cada cas en comptes de trobar-hi un patró. I les excepcions
que ha memoritzat no es repeteixen a l'examen, així que cau al 0,750.

L'arbre de profunditat 1 no pot memoritzar res: fa una sola pregunta. Falla les
excepcions de l'entrenament (d'aquí el 0,833) i encerta el patró, que és el que sí que
es repeteix.

Per això aquell 1,000 no era una bona notícia.

Això té nom: **sobreajustament** (*overfitting*). I es detecta així, mirant el forat
entre els dos números:

| entrenament | examen | què vol dir |
|---|---|---|
| alt | alt | el model funciona |
| **alt** | **molt més baix** | ha memoritzat, no ha après |
| baix | baix | el model és massa simple, o les dades no tenen la informació |
| baix | **més alt** | l'examen t'ha sortit fàcil per casualitat; mira'n la mida |

Un 100 % a l'entrenament, tot sol, **no és un resultat**: és un avís.

---

### El resum

Quatre preguntes, i les pots respondre totes sense que ningú et digui res:

1. Cada pas ha deixat l'empremta que havia de deixar?
2. Guanyo el model que no mira les dades?
3. El número que em surt pot existir, amb aquesta quantitat de mostres?
4. Quant de forat hi ha entre l'entrenament i l'examen?

**La feina no és encertar el número que el professor tenia apuntat: és saber si el que
has fet està bé.**
"""))

info = escriu(cells, DESTI, titol_colab="EX_00_caixa_eines.ipynb")
print(info)
