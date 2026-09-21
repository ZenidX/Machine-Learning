# Optativa de Machine Learning — pla del curs 2026-27

Document de treball per muntar el curs sencer. Fins ara la part final de Reinforcement Learning era l'única que impartia en Xavi; aquest curs també li toca la introducció, així que cal construir tot el recorregut que hi ha abans.

## 1. Marc oficial

De la fitxa d'inici del mòdul (`Fitxa inici_ICB0_ICC0_MPOML`):

| | |
|---|---|
| Mòdul | MPOML — Aprenentatge automàtic (Machine Learning) |
| Cicles | DAM (ICB0) i DAW (ICC0) |
| Hores | 66 h, totes al centre |
| Unitats formatives | UF1 única, 66 h |
| Ubicació | 2n curs, 2 h setmanals en una sola sessió |
| Resultat d'aprenentatge | **Crea aplicacions fent ús de models d'aprenentatge automàtic** |

Eines que la fitxa dona per descomptades: compte de Google i Workspace, Moodle, Teachable Machine, Colab, Python, R, Anaconda, Jupyter i scikit-learn.

### Com es qualifica

```
QMP = QUF1 = QRA1

QRA1 = 10 % · mitjana de 5 proves escrites
     + 10 % · mitjana de 25 activitats d'aprenentatge
     + 80 % · mitjana de 4 proves pràctiques
```

Condicions que marca la fitxa i que condicionen el disseny del curs:

- Una prova escrita per sota de 3 no pondera.
- Les proves pràctiques demanen un mínim de 5.
- Les activitats d'aprenentatge es qualifiquen 0 o 10: només cal lliurar-les, però fora de termini compten com a negatives.
- Les proves pràctiques es fan amb ordinador i s'assemblen a les activitats fetes a classe, o en són variacions.

Això fixa l'esquelet d'avaluació: **5 proves escrites, 4 proves pràctiques i 25 activitats**. El pla de sota s'hi ajusta.

## 2. D'on venim

**El que preveia la programació anterior** (seccions del Moodle, curs 24-25): introducció a l'aprenentatge automàtic amb Python bàsic · arbres de decisió i boscos aleatoris · Python · tècniques d'optimització (dades nul·les, variables categòriques, pipelines) · programació en R, amb prova pròpia.

**El que es va fer realment el curs 25-26** (secció visible del Moodle): Python des de zero amb lliuraments curts setmanals · Jupyter i Colab · Pandas · projecte d'anàlisi i representació de dades · aprenentatge supervisat amb DataCamp · i, l'últim mes, Reinforcement Learning amb la pràctica de l'agent DQN.

Les tres proves parcials que es van posar: conceptes bàsics de Python, exploració i visualització de dades, i supervised/unsupervised learning.

**El buit que cal omplir aquest curs:** entre "ja sé Pandas" i "entreno un agent amb DQN" falta el ML clàssic fet amb les mans, que el curs passat es va resoldre amb exercicis de DataCamp. Aquest és el tros que cal construir.

## 3. Decisions preses

- **R queda reduït a una o dues sessions.** És a la llista d'eines de la fitxa, així que no desapareix, però no es menja sis setmanes: es veu com a comparació, fent la mateixa regressió en R i en Python per entendre per què R existeix en estadística.
- **Reinforcement Learning manté la mida del curs passat**, quatre o cinc sessions al final amb la pràctica de l'agent DQN. La resta del curs és ML clàssic.
- **Els arbres de decisió recuperen espai.** Eren un bloc sencer de la programació anterior i el curs passat van quedar diluïts; encaixen de manera natural com a porta d'entrada al ML supervisat, perquè s'entenen sense matemàtiques.

## 4. Els blocs

Trenta-tres sessions de 2 h. Els mesos són orientatius, a ajustar amb el calendari real del grup.

### Bloc 0 — Punt de partida (1 sessió · setembre)

Què és i què no és l'aprenentatge automàtic, per a què s'usa i on falla. Recorregut pel curs i per com s'avalua.

Es fa servir **Teachable Machine** el primer dia: entrenar un classificador d'imatges amb la webcam en deu minuts, sense una línia de codi. Serveix per tenir la intuïció de "dades entren, model surt" abans de saber programar, i per parlar de biaix ensenyant-lo en calent amb un model entrenat amb quatre exemples.

### Bloc 1 — Python per treballar amb dades (7 sessions · setembre a novembre)

Tipus i variables · cadenes · condicionals · llistes i tuples · bucles · diccionaris · funcions · comprensions de llista.

És el bloc del curs passat i funcionava: lliuraments curts i freqüents (intercanvi de variables, inversió de cadena, lletra del DNI, pedra-paper-tisores, nombres únics ordenats). Es manté el ritme d'una activitat per sessió.

- **Prova escrita 1:** conceptes bàsics de Python.
- **Prova pràctica 1:** resoldre amb ordinador dos o tres exercicis de la mateixa família que els fets a classe.

### Bloc 2 — Dades: Pandas i visualització (5 sessions · novembre a desembre)

Jupyter i Colab · càrrega de dades · consultes i filtres amb Pandas · agrupacions · gràfics · com **no** fer un gràfic.

Es conserva l'article sobre errades en gràfics del curs passat, que és bon material de discussió.

- **Prova escrita 2:** exploració i visualització de dades.
- **Prova pràctica 2:** projecte d'anàlisi i representació de dades sobre un dataset donat. És la que ja existia i es manté.

### Bloc 3 — Aprenentatge supervisat (8 sessions · gener a febrer)

El cor del curs i la part que cal construir de nou.

Entrenament i test, i per què se separen · regressió lineal · classificació · **arbres de decisió** · **boscos aleatoris** · mètriques (exactitud, precisió, record, matriu de confusió) · sobreajust.

Tot amb **scikit-learn**. Els arbres entren primer perquè es poden dibuixar i explicar a algú que no sap matemàtiques, i d'aquí surt sol el concepte de bosc.

- **Prova escrita 3:** supervisat, mètriques i sobreajust.
- **Prova pràctica 3:** entrenar i avaluar un model sobre un dataset nou, amb justificació de les decisions.

### Bloc 4 — Dades reals i no supervisat (5 sessions · febrer a març)

Dades nul·les · variables categòriques · escalat · **pipelines** · agrupament amb k-means · reducció de dimensionalitat, a nivell d'idea.

Recupera el bloc de tècniques d'optimització de la programació anterior, que és el que separa un dataset de joguina d'un de real.

- **Prova escrita 4:** preparació de dades i no supervisat.

### Bloc 5 — R al costat de Python (1-2 sessions · març)

Què és R, d'on ve i per què continua viu en estadística. La mateixa regressió del bloc 3, feta en R, comparada línia a línia amb la de Python.

Sense prova pròpia: entra a la prova escrita 5.

### Bloc 6 — Xarxes neuronals i Reinforcement Learning (5-6 sessions · abril a maig)

Idea de xarxa neuronal i per què cal · de la xarxa a l'agent · Q-learning · DQN · Gymnasium.

Aquí ja hi ha material fet al repositori: els quaderns de `Deep Learning/01_teoria` per a la part de xarxes, i tot `Reinforcement Learning/` per a la resta, amb els models entrenats de `modelos/` per ensenyar un agent que ja juga bé sense esperar l'entrenament a classe.

- **Prova escrita 5:** xarxes, RL i R.
- **Prova pràctica 4:** agent DQN a un videojoc. És la pràctica final que ja existeix i funciona.

## 5. Resum del calendari

| Bloc | Sessions | Hores | Període orientatiu |
|---|---|---|---|
| 0 · Punt de partida | 1 | 2 | Setembre |
| 1 · Python per a dades | 7 | 14 | Setembre a novembre |
| 2 · Pandas i visualització | 5 | 10 | Novembre a desembre |
| 3 · Aprenentatge supervisat | 8 | 16 | Gener a febrer |
| 4 · Dades reals i no supervisat | 5 | 10 | Febrer a març |
| 5 · R al costat de Python | 2 | 4 | Març |
| 6 · Xarxes i Reinforcement Learning | 5 | 10 | Abril a maig |
| **Total** | **33** | **66** | |

## 6. Encaix amb l'avaluació

| Instrument | Quants | On |
|---|---|---|
| Proves escrites (10 %) | 5 | Un al final de cada bloc 1, 2, 3 i 4, i el cinquè al 6 amb R inclòs |
| Proves pràctiques (80 %) | 4 | Python · projecte de dades · model supervisat · agent DQN |
| Activitats (10 %) | 25 | Una per sessió als blocs 1 a 4, comptades 0 o 10 |

## 7. Què hi ha i què falta

**Ja fet i reaprofitable:**

- Tot el bloc 6: els quaderns de Deep Learning i Reinforcement Learning d'aquest repositori, amb els projectes i els models entrenats.
- El bloc 1 sencer: els materials i els lliuraments de Python del Moodle del curs passat.
- La prova pràctica del projecte de dades i la de l'agent DQN.

**Per construir:**

- El bloc 3 sencer. És la feina grossa: el curs passat es va cobrir amb exercicis de DataCamp i convé tenir material propi, amb els arbres de decisió com a fil conductor.
- El bloc 4, que es pot partir del material de tècniques d'optimització de la programació anterior si encara és accessible.
- La sessió de comparació amb R.
- Les proves escrites 3, 4 i 5.

**Per decidir:**

- Si es continua amb DataCamp com a suport del bloc 3 o es fa material propi.
- El dia i l'hora de la sessió setmanal, per fixar el calendari real amb dates.
