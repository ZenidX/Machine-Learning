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

**Objectiu:** que en surtin amb **un mètode**, no amb una llista de funcions. El mètode són cinc
preguntes que es fan a qualsevol conjunt de dades, i el descobreixen fent-les, no llegint-les.

### Per què aquesta sessió existeix

La del 28 no va acabar de funcionar: se'ls va llançar contra els exercicis i van quedar
encallats. **No és culpa seva ni de l'enunciat**, és que els faltava una peça: no sabien que
`dades.data` existeix, ni que `df.shape` va sense parèntesis, ni que un model entrenat guarda el
que ha après en atributs acabats en guió baix. I sobretot no sabien **com esbrinar-ho**.

**Comença dient-ho.** Si creuen que van encallar per falta de cap, s'ho creuran tota
l'assignatura. La frase, si serveix:

> Ahir us vau quedar encallats i no era cosa vostra. Us faltava saber una cosa que no us havia
> explicat ningú: que a un objecte de Python se li pot preguntar què té a dins. Avui ho fem, i
> a partir d'aquí podreu anar sols.

### Les cinc preguntes: escriu-les a la pissarra i deixa-les tot el dia

Són l'espina dorsal de la sessió i del curs. **Posa-les al principi com a promesa** («al final de
les dues hores sabreu fer-vos aquestes cinc preguntes davant de qualsevol fitxer de dades») i
torna-hi cada vegada que el quadern n'usi una.

1. **Què és això?** → `type()`
2. **Què porta dins?** → `dir()` filtrat, `.keys()`, `.columns`
3. **Quina mida té i de quins tipus?** → `.shape`, `.dtypes`, `.info()`
4. **Hi falta res? Hi ha repetits?** → `.isna().sum()`, `.duplicated().sum()`
5. **Com es reparteix el que vull predir?** → `.value_counts()`, `.groupby()`

### Repartiment: tres actes, i hi caben tots

**Sí que hi caben els tres actes sencers.** No és optimisme, és mesurat: comptant les paraules de
cada cel·la de text a 130 per minut i cada cel·la de codi a 45 segons d'executar i comentar, el
quadern sencer dona **116 minuts**, que no hi cabrien. Però d'aquests 116, **32 no són de classe**:

| Tram | Temps mesurat | Va a classe? |
|---|---|---|
| Portada i les cinc preguntes | 3 min | Sí |
| **Acte 1 · Wine** | **51 min** | Sí |
| **Acte 2 · Digits** | **14 min** | Sí |
| **Acte 3 · El model** | **16 min** | Sí |
| La xuleta | 20 min | **No: és referència, es llegeix a casa** |
| Els quatre exercicis | 12 min | **No: van a casa** |

Els tres actes més la portada són **84 minuts**. Amb 110 minuts útils de sessió, queden **uns 25
minuts de marge per a preguntes**, que amb aquest grup no és un luxe sinó una necessitat.

| Temps | Què |
|---|---|
| 8 min | El reconeixement de sobre i **les cinc preguntes a la pissarra**. I què canvia a partir d'avui: els enunciats diran quina eina fer servir; el resultat, no. |
| 51 min | **Acte 1 · «Què hi ha aquí dins?»** Wine. El quadern arrenca en fals a posta: `load_wine()` i prou. Cada eina entra **quan l'anàlisi es queda encallada sense ella**. |
| 14 min | **Acte 2 · «I ara, amb un que no has vist mai.»** `load_digits()` i les cinc preguntes, sense cap taula ni cap pista. |
| 16 min | **Acte 3 · «El model també és un objecte.»** Entrenen alguna cosa i li fan les mateixes preguntes. |
| 5 min | Assenyalar la xuleta i repartir la feina de casa. |
| ~25 min | **Marge.** Preguntes, ordinadors que no arrenquen, i el que s'allargui. |

### La manera d'anar a aquest ritme

L'acte 1 té **40 cel·les de text i 2.873 paraules**. Llegides en veu alta són 22 minuts, i llegir
en veu alta el que ells poden llegir amb els ulls és la manera més segura de no arribar.

**El repartiment que funciona: el text el llegeixen ells, el codi l'executes tu.** Tu vas
executant i comentant en una frase què acaba de sortir, i **t'atures de debò només en tres
moments**:

1. **L'error dels parèntesis**, quan `dades.data.shape()` peta amb `TypeError`.
2. **El `bound method`**, que no peta i és el que els menjarà mitja hora si no el veuen aquí.
3. **El pas de números a `DataFrame`**, quan es veu que sense noms de columna no es pot analitzar res.

La resta de l'acte 1 és encadenar preguntes, i va de pressa si no t'hi encalles.

### Acte 1 — el fil és «em cal això per continuar»

**No expliquis res per endavant.** L'ordre del quadern és l'ordre de la necessitat, i és el que
has de respectar en veu alta:

`type(dades)` dona `Bunch`, una paraula que no els diu res → per saber què hi porta cal `dir()`,
i **amb un `Bunch` surten sis noms nets**, perquè scikit-learn sobreescriu `__dir__`. Digues que
això és l'excepció: **el soroll dels guions baixos i el filtre arriben un pas més tard**, sobre
l'array de `dades.data`, on `dir()` torna 169 noms i el filtre els deixa en 73. Allà el filtre no
és un tecnicisme, és necessari.

`dades.data` és una altra cosa, i **la pregunta es repeteix amb el que hi ha a dins** → quina mida
té: `.shape`.

**I aquí, no abans, arriba l'error dels parèntesis.** És natural escriure `dades.data.shape()`, i
el `TypeError: 'tuple' object is not callable` cau just on els passaria de veritat. És el moment
d'introduir atribut contra mètode, amb la regla curta —**dada sense parèntesis, feina amb**— i
amb l'altre cas, el que **no peta**:

```
print(df.head)   →   <bound method NDFrame.head of ...>
```

**La frase que els resol la vida:** quan veus `bound method` a la sortida, t'has deixat els
parèntesis. És tot el diagnòstic que necessiten.

Després: tenim números però no noms de columna, i sense noms no s'analitza res → `.feature_names`
i `.target_names` → i la via bona, `load_wine(as_frame=True).frame`, que dona un `DataFrame`.
D'aquí les preguntes 3, 4 i 5, cada mètode perquè respon una pregunta i no perquè toca la taula.

**Un detall de la pregunta 4 que val la pena no amagar:** a Wine no falta cap valor i no hi ha
duplicats. Això no és un anticlímax, és una informació, i és excepcional. Digues que al quadern de
Pandas, el 13 d'octubre, veuran un fitxer real amb el 47 % de nuls en una columna.

### Acte 2 — el que demostra que el mètode val

**Aquest acte és el cor de la sessió i el que no pots retallar.** Se'ls dona `load_digits()` i les
cinc preguntes, i res més: cap taula, cap llista de mètodes, cap pista de què hi trobaran.

El premi arriba a la pregunta 2: apareix **`.images`**, que a Wine no hi era. Que descobreixin
ells que és el mateix que `.data` amb una altra forma —1797×64 contra 1797×8×8— i que ho
comprovin amb `.reshape()` i `np.array_equal`.

**Aquí el mètode els ha ensenyat una cosa que ningú els havia dit.** Fes-ho explícit: no ho han
llegit enlloc, ho han trobat preguntant. Dues o tres cel·les d'aquest acte estan buides a posta.

### Acte 3 — i el model també

Ja han analitzat les dades; ara entrenen alguna cosa i li fan **les mateixes cinc preguntes**.

`dir()` filtrat abans del `.fit()`, el `.fit()`, `dir()` filtrat després: **el salt real de 27 a
33 noms**, i els sis que apareixen de zero són els acabats en guió baix. Els dos errors reals
—`AttributeError` demanant `.coef_` abans d'entrenar, `NotFittedError` predient sense
entrenar— i el contrast amb un arbre, que aprèn uns altres atributs i **no té `coef_`**.

**La conclusió de la sessió:** un model entrenat no és una caixa negra, és un objecte, i se li pot
preguntar què ha après.

Això et sembra la S09 del 20 d'octubre: quan treguin el `.coef_` d'una logística per fer la
predicció a mà, ja sabran què estan traient i per què hi és.

### Els dos guions baixos, que són coses diferents

No ho trauran sols. Val la pena deixar-ho a la pissarra al costat de les cinc preguntes:

| On | Què vol dir |
|---|---|
| **al davant** (`__len__`) | intern de Python, no és per a tu — per això es filtra el `dir()` |
| **al final** (`coef_`) | **ho ha après de les dades**, i no existeix abans del `.fit()` |

### Què faran mal, i què dir

**Voldran memoritzar la taula de mètodes.** Talla-ho: la taula és de consulta, i per això és al
final i no al principi. El que s'aprèn és el TAB.

**Llegiran el `dir()` sencer i s'espantaran.** Sobre un DataFrame surten 193 mètodes. Ensenya'ls
el filtre i el `que_te(objecte, "na")` per buscar per text.

**Preguntaran per què `.loc` va amb claudàtors.** És l'excepció honesta del quadern: `callable()`
diu que sí que és invocable, però s'indexa. No t'allarguis.

**I algú preguntarà de què serveix això per fer machine learning.** La resposta curta: un model
entrenat és un objecte, i tot el que ha après és als seus atributs. Qui no sap mirar dins d'un
objecte, té els models com a caixes negres per sempre.

### Si tot i així vas just

El marge de 25 minuts se't pot menjar una aula amb ordinadors lents o una tanda de preguntes
bona, i si passa val més gastar-lo en les preguntes que córrer. L'ordre de retallada:

1. **L'acte 3**, que es reprèn en cinc minuts al començament de la S05 i no bloqueja res: el que
   hi ha allà es torna a necessitar el 20 d'octubre, a la sessió d'àlgebra lineal.
2. **La segona meitat de l'acte 1**, de `as_frame=True` endavant, com a lectura. Les preguntes 3,
   4 i 5 sobre el `DataFrame` es tornen a fer senceres als quaderns de Pandas.

**L'acte 2 no es toca.** Són 14 minuts i és l'únic tram on el mètode es posa a prova amb dades que
no han vist. Si el retalles, el quadern torna a ser un manual.

I si va al revés, si sobren vint minuts: que comencin els exercicis a classe, que és on veuràs de
debò si el mètode els ha quedat.

### Com saps que ha anat bé

Si al final algú, davant d'un objecte que no coneix, **escriu `dir()` o prem TAB en lloc
d'aixecar la mà**, la sessió sencera ha valgut.

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
