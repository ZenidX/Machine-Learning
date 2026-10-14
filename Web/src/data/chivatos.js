// Els xivatos de cada quadern: les eines que el quadern fa servir de debò, per ordre
// d'importància (les que el seu resultat et fa prendre una decisió), cadascuna amb el seu
// parany. Tret dels quaderns mateixos. Mai el resultat que l'alumne ha de descobrir.
// Format: { titol, intro, llista: [{ nom, text }], describe?, tancament }. Es pinten amb
// <Chivato f={...} /> de components/Bloc.jsx. Els de FO_00..FO_02 són a BlocDades.jsx.

// ---------------------------------------------------------------- Bloc 2 · supervisat

const ML_00 = {
  titol: "Les eines d'aquesta demo, per ordre d'importància",
  intro:
    "És una demo: no has d'escriure res. Però totes aquestes peces tornen a sortir a cada quadern del curs, i és bo reconèixer-les des del primer dia.",
  llista: [
    { nom: "train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)", text: "Separa les flors per ensenyar de les flors per examinar. Si examines el model amb les mateixes flors amb què l'has entrenat, no has mesurat res." },
    { nom: "model.fit(X_entrena, y_entrena)", text: "Entrenar és una línia. Sempre amb l'entrenament, mai amb l'examen." },
    { nom: "model.score(X_examen, y_examen)", text: "La precisió: quina fracció encerta. Sobre l'examen. Sobre l'entrenament només et diu com de bé ha memoritzat." },
    { nom: "DecisionTreeClassifier(max_depth=3)", text: "L'arbre que escriu sol els if/elif de la secció 3. max_depth limita quantes preguntes encadena; sense límit, creix fins a encertar totes les flors que ha vist." },
    { nom: "plot_tree(arbre, feature_names=..., class_names=..., filled=True)", text: "Et deixa llegir els condicionals que ha escrit la màquina i comparar-los amb els teus." },
    { nom: "for nom, model in models.items():", text: "Cinc models amb la mateixa interfície, fit i score. Per això un sol bucle els prova tots." },
    { nom: "ConfusionMatrixDisplay.from_estimator(model, X_examen, y_examen)", text: "No quantes s'equivoca, sinó quines confon amb quines. Les files són el que era; les columnes, el que ha dit." },
    { nom: 'dades.groupby("especie") + plt.scatter', text: "Un color per espècie. Mirar les dades abans de res és el que et diu si un tall a mà té sentit." },
  ],
  tancament: "fit per aprendre, score per examinar, i mai amb les mateixes files.",
};

const ML_01 = {
  titol: "Les eines del k-NN que fas servir, per ordre d'importància",
  intro:
    "train_test_split, fit i score continuen valent de ML_00. Aquestes són les que afegeix el k-NN.",
  llista: [
    { nom: "np.sqrt(np.sum((a - b) ** 2))", text: "La distància euclidiana: Pitàgores, amb 2 columnes o amb 4. Amb llistes de Python a - b peta; converteix-les abans amb np.array." },
    { nom: "np.argsort(dists)[:k]", text: "Les posicions dels k veïns més propers, no les seves distàncies. Amb aquestes posicions agafes les seves etiquetes." },
    { nom: "np.unique(veins, return_counts=True)", text: "El recompte de la votació. L'argmax dels comptes et dona la posició del guanyador dins de valors, no el nom." },
    { nom: "KNeighborsClassifier(n_neighbors=k)", text: "El mateix model fet per scikit-learn. n_neighbors és la k. Abans de fiar-te de cap dels dos, comprova que prediuen el mateix." },
    { nom: "(pred_ma == pred_sklearn).mean()", text: "La coincidència entre la teva funció i la de scikit-learn. Si no surt 1, el problema és a la teva funció." },
    { nom: "for k in range(1, 26): ... .score()", text: "La k no s'aprèn de les dades: la tries tu, provant-ne moltes i mirant l'examen." },
    { nom: "StandardScaler().fit_transform(X_entrena) / .transform(X_examen)", text: "El k-NN mesura distàncies: si una columna va en una escala molt més gran, decideix ella sola. fit només amb l'entrenament." },
    { nom: "abs(x1 - x2) + abs(y1 - y2)", text: "La distància de Manhattan, l'alternativa a l'euclidiana. Canviar la distància és canviar què vol dir «assemblar-se»." },
  ],
  tancament: "El k-NN no aprèn cap regla: guarda les dades i mesura distàncies. Per això l'escala de les columnes importa tant.",
};

const ML_02 = {
  titol: "Les fórmules dels arbres i la seva línia de codi, per ordre d'importància",
  intro:
    "Les de ML_00 i ML_01 continuen valent. Aquí l'arbre es desmunta: com mesura el desordre i com tria cada tall.",
  llista: [
    { nom: "1 - (proporcions ** 2).sum()", text: "La impuresa de Gini, amb proporcions = value_counts(normalize=True). Val 0 si el grup és pur, i puja com més barrejat està." },
    { nom: "gini_pare - gini_ponderat(esq, dre)", text: "El guany d'un tall. Cada fill pesa per la seva mida (len(fill) / n): sense ponderar, un fill petit i pur semblaria un tall excel·lent." },
    { nom: "(valors[:-1] + valors[1:]) / 2", text: "Els llindars candidats: punts mitjos entre valors consecutius que hi ha a les dades, amb np.sort(X[col].unique()). Provar-ne d'altres no canvia res." },
    { nom: "y[X[columna] <= llindar]", text: "Partir és una màscara booleana: el fill esquerre compleix la condició, el dret és la resta." },
    { nom: "arbre.tree_.feature[0], arbre.tree_.threshold[0]", text: "La columna i el llindar de l'arrel tal com els ha desat scikit-learn. feature és un índex: el nom és X.columns[...]." },
    { nom: "DecisionTreeClassifier(max_depth=1)", text: "Un arbre d'un sol tall: el que et serveix per comparar la teva millor_tall amb scikit-learn." },
    { nom: "for p in range(1, 11): ... .score() d'entrenament i d'examen", text: "Les dues corbes juntes. On se separen, l'arbre comença a memoritzar en comptes d'aprendre." },
    { nom: "-np.sum(p * np.log2(p))", text: "L'entropia, l'alternativa a Gini. Una p que val 0 fa log2(0): treu els zeros abans de calcular." },
    { nom: "np.argmax(precisio_examen)", text: "Et dona la posició dins de la llista, no el max_depth. Has de tornar a la llista de profunditats per saber quin és." },
  ],
  tancament: "Un arbre no és màgia: prova tots els talls possibles i es queda el que més baixa el desordre.",
};

const MA_04 = {
  titol: "Les fórmules i la seva línia de codi",
  intro:
    "Cada fórmula del quadern té la seva línia de NumPy i la funció de scikit-learn contra la qual es comprova. Aquestes són les que has de saber reconèixer.",
  llista: [
    { nom: "-np.log2(p)", text: "La sorpresa, en bits, d'un esdeveniment de probabilitat p. Un esdeveniment segur no informa de res." },
    { nom: "-np.sum(p * np.log2(p)), amb p = p[p > 0]", text: "L'entropia: la sorpresa mitjana. Els zeros es treuen abans, pel conveni 0·log 0 = 0; si no, surt nan." },
    { nom: "np.unique(y, return_counts=True)", text: "De les etiquetes a la distribució: comptes / comptes.sum(). És el que fa entropia_etiquetes." },
    { nom: "1 - np.sum(p ** 2)", text: "Gini, per comparar-la amb l'entropia. A scikit-learn és criterion=\"gini\" contra criterion=\"entropy\"." },
    { nom: "H(pare) - (n_esq/n)·H(esq) - (n_dre/n)·H(dre)", text: "El guany d'informació d'un tall. Es comprova contra DecisionTreeClassifier(criterion=\"entropy\", max_depth=1).tree_.threshold[0]; tree_.impurity[0] et deixa comprovar en quina base treballa." },
    { nom: "guany_multivia(col, y) / informacio_del_tall(col)", text: "La ràtio de guany. El guany sol premia les columnes amb molts valors diferents, i la ràtio el divideix per l'entropia de les mides dels fills." },
    { nom: "np.sum(p * np.log2(p / q))", text: "La divergència KL. No és una distància: kl(p, q) i kl(q, p) no són el mateix càlcul. H(p, q) = H(p) + KL(p‖q) es comprova amb np.isclose." },
    { nom: "-np.mean(y*np.log(p) + (1-y)*np.log(1-p))", text: "La log-loss, amb np.clip(p, eps, 1 - eps). Es comprova contra sklearn.metrics.log_loss. Va en nats (np.log); les funcions d'abans, en bits (np.log2): multiplica per np.log(2) per passar d'una a l'altra." },
    { nom: "mutual_info_classif(X, y, random_state=42)", text: "La informació mútua de cada columna amb l'etiqueta, en nats. Amb SelectKBest(puntua_mi, k=...) tries les k millors." },
  ],
  tancament: "Si la teva línia i la de scikit-learn no donen el mateix número, la fórmula no està ben escrita.",
};

const ML_03 = {
  titol: "Les eines del bosc aleatori que fas servir, per ordre d'importància",
  intro:
    "L'arbre de ML_02 continua valent: un bosc en són molts. Aquestes són les que afegeix aquest quadern.",
  llista: [
    { nom: "RandomForestClassifier(n_estimators=100, random_state=42)", text: "n_estimators és quants arbres vota. Sense random_state, cada execució fa un bosc diferent i no pots comparar res." },
    { nom: "rf.feature_importances_", text: "Un pes per columna, que sumen 1. Només existeix després del fit. Posa-li noms amb pd.Series(..., index=X.columns) i ordena-la." },
    { nom: "np.random.randint(0, n, size=n)", text: "El bootstrap: una mostra del mateix tamany amb reemplaçament. len(set(mostra)) et diu quantes files diferents hi han entrat de debò." },
    { nom: "np.random.rand(n_sim, n_votants) < p", text: "Simular vots independents: cada True és un encert. .sum(axis=1) > n / 2 et diu si ha guanyat la majoria." },
    { nom: "stats.mode(prediccions, axis=0)", text: "El vot de majoria, flor a flor (columna a columna). Treballa amb números: per això abans es fa pd.factorize de les etiquetes." },
    { nom: "make_classification(n_features=20, n_informative=5, ...)", text: "Fabricar un problema difícil, amb columnes de soroll, per veure els dos models fora d'Iris." },
    { nom: "time.time()", text: "El preu dels arbres: abans i després del fit, i res més dins del cronòmetre." },
    { nom: "int(np.sqrt(n_columnes))", text: "Quantes columnes veu cada tall per defecte. És l'altra font d'atzar del bosc, a més del bootstrap." },
  ],
  tancament: "Un bosc és molts arbres que han vist files i columnes diferents, i voten.",
};

const ML_04 = {
  titol: "Les eines de la regressió logística que fas servir, per ordre d'importància",
  intro:
    "train_test_split, fit i score continuen valent. La novetat és que el model ja no torna una classe, torna una probabilitat.",
  llista: [
    { nom: "1 / (1 + np.exp(-z))", text: "La sigmoide: converteix z = w1·x1 + w2·x2 + b en un número entre 0 i 1. A z = 0 dona 0,5, que és on es talla." },
    { nom: "model.coef_[0], model.intercept_[0]", text: "Els pesos i el biaix que ha après. coef_ és una matriu (una fila per classe): sense el [0] no tens els dos números." },
    { nom: "model.predict_proba(X)", text: "Una columna per classe, i cada fila suma 1. L'ordre de les columnes és el de model.classes_; mira'l abans de triar-ne una." },
    { nom: "-np.mean(y*np.log(p) + (1-y)*np.log(1-p))", text: "La pèrdua que minimitza el model. np.clip(p, eps, 1 - eps) abans del log: si una p val 0 o 1 exacte, surt infinit." },
    { nom: "x2 = -(w1 * x1 + b) / w2", text: "La frontera: on z val 0, aïllada per poder-la dibuixar amb plt.plot." },
    { nom: "np.meshgrid + plt.contourf", text: "La graella de pesos i el paisatge de la pèrdua. És força bruta: amb dos pesos encara es pot fer." },
    { nom: "LogisticRegression(C=...)", text: "C és el paràmetre de regularització. Per veure què fa, dibuixa les fronteres de diversos valors en un sol gràfic." },
    { nom: "LogisticRegression(max_iter=200)", text: "Amb tres classes i poques iteracions surt un ConvergenceWarning: no l'ignoris, puja max_iter." },
    { nom: '(bi["especie"] == "virginica").astype(int)', text: "Passar l'etiqueta a 0 i 1. Totes les fórmules del quadern suposen y en {0, 1}." },
  ],
  tancament: "La logística no et dona una classe: et dona una probabilitat, i la classe és només on talla el 0,5.",
};

const MA_02 = {
  titol: "Les fórmules i la seva línia de codi",
  intro:
    "El descens de gradient a mà, comprovat contra LogisticRegression. Cada línia d'aquesta llista surt al quadern i té la seva comprovació.",
  llista: [
    { nom: "(f(x + h) - f(x - h)) / (2 * h)", text: "La derivada numèrica centrada. Amb una h massa petita, l'arrodoniment de l'ordinador espatlla el resultat: hi ha una h bona, i no és la més petita." },
    { nom: "x = x - eta * derivada", text: "Un pas de descens. eta és la taxa d'aprenentatge, i és la que decideix si el mètode baixa, va lent o se'n va." },
    { nom: "X.T @ (p - y) / len(y)  i  np.mean(p - y)", text: "El gradient de la log-loss respecte de w i de b, amb p = sigmoide(X @ w + b). Són les dues línies que surten de la derivació del pas 6." },
    { nom: "sigmoide(z) * (1 - sigmoide(z))", text: "La derivada de la sigmoide. Es comprova contra la numèrica abans de fer-la servir." },
    { nom: "gradient_numeric(func, v, h=1e-6)", text: "El gradient checking: l'analític contra el numèric, component a component. Si difereixen més d'1e-7, no entrenis: la derivada està malament." },
    { nom: "np.clip(p, EPS, 1 - EPS)", text: "Dins de la log-loss. Sense el clip, una sigmoide que val 0 exacte fa log(0) i la pèrdua surt inf." },
    { nom: "w = w - eta * grad_w; b = b - eta * grad_b", text: "Entrenar és repetir el pas. Guarda la pèrdua de cada iteració i dibuixa-la: si no baixa, revisa eta abans que res." },
    { nom: "grad_w + 2 * lam * w", text: "La regularització: el terme nou del gradient. El biaix no es penalitza. lam = 1 / (2·C·n) és el que el fa equivalent a LogisticRegression(C=...)." },
    { nom: "np.unravel_index(np.argmin(L), L.shape)", text: "El millor punt d'una graella 2D: argmin et dona una posició plana i unravel_index la torna a fila i columna." },
  ],
  tancament: "Si el gradient numèric i l'analític no coincideixen, no entrenis: primer arregla la derivada.",
};

const MA_03 = {
  titol: "Les fórmules i la seva línia de codi",
  intro:
    "Probabilitat condicionada, Bayes i versemblança, cada una amb el recompte o la línia de NumPy que la calcula i la funció de scikit-learn o scipy que la comprova.",
  llista: [
    { nom: "(A & B).sum() / B.sum()", text: "P(A|B) són dos recomptes i una divisió, amb màscares booleanes. Es comprova contra la definició P(A i B) / P(B)." },
    { nom: "P_B_donat_A * P_A / P_B", text: "Bayes: gira la condició. Ha de donar el mateix que comptar files." },
    { nom: "sens * prev + (1 - espec) * (1 - prev)", text: "El denominador de Bayes: els dos camins cap a un positiu. Oblidar el dels sans és l'error que fa sortir una probabilitat absurda." },
    { nom: "p ** cares * (1 - p) ** creus", text: "La versemblança de la moneda sobre una graella de p; np.argmax et dona el millor p de la graella." },
    { nom: "cares * np.log(p) + creus * np.log(1 - p)", text: "La log-versemblança. El producte de molts factors petits arriba a 0.0 exacte a l'ordinador; la suma de logaritmes no, i el màxim no es mou." },
    { nom: "np.where(y == 1, p, 1 - p)", text: "La probabilitat que el model dona a l'etiqueta que era de debò. És el mateix que p ** y * (1 - p) ** (1 - y)." },
    { nom: "-np.mean(y*np.log(p) + (1-y)*np.log(1-p))", text: "La log-loss, amb np.clip. Es comprova contra sklearn.metrics.log_loss(y, p), amb p = predict_proba(X)[:, 1]." },
    { nom: "X[y == c].mean(axis=0), X[y == c].var(axis=0)", text: "Els paràmetres del Naive Bayes, per classe i per columna. Es comproven contra GaussianNB().theta_ i .var_." },
    { nom: "np.log(prior) + log_f.sum(axis=1)", text: "La puntuació de cada classe; argmax(axis=1) tria la guanyadora. Sumar logs en comptes de multiplicar densitats, pel mateix motiu d'abans." },
    { nom: "gnb.var_smoothing * X.var(axis=0).max()", text: "La correcció que scikit-learn suma a les variàncies. És el que explica que no coincideixis fins a l'últim decimal." },
  ],
  tancament: "Multiplicar probabilitats és la idea; sumar logaritmes és com es fa perquè l'ordinador no arrodoneixi a zero.",
};

const ML_05 = {
  titol: "Les eines de l'SVM que fas servir, per ordre d'importància",
  intro:
    "coef_, intercept_ i la recta de la frontera continuen valent de ML_04. Aquestes són les que afegeix l'SVM.",
  llista: [
    { nom: "np.abs(X @ w + b) / np.linalg.norm(w)", text: "La distància de cada punt a la recta. El marge d'una recta és la distància del punt més proper: d.min()." },
    { nom: 'SVC(kernel="linear", C=1e5)', text: "L'SVM lineal amb marge dur: C molt gran vol dir que no tolera cap punt dins del marge." },
    { nom: "model.support_vectors_ i model.support_", text: "Els vectors de suport (les mostres) i les seves posicions. Són els únics punts que decideixen la frontera." },
    { nom: "1 / np.linalg.norm(w)", text: "El marge que ha trobat l'SVM, a partir de w = model.coef_[0]." },
    { nom: 'SVC(kernel="rbf", C=..., gamma=...)', text: "El kernel, i els seus dos paràmetres. Mira sempre la precisió d'entrenament i la d'examen juntes: una sola no et diu si ha memoritzat." },
    { nom: "make_pipeline(StandardScaler(), SVC())", text: "L'SVM mesura distàncies, com el k-NN: escalar és obligatori. Dins d'un pipeline el fit de l'escalador no toca mai l'examen." },
    { nom: 'GridSearchCV(SVC(kernel="rbf"), graella, cv=5)', text: "Prova totes les combinacions de C i gamma amb validació creuada. .best_params_ diu la guanyadora; la precisió, mesura-la a l'examen." },
    { nom: "np.meshgrid + model.predict + contourf", text: "El mapa de la regió que el model assigna a cada classe. Només funciona amb dues columnes." },
    { nom: "make_circles(n_samples, noise, factor)", text: "Dades fabricades on cap recta serveix. noise és el soroll i factor, la mida del cercle de dins." },
  ],
  tancament: "Moltes rectes separen les dades; l'SVM tria la que deixa més espai, i la decideixen uns pocs punts.",
};

const EX_01 = {
  titol: "Les eines d'aquest exercici, per ordre d'importància",
  intro:
    "Les eines estan llistades al quadern, no encadenades: encaixar-les és la feina. Aquí tens per a què serveix cadascuna i on et pot fer caure.",
  llista: [
    { nom: "StandardScaler: .fit_transform(X_entrena) / .transform(X_examen)", text: "fit només amb l'entrenament. Després mira .mean_ i .scale_: et diuen què ha après l'escalador i de quines columnes." },
    { nom: ".score(X_examen, y_examen)", text: "Els cinc models tenen la mateixa interfície. Compara sempre sobre la mateixa partició, o la comparació no val." },
    { nom: "X_entrena.std(axis=0)", text: "La desviació de cada columna. Posa-li noms amb pd.Series(..., index=cols) i ordena-la amb .sort_values(ascending=False)." },
    { nom: "dades.describe()", text: "El min i el max de cada columna d'un cop d'ull. És la manera ràpida de veure escales incompatibles." },
    { nom: 'load_wine(as_frame=True)', text: "wine.frame porta les 13 columnes i també target: treu-la amb .drop(columns=...) abans de fer servir el frame com a X." },
    { nom: "train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)", text: "La mateixa partició per a tots els models i tots els exercicis." },
    { nom: "max_depth en un bucle + plt.plot amb label=", text: "Dues corbes, entrenament i examen, al mateix gràfic. El que llegeixes és el forat entre elles." },
    { nom: ".feature_importances_ + .plot(kind=\"barh\")", text: "Només els models d'arbre la tenen, i només després del fit. Un pes per columna, que sumen 1." },
    { nom: "DummyClassifier i confusion_matrix", text: "Per a les comprovacions dels exercicis 5 i 6. Un número sol no diu res fins que el compares amb el model que no mira les dades." },
  ],
  tancament: "Cap número d'aquest quadern val res sol: compara'l amb l'altre (sense escalar i escalat, entrenament i examen, el teu model i el Dummy).",
};

const EX_02 = {
  titol: "Les eines de mesurar d'aquest exercici, per ordre d'importància",
  intro:
    "La partició, l'escalador i els cinc models continuen valent d'EX_01. Les de mesurar no han sortit a la teoria: són totes a la caixa d'eines (EX_00).",
  llista: [
    { nom: "data.target_names", text: "L'única cosa que et diu quin número és malignant i quin benign. Mira-ho abans de triar cap pos_label." },
    { nom: "confusion_matrix(y_real, y_predit, labels=[0, 1])", text: "Files: el que era. Columnes: el que ha dit el model. Si gires els arguments no peta, però intercanvies falsos positius i falsos negatius." },
    { nom: "recall_score(..., pos_label=0)", text: "La sensibilitat: dels que eren de la classe que t'importa, quants n'ha trobat. Sense pos_label mesura la classe 1." },
    { nom: "precision_score(..., pos_label=0)", text: "Dels que el model ha dit que eren de la classe que t'importa, quants n'eren. La mateixa predicció té números diferents per a cada classe." },
    { nom: 'DummyClassifier(strategy="most_frequent")', text: "El model que no mira les dades. Amb la mateixa partició: si no el guanyes, no has fet res." },
    { nom: "classification_report(..., target_names=...)", text: "Precision, recall i F1 de cada classe en un text per llegir, no per calcular. La columna support et diu quants casos té cada classe." },
    { nom: "model.predict_proba(X) + model.classes_", text: "Una columna per classe, en l'ordre de classes_. Mira-ho abans de decidir quina columna és «maligne»." },
    { nom: "np.where(prob >= llindar, 0, 1)", text: "Prediccions amb un llindar que tries tu en comptes del 0,5 de .predict()." },
    { nom: "accuracy_score(y_real, y_predit)", text: "La precisió global: tots els encerts en un número. És la que amaga quins errors comet el model." },
  ],
  tancament: "En un diagnòstic, abans de preguntar quant encerta un model, pregunta quins errors comet.",
};

const EX_04 = {
  titol: "Les eines d'aquest exercici, per ordre d'importància",
  intro:
    "Els cinc models i el .score() de sempre. El que és nou és fabricar les dades i mirar la forma de la frontera, no només el número.",
  llista: [
    { nom: "Xm, ym = make_moons(n_samples=300, noise=0.2, random_state=42)", text: "make_blobs, make_moons, make_circles i make_classification tornen una tupla de dos arrays. Assignada a una sola variable, el .fit() peta." },
    { nom: "dibuixa_frontera(ax, model, X, y, titol)", text: "Ja la tens feta: pinta la regió de cada classe amb meshgrid, predict i contourf. Només va amb dues columnes." },
    { nom: "crea_models()", text: "Un joc nou de cinc models cada vegada. Si reaprofites un diccionari ja entrenat, sobreescrius els models d'un conjunt amb els d'un altre." },
    { nom: "plt.subplots(1, 5) i axs", text: "Una gràfica per model, una al costat de l'altra, per comparar formes." },
    { nom: "DecisionTreeClassifier(max_depth=...) + .get_n_leaves()", text: "max_depth és el que demanes; .get_depth() i .get_n_leaves() el que li ha sortit, i només després del fit." },
    { nom: "make_moons(noise=...)", text: "El soroll que barreja les dues classes. Canvia només aquest paràmetre i deixa la resta igual." },
    { nom: "pd.DataFrame(resultats_soroll).T", text: "La .T posa els nivells de soroll a les files i els models a les columnes." },
    { nom: ".score() d'entrenament i d'examen", text: "Les dues juntes: un 100 % a l'entrenament, sol, és un avís." },
    { nom: "apostes[conjunt][model]", text: "Escriu l'aposta abans de veure cap número. Si no, ja no és una aposta." },
  ],
  tancament: "Cada model dibuixa fronteres d'una forma: el que mires aquí és quina forma, no només quin número treu.",
};

const EX_00 = {
  titol: "Les eines de la caixa que més faràs servir en aquest bloc, per ordre d'importància",
  intro:
    "La caixa d'eines no resol cap exercici: explica cada eina amb taules de joguina i el parany que té. Aquestes són les del bloc 2.",
  llista: [
    { nom: ".fit_transform(X_entrena) / .transform(X_examen)", text: "El parany central del curs: fit només amb l'entrenament. Fer-ho amb tot no peta ni avisa, i et dona un número millor del que el model es mereix." },
    { nom: 'DummyClassifier(strategy="most_frequent")', text: "La referència honesta. La primera pregunta davant de qualsevol resultat: què treu el Dummy amb les mateixes dades?" },
    { nom: "train_test_split(..., stratify=y)", text: "Sense stratify, una classe amb pocs casos pot quedar tota a l'entrenament, i l'examen ja no examina res d'ella." },
    { nom: "confusion_matrix(y_real, y_predit)", text: "Files el real, columnes el predit. Primer sempre el real: amb l'ordre girat no peta, però llegeixes la matriu al revés." },
    { nom: "precision_score i recall_score(pos_label=...)", text: "Cada una mira un dels dos errors. La fórmula és el de menys: el que has de decidir és quin error no et pots permetre." },
    { nom: ".score() d'entrenament contra .score() d'examen", text: "El forat entre els dos és el que detecta el sobreajustament." },
    { nom: "classification_report(...)", text: "Tot de cop, per classe. Mira la columna support: t'avisa si la partició ha deixat una classe amb quatre casos." },
    { nom: "cross_val_score(model, X, y, cv=5)", text: "Cinc particions en comptes d'una. Amb el model sense entrenar; es reporta la mitjana, i la desviació diu com de fiable és." },
    { nom: "GridSearchCV(model, graella, cv=5)", text: "Prova totes les combinacions. Mira cv_results_ i no només best_params_: un empat també és un resultat. I multiplica entrenaments." },
    { nom: "meshgrid + predict + contourf", text: "La recepta de la frontera. És fontaneria: copia-la i fes-la servir. Només amb dues columnes." },
  ],
  tancament: "La caixa no et diu quin número t'ha de sortir: et diu com saber si el que has fet està bé.",
};

// ---------------------------------------------------------------- Bloc 3 · no supervisat

const MA_05 = {
  titol: "Les fórmules i la seva línia de codi",
  intro:
    "La distància i el marge de ML_05 continuen valent; aquí es dedueixen. Tret del problema dual, tot es comprova amb np.allclose contra un SVC entrenat.",
  llista: [
    { nom: "np.abs(X @ w + b) / np.linalg.norm(w)", text: "La distància a la recta, deduïda i comprovada per força bruta sobre 400.001 punts de la recta." },
    { nom: "w @ (p - q)", text: "Dóna 0 per a dos punts qualssevol de la recta: w és perpendicular a la frontera. D'aquí surt tota la fórmula de la distància." },
    { nom: "np.sign(X @ (c*w) + c*b)", text: "Multiplicar w i b per un mateix número no canvia ni la frontera ni les prediccions. Per això es pot exigir |w·x + b| = 1 al punt més proper, i el marge és 2 / ||w||." },
    { nom: "np.linalg.solve(A, b)", text: "El lagrangià convertit en un sistema lineal: dL/dx = 0, dL/dy = 0 i la restricció, en tres files." },
    { nom: 'minimize(f, x0, constraints=[{"type": "eq", "fun": ...}])', text: "El mateix problema resolt numèricament amb scipy. Mira res.success abans de fiar-te de res.x." },
    { nom: "np.abs(X[model.support_] @ w + b)", text: "Als vectors de suport ha de donar 1, i a la resta, més d'1. Compara amb np.allclose(..., 1, atol=1e-5): l'igual exacte no surt mai amb decimals." },
    { nom: "model.dual_coef_ @ model.support_vectors_", text: "Reconstrueix w a partir dels multiplicadors. dual_coef_ ja porta alpha·y amb el signe: no tornis a multiplicar per y." },
    { nom: "np.sum(A * B, axis=1) ** 2", text: "El kernel polinòmic (a·b)², que dona el mateix que phi(a)·phi(b) sense calcular mai phi." },
    { nom: "np.exp(-gamma * ((A[:, None, :] - B[None, :, :]) ** 2).sum(axis=-1))", text: "El kernel RBF, sense bucles. Es comprova contra sklearn.metrics.pairwise.rbf_kernel. gamma decideix a quina distància dos punts deixen de semblar-se." },
    { nom: "np.maximum(0, 1 - ym * (X @ w + b))", text: "Les xi del marge tou: el que li falta a cada punt per arribar a 1. Amb ym = 2*y - 1, perquè la fórmula vol etiquetes -1 i +1." },
  ],
  tancament: "Només el dual es pren sense derivar. Tota la resta la pots comprovar tu: si np.allclose dona False, la fórmula està mal escrita.",
};

const EX_00_brutes = {
  titol: "Les eines de les dades brutes, per ordre d'importància",
  intro:
    "El mateix quadern de referència del bloc 2, ara per les seccions 3 a 6. Cada eina hi és explicada amb una taula de joguina i el parany que té.",
  llista: [
    { nom: ".isna().sum()", text: "L'inventari del que falta, columna per columna. Sempre la primera línia davant d'unes dades que no coneixes." },
    { nom: ".duplicated().sum() i .drop_duplicates()", text: "duplicated no marca la primera aparició: el número són les files que sobren. Esborra'ls abans de partir; després, el mal ja està fet." },
    { nom: ".dropna()", text: "No modifica l'original i no avisa de quantes files s'emporta. Compta-les sempre després: pot ser la meitat de la taula." },
    { nom: 'SimpleImputer(strategy="median")', text: "Omple amb memòria: aprèn el valor amb fit i el desa a .statistics_. Torna un ndarray, no un DataFrame. most_frequent és l'única estratègia que va amb text." },
    { nom: 'OneHotEncoder(handle_unknown="ignore")', text: "Una columna per categoria. Vol dues dimensions, df[[\"col\"]]. Sense handle_unknown, una categoria nova a l'examen fa petar el transform." },
    { nom: "Pipeline([...])", text: "Fa impossible el fit sobre l'examen: tu ja no escrius els fit un per un. Parteix abans de construir-lo; el pipeline no sap quines files volies examinar." },
    { nom: 'ColumnTransformer([("num", ..., cols), ("cat", ..., ["col"])])', text: "Una transformació per a cada grup de columnes. Els prefixos num__ i cat__ de la sortida són els noms que li has posat." },
    { nom: "pd.get_dummies", text: "Per mirar, no per entrenar: no recorda res, i a l'examen et pot fer columnes diferents de les de l'entrenament." },
    { nom: "Badalona 1, Barcelona 2, Girona 3", text: "Codificar text amb números inventa un ordre que no existeix. Només és correcte si la categoria té ordre de debò (baix, mitjà, alt)." },
    { nom: 'df["col"].fillna(df["col"].mean())', text: "Per explorar, sí. Per a un model amb examen, no: aquesta mitjana ja coneix les files de l'examen." },
  ],
  tancament: "Diagnostica, treu duplicats, parteix, i només llavors imputa i codifica, dins d'un Pipeline.",
};

const MA_06 = {
  titol: "Les fórmules i la seva línia de codi",
  intro:
    "El PCA fet a mà en cinc passos i comprovat contra sklearn.decomposition.PCA. Cada línia té la seva comprovació al quadern.",
  llista: [
    { nom: "Xc = X - X.mean(axis=0)", text: "Centrar. Sense aquest pas, la matriu de covariància no és la de les dades." },
    { nom: "C = Xc.T @ Xc / n", text: "La matriu de covariància, en un sol producte. Es comprova contra np.cov(X.T, ddof=0): np.cov vol les variables per files, i per defecte divideix per n - 1." },
    { nom: "np.linalg.eigh(C)", text: "Valors i vectors propis d'una matriu simètrica. Els torna de menor a major, i els vectors per COLUMNA: ordena amb np.argsort(vaps)[::-1]." },
    { nom: "A @ v == lam * v", text: "La definició d'un vector propi: la matriu l'estira sense girar-lo. Es comprova amb np.allclose." },
    { nom: "v @ C @ v", text: "La variància de les dades projectades en la direcció v. És el que relaciona la força bruta per angles amb el primer valor propi." },
    { nom: "Z = Xc @ veps[:, :k]", text: "Projectar sobre les k primeres direccions: de d columnes a k." },
    { nom: "np.argmax(np.cumsum(vaps / vaps.sum()) >= 0.95) + 1", text: "Quantes components calen per a un llindar de variància. argmax sobre booleans et dona la primera posició True; el +1 la converteix en un nombre de components." },
    { nom: "PCA(n_components=2).fit_transform(X)", text: "La versió de scikit-learn: components_ va per FILES. Un vector pot sortir amb el signe girat, i no és un error. explained_variance_ divideix per n - 1." },
    { nom: "StandardScaler abans del PCA", text: "El PCA busca variància: sense escalar, la columna amb els números més grans s'emporta la primera component." },
    { nom: "pdist(P)", text: "Totes les distàncies entre parells de punts. min / max és com es mesura la maledicció de la dimensionalitat." },
    { nom: 'KernelPCA(n_components=2, kernel="rbf", gamma=...)', text: "Quan cap projecció lineal separa les dades, es canvia d'eina, no de paràmetres." },
  ],
  tancament: "El PCA és àlgebra: centrar, covariància i vectors propis. La resta és ordenar i projectar.",
};

const ML_06 = {
  titol: "Les eines de k-means que fas servir, per ordre d'importància",
  intro:
    "El broadcasting i les màscares de NumPy del bloc 1 són el que fa funcionar tot el quadern. Aquestes són les que afegeix k-means.",
  llista: [
    { nom: "((X[:, None, :] - M[None, :, :]) ** 2).sum(axis=2)", text: "La matriu (n, k) de distàncies al quadrat de cada punt a cada centre, sense cap bucle." },
    { nom: ".argmin(axis=1)", text: "Assignar: cada punt al centre més proper. Torna la posició del mínim de cada fila, que és el número del grup." },
    { nom: "X[etiquetes == j].mean(axis=0)", text: "Actualitzar: cada centre a la mitjana dels seus punts. axis=0, per columna." },
    { nom: "((X - M[etiquetes]) ** 2).sum()", text: "La inèrcia J. No puja mai d'un mig pas al següent: comprova-ho amb np.all(np.diff(historial) <= 1e-9)." },
    { nom: "KMeans(n_clusters=3, n_init=10, random_state=42)", text: ".fit(X) no rep y. Després: .labels_, .cluster_centers_, .inertia_. .transform(X) torna distàncies sense elevar al quadrat." },
    { nom: "n_init i k-means++", text: "Segons on comencen els centres, k-means pot acabar en un mínim local. n_init el repeteix diverses vegades i es queda el millor." },
    { nom: "silhouette_score(X, etiquetes)", text: "Per triar k. La inèrcia no serveix: sempre baixa quan k creix, fins a 0 amb un grup per punt." },
    { nom: "adjusted_rand_score(y, etiquetes) + pd.crosstab", text: "Per comparar amb unes etiquetes, si n'hi ha. El número del grup no vol dir res: renombrar els grups no canvia l'ARI." },
    { nom: "StandardScaler().fit_transform(X)", text: "k-means mesura distàncies: una columna que va per centenars decideix els grups ella sola." },
    { nom: "DBSCAN(eps=0.2)", text: "Quan els grups no són núvols rodons. k-means talla per la recta entre dos centres; DBSCAN segueix la densitat." },
  ],
  tancament: "k-means no sap què és cada grup: només sap quins punts són a prop. El nom el poses tu.",
};

const EX_05 = {
  titol: "Les eines d'aquest exercici, per ordre d'importància",
  intro:
    "Totes són a EX_00 (seccions 3 a 6), amb el seu parany. Aquí estan per importància, no en l'ordre en què les has de fer servir: l'ordre és la feina.",
  llista: [
    { nom: ".isna().sum(), .dtypes, .duplicated().sum()", text: "El diagnòstic. Cada desperfecte amb un número exacte, no «alguns nuls»." },
    { nom: 'pipe.named_steps["preprocessat"].named_transformers_["num"].statistics_', text: "Com arribes a l'imputador de dins del pipeline. És la comprovació de fuita: les medianes que hi ha desades et diuen amb quines files s'ha ajustat." },
    { nom: "np.allclose(a, b)", text: "Per comparar medianes amb decimals. L'== exacte et pot dir False per un arrodoniment." },
    { nom: 'SimpleImputer(strategy="mean" / "median")', text: "Torna un ndarray: els noms de les columnes es perden. Mira'n .statistics_." },
    { nom: ".dropna(subset=cols)", text: "Esborrar en comptes d'omplir. Compta les files que et queden: canvia també l'examen amb què mesures." },
    { nom: 'OneHotEncoder(handle_unknown="ignore")', text: "Vol vins_sd[[\"origen\"]], amb dobles claudàtors. .get_feature_names_out() i .categories_ et diuen quina columna és quina." },
    { nom: "ColumnTransformer + Pipeline", text: "Una branca per a les numèriques i una per a la de text, i el model al final. L'únic fit és pipe.fit(X_entrena, y_entrena)." },
    { nom: ".drop_duplicates().reset_index(drop=True)", text: "Després d'esborrar, l'índex queda amb forats; reset_index els tapa." },
    { nom: "try: ... except Exception as e:", text: "L'exercici 2 peta a posta. type(e).__name__ i el missatge et diuen quin desperfecte ha fet petar el fit." },
    { nom: "len(y_examen)", text: "Abans de comparar dues precisions, quantes files d'examen té cadascuna. Un punt de diferència pot ser una sola fila." },
  ],
  tancament: "Les dades brutes no sempre peten. Les que no peten són les que t'enganyen.",
};

const EX_03 = {
  titol: "Les eines d'aquest exercici, per ordre d'importància",
  intro:
    "Els cinc models, la partició i el Pipeline de sempre. El que és nou és que les columnes són píxels, i moure't entre imatge i taula.",
  llista: [
    { nom: "digits.data (1797, 64) i digits.images (1797, 8, 8)", text: "La mateixa informació amb dues formes. .reshape(-1) passa d'imatge a fila; .reshape(8, 8), de fila a imatge." },
    { nom: "make_pipeline(StandardScaler(), model)", text: "Per als models que treballen amb distàncies o coeficients. Si un d'aquests queda molt per sota, mira si porta l'escalador a dins." },
    { nom: "confusion_matrix(y_examen, prediccions)", text: "De 10×10. Els encerts són a la diagonal; el que busques és fora." },
    { nom: "m = matriu.copy(); np.fill_diagonal(m, 0)", text: "np.fill_diagonal no torna res: modifica l'array que li passes. Fes la còpia, guarda-la en una variable i omple aquella." },
    { nom: "np.unravel_index(m.argmax(), m.shape)", text: "argmax et dona la posició dins de la matriu aplanada; unravel_index la torna a (fila, columna), és a dir (real, predit)." },
    { nom: "np.where(prediccions != y_examen)[0]", text: "Les posicions dels errors. len() ha de quadrar amb la precisió de l'exercici 3." },
    { nom: "SelectKBest(f_classif, k=20)", text: ".fit_transform(X_entrena, y_entrena) i .transform(X_examen), que no es torna a ajustar. .get_support() són 64 booleans: .reshape(8, 8) te'ls ensenya a la imatge." },
    { nom: "time.time()", text: "Només al voltant del .fit(). Mesura-ho més d'una vegada abans de comparar." },
    { nom: "np.random.default_rng(42).choice(64, 20, replace=False)", text: "20 píxels a l'atzar: el que necessites per saber si la tria del SelectKBest aporta alguna cosa." },
    { nom: "rf.feature_importances_.reshape(8, 8)", text: "Les importàncies del bosc, posades on són a la imatge. np.argsort(...)[-20:] et dona les 20 més altes." },
  ],
  tancament: "Una imatge és una fila de 64 números. Tot el que ja saps de taules hi funciona igual.",
};

const EX_06 = {
  titol: "Les eines d'aquest exercici, per ordre d'importància",
  intro:
    "Les de ML_06 continuen valent (distàncies amb broadcasting, KMeans, silueta, ARI). Aquí no hi ha número per a les dades de veritat: hi ha comprovacions.",
  llista: [
    { nom: "KMeans(n_clusters=k, n_init=10, random_state=42)", text: "A tots els exercicis, llevat que l'enunciat digui una altra cosa. .fit(X) no rep la y." },
    { nom: ".inertia_ i silhouette_score per a cada k", text: "Les dues corbes juntes. La inèrcia no ha de pujar mai en créixer k; si puja, revisa el n_init." },
    { nom: "np.array_equal(km.labels_, km.transform(X).argmin(axis=1))", text: "La comprovació que cada punt és al centre més proper. Per als números amb decimals, np.allclose." },
    { nom: "StandardScaler().fit_transform(...)", text: "Comprova després mitjana ≈ 0 i desviació ≈ 1 a cada columna, amb axis=0." },
    { nom: "pd.crosstab(labels, target) i adjusted_rand_score", text: "La taula ha de sumar el total de files. L'ARI no canvia si renombres els grups amb una permutació." },
    { nom: "np.bincount(km.labels_)", text: "Quants punts té cada grup. La suma ha de ser el nombre de files." },
    { nom: "km.cluster_centers_[j].reshape(8, 8)", text: "Cada centre dels dígits és una imatge. Compara els valors amb tolerància (C.min() > -1e-9): un -1e-15 és arrodoniment." },
    { nom: "pca.transform(km.cluster_centers_)", text: "Per pintar els centres al mateix pla que les dades, amb el MATEIX PCA ja ajustat, no amb un de nou." },
    { nom: 'load_sample_image("china.jpg") / 255 + .reshape(-1, 3)', text: "Una foto és una taula de píxels per 3 colors. Entrena amb una mostra de 5000 i fes .predict de tots." },
    { nom: "np.sqrt(np.mean((a - b) ** 2))", text: "L'RMSE entre la foto original i la reconstruïda amb cluster_centers_[etiquetes]." },
  ],
  tancament: "La k que tries és la teva conclusió. Les comprovacions només et diuen que el procediment és correcte.",
};

// ---------------------------------------------------------------- Bloc 4 · xarxes i RL

const DL_00 = {
  titol: "L'única cosa que comprova aquest índex",
  intro:
    "És el mapa del bloc de xarxes, en castellà. Té una sola cel·la de codi, i serveix per saber si PyTorch hi és abans d'obrir res més.",
  llista: [
    { nom: "import torch; torch.__version__", text: "Si l'import peta, l'entorn no té PyTorch. Colab ja el porta; en local, el requirements.txt de la carpeta." },
    { nom: "torch.cuda.is_available()", text: "Dona False a Colab sense GPU i a la majoria de portàtils. No és un error: tot el codi del bloc funciona a CPU." },
    { nom: "torch.cuda.get_device_name(0)", text: "El nom de la GPU. Només té sentit si l'anterior ha donat True." },
  ],
  tancament: "Si aquestes tres línies funcionen, la resta del bloc arrencarà.",
};

const DL_01 = {
  titol: "Les eines i fórmules d'aquest quadern, per ordre d'importància",
  intro:
    "El quadern està en castellà. De PyTorch n'hi ha poc, però és el que farà servir tot el bloc. La retropropagació és el descens de gradient de MA_02 amb la regla de la cadena.",
  llista: [
    { nom: "loss.backward() i param.grad", text: "Autograd: PyTorch calcula totes les derivades de la pèrdua respecte de cada tensor amb requires_grad=True. El quadern les comprova contra les fetes a mà." },
    { nom: "nn.Linear(entrades, sortides)", text: "Una capa: torch.matmul(x, W.T) + b per dins. W té forma (sortides × entrades), i per això surt la .T." },
    { nom: "class MLP(nn.Module): __init__ + forward", text: "super().__init__() és obligatori. model(x) crida forward: mai el cridis directament." },
    { nom: "nn.Sequential(nn.Linear, nn.ReLU, ...)", text: "Capes encadenades. Sense activació entre elles, apilar capes lineals és el mateix que una sola capa lineal." },
    { nom: "nn.CrossEntropyLoss()(logits, y)", text: "Rep logits, no probabilitats: el softmax el fa ella. y són índexs de classe, no one-hot." },
    { nom: "F.softmax(logits, dim=1) i .argmax(dim=1)", text: "De logits a probabilitats que sumen 1 per fila, i de probabilitats a classe. dim=1 vol dir per fila." },
    { nom: "torch.sigmoid, torch.tanh, F.relu", text: "Les activacions. ReLU és la de les capes amagades; a la sortida d'un classificador no se'n posa cap." },
    { nom: "sum(p.numel() for p in model.parameters())", text: "Quants pesos té la xarxa. named_parameters() te'ls dona capa per capa, amb la forma." },
    { nom: "w += lr * error * x", text: "La regla del perceptró de 1958. Aprèn AND; XOR no el pot aprendre cap recta." },
    { nom: "nn.MSELoss, nn.L1Loss, nn.BCEWithLogitsLoss", text: "Les pèrdues de regressió i la de classificació binària. BCEWithLogitsLoss, com CrossEntropyLoss, vol logits." },
  ],
  tancament: "Retropropagar és el descens de gradient amb la regla de la cadena. PyTorch ho calcula; tu has de saber què calcula.",
};

const DL_02 = {
  titol: "Les eines de PyTorch que fas servir, per ordre d'importància",
  intro:
    "Les de DL_01 continuen valent (nn.Module, nn.Linear, CrossEntropyLoss, backward). Aquest quadern és la guia completa; aquestes són les que surten a cada entrenament.",
  llista: [
    { nom: "optimizer.zero_grad(); loss.backward(); optimizer.step()", text: "El cor de qualsevol entrenament. Sense zero_grad els gradients s'acumulen d'un lot al següent i el model aprèn malament sense cap error." },
    { nom: "model.train() / model.eval()", text: "Dropout i BatchNorm es comporten diferent a cada mode. Avaluar en mode train et dona números que canvien a cada execució." },
    { nom: "with torch.no_grad():", text: "Per avaluar, per fer inferència i per actualitzar pesos a mà. Fora d'un entrenament, no calcules gradients." },
    { nom: 'torch.device("cuda" if torch.cuda.is_available() else "cpu") + .to(DEVICE)', text: "El model i les dades al mateix dispositiu. Un a CPU i l'altre a GPU fa petar l'operació." },
    { nom: "DataLoader(dataset, batch_size=64, shuffle=True)", text: "Lots per entrenar. shuffle=True a l'entrenament; a validació i test, shuffle=False." },
    { nom: "optim.Adam(model.parameters(), lr=1e-3)", text: "L'optimitzador per defecte. També SGD amb momentum i AdamW. Un scheduler fa scheduler.step() un cop per època." },
    { nom: 'torch.save(model.state_dict(), "x.pt") / model.load_state_dict(torch.load(...))', text: "Desar només els pesos. Per carregar, primer crees la mateixa arquitectura; després, model.eval()." },
    { nom: ".flatten(), .view(), .unsqueeze(0), .permute()", text: "Canviar la forma. Les imatges van (lot, canals, alt, ample) a PyTorch; PIL i numpy les donen (alt, ample, canals)." },
    { nom: "loss.item() i tensor.detach()", text: "Treure el número d'un tensor. Acumular la loss com a tensor, sense .item(), arrossega tot el graf de càlcul." },
    { nom: "torch.manual_seed(42)", text: "Reproducibilitat: els pesos inicials són aleatoris." },
  ],
  tancament: "Tot entrenament de PyTorch és el mateix bucle de cinc línies. El que canvia és el model que hi poses.",
};

const DL_03 = {
  titol: "Les eines de les arquitectures, per ordre d'importància",
  intro:
    "El bucle d'entrenament de DL_02 continua valent: no canvia. El que canvia és el model, i la forma de les dades que hi entren.",
  llista: [
    { nom: "nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)", text: "La capa de les imatges. in_channels ha de coincidir amb la capa anterior: 3 per a una imatge RGB." },
    { nom: "(H + 2*padding - kernel_size) / stride + 1", text: "La mida de sortida d'una convolució. Amb kernel 3 i padding 1, la mida no canvia." },
    { nom: "nn.MaxPool2d(2, 2)", text: "Divideix l'alt i l'ample per 2." },
    { nom: "nn.Flatten() + nn.Linear(128 * 4 * 4, 256)", text: "La mida d'entrada de la Linear depèn de tot el que hi ha abans. Fes un forward amb torch.randn(...) per comprovar-la abans d'entrenar." },
    { nom: "nn.LSTM(..., batch_first=True)", text: "Per a seqüències. Torna output, (hidden, cell); output[:, -1, :] és l'últim pas. Sense batch_first, l'ordre de les dimensions és un altre." },
    { nom: "nn.Embedding(vocab_size, dim, padding_idx=0)", text: "De números de paraula a vectors. És la primera capa d'un model de text." },
    { nom: "nn.BatchNorm2d i nn.Dropout(0.5)", text: "Les dues que fan que model.train() i model.eval() es comportin diferent." },
    { nom: "encoder + decoder, nn.Sigmoid() a la sortida", text: "L'autoencoder: comprimeix i reconstrueix. En el VAE, mu + std * torch.randn_like(std)." },
    { nom: 'models.resnet18(weights="IMAGENET1K_V1")', text: "Transfer learning: param.requires_grad = False congela la xarxa, i es canvia només .fc per la capa de la teva tasca." },
  ],
  tancament: "Una CNN, una LSTM i un MLP s'entrenen igual. El que canvia és la forma de les dades que hi entren.",
};

const DL_04 = {
  titol: "Les eines de l'entrenament, per ordre d'importància",
  intro:
    "Les de DL_02 continuen valent (el bucle, train/eval, no_grad, state_dict). Aquest quadern afegeix el que fa que un entrenament llarg acabi bé.",
  llista: [
    { nom: "corbes de train_loss i val_loss juntes", text: "El diagnòstic: si la de validació puja mentre la d'entrenament baixa, el model memoritza." },
    { nom: "EarlyStopping(patience=...)", text: "Para quan la validació deixa de millorar i torna als millors pesos. Desa'ls amb copy.deepcopy(model.state_dict()): sense deepcopy guardes una referència que es continua modificant." },
    { nom: "torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)", text: "Retalla els gradients massa grans. Va després de backward() i abans de step()." },
    { nom: "optim.AdamW(params, lr=..., weight_decay=0.01)", text: "weight_decay és la regularització L2, posada a l'optimitzador." },
    { nom: "optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)", text: "La taxa d'aprenentatge que baixa durant l'entrenament. També StepLR, OneCycleLR i ReduceLROnPlateau, que rep la val_loss." },
    { nom: 'torch.save({"model_state_dict": ..., "optimizer_state_dict": ..., "epoch": ...})', text: "El checkpoint complet: el que necessites per continuar un entrenament, no només per fer servir el model." },
    { nom: "nn.Dropout i nn.BatchNorm1d", text: "Regularització dins del model. Per això model.eval() abans de validar." },
    { nom: "nn.CrossEntropyLoss(label_smoothing=0.1)", text: "Suavitza les etiquetes perquè el model no es torni massa segur." },
    { nom: "param.grad.isnan().any(), grad.abs() < 1e-7", text: "Revisar els gradients capa per capa: NaN o gradients que s'esvaeixen expliquen un entrenament que no avança." },
    { nom: "augmentació només a les transformacions d'entrenament", text: "Validació i test sense augmentació, o mesures una cosa diferent de la que el model veurà." },
  ],
  tancament: "Un entrenament llarg es controla mirant la validació, no l'entrenament.",
};

const DL_05 = {
  titol: "Les eines de les xarxes per a RL, per ordre d'importància",
  intro:
    "El bucle de PyTorch de DL_02 continua valent. Aquí la xarxa ja no classifica: estima Q(s, a) per a cada acció. És el pont cap als quaderns de RL.",
  llista: [
    { nom: "rewards + (1 - dones) * gamma * target_network(next_states).max(1)[0]", text: "El target del DQN, dins de torch.no_grad(). El (1 - dones) talla el futur quan l'episodi s'ha acabat." },
    { nom: "q_network(states).gather(1, actions.unsqueeze(1)).squeeze()", text: "La Q de l'acció que es va fer de debò, no de totes. gather vol les accions amb una dimensió més: d'aquí l'unsqueeze." },
    { nom: "if random.random() < epsilon: acció aleatòria", text: "L'epsilon-greedy. Si no, q_values.argmax().item() dins de no_grad." },
    { nom: "deque(maxlen=...) + random.sample(memory, batch_size)", text: "El replay buffer: entrenar amb experiències barrejades trenca la correlació entre passos seguits." },
    { nom: "target_network.load_state_dict(q_network.state_dict())", text: "La xarxa objectiu, una còpia que s'actualitza cada N episodis perquè el target no es mogui a cada pas." },
    { nom: "F.mse_loss(current_q, target_q) + clip_grad_norm_", text: "La pèrdua del DQN i el retall de gradients per estabilitat." },
    { nom: "epsilon = max(epsilon_min, epsilon * epsilon_decay)", text: "Un cop per episodi. Al principi explora molt; al final gairebé només explota." },
    { nom: "nn.Linear(..., n_actions) sense activació final", text: "Una sortida per acció. Els valors Q poden ser negatius: una ReLU a la sortida els tallaria." },
    { nom: "Double DQN: argmax amb q_network, gather amb target_network", text: "La xarxa principal tria l'acció i l'objectiu l'avalua. Redueix la sobreestimació dels valors Q." },
    { nom: "value + (advantage - advantage.mean(dim=1, keepdim=True))", text: "La Dueling DQN: separa quant val l'estat de quant val cada acció." },
  ],
  tancament: "DQN és el Q-learning de la taula amb una xarxa al lloc de la taula, i dos trucs perquè no es desestabilitzi.",
};

const DL_PR = {
  titol: "Les eines que et demana aquesta pràctica, per ordre d'importància",
  intro:
    "Reuneix DL_02 i DL_05 en exercicis amb verificacions. Aquí tens les eines, no les cel·les fetes: si la verificació passa, el procediment és correcte.",
  llista: [
    { nom: "optimizador.zero_grad(); loss.backward(); optimizador.step()", text: "El cicle d'entrenament de l'exercici 3.3. Sense zero_grad, els gradients s'acumulen." },
    { nom: "torch.FloatTensor(X) i torch.LongTensor(y)", text: "Les dades en float, les etiquetes en long. CrossEntropyLoss no accepta etiquetes float." },
    { nom: "scaler.fit_transform(X_train) / scaler.transform(X_test)", text: "Escalar abans de passar a tensors. fit només amb l'entrenament, com sempre." },
    { nom: "modelo.eval() + with torch.no_grad():", text: "Per avaluar al test. predicciones.max(1) torna (valors, índexs): la classe és el segon." },
    { nom: "current_q.gather(1, actions.unsqueeze(1)).squeeze()", text: "La Q de l'acció presa. És el mateix de DL_05." },
    { nom: "rewards + (1 - dones) * gamma * next_q", text: "El target, amb next_q de la xarxa objectiu i dins de no_grad." },
    { nom: "random.random() < self.epsilon", text: "L'epsilon-greedy de l'exercici 5.2. L'altra branca és l'argmax de la q_network." },
    { nom: "ReplayBuffer: push i sample", text: "Guardar cada transició i treure'n un lot a l'atzar. replay no entrena fins que el buffer té un lot sencer." },
    { nom: "x = torch.tensor(2.0, requires_grad=True); y.backward(); x.grad", text: "Autograd en una sola variable, per comprovar una derivada que pots fer a mà." },
    { nom: "agent.epsilon = 0", text: "Avaluar l'agent sense exploració. Si no, part de les accions són a l'atzar i no mesures el que ha après." },
  ],
  tancament: "Les verificacions et diuen si el procediment és correcte. Si l'agent guanya o no, és el que has de mirar tu.",
};

const RL_01 = {
  titol: "Les eines del RL tabular, per ordre d'importància",
  intro:
    "El quadern està en castellà i fa servir un GridWorld propi, sense Gymnasium. Tot el RL tabular cap en aquestes línies.",
  llista: [
    { nom: "Q[s][a] += alpha * (r + gamma * np.max(Q[s2]) - Q[s][a])", text: "La regla del Q-learning. Si l'episodi s'ha acabat, el target és només r: no hi ha futur." },
    { nom: "Q = defaultdict(lambda: np.zeros(n_acciones))", text: "La taula Q: un array de valors per estat, que es crea sol el primer cop que hi passes." },
    { nom: "random.random() < epsilon ? random.randint(...) : np.argmax(Q[s])", text: "L'epsilon-greedy: explorar o explotar. Sense explorar, l'agent repeteix el primer camí que li ha funcionat." },
    { nom: "estado = env.reset(); nuevo_estado, recompensa, terminado = env.step(accion)", text: "El bucle agent-entorn. Aquest GridWorld torna tres valors; Gymnasium (RL_02) en torna cinc." },
    { nom: "G += (gamma ** i) * r", text: "El retorn descomptat. gamma < 1 fa que una recompensa llunyana valgui menys que una d'immediata." },
    { nom: "epsilon = max(0.01, epsilon * 0.995)", text: "Reduir l'exploració episodi a episodi, sense baixar mai d'un mínim." },
    { nom: "G = gamma * G + recompensa_t", text: "Monte Carlo: el retorn calculat cap enrere des del final de l'episodi; V(s) és la mitjana dels retorns de cada estat." },
    { nom: "Q(s,a) += α[r + γ·Q(s',a') − Q(s,a)]", text: "SARSA: com Q-learning, però amb l'acció que farà de debò en comptes de la millor. Per això és on-policy." },
    { nom: "np.argmax(Q[s]) per a cada casella", text: "La política apresa, dibuixada com una fletxa per casella." },
  ],
  tancament: "Q-learning és una sola línia. Tota la resta és el bucle que li porta experiència.",
};

const RL_02 = {
  titol: "Les eines del DQN i de Gymnasium, per ordre d'importància",
  intro:
    "Les de DL_05 continuen valent (replay buffer, xarxa objectiu, gather, epsilon-greedy). Aquest quadern les porta a Gymnasium.",
  llista: [
    { nom: "obs, reward, terminated, truncated, info = env.step(accio)", text: "Gymnasium torna cinc valors. terminated: l'episodi s'ha acabat de debò; truncated: s'ha tallat per temps. L'episodi acaba amb qualsevol dels dos." },
    { nom: "obs, info = env.reset(seed=42)", text: "reset també torna dues coses. La llavor, al reset." },
    { nom: 'gym.make("CartPole-v1")', text: "Crear l'entorn. LunarLander necessita a més gymnasium[box2d]." },
    { nom: "env.observation_space.shape i env.action_space.n", text: "La mida d'entrada i de sortida de la xarxa Q. Mira-les abans de construir-la." },
    { nom: "env.action_space.sample()", text: "Una acció a l'atzar: l'agent de referència contra el qual compares el teu." },
    { nom: "q_siguientes * (1 - terminados)", text: "Sense futur quan l'episodi ha acabat. És la mateixa línia del target de DL_05." },
    { nom: "env.close()", text: "Tanca l'entorn, sobretot si l'has obert amb render_mode=\"human\", que obre finestra." },
    { nom: "4 variables contínues × bins", text: "Per què la taula Q no escala: discretitzar cada variable multiplica els estats. D'aquí la xarxa." },
  ],
  tancament: "Gymnasium sempre és reset, step i close. Si canvies d'entorn, el teu bucle no canvia.",
};

const RL_03 = {
  titol: "Les eines de Stable-Baselines3, per ordre d'importància",
  intro:
    "Per a qui vulgui anar més enllà del DQN fet a mà. L'algorisme ja està fet; Gymnasium de RL_02 continua valent.",
  llista: [
    { nom: 'PPO("MlpPolicy", env, verbose=1)', text: "Crear l'agent: l'algorisme, la xarxa i l'entorn (o el seu nom)." },
    { nom: "model.learn(total_timesteps=20_000)", text: "Entrenar. Són passos d'interacció, no episodis." },
    { nom: "evaluate_policy(model, env, n_eval_episodes=10)", text: "Torna mitjana i desviació de la recompensa. Avalua en un entorn nou, no en el d'entrenament." },
    { nom: "action, _ = model.predict(obs, deterministic=True)", text: "Torna una tupla. deterministic=True per avaluar sense atzar." },
    { nom: 'model.save("ppo_cartpole") / PPO.load("ppo_cartpole", env=...)', text: "Desa un .zip. Per continuar entrenant, cal passar-li l'entorn en carregar." },
    { nom: 'make_vec_env("CartPole-v1", n_envs=4)', text: "Entorns en paral·lel: més experiència per segon." },
    { nom: "EvalCallback i CheckpointCallback", text: "Avaluar i desar durant l'entrenament, amb model.learn(..., callback=...)." },
    { nom: 'SAC("MlpPolicy", "Pendulum-v1")', text: "Per a accions contínues. El DQN només funciona amb accions discretes." },
    { nom: "policy_kwargs=dict(net_arch=[128, 128, 64])", text: "Canviar la mida de la xarxa sense escriure-la." },
    { nom: "learning_rate, gamma, n_steps, batch_size, clip_range, ent_coef", text: "Els hiperparàmetres de PPO. ent_coef premia l'exploració." },
  ],
  tancament: "Amb SB3 l'algorisme ja està fet. La teva feina és triar-lo bé i saber llegir si ha après.",
};

const CONCURS = {
  titol: "Les eines de la plantilla del concurs, per ordre d'importància",
  intro:
    "El CarAgent és el DQN de DL_05 ja fet (replay buffer i xarxa objectiu). La teva feina és entrenar-lo i desar-lo bé. El reglament és al README.md de la carpeta.",
  llista: [
    { nom: 'torch.save(agent.q_network.state_dict(), CONCURS_DIR / "agent.pth")', text: "Només l'state_dict, no l'agent sencer, i amb el nom fix agent.pth a 06_concurs/. Amb un altre nom o lloc, el jutge no el troba." },
    { nom: "rg.CarAgent(agent_id=0, state_size=6, n_actions=9)", text: "No canviïs la forma de la xarxa (6 entrades, 128, 128, 9 sortides): el jutge carrega exactament aquesta arquitectura." },
    { nom: "jutge.avaluar_agent(str(RUTA_SORTIDA))", text: "El mateix jutge que farà servir el professor. Un error de càrrega vol dir que has tocat l'arquitectura o que el fitxer no s'ha desat bé." },
    { nom: "entrena(agent, episodis, max_passos=2000, render=False)", text: "render=False per a l'entrenament llarg, i obligatori a Colab. Pots tornar-la a cridar: l'agent continua des d'on era." },
    { nom: "agent.remember(...) + agent.replay()", text: "A cada pas: guardar la transició i entrenar amb un lot del buffer." },
    { nom: "agent.decay_epsilon() + agent.update_target()", text: "Un cop per episodi, i l'objectiu cada actualitza_cada episodis." },
    { nom: "seguents, recompenses, dones, all_done = joc.step([accio])", text: "El joc és per a diversos cotxes: tot són llistes, i el teu és el [0]." },
    { nom: "historial_fitness", text: "La fitness de cada episodi, que és la distància recorreguda. Compara'n la mitjana amb la de l'agent aleatori." },
    { nom: "agent.gamma, agent.epsilon_decay, agent.epsilon_min", text: "Els hiperparàmetres que pots retocar si vols experimentar. Canvia'n un cada vegada." },
  ],
  tancament: "Al concurs només viatja l'state_dict. Si el jutge el carrega i el cotxe arriba lluny, ja està.",
};

export const chivatos = {
  ML_00, ML_01, ML_02, MA_04, ML_03, ML_04, MA_02, MA_03, ML_05,
  EX_01, EX_02, EX_04, EX_00,
  MA_05, EX_00_brutes, MA_06, ML_06, EX_05, EX_03, EX_06,
  DL_00, DL_01, DL_02, DL_03, DL_04, DL_05, DL_PR,
  RL_01, RL_02, RL_03, CONCURS,
};
