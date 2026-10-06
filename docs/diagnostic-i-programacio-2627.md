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

**Les classes van començar el dilluns 21 de setembre**, no el 14. S'han fet **3 sessions de les 33** i avui es fa la quarta:

| | Data | Què s'hi va fer |
|---|---|---|
| S01 | dl 21 set | Presentació del mòdul i bases de Python, amb una mica de pràctica i els primers enunciats d'exercicis |
| S02 | dt 22 set | **Les dues hores senceres explorant els models de machine learning**, perquè es quedessin amb les formes del comportament de cadascun. El quadern d'Iris ho ensenya molt bé |
| S03 | dl 28 set | Pràctica de Python amb una mica de teoria dels models, i llançar-los contra els exercicis |
| **S04** | **dt 29 set** | **Avui.** Objectes de Python i primera anàlisi de dades |

### Què va passar el 28, que és el que ordena la sessió d'avui

Es van llançar contra els exercicis i **van quedar encallats**, per dues raons que convé tenir separades:

1. **Els faltava el manual per gestionar dades.** No sabien que `dades.data` existeix, ni que `df.shape` va sense parèntesis, ni que un model entrenat guarda el que ha après en atributs acabats en guió baix. I sobretot **no sabien com esbrinar-ho**: que a un objecte de Python se li pot preguntar què té a dins.
2. **Van pensar que les solucions eren dins del mateix enunciat.** I tenien raó: hi eren. Les línies de «com saps que ho has fet bé» donaven el resultat que havien de descobrir. Això ja està arreglat, i el criteri és a la secció «Com es dissenya un exercici» de [`didactica-matematica-ml.md`](didactica-matematica-ml.md).

**El diagnòstic, en una frase:** tenen la intuïció dels models i tenen Python bàsic, però **els falta la peça del mig**. Saben què fa un arbre de decisió i saben escriure un `if`, i no saben manejar una taula de dades.

**Per això el curs continua per aquí**, i no per més models. I per això la sessió d'avui comença pels objectes: sense saber interrogar-los, cada exercici és una endevinalla.

### La correcció de criteri que surt d'això

Als enunciats s'havia decidit a posta **no dir quines funcions encadenar**, perquè compondre-les era la feina. Amb el que va passar el 28, això queda corregit, i en paraules d'en Xavi: *«no hay que adivinar las funciones a usar; hay que ejecutarlas y ver cómo se llega a resultados usando lo que toca cuando toque»*.

| | Qui ho dona |
|---|---|
| **Quina eina fer servir** | **L'enunciat.** El nom del mètode hi va escrit. Endevinar l'API no ensenya res, només frustra |
| **Quin resultat surt** | **L'alumne.** Això és l'anàlisi, i és la seva feina |

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

**33 sessions de 2 h, del dilluns 21 de setembre de 2026 al dimarts 2 de febrer de 2027.** Ja descomptats els festius que cauen en dia de classe (12 d'octubre i 8 de desembre) i les vacances de Nadal, del 22 de desembre al 7 de gener.

> **Avís sobre la data de final, que cal confirmar.** Si el mòdul són 66 h de veritat, amb 4 h setmanals des del 21 de setembre **el curs arriba al 2 de febrer**. Si en canvi ha d'acabar el gener, hi caben **31 sessions, o sigui 62 h**, i falten 4 h: llavors el concurs es fa el 26 de gener i se'n perden dues sessions pel camí. Val la pena saber-ho abans de prometre res a l'alumnat.

| Bloc | Sessions | Hores | Del | Al |
|---|---|---|---|---|
| 0 · Arrencada i Python | S01-S03 | 6 | 21 set | 28 set |
| **1 · Fonaments de dades** | **S04-S11** | **16** | **29 set** | **27 oct** |
| 2 · Supervisat i la matemàtica que hi ha a sota | S12-S21 | 20 | 2 nov | 1 des |
| 3 · Optimització, dades reals i no supervisat | S22-S25 | 8 | 7 des | 21 des |
| 4 · Xarxes neuronals | S26-S28 | 6 | 11 gen | 18 gen |
| 5 · Reinforcement Learning i concurs | S29-S33 | 10 | 19 gen | 2 feb |

Els sis quaderns de matemàtiques **no són sessions afegides**: ocupen les sessions S09, S15, S18, S19, S20 i S22, que són la teoria del model corresponent portada fins al fons.

## 2.2 Sessió a sessió

### Bloc 0 — Arrencada i Python *(fet)*

| | Data | Contingut |
|---|---|---|
| S01 | dl 21 set | Presentació del mòdul i bases de Python |
| S02 | dt 22 set | **Els models de ML, explorats les dues hores**, amb el quadern d'Iris |
| S03 | dl 28 set | Pràctica de Python i primer contacte amb els exercicis |

### Bloc 1 — Fonaments de dades *(és on som)*

| | Data | Contingut | Material |
|---|---|---|---|
| **S04** | **dt 29 set** | **Objectes de Python i primera anàlisi de dades**: interrogar un objecte, atribut contra mètode, i una exploració guiada de principi a fi | `01_fonaments/FO_00_objectes_i_autocompletar.ipynb` |
| S05 | dl 5 oct | **NumPy 1**: per què no llistes, l'array, indexació i llesques | `FO_01_numpy.ipynb` |
| S06 | dt 6 oct | **NumPy 2**: operacions, màscares booleanes, agregacions i eixos | el mateix |
| S07 | dt 13 oct | **Pandas 1**: DataFrame i Series, carregar un CSV, `.loc` i `.iloc` | `FO_02_pandas.ipynb` |
| S08 | dl 19 oct | **Pandas 2**: nuls, `.groupby()`, gràfics, del DataFrame a `X` i `y` | el mateix |
| S09 | dt 20 oct | **Àlgebra lineal**: norma, producte escalar, projecció, i que un model entrenat és un vector i una multiplicació | `03_matematiques/MA_01_algebra_lineal.ipynb` |
| S10 | dl 26 oct | Diccionaris, funcions i comprensions, amb els quaderns de la Núria | `material-complet/Diccionaris.ipynb`, `Definicions.ipynb` |
| S11 | dt 27 oct | **Prova pràctica 1** i tancament del bloc | |

> El 12 d'octubre és festiu: aquella setmana només hi ha la sessió del dimarts.

El guió detallat és a [`guions-bloc-1-fonaments.md`](guions-bloc-1-fonaments.md).

### Bloc 2 — Supervisat i la matemàtica que hi ha a sota

| | Data | Contingut | Material |
|---|---|---|---|
| S12 | dl 2 nov | Entrenament i test, i per què se separen. Primer model complet | `00_demo/ML_00_demo_iris.ipynb` |
| S13 | dt 3 nov | **k veïns** i la distància. El parany de les escales | `ML_01_knn.ipynb` · a casa: `EX_01_wine` |
| S14 | dl 9 nov | **Arbres de decisió**: la impuresa i la tria del tall | `ML_02_arbres.ipynb` + PDF de la Núria |
| S15 | dt 10 nov | **Entropia i informació**: per què Gini, el guany, i que la log-loss i l'entropia creuada són el mateix número | `MA_04_entropia_informacio.ipynb` |
| S16 | dl 16 nov | **Boscos aleatoris** i **mètriques**: la precisió no serveix tota sola | `ML_03_boscos.ipynb` · a casa: `EX_02_cancer` |
| S17 | dt 17 nov | **Regressió logística**: la frontera, la sigmoide, i els pesos per força bruta | `ML_04_regressio_logistica.ipynb` |
| S18 | dl 23 nov | **Descens de gradient 1**: què és una derivada, des de zero, i la derivada de la log-loss | `MA_02_descens_gradient.ipynb` |
| S19 | dt 24 nov | **Descens de gradient 2**: la comprovació del gradient, l'entrenament amb bucle propi i la comparació amb scikit-learn | el mateix |
| S20 | dl 30 nov | **Probabilitat i versemblança**: Bayes, d'on surt la log-loss, i Naive Bayes implementat | `MA_03_probabilitat_versemblanca.ipynb` |
| S21 | dt 1 des | **SVM**: el marge i el kernel. **Prova pràctica 2** | `ML_05_svm.ipynb` · a casa: `EX_04_fronteres` |

**El descens de gradient té dues sessions**, i és deliberat: és el quadern més dur del curs i el que sosté tot el bloc de xarxes. Si es fa en una, es perd.

### Bloc 3 — Optimització, dades reals i no supervisat

| | Data | Contingut | Material |
|---|---|---|---|
| S22 | dl 7 des | **Optimització amb restriccions**: Lagrange, per què l'SVM depèn de pocs punts, i el kernel demostrat | `MA_05_marge_optimitzacio.ipynb` |
| S23 | dl 14 des | **Dades brutes i pipelines**: nuls, categòriques, i la fuita d'informació | `EX_05_dades_brutes.ipynb` + `Pipeline.ipynb` de la Núria |
| S24 | dt 15 des | **PCA i vectors propis**: la maledicció de la dimensionalitat, i reduir dimensions sense inventar-se res | `MA_06_pca_vectors_propis.ipynb` |
| S25 | dl 21 des | **k-means** i **imatges com a taula**. **Prova pràctica 3** | `EX_03_digits.ipynb` · a casa: R, enllaços de la Núria |

> El 8 de desembre és festiu: aquella setmana només hi ha la sessió del dilluns.

### Bloc 4 — Xarxes neuronals

| | Data | Contingut | Material |
|---|---|---|---|
| S26 | dl 11 gen | Què és una xarxa neuronal, i **que ja en saben el mecanisme**: és el descens de gradient de les S18 i S19 | `Deep Learning/01_teoria/DL_01`, `DL_02` |
| S27 | dt 12 gen | PyTorch: tensors, `autograd`, arquitectures i entrenament | `DL_02`, `DL_03`, `DL_04` |
| S28 | dl 18 gen | **De la xarxa a l'agent**: el pont cap a RL | `DL_05_redes_para_RL` |

### Bloc 5 — Reinforcement Learning i concurs

| | Data | Contingut | Material |
|---|---|---|---|
| S29 | dt 19 gen | Fonaments de RL: l'agent, l'entorn, la recompensa | `RL_01_fundamentos` |
| S30 | dl 25 gen | **DQN** i Gymnasium | `RL_02_dqn` |
| S31 | dt 26 gen | **Entrenament lliure**: cadascú entrena el seu agent | plantilla del concurs |
| S32 | dl 1 feb | Entrenament lliure i ajust. Lliurament dels agents | |
| S33 | dt 2 feb | **EL CONCURS** | `Reinforcement Learning/06_concurs/` |

## 2.3 Com s'avalua

**El detall sencer és a [`avaluacio-2627.md`](avaluacio-2627.md).** Aquí, el resum.

La fitxa fixa un **únic resultat d'aprenentatge** —«Crea aplicacions fent ús de models
d'aprenentatge automàtic»— i una fórmula sense ambigüitat: **10 % cinc proves escrites, 10 %
vint-i-cinc activitats, 80 % quatre proves pràctiques**, amb mínim de 5 a les pràctiques i
superior a 3 a les escrites per poder ponderar.

**La idea que ordena el calendari d'avaluació:** cada prova no pregunta què han après, pregunta
**si tenen el que els cal per al que ve**. El curs acaba amb un agent de RL competint, i cada
prova és un graó d'aquesta escala.

| | Quan | Pregunta que respon |
|---|---|---|
| **Pp1** | S11 · 27 oct | Pots manejar dades? *(porta del bloc 2)* |
| **Pp2** | S21 · 1 des | Pots entrenar, mesurar i verificar? *(porta de les xarxes)* |
| **Pp3** | S25 · 21 des | Pots treballar sense enganyar-te? |
| **Pp4** | S33 · 2 feb | L'agent, i la seva defensa |

Les cinc escrites (Pe1 a Pe5) cauen a les sessions **S08, S14, S20, S28 i S31**, sempre just
abans d'un salt. Valen un 2 % cadascuna: la seva funció no és qualificar, és **detectar qui es
despenja mentre encara s'hi pot fer alguna cosa**. La **Pe4 del 18 de gener** és la més important
de les cinc, perquè tapa les sis setmanes entre la Pp3 i el concurs, que són el material més dur
del curs i no tenien cap punt de control.

Les **25 activitats** són un quadern lliurat cadascuna, qualificades 0 o 10. Compte: **fora de
termini compten com a negatives**, no com a no lliurades.

**El bloc de matemàtiques no s'avalua com a deducció.** No es demana derivar el gradient de la
log-loss. Sí que es demana implementar una funció de pèrdua i comprovar-la, verificar un gradient
per diferències finites, o explicar per què un model dona el que dona mirant-ne els pesos.

**El concurs no es puntua per posició al marcador**, i la Pp4 és la **defensa a classe** de
l'agent, no l'entrenament: això resol alhora el problema de les màquines desiguals i el xoc amb
la clàusula d'ús d'IA de la fitxa.

## 2.4 Què cal preparar, i quan

| Per a quan | Què |
|---|---|
| **Feta** | El manual d'objectes de Python, els de NumPy i Pandas, la caixa d'eines i els sis quaderns de matemàtiques |
| Desembre | La sessió de k-means (S25), que encara no té material propi |
| Gener | Tenir el concurs provat: script jutge i plantilla |
| **Quan es pugui** | **Confirmar els pesos de l'avaluació** i demanar a la Núria còpia de les seves presentacions de Google |

## 2.5 Els punts on la programació es pot trencar

Quatre avisos, per ordre de probabilitat.

**La data de final no està confirmada.** Amb 66 h des del 21 de setembre, el curs acaba el **2 de febrer**. Si ha d'acabar el gener, hi caben 31 sessions i falten 4 h. En aquest cas el concurs es fa el **26 de gener** i el que se sacrifica són la S32 i la S33 d'entrenament lliure: es passa de dues sessions de taller a una, i el lliurament es tanca a la S30. **Això s'ha de saber abans d'anunciar el concurs a l'alumnat.**

**Si a la Prova pràctica 1 (S11) es veu que no han fet els exercicis de casa**, el trueque d'aquesta programació no funciona i cal recuperar temps de classe per a la pràctica. La manera menys dolenta de fer-ho és fondre S23 i S25 en una sola sessió.

**El descens de gradient ja té dues sessions (S18 i S19)**, que és el marge que abans no hi havia. Si tot i així no arriba, el que se sacrifica és la S20 (probabilitat), que es pot deixar en lectura i exercicis de casa sense trencar res del que ve després.

**Si a l'1 de desembre encara s'està al Bloc 2**, s'ha de saltar directament al Bloc 4 i deixar `MA_05` i `MA_06` com a material de consulta. El concurs no es toca: és el que sosté la motivació del grup i l'única cosa del curs que no es pot recuperar més endavant.
