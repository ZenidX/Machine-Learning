# Guions del bloc 1 — Fonaments de dades i àlgebra

Set sessions, del 29 de setembre al 26 d'octubre. Un guió per sessió, per obrir i tirar.

El material és a `Machine Learning/01_fonaments/`, a `Machine Learning/03_matematiques/` i, quan
es diu, a `_moodle-25-26/material-complet/` (els quaderns de la docent anterior).

**La frase que obre el bloc**, i val la pena dir-la tal qual el primer dia:

> La setmana passada vau veure què fa un arbre de decisió i què fa un k-NN. Avui anem a
> buscar l'eina que us falta per fer-ho vosaltres. Sense saber manejar una taula de dades,
> tot això es queda en un dibuix a la pissarra.

**I la que tanca la primera part**, per a la S08, que és la sessió que aquest grup recordarà:

> Un model entrenat no és una caixa. És un vector de quatre números. Avui li traurem els
> números i farem la predicció a mà.

---

## S06 · dimarts 29 de setembre · NumPy 1

**Objectiu:** que entenguin què és un array i el sàpiguen indexar.

| Temps | Què |
|---|---|
| 10 min | Per què NumPy i no llistes. **Executa la comparació de temps en directe**: sumar un milió de números amb llista i amb array. La diferència es veu sola. |
| 25 min | L'array: crear-lo, `shape`, `dtype`. Arrays de 2 dimensions. **Connecta-ho amb Iris**: 150 files per 4 columnes és exactament un array 2D. |
| 30 min | Indexació i llesques. `X[:, 0]` com a «totes les files, primera columna», que és com s'agafa una característica. |
| 15 min | El parany de la llesca contra la còpia. |
| 40 min | Exercicis 1 a 3 del quadern. |

**Si es queden encallats:** el problema sol ser `[fila, columna]` contra `[fila][columna]`. Dibuixa la
taula a la pissarra i assenyala el que retorna cada cosa.

---

## S07 · dilluns 5 d'octubre · NumPy 2

**Objectiu:** operacions sense bucles, i que `axis` deixi de fer por.

| Temps | Què |
|---|---|
| 20 min | Operacions vectoritzades. Ensenya el bucle equivalent al costat, perquè vegin què s'estalvien. |
| 30 min | Màscares booleanes. `X > 5`, `X[X > 5]`, combinar amb `&` i `\|`. **Avisa que `and` no funciona**, que ho provaran i petarà. |
| 30 min | Agregacions i **el concepte d'eix**. `axis=0` dona un valor per columna, `axis=1` per fila. Fes-ho amb una matriu de 3×4 a la pissarra abans de tocar el codi. |
| 20 min | Les dues coses que ja han vist sense saber-ho: la distància euclidiana és `np.sqrt(((a-b)**2).sum())` i la precisió és `(prediccions == reals).mean()`. **Aquest és el moment de la sessió**, i és la porta de la següent. |
| 20 min | Exercicis 4 a 7. |

**L'eix és el que més costa de tot el bloc.** Si en surten amb això clar, la sessió ha anat bé.

---

## S08 · dimarts 6 d'octubre · Àlgebra lineal

**Quadern:** `03_matematiques/MA_01_algebra_lineal.ipynb`

**Objectiu:** que vegin que les dades, els pesos i les prediccions són objectes geomètrics, i
que un model entrenat és un vector de números.

Aquesta és la primera sessió del bloc de matemàtiques i **marca el to de tot el curs**: aquí
es demostra que la teoria que se'ls ha explicat a la pissarra es pot escriure en tres línies
de NumPy i comprovar.

| Temps | Què |
|---|---|
| 15 min | Un vector és un punt i una fletxa. Una flor amb 4 mesures és un punt en 4 dimensions. Dibuixa'n dues. |
| 20 min | La norma com a Pitàgores estès. Implementada a mà i comparada amb `np.linalg.norm`. **Tanca el cercle amb la S07**: la distància euclidiana és la norma de la diferència, i és el que van implementar al k-NN. |
| 30 min | El producte escalar per les dues definicions, la de la suma de productes i la de $\|a\|\|b\|\cos\theta$, i que donen el mateix número. D'aquí surt l'angle, i que perpendicular vol dir producte escalar zero. |
| 20 min | La projecció d'un vector sobre un altre, amb el dibuix. Diguis que d'aquí sortiran les fronteres, el marge de l'SVM i el PCA. |
| 30 min | **El moment de la sessió.** Una matriu és dades i és transformació. `X @ w + b` dona una puntuació per fila. Agafa un `LogisticRegression` entrenat, treu-li `coef_` i `intercept_`, calcula el signe a mà i comprova que encerta les 150 files. |
| 5 min | La transposada, i que `X.T @ X` surt a tot arreu. Deixa-ho apuntat, es reprèn al PCA. |

**Si sobra temps:** els exercicis del quadern. Si no, van a casa.

**La pregunta que et faran:** «llavors entrenar què és?». No la responguis del tot: digues que
és trobar aquests números, i que es veurà a la S19. Que es quedin amb la pregunta oberta.

---

## S09 · dimarts 13 d'octubre · Pandas 1

> El 12 és festiu, així que aquesta setmana només hi ha dimarts.

**Objectiu:** carregar un CSV de veritat i saber-ne treure el que vulguis.

| Temps | Què |
|---|---|
| 15 min | Què afegeix Pandas sobre NumPy: noms de columna i tipus barrejats. Els dos de costat. |
| 20 min | Series i DataFrame. `head`, `shape`, `dtypes`, `describe`, `info`. |
| 25 min | Carregar `melb_data.csv`, que són habitatges de Melbourne de veritat, amb nuls i columnes de text. Mirar-lo abans de tocar-lo. |
| 40 min | Seleccionar: columnes, `loc` contra `iloc`, filtres amb condicions. **Els parèntesis en combinar condicions són obligatoris**; avisa-ho abans que hi caiguin. |
| 20 min | Exercicis 1 a 3. |

---

## S10 · dilluns 19 d'octubre · Pandas 2

**Objectiu:** tancar el cercle, del CSV al model.

| Temps | Què |
|---|---|
| 25 min | Valors que falten: `isna().sum()` per fer l'inventari, i què costa cada estratègia. Amb `melb_data.csv` això no és teòric. |
| 30 min | `groupby` i `agg`. Exemple que enganxa: preu mitjà per barri i per nombre d'habitacions. |
| 20 min | Gràfics ràpids des del DataFrame. |
| 30 min | **Del DataFrame al model**: com es passa a les `X` i `y` de scikit-learn. Un exemple mínim entrenant amb dades d'un CSV. **Aquí es tanca el bloc**: ja poden fer sols el que van veure a la S04. |
| 15 min | Exercicis. |

---

## S11 · dimarts 20 d'octubre · El que va quedar de Python

**Objectiu:** tapar els forats de Python que es notaran més endavant.

Aquí es fan servir **els quaderns de la docent anterior**, que són a
`_moodle-25-26/material-complet/`: `Estructures_iteratives.ipynb`, `Diccionaris.ipynb`,
`Definicions.ipynb` i `Una mica de tot.ipynb`.

| Temps | Què |
|---|---|
| 30 min | Diccionaris. Es fan servir a tot arreu (paràmetres dels models, resultats). |
| 30 min | Funcions pròpies, amb `Definicions.ipynb`. |
| 30 min | Comprensions de llista, que estalvien molt codi i surten a tots els exemples. |
| 30 min | `Una mica de tot.ipynb` com a repàs. |

**Per què aquí i no abans:** ara ja saben per a què els serveix. Un diccionari explicat en abstracte
s'oblida; un diccionari que configura un model, no.

---

## S12 · dilluns 26 d'octubre · Prova pràctica 1 i tancament

| Temps | Què |
|---|---|
| 60 min | **Prova pràctica 1**, amb ordinador. Format: dues o tres cel·les buides sobre un CSV que no hagin vist, del mateix estil que els exercicis. Carregar, netejar una mica, respondre dues preguntes amb `groupby` i fer un gràfic. Una quarta cel·la, curta: calcular una distància o una norma a mà amb NumPy. |
| 30 min | Correcció en comú dels errors més repetits. |
| 30 min | **Presentació del bloc següent**: tornen els models, però ara els faran ells i n'obriran les tripes. Ensenya'ls la pàgina de pràctica de la web i digues que **els exercicis dels quaderns van a casa**, perquè el temps de classe se'l menjarà la matemàtica. |

**Avís important d'aquesta sessió:** és on es comprova si el trueque de la programació funciona.
Si es veu que no faran els exercicis pel seu compte, hi ha el pla B a
[`diagnostic-i-programacio-2627.md`](diagnostic-i-programacio-2627.md), secció 2.5.

---

## Com saber si el bloc ha anat bé

Al final d'aquestes set sessions, un alumne hauria de poder, **sense ajuda**:

- Carregar un CSV i dir quantes files i columnes té i quins nuls.
- Filtrar per una condició i respondre una pregunta amb `groupby`.
- Passar un DataFrame a `X` i `y` i entrenar un model.
- Calcular una distància, una norma i un producte escalar amb NumPy, i dir què signifiquen.
- **Explicar què hi ha dins d'un model lineal entrenat**, i fer-ne una predicció a mà.

Les tres primeres són el mínim per continuar. Si no hi són, **val més gastar una sessió més aquí
que continuar**: tot el bloc 2 se sosté sobre això.
