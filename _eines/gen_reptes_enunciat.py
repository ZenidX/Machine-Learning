# -*- coding: utf-8 -*-
"""Genera els quaderns dels reptes (RE_*) en format «enunciat explicatiu».

Format decidit el 14-oct-2026: el repte de l'alumne és **només les dades i un enunciat que les
explica**. Res de bastida (ni caixa d'eines, ni nivells, ni cel.les per tasca, ni pistes plegades,
ni comprovacions). Cada quadern té:

1. Títol i encàrrec (rol i pregunta principal).
2. Les dades: font, llicència, què és cada fila, diccionari de les columnes que importen
   (significat, unitats, codis) i com s'han recollit.
3. Què has d'investigar: la pregunta principal i preguntes obertes, en prosa. Opcionalment,
   pistes que fan pensar (mai un número que sigui la troballa).
4. Exemples per inspirar-te: quaderns resolts del curs i de teoria.
5. Lliurament i, en dues o tres línies, quan cridar en Xavi.
6. La cel.la de càrrega (idèntica a la de la versió amb bastida, a `reptes_carrega.py`) i una
   cel.la de codi buida.

La versió resolta de cada repte és pública, a `04_reptes/resolts/` (la genera
`gen_reptes_resolts.py`). Els generadors antics amb bastida (`gen_RE_bloc34.py` i els de
`04_reptes/solucions/`) han quedat obsolets.

    python _eines/gen_reptes_enunciat.py            # tots
    python _eines/gen_reptes_enunciat.py RE_101     # un de sol
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reptes_carrega import CARREGA  # noqa: E402

ARREL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTI = os.path.join(ARREL, "Machine Learning", "04_reptes")

# Enllaços als quaderns del curs, relatius a 04_reptes/
EX00 = "[EX_00 · caixa d'eines](../02_practica/EX_00_caixa_eines.ipynb)"
EX01 = "[EX_01 · Wine](../02_practica/EX_01_wine.ipynb)"
EX02 = "[EX_02 · Breast cancer](../02_practica/EX_02_cancer.ipynb)"
EX03 = "[EX_03 · Digits](../02_practica/EX_03_digits.ipynb)"
EX04 = "[EX_04 · Fronteres](../02_practica/EX_04_fronteres.ipynb)"
EX05 = "[EX_05 · Dades brutes](../02_practica/EX_05_dades_brutes.ipynb)"
EX06 = "[EX_06 · k-means](../02_practica/EX_06_kmeans.ipynb)"
FO01 = "[FO_01 · NumPy](../01_fonaments/FO_01_numpy.ipynb)"
FO02 = "[FO_02 · Pandas](../01_fonaments/FO_02_pandas.ipynb)"
ML00 = "[ML_00 · demo Iris](../00_demo/ML_00_demo_iris.ipynb)"
ML01 = "[ML_01 · k veïns](../01_teoria/ML_01_knn.ipynb)"
ML02 = "[ML_02 · arbres](../01_teoria/ML_02_arbres.ipynb)"
ML03 = "[ML_03 · boscos](../01_teoria/ML_03_boscos.ipynb)"
ML04 = "[ML_04 · regressió logística](../01_teoria/ML_04_regressio_logistica.ipynb)"
ML06 = "[ML_06 · k-means](../01_teoria/ML_06_kmeans.ipynb)"
MA01 = "[MA_01 · àlgebra lineal](../03_matematiques/MA_01_algebra_lineal.ipynb)"
MA02 = "[MA_02 · descens del gradient](../03_matematiques/MA_02_descens_gradient.ipynb)"
MA06 = "[MA_06 · PCA i vectors propis](../03_matematiques/MA_06_pca_vectors_propis.ipynb)"

BLOCS = {
    1: "Bloc 1 — Dades",
    2: "Bloc 2 — Supervisat",
    3: "Bloc 3 — Dades brutes i Pipeline",
    4: "Bloc 4 — No supervisat",
}

LLIURAMENT_COMU = (
    "Lliura aquest quadern **executat**, sense errors, amb la teva anàlisi: cel·les de codi i, entre "
    "elles, cel·les de text on expliques què has fet i per què. Cada decisió que prenguis (què fas "
    "amb un buit, quina columna treus, quin model tries) ha de tenir la seva línia de justificació. "
    "Acaba amb una **conclusió** de tres a cinc frases, escrita per tu, que respongui l'encàrrec "
    "amb els números que has trobat."
)

# ---------------------------------------------------------------------------------------------
# Diccionaris compartits
# ---------------------------------------------------------------------------------------------
DIC_ACCIDENTS = [
    ("Numero_expedient", "identificador de l'accident (expedient de la Guàrdia Urbana)"),
    ("Codi_districte, Nom_districte", "districte de Barcelona (1-10) i el seu nom"),
    ("Codi_barri, Nom_barri", "barri (73 barris) i el seu nom"),
    ("Codi_carrer, Nom_carrer", "carrer on va passar l'accident"),
    ("Num_postal ", "número del carrer, tal com l'apunta l'agent (el nom de la columna acaba amb un espai)"),
    ("Descripcio_dia_setmana", "dia de la setmana, en català (`Dilluns` ... `Diumenge`)"),
    ("NK_Any, Mes_any, Nom_mes, Dia_mes", "data de l'accident, partida en any, mes (número i nom) i dia"),
    ("Hora_dia", "hora del dia (0-23)"),
    ("Descripcio_torn", "torn de la Guàrdia Urbana: `Matí`, `Tarda` o `Nit`"),
    ("Descripcio_causa_vianant", "si el vianant en va ser la causa, quina (creuar fora del pas, desobeir el semàfor...)"),
    ("Numero_morts", "morts (persones que moren en les 24 h següents)"),
    ("Numero_lesionats_greus", "ferits greus (ingrés hospitalari de més de 24 h)"),
    ("Numero_lesionats_lleus", "ferits lleus"),
    ("Numero_victimes", "víctimes en total"),
    ("Numero_vehicles_implicats", "vehicles implicats"),
    ("Coordenada_UTM_X_ED50, Coordenada_UTM_Y_ED50", "coordenades UTM (fus 31, datum ED50), en metres: la X és l'est i la Y el nord"),
    ("Longitud_WGS84, Latitud_WGS84", "longitud i latitud en graus (WGS84, la del GPS)"),
]

DIC_SPOTIFY = [
    ("track_id", "identificador de la cançó a Spotify"),
    ("track_name, track_artist", "títol i artista"),
    ("track_popularity", "popularitat a Spotify, de 0 a 100"),
    ("track_album_id, track_album_name", "identificador i nom de l'àlbum"),
    ("track_album_release_date", "data de publicació de l'àlbum (text)"),
    ("playlist_name, playlist_id", "playlist d'on s'ha tret la cançó"),
    ("playlist_genre, playlist_subgenre", "gènere (`pop`, `rap`, `rock`, `latin`, `r&b`, `edm`) i subgènere **de la playlist**"),
    ("danceability", "com de ballable és, de 0 a 1 (ritme, estabilitat del tempo, força del compàs)"),
    ("energy", "intensitat i activitat percebudes, de 0 a 1"),
    ("key", "tonalitat: 0 = Do, 1 = Do♯, 2 = Re ... 11 = Si"),
    ("loudness", "volum mitjà en decibels (dB), normalment entre −60 i 0"),
    ("mode", "mode: 1 = major, 0 = menor"),
    ("speechiness", "presència de veu parlada, de 0 a 1"),
    ("acousticness", "confiança que la cançó és acústica, de 0 a 1"),
    ("instrumentalness", "probabilitat que no tingui veu, de 0 a 1"),
    ("liveness", "probabilitat que sigui un enregistrament en directe, de 0 a 1"),
    ("valence", "com de «positiva» sona (alegre, eufòrica), de 0 a 1"),
    ("tempo", "tempo estimat, en pulsacions per minut (bpm)"),
    ("duration_ms", "durada, en mil·lisegons"),
]

# ---------------------------------------------------------------------------------------------
# Els reptes
# ---------------------------------------------------------------------------------------------
REPTES = [
    # ======================================================================== BLOC 1
    dict(
        id="RE_101", fitxer="RE_101_accidents_bcn.ipynb", bloc=1, dif=1,
        titol="On i quan hi ha accidents a Barcelona",
        encarrec="""Ets analista de dades a l'àrea de Mobilitat de l'Ajuntament de Barcelona. La regidoria
vol decidir on posar més controls i radars pedagògics l'any que ve, i et passa tots els accidents
que va gestionar la Guàrdia Urbana el 2024.""",
        pregunta="en quins districtes, a quines hores i quins dies hi ha més accidents, i on fan més mal?",
        font="""- **Font:** Open Data BCN, conjunt *Accidents gestionats per la Guàrdia Urbana a la ciutat de
  Barcelona*, fitxer del 2024. Llicència CC BY 4.0, © Ajuntament de Barcelona.
- **Còpia:** congelada al repositori el 14-oct-2026, sense cap canvi respecte de l'original.
- **Cada fila** és un accident (un expedient de la Guàrdia Urbana): on va passar, quan, quantes
  víctimes i vehicles hi va haver, i les coordenades. Unes 7.500 files i 25 columnes.""",
        diccionari=DIC_ACCIDENTS,
        recollida="""- Les dades surten dels atestats que redacta la Guàrdia Urbana quan hi intervé. Un accident sense
  intervenció policial no hi és.
- L'Ajuntament publica un fitxer per any. El format no sempre és el mateix d'un any a l'altre.
- El fitxer comença amb una marca invisible (BOM UTF-8); pandas la gestiona sola.""",
        investigar="""Respon la regidoria amb números i gràfics. **On**: quins districtes i barris acumulen més
accidents. **Quan**: com es reparteixen per hora del dia, per dia de la setmana (en l'ordre de la
setmana, no l'alfabètic) i per torn. **Com de greus**: quantes víctimes hi ha i quantes per
accident a cada districte. Que el districte amb més accidents sigui el més perillós no és
evident: decideix com ho mesures i defensa-ho.

Fes també un càlcul amb **NumPy**: la distància en metres de cada accident a la plaça de Catalunya
(latitud 41,3870, longitud 2,1700). A Barcelona, 1 grau de latitud ≈ 111.000 m i 1 grau de
longitud ≈ 111.000 · cos(latitud) m. Quants accidents hi ha a menys d'1 km? I els més llunyans, on
són?""",
        obertes=[
            "El fitxer porta les coordenades dues vegades (UTM i WGS84). Si calcules la mateixa distància amb les dues, coincideix?",
            "Els accidents de nit es concentren en algun dia de la setmana?",
            "Planteja't una pregunta que la regidoria agrairia i respon-la.",
        ],
        pistes=[
            "Abans de fer cap mitjana, mira quins valors pren cada columna de víctimes, comptant-hi els buits. Un buit pot voler dir «zero» o «no se sap», i la mitjana canvia molt segons quin dels dos sigui.",
            "Quan dues maneres de calcular la mateixa cosa no coincideixen, el problema pot ser a les dades i no al teu codi.",
        ],
        exemples=[
            f"{FO02}: §3-§4 (carregar i seleccionar), §6 (valors que falten), §7 (agrupar), §8 (ordenar i comptar) i §9 (gràfics ràpids).",
            f"{FO01}: §6 (agregacions i eixos) i §7 (la distància euclidiana).",
            f"{EX05}: com es diagnostica una taula abans de fer-hi preguntes.",
        ],
        xavi=[
            "Un buit vol dir el mateix a totes les columnes?",
            "El districte amb més accidents és el més perillós, o només el més gran i amb més trànsit?",
        ],
    ),
    dict(
        id="RE_102", fitxer="RE_102_spotify.ipynb", bloc=1, dif=1,
        titol="Quina música fa ballar",
        encarrec="""Treballes en una startup que fa playlists per a gimnasos, botigues i festes. L'equip de
producte vol entendre el catàleg abans de fer un recomanador, i et passa unes 30.000 cançons de
Spotify amb les seves característiques d'àudio.""",
        pregunta="""quin gènere fa més ballar i quin té més energia per entrenar? I, donada una cançó que
t'agrada, quines cinc del catàleg s'hi assemblen més?""",
        font="""- **Font:** TidyTuesday, setmana 2020-01-21 (`rfordatascience/tidytuesday`). Les dades es van
  obtenir de l'API de Spotify amb el paquet `spotifyr`. El repositori és CC0; les dades són de
  Spotify i aquí se'n fa un ús educatiu.
- **Cada fila** és una cançó **dins d'una playlist**: unes 33.000 files i 23 columnes.
- Diccionari original: <https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-01-21>""",
        diccionari=DIC_SPOTIFY,
        recollida="""- Algú va triar unes quantes playlists de cada gènere i en va baixar totes les cançons. El gènere i
  el subgènere són els de la playlist, no els de l'artista ni els de la cançó.
- Les característiques d'àudio (de `danceability` a `tempo`) les calcula Spotify amb els seus
  algorismes: són estimacions, no mesures.
- El fitxer fa uns 8 MB: la càrrega pot trigar uns segons.""",
        investigar="""Descriu el catàleg i respon l'equip de producte: quin gènere és més ballable, quin té més
energia i ritme per a un gimnàs (i si les dues columnes diuen el mateix), i com ha canviat la
durada de les cançons amb els anys. Pensa bé què és una fila abans de calcular mitjanes per
gènere.

Després, construeix un **recomanador amb NumPy**: tria nou característiques d'àudio, posa-les en
una escala comparable, tria una cançó que t'agradi i troba les cinc més properes per distància
euclidiana. Comprova que el resultat té sentit escoltant-les (o, almenys, mirant-ne el gènere).""",
        obertes=[
            "Les cançons més ballables són més populars?",
            "Quins subgèneres sonen més «tristos» i quins més «alegres» (`valence`)?",
            "Planteja't una pregunta que l'equip de producte agrairia i respon-la.",
        ],
        pistes=[
            "Si el recomanador et torna la mateixa cançó com a primera recomanació, no és cap error de NumPy: pregunta't per què.",
            "Abans de fer una distància, mira en quina escala està cada columna. Si una va de 0 a 1 i una altra fins a 200, quina manarà?",
        ],
        exemples=[
            f"{FO02}: §4 (filtrar), §5 (columnes noves), §7 (agrupar i `agg`), §8 i §9.",
            f"{FO01}: §6 (eixos), §7 (distància euclidiana) i §9, exercicis 4 i 5 (normalitzar una columna i la flor més propera).",
            f"{EX01}: com canvia una distància quan les columnes tenen escales molt diferents.",
        ],
        xavi=[
            "Si una cançó surt a pop i a latin, de quin gènere és?",
            "Normalitzo o no? Com ho sé, si les dues versions donen resultats diferents?",
        ],
    ),
    dict(
        id="RE_103", fitxer="RE_103_embassaments.ipynb", bloc=1, dif=2,
        titol="Com de greu va ser la sequera",
        encarrec="""Ets tècnic o tècnica de l'Agència Catalana de l'Aigua. Després de la sequera del 2022-2024, el
Govern vol un informe curt amb dades de tots els embassaments de les conques internes des de
l'any 2000.""",
        pregunta="""com de greu va ser la sequera comparada amb les anteriors, i com estan avui les reserves?
A quin moment del passat s'assemblen més?""",
        font="""- **Font:** Agència Catalana de l'Aigua, *Quantitat d'aigua als embassaments de les Conques
  Internes de Catalunya* (Dades Obertes de la Generalitat, conjunt `gn9e-3qhr`). Llicència oberta
  d'ús d'informació – Catalunya.
- **Còpia:** el conjunt s'actualitza cada dia. Aquí en tens una còpia congelada el 14-oct-2026, sense
  cap canvi.
- **Cada fila** és un embassament en un dia (format **llarg**): unes 88.000 files i 5 columnes.""",
        diccionari=[
            ("dia", "data de la lectura, com a text (`2000-01-01T00:00:00.000`)"),
            ("estaci", "nom de l'embassament i, entre parèntesis, el municipi (el nom de la columna està tallat)"),
            ("nivell_absolut", "alçada de l'aigua, en metres sobre el nivell del mar"),
            ("percentatge_volum_embassat", "volum d'aigua com a percentatge de la capacitat de l'embassament"),
            ("volum_embassat", "volum d'aigua, en hectòmetres cúbics (1 hm³ = mil milions de litres)"),
        ],
        recollida="""- Són les lectures diàries de l'ACA a nou embassaments de les conques internes (Ter, Llobregat,
  Muga, Foix...). No hi ha els de l'Ebre ni els del Segre, que gestiona una altra administració.
- Els embassaments són de mides molt diferents: comparar-ne els percentatges no és el mateix que
  comparar-ne els volums.
- El portal no garanteix l'ordre de les files.""",
        investigar="""Prepara l'informe per al Govern. Dibuixa la història de cada embassament i la de la **reserva
total** del sistema des del 2000. Troba el pitjor moment (dia i valor), el mínim de cada any, i
compara la sequera del 2022-2024 amb les anteriors. Després, situa el dia d'avui (l'últim de les
dades): quanta aigua hi ha comparada amb el mateix dia d'anys anteriors?

Amb **NumPy**, busca el dia del passat que més s'assembla a avui: tracta cada dia com un vector
amb el percentatge de cada embassament i calcula'n la distància al vector d'avui. Quins dies
d'anys anteriors surten més a prop, i té sentit?""",
        obertes=[
            "Quin és l'any típic: en quin mes estan més plens els embassaments? Tots igual?",
            "Quin embassament es va buidar més, quan, i quan va tornar a superar el 50 %?",
            "Planteja't una pregunta que el Govern agrairia i respon-la.",
        ],
        pistes=[
            "Abans de fer cap mitjana, decideix què vol dir «la reserva del sistema»: no és el mateix sumar volums que fer la mitjana de percentatges.",
            "Mira el resum numèric de cada columna i pregunta't si tots els valors són físicament possibles. Si n'hi ha que no, mira de quin embassament són.",
        ],
        exemples=[
            f"{FO02}: §4 (filtrar), §7 (agrupar i `pivot_table`), §8 (ordenar) i §9 (gràfics).",
            f"{FO01}: §6 (eixos), §7 (distància euclidiana) i §8 (broadcasting).",
            "Eines noves: `pd.to_datetime` (text a data) i `pivot` (de format llarg a ample). La documentació de pandas té exemples curts de totes dues.",
        ],
        xavi=[
            "Per a la reserva de tot el sistema, faig la mitjana dels percentatges o la suma dels volums?",
            "Comparar el mateix dia de l'any és just, si les pluges no cauen cada any al mateix moment?",
        ],
    ),
    dict(
        id="RE_104", fitxer="RE_104_lloguer.ipynb", bloc=1, dif=2,
        titol="Quant costa llogar un pis",
        encarrec="""Ets periodista de dades en un diari digital del Vallès. Prepares un article sobre el preu del
lloguer i tens les dades oficials de les fiances de tots els contractes de lloguer de Catalunya des
del 2007.""",
        pregunta="""quant ha pujat el lloguer a Barcelona, Sant Cugat del Vallès i Terrassa en deu anys? On és
més car llogar avui? I quants contractes se signen cada any?""",
        font="""- **Font:** Agència de l'Habitatge de Catalunya, *Preu mitjà del lloguer d'habitatges per
  municipi*, a partir de les fiances dipositades a l'INCASÒL (Dades Obertes de la Generalitat,
  conjunt `qww9-bvhh`). Llicència oberta d'ús d'informació – Catalunya.
- **Còpia:** congelada el 14-oct-2026, sense cap canvi.
- **Cada fila** és un municipi, un any i un període de l'any: unes 46.000 files i 8 columnes.""",
        diccionari=[
            ("ambit_territorial", "tipus de territori (aquí, sempre `Municipi`)"),
            ("codi_territorial", "codi INE del municipi (el portal en treu el zero de l'esquerra: `08001` → `8001`)"),
            ("nom_territori", "nom del municipi, amb l'article al final (`Ametlla del Vallès, l'`)"),
            ("any", "any"),
            ("periode", "període de l'any a què es refereix la fila (`gener-desembre`, `gener-març`...)"),
            ("habitatges", "nombre de contractes de lloguer (fiances) registrats en aquell període"),
            ("renda", "lloguer mitjà mensual dels contractes del període, en euros"),
            ("tram_preus", "franja de preu a què correspon la renda (text)"),
        ],
        recollida="""- Quan es signa un contracte de lloguer, el propietari ha de dipositar la fiança a l'INCASÒL. Les
  dades surten d'aquests dipòsits: és el preu dels **contractes nous**, no el de tots els pisos
  llogats.
- Els municipis no sempre han tingut el mateix nom al llarg de vint anys.
- L'últim any de les dades encara no s'ha acabat.""",
        investigar="""Escriu l'article amb números. Quants contractes es registren cada any a tot Catalunya (explica
quines files sumes i per què)? Quins municipis són els més cars l'últim any complet, i te'n
refiaries de tots? Com ha evolucionat la renda a **Barcelona**, **Sant Cugat del Vallès** i
**Terrassa**, i quant ha pujat entre el 2015 i el 2025? Quins municipis amb prou contractes han
pujat més?

Amb **NumPy**, compara trajectòries: cada municipi és un vector amb la renda de cada any del 2015
al 2025. Quins municipis s'assemblen més a Barcelona? Fes-ho dues vegades, en euros i amb cada
trajectòria dividida pel seu valor del 2015, i explica què compara cada versió.""",
        obertes=[
            "Què va passar el 2020 amb el nombre de contractes i amb la renda a Barcelona?",
            "Què indica `tram_preus`? El faries servir per comparar anys?",
            "Planteja't una pregunta per als lectors del diari (per exemple, sobre el teu municipi) i respon-la.",
        ],
        pistes=[
            "Abans de sumar files, mira bé quins valors té `periode` i pregunta't si un mateix contracte pot sortir en més d'una fila.",
            "Abans d'esborrar les files sense renda, mira què tenen en comú.",
            "Compta els municipis pel nom i pel codi. Si no surt el mateix, ja tens una pregunta.",
        ],
        exemples=[
            f"{FO02}: §4 (filtrar i combinar condicions), §6 (valors que falten), §7 (agrupar i `pivot_table`), §8 i §9.",
            f"{FO01}: §7 (distància euclidiana) i §8 (broadcasting).",
        ],
        xavi=[
            "Puc sumar files de períodes diferents? Què estaria comptant?",
            "Un municipi amb 7 contractes pot ser el més car de Catalunya? Com ho presentaria?",
        ],
    ),
    dict(
        id="RE_105", fitxer="RE_105_meteo_fabra.ipynb", bloc=1, dif=3,
        titol="Els estius de Barcelona, cada cop més calorosos?",
        encarrec="""Fas pràctiques al Servei Meteorològic de Catalunya. Una televisió prepara un reportatge sobre la
calor a Barcelona i us demana dades de l'Observatori Fabra, l'estació del Tibidabo que fa més de
cent anys que mesura el temps de la ciutat.""",
        pregunta="""des del 2016, els estius a Barcelona són cada cop més calorosos? Quins han estat els dies
més extrems, i quin any ha estat el més estrany?""",
        font="""- **Font:** Servei Meteorològic de Catalunya, *Dades meteorològiques diàries de la XEMA* (Dades
  Obertes de la Generalitat, conjunt `7bvh-jvq2`), estació **D5, Barcelona - Observatori Fabra**.
  Llicència oberta d'ús d'informació – Catalunya.
- **Còpia:** congelada el 14-oct-2026, de l'1-gen-2016 al 30-set-2026. Per no passar de 10 MB, no
  s'han baixat les columnes que són iguals a totes les files (el codi i el nom de l'estació). Els
  valors no s'han tocat.
- **Cada fila** és **una variable en un dia** (format **llarg**): unes 88.000 files i 7 columnes.
  No hi ha cap columna que es digui «temperatura».""",
        diccionari=[
            ("data_lectura", "dia de la lectura, com a text"),
            ("codi_variable", "codi numèric de la variable (per exemple, una temperatura, una pluja, una ràfega)"),
            ("nom_variable", "nom de la variable en català (`Temperatura màxima diària + hora`...)"),
            ("valor", "el valor del dia; la unitat depèn de la variable"),
            ("unitat", "unitat del valor: °C, mm, %, hPa, m/s, MJ/m²..."),
            ("hora_tu", "per a màximes i mínimes, hora (en temps universal) a què es van produir; buida per a la resta"),
            ("estat", "qualitat de la lectura segons el SMC (`Representatiu` / `No representatiu`)"),
        ],
        recollida="""- La XEMA és la xarxa d'estacions automàtiques del SMC. Cada estació envia les seves mesures, i el
  SMC en calcula els valors diaris i les valida.
- Algunes variables porten «+ hora» al nom: són màximes o mínimes, amb l'hora a què es van produir.
- Temps universal (TU) vol dir una hora menys que a l'hivern a Catalunya, i dues menys a l'estiu.""",
        investigar="""Prepara les dades per a la televisió. Primer cal tenir **una fila per dia i una columna per
variable**: decideix com fas aquest canvi de forma i justifica-ho. Després: quins han estat els
dies amb la màxima més alta i amb més pluja des del 2016? Fes un mapa de calor de la temperatura
mitjana de cada mes de cada any. Per a cada estiu, calcula la temperatura mitjana de juny, juliol
i agost i el nombre de dies de 30 °C o més: hi ha tendència?

Amb **NumPy**, busca l'any més estrany: cada any complet és un vector de 12 temperatures
mensuals. Calcula l'any mitjà i la distància de cada any a ell. Quin s'allunya més, i en quins
mesos és diferent?""",
        obertes=[
            "Quines variables són completes tot el període i quines no? N'hi ha alguna que només existeixi una part del temps?",
            "Quantes nits tropicals (la mínima no baixa de 20 °C) hi ha cada any? Encaixa amb el que has vist dels estius?",
            "Planteja't una pregunta que la televisió agrairia i respon-la.",
        ],
        pistes=[
            "Compta les variables de dues maneres, pel codi i pel nom. Si no surt el mateix, mira les que sobren abans de decidir com fas el canvi de forma.",
            "Un rècord que surt de pocs dies, o que desapareix quan canvies una decisió de neteja, mereix una segona mirada.",
        ],
        exemples=[
            f"{FO02}: §4 (filtrar), §6 (valors que falten), §7 (agrupar i `pivot_table`), §8 i §9.",
            f"{FO01}: §6 (eixos), §7 (distància euclidiana) i §8 (broadcasting).",
            "Si has fet el RE_103: `pd.to_datetime` i `pivot` són les mateixes eines. Per al mapa de calor, `plt.imshow`.",
        ],
        xavi=[
            "Dues files diuen el mateix amb noms escrits diferent: quina és la bona?",
            "Amb deu estius puc parlar de tendència, o és poc?",
        ],
    ),
    dict(
        id="RE_106", fitxer="RE_106_aire_bcn.ipynb", bloc=1, dif=3,
        titol="Quan i on es respira pitjor a Barcelona",
        encarrec="""Treballes a l'Agència de Salut Pública de Barcelona. Abans de la campanya sobre la zona de
baixes emissions, la direcció vol saber com es comporta la contaminació al llarg del dia i entre
barris, amb les dades horàries de totes les estacions de la ciutat durant el 2024.""",
        pregunta="""a quines hores i a quines estacions l'aire és pitjor? Els caps de setmana es respira millor?
Quines estacions es comporten igual i quines no?""",
        font="""- **Font:** Xarxa de Vigilància i Previsió de la Contaminació Atmosfèrica (XVPCA), *Qualitat de
  l'aire als punts de mesurament automàtics* (Dades Obertes de la Generalitat, conjunt `tasf-thgu`),
  municipi de Barcelona, any 2024. Llicència oberta d'ús d'informació – Catalunya.
- **Còpia:** congelada el 14-oct-2026, sense cap canvi.
- **Cada fila** és una estació, un contaminant i un dia, amb **24 columnes**, una per hora (format
  **ample**): unes 16.000 files i 40 columnes.""",
        diccionari=[
            ("codi_eoi, nom_estacio", "codi i nom de l'estació de mesura (8 estacions a Barcelona)"),
            ("data", "dia, com a text"),
            ("magnitud, contaminant", "codi numèric i nom del contaminant: NO2, NO, NOX, O3, PM10, PM2.5, SO2, CO"),
            ("unitats", "unitat de mesura del contaminant"),
            ("tipus_estacio", "`traffic` (al costat d'un carrer amb trànsit) o `background` (de fons, lluny de fonts directes)"),
            ("area_urbana", "`urban` o `suburban`"),
            ("h01 ... h24", "valor de cada hora: `h01` és de 0 a 1 h i `h24`, de 23 a 24 h"),
            ("altitud, latitud, longitud", "situació de l'estació"),
            ("codi_ine, municipi, codi_comarca, nom_comarca, geocoded_column", "iguals a totes les files o buides"),
        ],
        recollida="""- Les estacions són automàtiques i envien un valor cada hora. De tant en tant es calibren o s'avarien,
  i aquelles hores queden buides.
- No totes les estacions tenen els mateixos analitzadors: no totes mesuren tots els contaminants.
- Referència: la normativa europea fixa un valor límit diari de PM10 de 50 µg/m³ (la mitjana del
  dia).""",
        investigar="""Prepara l'informe per a la direcció. Primer, mira què es mesura, on i quan: quins contaminants
mesura cada estació i quants dies, i com es reparteixen els buits per hora. Després, passa la
taula a **una fila per hora** i respon: quin és el perfil horari del NO2 (que ve sobretot del
trànsit) i a quines hores hi ha els pics? Quina estació té el NO2 mitjà més alt, i el PM10? Hi ha
diferència entre els dies feiners i els caps de setmana?

Amb **NumPy**, busca estacions bessones: cada estació té un perfil horari de NO2 de 24 números.
Calcula la matriu de distàncies entre totes les parelles. Quines dues s'assemblen més, i quines
dues menys?""",
        obertes=[
            "Quants dies va superar cada estació el valor límit diari de PM10 el 2024?",
            "Té sentit dibuixar el perfil horari de tots els contaminants al mateix gràfic? Com ho faries perquè es poguessin comparar les formes?",
            "Planteja't una pregunta que la direcció agrairia i respon-la.",
        ],
        pistes=[
            "Una mitjana anual només es pot comparar amb una altra si totes dues cobreixen els mateixos dies. Abans de fer un rànquing, mira quants dies hi ha darrere de cada número.",
            "Llegeix la columna d'unitats com si fossis un ordinador: dues maneres d'escriure la mateixa unitat són dues categories.",
        ],
        exemples=[
            f"{FO02}: §4 (filtrar), §5 (columnes noves), §6 (valors que falten), §7 (agrupar i `pivot_table`), §8 i §9.",
            f"{FO01}: §6 (eixos), §7 (distància euclidiana) i §8 (broadcasting, per a la matriu de distàncies).",
            "Si has fet el RE_103 o el RE_105, allà vas canviar la forma d'una taula amb `pivot`. Aquí cal l'operació contrària, `melt`.",
        ],
        xavi=[
            "Puc comparar mitjanes d'estacions que no han mesurat els mateixos dies?",
            "La mitjana d'un any amaga els pics? Què és pitjor per a la salut?",
        ],
    ),
    # ======================================================================== BLOC 2
    dict(
        id="RE_201", fitxer="RE_201_bolets.ipynb", bloc=2, dif=1,
        titol="Bolets: comestible o verinós?",
        encarrec="""Fas de voluntari a una associació micològica. Volen una app que, a partir de trets que qualsevol
persona pot mirar al bosc (forma i color del barret, olor, làmines, anell...), digui si un bolet és
**comestible** o **verinós**.""",
        pregunta="""es pot decidir amb un model? Amb quin, i com de gran ha de ser? Què ha après el model (ha de
ser una cosa que una persona pugui seguir)? I què passa quan s'equivoca, si aquí no tots els
errors costen el mateix?""",
        font="""- **Font:** *Mushroom* (UCI Machine Learning Repository, 1987), a OpenML amb `data_id=24`. Llicència
  CC BY 4.0.
- **Cada fila** és una **espècie de bolet descrita** a la guia *The Audubon Society Field Guide to
  North American Mushrooms*: 8.124 files, 22 trets visibles codificats amb una lletra i la classe.
- Fitxes: <https://www.openml.org/d/24> i <https://archive.ics.uci.edu/dataset/73/mushroom>.""",
        diccionari=[
            ("class", "**objectiu**: `e` = comestible (*edible*), `p` = verinós o dubtós (*poisonous*)"),
            ("cap-shape", "forma del barret: b campana, c cònic, x convex, f pla, k amb mugró, s enfonsat"),
            ("cap-surface", "superfície del barret: f fibrosa, g amb solcs, y escatosa, s llisa"),
            ("cap-color", "color del barret: n marró, b beix, c canyella, g gris, r verd, p rosa, u porpra, e vermell, w blanc, y groc"),
            ("bruises%3F", "si es taca en tocar-lo: t sí, f no (el `%3F` és un `?` codificat)"),
            ("odor", "olor: a ametlla, l anís, c creosota, y peix, f fètida, m humitat, n cap, p picant, s espècies"),
            ("gill-attachment, gill-spacing, gill-size", "làmines: com s'uneixen al peu (a unides, f lliures...), separació (c juntes, w atapeïdes) i mida (b amples, n estretes)"),
            ("gill-color", "color de les làmines (mateixos codis de color; k negre, h xocolata, o taronja)"),
            ("stalk-shape, stalk-root", "peu: forma (e s'eixampla, t s'estreny) i base (b bulbosa, c en maça, e igual, r amb arrels...)"),
            ("stalk-surface-above-ring, stalk-surface-below-ring", "superfície del peu per sobre i per sota de l'anell: f fibrosa, y escatosa, k sedosa, s llisa"),
            ("stalk-color-above-ring, stalk-color-below-ring", "color del peu per sobre i per sota de l'anell"),
            ("veil-type, veil-color", "vel: tipus (p parcial, u universal) i color"),
            ("ring-number, ring-type", "anells: quants (n cap, o un, t dos) i de quin tipus (e evanescent, l gran, p penjant...)"),
            ("spore-print-color", "color de l'esporada"),
            ("population, habitat", "com creix (a abundant, c en grups, s escampat, y solitari...) i on (d bosc, g herba, l fulles, m prats, p camins, u urbà, w deixalles)"),
        ],
        recollida="""- No són bolets collits i analitzats: són **descripcions d'espècies** d'una guia de camp, amb una
  fila per cada combinació de trets possible. Les espècies de classe dubtosa s'han posat amb les
  verinoses.
- A la UCI, el valor que falta s'escrivia `?`; a OpenML arriba com a `NaN`.""",
        investigar="""Respon les tres preguntes de l'associació. Explora els trets i decideix què fas amb els valors
que falten. Codifica les lletres per poder entrenar, i compara un **arbre de decisió** (de quina
profunditat?) amb un **k veïns**. Per triar, pensa en el que demana l'associació: un model que
encerti, però que una persona pugui seguir al bosc.

La teoria ha d'aterrar al codi: calcula **a mà** el Gini del node arrel i dels dos fills del
primer tall, i comprova'ls contra el que guarda scikit-learn. Calcula també a mà, des de la matriu
de confusió, el *recall* de la classe que importa, i comprova'l amb `recall_score`. Quin dels dos
errors és el perillós, i quants en fa el model que portaries a l'app?""",
        obertes=[
            "Si l'app només pogués fer **tres preguntes**, quins tres trets triaries, i quant perdries?",
            "Amb dades codificades en 0 i 1, què mesura la distància euclidiana entre dos bolets?",
            "Amb només 60 bolets d'entrenament, quin dels dos models aguanta millor?",
        ],
        pistes=[
            "Si et surt un 100 %, no és necessàriament un error de codi. Però «zero errors al test» no és «zero errors al bosc».",
            "Una precisió molt alta pot amagar uns quants errors del tipus que no et pots permetre: compta'ls per separat.",
        ],
        exemples=[
            f"{ML00} i {EX00} §1: separar entrenament i test.",
            f"{ML01} §2-§4 (k veïns i distància) i {ML02} §2, §3 i §6 (Gini, el tall i la profunditat).",
            f"{EX00} §4 (columnes de text i `OneHotEncoder`) i §7 (matriu de confusió i *recall*).",
            f"{EX02}: per què la precisió sola no serveix quan un error és més greu que l'altre.",
        ],
        xavi=[
            "Em surt un 100 %. Això és creïble, o m'he equivocat?",
            "El model és prou bo per posar-lo en una app de veritat?",
        ],
    ),
    dict(
        id="RE_202", fitxer="RE_202_compres_en_linia.ipynb", bloc=2, dif=2,
        titol="Qui acabarà comprant?",
        encarrec="""Treballes a l'equip de dades d'una botiga en línia. Màrqueting no vol una caixa negra que
«endevini»: vol un model que **expliqui** quins senyals de la navegació empenyen una sessió cap a
la compra, i que doni una **probabilitat** que es pugui posar en un tauler.""",
        pregunta="""amb una regressió logística, quines variables pesen a favor i en contra de la compra, quant,
i com arriba el model a la probabilitat d'una sessió concreta?""",
        font="""- **Font:** *Online Shoppers Purchasing Intention* (Sakar i Kastro, 2018; UCI), a OpenML amb
  `data_id=46947`. Llicència CC BY 4.0.
- **Cada fila** és **una sessió** d'un visitant en una botiga en línia durant un any: 12.330 files i
  18 columnes. No hi ha cap identificador de persona.
- Documentació: <https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset>""",
        diccionari=[
            ("Revenue", "**objectiu**: si la sessió va acabar en compra (`True` / `False`, com a text)"),
            ("Administrative, Informational, ProductRelated", "nombre de pàgines de cada tipus vistes a la sessió (gestió del compte, informació, productes)"),
            ("Administrative_Duration, Informational_Duration, ProductRelated_Duration", "temps passat a cada tipus de pàgina, en segons"),
            ("BounceRates", "taxa de rebot mitjana de les pàgines vistes (Google Analytics): proporció de visites que entren per aquella pàgina i se'n van sense fer res més"),
            ("ExitRates", "taxa de sortida mitjana de les pàgines vistes: proporció de visites en què aquella pàgina és l'última"),
            ("PageValues", "valor mitjà de les pàgines vistes, segons Google Analytics. Llegeix a la documentació com es calcula"),
            ("SpecialDay", "proximitat a un dia especial (Sant Valentí, Dia de la Mare...), de 0 a 1"),
            ("Month", "mes de la sessió (text)"),
            ("OperatingSystems, Browser, Region, TrafficType", "codis del sistema operatiu, el navegador, la regió i l'origen del trànsit"),
            ("VisitorType", "`Returning_Visitor`, `New_Visitor` o `Other`"),
            ("Weekend", "si la sessió és en cap de setmana"),
        ],
        recollida="""- Les dades són d'una botiga real, recollides amb Google Analytics durant un any. Cada sessió és d'un
  usuari diferent, perquè no hi hagi tendències d'una sola persona.
- Les mètriques de Google Analytics es calculen sobre totes les visites del web, no només sobre
  aquesta sessió.""",
        investigar="""Construeix el model que demana màrqueting i explica'l. Abans, fixa la **línia de sortida**:
quina precisió té un model que mai no diu «compra»? Decideix quines columnes són números de
debò i quines són codis. Entrena una **regressió logística** amb les numèriques escalades, compara
la precisió amb la línia de sortida, i llegeix-ne els pesos: quines variables empenyen cap a la
compra, quines en contra, i quant (tradueix el pes més gran a *odds*).

La teoria ha d'aterrar al codi: calcula **a mà** la probabilitat de compra de totes les sessions
de test, primer $z = Xw + b$ i després la sigmoide, i comprova-la contra `predict_proba`.
Descompon la $z$ d'una sessió columna per columna. Implementa la **log-loss** amb NumPy i
comprova-la amb `log_loss`; compara-la amb la d'un model que dona a tothom la mateixa
probabilitat.""",
        obertes=[
            "Si afegeixes les categòriques (mes, tipus de visitant...), millora la log-loss? Què faria el model amb una sessió d'un mes que no ha vist mai?",
            "Si treus la variable amb més pes, quant empitjora el model? Aquesta variable, la sabries a mitja sessió, quan voldries oferir un descompte?",
        ],
        pistes=[
            "Si una sola variable fa gairebé tota la feina, abans de celebrar-ho pregunta't quan es coneix el seu valor.",
            "La precisió i la log-loss poden no anar juntes. Si el model amb prou feines supera la línia de sortida en precisió, mira l'altra mesura abans de dir que no serveix.",
        ],
        exemples=[
            f"{ML04} §2-§4: la regressió logística, la sigmoide i els pesos.",
            f"{MA01} §7 (un model és un vector i una multiplicació) i {MA02} §5 (la log-loss).",
            f"{EX00} §2 (`StandardScaler` i `fit` contra `transform`), §4, §6 i §7 (`OneHotEncoder`, `ColumnTransformer`, `DummyClassifier`).",
            f"{EX02}: la precisió que enganya.",
        ],
        xavi=[
            "El pes més gran és tan gran que em fa sospitar. Puc fer-me'l meu?",
            "Aquesta variable, la puc fer servir o és fer trampa?",
        ],
    ),
    dict(
        id="RE_203", fitxer="RE_203_campanya_banc.ipynb", bloc=2, dif=3,
        titol="A qui truquem?",
        encarrec="""Ets analista al departament de màrqueting d'un banc. La propera campanya ofereix un **dipòsit a
termini** per telèfon. Cada trucada costa temps i diners, i la majoria de clients diuen que no. La
directora vol una llista de clients a qui trucar.""",
        pregunta="""un model pot triar a qui trucar millor que l'atzar? Amb quina mesura s'ha de jutjar, i on poses
el llindar per decidir si truques o no?""",
        font="""- **Font:** *Bank Marketing* (Moro, Cortez i Rita, 2014; UCI), a OpenML amb `data_id=46910`.
  Llicència CC BY 4.0.
- **Cada fila** és **un client** d'un banc portuguès contactat en una campanya telefònica
  (2008-2010): 45.211 files i 14 columnes. No hi ha cap identificador de persona.
- Aquesta versió **ja no porta** la durada de la trucada, que en la versió original revelava el
  resultat (no se sap quant durarà una trucada abans de fer-la).
- Documentació: <https://archive.ics.uci.edu/dataset/222/bank+marketing>""",
        diccionari=[
            ("SubscribeTermDeposit", "**objectiu**: si el client va contractar el dipòsit (`yes` / `no`)"),
            ("age", "edat"),
            ("job", "tipus de feina (`admin.`, `blue-collar`, `management`, `student`...; `unknown` si no consta)"),
            ("marital", "estat civil: `married`, `single`, `divorced` (inclou vidus)"),
            ("education", "estudis: `primary`, `secondary`, `tertiary`, `unknown`"),
            ("default", "si té crèdits impagats"),
            ("balance", "saldo mitjà anual, en euros (pot ser negatiu)"),
            ("housing, loan", "si té hipoteca i si té un préstec personal"),
            ("contact", "com se'l contacta: `cellular`, `telephone`, `unknown`"),
            ("campaign", "nombre de contactes amb aquest client durant aquesta campanya (inclou l'últim)"),
            ("pdays", "dies passats des de l'últim contacte d'una campanya anterior; `-1` vol dir que no se l'havia contactat"),
            ("previous", "nombre de contactes amb aquest client abans d'aquesta campanya"),
            ("poutcome", "resultat de la campanya anterior: `success`, `failure`, `other`, `unknown`"),
        ],
        recollida="""- Són les trucades reals d'un banc portuguès. Un mateix client podia rebre diverses trucades
  durant la campanya; aquí n'hi ha una fila amb el resultat final.
- `unknown` apareix a diverses columnes de text, però no vol dir el mateix a totes.""",
        investigar="""Prepara la recomanació per a la directora. Comença per la línia de base: què fa un model que no
truca mai, segons la precisió, la *precision* i el *recall*? Entrena una **regressió logística** i
un **bosc aleatori** amb un `ColumnTransformer` i compara'ls. Decideix amb quina mesura els
jutges, i explica per què la precisió no serveix.

La teoria ha d'aterrar al codi: escriu una funció que, a partir **només** de les quatre caselles
d'una matriu de confusió, calculi *accuracy*, *precision*, *recall* i F1, i comprova-les contra
scikit-learn. Després, el negoci: suposa que cada trucada costa **5 €** i cada client que contracta
en deixa **50 €** de marge. Per a cada llindar, quantes trucades faries i quin benefici tindries?
Quin llindar triaries? Acaba comparant la corba ROC i la corba *precision-recall*: quina explica
millor aquest problema?""",
        obertes=[
            "`class_weight=\"balanced\"` i baixar el llindar: són dues maneres de fer el mateix?",
            "Què vol dir `pdays = -1` per al model? Si ho tractes d'una altra manera, canvia res?",
            "Si canvies els costos de l'escenari, has de tornar a entrenar el model?",
        ],
        pistes=[
            "Si dos models empaten amb el llindar per defecte, potser el llindar per defecte no és el bo per comparar-los.",
            "El millor F1 i el millor benefici no tenen per què sortir al mateix llindar.",
        ],
        exemples=[
            f"{EX02}, exercicis 5-7: moure el llindar de decisió.",
            f"{EX00} §6 (`ColumnTransformer`) i §7 (matriu de confusió, *precision*, *recall*, F1 i `DummyClassifier`).",
            f"{ML03} (boscos) i {ML04} (`predict_proba`).",
        ],
        xavi=[
            "Quin model guanya? Em surt un a cada mesura.",
            "Puc fer servir el test per triar el llindar?",
        ],
    ),
    dict(
        id="RE_204", fitxer="RE_204_formigo.ipynb", bloc=2, dif=2,
        titol="Formigó: memoritzar no és aprendre",
        encarrec="""Treballes al laboratori d'una planta de formigó. Per saber si una barreja aguanta, es fa una proveta
i es trenca a la premsa quan té 28 dies (o 7, o 90...). Això vol dir **esperar setmanes**. El cap de
laboratori et pregunta si es pot **predir la resistència** (en MPa) a partir de la recepta i
l'edat. És un problema de **regressió**: es prediu un número, no una classe.""",
        pregunta="""quin error real pots prometre al laboratori, i com saps que no t'estàs enganyant?""",
        font="""- **Font:** *Concrete Compressive Strength* (I-C. Yeh, 1998; UCI), a OpenML amb `data_id=44959`.
  Llicència CC BY 4.0.
- **Cada fila** és **una proveta de formigó**: 1.030 files i 9 columnes, totes numèriques.
- Documentació: <https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength>""",
        diccionari=[
            ("strength", "**objectiu**: resistència a compressió, en megapascals (MPa)"),
            ("cement", "ciment, en kg per m³ de barreja"),
            ("blast_furnace_slag", "escòria d'alt forn, kg/m³"),
            ("fly_ash", "cendres volants, kg/m³"),
            ("water", "aigua, kg/m³"),
            ("superplasticizer", "superplastificant (additiu que fa la barreja més fluida amb menys aigua), kg/m³"),
            ("coarse_aggregate", "àrid gros (grava), kg/m³"),
            ("fine_aggregate", "àrid fi (sorra), kg/m³"),
            ("age", "edat de la proveta quan es va trencar, en dies"),
        ],
        recollida="""- Són assajos de laboratori reals, recollits de diversos estudis. Les edats són les dels assajos
  habituals (3, 7, 28, 90 dies...), no qualsevol número.
- Dues provetes fetes amb la mateixa recepta no donen mai exactament la mateixa resistència.""",
        investigar="""Dona-li al cap de laboratori un número i la manera de defensar-lo. Explora les unitats i els rangs
de cada columna i quines van més amb la resistència. Entrena un **kNN** amb i sense escalar i
compara'n l'error absolut mitjà (MAE). Entrena **arbres** de profunditat creixent i dibuixa l'error
d'entrenament i el de test: a partir de quan l'arbre comença a **memoritzar**? Tria la profunditat
de l'arbre i la `k` del kNN **sense mirar el test** (validació creuada) i dona l'error real del
model triat.

La teoria ha d'aterrar al codi: fes **a mà** una predicció de kNN (distàncies a totes les provetes
d'entrenament, els 5 veïns, la mitjana) i comprova-la contra `predict` i `kneighbors`. Implementa
el MAE i el $R^2$ amb NumPy i comprova'ls amb scikit-learn. Què vol dir un $R^2$ de 0, i un de
negatiu?""",
        obertes=[
            "Al kNN sense escalar, quina columna mana a la distància? Prova d'escalar-les totes menys una, cada vegada una de diferent.",
            "I una recta? Els seus coeficients quadren amb el que diria un enginyer? Per què perd contra l'arbre?",
        ],
        pistes=[
            "Si el resultat no és el que esperaves (per exemple, que escalar gairebé no canviï res), no forcis la conclusió: busca per què.",
            "Mira el gràfic de la resistència contra l'edat. La forma d'aquesta relació explica molt de la resta del repte.",
        ],
        exemples=[
            f"{ML01} §3, §4 i §6 i {EX01}, exercicis 3-4: k veïns i el parany de les escales.",
            f"{ML02} §6 i {EX04}, exercici 4: fins on fer créixer un arbre.",
            f"{EX00} §2 (`StandardScaler`) i §9 (`cross_val_score` i `GridSearchCV`).",
            "La regressió és nova: els models es diuen igual però acaben en `Regressor`, i en lloc de la matriu de confusió es mesura quant s'equivoca de mitjana.",
        ],
        xavi=[
            "L'arbre sense límit dona el millor test. Llavors el sobreajust no és dolent?",
            "Per què la validació creuada i el test no donen el mateix número?",
        ],
    ),
    dict(
        id="RE_205", fitxer="RE_205_bicis.ipynb", bloc=2, dif=2,
        titol="Quantes bicis caldran a les 8?",
        encarrec="""Treballes per a un servei de bicicleta compartida, com el Bicing. Cada nit, l'equip de logística
redistribueix les bicis entre estacions, i per fer-ho bé necessita saber **quantes se'n llogaran cada
hora del dia següent**. Tens dos anys d'històric amb el temps que feia i el tipus de dia.""",
        pregunta="""quin model preveu millor els lloguers per hora, i com l'has d'avaluar perquè l'error que
prometis sigui el que hi haurà l'any que ve?""",
        font="""- **Font:** *Bike Sharing* (Fanaee-T i Gama, 2013; UCI), a OpenML amb `data_id=42712`. Llicència
  CC BY 4.0. Dades del sistema Capital Bikeshare de **Washington DC**, 2011 i 2012.
- **Cada fila** és **una hora**: 17.379 files i 13 columnes.
- Documentació: <https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset>""",
        diccionari=[
            ("count", "**objectiu**: bicis llogades en aquella hora"),
            ("season", "estació de l'any: `spring`, `summer`, `fall`, `winter`"),
            ("year", "any: 0 = 2011, 1 = 2012"),
            ("month", "mes (1-12)"),
            ("hour", "hora del dia (0-23)"),
            ("holiday", "si és festiu"),
            ("weekday", "dia de la setmana (0 = diumenge ... 6 = dissabte)"),
            ("workingday", "si és laborable (ni cap de setmana ni festiu)"),
            ("weather", "temps: `clear`, `misty` (boira o núvols), `rain` (pluja o neu lleugeres), `heavy_rain` (pluja forta, tempesta)"),
            ("temp, feel_temp", "temperatura real i sensació tèrmica, en °C"),
            ("humidity", "humitat relativa, de 0 a 1"),
            ("windspeed", "velocitat del vent"),
        ],
        recollida="""- El sistema registra cada lloguer; aquí estan sumats per hora i creuats amb el temps de l'hora i el
  calendari de festius de Washington.
- Una hora sense cap lloguer no té fila.""",
        investigar="""Prepara la previsió per a logística. Mira primer la forma del dia: com són els lloguers per hora
en un laborable i en un festiu, i què et diu sobre qui fa servir les bicis. Parteix les dades
**pel temps** (entrenament 2011, test 2012), perquè el model s'ha de fer servir l'any que ve, i
compara models: una **recta** amb l'hora com a número, la recta amb l'hora en one-hot, i un
**bosc**. Quin aprofita millor l'hora, i per què?

La teoria ha d'aterrar al codi: comprova que `predict` de la recta és exactament $Xw + b$
calculant-ho tu amb la matriu transformada; implementa el MAE i l'RMSE i comprova'ls amb
scikit-learn. Després, entrena el mateix bosc amb una partició **aleatòria** i compara l'error amb
el de la temporal. Quin número posaries a l'informe? Acaba mirant on s'equivoca el model: l'error
té signe? Varia per mesos?""",
        obertes=[
            "Escriu l'hora com a dues columnes, $\\sin(2\\pi h/24)$ i $\\cos(2\\pi h/24)$. Millora la recta? Per què no arriba al one-hot?",
            "Una columna que combini laborable i hora (per exemple, `\"1_8\"`): quant s'acosta la recta al bosc?",
        ],
        pistes=[
            "Si una partició et dona la meitat d'error que l'altra, pregunta't quina de les dues s'assembla a com es farà servir el model.",
            "Un error que té sempre el mateix signe no és soroll: és una cosa que el model no sap.",
        ],
        exemples=[
            f"{MA01} §7 (un model lineal és un vector i una multiplicació) i {MA02} §3-§4 (minimitzar un error).",
            f"{ML02} i {ML03}: arbres i boscos.",
            f"{EX00} §1 (`train_test_split` i el seu parany), §4 i §6 (`OneHotEncoder` i `ColumnTransformer`).",
            "MAE i $R^2$: si no has fet el RE_204, mira'n l'enunciat.",
        ],
        xavi=[
            "La partició aleatòria em dona molt millor resultat. Per què no la faig servir?",
            "El model es queda curt sempre. Ho puc corregir, o és trampa?",
        ],
    ),
    dict(
        id="RE_206", fitxer="RE_206_equitat_adult.ipynb", bloc=2, dif=3,
        titol="És just el model?",
        encarrec="""Treballes en una consultora que **audita algorismes**. Un banc vol fer servir un model per
**preaprovar** una targeta *premium* a les persones que guanyen més de 50.000 $ l'any, i abans
d'engegar-lo ha de demostrar que el model no discrimina. T'han passat les dades del cens amb què
l'entrenarien. Aquest repte no té una resposta tècnica única: hi ha números que has de calcular
bé, i decisions que has de **justificar**.""",
        pregunta="""el model encerta i s'equivoca igual per a dones i homes, i per als diferents grups? I si
traiem `sex` i `race` de les dades, el problema desapareix?""",
        font="""- **Font:** *Adult / Census Income* (Becker i Kohavi, 1996; UCI), a OpenML amb `data_id=1590`.
  Llicència CC BY 4.0.
- **Cada fila** és **una persona** del cens dels Estats Units de 1994 (anonimitzada): 48.842 files i
  15 columnes.
- Documentació: <https://archive.ics.uci.edu/dataset/2/adult>""",
        diccionari=[
            ("class", "**objectiu**: si guanyava més de 50.000 $ l'any (`>50K` / `<=50K`)"),
            ("age", "edat"),
            ("workclass", "tipus d'ocupador (privat, administració, autònom...)"),
            ("fnlwgt", "número que calcula l'oficina del cens. Llegeix a la documentació què és abans de decidir si entra al model"),
            ("education, education-num", "nivell d'estudis, en text i en número"),
            ("marital-status", "estat civil"),
            ("occupation", "ocupació"),
            ("relationship", "relació dins de la llar (`Husband`, `Wife`, `Own-child`, `Not-in-family`...)"),
            ("race", "grup ètnic, amb les categories del cens americà"),
            ("sex", "sexe (`Male` / `Female`)"),
            ("capital-gain, capital-loss", "guanys i pèrdues de capital, en dòlars"),
            ("hours-per-week", "hores de feina setmanals"),
            ("native-country", "país d'origen"),
        ],
        recollida="""- Les dades són del 1994 i dels Estats Units. Les categories de `race` i les de `relationship` són
  les del formulari del cens, no les que faríem servir avui.
- Alguns grups tenen molt poques persones.""",
        investigar="""Fes l'auditoria. Abans de cap model, mira si les dades ja són desiguals (proporció de `>50K` per
sexe i per grup, i quanta gent hi ha a cada grup). Decideix quines columnes entren al model i per
què. Entrena el model que s'auditarà (una **regressió logística** dins d'un `Pipeline`), i
compara'n la precisió global amb la d'un `DummyClassifier`.

La teoria ha d'aterrar al codi: escriu una funció que, per a cada grup d'una columna, calculi
**des de la seva matriu de confusió** el nombre de persones, la precisió, la **taxa de selecció**,
la **TPR** i la **FPR**, i comprova la TPR de cada grup amb `recall_score`. Aplica-la per sexe i
per grup ètnic. Després, torna a entrenar **sense** `sex` ni `race` i repeteix l'auditoria: la
diferència desapareix?""",
        obertes=[
            "Es pot predir el sexe a partir de les altres columnes? Què vol dir això per a la pregunta de treure `sex`?",
            "Un llindar diferent per a cada grup que iguali la TPR: quant canvia la precisió global? És una solució justa? Qui hi guanya i qui hi perd?",
            "`capital-gain` té un valor que es repeteix molt al màxim. Què és? I unes dades del 1994, serveixen avui?",
        ],
        pistes=[
            "Una precisió més alta en un grup no vol dir que el model el tracti millor: mira quina proporció de les persones que sí que guanyen més de 50K troba en cada grup.",
            "Treure una columna no treu la informació si altres columnes la porten a dins.",
            "Una mesura calculada sobre una dotzena de persones es mou molt amb un sol cas: posa la mida del grup al costat de cada número.",
        ],
        exemples=[
            f"{EX00} §3, §4 i §6 (nuls, `SimpleImputer`, `OneHotEncoder`, `ColumnTransformer`) i §7 (matriu de confusió, *recall*, `DummyClassifier`).",
            f"{ML04} i el RE_202: els pesos d'una regressió logística.",
            f"{EX02}, exercici 7, i el RE_203: el llindar de decisió.",
        ],
        xavi=[
            "Quina mesura d'equitat és la bona: la mateixa taxa de selecció, la mateixa TPR, o totes dues?",
            "Com escric això en un informe sense que sembli una acusació ni un rentat de cara?",
        ],
        lliurament_extra="Escriu la conclusió com si fos el **paràgraf final de l'informe d'auditoria** per al banc: què has mesurat, què has trobat, i què recomanes.",
    ),
    # ======================================================================== BLOC 3
    dict(
        id="RE_301", fitxer="RE_301_cotxes_preu.ipynb", bloc=3, dif=2,
        titol="Quant val aquest cotxe?",
        encarrec="""Treballes per a una empresa que importa **cotxes de col·lecció dels anys 80**. Cada cop que arriba
una oferta, algú ha de mirar-se la fitxa tècnica i dir un preu. El cap vol una estimació
automàtica.""",
        pregunta="""amb quin error, en dòlars, es pot estimar el preu d'un cotxe a partir de la seva fitxa? I aquest
número, és un número en què es pugui confiar?""",
        font="""- **Font:** *Automobile / imports-85* (J. Schlimmer, 1987; UCI Machine Learning Repository).
  Llicència CC BY 4.0.
- **Cada fila** és **un model de cotxe del 1985**: 205 files i 26 columnes.
- El fitxer **no té capçalera**: els noms de la cel·la de càrrega són els del fitxer de descripció,
  <https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.names>. Llegeix-lo:
  el necessitaràs.""",
        diccionari=[
            ("price", "**objectiu**: preu, en dòlars"),
            ("symboling", "risc segons l'assegurança, de −3 (segur) a +3 (arriscat)"),
            ("normalized-losses", "pèrdues mitjanes relatives per vehicle assegurat i any (dada de l'assegurança)"),
            ("make", "marca"),
            ("fuel-type, aspiration", "combustible (`gas` / `diesel`) i aspiració (`std` / `turbo`)"),
            ("num-of-doors, num-of-cylinders", "portes i cilindres, **escrits amb paraules** (`two`, `four`...)"),
            ("body-style", "carrosseria (`sedan`, `hatchback`, `wagon`, `convertible`, `hardtop`)"),
            ("drive-wheels, engine-location", "tracció (`fwd`, `rwd`, `4wd`) i posició del motor"),
            ("wheel-base, length, width, height", "batalla i mides, en polzades"),
            ("curb-weight", "pes en buit, en lliures"),
            ("engine-type, fuel-system", "tipus de motor i sistema d'alimentació"),
            ("engine-size, bore, stroke, compression-ratio", "cilindrada (polzades cúbiques), diàmetre i carrera del cilindre, relació de compressió"),
            ("horsepower, peak-rpm", "potència (CV) i revolucions de potència màxima"),
            ("city-mpg, highway-mpg", "consum en milles per galó, a ciutat i a carretera"),
        ],
        recollida="""- Es va fer el 1985 combinant tres fonts: les especificacions dels fabricants, un manual de
  l'assegurança i un informe de pèrdues de les asseguradores.
- Pandas i el fitxer `.names` no diuen el mateix sobre els valors que falten.""",
        investigar="""Dona-li al cap el número que demana, i que el número sigui honest. Mira què diu pandas de cada
columna i compara-ho amb el fitxer de descripció. Fes l'inventari dels forats, decideix què fas
amb cada un (també amb els cotxes que no tenen preu, que és l'objectiu) i escriu per què.

Munta un `Pipeline` que faci **tota** la preparació (omplir nuls, codificar el text) i el model, i
avalua'l amb **validació creuada** contra una referència que sempre diu el preu mitjà. Prova com a
mínim dos models. Quin error dones al cap, en dòlars i relatiu al preu típic? Quant varia d'un
tros de validació a un altre? I si mesures l'error sobre les mateixes dades d'entrenament, quin
número surt, i per què no és el que has de donar?""",
        obertes=[
            "Les columnes que són números escrits amb paraules: si les converteixes a número, millora alguna cosa?",
            "El model s'equivoca més en cotxes barats o cars? Prova d'entrenar sobre el logaritme del preu.",
            "Planteja't una pregunta sobre aquestes dades i respon-la.",
        ],
        pistes=[
            "Si `cross_val_score` et dona algun `nan`, llegeix l'avís sencer: et diu què ha trobat en un tros de validació que no havia vist en entrenar.",
            "Un error d'entrenament gairebé zero no és una bona notícia.",
        ],
        exemples=[
            f"{EX05}: un `Pipeline` amb dades brutes de cap a peus.",
            f"{EX00} §3 (valors que falten), §4 (text), §6 (`Pipeline` i `ColumnTransformer`) i §9 (validació creuada).",
            f"{FO02} §6: valors que falten.",
        ],
        xavi=[
            "Aquesta columna amb tants forats, la tiro o la imputo?",
            "L'error em canvia molt d'un tros a l'altre: quin número dono?",
        ],
    ),
    dict(
        id="RE_302", fitxer="RE_302_accidents_dos_anys.ipynb", bloc=3, dif=2,
        titol="El 2024 va ser pitjor?",
        encarrec="""Treballes a l'àrea de Mobilitat de l'Ajuntament de Barcelona. La regidora ha de presentar el
balanç de sinistralitat. Tens els dos fitxers que publica la Guàrdia Urbana, un per any, amb les
mateixes columnes, i has de lliurar **una sola taula amb els dos anys** i la comparació.""",
        pregunta="""comparat amb el 2023, el 2024 els accidents van ser més greus? La regidora vol el nombre de
**morts** i de **ferits greus per cada 1.000 accidents**, per a tota la ciutat i per districte.""",
        font="""- **Font:** *Accidents gestionats per la Guàrdia Urbana a Barcelona*, fitxers de 2023 i 2024 (Open
  Data BCN, conjunt `accidents-gu-bcn`). Llicència CC BY 4.0, font: Ajuntament de Barcelona.
- **Còpia:** són dades vives; en fem servir una **còpia congelada** (baixada el 14-oct-2026) que és
  al repositori del curs.
- **Cada fila** és **un accident**: unes 7.700 files el 2023 i 7.500 el 2024, amb les mateixes 25
  columnes.""",
        diccionari=DIC_ACCIDENTS,
        recollida="""- Cada any el publica el mateix servei, però el fitxer el genera qui toca aquell any, i ningú no
  garanteix que el format sigui idèntic: tipus, manera d'escriure els buits, noms, espais...
- Els morts i ferits greus són pocs: en un districte, un sol cas mou molt una taxa.""",
        investigar="""Prepara la taula i la resposta per a la regidora. Abans d'ajuntar res, compara els dos fitxers
columna per columna: tipus, valors que falten, noms de llocs, codis especials. Fes primer la
**resposta ràpida** (ajunta-ho tal com ve i calcula morts i ferits greus per accident de cada any)
i apunta-la. Després escriu **una funció de neteja** que deixi qualsevol dels dos anys en un format
comú (no arreglis un any a mà), comprova'n les propietats amb `assert`, i assegura't que cada
accident surt una sola vegada.

Amb les dades netes, calcula per a cada any i cada districte: accidents, morts, ferits greus, i
morts i ferits greus per cada 1.000 accidents. Decideix què fas amb els accidents sense districte
conegut i digues-ho. Respon la regidora i compara-ho amb la resposta ràpida.""",
        obertes=[
            "Dibuixa els accidents per longitud i latitud, un color per any. Les columnes UTM diuen el mateix els dos anys?",
            "Busca alguna altra diferència entre els fitxers (per exemple, el número postal), afegeix-la a la neteja i torna a comprovar-ho tot.",
        ],
        pistes=[
            "Si la resposta ràpida et dona un número absurd, no l'arreglis a ull: busca quina diferència entre els fitxers el provoca.",
            "Netejar no ha de crear ni fer desaparèixer cap mort: compara els totals abans i després.",
            "Un nul pot voler dir «zero» o «no se sap». Mira com escriu cada any un accident sense víctimes d'un tipus.",
        ],
        exemples=[
            f"{FO02} §4-§8: seleccionar, filtrar, `groupby` i `pivot_table`.",
            f"{EX00} §3 i §5: valors que falten i duplicats.",
            f"{EX05}, exercici 1: el diagnòstic d'una taula bruta.",
            "Si has fet el RE_101, ja coneixes el fitxer del 2024.",
        ],
        xavi=[
            "Un nul aquí vol dir «zero» o «no se sap»? Com ho puc saber del cert?",
            "Els números de districte canvien molt però són pocs casos: ho puc dir igualment?",
        ],
    ),
    dict(
        id="RE_303", fitxer="RE_303_hotels_cancellacions.ipynb", bloc=3, dif=2,
        titol="Es cancel·larà aquesta reserva?",
        encarrec="""Ets la persona de dades d'una petita cadena amb **dos hotels a Portugal**, un de ciutat i un de
platja. Una de cada tres reserves acaba cancel·lada, i la direcció vol fer *overbooking* amb cap:
quan entra una reserva nova, saber si és probable que es cancel·li.""",
        pregunta="""quin encert (*accuracy*) es pot prometre a la direcció, amb un model que funcioni **el dia que
entra la reserva**? Han de poder-se'l creure, perquè hi posaran clients al carrer si s'equivoca.""",
        font="""- **Font:** *Hotel booking demand* (N. Antonio, A. de Almeida i L. Nunes, *Data in Brief*, 2019), via
  TidyTuesday (2020-02-11). Llicència CC BY 4.0.
- **Cada fila** és **una reserva** amb arribada prevista entre juliol del 2015 i agost del 2017:
  119.390 files i 32 columnes. No hi ha noms ni contactes.
- Diccionari original: <https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-02-11>""",
        diccionari=[
            ("is_canceled", "**objectiu**: 1 si la reserva es va cancel·lar, 0 si no"),
            ("hotel", "`City Hotel` o `Resort Hotel`"),
            ("lead_time", "dies entre que es fa la reserva i el dia d'arribada"),
            ("arrival_date_year, arrival_date_month, arrival_date_week_number, arrival_date_day_of_month", "data d'arribada prevista, partida en quatre columnes"),
            ("stays_in_weekend_nights, stays_in_week_nights", "nits de cap de setmana i nits entre setmana reservades"),
            ("adults, children, babies", "persones de la reserva"),
            ("meal", "règim: `BB` allotjament i esmorzar, `HB` mitja pensió, `FB` pensió completa; mira al diccionari què volen dir `SC` i `Undefined`"),
            ("country", "país d'origen (codi ISO de tres lletres)"),
            ("market_segment, distribution_channel", "segment de mercat i canal de venda (`TA` = agència de viatges, `TO` = operador turístic)"),
            ("is_repeated_guest", "si el client ja havia estat a l'hotel"),
            ("previous_cancellations, previous_bookings_not_canceled", "reserves anteriors del client cancel·lades i no cancel·lades"),
            ("reserved_room_type, assigned_room_type", "tipus d'habitació reservada i tipus d'habitació assignada (codis)"),
            ("booking_changes", "nombre de canvis fets a la reserva des que es va registrar fins a l'arribada o la cancel·lació"),
            ("deposit_type", "dipòsit: `No Deposit`, `Refundable`, `Non Refund`"),
            ("agent, company", "identificador de l'agència i de l'empresa que paga (números)"),
            ("days_in_waiting_list", "dies en llista d'espera abans de confirmar-la"),
            ("customer_type", "`Transient`, `Contract`, `Group`, `Transient-Party`"),
            ("adr", "*average daily rate*: preu mitjà per nit, en euros"),
            ("required_car_parking_spaces, total_of_special_requests", "places d'aparcament i peticions especials"),
            ("reservation_status", "últim estat de la reserva: `Check-Out`, `Canceled` o `No-Show`"),
            ("reservation_status_date", "data de l'últim estat"),
        ],
        recollida="""- Les dades surten directament del programa de gestió dels dos hotels. Els autors en van treure
  tot el que identificava clients i reserves.
- Algunes columnes reflecteixen el que es coneix **al final** de la història d'una reserva, no el dia
  que entra. El diccionari ho diu per a cada una: llegeix-lo amb aquesta pregunta al cap.""",
        investigar="""Dona a la direcció un número que es pugui creure. Fixa primer la referència: quina *accuracy* té
un model que diu sempre la classe més freqüent? Entrena un primer model **sense pensar** (totes les
columnes, un arbre de profunditat 3 dins d'un `Pipeline` amb imputació i one-hot) i mira què
surt. Després fes la pregunta columna per columna: **aquest valor, el sé el dia que entra la
reserva?** Treu les que no, comprova cada sospita amb una taula creuada contra l'objectiu, i torna
a entrenar.

Mira també les files repetides: quantes n'hi ha, què poden ser, i quantes files del test tenen una
còpia exacta a l'entrenament. Compara un bosc aleatori amb duplicats i sense. Amb totes les
decisions preses, dona el número final al costat de la seva referència.""",
        obertes=[
            "Entrena amb les arribades del 2015 i el 2016 i avalua amb les del 2017. Quina *accuracy* surt? Quina partició és més honesta per a l'encàrrec?",
            "Hi ha valors sense sentit a `adr` o a `adults`, o categories de `meal` que volen dir el mateix? Canvia res si les arregles?",
        ],
        pistes=[
            "Si el model et surt gairebé perfecte, no ho celebris: busca quina columna li està dient la resposta, i pregunta't si la sabries el dia que entra la reserva.",
            "Si el test té files idèntiques a les de l'entrenament, el model no les ha de predir: les recorda.",
        ],
        exemples=[
            f"{EX00} §1 i §2 (partir les dades i la fuita d'informació), §3-§5 (nuls, text i duplicats), §6 i §7 (`Pipeline`, `DummyClassifier`) i §8 (importància de les columnes).",
            f"{EX05}: dades brutes de cap a peus.",
            f"{ML02}: llegir quines columnes fa servir un arbre.",
        ],
        xavi=[
            "He tret una columna que potser sí que es coneix el dia de la reserva: m'he passat?",
            "El model és pitjor ara que abans. He fet alguna cosa malament?",
        ],
    ),
    dict(
        id="RE_304", fitxer="RE_304_certificats_energetics.ipynb", bloc=3, dif=3,
        titol="Quina lletra traurà el meu pis?",
        encarrec="""Treballes en una empresa petita de rehabilitació energètica. Volen posar a la web una calculadora:
el propietari hi entra les dades del seu habitatge **que pot saber sense contractar cap tècnic**
(població, zona climàtica, any de construcció, metres, tipus d'edifici...) i la calculadora li diu
quina **lletra de consum** (de la A a la G) és probable que tregui al certificat energètic. És el
repte més complet del bloc: aquí ningú no et dirà què està brut.""",
        pregunta="""quin F1 *macro* es pot prometre, honestament, amb només aquestes dades? I on s'equivoca?""",
        font="""- **Font:** *Certificats d'eficiència energètica d'edificis* (Institut Català d'Energia, conjunt
  `j6ii-t3w2` de Dades Obertes de la Generalitat). Llicència oberta d'ús d'informació – Catalunya.
- **Còpia:** el conjunt sencer té més d'un milió de certificats; aquí en tens una **mostra aleatòria
  de 30.000**, congelada al repositori el 14-oct-2026, i **sense cap adreça** (ni carrer, ni número,
  ni referència cadastral, ni coordenades).
- **Cada fila** és **un certificat energètic** d'un habitatge o local: 30.000 files i 29 columnes.
- Descripció de les columnes al portal: <https://analisi.transparenciacatalunya.cat/d/j6ii-t3w2>""",
        diccionari=[
            ("qualificaci_de_consum_d", "**objectiu**: lletra de consum d'energia primària no renovable, de la A (millor) a la G (pitjor). Sí, el nom està tallat"),
            ("codi_postal, poblacio, comarca, nom_provincia", "on és l'immoble"),
            ("zona_climatica", "zona climàtica del Codi Tècnic de l'Edificació (lletra d'hivern A-E i número d'estiu 1-4: `C2`, `D3`...)"),
            ("metres_cadastre", "superfície segons el cadastre, en m²"),
            ("any_construccio", "any de construcció"),
            ("us_edifici", "ús: habitatge unifamiliar, bloc plurifamiliar, habitatge en bloc, terciari..."),
            ("normativa_construcci", "normativa tèrmica vigent quan es va construir (`Abans de 1979`, `NBE-CT-79`, `CTE 2006`...)"),
            ("energia_prim_ria_no_renovable", "energia primària no renovable que calcula el certificat (kWh/m² any)"),
            ("consum_d_energia_final", "energia final que calcula el certificat (kWh/m² any)"),
            ("emissions_de_co2, qualificacio_d_emissions", "emissions de CO₂ que calcula el certificat (kg/m² any) i la seva lletra"),
            ("cost_anual_aproximat_d_energia", "cost anual aproximat de l'energia, segons el certificat"),
            ("valor_aillaments, valor_finestres", "valors que el tècnic assigna a l'envolupant (aïllaments) i a les obertures (finestres)"),
            ("vehicle_electric, solar_termica, solar_fotovoltaica, sistema_biomassa, xarxa_districte, energia_geotermica", "si té cada instal·lació (`SI` / `NO`)"),
            ("ventilacio_us_residencial", "ventilació, en renovacions d'aire per hora"),
            ("eina_de_certificacio", "programa amb què el tècnic ha fet el certificat (`CE3X`, `HULC`...)"),
            ("motiu_de_la_certificacio", "per què es fa el certificat (compravenda, lloguer, obra nova...)"),
            ("tipus_tramit, rehabilitacio_energetica", "tipus de tràmit i si hi ha hagut rehabilitació energètica"),
            ("data_entrada", "data en què es va registrar el certificat"),
        ],
        recollida="""- El certificat el fa un tècnic, amb un programa homologat, a partir de l'immoble i de càlculs
  propis. Després es registra a l'ICAEN. Algunes columnes són **dades de l'immoble** i altres són
  **resultats del càlcul** del tècnic.
- Els formularis han canviat amb els anys i els han omplert milers de persones diferents, en
  català i en castellà.""",
        investigar="""Dona el número que es pot prometre, i explica on s'equivoca la calculadora. Comença per les
referències: quin F1 *macro* té un model que diu sempre la lletra més freqüent, i un que les diu a
l'atzar respectant les proporcions? Entrena un primer model **amb tot** i mira què surt. Després
torna a l'encàrrec: el propietari **no té** el certificat. Fes la llista de columnes que surten
del càlcul del certificat, comprova cada sospita mirant com es reparteix aquella columna dins de
cada lletra, i treu-les.

Revisa les columnes de text (quantes categories **reals** hi ha, si les llegeixes com una
persona?) i els números (quins valors són impossibles?), i posa tota aquesta neteja **dins** del
`Pipeline`, perquè la calculadora rebrà dades tal com les escriu la gent. Avalua amb validació
creuada estratificada, i acaba amb la matriu de confusió: quan s'equivoca, s'equivoca per una
lletra o per moltes?""",
        obertes=[
            "Un error de B per C hauria de comptar menys que un de A per G. Inventa una mètrica que ho tingui en compte i compara models amb ella.",
            "Les columnes `SI`/`NO` tenen buits. Vol dir «no» o «no consta»? Canvia res si el tractes com una categoria?",
            "Puc fer servir la població o el codi postal, o és massa detall?",
        ],
        pistes=[
            "Per a cada columna, pregunta't qui la coneix: el propietari, o el tècnic que fa el certificat?",
            "Que la neteja no mogui gaire el número no vol dir que no calgui: pregunta't per a què serveix dins de la calculadora.",
        ],
        exemples=[
            f"{EX05}: un `Pipeline` amb dades brutes de cap a peus.",
            f"{EX00} §3-§9: nuls, text, duplicats, `Pipeline`, mètriques i validació creuada.",
            "Si has fet el RE_303, la pregunta «aquesta columna la tindré?» és la mateixa.",
        ],
        xavi=[
            "Aquesta columna la pot saber el propietari o no?",
            "El F1 honest em surt baix: el model és dolent o les dades no donen per a més?",
        ],
    ),
    # ======================================================================== BLOC 4
    dict(
        id="RE_401", fitxer="RE_401_clients_majorista.ipynb", bloc=4, dif=1,
        titol="Quins tipus de clients tenim?",
        encarrec="""Treballes per a un distribuïdor d'alimentació de Portugal amb 440 clients (restaurants, hotels,
botigues...). Màrqueting vol fer ofertes diferents per a cada tipus de client, però **no té cap
etiqueta**: només sap quant gasta cada client en sis famílies de productes.""",
        pregunta="""quants grups de clients hi ha, i com els descriuries amb paraules? Han de ser grups que
màrqueting pugui fer servir.""",
        font="""- **Font:** *Wholesale customers* (M. G. M. S. Cardoso, UCI Machine Learning Repository, 2014).
  Llicència CC BY 4.0.
- **Cada fila** és **un client** del majorista: 440 files i 8 columnes, totes enteres, sense buits.""",
        diccionari=[
            ("Fresh", "despesa anual en productes frescos (unitats monetàries)"),
            ("Milk", "despesa anual en làctics"),
            ("Grocery", "despesa anual en ultramarins (alimentació envasada)"),
            ("Frozen", "despesa anual en congelats"),
            ("Detergents_Paper", "despesa anual en detergents i paper"),
            ("Delicassen", "despesa anual en delicatessen (xarcuteria, formatges...)"),
            ("Channel", "canal: 1 = hoteleria i restauració (*Horeca*), 2 = comerç al detall. **No la facis servir per agrupar**"),
            ("Region", "regió: 1 = Lisboa, 2 = Porto, 3 = altres. **Tampoc per agrupar**"),
        ],
        recollida="""- És la facturació d'un any de clients reals d'un majorista portuguès.
- `Channel` i `Region` són les úniques etiquetes que hi ha. Es guarden per comprovar **després** si
  els grups que trobis tenen sentit, no per fer-los.""",
        investigar="""Proposa a màrqueting uns quants tipus de clients. Mira primer com és cada distribució de
despesa (mitjana, mediana, màxim, histograma) i decideix com prepares les dades per mesurar
distàncies entre clients: tal com venen, estandarditzades, o amb un logaritme abans. Per a cada
preparació, fes **k-means** amb k de 2 a 8 i compara la inèrcia, la silueta i la mida dels grups.
Tria una preparació i una k, i justifica-ho amb més d'un criteri.

La teoria ha d'aterrar al codi: estandarditza **a mà** amb NumPy i comprova-ho contra
`StandardScaler`; calcula **a mà** la inèrcia d'un model a partir de les etiquetes i els centres,
i comprova-la contra `inertia_`. Acaba descrivint cada grup amb paraules teves, a partir de la
seva despesa típica en unitats originals, i només aleshores compara els grups amb `Channel`.""",
        obertes=[
            "Projecta els clients a dues dimensions amb PCA i pinta'ls pel teu grup i, al costat, per `Channel`.",
            "Torna a fer k-means amb cinc `random_state` diferents. Els grups canvien? Com ho mesuraries, si el número del grup no vol dir res?",
        ],
        pistes=[
            "Una silueta alta vol dir grups separats, no grups útils. Mira quants clients té cada grup abans de quedar-te una k.",
            "Si l'estandardització a mà no et coincideix amb la de scikit-learn per poc, la diferència és de definició, no d'error.",
        ],
        exemples=[
            f"{ML06} §2-§8 (k-means, inèrcia, colze i silueta), §9 (el número del grup no vol dir res) i §10 (unitats diferents i escalar).",
            f"{EX06}: agrupar sense etiquetes i comparar-ho al final amb les reals.",
            f"{EX00} §2: `StandardScaler`.",
        ],
        xavi=[
            "Faig servir el logaritme o no? No sé si m'estic inventant les dades.",
            "La silueta i les mides dels grups em diuen coses diferents: a qui faig cas?",
        ],
    ),
    dict(
        id="RE_402", fitxer="RE_402_spotify_estils.ipynb", bloc=4, dif=2,
        titol="Quants estils hi ha en un número?",
        encarrec="""Treballes a l'equip de recomanacions d'una plataforma de música. Spotify dona 12 números per a cada
cançó (ballable, energia, acústica, tempo...). El cap de producte vol fer «estils» automàtics a
partir d'aquests números, sense fer servir el gènere que diu la playlist.""",
        pregunta="""quanta informació diferent hi ha de debò en aquestes 12 columnes? I els grups que surten
d'agrupar-les, s'assemblen als gèneres musicals?""",
        font="""- **Font:** *30.000 cançons de Spotify* (TidyTuesday, 2020-01-21, obtingudes amb el paquet `spotifyr`
  de l'API de Spotify). El repositori és CC0; les dades són de Spotify i se'n fa un ús educatiu.
- **Cada fila** és **una cançó dins d'una playlist** d'un gènere: unes 33.000 files i 23 columnes.
- Diccionari original: <https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-01-21>""",
        diccionari=DIC_SPOTIFY,
        recollida="""- Algú va triar unes quantes playlists de cada gènere i en va baixar totes les cançons. El gènere és
  el de la playlist.
- Les 12 columnes d'àudio (de `danceability` a `duration_ms`) les calcula Spotify. No totes són
  mesures del so, ni totes estan en la mateixa escala.""",
        investigar="""Respon el cap de producte en dues parts. **Quanta informació hi ha:** decideix quines files i
quines columnes fas servir (una cançó, una fila?), fes un **PCA** de les 12 columnes tal com
venen i un altre amb les dades estandarditzades, i explica la diferència. Quantes components calen
per explicar el 80 % de la variància?

**Hi ha estils?** Sobre una mostra de 5.000 cançons estandarditzades, fes **k-means** per a diversos
valors de k i tria'n un amb el colze i la silueta. Només després, creua els grups amb
`playlist_genre`: s'hi assemblen? Descriu dos o tres grups amb paraules (com sonen?), a partir de
la mitjana de les columnes d'àudio en unitats originals.

La teoria ha d'aterrar al codi: fes el PCA **a mà** (matriu de covariància, valors i vectors
propis amb NumPy) i comprova la variància explicada i els vectors contra `PCA` de scikit-learn.""",
        obertes=[
            "Dibuixa les cançons a les dues primeres components, pintades per gènere. Quins gèneres queden separats? Què representa cada eix?",
            "Si treus les columnes que no són característiques del so, canvia la resposta?",
        ],
        pistes=[
            "Si una sola component explica gairebé tota la variància, mira quina columna hi mana i en quines unitats està.",
            "Els vectors propis poden sortir amb el signe girat respecte dels de scikit-learn, i no és cap error.",
            "Que no surtin grups clars també és una resposta, si la pots defensar.",
        ],
        exemples=[
            f"{MA06} §3-§10: PCA, variància explicada i escalar.",
            f"{ML06} §8 i {EX06}: k-means, colze i silueta.",
            f"{EX00} §5: duplicats.",
            "Si has fet el RE_102, ja coneixes les dades.",
        ],
        xavi=[
            "Els grups no s'assemblen als gèneres. Està malament el model o la pregunta?",
            "Les columnes `key` i `mode`, les faig servir o no?",
        ],
    ),
    dict(
        id="RE_403", fitxer="RE_403_municipis_catalunya.ipynb", bloc=4, dif=3,
        titol="Quins tipus de municipis té Catalunya?",
        encarrec="""Treballes a l'Observatori del Territori. Hi ha 947 municipis, i cada any se'n publiquen desenes
d'indicadors: població, habitatge, renda, turisme, sòl, aigua, residus... Et demanen una
**tipologia** que una persona que no sap PCA pugui entendre.""",
        pregunta="""quins tipus de municipis hi ha a Catalunya, què els distingeix, i on cau el teu?""",
        font="""- **Font:** *Indicadors territorials dels municipis de Catalunya* (Observatori del Territori, conjunt
  `8aaj-ypcb` de Dades Obertes de la Generalitat). **Domini públic.**
- **Còpia:** són dades vives; en fem servir una **còpia congelada** (baixada el 14-oct-2026).
- **Cada fila** és un municipi en un any (2023 i 2024): 1.896 files i 85 columnes.
- El significat de cada indicador és al portal: <https://analisi.transparenciacatalunya.cat/d/8aaj-ypcb>.
  El necessitaràs per triar columnes.""",
        diccionari=[
            ("codi_municipi, municipi", "codi i nom del municipi; els articles van al final (`Escala, l'`, `Bisbal d'Empordà, la`)"),
            ("codi_comarca, comarca, provincia, ambit_funcional, sistema_urba", "on és: comarca, província, àmbit del pla territorial i sistema urbà"),
            ("utm_x, utm_y, longitud, latitud, georeferencia", "coordenades del nucli"),
            ("any", "any de l'indicador (2023 o 2024)"),
            ("_01_ ... _09_", "**població**: total, evolució (%), densitat (hab/km²), taxa de dependència, moviment natural, migracions, població estacional (ETCA)"),
            ("_10_ ... _16_", "**habitatge**: habitatges acabats (total i protegits), preu mitjà del lloguer (€/mes), esforç sobre els ingressos (%) i si compleix uns llindars"),
            ("_17_ ... _22_", "**socioeconomia**: taxa d'ocupació (`toe`), taxa d'atur registrat (`tar`), renda neta mitjana per persona (`rnmp`, €), índex de Gini, índex socioeconòmic territorial (`ist`)"),
            ("_23_ ... _28_", "**turisme**: places turístiques i habitatges d'ús turístic (HUT), en total i per 100 habitants"),
            ("_29_ ... _39_", "**sòl**: superfícies de cada classe de sòl, en total i per habitant (m²/hab)"),
            ("_41_ ... _54_", "**desenvolupament i ocupació del sòl**: sectors pendents, sòl artificialitzat"),
            ("_55_ ... _60_", "**medi ambient**: consum d'aigua (total i per habitant), consum d'energia, residus (kg/hab/dia) i recollida selectiva (%)"),
            ("_61_ ... _72_", "**planejament**: figura vigent, antiguitat, modificacions"),
        ],
        recollida="""- Cada indicador ve d'una font diferent (Idescat, Agència de l'Habitatge, cadastre, Agència de
  Residus...) i l'Observatori els ajunta. No tots els indicadors existeixen per a tots els
  municipis, ni es calculen de la mateixa manera per als petits que per als grans.
- Hi ha indicadors **absoluts** (habitants, places, m³) i **relatius** (per habitant, per 100
  habitants, percentatges).""",
        investigar="""Fes la tipologia. Primer, aconsegueix **una fila per municipi** d'un sol any, i mira si totes
les files són municipis. Tria entre 8 i 15 indicadors: per a cada candidat, mira quina proporció
de nuls i de zeros té i si el rang té sentit, pensa si és absolut o relatiu, i justifica cada
tria en una línia.

Estandarditza i fes el **PCA**: quanta variància expliquen les dues primeres components, quantes
en calen per al 80 %, i què vol dir cada eix (posa-li un nom, i comprova'l amb els municipis dels
extrems). Fes **k-means**, tria k amb el colze, la silueta i la mida dels grups, i dona per a cada
grup un perfil en unitats originals i tres municipis d'exemple. On cau el teu municipi (o el de
l'institut)? Quins municipis té més a prop?

La teoria ha d'aterrar al codi: calcula **a mà** les coordenades dels municipis a les components
(amb `mean_` i `components_`) i comprova-les contra `pca.transform`.""",
        obertes=[
            "Afegeix dues o tres columnes absolutes (població, places turístiques, consum total d'aigua) i torna a fer el PCA. Què passa amb la primera component?",
            "Fes la tipologia amb l'altre any: quants municipis canvien de grup? Són canvis reals o soroll?",
        ],
        pistes=[
            "Un zero no sempre és un zero: pregunta't si, en aquella variable i en un municipi petit, té sentit.",
            "Els veïns d'un municipi al mapa de dues components i els veïns amb tots els indicadors no tenen per què ser els mateixos.",
        ],
        exemples=[
            f"{MA06} §6-§10: PCA, *loadings* i escalar.",
            f"{ML06} §8-§10: k-means, colze, silueta i unitats.",
            f"{EX00} §3: valors que falten.",
            "Si has fet el RE_401 o el RE_402, la recepta és la mateixa amb moltes més columnes per triar.",
        ],
        xavi=[
            "Aquests indicadors que només tenen els municipis grans, els faig servir?",
            "Ho faig amb totes les components o amb les dues primeres?",
        ],
    ),
]


# ---------------------------------------------------------------------------------------------
# Construcció del quadern
# ---------------------------------------------------------------------------------------------
def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n").splitlines(True)}


def codi(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": text.splitlines(True)}


def taula(files):
    linies = ["| Columna | Què és |", "| --- | --- |"]
    for col, desc in files:
        # "Num_postal " acaba amb un espai de debò: es manté dins dels accents greus
        noms = [col] if col.endswith(" ") else [c.strip() for c in col.split(",")]
        cols = ", ".join(f"`{c}`" for c in noms)
        linies.append(f"| {cols} | {desc} |")
    return "\n".join(linies)


def construeix(r):
    capcalera = f"**Optativa d'Aprenentatge automàtic · {BLOCS[r['bloc']]} · Dificultat {r['dif']} · durada: 1 o 2 sessions de 2 h**"
    c0 = f"""# {r['id']} · {r['titol']}

{capcalera}

{r['encarrec']}

**La pregunta:** {r['pregunta']}"""

    c1 = f"""## Les dades

{r['font']}

### Diccionari de columnes

{taula(r['diccionari'])}

### Com s'han recollit, i què cal tenir present

{r['recollida']}"""

    obertes = "\n".join(f"- {o}" for o in r["obertes"])
    c2 = f"""## Què has d'investigar

{r['investigar']}

**Per anar més enllà** (no és obligatori, i no hi ha una sola manera de fer-ho):

{obertes}"""
    if r.get("pistes"):
        pistes = "\n".join(f"- {p}" for p in r["pistes"])
        c2 += f"""

**Pistes per pensar** (no són la resposta):

{pistes}"""

    exemples = "\n".join(f"- {e}" for e in r["exemples"])
    c3 = f"""## Exemples per inspirar-te

Quaderns del curs on es fan servir les eines que et caldran. Mira com es treballa, no hi busquis
la resposta: les dades d'aquest repte són unes altres.

{exemples}"""

    lliura = LLIURAMENT_COMU
    if r.get("lliurament_extra"):
        lliura += " " + r["lliurament_extra"]
    assert len(r["xavi"]) <= 2
    xavi = " ".join(f"«{q}»" for q in r["xavi"])
    c4 = f"""## Lliurament

{lliura}

> **Quan cridar en Xavi:** per a dubtes de **criteri**, no de sintaxi (per a la sintaxi hi ha la
> documentació i els exemples). Per exemple: {xavi}

La cel·la següent carrega les dades. A partir d'aquí el quadern és teu: afegeix-hi totes les
cel·les de codi i de text que necessitis."""

    return {
        "cells": [md(c0), md(c1), md(c2), md(c3), md(c4), codi(CARREGA[r["id"]]), codi("")],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
            "colab": {"provenance": [], "name": r["fitxer"]},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main(ids):
    for r in REPTES:
        if ids and r["id"] not in ids:
            continue
        nb = construeix(r)
        ruta = os.path.join(DESTI, r["fitxer"])
        with open(ruta, "w", encoding="utf-8", newline="\n") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("escrit", os.path.relpath(ruta, ARREL))


if __name__ == "__main__":
    main(sys.argv[1:])
