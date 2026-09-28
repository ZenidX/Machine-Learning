# Bateria d'exercicis de Machine Learning clàssic

Cinc quaderns de pràctica, un per conjunt de dades. Es fan **després** de la teoria dels cinc
models, que està a `../01_teoria/` i es va fer tota sobre Iris.

Cada quadern té les cel·les de codi **buides**, amb comentaris que guien, i comença amb la
llista de les eines que necessita, que estan explicades a `EX_00_caixa_eines.ipynb`.

Cada exercici acaba amb una línia de **com saps que ho has fet bé**, i el que hi va segueix una
regla: **si és un càlcul amb una sola resposta correcta, hi va el número** (funciona com una
prova unitària i els deixa trobar el seu propi error); **si és la troballa que dona sentit a
l'exercici, no hi va mai**, i al seu lloc hi ha una comprovació de propietat que verifica el
procediment sense dir el resultat. El raonament és a
[`../../docs/didactica-matematica-ml.md`](../../docs/didactica-matematica-ml.md), secció «Com es
dissenya un exercici».

**Els solucionaris no són en aquest repositori.** És públic i està enllaçat des de la web del
mòdul, així que un solucionari aquí és un solucionari a un clic de l'alumnat. Estan en local,
exclosos per `.gitignore`, i els reparteix el professor quan toca.

## Per què aquests cinc conjunts

No són cinc versions del mateix. **Cada conjunt existeix per ensenyar una cosa que Iris no
pot ensenyar**, i aquesta és tota la gràcia de la bateria:

| | Conjunt | El que ensenya que Iris no pot |
|---|---|---|
| **EX_01** | Wine · 178×13, 3 classes | Amb 13 columnes ja no es pot mirar tot en un gràfic. I com que `proline` va per centenars i altres columnes no arriben a 1, **el parany de les escales aquí es mesura**. |
| **EX_02** | Breast cancer · 569×30, binari | **La precisió no serveix de res tota sola.** En un diagnòstic, deixar passar un tumor maligne no val igual que una falsa alarma. |
| **EX_03** | Digits · 1797×64, 10 classes | **Una imatge també és una taula.** Cada columna és un píxel i no vol dir res tota sola, i els mateixos cinc models funcionen igual. |
| **EX_04** | Dades fabricades · 2 columnes | Amb només dues columnes **es pot dibuixar la frontera de cada model** i veure'n la forma: la recta de la logística, les escales de l'arbre, les corbes de l'SVM. |
| **EX_05** | Wine, embrutat a posta | **A la feina les dades no vénen netes.** Valors que falten, columnes de text, duplicats. I per què l'ordre de les operacions importa. |

## Ordre i quan fer-los

L'ordre és el recomanat i va de menys a més exigent. El primer és un calentament, el segon
i el cinquè són els que més canvien la manera de pensar.

- **EX_01 Wine** — just després de la teoria. Repeteix el flux sencer amb més columnes.
- **EX_02 Cancer** — quan ja donen per bona la precisió com a mesura. Serveix per trencar-la.
- **EX_03 Digits** — quan ja es mouen amb soltesa pel flux.
- **EX_04 Fronteres** — es pot avançar: ajuda a entendre la teoria, no només a practicar-la.
- **EX_05 Dades brutes** — l'últim, perquè necessita tota la resta i és el més pròxim a la feina real.

## Com es fan servir

Tot funciona a **Google Colab** sense instal·lar ni baixar res: els conjunts vénen dins de
scikit-learn, i el de dades brutes es fabrica sol.

Els exercicis estan pensats per **lliurar-los resolts**, i encaixen amb el tipus de prova
pràctica que demana la fitxa del mòdul: una prova pot ser una d'aquestes cel·les buides
sobre un conjunt que no hagin vist.

## Verificar-los

Els solucionaris (locals, no publicats) s'executen sencers abans de fer-los servir, i **els
números que apareixen als enunciats són els reals**. L'script força també el dibuix de les
figures, així que detecta una etiqueta amb LaTeX mal escrit, que altrament petaria en
projectar-la a classe:

```bash
# des de E:\WORK\Xavi\ProjectsITIC
CEIABD-IA\.venv\Scripts\python.exe "OPT-ML\_eines\executa_nb.py" "<el solucionari que toqui, que es en local>"
```
