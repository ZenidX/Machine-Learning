# Guions del bloc 2 — Supervisat i la matemàtica que hi ha a sota

Nou sessions, del 27 d'octubre al 24 de novembre. Un guió per sessió, per obrir i tirar.

Material a `Machine Learning/00_demo/`, `01_teoria/` i `03_matematiques/`. Els exercicis de
`02_practica/` **van a casa**, amb `EX_00_caixa_eines.ipynb` com a referència al costat.

> **Regla d'aquest bloc, i val per a tot el curs:** els números que un exercici vol que
> descobreixin **no es diuen a classe**. El que sí que se'ls dona és la manera de comprovar-se:
> si el procediment és correcte, no quin resultat els ha de sortir. Hi ha el raonament a
> [`didactica-matematica-ml.md`](didactica-matematica-ml.md), secció «Com es dissenya un exercici».

Que vagin a casa és el trueque que fa possible la programació: el temps de classe se'l menja la
matemàtica. Convé recordar-ho cada sessió.

## L'estructura del bloc, en una frase

Tres models es veuen i es fan servir (S14, S15, S17), i després **es tornen a obrir per sota**
(S16, S19, S20, i el marge a la S22 del bloc següent). No és repetir: és que la segona passada
respon la pregunta que la primera deixa oberta.

**La frase que obre el bloc**, a la S13:

> A la S04 us vaig explicar aquests models a la pissarra i us els vaig fer creure. Durant
> aquestes nou sessions no us n'heu de creure cap: els escriurem i comprovarem que la
> llibreria fa exactament el mateix que nosaltres.

---

## S13 · dimarts 27 d'octubre · Entrenament i test

**Quadern:** `00_demo/ML_00_demo_iris.ipynb`

**Objectiu:** que quedi clar per què les dades es parteixen, i tenir un model complet corrent.

| Temps | Què |
|---|---|
| 20 min | Repàs del que van fer a la S04, ara amb les dades a les mans i no a la pissarra. |
| 25 min | **Per què es parteix el conjunt.** No ho expliquis abans de fer-ho: entrena un arbre sense límit de profunditat, ensenya que encerta el 100 % de l'entrenament, i després mesura-ho contra dades que no ha vist. El número que cau és l'argument. |
| 20 min | `train_test_split`, què fa `random_state` i per què cal fixar-lo. |
| 30 min | Els cinc models, entrenats i comparats sobre Iris. **No entris en cap.** Aquí només és la fotografia de grup. |
| 25 min | **El moment de la demo:** el classificador manual d'`if`/`elif` fa 96,0 % i l'arbre 97,8 %, i el llindar que l'arbre tria tot sol, 2,45, és el que ells van triar a ull. Recupera-ho. |

**L'error conceptual a matar aquí:** precisió d'entrenament contra precisió d'examen. Tornarà a
sortir tot el curs, però es guanya o es perd avui.

---

## S14 · dilluns 2 de novembre · k veïns més propers

**Quadern:** `01_teoria/ML_01_knn.ipynb` · **A casa:** `02_practica/EX_01_wine.ipynb`

**Objectiu:** el primer model implementat a mà i verificat contra scikit-learn.

| Temps | Què |
|---|---|
| 15 min | El problema: classificar mirant a qui t'assembles. Sense fórmula encara. |
| 20 min | La distància en 4 dimensions. **Ja la tenen de la S08**: és la norma de la diferència. Que la recuperin ells. |
| 35 min | **Implementar el k-NN sencer a mà**: distàncies a tots els punts, ordenar, agafar els k primers, votar. És la primera vegada que escriuen un model. |
| 20 min | **La comparació amb `KNeighborsClassifier`.** Ha de donar el mateix. Aquest és el minut que canvia la seva relació amb la llibreria: atura't aquí. |
| 15 min | Per què k importa, amb la corba de precisió segons k. |
| 15 min | **El parany de les escales.** Canvia les unitats d'una columna i mira caure la precisió. |

**Feina de casa, explicada aquí i no per correu:** `EX_01_wine`, i abans la caixa d'eines
`EX_00_caixa_eines`, que és la referència que han de tenir oberta al costat.

**No els diguis quant puja la precisió en escalar.** És la troballa de l'exercici i han de
descobrir-la ells. El que sí que els has de dir és **com es comproven**: si el conjunt escalat
no té mitjana ≈ 0 i desviació ≈ 1 a cada columna, l'escalat no s'ha aplicat i la comparació no
val res. Amb això tenen criteri per saber si ho han fet bé sense saber el resultat.

---

## S15 · dimarts 3 de novembre · Arbres de decisió

**Quadern:** `01_teoria/ML_02_arbres.ipynb` + el PDF d'arbres de la Núria

**Objectiu:** entendre com una màquina tria un `if`.

| Temps | Què |
|---|---|
| 15 min | La connexió amb Python: un arbre és un `if` encadenat que algú ha escrit per tu. |
| 25 min | **La impuresa de Gini.** Calcula-la a mà sobre grups petits, a la pissarra, abans del codi. |
| 30 min | **Com es tria el tall**: recórrer tots els punts de tall possibles, mesurar la impuresa de les dues meitats, quedar-se el millor. Implementat amb NumPy, amb la corba del guany dibuixada. |
| 20 min | Que el tall que surt és 2,45, el mateix de la S13 i de la S04. |
| 20 min | **El sobreajust**, amb la corba de precisió segons `max_depth`. És el lloc del curs on es veu més net. |
| 10 min | Avís: demà s'obre aquesta fórmula per sota. |

---

## S16 · dilluns 9 de novembre · Entropia i informació

**Quadern:** `03_matematiques/MA_04_entropia_informacio.ipynb`

**Objectiu:** que el Gini deixi de ser una fórmula arbitrària, i tancar una equivalència que
no s'esperen.

Aquesta és la primera de les sessions de matemàtiques del bloc. **El to importa**: no és
ampliació ni és per a qui va bé. És la resposta a «i d'on surt aquesta fórmula».

| Temps | Què |
|---|---|
| 20 min | Informació com a sorpresa, i per què $-\log_2 p$. Que la sorpresa d'una cosa segura sigui zero no és un conveni: és el que obliga la propietat de sumar-se. |
| 25 min | **L'entropia en bits, amb el bit volent dir alguna cosa.** Una moneda justa és exactament 1 bit; un dau de 8 cares, 3. Lliga-ho amb quantes preguntes de sí o no calen per endevinar el resultat. |
| 20 min | **Entropia contra Gini, dibuixades juntes.** Mateixa forma, mateixos zeros, mateix màxim. Per això donen arbres gairebé iguals, i es comprova entrenant-ne dos. |
| 25 min | El guany d'informació, i el tall que surt coincidint amb el de `DecisionTreeClassifier`. |
| 20 min | **La trampa de la columna d'identificadors.** Afegeix una columna 0..149 a Iris i mira com el guany d'informació la tria per sobre dels pètals. Un model perfecte i inútil. Això és fuita d'informació, i tornarà a la S23. |
| 10 min | **El tancament:** que la log-loss i l'entropia creuada són el mateix número. Encara no saben què és la log-loss; deixa-ho plantat, es cull a la S19 i la S20. |

---

## S17 · dimarts 10 de novembre · Boscos i mètriques

**Quadern:** `01_teoria/ML_03_boscos.ipynb` + PDF de boscos de la Núria · **A casa:** `EX_02_cancer.ipynb`

**Objectiu:** per què votar funciona, i per què la precisió tota sola no serveix.

| Temps | Què |
|---|---|
| 25 min | Per què votar funciona, i **la condició que ho fa funcionar**: que els errors siguin diferents. Si tots s'equivoquen igual, votar no arregla res. |
| 20 min | Com es fan diferents: bootstrap i atzar a les columnes. |
| 20 min | Construir un bosc a mà, amb uns pocs arbres. |
| 15 min | **El cas incòmode d'Iris**, on el bosc perd contra l'arbre sol. Ensenya els dos casos junts, amb el segon exemple de `make_classification` on el bosc guanya clarament. **No amaguis el resultat que no convé.** |
| 30 min | **Mètriques**: matriu de confusió, precisió i exhaustivitat, **sobre un exemple petit de deu mostres que es puguin comptar a mà** (el de la caixa d'eines serveix). Ensenya com es llegeix la matriu, què és un fals negatiu i per què en un diagnòstic mèdic és l'error que no et pots permetre. **Aquí ensenyes la maquinària, no el resultat del càncer**: el cop de descobrir què hi ha darrere d'una precisió alta és l'exercici d'aquesta nit, i si el destapes avui te'l quedes sense. |
| 10 min | Lligam amb la S16: el desequilibri de classes es pot mesurar amb l'entropia de l'etiqueta. |

---

## S18 · dilluns 16 de novembre · Regressió logística

**Quadern:** `01_teoria/ML_04_regressio_logistica.ipynb`

**Objectiu:** la frontera i la probabilitat. I deixar una trampa a la vista.

| Temps | Què |
|---|---|
| 20 min | Una manera diferent de decidir: en lloc de mirar veïns o encadenar condicions, traçar una frontera. |
| 20 min | De la recta a la probabilitat. El problema del signe, i la sigmoide com a solució. **Ja saben què és `X @ w + b`** de la S08: aquí només se li posa la sigmoide a sobre. |
| 25 min | Calcular la probabilitat a mà per a tres flors concretes, i comparar-la amb `predict_proba`. |
| 30 min | **L'entrenament per força bruta**: una graella de pesos, calcular la pèrdua de cada combinació, quedar-se la millor. Dibuixa el paisatge amb corbes de nivell i marca on cau la solució de scikit-learn. |
| 15 min | **Digues en veu alta que això és una trampa.** No ho dissimulis: així no s'entrena cap model de veritat, i demà es fa bé. Que se'n vagin amb la pregunta oberta. |

**La pregunta que et faran i que no has de respondre del tot:** «i com ho fa scikit-learn?».
Resposta: «baixant per aquest paisatge. Demà veurem com se sap cap a on baixar».

---

## S19 · dimarts 17 de novembre · Descens de gradient

**Quadern:** `03_matematiques/MA_02_descens_gradient.ipynb`

**Objectiu:** que entenguin com aprèn un model. **És la sessió més important del curs.**

| Temps | Què |
|---|---|
| 10 min | **Per què la força bruta no serveix.** El càlcul, executat en directe: amb 2 pesos són 10.000 combinacions; amb 4, cent milions; amb els 30 del dataset de càncer, un número que no cap enlloc. Deixa que el número incomodi. |
| 25 min | **Què és una derivada, des de zero.** El pendent d'una recta, i després el pendent d'una corba en un punt. Calculat numèricament amb una `h` petita, i comprovant que per $x^2$ dona $2x$. La lectura útil: **la derivada diu cap a on moure's per baixar.** |
| 20 min | El descens de gradient en una dimensió, amb la trajectòria dibuixada. Els tres casos de la taxa d'aprenentatge: bé, massa gran (divergeix) i massa petita (no arriba). |
| 15 min | El gradient com a vector de derivades parcials, sobre les corbes de nivell. Que es vegi que baixa perpendicular a les corbes. |
| 20 min | **Per què la log-loss i no el nombre d'errors.** El nombre d'errors és un esglaó: derivada zero a tot arreu, no diu cap a on anar. Les dues corbes dibuixades juntes. |
| 15 min | La derivada de la log-loss, i el fet que surti $\frac{1}{n}X^\top(p-y)$. Una línia de codi. |
| 15 min | **La comprovació del gradient** contra el gradient numèric. Té nom, *gradient checking*, i és com es verifica un gradient de veritat. |

**Dues coses que segurament no hi cabran, i què fer:** l'entrenament complet amb el bucle i la
comparació amb scikit-learn són al quadern i es poden deixar per a casa. El que **no** es pot
deixar per a casa és la derivada i la comprovació numèrica.

**Si veus que la sessió no arriba**, hi ha el pla B a la secció 2.5 de
[`diagnostic-i-programacio-2627.md`](diagnostic-i-programacio-2627.md): es reparteix en dues
sessions i el que se sacrifica és la S20.

**El tancament que val la pena dir:** això mateix és el que entrena les xarxes neuronals que
veureu al desembre. La part difícil ja està feta.

---

## S20 · dilluns 23 de novembre · Probabilitat i versemblança

**Quadern:** `03_matematiques/MA_03_probabilitat_versemblanca.ipynb`

**Objectiu:** que la log-loss deixi de ser una fórmula caiguda del cel.

| Temps | Què |
|---|---|
| 15 min | Probabilitat condicionada comptant files amb màscares. Que vegin que és una divisió de dos recomptes, no una definició abstracta. |
| 25 min | **Bayes, i el resultat que els sorprendrà**: una prova amb 99 % d'encert sobre una malaltia d'1 entre 1.000 dona, davant d'un positiu, menys d'un 10 % de probabilitat de malaltia. Calculat en directe. Lliga-ho amb la S17: és el mateix problema del desequilibri de classes, vist des de la probabilitat. |
| 20 min | **Versemblança amb una moneda.** Han sortit 7 cares de 10; quina $p$ ho fa més versemblant? Primer la graella i la corba, després la derivada, i que les dues donin 0,7. |
| 15 min | **Per què el logaritme**, amb la demostració que convenç: el producte de 2.000 probabilitats de 0,5 dona exactament `0.0` en coma flotant, i la suma de logaritmes encara dona un número utilitzable. |
| 20 min | **De la versemblança a la log-loss.** Aquí es tanca el que es va plantar a la S16 i es va fer servir a la S19: la log-loss és la versemblança amb un logaritme i un signe menys. Comprovat contra `sklearn.metrics.log_loss`. |
| 25 min | **Naive Bayes implementat de zero**, que és un model sencer que surt directament de Bayes. On és «naive»: suposa columnes independents, i a Iris no ho són. Comparat amb `GaussianNB`. |

**Un detall que val la pena ensenyar:** la diferència amb scikit-learn no és aleatòria, és el
`var_smoothing`. Al quadern es localitza i es tanca fins a $10^{-13}$. La lliçó no és el
paràmetre: és que una diferència petita té una causa i es pot trobar.

---

## S21 · dimarts 24 de novembre · SVM i prova pràctica 2

**Quadern:** `01_teoria/ML_05_svm.ipynb` · **A casa:** `EX_04_fronteres.ipynb`

| Temps | Què |
|---|---|
| 15 min | Tres rectes, totes perfectes. Quina és millor, i per què la pregunta té resposta. |
| 20 min | El marge amb la distància punt-recta. Calcular el marge de tres rectes i veure quina guanya. |
| 15 min | Els vectors de suport: que el model només depèn d'uns pocs punts. **Deixa-ho com a fet estrany**, que a la S22 es demostra que no és casualitat. |
| 15 min | El kernel a nivell intuïtiu, i per què l'escalat aquí és obligatori. |
| 55 min | **Prova pràctica 2.** Format: cel·les buides sobre un dataset que no hagin vist. Entrenar dos models i comparar-los amb la mètrica adequada; implementar una funció de pèrdua i comprovar-la contra la de scikit-learn; explicar, mirant els pesos, per què un model prediu el que prediu. |

**La taula final del quadern de l'SVM** compara els cinc models: com decideix cadascun, què el
trenca i què demana de les dades. És la resposta a «per què cinc models si tots fan el mateix»,
i és bon material de repàs.

---

## Com saber si el bloc ha anat bé

Al final d'aquestes nou sessions, un alumne hauria de poder, **sense ajuda**:

- Partir un conjunt de dades, entrenar un model i dir si el resultat és bo, amb la mètrica adequada.
- **Implementar una funció de pèrdua** i comprovar-la contra la de scikit-learn.
- **Explicar què vol dir una derivada** en el context d'entrenar un model, i verificar un gradient.
- Dir d'on surt la log-loss, i per què no es minimitza el nombre d'errors.
- Mirar un model lineal entrenat i explicar per què prediu el que prediu.

Les dues primeres són el mínim. Les tres últimes són el que fa que aquesta optativa valgui la
pena per a aquest grup, i són bones preguntes d'examen pràctic.

**El senyal d'alarma:** si a la S19 la sala es queda muda, el problema no és la derivada, és que
els falta l'àlgebra de la S08. Es recupera en mitja sessió i val la pena aturar-se.
