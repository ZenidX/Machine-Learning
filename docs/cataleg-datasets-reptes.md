# Catàleg de datasets per als reptes

Dades reals i públiques que l'alumnat no ha vist mai, per a reptes autònoms. Cada fitxa porta la línia
de càrrega per a Colab, el que s'ha comprovat descarregant-lo, de què va i unes quantes preguntes per
començar. **No hi ha respostes**: el que surti malament és part de l'aprenentatge.

- Verificació: 14-oct-2026. Cada dataset s'ha descarregat amb la mateixa URL que hi ha a la fitxa,
  amb `pandas` (`pd.read_csv(URL)` directe) o amb `fetch_openml`. La mida és la del fitxer descarregat.
- Les dades de la Generalitat (Socrata) i de l'Ajuntament estan **vives**: el nombre de files pot créixer
  respecte del que s'indica aquí.
- No s'hi fan servir ni Kaggle ni claus d'API. Cap dataset no conté noms ni identificadors de persones
  particulars.
- Ja usats al curs (exclosos): Iris, Wine (i `vins_bruts.csv`), Breast Cancer, Digits, `melb_data`,
  `load_sample_image`, i els sintètics `make_blobs`, `make_moons`, `make_circles` i `make_classification`.
- Dificultat: **1** = carrega net i les preguntes surten amb `groupby`; **2** = cal netejar o canviar
  de forma la taula; **3** = les dades enganyen si no es miren bé.
- Els reptes fets amb aquests datasets són a `Machine Learning/04_reptes/` (enunciat i dades) i, resolts,
  a `Machine Learning/04_reptes/resolts/`. Les fitxes no tenen respostes però sí alguna pista: si voleu
  fer un repte sense cap ajuda, llegiu-ne només l'enunciat.

### Llicències

| Origen | Llicència |
|---|---|
| Open Data BCN (`opendata-ajuntament.barcelona.cat`) | CC BY 4.0 (citar "Ajuntament de Barcelona") |
| Dades Obertes de la Generalitat (`analisi.transparenciacatalunya.cat`) | Llicència oberta d'ús d'informació – Catalunya (reutilització lliure citant la font). Alguns conjunts indiquen ODC-BY o domini públic, i s'assenyala a la seva fitxa |
| UCI ML Repository i còpies a OpenML | CC BY 4.0 (citar l'article o dataset) |
| TidyTuesday (`rfordatascience/tidytuesday`) | CC0 per al repositori; les dades vénen de tercers i s'indica l'origen a cada fitxa |
| Our World in Data | CC BY 4.0 |

### Paranys comuns a Colab

- Les URL de Socrata porten `$limit=`: sense aquest paràmetre només es baixen **1.000 files**.
- Socrata no conserva els zeros a l'esquerra dels codis (`08001` es llegeix com `8001`). Si cal
  conservar-los, carregueu amb `dtype={'codi_...': str}`.
- `pandas` de Colab (2.x) mostra els textos com a `object`; en local, amb pandas 3, surten com a `str`.

---

## Bloc 1 — Dades (NumPy / Pandas)

| # | Dataset | Origen | Files × columnes | MB | Dif. |
|---|---|---|---|---|---|
| 1.1 | Accidents gestionats per la Guàrdia Urbana (2024) | Open Data BCN | 7.536 × 25 | 1,2 | 1 |
| 1.4 | Spotify: 30.000 cançons | TidyTuesday | 32.833 × 23 | 8,0 | 1 |
| 1.5 | Aigua als embassaments de les conques internes | Generalitat | 88.047 × 5 | 8,0 | 2 |
| 1.6 | Preu mitjà del lloguer per municipi | Generalitat | 46.105 × 8 | 4,2 | 2 |
| 1.7 | Jocs de Steam | TidyTuesday | 26.688 × 10 | 2,7 | 2 |
| 1.8 | Accidents amb morts o ferits greus a Catalunya 2010-2023 | Generalitat | 24.478 × 58 | 15 | 2 |
| 1.9 | Meteo diària de l'Observatori Fabra (XEMA, des de 2015) | Generalitat / SMC | 96.036 × 10 | 15 | 3 |
| 1.10 | Qualitat de l'aire a Barcelona, 2024 (horària) | Generalitat | 15.898 × 40 | 4,5 | 3 |

### 1.1 Accidents de la Guàrdia Urbana a Barcelona (2024)
- **Font:** Open Data BCN, conjunt `accidents-gu-bcn`. CC BY 4.0. Hi ha un fitxer per any des del 2010.
- **Càrrega:**
  ```python
  df = pd.read_csv("https://opendata-ajuntament.barcelona.cat/data/dataset/e769eb9d-d778-4cd7-9e3a-5858bba49b20/resource/66f5e7e3-045b-4d19-b649-2eaea622ae93/download/2024_accidents_gu_bcn.csv")
  ```
- **Verificat:** 7.536 × 25 · 1,2 MB · 9 columnes de text i 16 numèriques. Nuls: `Numero_morts` 99,9 %,
  `Numero_lesionats_greus` 96,8 %, `Descripcio_causa_vianant` 93,8 %, `Num_postal ` 41 %.
- **Interès:** és de la nostra ciutat, té districte, barri, hora, dia de la setmana i coordenades.
- **Preguntes:**
  1. Quins districtes i barris acumulen més accidents? I més víctimes per accident?
  2. Com es reparteixen els accidents per hora del dia i per dia de la setmana? Feu-ne un gràfic.
  3. Què vol dir un `NaN` a `Numero_morts`? Com ho comprovaríeu amb les altres columnes?
  4. Amb NumPy: distància (euclidiana, en graus o aproximada en metres) de cada accident a la plaça de
     Catalunya (41,387, 2,170). Quins són els 10 més llunyans?
- **Paranys:** BOM UTF-8 al principi. La columna `Num_postal ` acaba amb un **espai**.

### 1.4 Spotify: 30.000 cançons
- **Font:** TidyTuesday 2020-01-21 (obtingut amb `spotifyr` de l'API de Spotify). Repositori CC0;
  les dades són de Spotify i se'n fa un ús educatiu.
- **Càrrega:**
  ```python
  df = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv")
  ```
- **Verificat:** 32.833 × 23 · 8,0 MB · nuls gairebé inexistents (5 files sense nom).
- **Interès:** és música que coneixen. Té 12 característiques d'àudio (danceability, energy, valence…),
  gènere i subgènere de la playlist, i popularitat. També serveix per al Bloc 4.
- **Preguntes:**
  1. Quin gènere és més "ballable" de mitjana? I el més enèrgic?
  2. Hi ha cançons repetides? Per què podria passar en aquest dataset?
  3. Com ha evolucionat la durada de les cançons per any de llançament?
  4. Amb NumPy: normalitzeu les característiques d'àudio i trobeu les 5 cançons més properes (distància
     euclidiana) a la vostra preferida.
- **Paranys:** `track_album_release_date` barreja `AAAA-MM-DD`, `AAAA-MM` i `AAAA`.

### 1.5 Aigua als embassaments de les conques internes
- **Font:** Agència Catalana de l'Aigua, conjunt `gn9e-3qhr`. Llicència oberta Catalunya.
- **Càrrega:**
  ```python
  df = pd.read_csv("https://analisi.transparenciacatalunya.cat/resource/gn9e-3qhr.csv?$limit=200000")
  ```
- **Verificat:** 88.047 × 5 · 8,0 MB · 0,1 % de nuls · 9 embassaments, dades diàries des del 2000.
- **Interès:** és una sèrie temporal llarga amb la sequera de 2022-2024 al mig. Format llarg: una fila per
  dia i embassament.
- **Preguntes:**
  1. Feu la corba del percentatge de volum de cada embassament al llarg dels anys.
  2. Quin any i mes van tenir el mínim de reserva total?
  3. Passeu la taula a format ample (`pivot`) amb una columna per embassament. Quants forats apareixen?
  4. Hi ha valors que no tinguin sentit físic?
- **Paranys:** cal convertir `dia` a data. El nom de la columna és `estaci` (truncat). Socrata no garanteix
  l'ordre de les files: ordeneu abans de fer gràfics.

### 1.6 Preu mitjà del lloguer per municipi
- **Font:** Agència de l'Habitatge de Catalunya (fiances INCASÒL), conjunt `qww9-bvhh`. Llicència oberta
  Catalunya.
- **Càrrega:**
  ```python
  df = pd.read_csv("https://analisi.transparenciacatalunya.cat/resource/qww9-bvhh.csv?$limit=200000")
  ```
- **Verificat:** 46.105 × 8 · 4,2 MB · `renda` buida en el 43 % de les files · anys 2007-2026.
- **Interès:** és el tema que els toca de prop. Té municipi, any, període, nombre de contractes i renda
  mitjana.
- **Preguntes:**
  1. Quins són els 10 municipis amb el lloguer més car l'últim any complet? I Sant Cugat i Terrassa?
  2. Quant ha pujat el lloguer a Barcelona des del 2014?
  3. Per què hi ha files sense `renda`?
  4. Quants contractes es signen cada any?
- **Paranys:** `codi_territorial` perd el zero (`08001` → `8001`).

### 1.7 Jocs de Steam
- **Font:** TidyTuesday 2019-07-30 (dades de SteamSpy). Repositori CC0; les dades són de tercers i se'n
  fa un ús educatiu.
- **Càrrega:**
  ```python
  df = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-07-30/video_games.csv")
  ```
- **Verificat:** 26.688 × 10 · 2,7 MB · `metascore` buit en el 89 % de les files, `price` en el 12 %.
- **Interès:** són videojocs, i la columna de propietaris és un rang en text, no un número.
- **Preguntes:**
  1. Quins desenvolupadors i editors tenen més jocs?
  2. Convertiu `owners` en un número (el punt mig del rang, per exemple). Quins són els jocs més venuts?
  3. Els jocs amb `metascore` són més cars o més jugats que els que no en tenen?
  4. Com ha evolucionat el nombre de llançaments per any?
- **Paranys:** `owners` té separador de milers i espais no separables (`\xa0..\xa0`). `release_date` té el
  format `"Nov 16, 2004"`. Hi ha títols de jocs repetits.

### 1.8 Accidents amb morts o ferits greus a Catalunya 2010-2023
- **Font:** Servei Català de Trànsit, conjunt `rmgc-ncpb`. Llicència oberta Catalunya.
- **Càrrega:**
  ```python
  df = pd.read_csv("https://analisi.transparenciacatalunya.cat/resource/rmgc-ncpb.csv?$limit=100000")
  ```
- **Verificat:** 24.478 × 58 · 15 MB · 42 columnes de text · nuls a `d_regulacio_prioritat` (71 %),
  `d_subtipus_tram` (67 %), `d_titularitat_via` (51 %) i `c_velocitat_via` (12,5 %).
- **Interès:** té moltes columnes amb sentit (meteo, lluminositat, tipus de via, vehicles implicats,
  gravetat), i és la base d'un problema de classificació desequilibrat al Bloc 2.
- **Preguntes:**
  1. Accidents i morts per any: s'observa algun canvi brusc? A quin any?
  2. Carretera o zona urbana: on hi ha més proporció d'accidents mortals?
  3. Quines combinacions de lluminositat i climatologia apareixen més en els accidents mortals?
  4. Quines comarques tenen més accidents greus? Ho relativitzaríeu d'alguna manera?
- **Paranys:** 58 columnes de noms críptics (`d_`, `f_`, `c_`). Cal interpretar-les abans de fer
  preguntes. Hi ha codis com `Sense especificar` que no són nuls però ho semblen.

### 1.9 Meteo diària de l'Observatori Fabra (XEMA)
- **Font:** Servei Meteorològic de Catalunya, conjunt `7bvh-jvq2` (estació D5, des de 2015). Llicència
  oberta Catalunya.
- **Càrrega:**
  ```python
  url = ("https://analisi.transparenciacatalunya.cat/resource/7bvh-jvq2.csv"
         "?$where=codi_estacio=%27D5%27%20AND%20data_lectura%3E=%272015-01-01%27&$limit=200000")
  df = pd.read_csv(url)
  ```
- **Verificat:** 96.036 × 10 · 15 MB · format **llarg** (una fila per dia i variable, amb 52 variables
  diferents) · `hora_tu` buit en el 51 % de les files.
- **Interès:** són dades reals de temperatura, pluja, vent i humitat de Barcelona. Obliguen a fer
  `pivot` abans de poder fer cap pregunta.
- **Preguntes:**
  1. Passeu a una taula d'una fila per dia, amb una columna per variable.
  2. Quin ha estat el dia més calorós i el més plujós des del 2015?
  3. Temperatura mitjana per mes i any: feu-ne un mapa de calor.
  4. Hi ha dies que falten? Quins?
- **Paranys:** `valor` és numèric però les unitats canvien segons la variable. Algunes variables porten
  "+ hora". La URL ha de dur els caràcters codificats (`%27`, `%20`).
- **Variant:** canvieu `D5` per una altra estació (p. ex. `X4` Barcelona-el Raval, o la més propera a
  casa vostra).

### 1.10 Qualitat de l'aire a Barcelona (2024, horària)
- **Font:** Xarxa de Vigilància i Previsió de la Contaminació Atmosfèrica, conjunt `tasf-thgu`. Llicència
  oberta Catalunya.
- **Càrrega:**
  ```python
  url = ("https://analisi.transparenciacatalunya.cat/resource/tasf-thgu.csv"
         "?$where=municipi=%27Barcelona%27%20AND%20data%3E=%272024-01-01%27%20AND%20data%3C%272025-01-01%27&$limit=100000")
  df = pd.read_csv(url)
  ```
- **Verificat:** 15.898 × 40 · 4,5 MB · format **ample** (columnes `h01`…`h24`) · fins a un 8,5 % de
  forats per hora · 8 estacions i 8 contaminants.
- **Interès:** el contrari del 1.9: cal fer `melt` per tenir una fila per hora. Es pot comparar trànsit,
  hora punta i estacions.
- **Preguntes:**
  1. Perfil mitjà de NO2 per hora del dia: a quines hores hi ha els pics?
  2. Quina estació té el NO2 mitjà més alt? I la de PM10?
  3. Laborables o cap de setmana: hi ha diferència?
  4. A quines hores falten més dades? Per què podria ser?
- **Paranys:** la unitat depèn del contaminant. `geocoded_column` és 100 % nul·la.

---

## Bloc 2 — Aprenentatge supervisat

Tots es carreguen amb `fetch_openml` (sense login):
```python
from sklearn.datasets import fetch_openml
df = fetch_openml(data_id=XXXX, as_frame=True).frame
```

| # | Dataset | OpenML id | Tipus | Files × col. | Desequilibri / objectiu | Dif. |
|---|---|---|---|---|---|---|
| 2.1 | Mushroom | 24 | classificació, tot categòric | 8.124 × 23 | 52 / 48 | 1 |
| 2.2 | Concrete Compressive Strength | 44959 | regressió | 1.030 × 9 | MPa | 1 |
| 2.5 | Bike Sharing (Washington) | 42712 | regressió | 17.379 × 13 | lloguers per hora | 2 |
| 2.6 | Online Shoppers Intention | 46947 | classificació | 12.330 × 18 | 85 / 15 | 2 |
| 2.7 | Bank Marketing (versió amb noms) | 46910 | classificació | 45.211 × 14 | 88 / 12 | 3 |
| 2.8 | Adult (census income) | 1590 | classificació | 48.842 × 15 | 76 / 24 | 3 |
| (2.9) | Accidents greus Catalunya (fitxa 1.8) | Socrata | classificació | 24.478 × 58 | 87 / 13 | 3 |

La llicència és CC BY 4.0 (UCI) o domini públic, segons l'OpenML. Cap d'aquests datasets no conté
identificadors.

### 2.1 Mushroom (`data_id=24`)
- **Verificat:** 8.124 × 23, totes categòriques, amb lletres (`'x'`, `'f'`…) · `stalk-root` buit en el
  30,5 % de les files.
- **Interès:** arbres de decisió en estat pur. És el primer contacte amb el `OneHotEncoder`.
- **Preguntes:** Quina profunditat d'arbre cal per classificar bé? Quina variable surt a dalt de tot de
  l'arbre? Funcionaria kNN amb aquestes dades? Quin cost té un fals negatiu aquí?
- **Paranys:** cal codificar-ho tot. El nom de columna `bruises%3F` porta un `?` codificat.

### 2.2 Concrete Compressive Strength (`data_id=44959`)
- **Verificat:** 1.030 × 9, tot numèric, sense nuls, 25 duplicats.
- **Interès:** regressió lineal contra arbre amb pocs atributs i físicament interpretables (ciment, aigua,
  edat…).
- **Preguntes:** Quina variable correlaciona més amb la resistència? Lineal o arbre: quin guanya, i per
  què? Feu la corba d'error en funció de la profunditat. Què passa si no escaleu les variables abans
  d'un kNN?
- **Paranys:** `age` té pocs valors diferents (dies de curat).

### 2.5 Bike Sharing (`data_id=42712`)
- **Verificat:** 17.379 × 13 · `season`, `weather`, `holiday` i `workingday` categòriques · sense nuls.
- **Interès:** és una regressió amb temps, meteo i dies festius, comparable amb el Bicing.
- **Preguntes:** Com és la corba de lloguers per hora en dies laborables i en festius? Quin model
  aprofita millor l'hora: lineal o arbre? Un `train_test_split` aleatori és honest amb dades
  temporals? Proveu de partir per any.
- **Paranys:** `hour` i `month` són cícliques.

### 2.6 Online Shoppers Intention (`data_id=46947`)
- **Verificat:** 12.330 × 18 · 15 % de compres · 125 duplicats · CC BY 4.0.
- **Interès:** sessions de botiga en línia. Introdueix el desequilibri moderat i l'*accuracy* enganyosa.
- **Preguntes:** Quina *accuracy* treu un model que sempre diu "no compra"? Quines variables de navegació
  predeuen la compra? Feu servir `class_weight` o un llindar diferent i compareu el F1.
- **Paranys:** `OperatingSystems`, `Browser` i `Region` són codis numèrics que en realitat són
  categories.

### 2.7 Bank Marketing (`data_id=46910`)
- **Verificat:** 45.211 × 14 · 12 % de "yes" · 274 duplicats · CC BY 4.0. Aquesta versió ja no porta la
  columna `duration`, que filtrava el resultat.
- **Interès:** és un desequilibri real (88/12), amb moltes categòriques i el valor `unknown`.
- **Preguntes:** Quin model supera la línia base de "ningú no contracta"? Què és `pdays = -1`? Com el
  tractaríeu? `unknown` és un nul o una categoria? Corba ROC contra precision-recall: quina explica
  millor aquest problema?
- **Paranys:** no feu servir `data_id=1461`, que té les columnes anomenades `V1`…`V16`.

### 2.8 Adult (`data_id=1590`)
- **Verificat:** 48.842 × 15 · nuls a `occupation` (5,8 %), `workclass` (5,7 %) i `native-country`
  (1,8 %) · 52 duplicats.
- **Interès:** és el clàssic per parlar de **biaix i equitat**: té `sex` i `race` com a atributs. Ens
  permet preguntar si el model és igual de bo per a tothom.
- **Preguntes:** Quina *accuracy* té el model per sexe i per grup? Què passa si traieu `sex` i `race`?
  Desapareix el biaix? `education` i `education-num` diuen el mateix? `fnlwgt` és un atribut o un pes?

### 2.9 (Extra) Accidents mortals a Catalunya
Fitxa 1.8. L'objectiu és `d_gravetat` (`Accident mortal` contra `Accident greu`, 13 % de mortals). Les
columnes `f_morts`, `f_ferits_greus` i `f_victimes` **revelen l'objectiu**: cal decidir què es pot fer
servir per predir.

---

## Bloc 3 — Dades brutes i Pipeline

| # | Dataset | Origen | Files × col. | MB | Objectiu | Dif. |
|---|---|---|---|---|---|---|
| 3.2 | Automobile (imports-85) | UCI | 205 × 26 | 0,03 | `price` | 2 |
| 3.3 | Hotel booking demand | TidyTuesday | 119.390 × 32 | 16,9 | `is_canceled` (37 %) | 2 |
| 3.4 | Accidents GU Barcelona 2023 + 2024 | Open Data BCN | 7.724 + 7.536 × 25 | 2,1 + 1,2 | — (neteja i unió) | 2 |
| 3.5 | Certificats d'eficiència energètica d'edificis | Generalitat | 60.000 × 29 (mostra) | 16 | `qualificaci_de_consum_d` (A-G) | 3 |

### 3.2 Automobile / imports-85
- **Font:** UCI ML Repository (1985). CC BY 4.0.
- **Càrrega:**
  ```python
  df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data", header=None)
  ```
- **Verificat:** 205 × 26 · 0,03 MB · sense capçalera.
- **Interès:** és petit però brut de debò. Cal llegir el fitxer de descripció de la UCI
  (`imports-85.names`) per posar-hi els noms i entendre cada columna.
- **Preguntes:** Pandas i el fitxer de descripció coincideixen en el tipus de cada columna? Què falta, i
  què hi faríeu? Pipeline amb imputació i one-hot: quin error (MAE) traieu amb validació creuada?
- **Paranys:** `header=None`; hi ha números escrits amb lletres (`two`, `four`).

### 3.3 Hotel booking demand
- **Font:** Antonio, Almeida i Nunes (2019), *Data in Brief*, via TidyTuesday 2020-02-11. CC BY 4.0. No
  conté noms ni contactes.
- **Càrrega:**
  ```python
  df = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-11/hotels.csv")
  ```
- **Verificat:** 119.390 × 32 · 16,9 MB · `company` buit en el 94 % de les files, `agent` en el 13,7 % i
  `country` en el 0,4 %.
- **Interès:** és un problema de negoci real, amb una reserva cancel·lada de cada tres. Barreja
  numèriques i categòriques i té dates partides en tres columnes.
- **Preguntes:** Quina *accuracy* treu el primer model sense pensar? És creïble? Quines columnes es
  coneixen el dia que entra la reserva? `agent` i `company`: els buits volen dir "no n'hi ha" o "no se
  sap"?
- **Paranys:** llegiu el diccionari de columnes abans de començar.

### 3.4 Accidents GU Barcelona, dos anys junts
- **Font:** com la fitxa 1.1, però amb el 2023 i el 2024.
- **Càrrega:**
  ```python
  a23 = pd.read_csv("https://opendata-ajuntament.barcelona.cat/data/dataset/e769eb9d-d778-4cd7-9e3a-5858bba49b20/resource/d12c8a6f-feb0-4c3e-bcf1-46b8a8b3d651/download/2023_accidents_gu_bcn.csv")
  a24 = pd.read_csv("https://opendata-ajuntament.barcelona.cat/data/dataset/e769eb9d-d778-4cd7-9e3a-5858bba49b20/resource/66f5e7e3-045b-4d19-b649-2eaea622ae93/download/2024_accidents_gu_bcn.csv")
  ```
- **Verificat:** 2023: 7.724 × 25 · 2024: 7.536 × 25. **Les columnes tenen el mateix nom.**
- **Interès:** el món real. El mateix publicador, el mateix dataset i un any de diferència basten perquè
  el `concat` "funcioni" i les dades quedin mal fetes.
- **Preguntes:** Compareu `dtypes`, `isna()` i `value_counts()` de cada any. Què ha canviat? Escriviu una
  funció de neteja que deixi els dos anys homogenis. Després del `concat`, el nombre de morts per any
  quadra?
- **Paranys:** que les columnes es diguin igual no vol dir que s'omplin igual.

### 3.5 Certificats d'eficiència energètica d'edificis (mostra de 60.000)
- **Font:** Institut Català d'Energia, conjunt `j6ii-t3w2` (uns 1,4 milions de certificats). Llicència
  oberta Catalunya. **La URL selecciona només columnes sense adreça**: no hi ha carrer, pis, porta, número,
  referència cadastral ni coordenades.
- **Càrrega:**
  ```python
  cols = ("codi_postal,poblacio,comarca,nom_provincia,zona_climatica,metres_cadastre,any_construccio,"
          "us_edifici,qualificaci_de_consum_d,energia_prim_ria_no_renovable,qualificacio_d_emissions,"
          "emissions_de_co2,consum_d_energia_final,cost_anual_aproximat_d_energia,vehicle_electric,"
          "solar_termica,solar_fotovoltaica,sistema_biomassa,xarxa_districte,energia_geotermica,"
          "eina_de_certificacio,valor_aillaments,valor_finestres,motiu_de_la_certificacio,"
          "normativa_construcci,tipus_tramit,ventilacio_us_residencial,rehabilitacio_energetica,data_entrada")
  url = f"https://analisi.transparenciacatalunya.cat/resource/j6ii-t3w2.csv?$select={cols}&$limit=60000"
  df = pd.read_csv(url)
  ```
- **Verificat:** 60.000 × 29 · 16 MB · nuls a `ventilacio_us_residencial` (82 %), `solar_termica` i
  `solar_fotovoltaica` (75 %), `any_construccio` (28 %) i `rehabilitacio_energetica` (15 %) · 437
  duplicats.
- **Interès:** és el repte més complet. Objectiu multiclasse ordinal (A-G), moltes columnes de text i
  nuls de molts tipus.
- **Preguntes:** Quines columnes coneixeria el propietari sense haver fet el certificat? Netegeu
  `motiu_de_la_certificacio`: quantes categories reals hi ha? Els anys de construcció són plausibles?
  Pipeline complet (imputació, encoding i model) amb validació creuada: quin F1 *macro* traieu?
- **Paranys:** `codi_postal` surt com a float sense el zero. Les columnes SI/NO tenen nuls.

---

## Bloc 4 — No supervisat (k-means, PCA)

| # | Dataset | Origen | Files × col. | Què s'agrupa | Dif. |
|---|---|---|---|---|---|
| 4.1 | Wholesale customers | UCI | 440 × 8 | clients d'un majorista | 1 |
| 4.2 | Spotify (fitxa 1.4) | TidyTuesday | 32.833 × 23 | cançons per característiques d'àudio | 2 |
| 4.3 | Indicadors territorials dels municipis | Generalitat (domini públic) | 1.896 × 85 | 947 municipis de Catalunya | 3 |
| 4.4 | CO₂ i energia per país | Our World in Data | 50.411 × 79 | països | 3 |

### 4.1 Wholesale customers
- **Font:** UCI (Cardoso, 2014). CC BY 4.0.
- **Càrrega:**
  ```python
  df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/00292/Wholesale%20customers%20data.csv")
  ```
- **Verificat:** 440 × 8 · 0,02 MB · tot enter, sense nuls.
- **Interès:** és la segmentació de clients clàssica. Té `Channel` (Horeca o retail) per comprovar *a
  posteriori* si els clústers tenen sentit.
- **Preguntes:** Quina k proposen el colze i la silueta? Els clústers canvien si escaleu, o si apliqueu un
  logaritme? Amb PCA a 2D: es veuen grups? Coincideixen amb `Channel`?
- **Paranys:** no feu servir `fetch_openml(1511)`, que porta les columnes anomenades `V1`…`V7`.

### 4.2 Spotify: clústers de cançons
- Mateixa càrrega que la fitxa 1.4. Feu servir només les columnes d'àudio (`danceability` … `tempo`).
- **Preguntes:** Els clústers de k-means s'assemblen als gèneres (`playlist_genre`)? Quantes components de
  PCA calen per explicar el 80 % de la variància? Què passa si no escaleu `tempo`, `loudness` i
  `duration_ms`?
- **Paranys:** convé mostrejar (k-means i silueta amb 30.000 files van lents).

### 4.3 Indicadors territorials dels municipis de Catalunya
- **Font:** Observatori del Territori, conjunt `8aaj-ypcb`. **Domini públic.**
- **Càrrega:**
  ```python
  df = pd.read_csv("https://analisi.transparenciacatalunya.cat/resource/8aaj-ypcb.csv?$limit=10000")
  ```
- **Verificat:** 1.896 × 85 (dos anys, 2023 i 2024) · 1,7 MB · 31 columnes amb nuls, alguns per sobre
  del 75 %.
- **Interès:** és molt nostre. Hi ha població, habitatge, renda, turisme, sòl i consum d'aigua per
  municipi. És el millor exemple de PCA amb moltes variables reals.
- **Preguntes:** Filtreu un any i trieu els indicadors amb pocs nuls. Quins municipis queden junts? On cau
  el vostre? Què "volen dir" les dues primeres components? Mireu-ne els *loadings*. Com afecten la
  població o les variables absolutes, comparades amb les relatives (per habitant)?
- **Paranys:** cal triar columnes (n'hi ha de redundants, com `_29_*`) i decidir entre imputar o
  descartar. Els noms tenen el prefix `_NN_`. Hi ha el dataset dels dos anys barrejats.

### 4.4 CO₂ i energia per país (Our World in Data)
- **Font:** `owid/co2-data`. CC BY 4.0.
- **Càrrega:**
  ```python
  df = pd.read_csv("https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv")
  ```
- **Verificat:** 50.411 × 79 · 14 MB · 53 % de cel·les nul·les (moltes sèries comencen tard) · anys fins
  al 2024.
- **Interès:** es poden agrupar països per perfil d'emissions (carbó, petroli, gas, per càpita, per PIB)
  i comparar anys diferents.
- **Preguntes:** Filtreu un any i una selecció de columnes per càpita. Quants països queden sense nuls?
  Quins clústers surten? On queda Espanya? Amb PCA a 2D, quins països són *outliers*?
- **Paranys:** hi ha files que **no són països** (continents, grups de renda, la UE…), i
  `iso_code` us pot ajudar a identificar-les. Les variables absolutes i per càpita no s'han de barrejar
  sense pensar-hi.

---

## Re-allotjament

Cap dataset del catàleg **no necessita re-allotjar-se**: tots es baixen d'una URL estable sense
autenticació. Si un dia algun deixa de funcionar (sobretot Open Data BCN, que canvia identificadors de
recurs), totes les llicències permeten penjar-ne una còpia al repositori citant la font. TidyTuesday és
CC0; UCI, OWID i Open Data BCN són CC BY; Generalitat, llicència oberta.
