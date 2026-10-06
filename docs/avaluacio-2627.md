# Avaluació del mòdul · curs 2026-27

Com s'avalua l'optativa d'Aprenentatge automàtic, i **per què cada prova cau on cau**.

La idea que ordena tot el document: **l'avaluació d'aquest mòdul no mira enrere, mira endavant.**
Cada prova no pregunta «què has après del que hem fet», pregunta **«tens el que et cal per al
que ve ara»**. El curs acaba amb un agent de Reinforcement Learning competint en directe, i
arribar-hi demana una cadena de peces que s'han de tenir totes. Les proves són els graons
d'aquesta escala, no un peatge administratiu paral·lel.

---

## 1. El marc oficial

### El resultat d'aprenentatge, que és un de sol

> **Crea aplicacions fent ús de models d'aprenentatge automàtic.**

Un mòdul, una unitat formativa, un resultat d'aprenentatge. `QMP = QUF1 = QRA1`.

**La fitxa no el desglossa en criteris d'avaluació**: no n'hi ha cap llista al document. Si
calen per a la programació didàctica, s'han de demanar o redactar.

I val la pena fixar-se en el verb: diu **crea aplicacions**. No diu coneix algorismes ni demostra
teoremes. Això és el que justifica que el 80 % de la nota sigui pràctica amb ordinador, i és
coherent amb com està fet tot el material.

### La fórmula, literal

```
QRA1 = 10 % · ((Pe1+…+Pe5)/5)
     + 10 % · ((P1+…+P25)/25)
     + 80 % · ((Pp1+Pp2+Pp3+Pp4)/4)
```

**Cinc proves escrites, vint-i-cinc activitats, quatre proves pràctiques.** Sense ambigüitat.

### Les condicions que condicionen el disseny

| | |
|---|---|
| Proves escrites | Han de superar el **3** per poder ponderar |
| Proves pràctiques | Cal un **mínim de 5** |
| No presentar-s'hi sense justificació | **Pèrdua del dret a realitzar-la** |
| Activitats | Es qualifiquen **0 o 10**: només cal lliurar-les. **Fora de termini compten com a negatives** |
| Còpia o ús indegut d'internet o d'IA en una prova | Pot suposar la **pèrdua del dret a l'avaluació contínua** del RA, i zero a l'activitat |
| Format de les pràctiques | Amb ordinador, **semblants a les activitats fetes a classe** o modificacions seves |

**L'última fila és la més important de totes.** La fitxa demana que les proves pràctiques
s'assemblin a les activitats de classe, i el material està fet exactament així: quaderns amb les
cel·les de codi buides i comentaris que guien. **Una prova pràctica és literalment una d'aquestes
cel·les sobre un conjunt de dades que no hagin vist.** No cal inventar cap format nou.

### Un avís sobre la fitxa

**La fitxa de què surt tot això és la del curs 2024-25.** Ho diu ella mateixa: UF1 del 18/09/2024
al 21/05/2025, i «2 hores setmanals distribuïdes en una sessió de dues hores».

Això explica la contradicció que es va arrossegar setmanes: a 2 h setmanals durant tot el curs
surten 66 h, i a 4 h setmanals surten les mateixes 66 h però s'acaben al febrer. **No hi havia
cap contradicció d'hores, hi havia una fitxa vella.** Convé actualitzar-la.

La fitxa també llista R i Teachable Machine entre les eines del mòdul, i aquest curs R queda en
lectura recomanada.

---

## 2. L'escala cap al concurs

Abans de col·locar cap prova, la pregunta que les ordena: **què li cal, de veritat, a un alumne
per entrenar un agent el 2 de febrer?**

| Per fer això al concurs | Li cal haver assolit | On es guanya |
|---|---|---|
| Llegir i modificar la classe de l'agent | Que un model és un objecte amb atributs apresos | S04, S09 |
| Entendre el bucle d'entrenament | Haver-ne escrit un a mà | S18-S19 |
| Llegir una corba d'aprenentatge | Saber què és una funció de pèrdua i per què baixa | S17-S20 |
| Dissenyar una recompensa i justificar-la | Entendre què optimitza un model | tot el bloc 2 |
| Mesurar si el seu agent val alguna cosa | Mètriques i una referència honesta | S16 |
| Preparar i manejar les dades de l'entorn | NumPy, formes, eixos | S05-S08 |

**Cap d'aquestes peces es pot saltar.** Per això les proves es col·loquen just abans de cada
salt, no després de cada tema: han de dir si l'alumne pot continuar, mentre encara hi ha temps
de fer-hi alguna cosa.

---

## 3. Les quatre proves pràctiques (80 %)

Són el mòdul. Amb un mínim de 5 a cada una, són també l'única cosa que pot fer que algú no
superi el curs.

### Pp1 · S11 · dimarts 27 d'octubre — *Pots manejar dades?*

**Porta del bloc 2.** Sense això, tot el que ve després es fa a cegues.

Un CSV que no hagin vist. Carregar-lo, dir quantes files i columnes té, fer l'inventari de nuls,
respondre dues preguntes amb `.groupby()`, i un gràfic. Una cel·la final més curta: una norma o
una distància amb NumPy.

**L'enunciat diu quines eines fer servir.** El que s'avalua és que les sàpiguen encadenar i que
sàpiguen llegir el resultat, no que endevinin el nom d'un mètode.

> **No és un sondeig.** És la primera de les quatre i ja compta amb mínim de 5. Convé dir-ho a
> classe amb temps, a la S04 i un altre cop a la S10.

### Pp2 · S21 · dimarts 1 de desembre — *Pots entrenar, mesurar i verificar?*

**Porta cap a les xarxes.** Qui no arribi aquí, al gener no entendrà què fa `loss.backward()`.

Tres coses, sobre un conjunt que no hagin vist:

1. Entrenar dos models i comparar-los **amb la mètrica adequada**, no amb l'exactitud per defecte.
2. **Implementar una funció de pèrdua i comprovar-la** contra la de scikit-learn.
3. Explicar, mirant els pesos o les importàncies, per què un model prediu el que prediu.

Els punts 2 i 3 només són possibles gràcies al bloc de matemàtiques, i són exactament el que la
fitxa permet demanar: no és deduir una fórmula, és fer-la servir i verificar-la.

### Pp3 · S25 · dilluns 21 de desembre — *Pots treballar sense enganyar-te?*

Un CSV brut: nuls, columnes de text, duplicats. Muntar un `Pipeline` que **no filtri informació**
del test a l'entrenament, entrenar i justificar les decisions de neteja.

El que es mesura de debò aquí no és la precisió que obtinguin, és **si el número que donen és
honest**.

### Pp4 · S33 · dimarts 2 de febrer — *L'agent, i la seva defensa*

L'agent lliurat, que funcioni, i **la justificació de les decisions**: quina recompensa van
dissenyar i per què, què van provar i què van descartar.

> **Aquí hi ha un xoc amb la fitxa que s'ha de resoldre explícitament.** L'agent s'entrena a
> casa, sense supervisió, amb internet i amb IA a l'abast, i la fitxa diu que l'ús indegut d'IA
> en una prova pot costar l'avaluació contínua.
>
> **La solució: la Pp4 no és l'entrenament, és la defensa a classe.** L'agent és el lliurament
> previ; el que es qualifica és que funcioni i que l'alumne pugui explicar-lo davant del grup.
> Qui no pugui justificar el seu propi agent, no el té. Això ja és el que diu el reglament del
> concurs, i a més resol el problema de les màquines desiguals.

**I el concurs no es puntua per posició al marcador.** Guanyar és el premi, no la nota: si no,
guanya qui tingui millor portàtil.

---

## 4. Les cinc proves escrites (10 %)

**Cada una val un 2 % de la nota final.** La seva funció real no és qualificar: és **detectar qui
s'està descolgant abans de la pràctica que sí que pesa**, quan encara es pot fer alguna cosa.

Per això van col·locades **just abans de cada salt**, i són curtes: 15-20 minuts a l'inici de
sessió, conceptuals, sense ordinador.

| | Sessió | Data | Sobre què | Què protegeix |
|---|---|---|---|---|
| **Pe1** | S08 | dl 19 oct | Atribut contra mètode, què retorna cada cosa, què vol dir `axis` | La Pp1 |
| **Pe2** | S14 | dl 9 nov | Per què es parteix el conjunt, què és el sobreajust, què vol dir que un model «encerti» | El bloc de matemàtiques |
| **Pe3** | S20 | dl 30 nov | Què és una derivada en aquest context, què fa el descens de gradient, per què la log-loss i no el nombre d'errors | La Pp2 |
| **Pe4** | S28 | dl 18 gen | Què és una xarxa, per què la retropropagació és el gradient de la S18, què és una Q-xarxa | **El bloc de RL** |
| **Pe5** | S31 | dt 26 gen | Agent, entorn, recompensa, exploració contra explotació, i per què el crèdit diferit fa difícil l'RL | El concurs |

**La Pe4 és la que tapa el forat més perillós del curs.** Entre la Pp3 del 21 de desembre i el
concurs del 2 de febrer hi ha sis setmanes que inclouen tot el bloc de xarxes i tot el de RL,
que és el material més dur, **sense cap punt de control**. Sense la Pe4, si algú es despenja al
gener no te n'assabentes fins al dia del concurs, quan ja no hi ha remei.

Cost total de les cinc: uns 100 minuts de les 66 hores.

---

## 5. Les vint-i-cinc activitats (10 %)

**Un quadern lliurat = una activitat.** Es qualifiquen 0 o 10: només cal lliurar-les.

| Bloc | Quaderns |
|---|---|
| Fonaments | `FO_00`, `FO_01`, `FO_02` |
| Models | `ML_00`, `ML_01`, `ML_02`, `ML_03`, `ML_04`, `ML_05` |
| Matemàtiques | `MA_01` a `MA_06` |
| Pràctica | `EX_01` a `EX_05` |
| Xarxes i RL | els de `Deep Learning/` i `Reinforcement Learning/` que es treballin |

Són **20 al bloc de Machine Learning**, i amb els de xarxes i RL s'arriba a 25 sense forçar res.

**Dues coses que s'han de dir a classe el primer dia que es reparteixin:**

1. **Fora de termini compten com a negatives**, no com a no lliurades. No és el mateix.
2. Només cal lliurar-les, però **no fer-les és la manera més segura de suspendre les pràctiques**,
   perquè les pràctiques són variacions d'aquestes mateixes activitats. És el que diu la fitxa i
   és literalment cert amb aquest material.

---

## 6. El calendari d'avaluació, de cop

| Data | Sessió | Què |
|---|---|---|
| dl 19 oct | S08 | Pe1 |
| dt 27 oct | S11 | **Pp1 · dades** |
| dl 9 nov | S14 | Pe2 |
| dl 30 nov | S20 | Pe3 |
| dt 1 des | S21 | **Pp2 · entrenar i mesurar** |
| dl 21 des | S25 | **Pp3 · dades brutes i pipeline** |
| dl 18 gen | S28 | Pe4 — *el punt de control del bloc dur* |
| dt 26 gen | S31 | Pe5 |
| dl 1 feb | S32 | Tancament del lliurament dels agents |
| dt 2 feb | S33 | **Pp4 · el concurs i la defensa** |

---

## 7. Què queda per fer

1. **Actualitzar la fitxa d'inici**, que és la del 2024-25: hores setmanals i dates.
2. **Refer el llibre de qualificacions del Moodle.** Les tres categories i els seus pesos són
   correctes (`Pràctiques` 1,0 · `Proves escrites` 1,0 · `Proves pràctiques` 8,0), però el
   contingut és del curs passat: venciments de 2025, material de R, i dins de «Proves pràctiques»
   hi ha una vintena d'items que són activitats i algun que és una prova escrita.
3. **Redactar les cinc proves escrites.**
4. **Demanar o redactar els criteris d'avaluació** del RA, que la fitxa no porta.
