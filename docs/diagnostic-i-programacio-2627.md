# Diagnòstic del curs i programació 2026-27

Optativa d'Aprenentatge automàtic · MPOML · DAM i DAW, 2n curs
**66 h · 4 h setmanals · sessions de 2 h dilluns i dimarts**

---

# Part 1 — Diagnòstic

## 1.1 El que sabem del marc oficial, i el que no

La **fitxa d'inici del mòdul** diu 66 h en una UF única, amb un resultat d'aprenentatge únic: «Crea aplicacions fent ús de models d'aprenentatge automàtic». Això queda confirmat.

El que **no** quadra és la resta. La fitxa parla de 2 h setmanals i d'una avaluació de 10 % proves escrites, 10 % activitats i 80 % proves pràctiques. La presentació que es va passar al grup el curs 25-26 deia 4 h setmanals i una avaluació de 60 % proves escrites en paper i 40 % projectes.

**La realitat d'aquest curs són 4 h setmanals**, o sigui que en aquest punt mana la presentació i no la fitxa. Això obliga a mirar-se també l'altra discrepància: **cal confirmar quina avaluació val abans d'anunciar percentatges a l'alumnat**. Fins llavors, ni la web ni cap document en donen.

## 1.2 D'on venim: què tenia muntat la Núria

El curs passat el portava una altra docent. El seu recorregut era: **Python des de zero** amb lliuraments curts setmanals → **Jupyter i Colab** → **Pandas** → un **projecte d'anàlisi i representació de dades** → **aprenentatge supervisat resolt amb DataCamp** → i, l'últim mes, el bloc de **Reinforcement Learning** que impartia en Xavi.

A la seva programació hi havia, a més, blocs que el curs passat no es van arribar a fer o van quedar amagats: **arbres de decisió**, **tècniques d'optimització** (nuls, categòriques, pipelines) i **programació en R**.

**Material seu que s'ha recuperat i és aprofitable** (a `_moodle-25-26/material-complet/`):

| Què | Per a què serveix ara |
|---|---|
| 9 quaderns de Python (introducció, estructures selectives i iteratives, definicions, diccionaris, classes, lambda, exercicis) | Són els enunciats reals del bloc de Python, que al Moodle apareixien buits |
| `Pipeline.ipynb`, `Exercici Pipelines.ipynb`, `ExempleIris.py`, `DadesEntrenamentTest.py` | El bloc de preparació de dades, ja plantejat |
| `melb_data.csv` (habitatges de Melbourne, amb nuls i text) | **El conjunt de dades del manual de Pandas**: realista i ja conegut |
| `train.csv` i `test.csv` | Dataset de competició |
| Un zip amb 26 imatges de gats, entrenament i prova | Un exercici de classificació d'imatges que no sabíem que existia |
| PDFs d'arbres de decisió, boscos aleatoris i repositori de preguntes | Teoria ja escrita d'aquests dos models |

A `_moodle-25-26/ENLLACOS.md` hi ha, a més, les adreces de **les seves presentacions de Google**: introducció a ML, tipus de models, models i algorismes, variables categòriques, pipelines i **les cinc del bloc de R**. Viuen al seu Drive, així que convé demanar-ne còpia abans de dependre'n.

## 1.3 On són els alumnes ara (29 de setembre)

S'han consumit **5 de les 33 sessions**:

| | Data | Què s'hi va fer |
|---|---|---|
| S01-S02 | 14 i 15 set | Presentació i Python bàsic |
| S03 | 21 set | Python fins als condicionals |
| S04 | 22 set | **Els models de ML supervisat, explicats conceptualment**, amb els exemples d'Iris |
| S05 | 28 set | Primera pràctica contra conjunts de dades |

**El diagnòstic, en una frase:** tenen la intuïció dels models i tenen Python bàsic, però **els falta la peça del mig**. Saben què fa un arbre de decisió i saben escriure un `if`, però no saben manejar una taula de dades. Sense NumPy i Pandas no poden fer els exercicis que ja estan preparats, i tot el que vingui després se'ls farà a cegues.

**Per això el curs continua per NumPy i Pandas**, i no per més models.

## 1.4 El grup: el que canvia la planificació sencera

Hi ha un fet que no es pot tractar com una anècdota, perquè condiciona tot el que ve després.

L'optativa es va plantejar difícil a posta, es va anunciar com a difícil, i **tot i això s'hi han apuntat 15 alumnes que estan contents precisament per això**. El que els enganxa no és fer córrer models: és **entendre la matemàtica que hi ha a sota i el perquè de les coses**.

Això inverteix el risc habitual. El perill d'aquest curs no és passar-se de nivell i perdre el grup; és el contrari:

> Explicar-los teoria potent i no aterrar-la mai al codi.

Fins ara el professor els ha explicat conceptes i models a la pissarra sense que ho hagin tocat amb les mans. Impressiona, i s'esgota de seguida. **Una teoria que no baixa a una línia de NumPy no la poden fer servir per res.**

La conseqüència pràctica és un **bloc de matemàtiques de sis quaderns** (`Machine Learning/03_matematiques/`) on cada fórmula va seguida del codi que la calcula i cada implementació acaba comparant-se amb scikit-learn. No és material d'ampliació per als que van bé: **és el recorregut d'aquest grup**, i és el que justifica les 66 h. El detall didàctic és a [`didactica-matematica-ml.md`](didactica-matematica-ml.md).

## 1.5 Els riscos que veig

**El bloc de fonaments es pot menjar el curs.** NumPy i Pandas donen per moltes sessions si s'hi entra a fons. Aquí se'n fan **quatre i mitja**, les justes per poder treballar, i la resta s'aprèn fent servir les eines als blocs següents. Si al gener no s'ha arribat a RL, el concurs no existeix.

**Els fonaments arriben tard per a alguns.** Ja s'ha explicat ML supervisat conceptualment a la S04 i encara no poden tocar dades. Convé dir-ho explícitament a classe: «ara anem a buscar l'eina que us falta per fer allò que vau veure».

**Les matemàtiques han costat sis sessions d'algun altre lloc.** No és gratis i s'ha de dir. D'on surten, exactament: dels **exercicis de pràctica, que passen a ser feina de casa**, i del **bloc de xarxes neuronals, que baixa de quatre sessions a tres**. Els cinc quaderns de `02_practica/` estan fets per treballar-los sols —cel·les buides, comentaris guia i una línia de «com saps que ho has fet bé» amb el resultat esperat— i aquest grup els farà. Si resulta que no els fan, el trueque s'ha de desfer, i això es veurà a la Prova pràctica 1.

**R queda fora.** És a la llista d'eines de la fitxa i la Núria hi dedicava sis setmanes. Amb 4 h setmanals, el bloc de matemàtiques i el concurs al final, no hi cap. Es resol amb **lectura recomanada** a partir dels seus enllaços, i queda dit.

**El concurs necessita que tot el que hi ha abans funcioni.** És l'última cosa del curs i la primera que es perd si hi ha retards. Per això té cinc sessions reservades i el material ja existeix.

---

# Part 2 — Programació

## 2.1 Calendari real

33 sessions, del **14 de setembre de 2026** al **26 de gener de 2027**. Ja descomptats els festius que cauen en dilluns o dimarts (12 d'octubre i 8 de desembre) i les vacances de Nadal (del 22 de desembre al 7 de gener).

| Bloc | Sessions | Hores | Del | Al |
|---|---|---|---|---|
| 0 · Arrencada i Python | S01-S05 | 10 | 14 set | 28 set |
| **1 · Fonaments de dades i àlgebra** | **S06-S12** | **14** | **29 set** | **26 oct** |
| 2 · Supervisat i la matemàtica que hi ha a sota | S13-S21 | 18 | 27 oct | 24 nov |
| 3 · Optimització, dades reals i no supervisat | S22-S25 | 8 | 30 nov | 14 des |
| 4 · Xarxes neuronals | S26-S28 | 6 | 15 des | 11 gen |
| 5 · Reinforcement Learning i concurs | S29-S33 | 10 | 12 gen | 26 gen |

Els sis quaderns de matemàtiques **no són sessions afegides**: ocupen les sessions S08, S16, S19, S20, S22 i S24, que són la teoria del model corresponent portada fins al fons.

## 2.2 Sessió a sessió

### Bloc 0 — Arrencada i Python *(fet)*

| | Data | Contingut |
|---|---|---|
| S01 | dl 14 set | Presentació del mòdul |
| S02 | dt 15 set | Python: tipus, variables, cadenes |
| S03 | dl 21 set | Python: condicionals |
| S04 | dt 22 set | **Els models de ML supervisat, conceptualment, amb Iris** |
| S05 | dl 28 set | Primer contacte amb conjunts de dades |

### Bloc 1 — Fonaments de dades i àlgebra *(és on som)*

| | Data | Contingut | Material |
|---|---|---|---|
| S06 | dt 29 set | **NumPy 1**: per què no llistes, l'array, indexació i llesques | `01_fonaments/FO_01_numpy.ipynb` |
| S07 | dl 5 oct | **NumPy 2**: operacions, màscares booleanes, agregacions i eixos | el mateix |
| S08 | dt 6 oct | **Àlgebra lineal**: norma, producte escalar, projecció, i que un model entrenat és un vector i una multiplicació | `03_matematiques/MA_01_algebra_lineal.ipynb` |
| S09 | dt 13 oct | **Pandas 1**: Series i DataFrame, carregar CSV, seleccionar amb `loc` i `iloc` | `01_fonaments/FO_02_pandas.ipynb` |
| S10 | dl 19 oct | **Pandas 2**: nuls, `groupby`, gràfics ràpids, del DataFrame a `X` i `y` | el mateix |
| S11 | dt 20 oct | Diccionaris, funcions i comprensions, amb els quaderns de la Núria | `material-complet/Diccionaris.ipynb`, `Definicions.ipynb` |
| S12 | dl 26 oct | **Prova pràctica 1** i tancament del bloc | |

> El 12 d'octubre és festiu: aquella setmana només hi ha la sessió del dimarts.

El guió detallat d'aquestes sessions és a [`guions-bloc-1-fonaments.md`](guions-bloc-1-fonaments.md).

### Bloc 2 — Supervisat i la matemàtica que hi ha a sota

| | Data | Contingut | Material |
|---|---|---|---|
| S13 | dt 27 oct | Entrenament i test, i per què se separen. Primer model complet | `00_demo/ML_00_demo_iris.ipynb` |
| S14 | dl 2 nov | **k veïns** i la distància. El parany de les escales | `ML_01_knn.ipynb` · a casa: `EX_01_wine` |
| S15 | dt 3 nov | **Arbres de decisió**: la impuresa i la tria del tall | `ML_02_arbres.ipynb` + PDF de la Núria |
| S16 | dl 9 nov | **Entropia i informació**: per què Gini, el guany, i que la log-loss i l'entropia creuada són el mateix número | `MA_04_entropia_informacio.ipynb` |
| S17 | dt 10 nov | **Boscos aleatoris** i **mètriques**: la precisió no serveix tota sola | `ML_03_boscos.ipynb` · a casa: `EX_02_cancer` |
| S18 | dl 16 nov | **Regressió logística**: la frontera, la sigmoide, i els pesos per força bruta | `ML_04_regressio_logistica.ipynb` |
| S19 | dt 17 nov | **Descens de gradient**: què és una derivada, la derivada de la log-loss, i entrenar la logística amb un bucle propi | `MA_02_descens_gradient.ipynb` |
| S20 | dl 23 nov | **Probabilitat i versemblança**: Bayes, d'on surt la log-loss, i Naive Bayes implementat | `MA_03_probabilitat_versemblanca.ipynb` |
| S21 | dt 24 nov | **SVM**: el marge i el kernel. **Prova pràctica 2** | `ML_05_svm.ipynb` · a casa: `EX_04_fronteres` |

**La sessió clau del bloc és la S19.** És on es desfà la trampa de la força bruta de la S18 i on entenen, de veritat, com aprèn un model. Val la pena avisar-los a la S18 que allò que estan fent és provisional.

### Bloc 3 — Optimització, dades reals i no supervisat

| | Data | Contingut | Material |
|---|---|---|---|
| S22 | dl 30 nov | **Optimització amb restriccions**: Lagrange, per què l'SVM depèn de pocs punts, i el kernel demostrat | `MA_05_marge_optimitzacio.ipynb` |
| S23 | dt 1 des | **Dades brutes i pipelines**: nuls, categòriques, i la fuita d'informació | `EX_05_dades_brutes.ipynb` + `Pipeline.ipynb` de la Núria |
| S24 | dl 7 des | **PCA i vectors propis**: la maledicció de la dimensionalitat, i reduir dimensions sense inventar-se res | `MA_06_pca_vectors_propis.ipynb` |
| S25 | dl 14 des | **k-means** i **imatges com a taula**. **Prova pràctica 3** | `EX_03_digits.ipynb` · a casa: R, enllaços de la Núria |

> El 8 de desembre és festiu: aquella setmana només hi ha la sessió del dilluns.

### Bloc 4 — Xarxes neuronals

| | Data | Contingut | Material |
|---|---|---|---|
| S26 | dt 15 des | Què és una xarxa neuronal, i **que ja en saben el mecanisme**: és el descens de gradient de la S19 | `Deep Learning/01_teoria/DL_01`, `DL_02` |
| S27 | dl 21 des | PyTorch: tensors, arquitectures i entrenament | `DL_02`, `DL_03`, `DL_04` |
| S28 | dl 11 gen | **De la xarxa a l'agent**: el pont cap a RL | `DL_05_redes_para_RL` |

Aquest bloc va comprimit a posta. El pot anar de pressa perquè **la part difícil ja està feta**: qui ha entès la S19 ja té la retropropagació a mig camí.

### Bloc 5 — Reinforcement Learning i concurs

| | Data | Contingut | Material |
|---|---|---|---|
| S29 | dt 12 gen | Fonaments de RL: l'agent, l'entorn, la recompensa | `RL_01_fundamentos` |
| S30 | dl 18 gen | **DQN** i Gymnasium | `RL_02_dqn` |
| S31 | dt 19 gen | **Entrenament lliure**: cadascú entrena el seu agent | plantilla del concurs |
| S32 | dl 25 gen | Entrenament lliure i ajust. Lliurament dels agents | |
| S33 | dt 26 gen | **EL CONCURS** | `Reinforcement Learning/06_concurs/` |

## 2.3 Com s'avalua

Els instruments segueixen el que demana la fitxa, **a l'espera de confirmar els pesos**:

- **Proves pràctiques**, amb ordinador i semblants als exercicis de classe: una per bloc (S12, S21, S25) més el **projecte final de RL**, que és l'agent del concurs.
- **Activitats**: els exercicis dels quaderns, amb les cel·les buides. **Amb aquesta programació passen a ser feina de casa i deixen de ser opcionals**, perquè el temps de classe se'l menja la matemàtica. Es lliuren i es qualifiquen 0 o 10.
- **Proves escrites**: les que calguin segons quina versió de l'avaluació acabi valent.

**El bloc de matemàtiques no s'avalua com a deducció.** No es demana derivar el gradient de la log-loss en un examen. Sí que es demana implementar una funció de pèrdua i comprovar-la, verificar un gradient per diferències finites, o explicar per què un model dona el que dona mirant-ne els pesos. Hi ha la llista a [`didactica-matematica-ml.md`](didactica-matematica-ml.md).

**El concurs no es puntua per posició al marcador.** Es puntua l'agent lliurat, que funcioni, i la justificació de les decisions. Guanyar el concurs és el premi, no la nota: si no, els que tinguin portàtil potent tenen avantatge.

## 2.4 Què cal preparar, i quan

| Per a quan | Què |
|---|---|
| **Feta** | Els manuals de NumPy i Pandas, i els sis quaderns de matemàtiques |
| Desembre | La sessió de k-means (S25), que encara no té material propi |
| Gener | Tenir el concurs provat: script jutge i plantilla |
| **Quan es pugui** | **Confirmar els pesos de l'avaluació** i demanar a la Núria còpia de les seves presentacions de Google |

## 2.5 Els punts on la programació es pot trencar

Tres avisos, per ordre de probabilitat.

**La S19 pot demanar dues sessions.** És el quadern més dur del curs: derivades des de zero, gradient, i un bucle d'entrenament. Si es veu que no cabrà, el que se sacrifica és la S20 (probabilitat), que es pot deixar en lectura i exercicis de casa sense trencar res del que ve després.

**Si a la Prova pràctica 1 (S12) es veu que no han fet els exercicis de casa**, el trueque d'aquesta programació no funciona i cal recuperar temps de classe per a la pràctica. La manera menys dolenta de fer-ho és fondre S23 i S25 en una sola sessió.

**Si l'1 de desembre encara s'està al Bloc 2**, s'ha de saltar directament al Bloc 4 i deixar `MA_05` i `MA_06` com a material de consulta. El concurs no es toca.
