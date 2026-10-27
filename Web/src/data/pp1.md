# Prova pràctica 1 · Dades amb NumPy i Pandas

**Lliurament:** el quadern `.ipynb` a la tasca **Pp1** del Moodle, fins al final de la classe (20:00). Fes **Fitxer → Baixa → Baixa el fitxer .ipynb** a Colab i puja aquest fitxer.

**Tria una de les fitxes** (A, B, C o D) i lliura només aquella. Carrega el conjunt de dades amb la línia indicada i respon les preguntes en un quadern de Colab. Indica a l'inici del quadern quina fitxa has triat.
Cada resposta ha d'anar acompanyada del codi que la calcula i d'una frase que expliqui el resultat.

Primeres línies del quadern:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

---

## A · Instal·lacions d'autoconsum elèctric

**[▶ Obre la fitxa A a Colab](https://colab.research.google.com/github/ZenidX/Machine-Learning/blob/main/Machine%20Learning/05_proves/Pp1_A.ipynb)** · el quadern ja porta la càrrega de les dades i un espai per a cada pregunta. Fes **Fitxer → Desa una còpia a Drive** abans de començar.


- **Origen:** Departament de Territori, Habitatge i Transició Ecològica · Dades Obertes de la Generalitat
- **Font:** https://analisi.transparenciacatalunya.cat/d/2b4s-skfm
- **Llicència:** Llicència oberta d'ús d'informació – Catalunya
- **Mida:** 138.769 × 12

```python
df = pd.read_csv("https://analisi.transparenciacatalunya.cat/resource/2b4s-skfm.csv?$limit=200000")
```

**Context.** Les instal·lacions d'autoconsum elèctric inscrites al Registre d'Autoconsum de Catalunya,
amb la data en què es van posar en servei, la potència, la tecnologia i el municipi on són. Les dades
són vives: cada actualització hi afegeix files.

| Columna | Què és |
|---|---|
| `n_mero_rac` | número d'inscripció al registre |
| `n_mero_cau` | codi del punt d'autoconsum |
| `secci_registre` | `Amb excedents` o `Sense excedents` (si la instal·lació aboca a la xarxa l'energia que no consumeix) |
| `data_d_inscripci`, `data_de_posada_en_servei` | quan es va inscriure i quan es va posar en servei |
| `pot_ncia` | potència de la instal·lació, en kW |
| `tecnologia` | fotovoltaica, cogeneració, biogàs... |
| `codi_ine_municipi`, `municipi` | on |
| `codi_ine_comarca`, `comarca` | comarca |

**Preguntes**

1. Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?
2. Quantes instal·lacions hi ha de cada tecnologia i quanta potència sumen? Compara la potència
   mitjana i la mediana de les instal·lacions amb excedents i sense excedents.
3. Quines són les deu comarques i els deu municipis amb més instal·lacions?
4. Fes un gràfic de barres del nombre d'instal·lacions posades en servei cada any. L'any es treu
   així: `df["any_servei"] = pd.to_datetime(df["data_de_posada_en_servei"]).dt.year`.
5. Amb NumPy, construeix el vector de potència posada en servei cada any del 2019 al 2025 al
   Vallès Occidental i el del Baix Llobregat, i calcula la norma de la seva diferència.

---

## B · Intensitat mitjana diària de vehicles a les carreteres

**[▶ Obre la fitxa B a Colab](https://colab.research.google.com/github/ZenidX/Machine-Learning/blob/main/Machine%20Learning/05_proves/Pp1_B.ipynb)** · el quadern ja porta la càrrega de les dades i un espai per a cada pregunta. Fes **Fitxer → Desa una còpia a Drive** abans de començar.


- **Origen:** Direcció General d'Infraestructures i Mobilitat · Dades Obertes de la Generalitat
- **Font:** https://analisi.transparenciacatalunya.cat/d/xsvx-ym46
- **Llicència:** Llicència oberta d'ús d'informació – Catalunya
- **Mida:** 4.297 × 23

```python
df = pd.read_csv("https://analisi.transparenciacatalunya.cat/resource/xsvx-ym46.csv?$limit=10000")
```

**Context.** Les estacions d'aforament de trànsit de la xarxa de carreteres de la Generalitat i la
intensitat mitjana diària (IMD) de vehicles que hi passen, del 2017 al 2022. Cada fila és una
estació en un any.

| Columna | Què és |
|---|---|
| `any` | any del pla d'aforaments |
| `codi`, `carretera`, `pk` | l'estació: codi, carretera i punt quilomètric |
| `tipus_estaci` | Permanent, Primària, Secundària o Cobertura |
| `poblaci`, `comarca` | municipi i comarca de l'estació |
| `imd` | intensitat mitjana diària: vehicles al dia |
| `pesants` | percentatge de vehicles pesants respecte al trànsit total |
| `velocitat_km_h` | velocitat mitjana, en km/h |
| `carrils` | nombre de carrils |
| `any_1` | any en què es van prendre les dades |
| `latitud`, `longitud` | coordenades de l'estació, en graus |

**Preguntes**

1. Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?
2. Quines són les deu carreteres amb la IMD mitjana més alta l'any 2022?
3. Per comarques, quina IMD mitjana i quin percentatge mitjà de vehicles pesants hi ha l'any 2022?
   Quines són les cinc comarques amb més vehicles pesants?
4. Fes un gràfic de l'evolució de la IMD mitjana per any, amb totes les estacions juntes.
5. Amb NumPy, calcula la distància aproximada, en km, de cada estació de l'any 2022 al centre de
   Barcelona (41,3874, 2,1686), prenent 1° de latitud = 111 km i 1° de longitud = 111 · cos(41,39°) km.
   Compara la IMD mitjana de les estacions a menys de 25 km amb la de la resta.

---

## C · Meteorits

**[▶ Obre la fitxa C a Colab](https://colab.research.google.com/github/ZenidX/Machine-Learning/blob/main/Machine%20Learning/05_proves/Pp1_C.ipynb)** · el quadern ja porta la càrrega de les dades i un espai per a cada pregunta. Fes **Fitxer → Desa una còpia a Drive** abans de començar.


- **Origen:** The Meteoritical Society, publicat al portal de dades obertes de la NASA · TidyTuesday 2019-06-11
- **Font:** https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-06-11
- **Llicència:** dades de la NASA, de domini públic; repositori CC0
- **Mida:** 45.716 × 10

```python
df = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-06-11/meteorites.csv")
```

**Context.** Els meteorits registrats per la Meteoritical Society: on i quan es van trobar o es van
veure caure, de quina classe són i quant pesaven.

| Columna | Què és |
|---|---|
| `name`, `id` | nom i identificador del meteorit |
| `name_type` | `Valid` o `Relict` (meteorit molt alterat pel temps) |
| `class` | classe del meteorit |
| `mass` | massa, en grams |
| `fall` | `Fell` (es va veure caure) o `Found` (es va trobar després) |
| `year` | any de la caiguda o de la troballa |
| `lat`, `long` | coordenades, en graus |
| `geolocation` | les coordenades en una sola columna de text |

**Preguntes**

1. Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?
2. Quants meteorits es van veure caure i quants es van trobar? Compara la massa mitjana i la mediana
   dels dos grups.
3. Quants meteorits hi ha registrats per dècada? Quina dècada en té més?
4. Fes un gràfic de dispersió (`plt.scatter`) de la ubicació dels meteorits, amb la longitud a l'eix x
   i la latitud a l'eix y.
5. Amb NumPy, calcula la distància euclidiana, en graus, de cada meteorit a Barcelona (41,39, 2,17) i
   digues quins són els cinc més propers.

---

## D · Actuacions dels Bombers de la Generalitat (2025)

**[▶ Obre la fitxa D a Colab](https://colab.research.google.com/github/ZenidX/Machine-Learning/blob/main/Machine%20Learning/05_proves/Pp1_D.ipynb)** · el quadern ja porta la càrrega de les dades i un espai per a cada pregunta. Fes **Fitxer → Desa una còpia a Drive** abans de començar.


- **Origen:** Departament d'Interior i Seguretat Pública · Dades Obertes de la Generalitat
- **Font:** https://analisi.transparenciacatalunya.cat/d/g2ay-3vnj
- **Llicència:** Llicència oberta d'ús d'informació – Catalunya
- **Mida:** 67.948 × 17

```python
df = pd.read_csv("https://analisi.transparenciacatalunya.cat/resource/g2ay-3vnj.csv?$where=any=2025&$limit=100000")
```

**Context.** Les actuacions ateses pel cos de Bombers de la Generalitat durant el 2025, amb el tipus
d'actuació, la data i el municipi, la comarca i la regió d'emergències on es van fer.

| Columna | Què és |
|---|---|
| `act_num_actuacio` | identificador de l'actuació |
| `tga_nom_grupo` | grup d'actuació: salvaments, incendi urbà, mobilitat... |
| `tal_nom_alarma` | tipus d'actuació, més detallat |
| `municipi`, `nom_poblacio` | municipi i població on es va fer |
| `nom_comarca`, `nom_regio` | comarca i regió d'emergències |
| `any`, `mes`, `act_dat_actuacio` | quan |
| `urgents` | `S` si el tipus d'actuació és urgent, `N` si no ho és |
| `validat` | si la informació ja és definitiva |

**Preguntes**

1. Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?
2. Quantes actuacions hi ha de cada grup i quin percentatge del total representen? Quin percentatge
   de les actuacions són urgents?
3. Quines són les cinc comarques i els deu municipis amb més actuacions?
4. Fes un gràfic de barres del nombre d'actuacions de cada mes (la columna `mes`).
5. Amb NumPy, construeix el vector d'actuacions per mes de la regió de Girona i el de la regió de
   Lleida, divideix cada vector pel seu total i calcula la distància euclidiana entre tots dos.
