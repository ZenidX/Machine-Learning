# Guions del bloc 3 — Optimització, dades reals i no supervisat

Quatre sessions, del 30 de novembre al 14 de desembre. Un guió per sessió, per obrir i tirar.

És el bloc més heterogeni del curs, i no per descuit: aquí es tanca el que va quedar obert al
bloc 2 (el marge de l'SVM), es fa l'única cosa del curs que s'assembla a la feina real (dades
brutes i pipelines) i s'obre el no supervisat, que fins ara no havien vist.

---

## S22 · dilluns 30 de novembre · Optimització amb restriccions

**Quadern:** `03_matematiques/MA_05_marge_optimitzacio.ipynb`

**Objectiu:** que els vectors de suport deixin de ser un fet estrany i passin a ser una
conseqüència.

Van sortir a la S21 com una curiositat: «el model només depèn d'uns pocs punts». Avui es
demostra que no és una optimització d'enginyeria ni una casualitat, sinó **el que obliga la
matemàtica del problema**. És una de les conclusions més boniques del curs i val la pena
anunciar-la al començament.

| Temps | Què |
|---|---|
| 15 min | La distància d'un punt a una recta, deduïda i no donada. I la comprovació que `w` és perpendicular a la frontera, amb dos punts de la recta i un producte escalar. |
| 15 min | **El marge com a $2/\|w\|$, i l'escalat que sembla trampa.** Per què imposar que els punts més propers donin 1 no perd generalitat: multiplica `w` i `b` per 5 i ensenya que la frontera no es mou. |
| 10 min | El plantejament formal: minimitzar $\frac{1}{2}\|w\|^2$ amb les restriccions. **La inversió que costa d'acceptar**: maximitzar el marge és minimitzar els pesos. |
| 30 min | **Lagrange, amb un exemple que es pot tocar.** No comencis per l'SVM. Minimitza $x^2+y^2$ amb $x+y=1$ de tres maneres —substituint, amb el lagrangià, i amb `scipy`— i que les tres donin (0,5, 0,5). Amb les corbes de nivell i la recta a sobre, es veu que la solució és on són tangents. |
| 25 min | **La folgança complementària, que és el cor de la sessió.** O el multiplicador és zero i el punt no compta, o el punt és exactament sobre el marge. Verificat amb un `SVC` entrenat: tots els vectors de suport donen $\|w\cdot x+b\|\approx 1$ i la resta, més. |
| 15 min | Reconstruir `w` a partir dels multiplicadors i comprovar que surt el `coef_` de scikit-learn. |
| 10 min | El kernel polinòmic demostrat: $(a\cdot b)^2$ és igual al producte escalar de la transformació explícita. **El truc del kernel no és màgia.** |

**El que no es deriva, i s'ha de dir:** el problema dual sencer. No hi cap en el temps. El que
es fa és presentar-ne el resultat, dir-ho clarament, i verificar-lo numèricament. Aquesta
distinció —entre saltar-se una cosa i amagar-la— és la que sosté la credibilitat de tot el curs.

---

## S23 · dimarts 1 de desembre · Dades brutes i pipelines

**Quadern:** `02_practica/EX_05_dades_brutes.ipynb` + `Pipeline.ipynb` i `Exercici Pipelines.ipynb` de la Núria

**Objectiu:** l'única sessió del curs que s'assembla a la feina de veritat.

Fins ara tots els conjunts de dades han vingut nets, de `sklearn.datasets`. Cap dada real ve
així, i **si no es diu, se'n van del curs creient que carregar dades és una línia**.

| Temps | Què |
|---|---|
| 20 min | L'inventari abans de tocar res: `isna().sum()`, duplicats, tipus de cada columna. Ja ho saben fer de la S10; aquí es fa amb intenció. |
| 25 min | **Valors que falten**: esborrar files, esborrar columnes, imputar. Cada estratègia té un cost, i es mesura sobre el mateix model. No hi ha una resposta bona a priori. |
| 25 min | **Columnes de text**: `OneHotEncoder`, i per què no es codifiquen com a números ordenats. Que provin de fer-ho mal i vegin què passa. |
| 30 min | **La fuita d'informació, i per què l'ordre de les operacions importa.** Escalar abans de partir el conjunt fa que el test hagi influït en l'entrenament. El número puja i és mentida. **Aquesta és la idea que s'han d'endur.** Lliga-ho amb la columna d'identificadors de la S16: és la mateixa trampa per una altra porta. |
| 20 min | `ColumnTransformer` i `Pipeline` com la manera d'evitar-ho estructuralment, no per disciplina. Amb el material de la Núria, que ja ho tenia plantejat. |

**Si has de retallar aquesta sessió**, el que es salva és la fuita d'informació. La imputació
s'aprèn sola; la fuita, no, i és l'error que els farà publicar un model que no funciona.

---

## S24 · dilluns 7 de desembre · PCA i vectors propis

> El 8 és festiu: aquesta setmana només hi ha dilluns.

**Quadern:** `03_matematiques/MA_06_pca_vectors_propis.ipynb`

**Objectiu:** la porta al no supervisat, i la sessió amb el millor moment matemàtic del curs.

| Temps | Què |
|---|---|
| 20 min | **La maledicció de la dimensionalitat, mesurada.** Punts a l'atzar en dimensió creixent: la distància mínima i la màxima s'acosten. Si totes les distàncies s'assemblen, **el k-NN que van implementar a la S14 deixa de tenir sentit**. Que això es pugui mesurar i no només explicar, val la sessió. |
| 20 min | Variància i covariància, des del recompte, comparades amb `np.var` i `np.cov`. El detall de `ddof` i el denominador $n$ contra $n-1$. |
| 15 min | La matriu de covariància com a $\frac{1}{n}X_c^\top X_c$. **És el `X.T @ X` que va quedar apuntat a la S08.** |
| 25 min | **Vectors i valors propis, vistos.** Aplica una matriu 2×2 a moltes fletxes i que es vegi que gairebé totes giren i unes poques no. Per què `eigh` i no `eig`: la covariància és simètrica, i això garanteix vectors propis ortogonals. |
| 25 min | **El moment de la sessió, i no te'l saltis ni el resumeixis.** Busca la direcció de màxima variància **per força bruta**: recorre tots els angles, projecta, mesura, dibuixa la corba, marca el màxim. I després ensenya que aquell angle és exactament el primer vector propi. La força bruta convenç; el vector propi explica. |
| 15 min | PCA sencer en cinc passos, aplicat a Iris. **I el detall que ho fa gran: el PCA no ha vist les etiquetes i tot i així les espècies surten separades.** Això és el que vol dir «no supervisat». |

**Dos avisos pràctics del quadern:** el PCA exigeix escalar abans, perquè mesura variància (es
demostra amb Wine, amb i sense `StandardScaler`, i el cas sense escalar és un desastre); i els
vectors propis poden sortir amb el signe girat, cosa que no és un error sinó una indeterminació
de la definició.

**On el PCA falla, i s'ensenya:** dos anells concèntrics. Cap projecció lineal els separa. Es
canvia d'eina (`KernelPCA`, `TSNE`), no de paràmetres.

---

## S25 · dilluns 14 de desembre · k-means, imatges i prova pràctica 3

**Quadern:** `02_practica/EX_03_digits.ipynb` · **A casa:** els enllaços de R de la Núria

**Objectiu:** tancar el no supervisat i el bloc.

**Aquesta sessió encara no té material propi per a la part de k-means.** És l'únic forat que
queda a la programació i cal preparar-lo al desembre.

| Temps | Què |
|---|---|
| 30 min | **k-means**: agrupar sense etiquetes. L'algorisme és prou senzill per implementar-lo a mà en una sessió —assignar cada punt al centre més pròxim, recalcular els centres, repetir— i **ja tenen les distàncies de la S14 i els eixos de la S07**. Aplica-ho a Iris i compara els grups que surten amb les espècies reals, que el model no ha vist. |
| 20 min | **Imatges com a taula**: el conjunt digits, on cada columna és un píxel. Els mateixos cinc models funcionen igual. Enllaça-ho amb el PCA de la S24 per dibuixar els dígits en dues dimensions. |
| 50 min | **Prova pràctica 3.** Format: un CSV brut que no hagin vist. Netejar-lo, muntar un `Pipeline` sense fuita d'informació, entrenar, i respondre per què el resultat és el que és. |
| 20 min | **R al costat de Python**, en cinc minuts de conversa i prou. És a la llista d'eines oficial i la docent anterior hi dedicava sis setmanes; aquí no hi cap. Es reparteixen els enllaços de `_moodle-25-26/ENLLACOS.md` com a lectura, i **es diu que no entra a l'examen**. I presentació del bloc de xarxes. |

---

## Com saber si el bloc ha anat bé

Al final d'aquestes quatre sessions, un alumne hauria de poder, **sense ajuda**:

- Agafar un CSV brut i muntar un `Pipeline` que no filtri informació del test a l'entrenament.
- Explicar per què escalar abans de partir el conjunt és un error, i no només recordar que ho és.
- Reduir un conjunt de 30 columnes a dues i dir quanta informació s'hi ha perdut.
- Dir per què les distàncies deixen de servir en dimensió alta.

**El senyal d'alarma d'aquest bloc és a la S22**: si no els diu res la folgança complementària,
segurament el que falla és el descens de gradient de la S19. Val més tornar-hi mitja sessió que
continuar, perquè el bloc 4 sencer se sosté sobre la S19.
