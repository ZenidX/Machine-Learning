# Optativa de Machine Learning

Material docent de l'optativa d'Aprenentatge automàtic (MPOML) de 2n dels cicles formatius de grau superior de l'Institut TIC de Barcelona (DAM i DAW).

**66 h · 4 h setmanals en sessions de 2 h · curs 2026-27.** El recorregut va de Python i els fonaments de dades fins a un **concurs d'agents de Reinforcement Learning** competint en entorns virtuals, que és la sessió que tanca el curs.

Web del mòdul: **[zenidx.github.io/Machine-Learning](https://zenidx.github.io/Machine-Learning/)**

## El criteri del material

Cada fórmula que apareix en un text va seguida de **la línia de NumPy que la calcula**, i cada implementació acaba **comparant-se amb scikit-learn**. Els models s'implementen a mà abans d'invocar-los, i la comparació ha de donar el mateix número.

Això no és un detall d'estil: és el que distingeix aquest material d'un tutorial d'API. Quan un alumne treu el `coef_` d'un model entrenat, calcula `X @ w + b` a mà i veu que el signe encerta les 150 files d'Iris, `fit` deixa de ser màgia.

## Estructura

```
docs/                   Programació del curs, diagnòstic, didàctica i guions de sessió.
                        Comença per diagnostic-i-programacio-2627.md

Machine Learning/
  00_demo/              La demostració del primer dia: Iris amb els cinc models
  01_fonaments/         NumPy i Pandas, amb dades reals d'habitatges
  01_teoria/            Els cinc models supervisats: k-NN, arbres, boscos,
                        regressió logística i SVM. Cada un implementat a mà
                        i comparat amb scikit-learn
  02_practica/          Cinc quaderns d'exercicis amb datasets diferents,
                        amb les cel·les buides. Amb solucionari a solucions/
  03_matematiques/      La matemàtica que hi ha a sota, aterrada al codi:
                        àlgebra lineal, descens de gradient, versemblança,
                        entropia, optimització amb restriccions i PCA

Deep Learning/
  01_teoria/            Fonaments de xarxes, PyTorch, arquitectures,
                        entrenament i les xarxes que després fan servir els agents
  02_fundamentos/       core/ i exemples: MLP amb MNIST, CNN amb CIFAR-10, LSTM
  03_proyectos/         Classificació d'imatges amb transfer learning
  04_practica/          Pràctica de PyTorch cap a DQN

Reinforcement Learning/
  01_teoria/            Fonaments de RL, DQN i Stable-Baselines3
  02_fundamentos/       core/ i exemples: Q-learning amb Taxi, DQN amb CartPole
  03_proyectos_dqn/     Flappy Bird, Nibbler i Racing
  04_proyectos_avanzados/  Highway, LunarLander, MiniGrid i PyBullet
  05_Practica/          Pràctica final: entrenar un agent al teu propi entorn
  06_concurs/           El concurs de la darrera sessió: plantilla d'agent,
                        script jutge i regles
  modelos/              Pesos ja entrenats per fer demostracions sense esperar

Web/                    La web del mòdul (React + Vite + Tailwind), desplegada
                        a GitHub Pages
_eines/                 Generador i verificador de quaderns
```

## Els quaderns

Tots els quaderns de `Machine Learning/` **funcionen a Google Colab sense instal·lar res**: només fan servir `numpy`, `pandas`, `matplotlib`, `scikit-learn` i `scipy`, i les dades surten de `sklearn.datasets` o es generen amb NumPy. Es poden obrir des de la web amb un botó, o baixar-los.

Els blocs de Deep Learning i Reinforcement Learning sí que demanen entorn propi, perquè fan servir PyTorch i Gymnasium:

```bash
cd "Reinforcement Learning"    # o "Deep Learning"
python -m venv .venv
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
jupyter lab
```

Els datasets (MNIST, CIFAR-10) i els entorns de Gymnasium es descarreguen sols la primera vegada, així que no són al repositori. Els models entrenats de `Reinforcement Learning/modelos/` sí que hi són, perquè permeten ensenyar un agent que ja juga bé sense haver d'entrenar-lo a classe.

## Escriure o modificar un quadern

**No editis un `.ipynb` a mà.** El format demana que cada línia de `source` acabi en `\n` excepte l'última; si no es respecta, les línies es peguen i el quadern no s'executa encara que el JSON sigui vàlid. Fes servir el generador:

```python
import sys; sys.path.insert(0, "_eines")
from nbgen import md, code, escriu
escriu([md("# Títol"), code("print('hola')")], "ruta/al/quadern.ipynb")
```

I verifica sempre que corre sencer abans de portar-lo a classe:

```bash
python _eines/executa_nb.py "Machine Learning/03_matematiques/MA_01_algebra_lineal.ipynb"
```

Executa totes les cel·les en ordre en un sol espai de noms i surt amb codi 1 si alguna peta.

## Nota sobre dades personals

Aquest repositori **no conté cap treball d'alumnat**. Les entregues de la pràctica final, les notes i les rúbriques nominals queden excloses per `.gitignore` i no s'han de publicar mai aquí.

Tampoc no conté el material del Moodle del curs passat: el va preparar una altra docent i es guarda només com a referència local, fora del repositori.

## Mòdul relacionat

El material del mòdul 1665 de Digitalització vivia abans en aquest mateix repositori i ara té el seu:
[ZenidX/Digitalitzacio-1665](https://github.com/ZenidX/Digitalitzacio-1665) · [web del mòdul](https://zenidx.github.io/Digitalitzacio-1665/)
