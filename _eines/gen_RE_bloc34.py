# -*- coding: utf-8 -*-
"""OBSOLET (14-oct-2026): genera el format antic amb bastida. Els enunciats es fan ara amb
gen_reptes_enunciat.py i els resolts amb gen_reptes_resolts.py. Es conserva com a referència.

Genera els quaderns de l'alumne dels reptes dels blocs 3 i 4.

    ../CEIABD-IA/.venv/Scripts/python.exe _eines/gen_RE_bloc34.py

Bloc 3 (dades brutes i Pipeline): RE_301..RE_304. Bloc 4 (no supervisat): RE_401..RE_403.
Format i regles: docs/plantilla-reptes.md. Aquest fitxer NO conte respostes: els solucionaris
es generen amb Machine Learning/04_reptes/solucions/gen_RE_bloc34_solucions.py, que reaprofita
les cel.les de carrega d'aqui perque siguin identiques.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from nbgen import md, code, escriu  # noqa: E402

ARREL = os.path.dirname(AQUI)
REPTES = os.path.join(ARREL, "Machine Learning", "04_reptes")

RAW = ("https://raw.githubusercontent.com/ZenidX/Machine-Learning/main/"
       "Machine%20Learning/04_reptes/dades/")


# ---------------------------------------------------------------------------
# Peces de format
# ---------------------------------------------------------------------------
def pistes(p1, p2, p3):
    out = []
    for i, p in enumerate((p1, p2, p3), 1):
        out.append(f"<details><summary>Pista {i}</summary>\n\n{p}\n\n</details>")
    return "\n\n".join(out)


def tasca(titol, enunciat, comprova, p1, p2, p3, resposta=False):
    """Una tasca: enunciat + comprovacio + pistes plegades, i una cel.la buida."""
    text = f"### {titol}\n\n{enunciat.strip()}\n\n**Comprova.** {comprova.strip()}\n\n{pistes(p1, p2, p3)}"
    cells = [md(text), code("# el teu codi")]
    if resposta:
        cells.append(md("**La teva resposta:** *escriu-la aquí, amb les teves paraules.*"))
    return cells


def oberta(titol, enunciat, p1=None, p2=None, p3=None):
    text = f"### {titol}\n\n{enunciat.strip()}"
    if p1:
        text += "\n\n" + pistes(p1, p2, p3)
    return [md(text), code("# el teu codi")]


def la_teva_pregunta(num):
    return [md(f"### {num} · La teva pregunta\n\nPlanteja't una pregunta sobre aquestes dades que no "
               "s'hagi fet aquí, i respon-la. Escriu primer la pregunta en una cel·la de text."),
            code("# el teu codi")]


def xavi(*dubtes):
    llista = "\n".join(f"> - «{d}»" for d in dubtes)
    return md("> **Quan cridar en Xavi.** Dubtes de criteri, no de sintaxi (per a la sintaxi hi ha "
              "les pistes i la documentació):\n>\n" + llista)


def lliurament(que_ha_de_dir):
    return [md("## Lliurament\n\nCompta com a activitat si hi ha, com a mínim:\n\n"
               "- els **nivells 1 i 2 complets**, amb les comprovacions passant;\n"
               "- la **conclusió** de sota, escrita per tu, en **tres a cinc frases**: "
               + que_ha_de_dir),
            md("## Conclusió\n\n*Escriu-la aquí.*")]


def caixa(files):
    taula = "\n".join(f"| {a} | {b} |" for a, b in files)
    return md("## Caixa d'eines\n\nL'enunciat et diu **quina eina** fer servir. Mai **quin resultat** "
              "surt.\n\n| Eina | Què fa |\n|---|---|\n" + taula)


def _carrega(linies):
    return code(f'''import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Còpia congelada al repositori del curs (les dades originals són vives i canvien).
# Si tens el repositori clonat, llegeix la còpia local; si no (Colab), la baixa de GitHub.
DADES = "{RAW}"

def llegeix(fitxer, **opcions):
    for ruta in ("dades/" + fitxer, "../dades/" + fitxer):
        if os.path.exists(ruta):
            return pd.read_csv(ruta, **opcions)
    return pd.read_csv(DADES + fitxer, **opcions)

{linies}''')


# ---------------------------------------------------------------------------
# Cel.les de carrega (les reaprofita el generador dels solucionaris)
# ---------------------------------------------------------------------------
NOMS_AUTOS = ["symboling", "normalized-losses", "make", "fuel-type", "aspiration",
              "num-of-doors", "body-style", "drive-wheels", "engine-location", "wheel-base",
              "length", "width", "height", "curb-weight", "engine-type", "num-of-cylinders",
              "engine-size", "fuel-system", "bore", "stroke", "compression-ratio", "horsepower",
              "peak-rpm", "city-mpg", "highway-mpg", "price"]

CARREGA = {
    "301": lambda: code(f'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data"
# El fitxer no porta capçalera: els noms són els del fitxer de descripció de la UCI
NOMS = {NOMS_AUTOS!r}

df = pd.read_csv(URL, header=None, names=NOMS)
print(df.shape)
df.head()'''),
    "302": lambda: _carrega('''a23 = llegeix("accidents_gu_bcn_2023.csv")
a24 = llegeix("accidents_gu_bcn_2024.csv")
print(a23.shape, a24.shape)
a24.head()'''),
    "303": lambda: code('''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-11/hotels.csv"
df = pd.read_csv(URL)
print(df.shape)
df.head()'''),
    "304": lambda: _carrega('''df = llegeix("certificats_energetics_mostra.csv")
print(df.shape)
df.head()'''),
    "401": lambda: code('''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00292/Wholesale%20customers%20data.csv"
df = pd.read_csv(URL)
print(df.shape)
df.head()'''),
    "402": lambda: code('''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv"
df = pd.read_csv(URL)
print(df.shape)
df.head()'''),
    "403": lambda: _carrega('''df = llegeix("indicadors_municipis_2023_2024.csv")
print(df.shape)
df.head()'''),
}

CAP_B3 = "**Bloc 3 · Dades brutes i Pipeline · repte {n} de 4 · durada: 1 o 2 sessions de 2 h**"
CAP_B4 = "**Bloc 4 · No supervisat · repte {n} de 3 · durada: 1 o 2 sessions de 2 h**"

# Enllacos al material del curs (relatius des de 04_reptes/)
EX00 = "../02_practica/EX_00_caixa_eines.ipynb"
EX05 = "../02_practica/EX_05_dades_brutes.ipynb"
FO02 = "../01_fonaments/FO_02_pandas.ipynb"
ML06 = "../01_teoria/ML_06_kmeans.ipynb"
EX06 = "../02_practica/EX_06_kmeans.ipynb"
MA06 = "../03_matematiques/MA_06_pca_vectors_propis.ipynb"


# ===========================================================================
# RE_301 · Cotxes dels 80
# ===========================================================================
def re_301():
    c = [md(f"""# RE_301 · Quant val aquest cotxe?

{CAP_B3.format(n=1)}

Treballes per a una empresa que importa **cotxes de col·lecció dels anys 80**. Cada cop que arriba
una oferta, algú ha de mirar-se la fitxa tècnica i dir un preu. El cap vol una estimació
automàtica, i te'n fa una sola pregunta:

- **Amb quin error, en dòlars, es pot estimar el preu d'un cotxe a partir de la seva fitxa?** I
  aquest número, és un número en què es pugui confiar?"""),
         md(f"""## Què necessites saber abans

- Valors que falten (`isna`, `dropna`, `fillna`): [FO_02 §6]({FO02}) i [EX_00 §3]({EX00})
- Columnes de text i `OneHotEncoder`: [EX_00 §4]({EX00})
- `Pipeline` i `ColumnTransformer`: [EX_00 §6]({EX00}) i [EX_05]({EX05})
- Validació creuada (`cross_val_score`): [EX_00 §9]({EX00})"""),
         md("""## Les dades

**Automobile / imports-85** (UCI Machine Learning Repository, J. Schlimmer, 1987). Llicència
CC BY 4.0. Cada fila és **un model de cotxe del 1985**: la fitxa tècnica (marca, carrosseria, motor,
mides, consum...), una puntuació de risc de l'assegurança (`symboling`) i el **preu** en dòlars.

El fitxer no té capçalera. Què vol dir cada columna, i quins valors hi pot haver, ho explica el
fitxer de descripció: <https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.names>"""),
         CARREGA["301"](),
         caixa([
             ("`df.dtypes`, `df.info()`", "el tipus de cada columna"),
             ("`df[col].unique()`, `value_counts()`", "quins valors diferents hi ha, i quants de cada"),
             ("`pd.to_numeric(serie, errors='coerce')`", "converteix a número; el que no pot, ho deixa com a `NaN`"),
             ("`pd.read_csv(..., na_values=...)`", "quins textos s'han de llegir com a valor que falta"),
             ("`df.isna().sum()`, `dropna(subset=[...])`", "comptar nuls; esborrar files amb nul en unes columnes concretes"),
             ("`SimpleImputer(strategy=...)`", "omple els nuls amb un valor après de l'entrenament"),
             ("`OneHotEncoder(handle_unknown=...)`", "columnes 0/1 per a cada categoria"),
             ("`make_column_transformer`, `make_pipeline`", "encadenar la preparació i el model en un sol objecte"),
             ("`KFold(n_splits=5, shuffle=True, random_state=0)`", "una partició en 5 trossos que pots reutilitzar"),
             ("`cross_val_score(model, X, y, cv=..., scoring='neg_mean_absolute_error')`", "l'error absolut mitjà (MAE) en cada tros, amb el signe canviat"),
             ("`DummyRegressor()`", "el model que sempre diu la mitjana: la referència"),
             ("`LinearRegression()`, `DecisionTreeRegressor()`, `RandomForestRegressor()`", "tres models de regressió"),
             ("`mean_absolute_error(y_real, y_predit)`", "l'error absolut mitjà"),
         ]),
         md("## Nivell 1 · Explorar")]
    c += tasca("1.1 · Què diu pandas, i què diu la UCI",
               """Mira la forma i el tipus de cada columna. Compara-ho amb el fitxer de descripció de la UCI:
hi ha columnes que la UCI diu que són `continuous` i pandas no les llegeix com a números? Quines?""",
               """la teva llista de columnes «sospitoses» ha de quadrar amb el fitxer de descripció: cada
columna que hi apunts ha de ser `continuous` a la UCI i `object` (o `str`) a `df.dtypes`.""",
               "Una columna de números es llegeix com a text quan **una sola** cel·la no és un número.",
               "`df.dtypes` al costat de la secció *Attribute Information* del fitxer `.names`.",
               "`df.select_dtypes(exclude='number').columns`, i d'aquesta llista, treu les que són categories de debò.",
               resposta=True)
    c += tasca("1.2 · Per què passa",
               """Troba **quins valors** impedeixen que aquestes columnes siguin numèriques. Quan ho sàpigues,
**torna a carregar** el fitxer de manera que pandas ho entengui a la primera, sense arreglar les
columnes a mà una per una.""",
               """després de tornar a carregar, `df.select_dtypes('number').shape[1] == 16`, i el nombre total de
`NaN` (`df.isna().sum().sum()`) és exactament el nombre de cel·les de **tota** la taula original que
tenien aquell valor estrany (compta'l també a les columnes de text).""",
               "Si una columna hauria de ser numèrica, el valor culpable és el que **no** es pot convertir a número.",
               "`pd.to_numeric(df[col], errors='coerce')` et diu quines cel·les no es poden convertir: les que hi passen a `NaN`.",
               "`df.loc[pd.to_numeric(df[col], errors='coerce').isna(), col].unique()`, i després el paràmetre `na_values` de `read_csv`.")
    c += tasca("1.3 · L'inventari de forats",
               """Ara que pandas els veu: quines columnes tenen valors que falten, quants, i quina proporció
de la taula són? Hi ha files sense **preu**?""",
               "la suma de la teva taula de nuls per columna és igual a `df.isna().sum().sum()`.",
               "Ordena: la columna amb més forats és la primera decisió que hauràs de prendre.",
               "`df.isna().sum()` i `df.isna().mean()`.",
               "`df.isna().sum()[lambda s: s > 0].sort_values(ascending=False)`",
               resposta=True)
    c.append(xavi("Aquesta columna amb tants forats, la tiro o la imputo?",
                  "Un valor que falta, el puc omplir amb la mitjana de tota la taula?"))
    c.append(md("## Nivell 2 · Respondre"))
    c += tasca("2.1 · L'objectiu i les dades d'entrada",
               """Separa `X` (la fitxa) i `y` (el preu). Què fas amb els cotxes que no tenen preu? Escriu per
què. (Pensa què vol dir *imputar* l'objectiu: amb quina resposta estaries entrenant el model?)""",
               "`y.isna().sum() == 0`, `len(X) == len(y)` i `'price' not in X.columns`.",
               "El preu és el que vols aprendre. Un preu inventat és una resposta inventada.",
               "`df.dropna(subset=[...])`",
               "`dades = df.dropna(subset=['price'])` i després `X = dades.drop(columns='price')`.",
               resposta=True)
    c += tasca("2.2 · La referència",
               """Abans de cap model de debò: quin error té un model que **sempre diu el preu mitjà**? Fes-ho
amb validació creuada de 5 trossos, i guarda la partició (`cv`) en una variable: la faràs servir
per a **tots** els models d'aquí endavant, perquè siguin comparables.""",
               """`cross_val_score` torna 5 números; l'MAE (el número amb el signe girat) és positiu i és de
l'ordre de milers de dòlars.""",
               "Si un model no millora aquest número, no ha après res.",
               "`DummyRegressor()` i `KFold(n_splits=5, shuffle=True, random_state=0)`.",
               "`-cross_val_score(DummyRegressor(), X, y, cv=cv, scoring='neg_mean_absolute_error')`")
    c += tasca("2.3 · El Pipeline",
               """Munta un `Pipeline` que faci **tota** la preparació (omplir nuls de les numèriques, omplir nuls i
codificar les de text) i el model, i avalua'l amb la mateixa validació creuada. Prova com a mínim
dos models diferents.

Si et peta o et surten `nan`, llegeix l'avís sencer: et diu què ha vist en un tros de validació
que no havia vist en entrenar.""",
               """cap dels 5 números de `cross_val_score` és `nan` (`np.isnan(scores).sum() == 0`), i el
`Pipeline` s'entrena directament amb `X` tal com ve de la tasca 2.1, sense haver omplert ni
codificat res abans a mà.""",
               "Per què és important que l'imputador s'entreni **dins** de cada tros i no amb tota la taula?",
               "`make_column_transformer((SimpleImputer(...), numeriques), (make_pipeline(SimpleImputer(...), OneHotEncoder(...)), text))`.",
               "Amb 205 cotxes, hi ha marques amb un sol cotxe: `OneHotEncoder(handle_unknown='ignore')`.")
    c += tasca("2.4 · Quin número dones al cap",
               """Entrena el millor model amb totes les dades i calcula'n l'MAE **sobre les mateixes dades
d'entrenament**. Compara'l amb el de la validació creuada. Quin dels dos li diries al cap, i per
què?""",
               "l'MAE d'entrenament d'un arbre sense límit de profunditat és més petit que el de validació creuada.",
               "Un examen amb les mateixes preguntes que els exercicis, què mesura?",
               "`model.fit(X, y)` i `mean_absolute_error(y, model.predict(X))`.",
               "Posa al costat `mean_absolute_error(y, model.predict(X))` i `(-scores).mean()`.",
               resposta=True)
    c += tasca("2.5 · La resposta",
               """Respon l'encàrrec: amb quin error es pot estimar el preu? Dona'l en dòlars i també relatiu al
preu típic d'un cotxe. Quant varia d'un tros de validació a un altre? Te'l creuries?""",
               "el teu error relatiu és l'MAE dividit pel preu mitjà (o la mediana): digues quin dels dos fas servir.",
               "Un error de 2.000 $ no és el mateix en un cotxe de 6.000 que en un de 40.000.",
               "`scores.mean()`, `scores.std()` i `y.median()`.",
               "`(-scores).mean() / y.median()`",
               resposta=True)
    c.append(xavi("L'error em canvia molt d'un tros a l'altre: quin número dono?",
                  "Un model millora la referència però poc: val la pena?"))
    c.append(md("## Nivell 3 · Més enllà"))
    c += oberta("3.1 · Números escrits amb lletres",
                """Hi ha columnes que són números però estan escrites amb paraules. Converteix-les a número i
compara l'error amb el que tenies quan les tractaves com a text. Millora? Per què podria ser?""",
                "Mira `value_counts()` de les columnes de text: quines tenen un ordre natural?",
                "`serie.map({...})` amb un diccionari.",
                "`{'two': 2, 'three': 3, 'four': 4, ...}`")
    c += oberta("3.2 · Errors grans i errors petits",
                """Mira on s'equivoca més el model: en cotxes barats o cars? Prova d'entrenar sobre el
logaritme del preu (`TransformedTargetRegressor`) i compara l'MAE en dòlars.""")
    c += la_teva_pregunta("3.3")
    c.append(xavi("Aquesta millora, és de debò o és soroll de la partició?"))
    c += lliurament("quin error es pot prometre i amb quin model, quina decisió de neteja t'ha "
                    "costat més i per què, i de què no estàs segur.")
    return c


# ===========================================================================
# RE_302 · Accidents de Barcelona, dos anys
# ===========================================================================
def re_302():
    c = [md(f"""# RE_302 · El 2024 va ser pitjor?

{CAP_B3.format(n=2)}

Treballes a l'àrea de Mobilitat de l'Ajuntament de Barcelona. La regidora ha de presentar el
balanç de sinistralitat i et demana una cosa concreta:

- **Comparat amb el 2023, el 2024 els accidents van ser més greus?** Vol el nombre de **morts** i
  de **ferits greus per cada 1.000 accidents**, per a tota la ciutat i per districte.

Tens els dos fitxers que publica la Guàrdia Urbana, un per any, amb les mateixes columnes. Has de
lliurar **una sola taula amb els dos anys** i la comparació."""),
         md(f"""## Què necessites saber abans

- Seleccionar, filtrar, `groupby` i `pivot_table`: [FO_02 §4-§8]({FO02})
- Valors que falten i duplicats: [EX_00 §3 i §5]({EX00})
- El diagnòstic d'una taula bruta: [EX_05, exercici 1]({EX05})"""),
         md("""## Les dades

**Accidents gestionats per la Guàrdia Urbana a Barcelona**, fitxers de 2023 i 2024 (Open Data BCN,
conjunt `accidents-gu-bcn`). Llicència CC BY 4.0, font: Ajuntament de Barcelona. Cada fila és **un
accident** amb número d'expedient, lloc (districte, barri, carrer), data i hora, i el nombre de
víctimes de cada gravetat.

Són dades vives que l'Ajuntament pot tornar a publicar: per això en fem servir una **còpia
congelada** (baixada el 14-oct-2026) que és al repositori del curs."""),
         CARREGA["302"](),
         caixa([
             ("`df.dtypes`, `df.isna().sum()`", "tipus i nuls de cada columna"),
             ("`pd.DataFrame({'2023': ..., '2024': ...})`", "posar dues sèries una al costat de l'altra per comparar-les"),
             ("`value_counts(dropna=False)`", "quants de cada valor, **comptant també els `NaN`**"),
             ("`set(a) - set(b)`, `set(a) ^ set(b)`", "valors que hi ha en un conjunt i no en l'altre"),
             ("`serie.str.strip()`, `serie.str.replace(...)`", "treure espais del principi i del final; substituir text"),
             ("`serie.replace({...})`, `fillna(...)`", "canviar uns valors per uns altres; omplir nuls"),
             ("`pd.to_numeric(..., errors='coerce')`", "passar text a número"),
             ("`duplicated(subset=[...])`, `is_unique`", "files repetides segons unes columnes; si una columna no repeteix cap valor"),
             ("`pd.concat([a, b], ignore_index=True)`", "apilar dues taules"),
             ("`groupby(...).agg(...)`, `pivot_table(...)`", "resumir per grups"),
             ("`assert condicio, 'missatge'`", "atura't si una propietat que esperes no es compleix"),
         ]),
         md("## Nivell 1 · Explorar")]
    c += tasca("1.1 · Les mateixes columnes?",
               """Els dos fitxers tenen les mateixes columnes amb el mateix nom. Tenen també el **mateix tipus**?
Fes una taula amb una fila per columna i el tipus de cada any al costat. Quines no coincideixen?""",
               "la teva taula té 25 files, una per columna, i dues columnes (2023 i 2024).",
               "Una columna que un any és `int64` i l'altre `float64`, o `object` i `float64`, ja t'està dient alguna cosa.",
               "`pd.DataFrame({'2023': a23.dtypes, '2024': a24.dtypes})`",
               "Filtra les files on les dues columnes són diferents: `taula[taula['2023'] != taula['2024']]`.",
               resposta=True)
    c += tasca("1.2 · Els nuls, any per any",
               """Fes el mateix amb els valors que falten: quants `NaN` té cada columna cada any? Per a les
columnes on la diferència és gran, mira `value_counts(dropna=False)` d'**un any i de l'altre**.
Ha canviat la realitat d'un any a l'altre, o la manera d'apuntar-la?""",
               """per a cada columna que estudiïs, la suma dels recomptes de `value_counts(dropna=False)` és el
nombre de files d'aquell any.""",
               "Si un any hi ha milers de nuls i l'altre cap, mira quin valor té l'altre any on aquest té el nul.",
               "`a23[col].value_counts(dropna=False)` al costat de `a24[col].value_counts(dropna=False)`.",
               "Mira sobretot les columnes de víctimes i la de la causa del vianant.",
               resposta=True)
    c += tasca("1.3 · Els noms dels llocs",
               """Els districtes i els barris, s'escriuen igual els dos anys? Compara els conjunts de noms. Mira
també si els textos tenen espais de més, i si hi ha codis que no corresponguin a cap lloc.""",
               """quan dos conjunts són iguals, `set(a) ^ set(b)` és buit; si no ho és, el que hi surt és
exactament el que has d'explicar.""",
               "Un text amb espais al final no és igual al mateix text sense: per a pandas són dues categories.",
               "`set(a23['Nom_barri']) ^ set(a24['Nom_barri'])`, i `value_counts()` dels codis de districte.",
               "`(s.str.strip() != s).sum()` compta quants textos tenen espais sobrants.",
               resposta=True)
    c.append(xavi("Aquest valor que només surt un any, és un error o una categoria de debò?",
                  "Un nul aquí vol dir «zero» o vol dir «no se sap»? Com ho puc saber del cert?"))
    c.append(md("## Nivell 2 · Respondre"))
    c += tasca("2.1 · La resposta ràpida (i desconfiada)",
               """Ajunta les dues taules **tal com venen** i calcula, per a cada any, els morts per accident i els
ferits greus per accident (la mitjana de les columnes). Apunta els números. Te'ls creus?""",
               "`len(tot) == len(a23) + len(a24)`.",
               "La mitjana d'una columna amb `NaN`, sobre quantes files es calcula?",
               "`pd.concat([a23, a24], ignore_index=True)` i `groupby('NK_Any')[...].mean()`.",
               "Compara `.mean()` amb `.sum() / .size()` del mateix grup.",
               resposta=True)
    c += tasca("2.2 · Una funció de neteja",
               """Escriu **una funció** `neteja(df)` que deixi qualsevol dels dos anys en un format comú: mateixos
tipus, mateixa manera d'escriure els zeros i els noms, sense espais sobrants. Fes-la servir per
als dos anys (no arreglis un any a mà). Cada decisió que prenguis, escriu-la en una línia.""",
               """totes aquestes propietats són certes per a `n23 = neteja(a23)` i `n24 = neteja(a24)`:

- `(n23.dtypes == n24.dtypes).all()`
- cap columna de text té espais al principi o al final;
- a totes les files dels dos anys, `Numero_victimes` és la suma de lleus, greus i morts;
- la funció no esborra ni afegeix files que no hagis decidit esborrar (compta-les).""",
               "Primer fes la llista de diferències de les tasques 1.1 a 1.3; la funció és aquesta llista en codi.",
               "`df = df.copy()` al principi, i després `str.strip()`, `fillna(...)`, `astype(...)`, `replace({...})`.",
               "Per a les columnes de text: `for col in df.select_dtypes(exclude='number'): df[col] = df[col].str.strip()`.",
               resposta=True)
    c += tasca("2.3 · Un accident, una fila",
               """El número d'expedient identifica un accident. És únic dins de cada any? I un cop netejat? Si
hi ha repetits, mira'ls sencers abans de decidir què en fas.""",
               """després de la teva decisió, `tot['Numero_expedient'].is_unique` és `True`, i saps quantes
files has tret i per què.""",
               "Un expedient repetit pot ser la mateixa fila dues vegades o dues files diferents amb el mateix número.",
               "`duplicated(subset='Numero_expedient', keep=False)` per veure'ls tots.",
               "`tot[tot.duplicated('Numero_expedient', keep=False)].sort_values('Numero_expedient')`",
               resposta=True)
    c += tasca("2.4 · La taula per a la regidora",
               """Amb les dades netes, calcula per a cada any i per a cada districte: nombre d'accidents, morts i
ferits greus, i morts i ferits greus **per cada 1.000 accidents**. Decideix què fas amb els
accidents que no tenen districte conegut, i digues-ho a la taula.""",
               """la suma dels accidents de cada any a la taula és el nombre de files d'aquell any (després de les
teves decisions); i el total de morts de cada any és el mateix que dona `a23` i `a24` sense
netejar amb `.sum()` (netejar no ha de crear ni fer desaparèixer cap mort).""",
               "Fes primer la taula de tota la ciutat (dues files) i després la de districtes.",
               "`groupby(['NK_Any', 'Nom_districte']).agg(accidents=(..., 'size'), morts=(..., 'sum'), ...)`",
               "Després, `taula['morts_1000'] = 1000 * taula['morts'] / taula['accidents']`, i `unstack('NK_Any')` per posar els anys de costat.")
    c += tasca("2.5 · La resposta",
               """Respon la regidora: el 2024 els accidents van ser més greus que el 2023? Quins districtes han
canviat més? Compara-ho amb el que havies dit a la tasca 2.1.""",
               """els números de tota la ciutat que dones surten de la taula de la 2.4, i són coherents amb els
totals de morts i ferits greus de cada any.""",
               "Amb tan pocs morts per any, un canvi d'un o dos morts en un districte és molt o poc?",
               "Mira la diferència entre anys i també el nombre absolut del qual surt.",
               "`taula.sort_values(...)` per la diferència entre els dos anys.",
               resposta=True)
    c.append(xavi("Els números de districte canvien molt però són pocs casos: ho puc dir igualment?",
                  "Les files sense districte: les trec, o les deixo en una fila a part?"))
    c.append(md("## Nivell 3 · Més enllà"))
    c += oberta("3.1 · On són",
                """Dibuixa els accidents amb la longitud i la latitud, un color per any. Les columnes de
coordenades UTM, diuen el mateix els dos anys? Quina faries servir?""",
                "Un mapa de punts és un `scatter` de longitud contra latitud.",
                "`plt.scatter(lon, lat, s=1, alpha=0.3)`",
                "Mira els rangs de les dues columnes UTM: quina té valors d'ordre 4,5 milions?")
    c += oberta("3.2 · Altres diferències",
                """Busca alguna altra diferència entre els dos fitxers que no hagis arreglat (pista: el número
postal). Afegeix-la a `neteja` i torna a comprovar totes les propietats de la 2.2.""")
    c += la_teva_pregunta("3.3")
    c.append(xavi("He trobat més coses rares que no afecten la pregunta: les arreglo igualment?"))
    c += lliurament("la resposta a la regidora amb els números, quines diferències entre els dos "
                    "fitxers t'haurien fet donar una resposta falsa, i de què no estàs segur.")
    return c


# ===========================================================================
# RE_303 · Hotels
# ===========================================================================
def re_303():
    c = [md(f"""# RE_303 · Es cancel·larà aquesta reserva?

{CAP_B3.format(n=3)}

Ets la persona de dades d'una petita cadena amb **dos hotels a Portugal**, un de ciutat i un de
platja. Una de cada tres reserves acaba cancel·lada, i la direcció vol fer *overbooking* amb cap:
quan entra una reserva nova, saber si és probable que es cancel·li.

- **Quina encert (*accuracy*) es pot prometre a la direcció, amb un model que funcioni el dia que
  entra la reserva?** Han de poder-se'l creure, perquè hi posaran clients al carrer si s'equivoca."""),
         md(f"""## Què necessites saber abans

- Partir les dades i la fuita d'informació: [EX_00 §1 i §2]({EX00})
- Valors que falten, text i duplicats: [EX_00 §3, §4 i §5]({EX00})
- `Pipeline`, `ColumnTransformer` i la referència (`DummyClassifier`): [EX_00 §6 i §7]({EX00})
- Importància de les columnes: [EX_00 §8]({EX00})"""),
         md("""## Les dades

**Hotel booking demand** (N. Antonio, A. de Almeida i L. Nunes, *Data in Brief*, 2019), via
TidyTuesday (2020-02-11). Llicència CC BY 4.0. Cada fila és **una reserva** feta entre 2015 i
2017 en un dels dos hotels: quan es va fer, per a quan, quantes persones, quin règim, quin canal,
quin preu per nit (`adr`)... i si es va cancel·lar (`is_canceled`). No hi ha noms ni contactes.

El diccionari de columnes és a
<https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-02-11>. **Llegeix-lo**:
el necessitaràs."""),
         CARREGA["303"](),
         caixa([
             ("`df.isna().sum()`, `df.duplicated().sum()`", "nuls i files repetides"),
             ("`value_counts(normalize=True)`", "la proporció de cada valor"),
             ("`pd.crosstab(a, b)`", "taula de recomptes de dues columnes"),
             ("`train_test_split(..., stratify=y, random_state=0)`", "partir mantenint la proporció de classes"),
             ("`DummyClassifier()`", "el model que sempre diu la classe més freqüent: la referència"),
             ("`make_column_selector(dtype_include='number')`", "triar les columnes d'un tipus dins d'un `ColumnTransformer`"),
             ("`SimpleImputer`, `OneHotEncoder(handle_unknown='ignore', min_frequency=...)`", "omplir nuls; codificar text agrupant les categories rares"),
             ("`make_column_transformer`, `make_pipeline`", "la preparació i el model en un sol objecte"),
             ("`DecisionTreeClassifier(max_depth=...)`, `RandomForestClassifier(n_jobs=-1)`", "dos classificadors (el bosc, amb tots els nuclis)"),
             ("`pipe[-1].feature_importances_`, `pipe[:-1].get_feature_names_out()`", "quant ha fet servir el model cada columna, i el seu nom"),
             ("`df.merge(..., how='left', indicator=True)`", "creuar dues taules i saber quines files hi són a les dues"),
         ]),
         md("## Nivell 1 · Explorar")]
    c += tasca("1.1 · La foto",
               """Forma, tipus i nuls. Quina proporció de reserves es cancel·len? Quina *accuracy* tindria un
model que digués sempre la classe més freqüent?""",
               "la proporció de cancel·lades i la de no cancel·lades sumen 1, i l'*accuracy* del model ximple és la més gran de les dues.",
               "Aquesta *accuracy* és la línia de sortida de tot el repte.",
               "`df['is_canceled'].value_counts(normalize=True)`",
               "`DummyClassifier().fit(X, y).score(X, y)` hauria de donar el mateix número.")
    c += tasca("1.2 · Files repetides",
               """Quantes files són idèntiques a una altra? Mira-ne unes quantes. Poden ser reserves diferents que
coincideixen en tot, o són un error? Tingues en compte quines columnes **no** hi ha a la taula.""",
               "el nombre de duplicats més el nombre de files úniques (`len(df.drop_duplicates())`) és `len(df)`.",
               "Hi ha cap columna que identifiqui la reserva o el client?",
               "`df[df.duplicated(keep=False)].head(10)`",
               "Compara la proporció de cancel·lades entre les files repetides i les que no: `df.groupby(df.duplicated(keep=False))['is_canceled'].mean()`.",
               resposta=True)
    c.append(xavi("Els duplicats, els trec o els deixo? Són reserves de grup?",
                  "Un buit a `agent` o a `company` vol dir «no n'hi ha» o «no se sap»?"))
    c.append(md("## Nivell 2 · Respondre"))
    c += tasca("2.1 · El primer model, sense pensar",
               """Fes servir **totes** les columnes (menys l'objectiu) en un `Pipeline` amb imputació i one-hot, i
entrena un arbre de decisió de profunditat 3. Quina *accuracy* treu al test? Compara-la amb la
referència de la 1.1. És creïble?""",
               "el `Pipeline` rep el `DataFrame` cru (amb nuls i text) i no peta; l'*accuracy* és un número entre 0 i 1.",
               "Un arbre de profunditat 3 només pot fer 3 preguntes seguides. Mira quines ha fet.",
               "`DecisionTreeClassifier(max_depth=3, random_state=0)` i `export_text` o `plot_tree` del model del final del `Pipeline`.",
               "`export_text(pipe[-1], feature_names=list(pipe[:-1].get_feature_names_out()))`",
               resposta=True)
    c += tasca("2.2 · Què sap el model que no hauria de saber",
               """Fes la pregunta columna per columna: **aquest valor, el sé el dia que entra la reserva?** Llegeix
el diccionari de dades. Fes una llista de les columnes que no es poden fer servir i, per a cada
una, escriu en una línia per què. Comprova la teva sospita amb una taula creuada contra
l'objectiu.""",
               """cap de les columnes de la teva llista és dins de `X` quan entrenes el model següent
(`set(llista) & set(X.columns) == set()`), i l'*accuracy* del mateix arbre sense elles baixa.""",
               "Pensa en el moment en què s'escriu cada columna: en fer la reserva, en arribar a l'hotel, en marxar?",
               "El diccionari de dades: llegeix la descripció de cada columna, sobretot de les que el primer arbre ha fet servir.",
               "`pd.crosstab(df[col], df['is_canceled'])` per a cada columna de text: si una separa les dues classes gairebé sense error, pregunta't quan s'escriu.",
               resposta=True)
    c += tasca("2.3 · Els duplicats i el test",
               """Parteix en entrenament i test **sense** treure els duplicats. Quina proporció de files del test
té una còpia exacta a l'entrenament? Després entrena un bosc aleatori dues vegades —amb duplicats
i sense— i compara l'*accuracy* de test. Quina diferència hi ha, i per què?""",
               """la proporció és un número entre 0 i 1; després de `drop_duplicates()`, `df.duplicated().sum() == 0`; i
els dos boscos fan servir exactament les mateixes columnes.""",
               "Si una fila del test és idèntica a una de l'entrenament, el model ja coneix la resposta.",
               "`X_test.merge(X_train.drop_duplicates(), how='left', indicator=True)`",
               "`(fusio['_merge'] == 'both').mean()`",
               resposta=True)
    c += tasca("2.4 · El número honest",
               """Amb les decisions de la 2.2 i la 2.3, entrena el model final i dona'n l'*accuracy* de test, al
costat de la referència (que també canvia si has tret duplicats: torna-la a calcular).""",
               "la referència i el model es mesuren sobre el **mateix** test.",
               "Un model val el que millora la referència, no el seu número sol.",
               "`DummyClassifier().fit(X_train, y_train).score(X_test, y_test)`",
               "Dona les dues *accuracy* i la diferència.",
               resposta=True)
    c.append(xavi("He tret una columna que potser sí que es coneix el dia de la reserva: m'he passat?",
                  "El model és pitjor ara que abans. He fet alguna cosa malament?"))
    c.append(md("## Nivell 3 · Més enllà"))
    c += oberta("3.1 · Partir pel temps",
                """Un model es fa servir amb reserves **futures**. Entrena amb les arribades de 2015 i 2016 i
avalua amb les de 2017. Quina *accuracy* surt, comparada amb la partició aleatòria? Quina és més
honesta per a l'encàrrec?""",
                "Les dates d'arribada estan partides en tres columnes; amb l'any n'hi ha prou.",
                "`df['arrival_date_year'] < 2017` com a màscara.",
                "Recorda treure els duplicats abans i les columnes de la 2.2.")
    c += oberta("3.2 · Valors estranys",
                """Mira `adr` (preu per nit), `adults` i `meal`. Hi ha valors sense sentit, o categories que volen
dir el mateix? Què en faries, i canvia el resultat?""")
    c += la_teva_pregunta("3.3")
    c.append(xavi("La partició per temps dona pitjor: quin número dono a la direcció?"))
    c += lliurament("quina *accuracy* prometries i per què és honesta, quines columnes has tret "
                    "i per què, i què has decidit amb els duplicats.")
    return c


# ===========================================================================
# RE_304 · Certificats energetics
# ===========================================================================
def re_304():
    c = [md(f"""# RE_304 · Quina lletra traurà el meu pis?

{CAP_B3.format(n=4)}

Treballes en una empresa petita de rehabilitació energètica. Volen posar a la web una calculadora:
el propietari hi entra les dades del seu habitatge **que pot saber sense contractar cap tècnic**
(població, zona climàtica, any de construcció, metres, tipus d'edifici...) i la calculadora li diu
quina **lletra de consum** (de la A a la G) és probable que tregui al certificat energètic.

- **Quin F1 *macro* es pot prometre, honestament, amb només aquestes dades?** I on s'equivoca?

Aquest és el repte més complet del bloc: aquí ningú no et dirà què està brut."""),
         md(f"""## Què necessites saber abans

- Tot el que surt a [EX_00 §3-§9]({EX00}): nuls, text, duplicats, `Pipeline`, mètriques i validació creuada
- El F1 i la matriu de confusió: [EX_00 §7]({EX00})
- Un `Pipeline` amb dades brutes de cap a peus: [EX_05]({EX05})"""),
         md("""## Les dades

**Certificats d'eficiència energètica d'edificis** (Institut Català d'Energia, conjunt `j6ii-t3w2`
de Dades Obertes de la Generalitat). Llicència oberta d'ús d'informació – Catalunya. Cada fila és
**un certificat energètic** d'un habitatge o local. El conjunt sencer té més d'un milió de
certificats; aquí en tens una **mostra aleatòria de 30.000**, congelada al repositori el
14-oct-2026, i **sense cap adreça** (ni carrer, ni número, ni referència cadastral, ni
coordenades).

L'objectiu és `qualificaci_de_consum_d` (sí, el nom està tallat). La descripció de les columnes és
a <https://analisi.transparenciacatalunya.cat/d/j6ii-t3w2>."""),
         CARREGA["304"](),
         caixa([
             ("`df.dtypes`, `isna().mean()`, `describe()`", "tipus, proporció de nuls, resum de les numèriques"),
             ("`value_counts()`, `nunique()`", "quantes categories hi ha i quantes files té cada una"),
             ("`df.groupby(objectiu)[col].describe()`", "com es reparteix una columna dins de cada lletra"),
             ("`serie.str.lower()`, `str.strip()`, `serie.replace({...})`, `serie.map(...)`", "normalitzar textos i ajuntar categories"),
             ("`serie.where(condicio)`", "deixa el valor si la condició es compleix i posa `NaN` si no"),
             ("`FunctionTransformer(funcio)`", "converteix una funció teva en un pas d'un `Pipeline`"),
             ("`SimpleImputer`, `OneHotEncoder(handle_unknown='ignore', min_frequency=...)`", "omplir nuls; codificar text"),
             ("`make_column_transformer`, `make_pipeline`", "la preparació i el model en un sol objecte"),
             ("`StratifiedKFold`, `cross_val_score(..., scoring='f1_macro')`", "validació creuada mantenint les proporcions de les lletres"),
             ("`DummyClassifier(strategy=...)`", "la referència"),
             ("`RandomForestClassifier(n_jobs=-1)`", "un bosc aleatori"),
             ("`f1_score(..., average='macro')`, `ConfusionMatrixDisplay.from_predictions`", "el F1 mitjà de les set lletres; la matriu dibuixada"),
         ]),
         md("## Nivell 1 · Explorar")]
    c += tasca("1.1 · La foto",
               """Forma, tipus, nuls i duplicats. Com es reparteixen les lletres? Quin F1 *macro* tindria un model
que digués sempre la lletra més freqüent? I un que les digués a l'atzar respectant les proporcions?""",
               "els recomptes de les lletres sumen 30.000; el F1 *macro* del model que diu sempre la mateixa lletra és més petit que la seva *accuracy*.",
               "El F1 *macro* fa la mitjana de les set lletres, i una lletra que el model no diu mai hi compta amb un zero.",
               "`DummyClassifier(strategy='most_frequent')` i `DummyClassifier(strategy='stratified', random_state=0)`.",
               "`f1_score(y, dummy.predict(X), average='macro')`")
    c += tasca("1.2 · Les columnes de text",
               """Per a cada columna de text, quantes categories té? Mira de prop les que en tenen més d'una
dotzena: **quantes categories reals** hi ha, si les llegeixes com ho faria una persona? Escriu una
funció que les ajunti.""",
               """després d'aplicar la funció, cada columna que has tractat té menys categories que abans, i la
suma de `value_counts(dropna=False)` continua sent 30.000 (no has perdut cap fila).""",
               "Llegeix les categories una per una, en veu alta. Algunes diuen el mateix de maneres diferents.",
               "`df[col].value_counts()` sencer, no només el `head()`.",
               "Un diccionari `{'escrit així': 'categoria bona', ...}` i `serie.replace(diccionari)`; o regles amb `str.contains(...)`.",
               resposta=True)
    c += tasca("1.3 · Els números plausibles",
               """Mira el mínim i el màxim de cada columna numèrica que podria conèixer el propietari. Quins valors
són impossibles o molt sospitosos? Decideix uns límits i converteix el que en quedi fora en `NaN`
(no esborris files).""",
               "`len(df)` no canvia; i amb els teus límits, `serie.dropna().between(minim, maxim).all()` és `True`.",
               "Un any de construcció, quin és el mínim raonable a Catalunya? I uns metres?",
               "`describe()` i `sort_values().head(20)` / `.tail(20)`.",
               "`serie.where(serie.between(minim, maxim))`",
               resposta=True)
    c.append(xavi("Aquests anys tan antics, són errors o hi ha edificis així?",
                  "Una categoria escrita en castellà i en català: segur que és la mateixa?"))
    c.append(md("## Nivell 2 · Respondre"))
    c += tasca("2.1 · El primer model, amb tot",
               """Entrena un bosc aleatori amb totes les columnes (menys l'objectiu i `data_entrada`) dins d'un
`Pipeline`. Quin F1 *macro* treu amb validació creuada de 5 trossos estratificats? Compara'l amb la
referència.""",
               "`cross_val_score` torna 5 números, cap `nan`, i la seva mitjana és més gran que la referència.",
               "Guarda la partició en una variable, la necessitaràs a cada model.",
               "`StratifiedKFold(n_splits=5, shuffle=True, random_state=0)`",
               "`cross_val_score(pipe, X, y, cv=cv, scoring='f1_macro', n_jobs=-1)`",
               resposta=True)
    c += tasca("2.2 · Què sabrà el propietari, i què no",
               """Torna a l'encàrrec: el propietari **no té** el certificat. Fes la llista de columnes que **surten
del càlcul del certificat** i que, per tant, la calculadora no tindrà. Comprova cada sospita mirant
com es reparteix aquella columna dins de cada lletra. Entrena el mateix model sense elles.""",
               """`set(llista) & set(X.columns) == set()`, i cada columna de la llista té una línia que explica per
què hi és.""",
               "Si saps el consum d'un pis, ja saps gairebé la lletra. Qui calcula aquest consum?",
               "La descripció de les columnes del conjunt: quines són dades de l'edifici i quines són resultats del càlcul?",
               "`df.groupby('qualificaci_de_consum_d')[numeriques].median()` i `pd.crosstab` per a les de text: si una columna creix (o canvia) sense excepció de la A a la G, pregunta't qui la calcula.",
               resposta=True)
    c += tasca("2.3 · El Pipeline que neteja sol",
               """Posa la neteja de la 1.2 i la 1.3 **dins** del `Pipeline` (amb `FunctionTransformer`), de manera
que el `Pipeline` accepti la taula **tal com es carrega**. Avalua'l amb la mateixa validació creuada.""",
               """`pipe.fit(X_cru, y)` funciona amb `X_cru` sortit directament de `df` (sense haver fet cap neteja
a mà abans), i el F1 *macro* és un número que pots comparar amb el de la 2.2.""",
               "Per què és millor que la neteja visqui dins del `Pipeline` que fer-la abans a mà?",
               "`make_pipeline(FunctionTransformer(neteja), preparacio, model)`",
               "La funció rep un `DataFrame` i en torna un altre: `def neteja(X): X = X.copy(); ...; return X`.")
    c += tasca("2.4 · On s'equivoca",
               """Fes la matriu de confusió del model final (amb una partició d'entrenament i test). Quan s'equivoca,
s'equivoca per una lletra o per moltes? Quines lletres confon més, i per què pot ser?""",
               "la matriu és 7×7, en ordre A-G, i la suma de totes les caselles és el nombre de files del test.",
               "Les lletres tenen ordre. Un error de A per B no és el mateix que de A per G.",
               "`ConfusionMatrixDisplay.from_predictions(y_test, y_pred, labels=list('ABCDEFG'))`",
               "Per mesurar la distància: passa les lletres a números (`'ABCDEFG'.index(l)`) i fes la mitjana de la diferència absoluta.",
               resposta=True)
    c += tasca("2.5 · La resposta",
               """Respon l'encàrrec: quin F1 *macro* es pot prometre, quant més alt sortia amb el primer model, i
per què el primer no valia. Afegeix una frase sobre si la calculadora és útil tal com està.""",
               "els dos F1 que comparis estan calculats amb la mateixa validació creuada.",
               "Útil per a qui? Una persona que vol saber si val la pena rehabilitar.",
               "Posa'ls en una taula: referència, primer model, model honest.",
               "`pd.Series({...})`",
               resposta=True)
    c.append(xavi("Aquesta columna la pot saber el propietari o no?",
                  "El F1 honest em surt baix: el model és dolent o les dades no donen per a més?"))
    c.append(md("## Nivell 3 · Més enllà"))
    c += oberta("3.1 · Sense pensar en l'ordre",
                """Un error de B per C hauria de comptar menys que un de A per G. Inventa una mètrica que ho
tingui en compte (per exemple, l'error mitjà en lletres) i compara models amb ella.""")
    c += oberta("3.2 · El que no és text ni número",
                """Les columnes `SI`/`NO` tenen nuls. Vol dir «no», o «no consta»? Prova de tractar el nul com una
categoria pròpia i mira si canvia res.""")
    c += la_teva_pregunta("3.3")
    c.append(xavi("Puc fer servir la població o el codi postal, o és massa detall?"))
    c += lliurament("el F1 honest i com l'has obtingut, quines columnes has tret i per què, quina "
                    "neteja t'ha canviat més el resultat, i de què no estàs segur.")
    return c


# ===========================================================================
# RE_401 · Clients d'un majorista
# ===========================================================================
def re_401():
    c = [md(f"""# RE_401 · Quins tipus de clients tenim?

{CAP_B4.format(n=1)}

Treballes per a un distribuïdor d'alimentació de Portugal amb 440 clients (restaurants, hotels,
botigues...). Màrqueting vol fer ofertes diferents per a cada tipus de client, però **no té cap
etiqueta**: només sap quant gasta cada client en sis famílies de productes.

- **Quants grups de clients hi ha, i com els descriuries amb paraules?** Han de ser grups que
  màrqueting pugui fer servir."""),
         md(f"""## Què necessites saber abans

- k-means, inèrcia, colze i silueta: [ML_06 §2-§8]({ML06})
- Unitats diferents i escalar: [ML_06 §10]({ML06}) i [EX_00 §2]({EX00})
- El número del grup no vol dir res: [ML_06 §9]({ML06}) i [EX_06]({EX06})"""),
         md("""## Les dades

**Wholesale customers** (M. G. M. S. Cardoso, UCI Machine Learning Repository, 2014). Llicència CC BY
4.0. Cada fila és **un client** d'un majorista portuguès, amb la despesa anual (en unitats
monetàries) en sis famílies: `Fresh`, `Milk`, `Grocery`, `Frozen`, `Detergents_Paper` i
`Delicassen`.

Hi ha dues columnes més: `Channel` (1 = hoteleria i restauració, 2 = comerç al detall) i `Region`
(1 = Lisboa, 2 = Porto, 3 = altres). **No les facis servir per agrupar**: les guardem per
comprovar *després* si els grups tenen sentit."""),
         CARREGA["401"](),
         caixa([
             ("`describe()`, `hist()`, `median()`", "resum, histogrames, mediana"),
             ("`StandardScaler()`", "resta la mitjana i divideix per la desviació de cada columna"),
             ("`np.log1p(X)`", "logaritme de 1 + x: comprimeix els valors molt grans"),
             ("`KMeans(n_clusters=k, n_init=10, random_state=0)`", "k-means"),
             ("`km.labels_`, `km.cluster_centers_`, `km.inertia_`", "el grup de cada client, els centres, la inèrcia"),
             ("`silhouette_score(X, etiquetes)`", "la silueta mitjana"),
             ("`np.bincount(etiquetes)`", "quants clients té cada grup"),
             ("`df.groupby(etiquetes).median()`", "el perfil típic de cada grup, en unitats originals"),
             ("`pd.crosstab(a, b)`", "taula de recomptes"),
             ("`PCA(n_components=2)`", "per dibuixar en dues dimensions"),
         ]),
         md("## Nivell 1 · Explorar")]
    c += tasca("1.1 · La foto",
               """Forma, tipus i nuls. Separa les sis columnes de despesa en una matriu `X`. Per a cada columna,
compara la mitjana, la mediana i el màxim. Què et diu?""",
               "`X.shape == (440, 6)` i `X` no conté `Channel` ni `Region`.",
               "Quan la mitjana és molt més gran que la mediana, què passa a la cua de la distribució?",
               "`X.describe().T` i `X.median()`.",
               "`X.max() / X.median()` per a cada columna.",
               resposta=True)
    c += tasca("1.2 · Com és cada distribució",
               """Dibuixa l'histograma de cada columna, primer tal com ve i després amb `np.log1p`. Quina de les
dues formes et sembla més adequada per mesurar distàncies entre clients?""",
               "tens 12 histogrames (6 + 6), i el de logaritme de cada columna no té valors negatius.",
               "k-means fa servir distàncies: un client que gasta deu vegades més que la resta, on el posarà?",
               "`X.hist(bins=30)` i `np.log1p(X).hist(bins=30)`.",
               "`fig, eixos = plt.subplots(2, 6, figsize=(18, 5))` si els vols tots junts.",
               resposta=True)
    c.append(xavi("Faig servir el logaritme o no? No sé si m'estic inventant les dades.",
                  "Aquests clients que gasten tantíssim, els trec?"))
    c.append(md("## Nivell 2 · Respondre"))
    c += tasca("2.1 · Escalar a mà",
               """Estandarditza `X` **a mà** amb NumPy (restar la mitjana i dividir per la desviació de cada columna)
i compara-ho amb `StandardScaler`. Si no et coincideix, busca per què.""",
               """`np.allclose(la_teva, StandardScaler().fit_transform(X))` és `True`; i cada columna de la teva
matriu té mitjana 0 i desviació 1 (amb el mateix criteri que fa servir `StandardScaler`).""",
               "Hi ha dues maneres de calcular una desviació estàndard. Quina fa servir cadascú?",
               "`X.std()` de pandas i `np.std(X)` de NumPy no donen el mateix: mira el paràmetre `ddof`.",
               "`(X - X.mean()) / X.std(ddof=0)`")
    c += tasca("2.2 · Tres versions, set valors de k",
               """Prepara tres versions de les dades: **tal com venen**, **estandarditzades** i **logaritme i després
estandarditzades**. Per a cada una, fes k-means amb k de 2 a 8 i guarda la inèrcia, la silueta i
la mida del grup més petit. Fes una taula i el gràfic del colze i de la silueta.""",
               """la taula té 21 files (3 versions × 7 valors de k); dins de cada versió, la inèrcia baixa (o no
puja) quan k creix; i les mides dels grups de cada model sumen 440.""",
               "Fes un bucle doble: per a cada versió, per a cada k.",
               "`files.append({'versio': nom, 'k': k, 'inercia': km.inertia_, 'silueta': silhouette_score(Z, km.labels_), 'minim': np.bincount(km.labels_).min()})`",
               "`pd.DataFrame(files).pivot(index='k', columns='versio', values='silueta')`",
               resposta=True)
    c += tasca("2.3 · La inèrcia, comprovada",
               """Agafa un dels models de la 2.2 i calcula la inèrcia **a mà**, a partir de les etiquetes i dels
centres. Ha de coincidir amb `km.inertia_`.""",
               "`np.isclose(la_teva, km.inertia_)` és `True`.",
               "La inèrcia és la suma, per a tots els punts, de la distància al quadrat al centre del seu grup.",
               "`km.cluster_centers_[km.labels_]` et dona el centre de cada punt.",
               "`((Z - km.cluster_centers_[km.labels_]) ** 2).sum()`")
    c += tasca("2.4 · Quina versió i quina k",
               """Tria una versió i una k. No et quedis només amb la silueta més alta: mira també **quants clients
té cada grup**. Un grup que màrqueting no pot fer servir, és un bon grup?""",
               "la teva elecció té una frase de justificació que esmenta com a mínim dos criteris.",
               "Una silueta alta vol dir grups ben separats. Separats per què?",
               "`np.bincount(km.labels_)` del model que triïs, i també dels que has descartat.",
               "Compara la silueta i les mides de la versió crua amb les de la versió amb logaritme.",
               resposta=True)
    c += tasca("2.5 · Posa'ls nom",
               """Descriu cada grup amb **les teves paraules**, a partir de la seva despesa típica en unitats
originals (no estandarditzades). Dona-li un nom a cada un. Només al final, compara els grups amb
`Channel`: s'hi assemblen?""",
               "la taula de perfils té una fila per grup i les sis columnes de despesa, en les unitats del fitxer.",
               "La mediana resisteix millor els clients extrems que la mitjana.",
               "`df.groupby(km.labels_)[columnes].median()`",
               "`pd.crosstab(km.labels_, df['Channel'])`",
               resposta=True)
    c.append(xavi("La silueta i les mides dels grups em diuen coses diferents: a qui faig cas?",
                  "Els meus grups no coincideixen amb `Channel`: he fet alguna cosa malament?"))
    c.append(md("## Nivell 3 · Més enllà"))
    c += oberta("3.1 · Dibuixa-ho",
                """Projecta les dades (la versió que hagis triat) a dues dimensions amb PCA i dibuixa els clients
pintats pel teu grup i, al costat, per `Channel`.""")
    c += oberta("3.2 · Estabilitat",
                """Torna a fer k-means amb la teva k i cinc `random_state` diferents. Els grups canvien? Com ho
mesuraries, si el número del grup no vol dir res?""",
                "Dos agrupaments iguals poden tenir els números de grup canviats.",
                "`pd.crosstab(etiquetes_a, etiquetes_b)`",
                "`adjusted_rand_score(etiquetes_a, etiquetes_b)` val 1 si els grups són idèntics encara que tinguin els números canviats.")
    c += la_teva_pregunta("3.3")
    c += lliurament("quants grups proposes i com són, quina preparació de les dades has triat i "
                    "per què, i de què no estàs segur.")
    return c


# ===========================================================================
# RE_402 · Spotify
# ===========================================================================
def re_402():
    aud = ("danceability, energy, key, loudness, mode, speechiness, acousticness, "
           "instrumentalness, liveness, valence, tempo, duration_ms")
    c = [md(f"""# RE_402 · Quants estils hi ha en un número?

{CAP_B4.format(n=2)}

Treballes a l'equip de recomanacions d'una plataforma de música. Spotify dona 12 números per a cada
cançó (ballable, energia, acústica, tempo...). El cap de producte vol fer «estils» automàtics a
partir d'aquests números, sense fer servir el gènere que diu la playlist. Abans d'invertir-hi, et
pregunta:

- **Quanta informació diferent hi ha de debò en aquestes 12 columnes?** I els grups que surten
  d'agrupar-les, **s'assemblen als gèneres** musicals?"""),
         md(f"""## Què necessites saber abans

- PCA, variància explicada i escalar: [MA_06 §3-§10]({MA06})
- k-means, colze i silueta: [ML_06 §8]({ML06}) i [EX_06]({EX06})
- Duplicats: [EX_00 §5]({EX00})"""),
         md(f"""## Les dades

**30.000 cançons de Spotify** (TidyTuesday, 2020-01-21, obtingudes amb el paquet `spotifyr` de
l'API de Spotify). El repositori és CC0; les dades són de Spotify i se'n fa un ús educatiu. Cada
fila és **una cançó dins d'una playlist** d'un gènere (`playlist_genre`: pop, rap, rock, latin, r&b,
edm) amb les característiques d'àudio que calcula Spotify.

Les 12 columnes d'àudio són: {aud}. El significat de cadascuna és al diccionari:
<https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-01-21>."""),
         CARREGA["402"](),
         caixa([
             ("`describe()`", "el rang de cada columna"),
             ("`duplicated(subset=...)`, `drop_duplicates(subset=...)`", "files repetides segons unes columnes"),
             ("`StandardScaler()`", "estandarditzar"),
             ("`PCA()`, `pca.explained_variance_ratio_`, `pca.components_`", "PCA, quina part de la variància explica cada component, i els pesos (*loadings*)"),
             ("`np.cov(Z, rowvar=False)`", "la matriu de covariància de les columnes"),
             ("`np.linalg.eigh(C)`", "valors i vectors propis d'una matriu simètrica (en ordre creixent!)"),
             ("`np.cumsum(...)`, `np.argmax(condicio)`", "suma acumulada; la primera posició on es compleix una condició"),
             ("`df.sample(n, random_state=0)`", "una mostra aleatòria reproduïble"),
             ("`KMeans(...)`, `silhouette_score(...)`", "k-means i la silueta"),
             ("`pd.crosstab(a, b, normalize='index')`", "taula de proporcions per fila"),
         ]),
         md("## Nivell 1 · Explorar")]
    c += tasca("1.1 · Les 12 columnes",
               """Mira el rang (mínim, màxim, desviació) de les 12 columnes d'àudio. Quines estan en una escala
molt diferent de les altres? Quines són, en realitat, categories escrites amb números?""",
               "la teva matriu `X` d'àudio té 12 columnes i cap nul.",
               "Llegeix el diccionari: quines van de 0 a 1, i quines no?",
               "`df[audio].describe().T`",
               "Mira també `nunique()` de cada columna.",
               resposta=True)
    c += tasca("1.2 · Una cançó, una fila?",
               """La mateixa cançó (`track_id`) pot sortir més d'una vegada? Per què passaria en aquest dataset?
Decideix com et quedes amb una fila per cançó, i explica què passa amb el gènere de les que surten
en playlists de gèneres diferents.""",
               "després de la teva decisió, `df['track_id'].is_unique` és `True`.",
               "Cada fila és una cançó **dins d'una playlist**.",
               "`df['track_id'].duplicated().sum()` i, per a les repetides, `groupby('track_id')['playlist_genre'].nunique()`.",
               "`df.drop_duplicates(subset='track_id')`",
               resposta=True)
    c.append(xavi("Una cançó que és a una playlist de pop i a una de rock: de quin gènere és?",
                  "Les columnes `key` i `mode`, les faig servir o no?"))
    c.append(md("## Nivell 2 · Respondre"))
    c += tasca("2.1 · PCA sense escalar",
               """Fes un PCA de les 12 columnes **tal com venen**. Quina part de la variància explica la primera
component? Mira'n els pesos (`components_[0]`): quina columna hi mana? Què vol dir això?""",
               "la suma de `explained_variance_ratio_` és 1 (amb totes les components).",
               "Un PCA busca la direcció on les dades varien més. En quines unitats?",
               "`PCA().fit(X)` i `pd.Series(pca.components_[0], index=audio)`.",
               "Compara-ho amb el rang de cada columna de la 1.1.",
               resposta=True)
    c += tasca("2.2 · PCA a mà",
               """Estandarditza les dades i fes el PCA **a mà**: la matriu de covariància, els valors i vectors
propis, ordenats de més gran a més petit. Compara la variància explicada amb la de `PCA` de
scikit-learn sobre les mateixes dades.""",
               """`np.allclose(la_teva_ratio, pca.explained_variance_ratio_)` és `True`; i els vectors propis
coincideixen amb `pca.components_` **llevat del signe** (`np.allclose(np.abs(...), np.abs(...))`).""",
               "`eigh` torna els valors propis en ordre creixent.",
               "`valors, vectors = np.linalg.eigh(np.cov(Z, rowvar=False))`, i després `[::-1]`.",
               "Els vectors propis són les **columnes** de `vectors`; a `components_` són les **files**.")
    c += tasca("2.3 · Quantes dimensions de debò",
               """Amb les dades estandarditzades: quantes components calen per explicar el 80 % de la variància?
Dibuixa la variància explicada acumulada. Què respondries al cap de producte sobre «quanta
informació diferent» hi ha?""",
               "la corba acumulada creix sempre i acaba a 1; el número que dones és la primera posició on arriba al 0,8 (comptant des d'1).",
               "Si les 12 columnes diguessin el mateix, quantes components caldrien?",
               "`np.cumsum(pca.explained_variance_ratio_)`",
               "`np.argmax(acumulada >= 0.8) + 1`",
               resposta=True)
    c += tasca("2.4 · Grups contra gèneres",
               """Agafa una mostra de 5.000 cançons (amb `random_state`), estandarditza i fes k-means per a
diversos valors de k. Tria'n un amb el colze i la silueta. Després, només després, creua els grups
amb `playlist_genre`. S'hi assemblen?""",
               "les mides dels grups sumen 5.000, i la taula creuada té una fila per grup i una columna per gènere.",
               "Una silueta molt baixa, què et diu dels grups?",
               "`pd.crosstab(km.labels_, mostra['playlist_genre'], normalize='index')`",
               "Si un grup fos un gènere, la seva fila tindria un valor proper a 1 en una sola columna.",
               resposta=True)
    c += tasca("2.5 · Què és cada grup",
               """Descriu dos o tres dels teus grups amb paraules (no amb noms de gènere): com sonen? Fes-ho a
partir de la mitjana de les columnes d'àudio en unitats originals.""",
               "la taula de perfils té una fila per grup i les columnes d'àudio en les unitats del fitxer.",
               "Un grup amb `acousticness` alta i `energy` baixa, com sona?",
               "`mostra.groupby(km.labels_)[audio].mean()`",
               "També pots desfer l'escalat dels centres: `scaler.inverse_transform(km.cluster_centers_)`.",
               resposta=True)
    c.append(xavi("Els grups no s'assemblen als gèneres. Està malament el model o la pregunta?",
                  "La silueta és baixa per a totes les k: n'hi ha prou per dir que no hi ha grups?"))
    c.append(md("## Nivell 3 · Més enllà"))
    c += oberta("3.1 · El mapa",
                """Dibuixa les 5.000 cançons a les dues primeres components, pintades per gènere. Quins gèneres
queden separats i quins es barregen? Mira els pesos de les dues components per dir què
representa cada eix.""")
    c += oberta("3.2 · Menys columnes",
                """Treu les columnes que no són característiques del so (les categories escrites amb números i la
durada) i torna a fer la 2.3 i la 2.4. Canvia la resposta?""")
    c += la_teva_pregunta("3.3")
    c += lliurament("quanta informació diferent hi ha en les 12 columnes, si els grups s'assemblen "
                    "als gèneres i per què creus que és així, i de què no estàs segur.")
    return c


# ===========================================================================
# RE_403 · Municipis de Catalunya
# ===========================================================================
def re_403():
    c = [md(f"""# RE_403 · Quins tipus de municipis té Catalunya?

{CAP_B4.format(n=3)}

Treballes a l'Observatori del Territori. Hi ha 947 municipis, i cada any se'n publiquen desenes
d'indicadors: població, habitatge, renda, turisme, sòl, aigua, residus... Et demanen una
**tipologia**:

- **Quins tipus de municipis hi ha a Catalunya, què els distingeix, i on cau el teu?** Ha de ser
  una cosa que una persona que no sap PCA pugui entendre."""),
         md(f"""## Què necessites saber abans

- PCA, *loadings* i escalar: [MA_06 §6-§10]({MA06})
- k-means, colze i silueta: [ML_06 §8-§10]({ML06})
- Valors que falten: [EX_00 §3]({EX00})"""),
         md("""## Les dades

**Indicadors territorials dels municipis de Catalunya** (Observatori del Territori, conjunt
`8aaj-ypcb` de Dades Obertes de la Generalitat). **Domini públic.** Cada fila és **un municipi en un
any** amb 85 columnes: identificació (codi, nom, comarca, coordenades) i indicadors amb el prefix
`_NN_` (`_01_pob_total`, `_20_socioeco_rnmp`, `_56_ma_consum_aigua_hab`...).

Són dades vives: en fem servir una **còpia congelada** (baixada el 14-oct-2026). El significat de
cada indicador és a <https://analisi.transparenciacatalunya.cat/d/8aaj-ypcb>. El necessitaràs per
triar columnes."""),
         CARREGA["403"](),
         caixa([
             ("`value_counts()`, `is_unique`, `isna()`", "quants de cada, si una columna no repeteix valors, nuls"),
             ("`df.filter(regex=...)`", "triar columnes pel nom"),
             ("`describe()`, `(serie == 0).mean()`", "rangs; proporció de zeros"),
             ("`SimpleImputer(strategy='median')`", "omplir nuls amb la mediana"),
             ("`StandardScaler()`, `np.log1p(...)`", "estandarditzar; comprimir valors molt grans"),
             ("`PCA()`, `explained_variance_ratio_`, `components_`, `mean_`", "PCA, variància explicada, pesos i la mitjana que resta"),
             ("`pca.transform(Z)`", "les coordenades de cada municipi a les components"),
             ("`KMeans(...)`, `silhouette_score(...)`", "k-means i la silueta"),
             ("`df.groupby(etiquetes)[cols].median()`", "el perfil típic de cada grup"),
         ]),
         md("## Nivell 1 · Explorar")]
    c += tasca("1.1 · Una fila per municipi?",
               """Quantes files hi hauria d'haver si fos una fila per municipi? Quantes n'hi ha? Per què? Mira
també les files que no tenen codi de municipi: què són? Queda't amb una taula amb **un sol any i
una fila per municipi**.""",
               "`df1['codi_municipi'].is_unique` és `True`, cap fila té el codi o el nom buit, i saps quantes files has tret i per què.",
               "Hi ha una columna `any`.",
               "`df['any'].value_counts()` i `df[df['codi_municipi'].isna()]`.",
               "Mira la població d'aquestes files sense codi.",
               resposta=True)
    c += tasca("1.2 · Columnes que serveixen",
               """Per a cada indicador `_NN_` numèric: quina proporció de nuls té, i quina de zeros? Un zero, té
sentit en aquella variable, o és un forat amb una altra disfressa? Mira també el rang: hi ha
alguna columna amb valors que no poden ser?""",
               "la teva taula té una fila per indicador i com a mínim tres columnes: proporció de nuls, proporció de zeros, màxim.",
               "Un municipi de 30 habitants, pot tenir un preu de lloguer de 0 €?",
               "`ind = df1.filter(regex='^_').select_dtypes('number')` i `pd.DataFrame({'nuls': ind.isna().mean(), 'zeros': (ind == 0).mean(), 'max': ind.max()})`.",
               "Ordena per nuls i per zeros i mira les primeres files.",
               resposta=True)
    c += tasca("1.3 · La teva selecció",
               """Tria entre 8 i 15 indicadors per fer la tipologia. Pensa si són **absoluts** (habitants, places,
metres cúbics) o **relatius** (per habitant, per 100 habitants, percentatges), i justifica cada
tria en una línia. Decideix què fas amb els nuls que quedin.""",
               "la matriu final té una fila per municipi, entre 8 i 15 columnes, i `np.isnan(matriu).sum() == 0`.",
               "Si poses habitants i places turístiques, què separarà el k-means primer de tot?",
               "Els noms porten pistes: `_hab`, `_100hab`, `_perc`.",
               "`SimpleImputer(strategy='median')` o treure els municipis amb nuls; compta quants en perds.",
               resposta=True)
    c.append(xavi("Aquests indicadors que només tenen els municipis grans, els faig servir?",
                  "Absolut o relatiu: no ho tinc clar per a aquesta columna."))
    c.append(md("## Nivell 2 · Respondre"))
    c += tasca("2.1 · El PCA",
               """Estandarditza la selecció i fes el PCA. Quina variància expliquen les dues primeres components?
Quantes en calen per al 80 %?""",
               "la variància explicada acumulada creix i acaba a 1.",
               "Si cada indicador digués una cosa diferent, quanta explicaria cada component?",
               "`np.cumsum(pca.explained_variance_ratio_)`",
               "`np.argmax(acumulada >= 0.8) + 1`",
               resposta=True)
    c += tasca("2.2 · Què vol dir cada eix",
               """Mira els pesos de les dues primeres components. Quines columnes hi pesen més, i amb quin signe?
Posa un nom a cada eix amb paraules teves (per exemple, «de rural a urbà»). Busca els municipis
dels extrems de cada eix per comprovar que el nom té sentit.""",
               "la taula de pesos té una fila per indicador i dues columnes (PC1 i PC2).",
               "Els pesos grans en valor absolut són els que compten. El signe diu cap a quina banda.",
               "`pd.DataFrame(pca.components_[:2].T, index=columnes, columns=['PC1', 'PC2'])`",
               "`df1.assign(pc1=coords[:, 0]).nlargest(5, 'pc1')[['municipi', 'pc1']]`",
               resposta=True)
    c += tasca("2.3 · Projectar a mà",
               """Calcula **a mà** les coordenades dels municipis a les components (amb `mean_` i `components_`) i
comprova que coincideixen amb `pca.transform`.""",
               "`np.allclose(les_teves, pca.transform(Z))` és `True`.",
               "Projectar és fer el producte escalar amb cada vector de pesos, un cop centrat.",
               "`(Z - pca.mean_) @ pca.components_.T`",
               "Si `Z` ja estava estandarditzada, `pca.mean_` és pràcticament zero, però fes-lo servir igualment.")
    c += tasca("2.4 · Els tipus de municipis",
               """Fes k-means (sobre les dades estandarditzades o sobre unes quantes components; decideix-ho i
digues per què). Tria k amb el colze, la silueta i les mides dels grups. Per a cada grup, dona el
perfil (mediana de cada indicador, en unitats originals) i tres municipis d'exemple.""",
               "les mides dels grups sumen el nombre de municipis de la teva taula, i cada grup té perfil i exemples.",
               "Un grup amb un sol municipi, és un tipus?",
               "`df1.groupby(km.labels_)[columnes].median()`",
               "`df1.groupby(km.labels_)['municipi'].apply(lambda s: list(s.sample(3, random_state=0)))`",
               resposta=True)
    c += tasca("2.5 · I el teu?",
               """On cau el teu municipi (o el de l'institut)? A quin grup és, quins municipis té més a prop al
mapa de les dues primeres components, i et sembla que el retrat és just?""",
               "el municipi que tries és a la taula (busca'l pel nom, i compte amb els articles: «Cugat del Vallès, Sant»?).",
               "Primer troba'l: `df1[df1['municipi'].str.contains('...')]`.",
               "La distància a la resta de municipis a l'espai de les components.",
               "`np.linalg.norm(coords - coords[i], axis=1)` i `argsort()`.",
               resposta=True)
    c.append(xavi("Els meus grups els separa sobretot una sola variable. Està bé?",
                  "Ho faig amb totes les components o amb les dues primeres?"))
    c.append(md("## Nivell 3 · Més enllà"))
    c += oberta("3.1 · Absolut contra relatiu",
                """Afegeix a la teva selecció dues o tres columnes absolutes (població, places turístiques, consum
total d'aigua) i torna a fer el PCA. Què passa amb la primera component? I amb els grups?""")
    c += oberta("3.2 · 2023 contra 2024",
                """Fes la tipologia amb l'altre any i compara: quants municipis canvien de grup? Són canvis reals
o soroll?""",
                "Els números dels grups no es corresponen d'un any a l'altre.",
                "Entrena amb un any i fes `km.predict` amb l'altre (amb el mateix escalat).",
                "`pd.crosstab(grups_2023, grups_2024)`")
    c += la_teva_pregunta("3.3")
    c += lliurament("quants tipus de municipis proposes i com els descriuries, què volen dir els dos "
                    "primers eixos, on cau el teu municipi, i de què no estàs segur.")
    return c


QUADERNS = {
    "RE_301_cotxes_preu.ipynb": re_301,
    "RE_302_accidents_dos_anys.ipynb": re_302,
    "RE_303_hotels_cancellacions.ipynb": re_303,
    "RE_304_certificats_energetics.ipynb": re_304,
    "RE_401_clients_majorista.ipynb": re_401,
    "RE_402_spotify_estils.ipynb": re_402,
    "RE_403_municipis_catalunya.ipynb": re_403,
}

if __name__ == "__main__":
    for nom, f in QUADERNS.items():
        print(escriu(f(), os.path.join(REPTES, nom)))
