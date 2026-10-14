// Inventari dels quaderns del curs i com s'obren.
// L'enllaç de Colab es construeix sempre igual: la ruta del fitxer dins del repositori
// ZenidX/Machine-Learning, branca main, amb cada tros codificat (l'espai de
// "Machine Learning" passa a ser %20).

const COLAB = "https://colab.research.google.com/github/ZenidX/Machine-Learning/blob/main/";
export const REPO_URL = "https://github.com/ZenidX/Machine-Learning";
export const GITHUB_BLOB = `${REPO_URL}/blob/main/`;

const codifica = (ruta) => ruta.split("/").map(encodeURIComponent).join("/");

export const colabUrl = (ruta) => `${COLAB}${codifica(ruta)}`;
export const githubUrl = (ruta) => `${GITHUB_BLOB}${codifica(ruta)}`;

const ML = "Machine Learning";

// descarrega: true vol dir que hi ha còpia a public/quaderns/ i es pot baixar des de la web.
export const quaderns = {
  // ---------- Bloc 1 · Dades ----------
  FO_00: {
    fitxer: "FO_00_objectes_i_autocompletar.ipynb",
    carpeta: `${ML}/01_fonaments`,
    titol: "Objectes de Python i autocompletat",
    descarrega: true,
    descripcio:
      "Com es pregunta a un objecte de Python què té a dins: type(), dir(), objecte.metode? i l'autocompletat amb la tecla TAB. La diferència entre un atribut i un mètode, que és per què df.shape va sense parèntesis i df.head() amb. I els objectes que et trobaràs a tot el curs: el Bunch que tornen els load_*, l'ndarray, el DataFrame, la Series, i un model de scikit-learn abans i després d'entrenar-lo. Acaba amb una exploració de dades guiada de principi a fi.",
  },
  FO_01: {
    fitxer: "FO_01_numpy.ipynb",
    carpeta: `${ML}/01_fonaments`,
    titol: "NumPy",
    descarrega: true,
    descripcio:
      "Per què no n'hi ha prou amb les llistes de Python, amb la comparació de temps executada. L'array, shape i dtype, indexació i llesques, i el parany de la llesca contra la còpia. Operacions vectoritzades, màscares booleanes, i les agregacions amb el concepte d'eix. Acaba ensenyant que la distància euclidiana i la precisió d'un model són una línia de NumPy cadascuna.",
  },
  FO_02: {
    fitxer: "FO_02_pandas.ipynb",
    carpeta: `${ML}/01_fonaments`,
    titol: "Pandas",
    descarrega: true,
    descripcio:
      "Què afegeix Pandas sobre NumPy: noms de columna i tipus barrejats. Series i DataFrame, i melb_data.csv, que són 13.580 habitatges venuts a Melbourne, amb nuls i columnes de text de veritat. Seleccionar amb loc i iloc, filtrar, l'inventari de valors que falten, groupby i agg, i com es passa d'un DataFrame a les X i y de scikit-learn. El CSV es baixa sol en executar el quadern: no has de pujar res.",
  },

  // ---------- Bloc 2 · Supervisat ----------
  ML_00: {
    fitxer: "ML_00_demo_iris.ipynb",
    carpeta: `${ML}/00_demo`,
    titol: "Iris: un model complet de principi a fi",
    descarrega: true,
    descripcio:
      "Entrenament i test, i per què se separen. El primer model complet sobre Iris, i on porta tot plegat. És el quadern de la sessió 2, que ara ja pots llegir entenent cada línia.",
  },
  ML_01: {
    fitxer: "ML_01_knn.ipynb",
    carpeta: `${ML}/01_teoria`,
    titol: "k veïns més propers (k-NN)",
    descarrega: true,
    descripcio:
      "El primer model de veritat, i el més senzill: la seva matemàtica és el teorema de Pitàgores. La distància, i el parany de les escales quan una columna va per centenars i l'altra no arriba a 1.",
  },
  ML_02: {
    fitxer: "ML_02_arbres.ipynb",
    carpeta: `${ML}/01_teoria`,
    titol: "Arbres de decisió",
    descarrega: true,
    descripcio:
      "Per què l'arbre d'Iris talla a petal_llarg <= 2,45 i no en un altre lloc. La impuresa i la tria del tall, calculades a mà i amb codi.",
  },
  ML_03: {
    fitxer: "ML_03_boscos.ipynb",
    carpeta: `${ML}/01_teoria`,
    titol: "Boscos aleatoris i mètriques",
    descarrega: true,
    descripcio:
      "Un arbre prou profund memoritza l'entrenament. La solució és fer-ne molts alhora i que votin. I les mètriques: per què la precisió tota sola no serveix.",
  },
  ML_04: {
    fitxer: "ML_04_regressio_logistica.ipynb",
    carpeta: `${ML}/01_teoria`,
    titol: "Regressió logística",
    descarrega: true,
    descripcio:
      "Traçar una ratlla i mirar de quin costat caus. La frontera, la sigmoide, i els pesos trobats per força bruta abans de saber fer-ho bé.",
  },
  ML_05: {
    fitxer: "ML_05_svm.ipynb",
    carpeta: `${ML}/01_teoria`,
    titol: "Màquines de vectors de suport (SVM)",
    descarrega: true,
    descripcio:
      "Si hi ha moltes rectes que separen bé les dades, quina és la millor situada? El marge, els vectors de suport i el kernel.",
  },

  // ---------- Bloc 3 · Dades brutes i no supervisat ----------
  ML_06: {
    fitxer: "ML_06_kmeans.ipynb",
    carpeta: `${ML}/01_teoria`,
    titol: "Agrupar sense etiquetes: k-means",
    descarrega: true,
    descripcio:
      "Si ningú et diu quins grups hi ha, els pots trobar? La inèrcia com a número a minimitzar, els dos passos de l'algorisme deduïts i no donats, Lloyd en deu línies i la comparació amb KMeans de scikit-learn. La part final (mínims locals, triar k, on falla) és lectura abans de l'EX_06.",
  },

  // ---------- Matemàtiques ----------
  MA_01: {
    fitxer: "MA_01_algebra_lineal.ipynb",
    carpeta: `${ML}/03_matematiques`,
    titol: "Àlgebra lineal",
    descarrega: true,
    mates: true,
    descripcio:
      "Norma, producte escalar, projecció, i la matriu entesa com una transformació. Acaba traient el coef_ d'un model ja entrenat i fent la predicció a mà amb X @ w + b per a les 150 flors d'Iris: el mateix número que dona scikit-learn.",
  },
  MA_02: {
    fitxer: "MA_02_descens_gradient.ipynb",
    carpeta: `${ML}/03_matematiques`,
    titol: "Descens de gradient",
    descarrega: true,
    mates: true,
    descripcio:
      "Què és una derivada, des de zero. La derivada de la log-loss, verificada contra el gradient numèric per diferències finites. I la regressió logística entrenada amb un bucle propi, sense scikit-learn. És el quadern més dur del curs i el que sosté tot el bloc de xarxes.",
  },
  MA_03: {
    fitxer: "MA_03_probabilitat_versemblanca.ipynb",
    carpeta: `${ML}/03_matematiques`,
    titol: "Probabilitat i versemblança",
    descarrega: true,
    mates: true,
    descripcio:
      "Bayes, i per què una prova amb un 99 % d'encert pot dir ben poca cosa. D'on surt la log-loss: és la versemblança amb un logaritme i un signe menys. Naive Bayes implementat de zero.",
  },
  MA_04: {
    fitxer: "MA_04_entropia_informacio.ipynb",
    carpeta: `${ML}/03_matematiques`,
    titol: "Entropia i informació",
    descarrega: true,
    mates: true,
    descripcio:
      "L'entropia mesurada en bits, i per què Gini i entropia donen arbres iguals. El guany d'informació, i la trampa de la columna d'identificadors. Que la log-loss i l'entropia creuada són el mateix número.",
  },
  MA_05: {
    fitxer: "MA_05_marge_optimitzacio.ipynb",
    carpeta: `${ML}/03_matematiques`,
    titol: "Marge i optimització",
    descarrega: true,
    mates: true,
    descripcio:
      "Multiplicadors de Lagrange amb un exemple que es pot tocar. Per què l'SVM només depèn d'uns pocs punts, que és una conseqüència matemàtica i no una optimització del programa. El truc del kernel, demostrat.",
  },
  MA_06: {
    fitxer: "MA_06_pca_vectors_propis.ipynb",
    carpeta: `${ML}/03_matematiques`,
    titol: "PCA i vectors propis",
    descarrega: true,
    mates: true,
    descripcio:
      "La maledicció de la dimensionalitat, mesurada. La direcció de màxima variància trobada per força bruta, i el descobriment que allò que surt és un vector propi. PCA implementat en cinc passos, i on falla.",
  },

  // ---------- Pràctica ----------
  EX_00: {
    fitxer: "EX_00_caixa_eines.ipynb",
    carpeta: `${ML}/02_practica`,
    titol: "La caixa d'eines",
    descarrega: true,
    descripcio:
      "Totes les eines que surten als exemples i als reptes: què fa cadascuna, què li dones, què et torna, un exemple mínim sobre una taula de sis files, i el parany de cadascuna. És una referència, no un exercici: no té cel·les buides i es pot executar sencer.",
  },
  EX_01: {
    fitxer: "EX_01_wine.ipynb",
    carpeta: `${ML}/02_practica`,
    titol: "El dataset Wine",
    dades: "178 files × 13 columnes, 3 classes",
    descarrega: true,
    descripcio:
      "El pas natural després d'Iris. Amb 13 columnes ja no es pot mirar tot en un gràfic, i les columnes van en escales molt diferents. Hi veuràs què li fa això a un model que mesura distàncies, i què canvia quan les escales s'igualen.",
  },
  EX_02: {
    fitxer: "EX_02_cancer.ipynb",
    carpeta: `${ML}/02_practica`,
    titol: "Diagnòstic de càncer de mama",
    dades: "569 × 30, binari",
    descarrega: true,
    descripcio:
      "Un problema binari amb les dues classes desiguals, i on els dos errors possibles no costen el mateix. Hi veuràs per què l'exactitud no és una mesura suficient, què hi afegeix la matriu de confusió, i com es compara un model amb un que respongui sempre la classe majoritària.",
  },
  EX_03: {
    fitxer: "EX_03_digits.ipynb",
    carpeta: `${ML}/02_practica`,
    titol: "Xifres escrites a mà",
    dades: "1797 imatges de 8×8, 10 classes",
    descarrega: true,
    descripcio:
      "Una imatge també és una taula: cada píxel és una columna. Hi veuràs si els models que ja coneixes serveixen igual quan les columnes són píxels i les classes són deu.",
  },
  EX_04: {
    fitxer: "EX_04_fronteres.ipynb",
    carpeta: `${ML}/02_practica`,
    titol: "La forma de cada model",
    dades: "Dades fabricades, 2 columnes",
    descarrega: true,
    descripcio:
      "Amb només dues columnes, la frontera de decisió es pot dibuixar. Hi veuràs quina forma li surt a cadascun dels cinc models sobre les mateixes dades, i què d'aquella forma ve del model i no de les dades.",
  },
  EX_05: {
    fitxer: "EX_05_dades_brutes.ipynb",
    carpeta: `${ML}/02_practica`,
    titol: "Quan les dades no vénen netes",
    dades: "Wine embrutat a posta",
    descarrega: true,
    descripcio:
      "Valors que falten, columnes de text i files duplicades. Hi veuràs per què importa l'ordre de les operacions: què passa segons en quin moment del procés es netegen i s'escalen les dades. És el model més directe de la Pp3.",
  },
  EX_06: {
    fitxer: "EX_06_kmeans.ipynb",
    carpeta: `${ML}/02_practica`,
    titol: "Agrupar sense etiquetes amb k-means",
    dades: "Una taula de set punts i dades reals",
    descarrega: true,
    descripcio:
      "Aquí la y no es toca: l'algorisme només veu X. Primer, càlcul a mà sobre set punts; després, dades reals, on les etiquetes, quan n'hi ha, només serveixen al final per comparar.",
  },

  // ---------- Bloc 4 · Xarxes i RL ----------
  DL_00: { fitxer: "DL_00_indice.ipynb", carpeta: "Deep Learning/01_teoria", titol: "Índex del bloc de xarxes", descripcio: "El mapa de tot el contingut i els requisits." },
  DL_01: { fitxer: "DL_01_fundamentos.ipynb", carpeta: "Deep Learning/01_teoria", titol: "Fonaments", descripcio: "Perceptró, funcions d'activació i retropropagació, que és el descens de gradient de MA_02." },
  DL_02: { fitxer: "DL_02_pytorch_basico.ipynb", carpeta: "Deep Learning/01_teoria", titol: "PyTorch bàsic", descripcio: "Tensors, autograd i mòduls nn." },
  DL_03: { fitxer: "DL_03_arquitecturas.ipynb", carpeta: "Deep Learning/01_teoria", titol: "Arquitectures", descripcio: "MLP, CNN, RNN/LSTM i autoencoders." },
  DL_04: { fitxer: "DL_04_entrenamiento.ipynb", carpeta: "Deep Learning/01_teoria", titol: "Entrenament", descripcio: "Optimització, regularització i callbacks." },
  DL_05: { fitxer: "DL_05_redes_para_RL.ipynb", carpeta: "Deep Learning/01_teoria", titol: "Xarxes per a RL", descripcio: "Per què el Q-learning amb taules no escala i com una xarxa fa d'aproximador de funció. És el pont cap a RL." },
  DL_PR: { fitxer: "DL_practica_pytorch_a_DQN.ipynb", carpeta: "Deep Learning/04_practica", titol: "Pràctica: de PyTorch a DQN", descripcio: "Tanca el bloc de xarxes i obre el de RL." },
  RL_01: { fitxer: "RL_01_fundamentos.ipynb", carpeta: "Reinforcement Learning/01_teoria", titol: "Fonaments de RL", descripcio: "El marc agent-entorn, el procés de decisió de Markov, polítiques i funcions de valor, SARSA i Q-learning." },
  RL_02: { fitxer: "RL_02_dqn.ipynb", carpeta: "Reinforcement Learning/01_teoria", titol: "DQN i Gymnasium", descripcio: "Deep Q-Networks, amb pràctica inclosa." },
  RL_03: { fitxer: "RL_03_sb3.ipynb", carpeta: "Reinforcement Learning/01_teoria", titol: "Stable-Baselines3", descripcio: "PPO i SAC, per a qui vulgui anar més enllà del DQN." },
  CONCURS: { fitxer: "plantilla_agent.ipynb", carpeta: "Reinforcement Learning/06_concurs", titol: "Plantilla del concurs", descripcio: "Entrena el teu cotxe de Racing. El reglament és al README.md de la mateixa carpeta." },
};

export const rutaQuadern = (q) => `${q.carpeta}/${q.fitxer}`;
