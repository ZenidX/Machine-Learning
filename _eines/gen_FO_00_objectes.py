# -*- coding: utf-8 -*-
"""Genera el quadern FO_00: els objectes de Python dels exercicis i com interrogar-los.

    CEIABD-IA/.venv/Scripts/python.exe _eines/gen_FO_00_objectes.py

Es el quadern que obre la sessio de practica: els alumnes no sabien que `digits`
te `.data` a dins ni que un DataFrame te `.shape`, i sobretot no sabien com
esbrinar-ho sols. Aqui aprenen a preguntar-li a l'objecte (type, dir, help, TAB)
i despres tenen la taula d'atributs i metodes de cada objecte que es trobaran.

Els numeros que apareixen al text son els de l'execucio real amb llavor 42; si es
canvia el codi, cal tornar a executar el quadern i actualitzar-los.

Els errors que s'ensenyen a posta (TypeError dels parentesis, AttributeError i
NotFittedError) van dins d'un try/except: si no, `executa_nb.py` els comptaria com
a errors de debo, i a classe el quadern es trencaria a mitges.
"""
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code, escriu

cells = []
A = cells.append

# ============================================================ portada
A(md(r"""
# Objectes de Python i autocompletar: com esbrinar què pots fer amb el que tens a les mans

**Optativa d'Aprenentatge automàtic - DAM/DAW 2n**

A la sessió anterior vas llançar-te contra els exercicis i et vas quedar encallat. No
perquè no sàpigues programar: perquè tenies al davant una variable anomenada `digits` i no
tenies cap manera de saber què hi havia a dins. Vas provar `print(digits)`, et va sortir
una paret de números, i d'allà no es passa.

Aquest quadern resol exactament això. La idea central és aquesta, i val la pena que te la
quedis:

> **No cal recordar els noms. Cal saber preguntar-los-hi.**

Ningú es recorda de memòria que un DataFrame té `.dtypes`, ni que un model entrenat té
`.coef_`. El que sí que sap tothom que treballa amb això és **com demanar-li a l'objecte
que t'ensenyi el que té**. Són quatre eines, i les tindràs totes en deu minuts.

La segona part del quadern és el catàleg: els cinc objectes que et trobaràs a tots els
exercicis del curs, amb els atributs i els mètodes que faràs servir de veritat. La tercera
és una exploració de dades sencera, per veure-ho funcionant.

Tot el codi d'aquest quadern es pot executar. Executa'l, canvia'l, torna a executar-lo.
"""))

A(code(r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

print("numpy: ", np.__version__)
print("pandas:", pd.__version__)
"""))

# ============================================================ PART 1
A(md(r"""
---

# Part 1 - Com interrogar un objecte qualsevol

A Python, gairebé tot és un **objecte**. Un objecte és una cosa que porta dades a dins i
sap fer coses. Les dades que porta són els seus **atributs**; les coses que sap fer són els
seus **mètodes**. Tots dos s'accedeixen amb un punt: `objecte.alguna_cosa`.

El problema pràctic és saber quines "algunes coses" hi ha. Per això hi ha quatre eines.
"""))

# ---------------------------------------------------------- type
A(md(r"""
## 1.1 `type(objecte)` - de quina classe és

La primera pregunta sempre és la mateixa: **què és això?** Perquè el que pots fer-hi depèn
de la resposta. Un DataFrame i un array de NumPy s'assemblen quan els imprimeixes, però no
tenen els mateixos mètodes.
"""))

A(code(r"""
numero = 3.14
text = "iris"
llista = [1, 2, 3]
diccionari = {"a": 1}

print(type(numero))
print(type(text))
print(type(llista))
print(type(diccionari))
"""))

A(md(r"""
`<class 'float'>` es llegeix: això és de la classe `float`. Si només vols el nom net, sense
l'embolcall de `<class ...>`, demana-li `__name__` a la classe:
"""))

A(code(r"""
print(type(numero).__name__)
print(type(llista).__name__)
"""))

# ---------------------------------------------------------- dir
A(md(r"""
## 1.2 `dir(objecte)` - tot el que té a dins

`dir()` et torna una llista amb **tots** els noms que hi ha dins de l'objecte: atributs i
mètodes, barrejats i ordenats alfabèticament. És la manera més directa de veure què tens.

El problema és que la llista és llarga i ve plena de coses que no són per a tu.
"""))

A(code(r"""
tots = dir(llista)
print("Una llista de Python té", len(tots), "noms a dins.")
print()
print(tots)
"""))

A(md(r"""
### El guió baix davant

Has vist que la majoria comencen per `__`: `__add__`, `__len__`, `__class__`...

**Un nom que comença per guió baix és cosa interna de Python, no és per a tu.** Són els
engranatges: `__add__` és el que s'executa de debò quan escrius `a + b`, i `__len__` és el
que s'executa quan escrius `len(a)`. Existeixen, funcionen, i no els cridaràs mai
directament. Escriure `llista.__len__()` funciona, però és escriure `len(llista)` amb
lletjor i sense cap avantatge.

Així que la manera útil de fer servir `dir()` és **filtrant-los**:
"""))

A(code(r"""
publics = [n for n in dir(llista) if not n.startswith("_")]
print(len(publics), "noms útils:")
print(publics)
"""))

A(md(r"""
De 48 noms a 11. Aquests sí que són els que has de fer servir, i `append`, `sort` i `count`
ja els coneixes.

Aquesta línia la faràs servir tot el curs, així que val la pena llegir-la a poc a poc:
recorre tots els noms de `dir(llista)` i es queda **només** amb els que **no** comencen per
guió baix.

Provem-la amb un objecte que encara no has explorat:
"""))

A(code(r"""
print([n for n in dir(text) if not n.startswith("_")])
"""))

A(md(r"""
Aquests són tots els mètodes d'un text. No te'ls has de mirar ara: el que importa és que
**no els has hagut de buscar enlloc**. Els has preguntat.
"""))

# ---------------------------------------------------------- help i ?
A(md(r"""
## 1.3 `help()` i `objecte.metode?` - què fa i què li has de passar

`dir()` et diu **que una cosa existeix**. No et diu què fa ni quins arguments vol. Per això
hi ha `help()`, que t'ensenya la documentació.
"""))

A(code(r"""
help(llista.count)
"""))

A(md(r"""
Amb això ja el pots fer servir: t'ha dit com es crida (`count(value, /)`) i què fa (torna
quantes vegades apareix el valor que li passis).

### La versió curta: el signe d'interrogació

A Colab i a Jupyter tens una manera més còmoda, que **només funciona al quadern**: posar un
`?` darrere del nom.

```python
llista.count?
```

Escriu-ho tu ara mateix en una cel·la nova i executa-la: la documentació s'obre en un
**panell a baix de la pantalla**, sense embrutar la sortida de la cel·la. Amb dos
interrogants (`llista.count??`) veus fins i tot el codi font, quan està escrit en Python.

Aquesta és la que faràs servir en la pràctica. Amb pandas i scikit-learn els textos d'ajuda
són llarguíssims (el de `DataFrame.groupby` fa desenes de línies) i al panell es llegeixen
molt millor que enmig del quadern.

> Compte: `llista.count?` **només** funciona dins d'un quadern. En un fitxer `.py` és un
> error de sintaxi. Allà has de fer servir `help(llista.count)`.
"""))

# ---------------------------------------------------------- TAB
A(md(r"""
## 1.4 La tecla TAB - l'autocompletat

Aquesta és la més important de les quatre, i no es pot ensenyar amb una cel·la executada:
l'has de fer tu.

**Escriu el nom d'un objecte, un punt, i prem TAB.** Surt una llista amb tot el que pots
posar després del punt, i mentre escrius lletres es va escurçant.

Prova-ho ara. Crea una cel·la nova, escriu això **sense executar-ho**:

```python
llista.
```

i amb el cursor just darrere del punt, prem **TAB**. Apareixerà `append`, `clear`, `copy`,
`count`... Ara escriu una `s` (`llista.s`) i torna a prémer TAB: només queda `sort`.

Això és **la manera normal de treballar**. No és una drecera per a principiants ni una
ajuda per quan no te'n recordes: és com ho fa tothom, tot el dia. Ningú es recorda de
memòria els noms dels mètodes de pandas, i ningú els busca a Google un per un. Es prem TAB
i es tria de la llista.

De les quatre eines, l'ordre pràctic acaba sent aquest:

| Quan | Eina |
|---|---|
| Estic escrivint i vull veure què hi ha | **TAB** |
| Vull la llista completa, per llegir-la amb calma | `dir(objecte)` filtrat |
| He trobat un mètode i no sé què li he de passar | `objecte.metode?` |
| No sé ni de quin tipus és el que tinc | `type(objecte)` |
"""))

# ---------------------------------------------------------- atribut vs metode
A(md(r"""
## 1.5 Atribut o mètode: la diferència que et farà perdre una hora

Després del punt hi pot haver dues coses molt diferents, i confondre-les és l'error que
veuràs més vegades avui.

- Un **atribut** és una **dada** que l'objecte porta guardada. Es llegeix i prou. **No
  porta parèntesis.**
- Un **mètode** és una **acció** que l'objecte sap fer. L'has de **cridar**, i cridar-lo
  vol dir posar-li **parèntesis**.

La regla curta: **si és una dada, no hi ha parèntesis; si és una feina, sí.**

Fem-nos una taula petita per veure-ho. No et preocupis encara per què és un DataFrame: de
moment, una taula.
"""))

A(code(r"""
alumnes = pd.DataFrame({
    "nom": ["Aina", "Bruno", "Clara", "Dídac"],
    "nota": [7.5, 4.0, 9.25, 6.0],
    "assistencia": [0.92, 0.55, 1.00, 0.80],
})
alumnes
"""))

A(code(r"""
# .shape és un ATRIBUT: una dada guardada, sense parèntesis
print("shape:  ", alumnes.shape)
print("columns:", list(alumnes.columns))

# .head() és un MÈTODE: una feina, amb parèntesis
print()
print(alumnes.head(2))
"""))

A(md(r"""
### Què passa si els confons

Val més que aquests dos errors els vegis aquí, tranquil, que no d'aquí a mitja hora enmig
d'un exercici. Els dos els veuràs avui.

**Cas 1: posar parèntesis a un atribut.** `alumnes.shape` ja és una tupla, `(4, 3)`.
Escriure `alumnes.shape()` vol dir "crida la tupla `(4, 3)`", i una tupla no es pot cridar.
"""))

A(code(r"""
try:
    alumnes.shape()
except TypeError as e:
    print(type(e).__name__, "->", e)
"""))

A(md(r"""
`TypeError: 'tuple' object is not callable`. **"Object is not callable" vol dir sempre el
mateix: has posat parèntesis a una cosa que no és una funció.** Treu-los.

**Cas 2: oblidar els parèntesis d'un mètode.** Això no peta, i per això és més traïdor: et
surt una cosa rara i no un error.
"""))

A(code(r"""
print(alumnes.head)
"""))

A(md(r"""
`<bound method NDFrame.head of ...>`. Això no són les dades: és **el mètode en si**, sense
executar. Python t'ensenya l'etiqueta de la feina en lloc de fer-la, perquè no li has
demanat que la faci.

**Quan veus `bound method` a la sortida, t'has deixat els parèntesis.** És literalment tot
el diagnòstic que necessites.

I com saber de quin dels dos es tracta abans d'equivocar-te? Pregunta-ho:
"""))

A(code(r"""
print("callable(alumnes.shape) ->", callable(alumnes.shape))   # False: és un atribut
print("callable(alumnes.head)  ->", callable(alumnes.head))    # True: és un mètode
"""))

# ---------------------------------------------------------- que_te
A(md(r"""
## 1.6 `que_te()`: la funció que faràs servir tot el curs

Ajuntem-ho tot en una sola funció. Li passes un objecte qualsevol i t'imprimeix de quin
tipus és, quins atributs públics té i quins mètodes públics té, **separats**, que és
justament el que `dir()` no fa.

Copia-la als teus quaderns. Com distingeix els atributs dels mètodes? Amb `callable()`,
exactament com acabes de veure.
"""))

A(code(r'''
def que_te(objecte, filtre=""):
    """Imprimeix el tipus, els atributs públics i els mètodes públics d'un objecte.

    Amb `filtre`, només mostra els noms que contenen aquell text:
    que_te(df, "na") per trobar isna, dropna, fillna...
    """
    atributs = []
    metodes = []
    for nom in dir(objecte):
        if nom.startswith("_") or filtre not in nom:
            continue
        try:
            valor = getattr(objecte, nom)
        except Exception:
            continue          # n'hi ha que peten si encara no existeixen: les saltem
        if callable(valor):
            metodes.append(nom)
        else:
            atributs.append(nom)

    print("TIPUS:", type(objecte).__name__)
    print()
    print(f"ATRIBUTS ({len(atributs)}) - sense parèntesis:")
    print("  " + (", ".join(atributs) if atributs else "(cap)"))
    print()
    print(f"MÈTODES ({len(metodes)}) - amb parèntesis:")
    print("  " + (", ".join(metodes) if metodes else "(cap)"))


que_te(alumnes)
'''))

A(md(r"""
18 atributs i 193 mètodes: un DataFrame té molta cosa. Dues observacions sobre aquesta
sortida, perquè si no et despistaran:

- Entre els atributs hi surten `nom`, `nota` i `assistencia`, que són **els noms de les
  columnes**. pandas les exposa també com a atributs, o sigui que `alumnes.nota` funciona
  igual que `alumnes["nota"]`. Amb els claudàtors sempre funciona; amb el punt, no (prova-ho
  amb una columna que es digui `od280/od315_of_diluted_wines`).
- `loc` i `iloc` han anat a la llista de mètodes, perquè `callable()` diu que sí. Són
  l'excepció de tot plegat: es fan servir amb **claudàtors**, `alumnes.loc[0, "nota"]`. Hi
  tornem a la secció 2.3.

Com que la llista és tan llarga, `que_te()` accepta un filtre: quan busques alguna cosa
concreta i no recordes com es diu, filtra per un tros del nom. Per exemple, saps que hi ha
alguna cosa per als valors que falten i que en anglès es diu "NA":
"""))

A(code(r"""
que_te(alumnes, "na")
"""))

A(md(r"""
`isna`, `dropna`, `fillna`, `notna`: els que buscaves. També hi surten `rename` i
`rename_axis`, perquè el filtre és una cerca de text ximple i "rename" conté "na". No hi
passa res: sis noms es llegeixen en un segon, 193 no.

El que importa és que no els has buscat enlloc. Els has trobat preguntant, i aquesta és tota
la tècnica.
"""))

# ============================================================ PART 2
A(md(r"""
---

# Part 2 - Els cinc objectes que et trobaràs

Amb les eines de la Part 1 pots explorar qualsevol cosa. Però anar a cegues cada vegada és
lent, i aquests cinc objectes sortiran a tots els exercicis del curs. Aquí tens, per a cada
un, la taula del que faràs servir **de veritat** (no la llista completa) i una cel·la que ho
toca tot.

Aquesta part és **material de consulta**: torna-hi quan estiguis encallat.
"""))

# ---------------------------------------------------------- Bunch
A(md(r"""
## 2.1 `Bunch` - el que et torna `load_iris()`

Aquest és el que et va desconcertar. Quan escrius `digits = load_digits()`, `digits` **no
són les dades**: és una capsa que porta les dades a dins, juntament amb les etiquetes, els
noms de les columnes i la descripció del dataset. La classe es diu `Bunch`.

| | Nom | Què és |
|---|---|---|
| atribut | `.data` | les dades: array 2D, files = mostres, columnes = característiques |
| atribut | `.target` | la resposta correcta de cada fila: array 1D de números |
| atribut | `.feature_names` | els noms de les columnes de `.data` |
| atribut | `.target_names` | a què correspon cada número de `.target` |
| atribut | `.DESCR` | la descripció del dataset, en text |
| atribut | `.images` | **només a `load_digits`**: les mateixes dades en forma d'imatge 8x8 |
| mètode | `.keys()` | què porta a dins (perquè un `Bunch` també és un diccionari) |
"""))

A(code(r"""
from sklearn.datasets import load_iris, load_wine, load_digits

iris = load_iris()

print("type:", type(iris).__name__)
print()
print("dir() filtrat:", [n for n in dir(iris) if not n.startswith("_")])
"""))

A(md(r"""
Aquí passa una cosa que val la pena dir, perquè és una excepció: **en un `Bunch`, `dir()`
et torna just les claus que porta**, no la llista de quaranta coses que esperaries.
scikit-learn ho ha programat així expressament, per fer-te fàcil justament el que estàs
fent.

I com que un `Bunch` **també és un diccionari**, té una segona manera de mirar-hi dins:
"""))

A(code(r"""
print(iris.keys())
print()
print("iris.data i iris['data'] són el mateix objecte:", iris.data is iris["data"])
"""))

A(code(r"""
print("data.shape:   ", iris.data.shape)
print("target.shape: ", iris.target.shape)
print("feature_names:", iris.feature_names)
print("target_names: ", iris.target_names)
print()
print("primera fila de data:", iris.data[0])
print("el seu target:       ", iris.target[0], "->", iris.target_names[iris.target[0]])
"""))

A(md(r"""
Llegit: `data` té 150 files i 4 columnes, `target` té 150 números (un per flor), i el
`target` de la primera flor és `0`, que segons `target_names` vol dir `setosa`.

`.DESCR` és un text llarg amb la fitxa del dataset: d'on surt, què vol dir cada columna,
quantes mostres hi ha. No l'imprimeixis sencer, que fa mig metre; talla'l.
"""))

A(code(r"""
print(type(iris.DESCR).__name__, "de", len(iris.DESCR), "caràcters")
print()
print(iris.DESCR[:360])
"""))

A(md(r"""
### El cas de `load_digits`: `.images`

`load_digits` porta dígits escrits a mà, en imatges de 8x8 píxels. Té les mateixes dades
guardades de dues maneres, i aquest és l'atribut que ningú endevina:

- `.data` és `(1797, 64)`: cada imatge **aplanada** en una fila de 64 números. És la forma
  que volen els models.
- `.images` és `(1797, 8, 8)`: la mateixa cosa **en forma de quadrat**. És la forma que vols
  per dibuixar-la.
"""))

A(code(r"""
digits = load_digits()

print("keys:  ", list(digits.keys()))
print("data:  ", digits.data.shape)
print("images:", digits.images.shape)
print("target:", digits.target.shape, " classes:", digits.target_names)
print()
print("La primera imatge, en forma de quadrat 8x8:")
print(digits.images[0].astype(int))
print()
print("És un:", digits.target[0])
"""))

A(md(r"""
Si mires el quadrat de números de reüll, ja s'hi endevina un zero: els valors alts (16, 15,
13) dibuixen l'anell i al mig hi ha el forat de zeros. Dibuixem-lo de debò:
"""))

A(code(r"""
fig, eixos = plt.subplots(1, 5, figsize=(9, 2))
for i, eix in enumerate(eixos):
    eix.imshow(digits.images[i], cmap="gray_r")
    eix.set_title(f"target = {digits.target[i]}")
    eix.axis("off")
plt.tight_layout()
plt.show()
"""))

A(md(r"""
### `as_frame=True`: el mateix dataset com a DataFrame

Els carregadors accepten `as_frame=True`. Llavors el `Bunch` porta dos atributs més que et
faran la vida molt més fàcil: `.frame`, amb tot el dataset en un DataFrame (dades **i**
target), i `.data` convertit també en DataFrame, amb els noms de columna ja posats.
"""))

A(code(r"""
iris_df = load_iris(as_frame=True)

print("keys:", list(iris_df.keys()))
print()
print("type de .data: ", type(iris_df.data).__name__)
print("type de .frame:", type(iris_df.frame).__name__)
print("shape de .frame:", iris_df.frame.shape, "(les 4 columnes + la del target)")
print()
print(iris_df.frame.head(3))
"""))

# ---------------------------------------------------------- ndarray
A(md(r"""
## 2.2 `ndarray` - l'array de NumPy

És el que hi ha dins de `.data`. Files = mostres, columnes = característiques.

| | Nom | Què és |
|---|---|---|
| atribut | `.shape` | la forma: `(files, columnes)` |
| atribut | `.dtype` | el tipus de dada que guarda: `float64`, `int64`... |
| atribut | `.ndim` | quantes dimensions té: 1 = fila, 2 = taula |
| atribut | `.size` | quants números hi ha en total |
| atribut | `.T` | el mateix array transposat (files per columnes) |
| mètode | `.mean()` `.std()` | mitjana, desviació típica |
| mètode | `.min()` `.max()` `.sum()` | mínim, màxim, suma |
| mètode | `.argmin()` `.argmax()` | **la posició** del mínim i del màxim, no el valor |
| mètode | `.reshape()` | canvia la forma sense canviar els números |
| mètode | `.copy()` | una còpia independent |
| mètode | `.astype()` | el mateix array amb un altre tipus de dada |
| mètode | `.round()` | arrodonit a tants decimals |
"""))

A(code(r"""
X = iris.data

print("TIPUS:", type(X).__name__)
print()
print("shape:", X.shape)
print("dtype:", X.dtype)
print("ndim: ", X.ndim)
print("size: ", X.size, "=", X.shape[0], "x", X.shape[1])
print("T:    ", X.T.shape, "(files i columnes intercanviades)")
"""))

A(md(r"""
### `axis`: el que costa més de tots

Aquí és on tothom ensopega, així que aquesta cel·la la val la pena mirar-se dos cops.

Els mètodes de resum (`.mean()`, `.sum()`, `.max()`...) es comporten de tres maneres segons
què li posis a `axis`:

- **`X.mean()`**, sense res: un **sol número**, la mitjana dels 600 valors alhora. Gairebé
  mai és el que vols.
- **`X.mean(axis=0)`**, "aixafa les files": **un número per columna**. La mitjana de cada
  característica. **És el que voldràs el 90% de les vegades.**
- **`X.mean(axis=1)`**, "aixafa les columnes": **un número per fila**. La mitjana de cada
  flor, que aquí no vol dir gran cosa (barreja centímetres de sèpal amb centímetres de
  pètal), però en altres datasets sí.

El truc per recordar-ho: `axis` diu **quin eix desapareix**. `axis=0` és l'eix de les files,
i el resultat ja no té files: en queda un valor per columna.
"""))

A(code(r"""
print("X.shape            ->", X.shape)
print()
print("X.mean()           ->", X.mean().round(4), " (un sol número)")
print("X.mean(axis=0)     ->", X.mean(axis=0).round(3), " shape", X.mean(axis=0).shape)
print("X.mean(axis=1)[:5] ->", X.mean(axis=1)[:5].round(3), " shape", X.mean(axis=1).shape)
"""))

A(code(r"""
# La resta de mètodes de resum funcionen igual
print("mínim de cada columna:  ", X.min(axis=0))
print("màxim de cada columna:  ", X.max(axis=0))
print("desviació per columna:  ", X.std(axis=0).round(3))
print("suma de cada columna:   ", X.sum(axis=0).round(1))
print()
# argmax NO dona el valor: dona la POSICIÓ
columna_petal = X[:, 2]
print("El pètal més llarg fa     ", columna_petal.max())
print("i és el de la flor número ", columna_petal.argmax())
print("comprovació:              ", columna_petal[columna_petal.argmax()])
"""))

A(code(r"""
# reshape, astype i round
petit = np.arange(6)
print("petit:         ", petit, petit.shape)
print("reshape(2, 3):")
print(petit.reshape(2, 3))
print()
print("dtype original:", X.dtype)
print("astype(int):   ", X[:2].astype(int).tolist(), "(talla els decimals, no arrodoneix)")
print("round(0):      ", X[:2].round(0).tolist())
"""))

# ---------------------------------------------------------- DataFrame
A(md(r"""
## 2.3 `DataFrame` - la taula de pandas

Un array de NumPy amb noms a les columnes i moltíssims mètodes d'anàlisi. És el que faràs
servir per **mirar** les dades; l'array és el que faràs servir per **entrenar** els models.

| | Nom | Què és |
|---|---|---|
| atribut | `.shape` | `(files, columnes)` |
| atribut | `.columns` | els noms de les columnes |
| atribut | `.index` | les etiquetes de les files |
| atribut | `.dtypes` | el tipus de cada columna, una per una |
| atribut | `.values` | les dades com a array de NumPy, sense els noms |
| atribut | `.loc` | selecció **per etiqueta**: `df.loc[3, "nota"]` |
| atribut | `.iloc` | selecció **per posició**: `df.iloc[0, 1]` |
| mètode | `.head()` `.tail()` | les primeres / les últimes files |
| mètode | `.info()` | resum: columnes, tipus, quants valors no nuls, memòria |
| mètode | `.describe()` | estadístiques de cada columna numèrica |
| mètode | `.isna()` | on falten valors (True/False a cada casella) |
| mètode | `.dropna()` `.fillna()` | treure les files amb buits / omplir-los |
| mètode | `.groupby()` | agrupar per una columna per calcular per grup |
| mètode | `.sort_values()` | ordenar per una columna |
| mètode | `.value_counts()` | comptar quantes vegades surt cada valor |
| mètode | `.drop()` | treure columnes o files |
| mètode | `.copy()` | una còpia independent |
| mètode | `.duplicated()` `.drop_duplicates()` | trobar / treure files repetides |

Nota sobre `.loc` i `.iloc`: són **atributs**, sense parèntesis, però es fan servir amb
**claudàtors**: `df.loc[...]`. És l'única parella que es comporta així.
"""))

A(code(r"""
vins = load_wine(as_frame=True).frame

print("TIPUS:", type(vins).__name__)
print()
print("shape:", vins.shape)
print("index:", vins.index)
print()
print("columns:")
for nom in vins.columns:
    print("  -", nom)
"""))

A(code(r"""
print("dtypes:")
print(vins.dtypes)
print()
print("values és un", type(vins.values).__name__, "de shape", vins.values.shape)
"""))

A(md(r"""
`.dtypes` diu que 13 columnes són `float64` i la del `target` és `int64`. Té sentit: les
mesures són decimals i la classe és un número enter.

`.info()` ho ajunta tot en un sol cop d'ull i, sobretot, et diu **quants valors no nuls** hi
ha a cada columna. Si en alguna surt un número més petit que el total de files, hi falten
dades.
"""))

A(code(r"""
vins.info()
"""))

A(code(r"""
# .head() i .tail(): sempre el primer que es mira
print(vins.head(3).iloc[:, :5])
print()
print(vins.tail(3).iloc[:, :5])
"""))

A(md(r"""
He fet servir `.iloc[:, :5]` per no imprimir les 14 columnes de cop: "totes les files, les 5
primeres columnes". Compara-ho amb `X[:, :5]` de NumPy: la notació és la mateixa.

`.loc` i `.iloc` es diferencien en què fan servir per identificar les files i les columnes:
"""))

A(code(r"""
print("iloc[0, 0]  (fila 0, columna 0, per POSICIÓ):", vins.iloc[0, 0])
print("loc[0, 'alcohol']  (per ETIQUETA):           ", vins.loc[0, "alcohol"])
print()
print("iloc[:3, :2] (les 3 primeres files, 2 columnes):")
print(vins.iloc[:3, :2])
print()
print("loc[:2, ['alcohol', 'target']] (per nom de columna):")
print(vins.loc[:2, ["alcohol", "target"]])
"""))

A(md(r"""
`.describe()` és la millor primera mirada a un dataset numèric: per a cada columna, quants
valors hi ha, la mitjana, la desviació típica, el mínim, els tres quartils i el màxim.
"""))

A(code(r"""
print(vins[["alcohol", "malic_acid", "proline"]].describe().round(2))
"""))

A(md(r"""
Fixa't en l'escala: `alcohol` va de 11.03 a 14.83 i `proline` va de 278 a 1680. Són números
de mides completament diferents, i això tindrà conseqüències quan entrenis models basats en
distàncies. Però això és una altra sessió.

### Valors que falten i files repetides

El dataset dels vins està net, i és útil comprovar-ho en lloc de suposar-ho.
"""))

A(code(r"""
print("isna() torna un", type(vins.isna()).__name__, "de la mateixa shape:", vins.isna().shape)
print("valors que falten en total:", vins.isna().sum().sum())
print("files repetides:           ", vins.duplicated().sum())
print()
print("valors que falten per columna (les 4 primeres):")
print(vins.isna().sum().head(4))
"""))

A(md(r"""
Cap valor que falti i cap fila repetida: 0 i 0. Quan no és així, `.dropna()` treu les files
amb buits i `.fillna(valor)` els omple. Cap dels dos modifica el DataFrame original: **et
tornen un de nou**.
"""))

A(code(r"""
# Fem-nos una taula amb forats per veure-ho, que els vins no en tenen
amb_forats = pd.DataFrame({
    "a": [1.0, 2.0, np.nan, 4.0],
    "b": [10.0, np.nan, 30.0, 40.0],
})
print("original:")
print(amb_forats)
print()
print("dropna() ->", amb_forats.dropna().shape, "files que sobreviuen")
print(amb_forats.dropna())
print()
print("fillna(0):")
print(amb_forats.fillna(0))
print()
print("l'original NO ha canviat:", amb_forats.isna().sum().sum(), "forats encara")
"""))

# ---------------------------------------------------------- Series
A(md(r"""
## 2.4 `Series` - una columna

Això es passa per alt i després confon molt: **una columna d'un DataFrame no és un
DataFrame**. És una `Series`, que és una altra classe, amb els seus propis mètodes.

Una `Series` és una columna de valors amb un índex. Té els atributs que ja coneixes
(`.shape`, `.dtype`, `.values`, `.index`) i, a més, els seus:

| | Nom | Què és |
|---|---|---|
| mètode | `.value_counts()` | quantes vegades surt cada valor, de més a menys |
| mètode | `.unique()` | quins valors diferents hi ha |
| mètode | `.nunique()` | quants valors diferents hi ha |
| mètode | `.map()` | aplica una funció o un diccionari a cada valor |
| mètode | `.astype()` | canvia el tipus de dada |
| mètode | `.mean()` `.std()` `.min()` `.max()` `.sum()` | com a NumPy |
| mètode | `.idxmax()` `.idxmin()` | l'**índex** de la fila del màxim i del mínim |
"""))

A(code(r"""
columna = vins["alcohol"]

print("type de vins['alcohol']:", type(columna).__name__)
print("type de vins:           ", type(vins).__name__)
print()
print("shape:", columna.shape, "(una sola dimensió, no (178, 1))")
print("dtype:", columna.dtype)
print("name: ", columna.name)
print()
print(columna.head(3))
"""))

A(md(r"""
Un parany petit: `vins["alcohol"]`, amb un nom, és una `Series`; però `vins[["alcohol"]]`,
amb **doble claudàtor** (una llista d'una sola columna), és un DataFrame d'una columna. Es
veuen gairebé igual a la pantalla i no tenen els mateixos mètodes.
"""))

A(code(r"""
print("vins['alcohol']   ->", type(vins["alcohol"]).__name__, vins["alcohol"].shape)
print("vins[['alcohol']] ->", type(vins[["alcohol"]]).__name__, vins[["alcohol"]].shape)
"""))

A(code(r"""
# value_counts, unique, nunique: sempre sobre la columna del target, per començar
classes = vins["target"]

print("value_counts():")
print(classes.value_counts())
print()
print("value_counts().sort_index():")
print(classes.value_counts().sort_index())
print()
print("unique(): ", classes.unique())
print("nunique():", classes.nunique())
"""))

A(md(r"""
El dataset té **3 classes**, amb **59, 71 i 48** vins respectivament. Fixa't que
`.value_counts()` ordena de més freqüent a menys (surt primer la classe 1, amb 71), no pel
valor. Per veure-ho en ordre de classe, `.sort_index()`.

`.map()` serveix per traduir valors. Aquí, els números del target als noms de les varietats:
"""))

A(code(r"""
noms = load_wine().target_names
print("target_names:", noms)

etiquetes = classes.map({0: noms[0], 1: noms[1], 2: noms[2]})
print()
print(etiquetes.head(3))
print()
print(etiquetes.value_counts())
"""))

A(code(r"""
# idxmax: l'índex de la fila amb el valor més alt
print("l'alcohol més alt és", columna.max())
print("i és el de la fila  ", columna.idxmax())
print()
print("la fila sencera, fins a magnesium:")
print(vins.loc[columna.idxmax(), :"magnesium"])
"""))

A(md(r"""
El vi més alcohòlic fa **14.83 graus** i és el de la fila **8**.

Compte amb la diferència entre `.idxmax()` de pandas i `.argmax()` de NumPy: `.idxmax()` et
torna l'**etiqueta de l'índex** (que aquí coincideix amb la posició, perquè l'índex va de 0
a 177, però no sempre passa) i `.argmax()` et torna la **posició**.
"""))

# ---------------------------------------------------------- model
A(md(r"""
## 2.5 Un model de scikit-learn, abans i després d'entrenar

L'últim objecte, i el que té la propietat més curiosa: **canvia** quan l'entrenes. Té
atributs que **no existeixen** fins que li has donat dades.

| | Nom | Què és |
|---|---|---|
| mètode | `.fit(X, y)` | **entrena**: aprèn dels exemples |
| mètode | `.predict(X)` | prediu la classe de mostres noves |
| mètode | `.score(X, y)` | quina proporció encerta |
| mètode | `.get_params()` | amb quins ajustos l'has creat |
| atribut | `.coef_` | el que ha après: el pes de cada característica |
| atribut | `.classes_` | quines classes ha vist |
| atribut | `.n_features_in_` | quantes columnes esperava |
| atribut | `.feature_importances_` | (als models d'arbre) quant compta cada columna |

### La convenció del guió baix al final

Ja saps què vol dir un guió baix **davant**: cosa interna, no és per a tu. Doncs n'hi ha una
altra convenció, i és la que et desencallarà avui:

> **Un guió baix al FINAL del nom vol dir "això ho he après de les dades".**

`coef_`, `classes_`, `n_features_in_`, `feature_importances_`: tots acaben en `_` i tots
**només existeixen després de cridar `.fit()`**. No és decoració. És l'avís que no els pots
demanar abans.

Comprovem-ho: creem un model, mirem què té, l'entrenem i tornem a mirar.
"""))

A(code(r"""
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=5000, random_state=42)

print("TIPUS:", type(model).__name__)
print()
print("get_params(), els 6 primers:")
for clau, valor in list(model.get_params().items())[:6]:
    print(f"  {clau} = {valor}")
"""))

A(code(r"""
# El que té ABANS d'entrenar: cap nom que acabi en guió baix
abans = [n for n in dir(model) if not n.startswith("_")]
apresos_abans = [n for n in abans if n.endswith("_")]

print("noms públics abans de fit():", len(abans))
print("dels quals acabats en '_': ", apresos_abans)
"""))

A(md(r"""
La llista és **buida**. El model no ha après res perquè encara no ha vist cap dada.

I això és exactament el que passa si els demanes: **l'error que veuràs avui**.
"""))

A(code(r"""
try:
    print(model.coef_)
except AttributeError as e:
    print(type(e).__name__, "->", e)
"""))

A(code(r"""
from sklearn.exceptions import NotFittedError

try:
    model.predict(iris.data[:3])
except NotFittedError as e:
    print(type(e).__name__, "->")
    print(str(e)[:190])
"""))

A(md(r"""
Els dos errors diuen el mateix amb paraules diferents: **`AttributeError` si demanes un
atribut après, `NotFittedError` si li demanes que treballi**. Tots dos volen dir "encara no
has cridat `.fit()`". Quan te'n surti un, no busquis el problema al nom del mètode: busca la
línia del `fit` que t'has deixat.

Ara l'entrenem.
"""))

A(code(r"""
model.fit(iris.data, iris.target)

despres = [n for n in dir(model) if not n.startswith("_")]
apresos_despres = [n for n in despres if n.endswith("_")]

print("noms públics abans de fit():  ", len(abans))
print("noms públics després de fit():", len(despres))
print()
print("acabats en '_' que han APAREGUT:")
for n in apresos_despres:
    print("  ", n)
"""))

A(md(r"""
De 27 noms públics a 32: han aparegut **cinc atributs nous**, i tots acaben en guió baix.
Abans no hi eren. El mateix objecte, la mateixa variable, i ara té dades a dins que no
tenia. Això és el que fa `.fit()`: no torna res útil, **modifica el model**.

Mirem què ha après:
"""))

A(code(r"""
print("classes_:      ", model.classes_)
print("n_features_in_:", model.n_features_in_)
print()
print("coef_.shape:", model.coef_.shape, "-> una fila per classe, una columna per característica")
print(model.coef_.round(2))
"""))

A(code(r"""
print("score sobre les mateixes dades:", round(model.score(iris.data, iris.target), 4))
print()
prediccions = model.predict(iris.data[:8])
print("predict de les 8 primeres flors:", prediccions)
print("el que eren de veritat:         ", iris.target[:8])
"""))

A(md(r"""
`0.9733`: encerta 146 de les 150 flors. (Avaluar sobre les mateixes dades amb què has
entrenat està malament fet, i ho veuràs a la sessió de validació; aquí només volíem que
`.score()` tornés un número.)

### El mateix amb un arbre: `feature_importances_`

Cada família de models aprèn coses diferents, i per tant té atributs acabats en `_`
diferents. Un model lineal aprèn **coeficients**; un arbre aprèn **importàncies**. Si
n'agafes un que no has fet servir mai, `que_te()` t'ho diu.
"""))

A(code(r"""
from sklearn.tree import DecisionTreeClassifier

arbre = DecisionTreeClassifier(random_state=42).fit(iris.data, iris.target)

print("atributs apresos de l'arbre:")
print([n for n in dir(arbre) if not n.startswith("_") and n.endswith("_")])
print()
for nom, importancia in zip(iris.feature_names, arbre.feature_importances_):
    print(f"  {nom:22} {importancia:.3f}")
print()
print("l'arbre NO té coef_:", "coef_" in dir(arbre))
"""))

A(md(r"""
L'arbre diu que per distingir les tres espècies d'iris n'hi ha prou amb les mesures del
pètal: `petal length` s'emporta el **0.564** de la importància i `petal width` el **0.423**,
o sigui un **0.987** entre tots dos, mentre que les dues mesures del sèpal es queden amb
0.013 i 0.000. Això no ho has programat tu: ho ha après de les dades, i per això el nom
acaba en guió baix.

Fixa't també en l'última línia: `coef_ in dir(arbre)` dona `False`. L'arbre no té
coeficients, perquè un arbre no és un model lineal. **Els atributs acabats en `_` depenen del
model**, i per això `dir()` filtrat és millor que intentar recordar-los.
"""))

# ============================================================ PART 3
A(md(r"""
---

# Part 3 - Una exploració de dades de principi a fi

Ara ho posem tot a treballar. Anem a explorar el dataset dels vins de dalt a baix i, a cada
pas, diré **quin objecte tinc a les mans i què li estic demanant**. Aquest recorregut és el
que faràs cada vegada que et donin dades noves, sempre en el mateix ordre.

El dataset: 178 vins italians de tres varietats, amb 13 mesures químiques de cada un. La
pregunta que l'acompanya és: **es poden distingir les varietats a partir de la química?**
"""))

A(md(r"""
## Pas 1 - Carregar-ho i veure què tinc

Sempre igual: `type()` i `.shape` abans de qualsevol altra cosa.
"""))

A(code(r"""
dades = load_wine(as_frame=True)     # dades és un Bunch
vins = dades.frame                   # vins és un DataFrame

print("dades és un", type(dades).__name__, "amb claus:", list(dades.keys()))
print("vins  és un", type(vins).__name__, "de shape", vins.shape)
print()
print("varietats:", dades.target_names)
"""))

A(md(r"""
178 files i 14 columnes: les 13 mesures més la columna `target`. Li poso un nom més clar a
la columna del target perquè el codi de més avall es llegeixi millor, i faig `.copy()` per
treballar sobre una còpia meva i no tocar el que hi ha dins del `Bunch`.
"""))

A(code(r"""
vins = vins.copy()
vins["classe"] = vins["target"]
vins = vins.drop(columns=["target"])

print(vins.shape)
print(list(vins.columns))
"""))

A(md(r"""
## Pas 2 - Quins tipus, quantes files, hi falta res

`.info()` respon les tres preguntes de cop. Tinc un DataFrame i li demano el resum.
"""))

A(code(r"""
vins.info()
"""))

A(md(r"""
178 entrades, 14 columnes, i totes diuen `178 non-null`: **no falta cap valor**. Tot és
numèric (13 `float64` i la classe `int64`), o sigui que no hauré de convertir text a
números.

Ho comprovo també pel meu compte, que és una línia:
"""))

A(code(r"""
print("valors que falten:", vins.isna().sum().sum())
print("files repetides:  ", vins.duplicated().sum())
"""))

A(md(r"""
## Pas 3 - Quantes classes i quantes mostres de cada

`vins["classe"]` és una **Series**, i a una Series li puc demanar `.value_counts()`.
"""))

A(code(r"""
compte = vins["classe"].value_counts().sort_index()

print(compte)
print()
print("type del resultat:", type(compte).__name__, "-> també és una Series")
print()
print("proporcions:")
print((compte / len(vins)).round(3))
"""))

A(md(r"""
**59, 71 i 48**: un 33.1%, un 39.9% i un 27%. Les classes estan bastant equilibrades, i això
és bona notícia. Si una classe tingués el 95% de les mostres, un model que digués sempre
aquella classe encertaria el 95% sense haver après res, i el `.score()` mentiria.

De passada, el número a batre: si sempre digués "classe 1", encertaria el **39.9%**.
Qualsevol model ha de fer-ho millor que això, o no serveix.
"""))

A(md(r"""
## Pas 4 - La mitjana de cada columna per classe

Aquí ve el pas important, i és on cal anar amb compte amb què tens a les mans:

1. `vins` és un **DataFrame**.
2. `vins.groupby("classe")` **no** és un DataFrame: és un objecte d'agrupació
   (`DataFrameGroupBy`). És una promesa, no una taula. Si l'imprimeixes, no veus dades.
3. `.mean()` sobre aquest objecte **el converteix en un DataFrame nou**, amb una fila per
   classe i una columna per mesura.
"""))

A(code(r"""
agrupat = vins.groupby("classe")

print("type:", type(agrupat).__name__)
print("imprimir-lo no ensenya dades:", agrupat)
print()
print("grups:", list(agrupat.groups.keys()))
print("mides:", agrupat.size().to_dict())
"""))

A(code(r"""
mitjanes = agrupat.mean()

print("type:", type(mitjanes).__name__, " shape:", mitjanes.shape)
print()
print(mitjanes[["alcohol", "flavanoids", "color_intensity", "proline"]].round(2))
"""))

A(md(r"""
Això ja diu coses. Llegeix-ho per files:

- La **classe 0** és la més alcohòlica (**13.74**) i la que té més `proline`, molt destacada:
  **1115.71** contra 519.51 i 629.90.
- La **classe 2** és la que té menys `flavanoids` (**0.78** contra 2.98 i 2.08) i més
  `color_intensity` (**7.40**).
- La **classe 1** queda al mig en gairebé tot, i és la més fluixa en alcohol (**12.28**).

## Pas 5 - Quina columna separa millor les classes

"Les mitjanes són diferents" no n'hi ha prou. `magnesium` fa 106.34, 94.55 i 99.31: són
números diferents, però la columna sencera es mou tant que aquesta diferència es perd dins
del soroll.

El que vols és una mesura que compari **la distància entre les mitjanes** amb **la dispersió
de la columna**. La més senzilla: el rang de les mitjanes dividit per la desviació típica de
la columna. Com més gran, millor separa.
"""))

A(code(r"""
numeriques = vins.drop(columns=["classe"])

rang_mitjanes = mitjanes.max() - mitjanes.min()      # Series: un valor per columna
dispersio = numeriques.std()                         # Series: un valor per columna
separacio = (rang_mitjanes / dispersio).sort_values(ascending=False)

print("type de separacio:", type(separacio).__name__)
print()
print(separacio.round(2))
"""))

A(md(r"""
El rànquing: **`flavanoids` (2.20)**, `od280/od315_of_diluted_wines` (2.08), `proline`
(1.89), `color_intensity` (1.86). I a la cua, `ash` (0.77) i `magnesium` (0.83), que no
separen gairebé res.

Recorda que l'arbre entrenat amb iris deia que les mesures del pètal eren les que
importaven. Això que acabes de calcular a mà és la mateixa idea, i és la que un model
aprofitarà tot sol.

## Pas 6 - Veure-ho

Dibuixem les dues millors columnes, una contra l'altra, amb un color per classe. Si les tres
varietats surten en tres zones separades, un model les distingirà.
"""))

A(code(r"""
fig, (eix1, eix2) = plt.subplots(1, 2, figsize=(11, 4))

colors = {0: "tab:blue", 1: "tab:orange", 2: "tab:green"}

for c in [0, 1, 2]:
    grup = vins[vins["classe"] == c]      # màscara booleana: les files d'aquesta classe
    eix1.scatter(grup["flavanoids"], grup["proline"],
                 color=colors[c], label=f"classe {c}", alpha=0.75, s=28)

eix1.set_xlabel("flavanoids")
eix1.set_ylabel("proline")
eix1.set_title("Les dues columnes que separen més")
eix1.legend()

for c in [0, 1, 2]:
    eix2.hist(vins[vins["classe"] == c]["ash"], bins=12,
              color=colors[c], label=f"classe {c}", alpha=0.6)

eix2.set_xlabel("ash")
eix2.set_ylabel("nombre de vins")
eix2.set_title("Una columna que no separa (ash)")
eix2.legend()

plt.tight_layout()
plt.show()
"""))

A(md(r"""
A l'esquerra, tres núvols bastant separats: es veu a ull que amb dues mesures ja es
distingeixen les varietats. A la dreta, els tres histogrames de `ash` estan encavalcats: si
només tinguessis aquesta columna, no sabries de quina varietat és un vi. Per això `ash`
sortia última al rànquing del Pas 5.

Aquest és el recorregut sencer: `type` i `.shape`, `.info()`, `.value_counts()` del target,
`.groupby().mean()`, buscar què separa, i dibuixar-ho. Sis passos, i ja pots dir alguna cosa
sobre un dataset que no havies vist mai.
"""))

# ---------------------------------------------------------- exercicis
A(md(r"""
---

## Exercicis - ara tu

Quatre preguntes sobre aquestes mateixes dades. **A cada enunciat et dic quins mètodes has
de fer servir**: el nom de la funció no és el que has de descobrir. El que has de descobrir
és **el que surt de les dades**.

Si en algun moment no recordes com es diu alguna cosa, ja saps què fer: `que_te(vins)`,
`que_te(vins, "sort")`, TAB, o `vins.sort_values?`.
"""))

A(md(r"""
### Exercici 1 - Els cinc vins més alcohòlics

Amb **`.sort_values()`** i **`.head()`**: quins són els cinc vins amb més alcohol, i de
quina classe són?

`.sort_values("columna")` ordena de menys a més. Per ordenar de més a menys li has de passar
`ascending=False`. Imprimeix només les columnes `alcohol` i `classe`, que si no surten
catorze.
"""))

A(code(r"""
# Exercici 1

# ordenats = vins.sort_values("alcohol", ascending=False)
# imprimeix les 5 primeres files, només les columnes alcohol i classe:
#   ordenats[["alcohol", "classe"]].head(5)
"""))

A(md(r"""
**Com saps que ho has fet bé:** el primer ha de tenir `14.83` graus (és el que hem trobat
amb `.idxmax()` a la Part 2). I mira la columna `classe` dels cinc: no és casualitat, al Pas
4 hem vist quina varietat era la més alcohòlica.
"""))

A(md(r"""
### Exercici 2 - Quina varietat és més uniforme

Amb **`.groupby()`** i **`.std()`**: per a la columna `proline`, quina de les tres classes
té els vins més semblants entre ells?

La desviació típica mesura com de dispersos són els valors: com més petita, més semblants
entre ells. Agrupa per `classe`, agafa la columna `proline` i demana-li `.std()`. Compara-ho
després amb `.mean()` del mateix grup: la classe amb la mitjana més alta, és també la més
dispersa?
"""))

A(code(r"""
# Exercici 2

# desviacions = vins.groupby("classe")["proline"].std()
# mitjanes_proline = vins.groupby("classe")["proline"].mean()
# imprimeix les dues i digues quina classe és la més uniforme
"""))

A(md(r"""
**Com saps que ho has fet bé:** t'han de sortir tres números, un per classe, i la classe amb
la desviació més petita és la més uniforme. Pista sobre el resultat: la classe que té la
mitjana de `proline` més alta és també la que la té més dispersa, que és un patró
habitualíssim en mesures físiques.
"""))

A(md(r"""
### Exercici 3 - Els vins per damunt de la mitjana

Amb una **màscara booleana** i **`.value_counts()`**: quants vins tenen més alcohol que la
mitjana del dataset, i com es reparteixen per classe?

Calcula primer la mitjana amb `vins["alcohol"].mean()`. Després construeix la màscara
(`vins["alcohol"] > mitjana`), que és una Series de True i False. Aplica-la al DataFrame
(`vins[mascara]`) i demana `.value_counts()` a la columna `classe` del resultat.
"""))

A(code(r"""
# Exercici 3

# mitjana_alcohol = vins["alcohol"].mean()
# mascara = vins["alcohol"] > mitjana_alcohol
# imprimeix quants en són: mascara.sum()
# imprimeix el repartiment: vins[mascara]["classe"].value_counts().sort_index()
"""))

A(md(r"""
**Com saps que ho has fet bé:** `mascara.sum()` t'ha de donar un número entre 0 i 178, i
força a prop de la meitat. Al repartiment per classe, la classe 1 hi ha de ser molt poc
representada: al Pas 4 hem vist que és la de menys alcohol (12.28, per sota de la mitjana
general).
"""))

A(md(r"""
### Exercici 4 - La fitxa del vi més extrem

Amb **`.idxmax()`** i **`.loc`**: troba el vi amb el `color_intensity` més alt i imprimeix
la seva fila sencera. De quina classe és?

`.idxmax()` sobre la columna et dona l'índex de la fila; `vins.loc[aquell_index]` et dona la
fila. Compara després els seus valors amb les mitjanes de la seva classe
(`mitjanes.loc[la_seva_classe]`): en què es desvia més del que és normal a la seva varietat?
"""))

A(code(r"""
# Exercici 4

# posicio = vins["color_intensity"].idxmax()
# fila = vins.loc[posicio]
# imprimeix posicio i fila
# mira de quina classe és: fila["classe"]
# compara-ho amb: mitjanes.loc[fila["classe"]]
"""))

A(md(r"""
**Com saps que ho has fet bé:** `fila` és una **Series** (una fila d'un DataFrame també és
una Series, amb els noms de columna com a índex), no un DataFrame. Comprova-ho amb
`type(fila)`. I la classe que et surti hauria de ser la que al Pas 4 tenia el
`color_intensity` mitjà més alt.
"""))

# ============================================================ resum
A(md(r"""
---

## Resum

**Les quatre eines per interrogar qualsevol objecte:**

- `type(objecte)` - de quina classe és. Sempre la primera pregunta.
- `dir(objecte)` - tot el que té a dins. Filtra-ho:
  `[n for n in dir(obj) if not n.startswith("_")]`.
- `help(objecte.metode)` o, al quadern, `objecte.metode?` - què fa i què li has de passar.
- **TAB** darrere del punt - la que faràs servir el 90% de les vegades.

I `que_te(objecte)`, que ajunta les tres primeres i separa els atributs dels mètodes.

**Els dos guions baixos:**

| On | Què vol dir | Exemple |
|---|---|---|
| al **davant** | cosa interna de Python, no és per a tu | `__len__`, `__init__` |
| al **final** | ho ha après de les dades, **només existeix després de `.fit()`** | `coef_`, `classes_` |

**Atribut o mètode:**

- Atribut = una dada guardada, **sense** parèntesis: `df.shape`, `X.dtype`, `model.coef_`.
- Mètode = una acció, **amb** parèntesis: `df.head()`, `X.mean()`, `model.fit(X, y)`.
- `callable(objecte.nom)` t'ho diu, si tens dubtes.

**Els tres errors que ja has vist aquí, i què volen dir:**

| Error | Vol dir |
|---|---|
| `TypeError: 'tuple' object is not callable` | has posat parèntesis a un atribut |
| a la sortida surt `<bound method ...>` | t'has deixat els parèntesis d'un mètode |
| `AttributeError: coef_` o `NotFittedError` | no has cridat `.fit()` |

**Els cinc objectes:**

| Objecte | D'on surt | El primer que li demanes |
|---|---|---|
| `Bunch` | `load_iris()`, `load_wine()`, `load_digits()` | `.keys()`, `.data.shape` |
| `ndarray` | `.data`, `df.values` | `.shape`, `.dtype`, `.mean(axis=0)` |
| `DataFrame` | `load_wine(as_frame=True).frame` | `.shape`, `.info()`, `.head()` |
| `Series` | `df["columna"]`, `df.loc[fila]` | `.value_counts()`, `.unique()` |
| model | `LogisticRegression()` | `.fit()`, i després `.score()` i `.coef_` |

**El recorregut de sis passos per a un dataset nou:** `type` i `.shape` -> `.info()` ->
`.value_counts()` del target -> `.groupby().mean()` -> buscar quina columna separa ->
dibuixar-ho.

A partir d'aquí, quan un exercici et posi al davant un objecte que no coneixes, ja no estàs
encallat: li preguntes.
"""))

info = escriu(cells, "Machine Learning/01_fonaments/FO_00_objectes_i_autocompletar.ipynb")
print(info)
