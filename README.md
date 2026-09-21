# Optativa de Machine Learning

Material docent de l'optativa de Machine Learning dels cicles formatius de grau superior de l'Institut TIC de Barcelona (DAM, DAW i ASIX).

El curs es divideix en dos blocs que s'encadenen: primer **Deep Learning**, per tenir les xarxes neuronals i PyTorch per la mà, i després **Reinforcement Learning**, on aquestes xarxes passen a ser el cervell d'un agent que aprèn jugant.

## Estructura

```
Deep Learning/
  01_teoria/          Notebooks de teoria: fonaments, PyTorch, arquitectures,
                      entrenament i les xarxes que després fan servir els agents
  02_fundamentos/     core/ (models, entrenament, utils) i exemples executables:
                      MLP amb MNIST, CNN amb CIFAR-10, LSTM de sentiments
  03_proyectos/       Classificació d'imatges amb transfer learning
  04_practica/        Pràctica de PyTorch cap a DQN (amb solucions a 02)

Reinforcement Learning/
  01_teoria/          Fonaments de RL, DQN i Stable-Baselines3
  02_fundamentos/     core/ (agents, utils) i exemples: Q-learning amb Taxi,
                      DQN amb CartPole
  03_proyectos_dqn/   Projectes amb DQN: Flappy Bird, Nibbler i Racing
  04_proyectos_avanzados/  Highway, LunarLander, MiniGrid i PyBullet
  05_Practica/        Pràctica final: entrenar un agent al teu propi entorn
  modelos/            Pesos ja entrenats per fer demostracions sense esperar

Conceptes bàsics sobre Machine Learning.pdf
```

## Posar-ho en marxa

Cada bloc té les seves dependències, i convé un entorn virtual per bloc:

```bash
cd "Deep Learning"          # o "Reinforcement Learning"
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
jupyter lab
```

Els datasets (MNIST, CIFAR-10) i els entorns de Gymnasium es descarreguen sols la primera vegada que s'executa el notebook, així que no són al repositori.

Els models entrenats de `Reinforcement Learning/modelos/` sí que hi són, perquè permeten ensenyar un agent que ja juga bé sense haver d'entrenar-lo a classe.

## Nota sobre dades personals

Aquest repositori **no conté cap treball d'alumnat**. Les entregues de la pràctica final, les notes i les rúbriques nominals queden excloses per `.gitignore` i no s'han de publicar mai aquí.

## Mòdul relacionat

El material del mòdul 1665 de Digitalització vivia abans en aquest mateix repositori i ara té el seu:
[ZenidX/Digitalitzacio-1665](https://github.com/ZenidX/Digitalitzacio-1665) · [web del mòdul](https://zenidx.github.io/Digitalitzacio-1665/)
