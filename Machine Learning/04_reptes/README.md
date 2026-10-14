# Reptes

Quaderns per treballar **sols** amb dades reals que no heu vist mai. Cada repte és **un enunciat i
unes dades**:

- l'**encàrrec**: qui ets i quina pregunta has de respondre;
- **les dades**: d'on surten, la llicència, què és cada fila, el **diccionari de columnes** (què vol
  dir cada una, en quines unitats, quins codis) i com s'han recollit;
- **què has d'investigar**: la pregunta principal i unes quantes preguntes obertes, i de vegades
  alguna pista per pensar (mai la resposta);
- **exemples per inspirar-te**: els quaderns del curs on es fan servir les eines que et caldran;
- el **lliurament**, i quan val la pena cridar en Xavi;
- una cel·la que carrega les dades, i una de buida. La resta, la poses tu.

Ningú no et dirà quins passos has de seguir ni què està brut: decidir-ho forma part del repte.

- Obriu-los a Google Colab. No cal instal·lar res.
- Les dades vives (Generalitat, Ajuntament) estan congelades a [`dades/`](dades/) i es carreguen des
  de GitHub. Les fonts i les llicències són a cada quadern.
- **Lliurament:** el quadern executat i sense errors, amb la vostra anàlisi (codi i text que explica
  cada decisió) i una conclusió de tres a cinc frases, escrita per vosaltres, que respongui
  l'encàrrec amb números.
- Dificultat: **1** = carrega net i les preguntes surten amb `groupby`; **2** = cal netejar o canviar
  de forma la taula; **3** = les dades enganyen si no es miren bé.

## Resolts

Cada repte té una versió resolta a [`resolts/`](resolts/): una manera de resoldre'l (no l'única), amb
el codi executat de cap a peus, els comentaris de cada resultat i una conclusió. **Feu el repte
abans de mirar-la**: el que s'aprèn és trobar les coses, no llegir-les. Serveix per comparar la
vostra anàlisi un cop lliurada, o per desencallar-vos quan ja ho heu provat de debò.

## Bloc 1 — Dades

NumPy i Pandas sobre dades de veritat. Cada repte acaba amb un càlcul de NumPy (normes o
distàncies). És la preparació de la **Pp1** (27-oct): carregar un CSV desconegut, forma, inventari de
nuls, preguntes amb `groupby`, un gràfic i una distància amb NumPy.

| Repte | Dataset | Dif. | Eines | Resolt |
|---|---|---|---|---|
| [RE_101 · On i quan hi ha accidents a Barcelona](RE_101_accidents_bcn.ipynb) | Accidents gestionats per la Guàrdia Urbana, 2024 (Open Data BCN) | 1 | `groupby`, `agg`, valors que falten, gràfics de barres · NumPy: distància en metres amb `np.linalg.norm` | [resolt](resolts/RE_101_accidents_bcn_resolt.ipynb) |
| [RE_102 · Quina música fa ballar](RE_102_spotify.ipynb) | 30.000 cançons de Spotify (TidyTuesday) | 1 | duplicats, `groupby().agg`, gràfic de línia · NumPy: normalitzar per columnes i recomanador per distància | [resolt](resolts/RE_102_spotify_resolt.ipynb) |
| [RE_103 · Com de greu va ser la sequera](RE_103_embassaments.ipynb) | Aigua als embassaments de les conques internes, 2000-2026 (ACA) | 2 | `pd.to_datetime`, `pivot` de llarg a ample, mínims per any · NumPy: el dia del passat més semblant a avui | [resolt](resolts/RE_103_embassaments_resolt.ipynb) |
| [RE_104 · Quant costa llogar un pis](RE_104_lloguer.ipynb) | Preu mitjà del lloguer per municipi, 2007-2026 (Agència de l'Habitatge) | 2 | filtrar, `isin`, `pivot_table`, pujada percentual · NumPy: trajectòries semblants, en euros i normalitzades | [resolt](resolts/RE_104_lloguer_resolt.ipynb) |
| [RE_105 · Els estius de Barcelona, cada cop més calorosos?](RE_105_meteo_fabra.ipynb) | Meteo diària de l'Observatori Fabra, 2016-2026 (SMC, XEMA) | 3 | format llarg, `pivot`, `nlargest`, mapa de calor amb `imshow` · NumPy: l'any més allunyat de l'any mitjà | [resolt](resolts/RE_105_meteo_fabra_resolt.ipynb) |
| [RE_106 · Quan i on es respira pitjor a Barcelona](RE_106_aire_bcn.ipynb) | Qualitat de l'aire horària a Barcelona, 2024 (XVPCA) | 3 | `melt` d'ample a llarg, `dt.dayofweek`, `pivot_table` · NumPy: matriu de distàncies amb broadcasting | [resolt](resolts/RE_106_aire_bcn_resolt.ipynb) |

## Bloc 2 — Supervisat

Entrenar, mesurar i verificar, amb datasets d'OpenML que es carreguen amb `fetch_openml`. L'ordre
segueix el del curs: k veïns i arbres, regressió logística, mètriques amb classes desequilibrades,
sobreajust i escalat, regressió, i equitat. A cada repte **la teoria aterra al codi**: calcules una
cosa a mà (un Gini, una probabilitat, un *recall*, una predicció) i la comproves contra
scikit-learn. És la preparació de la **Pp2** (1-des): entrenar dos models i comparar-los amb la
mesura adequada, implementar una funció de pèrdua i comprovar-la, i explicar les prediccions amb els
pesos o les importàncies.

| Repte | Dataset | Dif. | Eines | Resolt |
|---|---|---|---|---|
| [RE_201 · Bolets: comestible o verinós?](RE_201_bolets.ipynb) | Mushroom (UCI, OpenML 24) | 1 | `OneHotEncoder`, arbre i profunditat, kNN · a mà: Gini i *recall* | [resolt](resolts/RE_201_bolets_resolt.ipynb) |
| [RE_202 · Qui acabarà comprant?](RE_202_compres_en_linia.ipynb) | Online Shoppers Intention (UCI, OpenML 46947) | 2 | `DummyClassifier`, `StandardScaler`, regressió logística i *odds* · a mà: la sigmoide i la log-loss | [resolt](resolts/RE_202_compres_en_linia_resolt.ipynb) |
| [RE_203 · A qui truquem?](RE_203_campanya_banc.ipynb) | Bank Marketing (UCI, OpenML 46910) | 3 | `ColumnTransformer`, logística contra bosc, llindar i benefici, ROC i *precision-recall* · a mà: les mesures des de la matriu | [resolt](resolts/RE_203_campanya_banc_resolt.ipynb) |
| [RE_204 · Formigó: memoritzar no és aprendre](RE_204_formigo.ipynb) | Concrete Compressive Strength (UCI, OpenML 44959) | 2 | regressió, kNN i escalat, sobreajust d'un arbre, `cross_val_score` · a mà: una predicció de kNN, MAE i $R^2$ | [resolt](resolts/RE_204_formigo_resolt.ipynb) |
| [RE_205 · Quantes bicis caldran a les 8?](RE_205_bicis.ipynb) | Bike Sharing, Washington (UCI, OpenML 42712) | 2 | partició temporal, l'hora com a número, one-hot o sin/cos, recta contra bosc · a mà: `predict` = $Xw+b$, MAE i RMSE | [resolt](resolts/RE_205_bicis_resolt.ipynb) |
| [RE_206 · És just el model?](RE_206_equitat_adult.ipynb) | Adult / Census Income (UCI, OpenML 1590) | 3 | auditoria per grups: taxa de selecció, TPR i FPR, atributs protegits, llindar per grup · a mà: les mesures de cada grup | [resolt](resolts/RE_206_equitat_adult_resolt.ipynb) |

## Bloc 3 — Dades brutes i Pipeline

Dades que no venen netes i un número que s'ha de poder defensar. Cap enunciat no us dirà què està
brut: ho heu de trobar vosaltres. És la preparació de la **Pp3** (21-des): un CSV brut, un
`Pipeline` que no filtri informació del test a l'entrenament, i justificar cada decisió de neteja.
Allà es mesura **si el número que doneu és honest**, no si és alt.

| Repte | Dataset | Dif. | Eines | Resolt |
|---|---|---|---|---|
| [RE_301 · Quant val aquest cotxe?](RE_301_cotxes_preu.ipynb) | Automobile / imports-85 (UCI, 1985) | 2 | llegir un fitxer amb la seva descripció, inventari de forats, `Pipeline` amb imputació i one-hot, MAE amb validació creuada contra `DummyRegressor` | [resolt](resolts/RE_301_cotxes_preu_resolt.ipynb) |
| [RE_302 · El 2024 va ser pitjor?](RE_302_accidents_dos_anys.ipynb) | Accidents de la Guàrdia Urbana, 2023 i 2024 (Open Data BCN) | 2 | comparar dos fitxers columna per columna, `value_counts(dropna=False)`, una funció de neteja amb propietats comprovades amb `assert`, taxes per 1.000 | [resolt](resolts/RE_302_accidents_dos_anys_resolt.ipynb) |
| [RE_303 · Es cancel·larà aquesta reserva?](RE_303_hotels_cancellacions.ipynb) | Hotel booking demand (Antonio et al., 2019) | 2 | «aquesta columna, la sé el dia de la reserva?», duplicats, `Pipeline` amb `make_column_selector`, `DummyClassifier`, partició per temps | [resolt](resolts/RE_303_hotels_cancellacions_resolt.ipynb) |
| [RE_304 · Quina lletra traurà el meu pis?](RE_304_certificats_energetics.ipynb) | Certificats d'eficiència energètica, mostra de 30.000 (ICAEN) | 3 | el repte complet: neteja dins del `Pipeline` amb `FunctionTransformer`, F1 *macro* amb `StratifiedKFold`, matriu de confusió d'una classe ordinal | [resolt](resolts/RE_304_certificats_energetics_resolt.ipynb) |

## Bloc 4 — No supervisat

Agrupar i reduir sense etiquetes. Les decisions que pesen són abans del model (escalar, logaritme,
quines columnes) i després (com es llegeixen els grups). Cada repte té una part **a mà** que es
comprova contra scikit-learn, i una descripció dels grups o dels eixos **amb les vostres paraules**.

| Repte | Dataset | Dif. | Eines | Resolt |
|---|---|---|---|---|
| [RE_401 · Quins tipus de clients tenim?](RE_401_clients_majorista.ipynb) | Wholesale customers (UCI) | 1 | escalar o logaritme, k-means amb colze i silueta, perfils, comparar *a posteriori* amb una etiqueta · a mà: l'estandardització i la inèrcia | [resolt](resolts/RE_401_clients_majorista_resolt.ipynb) |
| [RE_402 · Quants estils hi ha en un número?](RE_402_spotify_estils.ipynb) | 30.000 cançons de Spotify (TidyTuesday) | 2 | PCA amb i sense escalar, *loadings*, components per al 80 %, k-means sobre una mostra · a mà: PCA amb `np.cov` i `eigh` | [resolt](resolts/RE_402_spotify_estils_resolt.ipynb) |
| [RE_403 · Quins tipus de municipis té Catalunya?](RE_403_municipis_catalunya.ipynb) | Indicadors territorials dels municipis, 2023-2024 (Observatori del Territori) | 3 | triar indicadors, PCA i noms dels eixos, tipologia amb k-means, on cau el teu municipi · a mà: la projecció contra `transform` | [resolt](resolts/RE_403_municipis_catalunya_resolt.ipynb) |

## Per al professor: com es generen

- Enunciats: `python _eines/gen_reptes_enunciat.py` (el contingut de cada repte és al mateix script, i
  les cel·les de càrrega a `_eines/reptes_carrega.py`).
- Resolts: `python _eines/gen_reptes_resolts.py`, en local, a partir dels solucionaris de
  `solucions/` (fora del repositori). Treu tot el que és privat i ho comprova abans d'escriure.
- Els generadors antics amb bastida (`_eines/gen_RE_bloc34.py` i els `gen_*.py` de `solucions/`)
  produeixen el format anterior (caixa d'eines, nivells, pistes i comprovacions): **estan obsolets**.
  Les versions amb bastida es guarden en local a `solucions/bastides/`.
- Verificar: `CEIABD-IA/.venv/Scripts/python.exe _eines/executa_nb.py <quadern>`, des d'aquesta
  carpeta (perquè trobi `dades/`).
