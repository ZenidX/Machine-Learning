# Guions del bloc 1 — Fonaments de dades

Vuit sessions, del 29 de setembre al 27 d'octubre. Un guió per sessió, per obrir i tirar.

Material a `Machine Learning/01_fonaments/`, a `Machine Learning/03_matematiques/` i, quan es
diu, a `_moodle-25-26/material-complet/` (els quaderns de la docent anterior).

> **Regla que val per a tot el bloc, i per a tot el curs.** L'enunciat **sí** que diu quina eina
> fer servir: endevinar el nom d'un mètode no ensenya res. El que l'enunciat **no** diu és quin
> resultat sortirà, perquè això és l'anàlisi i és la feina de l'alumne. Hi ha el raonament a
> [`didactica-matematica-ml.md`](didactica-matematica-ml.md), secció «Com es dissenya un exercici».

---

## S04 · dimarts 29 de setembre · Objectes de Python i primera anàlisi de dades

**Quadern:** `01_fonaments/FO_00_objectes_i_autocompletar.ipynb`

**Objectiu:** que puguin treballar sols. En sortir d'aquí han de saber **interrogar un objecte**
i haver fet una exploració de dades de principi a fi.

### Per què aquesta sessió existeix

La del 28 no va acabar de funcionar: se'ls va llançar contra els exercicis i van quedar
encallats. **No és culpa seva ni de l'enunciat de l'exercici, és que els faltava una peça**: no
sabien que `dades.data` existeix, ni que `df.shape` va sense parèntesis, ni que un model
entrenat guarda el que ha après en atributs acabats en guió baix. I sobretot no sabien **com
esbrinar-ho**.

**Comença dient-ho.** Val més reconèixer-ho que fer com si res: si creuen que van encallar per
falta de cap, s'ho creuran tota l'assignatura. La frase, si serveix:

> Ahir us vau quedar encallats i no era cosa vostra. Us faltava saber una cosa que no us havia
> explicat ningú: que a un objecte de Python se li pot preguntar què té a dins. Avui ho fem, i
> a partir d'aquí podreu anar sols.

### Repartiment

| Temps | Què |
|---|---|
| 10 min | El reconeixement de sobre, i **què canvia a partir d'avui**: els enunciats diran quina eina fer servir. El que no diran és el resultat, perquè aquesta és la seva part. |
| 30 min | **Interrogar un objecte.** `type()`, `dir()` i com filtrar-ne el soroll, `help()`, i a Colab `objecte.metode?`. **Insisteix en l'autocompletat amb TAB**: ningú es recorda els noms de memòria, i creure que cal és el que els bloqueja. |
| 15 min | **Atribut contra mètode**, que és la confusió que més els costarà. `df.shape` sense parèntesis, `df.head()` amb. **Ensenya els dos errors en directe**: `df.shape()` dona `TypeError: 'tuple' object is not callable`, i `df.head` sense parèntesis els imprimeix una descripció del mètode en lloc de les dades. Els veuran avui; val més que els vegin aquí. |
| 25 min | **Els cinc objectes que es trobaran**: el `Bunch` de `load_wine()` amb `.data` i `.target`; l'`ndarray` amb `.shape` i `.mean(axis=0)`; el `DataFrame` i la `Series`; i **un model abans i després d'entrenar**. Aquí va la convenció del guió baix final: `.coef_` i `.feature_importances_` vol dir «això l'he après de les dades», i **no existeixen abans de cridar `.fit()`**. |
| 30 min | **L'exploració guiada**, amb el codi escrit i executable, que és el que demanava la sessió: quantes files i columnes, quins tipus, quantes mostres per classe, la mitjana per classe amb `.groupby()`, i un gràfic. **Comenta a cada pas quin objecte tens a les mans i què li demanes.** Que la modifiquin en directe. |
| 10 min | Les preguntes obertes del final, que l'enunciat ja els diu amb quin mètode es responen. Les que no acabin, a casa. |

### El que ha de quedar dit abans de marxar

- **A un objecte se li pregunta.** `type`, `dir`, `?` i TAB. No s'estudia de memòria.
- **Atribut sense parèntesis, mètode amb.**
- **Guió baix al final = après de les dades**, i només existeix després del `.fit()`.
- I que **la caixa d'eines** `02_practica/EX_00_caixa_eines.ipynb` és la referència de totes les
  funcions que faran servir, amb un exemple mínim i el parany de cada una. Que se l'obrin al
  costat sempre.

### Si sobra temps

Que comencin els exercicis de `FO_01_numpy.ipynb`. Si en falta, la sessió es tanca a
l'exploració guiada: el que no es pot deixar per a casa és la part d'interrogar l'objecte.

---

## S05 · dilluns 5 d'octubre · NumPy 1

**Quadern:** `01_fonaments/FO_01_numpy.ipynb`

**Objectiu:** que entenguin què és un array i el sàpiguen indexar.

| Temps | Què |
|---|---|
| 10 min | Per què NumPy i no llistes. **Executa la comparació de temps en directe**: sumar un milió de números amb llista i amb array. Surt unes 25 vegades més ràpid, i es veu sol. |
| 25 min | L'array: crear-lo, `.shape`, `.dtype`. Arrays de 2 dimensions. **Connecta-ho amb Iris**: 150 files per 4 columnes és exactament un array 2D. |
| 30 min | Indexació i llesques. `X[:, 0]` com a «totes les files, primera columna», que és com s'agafa una característica. |
| 15 min | El parany de la llesca contra la còpia, i per això existeix `.copy()`. |
| 40 min | Exercicis 1 a 3 del quadern. |

**Si es queden encallats:** el problema sol ser `[fila, columna]` contra `[fila][columna]`. Dibuixa
la taula a la pissarra i assenyala el que retorna cada cosa.

---

## S06 · dimarts 6 d'octubre · NumPy 2

**Objectiu:** operacions sense bucles, i que `axis` deixi de fer por.

| Temps | Què |
|---|---|
| 20 min | Operacions vectoritzades. Ensenya el bucle equivalent al costat, perquè vegin què s'estalvien. |
| 30 min | Màscares booleanes. `X > 5`, `X[X > 5]`, combinar amb `&` i `\|`. **Avisa que `and` no funciona** i que cada condició va entre parèntesis: ho provaran i petarà. |
| 30 min | Agregacions i **el concepte d'eix**. `.mean()` dona un número, `.mean(axis=0)` un per columna, `axis=1` un per fila. Fes-ho amb una matriu de 3×4 a la pissarra abans de tocar el codi. |
| 20 min | Les dues coses que ja han vist sense saber-ho: la distància euclidiana és `np.sqrt(((a-b)**2).sum())` i la precisió és `(prediccions == reals).mean()`. **Aquest és el moment de la sessió.** |
| 20 min | Exercicis 4 a 7. |

**L'eix és el que més costa de tot el bloc.** Si en surten amb això clar, la sessió ha anat bé.

---

## S07 · dimarts 13 d'octubre · Pandas 1

> El 12 és festiu, així que aquesta setmana només hi ha dimarts.

**Quadern:** `01_fonaments/FO_02_pandas.ipynb`

**Objectiu:** carregar un CSV de veritat i saber-ne treure el que vulguis.

| Temps | Què |
|---|---|
| 15 min | Què afegeix Pandas sobre NumPy: noms de columna i tipus barrejats. Els dos de costat. |
| 20 min | `DataFrame` i `Series`, amb `.head()`, `.shape`, `.dtypes`, `.describe()`, `.info()`. **Ja saben interrogar l'objecte de la S04**: que ho facin ells amb `dir()` abans que tu els donis la llista. |
| 25 min | Carregar `melb_data.csv`, 13.580 habitatges de Melbourne de veritat, amb nuls i columnes de text. **Es mira abans de tocar-lo**, sempre. |
| 40 min | Seleccionar: columnes, `.loc` contra `.iloc`, filtres amb condicions. **Els parèntesis en combinar condicions són obligatoris**; avisa-ho abans que hi caiguin. |
| 20 min | Exercicis 1 a 3. |

---

## S08 · dilluns 19 d'octubre · Pandas 2

**Objectiu:** tancar el cercle, del CSV al model.

| Temps | Què |
|---|---|
| 25 min | Valors que falten: `.isna().sum()` per fer l'inventari, i què costa cada estratègia. Amb aquestes dades no és teòric: `.dropna()` sencer se'n porta el 54,4 % de les files. |
| 30 min | `.groupby()` i `.agg()`. Exemple que enganxa: preu mitjà per barri i per nombre d'habitacions. |
| 20 min | Gràfics ràpids amb `.plot()`. |
| 30 min | **Del DataFrame al model**: com es passa a les `X` i `y` de scikit-learn. Un exemple mínim entrenant amb dades d'un CSV. **Aquí es tanca el bloc**: ja poden fer sols el que van veure explicat a la S02. |
| 15 min | Exercicis. |

---

## S09 · dimarts 20 d'octubre · Àlgebra lineal

**Quadern:** `03_matematiques/MA_01_algebra_lineal.ipynb`

**Objectiu:** que vegin que les dades, els pesos i les prediccions són objectes geomètrics, i que
un model entrenat és un vector de números.

És la primera sessió del bloc de matemàtiques i **marca el to del curs**: la teoria que se'ls ha
explicat es pot escriure en tres línies de NumPy i comprovar.

| Temps | Què |
|---|---|
| 15 min | Un vector és un punt i una fletxa. Una flor amb 4 mesures és un punt en 4 dimensions. Dibuixa'n dues. |
| 20 min | La norma com a Pitàgores estès, a mà i contra `np.linalg.norm`. **Tanca el cercle amb la S06**: la distància euclidiana és la norma de la diferència. |
| 30 min | El producte escalar per les dues definicions, i que donen el mateix número. D'aquí surt l'angle, i que perpendicular vol dir producte escalar zero. |
| 20 min | La projecció d'un vector sobre un altre, amb el dibuix. D'aquí sortiran les fronteres, el marge de l'SVM i el PCA. |
| 30 min | **El moment de la sessió.** Agafa una `LogisticRegression` entrenada, treu-li `.coef_` i `.intercept_` —**que ja saben què volen dir els guions baixos, de la S04**— calcula `X @ w + b` a mà, i comprova que el signe encerta les 150 files. Diferència màxima: zero. |
| 5 min | La transposada, i que `X.T @ X` surt a tot arreu. Es reprèn al PCA. |

**La pregunta que et faran:** «llavors entrenar què és?». No la responguis del tot: digues que és
trobar aquests números i que es veurà a la S19. Que es quedin amb la pregunta oberta.

---

## S10 · dilluns 26 d'octubre · El que va quedar de Python

**Objectiu:** tapar els forats de Python que es notaran més endavant.

Amb **els quaderns de la docent anterior**, a `_moodle-25-26/material-complet/`:
`Estructures_iteratives.ipynb`, `Diccionaris.ipynb`, `Definicions.ipynb` i `Una mica de tot.ipynb`.

| Temps | Què |
|---|---|
| 30 min | Diccionaris. Es fan servir a tot arreu: paràmetres dels models, resultats, el `models = {...}` dels exercicis. |
| 30 min | Funcions pròpies, amb `Definicions.ipynb`. |
| 30 min | Comprensions de llista, que estalvien molt codi i surten a tots els exemples. |
| 30 min | `Una mica de tot.ipynb` com a repàs. |

**Per què aquí i no abans:** ara ja saben per a què els serveix. Un diccionari explicat en abstracte
s'oblida; un diccionari que configura un model, no.

---

## S11 · dimarts 27 d'octubre · Prova pràctica 1 i tancament

| Temps | Què |
|---|---|
| 60 min | **Prova pràctica 1**, amb ordinador. Format: dues o tres cel·les buides sobre un CSV que no hagin vist, del mateix estil que els exercicis, **amb l'enunciat dient quines eines fer servir**. Carregar, fer l'inventari de nuls, respondre dues preguntes amb `.groupby()` i fer un gràfic. Una quarta cel·la curta: calcular una norma o una distància amb NumPy. |
| 30 min | Correcció en comú dels errors més repetits. |
| 30 min | **Presentació del bloc següent**: tornen els models, i ara els faran ells i n'obriran les tripes. Ensenya'ls la pàgina de pràctica de la web i digues que **els exercicis van a casa**, perquè el temps de classe se'l menjarà la matemàtica. |

**Avís:** aquesta sessió és on es comprova si el trueque de la programació funciona. Si es veu que
no faran els exercicis pel seu compte, hi ha el pla B a
[`diagnostic-i-programacio-2627.md`](diagnostic-i-programacio-2627.md), secció 2.5.

---

## Com saber si el bloc ha anat bé

Al final d'aquestes vuit sessions, un alumne hauria de poder, **sense ajuda**:

- **Agafar un objecte que no coneix i esbrinar què té a dins**, amb `type`, `dir` i l'autocompletat.
- Carregar un CSV i dir quantes files i columnes té i quins nuls.
- Filtrar per una condició i respondre una pregunta amb `.groupby()`.
- Passar un DataFrame a `X` i `y` i entrenar un model.
- Calcular una distància, una norma i un producte escalar, i dir què signifiquen.
- **Explicar què hi ha dins d'un model lineal entrenat**, i fer-ne una predicció a mà.

La primera és la que es guanya avui i la que sosté totes les altres. Si les tres primeres no hi
són a la S11, **val més gastar una sessió més aquí que continuar**: tot el bloc 2 se sosté sobre
això.
