// Els objectes del curs, amb els seus atributs i mètodes.
// Font: el final de FO_00 («Els cinc objectes del curs»), i l'inici de FO_01 i FO_02.

export const objectes = [
  {
    nom: "Bunch",
    on: "el que et torna load_wine(), load_digits(), load_iris()",
    que: "No són les dades: és la capsa que les porta a dins, amb les etiquetes, els noms de les columnes i la descripció.",
    atributs: [
      [".data", "les dades: array 2D, files = mostres, columnes = característiques"],
      [".target", "la resposta correcta de cada fila: array 1D de números"],
      [".feature_names", "els noms de les columnes de .data"],
      [".target_names", "a què correspon cada número de .target"],
      [".DESCR", "la descripció del dataset, en text (llarga: talla-la)"],
      [".frame", "tot el dataset en un DataFrame, només si has demanat as_frame=True"],
      [".images", "només a load_digits: les mateixes dades en forma d'imatge 8x8"],
    ],
    metodes: [[".keys()", "què porta a dins (un Bunch també és un diccionari)"]],
  },
  {
    nom: "ndarray",
    on: "l'array de NumPy, el que hi ha dins de .data",
    que: "Files = mostres, columnes = característiques. És el que fan servir els models per entrenar.",
    atributs: [
      [".shape", "la forma: (files, columnes)"],
      [".dtype", "el tipus de dada que guarda: float64, int64..."],
      [".ndim", "quantes dimensions té: 1 = fila, 2 = taula"],
      [".size", "quants números hi ha en total"],
      [".T", "el mateix array transposat"],
    ],
    metodes: [
      [".mean()  .std()", "mitjana, desviació típica (amb axis: vegeu a sota)"],
      [".min()  .max()  .sum()", "mínim, màxim, suma"],
      [".argmin()  .argmax()", "la posició del mínim i del màxim, no el valor"],
      [".argsort()", "les posicions que ordenarien l'array"],
      [".reshape()", "canvia la forma sense canviar els números"],
      [".copy()", "una còpia independent (una llesca no ho és)"],
      [".astype()", "el mateix array amb un altre tipus de dada"],
      [".round()", "arrodonit a tants decimals"],
    ],
    nota: "axis diu quin eix desapareix. .mean() sense res: un sol número. .mean(axis=0): un número per columna (el que voldràs el 90 % de les vegades). .mean(axis=1): un número per fila.",
  },
  {
    nom: "DataFrame",
    on: "la taula de pandas: pd.read_csv(), o un Bunch amb as_frame=True",
    que: "Un array amb noms a les columnes i moltíssims mètodes d'anàlisi. És el que fas servir per mirar les dades.",
    atributs: [
      [".shape", "(files, columnes)"],
      [".columns", "els noms de les columnes"],
      [".index", "les etiquetes de les files"],
      [".dtypes", "el tipus de cada columna, una per una"],
      [".values", "les dades com a array de NumPy, sense els noms"],
      [".loc[ ]", "selecció per etiqueta: df.loc[3, \"nota\"]"],
      [".iloc[ ]", "selecció per posició: df.iloc[0, 1]"],
    ],
    metodes: [
      [".head()  .tail()", "les primeres / les últimes files"],
      [".info()", "resum: columnes, tipus, quants valors no nuls, memòria"],
      [".describe()", "estadístiques de cada columna numèrica"],
      [".isna()", "on falten valors (True/False a cada casella); amb .sum(), quants per columna"],
      [".dropna()  .fillna()", "treure les files amb buits / omplir-los"],
      [".duplicated()  .drop_duplicates()", "trobar / treure files repetides"],
      [".groupby()", "agrupar per una columna per calcular per grup (.mean(), .agg([...]))"],
      [".sort_values()", "ordenar per una columna (ascending=False, de més a menys)"],
      [".value_counts()", "comptar quantes vegades surt cada combinació"],
      [".drop()", "treure columnes o files"],
      [".plot()", "un gràfic ràpid"],
      [".copy()", "una còpia independent"],
    ],
    nota: "df[\"col\"] dona una Series; df[[\"a\", \"b\"]], un DataFrame. Per filtrar: df[(cond1) & (cond2)], amb parèntesis, i mai and/or.",
  },
  {
    nom: "Series",
    on: "una columna d'un DataFrame (o una fila: df.loc[i])",
    que: "No és un DataFrame: té els seus propis mètodes. Té els atributs que ja coneixes.",
    atributs: [
      [".shape  .dtype  .values", "com a la resta"],
      [".index", "les etiquetes (si és una fila, els noms de les columnes)"],
      [".name", "el nom de la columna"],
    ],
    metodes: [
      [".value_counts()", "quantes vegades surt cada valor, de més a menys"],
      [".unique()  .nunique()", "quins valors diferents hi ha / quants"],
      [".map()", "aplica una funció o un diccionari a cada valor"],
      [".apply()", "aplica una funció pròpia a cada valor"],
      [".astype()", "canvia el tipus de dada"],
      [".mean()  .std()  .min()  .max()  .sum()", "com a NumPy"],
      [".idxmax()  .idxmin()", "l'índex de la fila del màxim i del mínim"],
    ],
  },
  {
    nom: "Model de scikit-learn",
    on: "KNeighborsClassifier(), DecisionTreeClassifier(), LogisticRegression()...",
    que: "Tots els models tenen la mateixa interfície. El que acaba en guió baix només existeix després de .fit().",
    atributs: [
      [".coef_", "el que ha après: el pes de cada característica (models lineals)"],
      [".feature_importances_", "quant compta cada columna (models d'arbre)"],
      [".classes_", "quines classes ha vist"],
      [".n_features_in_", "quantes columnes esperava"],
      [".feature_names_in_", "com es deien, si li has passat un DataFrame"],
      [".n_iter_", "quantes voltes li ha calgut per aprendre"],
    ],
    metodes: [
      [".fit(X, y)", "entrena: aprèn dels exemples"],
      [".predict(X)", "prediu la classe (o el valor) de mostres noves"],
      [".predict_proba(X)", "la probabilitat de cada classe"],
      [".score(X, y)", "quina proporció encerta (R² si és de regressió)"],
      [".get_params()", "amb quins ajustos l'has creat"],
    ],
  },
];

export const errorsTipics = [
  ["TypeError: 'tuple' object is not callable", "has posat parèntesis a un atribut (df.shape())"],
  ["a la sortida surt method o bound method", "t'has deixat els parèntesis d'un mètode (df.head)"],
  ["AttributeError: coef_ o NotFittedError", "no has cridat .fit()"],
  ["ValueError: The truth value of a Series is ambiguous", "has fet servir and/or en lloc de & / |, o t'has deixat els parèntesis"],
];

export const referencies = [
  { nom: "Pandas Cheat Sheet (oficial, PDF)", url: "https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf", desc: "La millor xuleta d'una pàgina de pandas. Va per tasques: seleccionar, agrupar, combinar." },
  { nom: "NumPy: the absolute basics for beginners", url: "https://numpy.org/doc/stable/user/absolute_beginners.html", desc: "La guia oficial de NumPy per començar." },
  { nom: "Referència de l'ndarray", url: "https://numpy.org/doc/stable/reference/arrays.ndarray.html", desc: "Tots els atributs i mètodes de l'array, separats. Són centenars: busca, no llegeixis." },
  { nom: "Referència del DataFrame", url: "https://pandas.pydata.org/docs/reference/frame.html", desc: "Tots els mètodes del DataFrame, agrupats per funció." },
  { nom: "Referència de la Series", url: "https://pandas.pydata.org/docs/reference/series.html", desc: "El mateix per a la Series." },
  { nom: "Glossari de scikit-learn", url: "https://scikit-learn.org/stable/glossary.html", desc: "Què vol dir fit, predict, estimator, i els atributs amb guió baix." },
];
