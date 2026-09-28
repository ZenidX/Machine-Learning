# -*- coding: utf-8 -*-
"""Genera el quadern MA_06: PCA i vectors propis.

    CEIABD-IA/.venv/Scripts/python.exe _eines/gen_MA_06_pca.py

Els numeros que apareixen al text son els de l'execucio real del quadern amb
llavor 42; si es canvia el codi, cal tornar a executar-lo i actualitzar-los.
"""
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code, escriu

cells = []
A = cells.append

# ---------------------------------------------------------------- portada
A(md(r"""
# Reduir dimensions: PCA i vectors propis

**Optativa d'Aprenentatge automàtic - DAM/DAW 2n**

El dataset de càncer de mama que ja heu fet servir té **30 columnes**. Cada pacient és un
punt en un espai de 30 dimensions. No es pot dibuixar: un full de paper té dos eixos i una
pantalla també.

La pregunta d'aquest quadern és aquesta:

> **Com es veu en dues dimensions un dataset de 30 columnes, sense inventar-se res?**

La trampa fàcil seria quedar-se amb dues columnes qualssevol i dibuixar-les. Això és
llençar 28 columnes a la brossa i esperar que no importessin. El que farem és diferent:
buscarem les **direccions** de l'espai de 30 dimensions on les dades varien més, i
dibuixarem el que es veu des d'allà.

I aquí passa una cosa que val la pena que us aturi: la pregunta és **geomètrica** (quina
direcció?) i la resposta resulta ser un **objecte d'àlgebra lineal** (un vector propi d'una
matriu). No hi ha cap motiu obvi perquè una cosa porti a l'altra. En aquest quadern ho
demostrarem: primer trobarem la direcció per **força bruta**, provant angles un a un, i
després veurem que el número que surt coincideix amb el primer vector propi de la matriu de
covariància. Els dos camins arriben al mateix lloc.

També és el vostre primer model **no supervisat**: cap dels càlculs que farem mira les
etiquetes. Ni una vegada.

Del quadern `MA_01_algebra_lineal.ipynb` donem per sabut el producte matriu-vector i la
projecció d'un vector sobre un altre. Si no els teniu frescos, repasseu-los abans.
"""))

A(code("""
import time

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.special import gammaln

np.random.seed(42)
np.set_printoptions(precision=4, suppress=True)

print("numpy", np.__version__)
"""))

# ---------------------------------------------------------------- 1
A(md(r"""
## 1. La maledicció de la dimensionalitat, mesurada

De la «maledicció de la dimensionalitat» se'n parla molt i es demostra poc. Aquí la
mesurarem, perquè té una conseqüència directa sobre un model que ja heu implementat.

L'experiment: llencem $n$ punts a l'atzar dins d'un cub de costat 1 en dimensió $d$,
calculem **totes** les distàncies entre parells de punts, i mirem la més petita i la més
gran. La quantitat interessant és la ràtio

$$\frac{d_{\min}}{d_{\max}}$$

Si val gairebé 0, hi ha parells molt a prop i parells molt lluny: les distàncies
distingeixen. Si val gairebé 1, **totes les distàncies són iguals**.

Fem servir `pdist` de SciPy, que calcula les $\binom{n}{2}$ distàncies d'un cop, i repetim
cada dimensió 3 vegades per suavitzar l'atzar. Amb 200 punts per dimensió el bucle sencer
tarda menys de mig segon; amb més punts la conclusió és la mateixa i triga més.
"""))

A(code("""
dimensions = [2, 3, 5, 10, 20, 50, 100, 200, 500]
n_punts = 200
repeticions = 3

ratios = []
for d in dimensions:
    r_d = []
    for _ in range(repeticions):
        P = np.random.rand(n_punts, d)   # n_punts dins del cub [0,1]^d
        dists = pdist(P)                 # totes les distàncies entre parells
        r_d.append(dists.min() / dists.max())
    ratios.append(np.mean(r_d))

for d, r in zip(dimensions, ratios):
    print(f"dim {d:4d}   d_min / d_max = {r:.4f}")
"""))

A(md(r"""
Els números de l'execució: en dimensió 2 la ràtio val **0.0017**, en dimensió 50 ja val
**0.4931** i en dimensió 500 val **0.8020**. Puja de manera monòtona i s'acosta a 1.
"""))

A(code("""
plt.figure(figsize=(7, 4.5))
plt.plot(dimensions, ratios, "o-", color="tab:blue")
plt.xscale("log")
plt.xlabel("Dimensió de l'espai (escala logarítmica)")
plt.ylabel("$d_{min} / d_{max}$")
plt.title("En dimensió alta totes les distàncies s'assemblen")
plt.ylim(0, 1)
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
### Què implica això

El k-NN que vau implementar fa una sola cosa: ordena les mostres per distància i es queda
les $k$ més properes. **Si totes les distàncies són gairebé iguals, aquest ordre deixa de
significar res**: el veí «més proper» ho és per una diferència del 20 % respecte del més
llunyà, i aquesta diferència se l'empassa qualsevol soroll de mesura. El model segueix
funcionant (retorna una predicció) però la noció de proximitat en què es basa s'ha buidat.

Això val per a tot model que treballi amb distàncies: k-NN, k-means, SVM amb kernel RBF.

### La mateixa cosa des del volum

Hi ha una segona manera de veure-ho, i és més desconcertant. Agafeu el cub de costat 1 i
l'esfera inscrita dins seu, de radi $1/2$. En dimensió 2 l'esfera (un cercle) ocupa el
78.5 % del quadrat. Quina fracció ocupa en dimensió 30?

El volum de l'esfera de radi $r$ en dimensió $d$ és

$$V_d(r) = \frac{\pi^{d/2}}{\Gamma\left(\frac{d}{2}+1\right)} r^d$$

i el del cub de costat 1 és 1. Amb $r = 1/2$ la fracció és

$$f(d) = \frac{\pi^{d/2}}{\Gamma\left(\frac{d}{2}+1\right) \, 2^{d}}$$

$\Gamma$ és la funció gamma, la generalització del factorial ($\Gamma(n+1) = n!$ per a
enters). Creix tan de pressa que calcular-la directament desborda; per això fem servir
`gammaln`, que dóna el seu logaritme, i treballem amb logaritmes fins al final.
"""))

A(code("""
def fraccio_esfera(d):
    \"\"\"Volum de l'esfera inscrita dividit pel volum del cub de costat 1, en dimensió d.\"\"\"
    log_f = (d / 2) * np.log(np.pi) - gammaln(d / 2 + 1) - d * np.log(2)
    return np.exp(log_f)


for d in [1, 2, 3, 5, 10, 20, 30, 50]:
    print(f"dim {d:3d}   fracció del cub que ocupa l'esfera: {fraccio_esfera(d):.3e}")
"""))

A(md(r"""
En dimensió 10 l'esfera ja ocupa el **0.25 %** del cub; en dimensió 30, $2\cdot10^{-14}$;
en dimensió 50, $1.5\cdot10^{-28}$. Gairebé tot el volum d'un cub en dimensió alta és **als
racons**, lluny del centre. Si llenceu punts a l'atzar dins d'un cub de dimensió 30,
pràcticament cap cau a prop del centre.

La conclusió pràctica: **en dimensió alta l'espai és buit**. Les dades reals no omplen les
30 dimensions; viuen en una regió molt més petita. Trobar-la és exactament el que fa el
PCA.
"""))

# ---------------------------------------------------------------- 2
A(md(r"""
## 2. Variància i covariància, des del recompte

Per buscar «la direcció on les dades varien més» cal saber mesurar quant varien. Dues
fórmules, les dues implementades a mà.

La **variància** d'una columna és la mitjana dels quadrats de les desviacions respecte de
la mitjana:

$$\sigma^2 = \frac{1}{n}\sum_{i=1}^{n} (x_i - \bar{x})^2$$

La **covariància** entre dues columnes és el mateix però multiplicant les desviacions de
les dues:

$$\mathrm{cov}(x,y) = \frac{1}{n}\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})$$

Fixeu-vos que $\mathrm{cov}(x,x) = \sigma_x^2$: la variància és un cas particular de la
covariància.

Treballarem amb Iris, que ja coneixeu: 150 flors, 4 columnes.
"""))

A(code("""
from sklearn.datasets import load_iris

iris = load_iris()
X_iris = iris.data
y_iris = iris.target
noms = ["sepal_llarg", "sepal_ample", "petal_llarg", "petal_ample"]

print("Forma de X:", X_iris.shape)
print("Mitjanes per columna:", X_iris.mean(axis=0))
"""))

A(code("""
x = X_iris[:, 2]          # petal_llarg
n = len(x)

# La fórmula, tal com està escrita
variancia_a_ma = np.sum((x - x.mean()) ** 2) / n

print(f"Variància a mà (denominador n):     {variancia_a_ma:.6f}")
print(f"np.var(x)              (ddof=0):    {np.var(x):.6f}")
print(f"np.var(x, ddof=1)      (n-1):       {np.var(x, ddof=1):.6f}")
"""))

A(md(r"""
### El denominador: $n$ contra $n-1$

Surten dos números diferents: **3.095503** amb denominador $n$ i **3.116278** amb
denominador $n-1$. No és un error de ningú; són dues coses diferents.

- Dividir per $n$ dóna la **variància de les dades que teniu**. És la descripció exacta
  d'aquestes 150 flors. És el que s'anomena variància *poblacional*.
- Dividir per $n-1$ dóna una **estimació de la variància de la població** de la qual les
  150 flors són una mostra. Fer servir $\bar{x}$ (calculada de les mateixes dades) en lloc
  de la mitjana real de la població fa que les desviacions surtin sistemàticament una mica
  petites; dividir per $n-1$ en lloc de $n$ ho corregeix. És la variància *mostral*, i és
  un estimador no esbiaixat.

A NumPy això és l'argument **`ddof`** (*delta degrees of freedom*): el denominador és
$n - \mathrm{ddof}$. I aquí ve el parany, perquè **les dues funcions no tenen el mateix
valor per defecte**:

| Funció | `ddof` per defecte | Denominador |
|---|---|---|
| `np.var`, `np.std`, `ndarray.var()` | 0 | $n$ |
| `np.cov` | 1 | $n-1$ |

Amb $n = 150$ la diferència és del 0.7 % i no canvia cap conclusió. Amb $n = 10$ és de
l'11 %. Per al PCA farem servir sempre **`ddof=0`** (denominador $n$), perquè volem
descriure les dades que tenim, i perquè així la matriu de covariància surt exactament
$\frac{1}{n}X_c^\top X_c$, sense factors de correcció pel mig.
"""))

A(code("""
y = X_iris[:, 3]          # petal_ample

covariancia_a_ma = np.sum((x - x.mean()) * (y - y.mean())) / n

print(f"cov(petal_llarg, petal_ample) a mà:      {covariancia_a_ma:.6f}")
print(f"np.cov(x, y, ddof=0)[0, 1]:              {np.cov(x, y, ddof=0)[0, 1]:.6f}")
print(f"np.cov(x, y)[0, 1]   (ddof=1 per defecte): {np.cov(x, y)[0, 1]:.6f}")

# La variància és el cas particular cov(x, x)
print(f"\\ncov(x, x) a mà: {np.sum((x - x.mean()) ** 2) / n:.6f}"
      f"   == variància: {np.var(x):.6f}")
"""))

A(md(r"""
### El signe de la covariància

La covariància entre `petal_llarg` i `petal_ample` val **+1.286972**: quan una puja,
l'altra també. Busquem-ne una de negativa: `sepal_ample` contra `petal_llarg` dóna
**-0.327459**, i el núvol de punts s'inclina al contrari.

El signe diu **la direcció** de la relació, no la seva força: la covariància depèn de les
unitats i no es pot comparar entre parells de columnes diferents. (Per comparar-les cal
dividir per les desviacions típiques, i això dóna el coeficient de correlació; no ens fa
falta aquí.)
"""))

A(code("""
parelles = [(2, 3), (1, 2)]

fig, axs = plt.subplots(1, 2, figsize=(11, 4.5))
for ax, (i, j) in zip(axs, parelles):
    a, b = X_iris[:, i], X_iris[:, j]
    cov_ij = np.sum((a - a.mean()) * (b - b.mean())) / n
    ax.scatter(a, b, s=18, color="tab:blue", alpha=0.7)
    ax.axvline(a.mean(), color="gray", linestyle="--", linewidth=1)
    ax.axhline(b.mean(), color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel(noms[i] + " (cm)")
    ax.set_ylabel(noms[j] + " (cm)")
    ax.set_title(f"cov = {cov_ij:+.3f}")
    ax.grid(alpha=0.3)

fig.suptitle("El signe de la covariància és la inclinació del núvol")
plt.tight_layout()
plt.show()
"""))

A(md(r"""
Les línies grises són les dues mitjanes, i parteixen el pla en quatre quadrants. La
covariància és la mitjana del producte $(x_i-\bar{x})(y_i-\bar{y})$: als quadrants superior
dret i inferior esquerre el producte és positiu, als altres dos negatiu. La covariància
surt positiva quan hi ha més punts (o més allunyats) a la diagonal que puja.
"""))

# ---------------------------------------------------------------- 3
A(md(r"""
## 3. La matriu de covariància

Amb 4 columnes hi ha $4 \times 4 = 16$ covariàncies possibles (comptant les variàncies de
la diagonal). Posades en una matriu:

$$C = \begin{pmatrix}
\mathrm{cov}(x_1,x_1) & \mathrm{cov}(x_1,x_2) & \cdots \\
\mathrm{cov}(x_2,x_1) & \mathrm{cov}(x_2,x_2) & \cdots \\
\vdots & & \ddots
\end{pmatrix}$$

Calcular-les una a una amb dos bucles seria correcte i lent. Hi ha una manera de fer-ho
d'un cop. Primer **centrem** les dades, restant a cada columna la seva mitjana:

$$X_c = X - \bar{x}$$

Ara $\bar{x}_j = 0$ per a tota columna $j$. I aleshores l'element $(j,k)$ de
$X_c^\top X_c$ és, per la definició del producte de matrius,

$$(X_c^\top X_c)_{jk} = \sum_{i=1}^{n} (X_c)_{ij}(X_c)_{ik} = \sum_{i=1}^{n}(x_{ij}-\bar{x}_j)(x_{ik}-\bar{x}_k)$$

que és exactament el numerador de la covariància entre les columnes $j$ i $k$. Dividint per
$n$:

$$\boxed{C = \frac{1}{n} X_c^\top X_c}$$

**Totes** les covariàncies, en un sol producte de matrius. `X.T @ X` és una expressió que
ja heu vist; aquí té un nom: sobre dades centrades i dividida per $n$, és la matriu de
covariància.
"""))

A(code("""
# Pas 1: centrar
X_c = X_iris - X_iris.mean(axis=0)
print("Mitjanes després de centrar (han de ser ~0):", X_c.mean(axis=0))

# Pas 2: un sol producte de matrius
C = X_c.T @ X_c / n

print("\\nForma de C:", C.shape)
print(C)
"""))

A(code("""
# C és simètrica: cov(a, b) == cov(b, a)
print("C == C.T ?", np.allclose(C, C.T))
print("Diferència màxima entre C i C.T:", np.abs(C - C.T).max())

# I coincideix amb np.cov, si li demanem el mateix denominador
C_numpy = np.cov(X_iris.T, ddof=0)     # atenció: np.cov vol les variables per FILES
print("\\nDiferència màxima entre la nostra C i np.cov(ddof=0):",
      np.abs(C - C_numpy).max())
print("Diferència màxima contra np.cov per defecte (ddof=1):",
      np.abs(C - np.cov(X_iris.T)).max())
"""))

A(md(r"""
La matriu és 4x4, la diferència amb la seva transposada és **0** exacte, i la diferència
amb `np.cov(ddof=0)` és de l'ordre de $4 \cdot 10^{-16}$, que és l'error de representació
dels `float64` i no un error de càlcul. Contra `np.cov` per defecte la diferència és de
**0.0208**: és el factor $n/(n-1)$ del qual parlàvem.

Tres detalls que faran falta després:

- A la **diagonal** hi ha les variàncies de cada columna: 0.6811, 0.1887, 3.0955, 0.5771.
  `petal_llarg` és la columna que més varia, amb molta diferència.
- La **traça** (suma de la diagonal) és la variància total de les dades, **4.5425**. Aquest
  número és el pressupost que el PCA reparteix entre les components.
- $C$ és **simètrica**. Això no és un detall estètic: és la propietat de la qual penja tota
  la resta del quadern.
"""))

A(code("""
print("Variàncies a la diagonal:", np.diag(C))
print(f"Traça de C (variància total): {np.trace(C):.4f}")
"""))

# ---------------------------------------------------------------- 4
A(md(r"""
## 4. Vectors i valors propis, des de la definició

Canviem de tema un moment. Aparentment.

Una matriu quadrada $A$ és una transformació: agafa un vector $v$ i en retorna un altre,
$Av$. En general la transformació **gira** el vector i li canvia la llargada. Però per a
cada matriu hi ha unes direccions especials on no hi ha gir: el vector de sortida apunta
exactament cap on apuntava el d'entrada, només estirat (o encongit, o girat 180 graus).

Aquests són els **vectors propis**, i el factor d'estirament és el **valor propi**:

$$\boxed{A v = \lambda v}$$

$v$ és un vector (no nul) i $\lambda$ un número. L'equació diu: aplicar la matriu a $v$ és
el mateix que multiplicar $v$ per un número. La matriu, sobre aquesta direcció concreta, es
comporta com una simple multiplicació.

Ho veurem amb una matriu 2x2 que podem dibuixar:

$$A = \begin{pmatrix} 3 & 1 \\ 1 & 2 \end{pmatrix}$$

Agafem molts vectors unitaris repartits per la circumferència, els apliquem $A$, i mirem
quants canvien de direcció.
"""))

A(code("""
A_demo = np.array([[3.0, 1.0],
                   [1.0, 2.0]])

# 16 vectors unitaris repartits per la circumferència
angles_demo = np.linspace(0, 2 * np.pi, 16, endpoint=False)
V = np.stack([np.cos(angles_demo), np.sin(angles_demo)])   # 2 x 16, un vector per columna


def gir_en_graus(A, V):
    \"\"\"Angle, en graus, entre cada columna de V i la seva transformada A@V.\"\"\"
    AV = A @ V
    cos = np.sum(V * AV, axis=0) / (np.linalg.norm(V, axis=0) * np.linalg.norm(AV, axis=0))
    return np.degrees(np.arccos(np.clip(np.abs(cos), -1, 1)))


AV = A_demo @ V
gir = gir_en_graus(A_demo, V)

print("Gir (graus) de cada vector:", np.round(gir, 1))
print(f"\\nVectors amb gir de més d'1 grau: {np.sum(gir > 1)} de {len(gir)}")
print(f"Gir mínim: {gir.min():.1f} graus.  Gir màxim: {gir.max():.1f} graus")
"""))

A(code("""
plt.figure(figsize=(6.5, 6.5))
for k in range(V.shape[1]):
    plt.arrow(0, 0, V[0, k], V[1, k], color="gray", width=0.008,
              length_includes_head=True, head_width=0.06, alpha=0.8)
    plt.arrow(0, 0, AV[0, k], AV[1, k], color="tab:blue", width=0.008,
              length_includes_head=True, head_width=0.06, alpha=0.6)

plt.plot([], [], color="gray", linewidth=3, label="vector original $v$")
plt.plot([], [], color="tab:blue", linewidth=3, label="transformat $Av$")
plt.gca().set_aspect("equal")
plt.xlim(-4.2, 4.2)
plt.ylim(-4.2, 4.2)
plt.xlabel("primera coordenada")
plt.ylabel("segona coordenada")
plt.title("La matriu gira gairebé tots els vectors")
plt.legend(loc="upper left")
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
**Els 16 giren**, entre 5.7 i 26.6 graus. Cap dels 16 angles equiespaiats que hem provat és
una direcció pròpia, i era d'esperar: les direccions pròpies són dues rectes concretes i
haurien de coincidir amb la reixa per casualitat.

Però al dibuix es veu que el gir **no és el mateix a tot arreu**: hi ha zones on la fletxa
blava i la grisa gairebé se superposen. Busquem amb una reixa fina on el gir es fa zero.
"""))

A(code("""
angles_fins = np.linspace(0, 180, 3601)            # pas de 0.05 graus
V_fins = np.stack([np.cos(np.radians(angles_fins)), np.sin(np.radians(angles_fins))])
gir_fins = gir_en_graus(A_demo, V_fins)

# busquem els mínims locals: punts més baixos que els seus dos veïns
es_minim = (gir_fins[1:-1] < gir_fins[:-2]) & (gir_fins[1:-1] < gir_fins[2:])
angles_sense_gir = angles_fins[1:-1][es_minim]

print("Angles on el gir es fa zero:", np.round(angles_sense_gir, 4))
print("Gir que queda en aquests angles:", gir_fins[1:-1][es_minim])
"""))

A(code("""
plt.figure(figsize=(7.5, 4.5))
plt.plot(angles_fins, gir_fins, color="tab:blue")
for a in angles_sense_gir:
    plt.axvline(a, color="tab:red", linestyle="--")
plt.xlabel("Angle del vector de partida (graus)")
plt.ylabel("Gir que li fa la matriu (graus)")
plt.title("Dues direccions, i només dues, que la matriu no gira")
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
Surten exactament **dues** direccions, a **31.70** i **121.70** graus, amb un gir residual
de 0.011 i 0.028 graus (no és zero exacte perquè la reixa té pas de 0.05 graus i el valor
de veritat cau entremig). I fixeu-vos en la diferència entre les dues: **90 graus justos**.
Res del que hem fet fins aquí obligava a això.

Ara calculem-les sense provar cap angle.
"""))

A(md(r"""
### Per què `eigh` i no `eig`

NumPy té dues funcions:

- `np.linalg.eig` serveix per a **qualsevol** matriu quadrada. Els valors propis poden
  sortir **complexos** (una rotació pura no té cap direcció que no giri, dins dels reals) i
  els vectors propis no tenen cap raó per ser perpendiculars entre ells.
- `np.linalg.eigh` és només per a matrius **simètriques** (la `h` és d'*hermitiana*, que en
  reals vol dir simètrica). Aprofita la simetria i garanteix dues coses:
  1. tots els valors propis són **reals**;
  2. els vectors propis són **ortogonals** entre ells.

Aquestes dues garanties són un teorema (el teorema espectral) i no les demostrarem aquí.
Però la matriu de covariància **és simètrica sempre**, per construcció, com hem comprovat a
la secció 3. Per tant, per al PCA sempre toca `eigh`: és més ràpida, més estable
numèricament, i retorna els valors propis ja ordenats de menor a major.
"""))

A(code("""
vaps, veps = np.linalg.eigh(A_demo)     # vaps: valors propis, veps: vectors propis

print("Valors propis (ordenats de menor a major):", vaps)
print("Vectors propis, un per COLUMNA:")
print(veps)

print("\\n--- Comprovem Av = lambda*v per a cadascun ---")
for i in range(len(vaps)):
    v = veps[:, i]
    esquerra = A_demo @ v
    dreta = vaps[i] * v
    print(f"  lambda = {vaps[i]:.4f}   A@v = {esquerra}   lambda*v = {dreta}"
          f"   iguals: {np.allclose(esquerra, dreta)}")

# I els seus angles, per comparar-los amb els de la reixa fina
angles_veps = np.degrees(np.arctan2(veps[1], veps[0])) % 180
print("\\nAngles dels vectors propis:", np.round(angles_veps, 4))
print("Angles trobats amb la reixa fina:", np.round(np.sort(angles_sense_gir), 4))
"""))

A(code("""
# Ortogonalitat: el producte escalar entre vectors propis diferents ha de ser 0
print(f"v1 · v2 = {veps[:, 0] @ veps[:, 1]:.2e}")

# I cada un té norma 1: eigh els retorna normalitzats
print("Normes:", np.linalg.norm(veps, axis=0))

# Tot junt: la matriu de vectors propis és ortogonal, V.T @ V = I
print("\\nV.T @ V =")
print(veps.T @ veps)
"""))

A(code("""
plt.figure(figsize=(6.5, 6.5))

# el mateix núvol de fons, en gris clar
for k in range(V.shape[1]):
    plt.arrow(0, 0, AV[0, k], AV[1, k], color="lightgray", width=0.004,
              length_includes_head=True, head_width=0.05)

colors = ["tab:red", "tab:green"]
for i in range(2):
    v = veps[:, i]
    Av = A_demo @ v
    plt.arrow(0, 0, v[0], v[1], color=colors[i], width=0.02,
              length_includes_head=True, head_width=0.12)
    plt.arrow(0, 0, Av[0], Av[1], color=colors[i], width=0.02, linestyle=":",
              length_includes_head=True, head_width=0.12, alpha=0.55)
    plt.plot([], [], color=colors[i], linewidth=3,
             label=f"$v_{i+1}$ i $Av_{i+1}$, $\\\\lambda = {vaps[i]:.3f}$")

plt.gca().set_aspect("equal")
plt.xlim(-4.2, 4.2)
plt.ylim(-4.2, 4.2)
plt.xlabel("primera coordenada")
plt.ylabel("segona coordenada")
plt.title("Els vectors propis: la matriu els estira sense girar-los")
plt.legend(loc="upper left")
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
Els valors propis són **1.382** i **3.618**, els dos reals, i el producte escalar entre els
dos vectors propis és de l'ordre de $10^{-17}$: ortogonals, com `eigh` promet. Els seus
angles són **121.7175** i **31.7175** graus: la reixa fina havia dit 121.70 i 31.70 a base
de provar 3601 direccions, i `eigh` dóna el valor exacte sense provar-ne cap.

Al dibuix, cada fletxa de color continu i la seva versió puntejada estan **sobre la mateixa
línia**: la matriu les ha estirat per un factor de 1.382 i de 3.618 respectivament, sense
moure-les de direcció.
"""))

# ---------------------------------------------------------------- 5
A(md(r"""
## 5. El pas clau: la direcció de màxima variància

Ara ajuntem les dues coses. Torneu a la pregunta del principi, però amb només dues columnes
d'Iris per poder-ho dibuixar: `petal_llarg` i `petal_ample`.

Volem **projectar** les dades sobre una recta que passa per l'origen (les dades estan
centrades) i quedar-nos amb un sol número per flor en lloc de dos. Hi ha infinites rectes.
Quina triem? La que **conserva més informació**, i informació aquí vol dir variància: si
després de projectar totes les flors queden apilades al mateix lloc, hem perdut el que les
distingia.

### La variància de la projecció

La recta la representem amb un vector unitari $v$ (norma 1). La projecció de la flor $x_i$
(centrada) sobre aquesta direcció és l'escalar

$$t_i = x_i^\top v$$

i per a totes les flors de cop, $t = X_c v$, un vector de $n$ números. Quina és la seva
variància?

**Primer, la mitjana de $t$ és zero.** Per linealitat:

$$\bar{t} = \frac{1}{n}\sum_i x_i^\top v = \left(\frac{1}{n}\sum_i x_i\right)^{\!\top} v = 0^\top v = 0$$

perquè les dades estan centrades. Això ens estalvia el terme de la mitjana:

$$\mathrm{Var}(t) = \frac{1}{n}\sum_i (t_i - \bar{t})^2 = \frac{1}{n}\sum_i t_i^2 = \frac{1}{n} t^\top t$$

**Segon, substituïm $t = X_c v$:**

$$\mathrm{Var}(t) = \frac{1}{n} (X_c v)^\top (X_c v) = \frac{1}{n} v^\top X_c^\top X_c v = v^\top \left(\frac{1}{n} X_c^\top X_c\right) v$$

I el parèntesi és la matriu de covariància de la secció 3. Per tant:

$$\boxed{\mathrm{Var}(X_c v) = v^\top C v}$$

El problema queda formulat així: **trobar el vector unitari $v$ que maximitza
$v^\top C v$**. La restricció $\|v\| = 1$ és imprescindible; sense ella només caldria fer
$v$ gran per fer créixer el valor, i no seria una direcció, seria una escala.
"""))

A(code("""
X2 = X_iris[:, [2, 3]]                  # petal_llarg, petal_ample
X2_c = X2 - X2.mean(axis=0)
C2 = X2_c.T @ X2_c / len(X2_c)

print("C2 =")
print(C2)

# Comprovem la fórmula v.T @ C @ v amb una direcció qualsevol, posem 30 graus
v_prova = np.array([np.cos(np.radians(30)), np.sin(np.radians(30))])
t_prova = X2_c @ v_prova

print(f"\\nDirecció de 30 graus, v = {v_prova}")
print(f"  variància de la projecció, calculada amb np.var: {t_prova.var():.6f}")
print(f"  v.T @ C2 @ v:                                    {v_prova @ C2 @ v_prova:.6f}")
"""))

A(md(r"""
Els dos números coincideixen, **3.580461**. La fórmula és correcta. Ara la força bruta:
recorrem tots els angles de 0 a 180 graus (de 180 a 360 es repeteix, perquè $v$ i $-v$
defineixen la mateixa recta) amb pas de 0.1 graus, i mirem on és màxima.
"""))

A(code("""
angles_graus = np.arange(0, 180, 0.1)   # 1800 direccions
variancies = np.empty_like(angles_graus)

for k, a in enumerate(angles_graus):
    v = np.array([np.cos(np.radians(a)), np.sin(np.radians(a))])
    variancies[k] = (X2_c @ v).var()    # np.var fa servir ddof=0, com la nostra C

i_max = variancies.argmax()
i_min = variancies.argmin()

print(f"Màxim:  angle {angles_graus[i_max]:.1f} graus, variància {variancies[i_max]:.6f}")
print(f"Mínim:  angle {angles_graus[i_min]:.1f} graus, variància {variancies[i_min]:.6f}")
print(f"Diferència entre els dos angles: {angles_graus[i_min] - angles_graus[i_max]:.1f} graus")
"""))

A(code("""
plt.figure(figsize=(7.5, 4.5))
plt.plot(angles_graus, variancies, color="tab:blue")
plt.axvline(angles_graus[i_max], color="tab:red", linestyle="--",
            label=f"màxim a {angles_graus[i_max]:.1f}°")
plt.scatter([angles_graus[i_max]], [variancies[i_max]], color="tab:red", zorder=3)
plt.xlabel("Angle de la direcció de projecció (graus)")
plt.ylabel("Variància de les dades projectades")
plt.title("Força bruta: variància en funció de l'angle")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
La força bruta dóna **22.8 graus**, amb una variància projectada de **3.636830**. El mínim
cau a **112.8 graus**, exactament 90 graus més enllà: la direcció que menys conserva és
perpendicular a la que més conserva. Això no és casualitat, i ho explica el que ve ara.

### El mateix angle, sense provar cap angle

Calculem els vectors propis de $C_2$ amb `eigh`, els ordenem per valor propi descendent, i
mirem l'angle del primer.
"""))

A(code("""
vaps2, veps2 = np.linalg.eigh(C2)

ordre = np.argsort(vaps2)[::-1]          # de major a menor
vaps2 = vaps2[ordre]
veps2 = veps2[:, ordre]

v1 = veps2[:, 0]
angle_v1 = np.degrees(np.arctan2(v1[1], v1[0])) % 180    # mod 180: v i -v són la mateixa recta

print("Valors propis (descendent):", vaps2)
print("Primer vector propi:", v1)
print()
print(f"Angle del primer vector propi:  {angle_v1:.4f} graus")
print(f"Angle trobat per força bruta:   {angles_graus[i_max]:.4f} graus")
print(f"Diferència:                     {abs(angle_v1 - angles_graus[i_max]):.4f} graus")
print()
print(f"Primer valor propi:             {vaps2[0]:.6f}")
print(f"Variància màxima (força bruta):  {variancies[i_max]:.6f}")
print(f"v1.T @ C2 @ v1:                 {v1 @ C2 @ v1:.6f}")
"""))

A(md(r"""
Aquí està el resultat del quadern:

| | Força bruta | Vector propi |
|---|---|---|
| Angle | 22.8 graus | **22.8126** graus |
| Variància | 3.636830 | **3.636830** |

L'angle coincideix fins a la resolució de la reixa que hem provat (el pas era de 0.1 graus,
així que 22.8 és el millor que la força bruta podia dir), i la variància coincideix a totes
les xifres.

**La direcció de màxima variància és el vector propi de $C$ amb el valor propi més gran, i
aquell valor propi és la variància que s'aconsegueix.** Això s'està veient, no s'està
demostrant: la demostració es fa amb multiplicadors de Lagrange i la deixem fora d'aquest
quadern. El que sí que podem dir és d'on ve la intuïció: $v^\top C v$ amb $\|v\|=1$ és
màxim quan $v$ apunta cap on la transformació $C$ estira més, i «cap on $C$ estira més» és
literalment la definició de vector propi dominant.

I la segona observació de la força bruta també queda explicada: el mínim cau a 90 graus del
màxim perquè $C$ és **simètrica**, i per tant `eigh` garanteix que els seus vectors propis
són **ortogonals**. La direcció de variància mínima és el segon vector propi. Dues coses que
semblaven independents (la geometria del núvol i l'àlgebra de la matriu) són la mateixa
cosa.

Un últim número que lliga la secció 3 amb aquesta: la suma dels valors propis val
**3.672636**, i la traça de $C_2$ també. Els valors propis **reparteixen** la variància
total; no en creen ni en perden.
"""))

A(code("""
print(f"Suma dels valors propis: {vaps2.sum():.6f}")
print(f"Traça de C2:             {np.trace(C2):.6f}")
"""))

A(code("""
plt.figure(figsize=(6.5, 6))
plt.scatter(X2_c[:, 0], X2_c[:, 1], s=18, color="tab:blue", alpha=0.6,
            label="flors (centrades)")

escala = 2.5
for i, color in zip(range(2), ["tab:red", "tab:green"]):
    v = veps2[:, i]
    llarg = escala * np.sqrt(vaps2[i])       # llargada proporcional a la desviació típica
    plt.plot([-llarg * v[0], llarg * v[0]], [-llarg * v[1], llarg * v[1]],
             color=color, linewidth=2.5,
             label=f"vector propi {i+1}, $\\\\lambda$ = {vaps2[i]:.3f}")

plt.gca().set_aspect("equal")
plt.xlabel("petal_llarg centrada (cm)")
plt.ylabel("petal_ample centrada (cm)")
plt.title("Les dues direccions pròpies del núvol de punts")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
La línia vermella és la direcció on el núvol és més llarg; la verda, perpendicular, és on és
més estret. Les llargades del dibuix són proporcionals a $\sqrt{\lambda_i}$, és a dir a la
desviació típica en cada direcció.
"""))

# ---------------------------------------------------------------- 6
A(md(r"""
## 6. PCA sencer, implementat a mà

Tot el PCA són cinc passos, i ja n'hem fet quatre:

1. **Centrar** les dades: $X_c = X - \bar{x}$.
2. **Matriu de covariància**: $C = \frac{1}{n} X_c^\top X_c$.
3. **Vectors i valors propis** de $C$, amb `eigh` perquè $C$ és simètrica.
4. **Ordenar** per valor propi descendent: la primera component és la que més variància
   conserva.
5. **Projectar**: $Z = X_c V_k$, on $V_k$ són les $k$ primeres columnes de la matriu de
   vectors propis.

Vint línies de codi. No hi ha res més.
"""))

A(code("""
def pca_a_ma(X, k):
    \"\"\"PCA des de zero. Retorna (Z, vectors_propis, valors_propis, mitjana).

    Z: dades projectades, de forma (n, k)
    vectors_propis: (d, k), un per columna, ordenats per variància descendent
    valors_propis: (d,) TOTS els valors propis, ordenats descendent
    \"\"\"
    # 1. centrar
    mitjana = X.mean(axis=0)
    Xc = X - mitjana

    # 2. matriu de covariància (denominador n)
    C = Xc.T @ Xc / len(Xc)

    # 3. vectors i valors propis (eigh perquè C és simètrica)
    vaps, veps = np.linalg.eigh(C)

    # 4. ordenar de major a menor valor propi
    ordre = np.argsort(vaps)[::-1]
    vaps = vaps[ordre]
    veps = veps[:, ordre]

    # 5. projectar sobre les k primeres direccions
    Z = Xc @ veps[:, :k]

    return Z, veps[:, :k], vaps, mitjana


Z_iris, V_iris, vaps_iris, mitjana_iris = pca_a_ma(X_iris, k=2)

print("Forma original:", X_iris.shape, "-> forma projectada:", Z_iris.shape)
print("\\nValors propis:", vaps_iris)
print("Variància explicada per cadascun:", vaps_iris / vaps_iris.sum())
print(f"\\nLes dues primeres components conserven el "
      f"{100 * vaps_iris[:2].sum() / vaps_iris.sum():.2f} % de la variància total")
"""))

A(code("""
plt.figure(figsize=(7.5, 6))
for classe, nom, color in zip(range(3), iris.target_names,
                              ["tab:blue", "tab:orange", "tab:green"]):
    mascara = y_iris == classe
    plt.scatter(Z_iris[mascara, 0], Z_iris[mascara, 1], s=30, alpha=0.8,
                color=color, label=nom)

plt.xlabel("Primera component principal")
plt.ylabel("Segona component principal")
plt.title("Iris en 2 dimensions, amb el PCA fet a mà")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
Les tres espècies surten separades, sobretot `setosa`, que queda a part del tot. I aquí cal
aturar-se, perquè és el punt important d'aquesta secció:

**El PCA no ha vist `y_iris` en cap moment.** Torneu a mirar la funció `pca_a_ma`: rep `X` i
`k`, i prou. No hi ha etiquetes enlloc. Els colors del dibuix els hem posat **després**,
únicament per mirar el resultat.

Això és el que vol dir **aprenentatge no supervisat**: l'algorisme troba estructura a les
dades sense que ningú li digui quina és la resposta correcta. El PCA no ha buscat separar
espècies; ha buscat direccions de màxima variància. Que les espècies surtin separades és una
conseqüència: **la variabilitat més gran d'aquest dataset és, de fet, la diferència entre
espècies**. Podria no haver estat així, i sovint no ho és.

Les dues primeres components conserven el **97.77 %** de la variància: hem passat de 4
columnes a 2 perdent el 2.23 %.
"""))

# ---------------------------------------------------------------- 7
A(md(r"""
## 7. Comparació amb scikit-learn

`sklearn.decomposition.PCA` fa el mateix (per un camí diferent: fa servir la descomposició
en valors singulars en lloc de diagonalitzar $C$, que és més estable numèricament, però el
resultat matemàtic és el mateix). Comprovem-ho.
"""))

A(code("""
from sklearn.decomposition import PCA

pca_sk = PCA(n_components=2)
Z_sk = pca_sk.fit_transform(X_iris)      # fit_transform centra pel seu compte

print("Components de scikit-learn (una per FILA):")
print(pca_sk.components_)
print("\\nEls nostres vectors propis (els passem a files per comparar):")
print(V_iris.T)
"""))

A(md(r"""
Mireu-ho amb calma abans de continuar. La segona fila coincideix xifra per xifra. **La
primera té tots els signes girats.**
"""))

A(code("""
print("Diferència directa (amb signe) entre components:",
      np.abs(pca_sk.components_ - V_iris.T).max())
print("Diferència directa entre projeccions:",
      np.abs(Z_sk - Z_iris).max())
"""))

A(md(r"""
### El parany del signe

La diferència directa dóna **1.7134** a les components i **7.5913** a les projeccions. Si
haguéssiu escrit un test amb `np.allclose(Z_sk, Z_iris)` diria que la vostra implementació
està malament. **No ho està.**

El motiu és a la definició mateixa. Si $Av = \lambda v$, aleshores multiplicant els dos
costats per $-1$:

$$A(-v) = \lambda(-v)$$

$-v$ també és un vector propi, amb el mateix valor propi. **La definició no fixa el signe**,
i la norma 1 tampoc: totes dues opcions tenen norma 1. Cada llibreria (i cada versió de cada
llibreria, i cada plataforma) tria un criteri intern, i no té per què ser el mateix.

Geomètricament és evident: la recta de màxima variància és una recta, no una fletxa. Girar
el vector 180 graus dóna la mateixa recta. L'únic efecte és que el gràfic surt reflectit, i
les projeccions canvien de signe totes alhora.

La comprovació correcta és fer-la en **valor absolut**.
"""))

A(code("""
print("Diferència en valor absolut, components:",
      np.abs(np.abs(pca_sk.components_) - np.abs(V_iris.T)).max())
print("Diferència en valor absolut, projeccions:",
      np.abs(np.abs(Z_sk) - np.abs(Z_iris)).max())

# Quina component està girada, exactament: el producte escalar ens ho diu
signes = np.sign(np.sum(pca_sk.components_ * V_iris.T, axis=1))
print("\\nSigne relatiu de cada component (1 = igual, -1 = girada):", signes)

# I amb els signes arreglats, la coincidència és exacta
Z_alineat = Z_iris * signes
print("Diferència després d'alinear els signes:", np.abs(Z_sk - Z_alineat).max())
"""))

A(md(r"""
En valor absolut la diferència és de $2 \cdot 10^{-14}$ a les components i
$3.8 \cdot 10^{-14}$ a les projeccions: coincidència exacta dins de la precisió dels
`float64`. El vector de signes és `[-1, 1]`: la primera component està girada, la segona no.
Alineant els signes, la diferència amb signe baixa també a $10^{-14}$.

### La variància explicada

La fracció de variància que conserva la component $i$ és

$$r_i = \frac{\lambda_i}{\sum_j \lambda_j}$$

A scikit-learn això és `explained_variance_ratio_`.
"""))

A(code("""
ratio_propi = vaps_iris[:2] / vaps_iris.sum()

print("La nostra variància explicada:  ", ratio_propi)
print("explained_variance_ratio_:      ", pca_sk.explained_variance_ratio_)
print("Diferència:                     ",
      np.abs(ratio_propi - pca_sk.explained_variance_ratio_).max())

print("\\nEls nostres valors propis:      ", vaps_iris[:2])
print("explained_variance_ (sklearn):  ", pca_sk.explained_variance_)
print("Factor entre els dos:           ", pca_sk.explained_variance_ / vaps_iris[:2])
print(f"n / (n-1) = {n / (n - 1):.6f}")
"""))

A(md(r"""
La **ràtio** coincideix a $10^{-15}$: 0.9246 i 0.0531. Els **valors propis**, en canvi, no:
nosaltres tenim 4.2001 i 0.2411, i scikit-learn 4.2282 i 0.2427. El factor entre els dos és
exactament **1.006711**, que és $n/(n-1) = 150/149$: `sklearn` fa servir el denominador
$n-1$ a `explained_variance_`, com `np.cov`. A la ràtio el factor se'n va perquè apareix al
numerador i al denominador. Un altre lloc on `ddof` es cola.
"""))

# ---------------------------------------------------------------- 8
A(md(r"""
## 8. Quantes components? La variància explicada com a criteri

Tornem a la pregunta del principi: el dataset de **càncer de mama**, 569 pacients i 30
columnes. Volem reduir-lo, però a quantes dimensions?

El criteri habitual: dibuixar la **variància explicada acumulada** i tallar on s'arriba a un
llindar, normalment el 95 %. És un criteri arbitrari, però és un criteri, i respon amb un
número.

Les columnes del dataset van des de centenars (l'àrea mitjana) fins a centèsimes (la
concavitat). Per tant **escalem abans**; el motiu és a la secció 10 i és important.
"""))

A(code("""
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler

cancer = load_breast_cancer()
X_can = StandardScaler().fit_transform(cancer.data)
y_can = cancer.target

print("Forma:", X_can.shape)

# PCA a mà. Ens interessen tots els valors propis, no només les 2 components
_, _, vaps_can, _ = pca_a_ma(X_can, k=2)

ratio_can = vaps_can / vaps_can.sum()
acumulada = np.cumsum(ratio_can)

for i in range(12):
    print(f"  component {i+1:2d}: {100*ratio_can[i]:5.2f} %   "
          f"acumulat {100*acumulada[i]:6.2f} %")
"""))

A(code("""
k95 = int(np.argmax(acumulada >= 0.95) + 1)     # argmax sobre booleans: la primera True
print(f"Components necessàries per al 95 % de la variància: {k95}")
print(f"Variància acumulada amb {k95} components: {100*acumulada[k95-1]:.2f} %")
print(f"Amb {k95-1} components: {100*acumulada[k95-2]:.2f} %, que no hi arriba")
"""))

A(code("""
plt.figure(figsize=(7.5, 4.5))
plt.plot(np.arange(1, len(acumulada) + 1), 100 * acumulada, "o-", color="tab:blue",
         markersize=4)
plt.axhline(95, color="tab:red", linestyle="--", label="llindar del 95 %")
plt.axvline(k95, color="tab:green", linestyle="--", label=f"{k95} components")
plt.xlabel("Nombre de components principals")
plt.ylabel("Variància explicada acumulada (%)")
plt.title("Càncer de mama: 30 columnes, quantes en fan falta")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
La resposta és **10 components**. Amb 10 de les 30 dimensions es conserva el **95.16 %** de
la variància; amb 9, el 93.99 %, que no arriba al llindar.

### Ha servit de res?

Dir «hem passat de 30 a 10» no és un resultat fins que es mesura. Entrenem una regressió
logística amb les 30 columnes i amb les 10 components, i comparem precisió i temps.

Una precaució metodològica: el PCA s'ajusta **només amb les dades d'entrenament** i després
s'aplica al test. Ajustar-lo amb tot el dataset seria deixar que informació del test
s'infiltri al preprocessament.

Els temps d'entrenament aquí són de mil·lisegons, i una sola mesura seria pur soroll: fem la
mitjana de 20 entrenaments.
"""))

A(code("""
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X_tr, X_te, y_tr, y_te = train_test_split(X_can, y_can, test_size=0.3,
                                          random_state=42, stratify=y_can)


def entrena_i_cronometra(Xa, ya, Xb, yb, repeticions=20):
    \"\"\"Entrena una regressió logística `repeticions` vegades. Retorna (precisió, ms).\"\"\"
    t0 = time.perf_counter()
    for _ in range(repeticions):
        model = LogisticRegression(max_iter=5000).fit(Xa, ya)
    ms = 1000 * (time.perf_counter() - t0) / repeticions
    return model.score(Xb, yb), ms


# cas 1: les 30 columnes
acc_30, ms_30 = entrena_i_cronometra(X_tr, y_tr, X_te, y_te)

# cas 2: les k95 components. El PCA s'ajusta NOMÉS amb l'entrenament
pca_red = PCA(n_components=k95).fit(X_tr)
acc_k, ms_k = entrena_i_cronometra(pca_red.transform(X_tr), y_tr,
                                   pca_red.transform(X_te), y_te)

print(f"30 columnes    -> precisió {acc_30:.4f}   temps {ms_30:.2f} ms")
print(f"{k95} components  -> precisió {acc_k:.4f}   temps {ms_k:.2f} ms")
print(f"\\nPrecisió perduda: {100*(acc_30 - acc_k):.2f} punts")
print(f"Temps: {ms_30/ms_k:.2f} vegades més ràpid")
"""))

A(md(r"""
Els números de la nostra execució:

| | Precisió al test | Temps d'entrenament |
|---|---|---|
| 30 columnes | **0.9825** | 3.2 ms |
| 10 components | **0.9708** | 2.7 ms |

Es perd **1.17 punts** de precisió i s'estalvia entre un 15 i un 20 % de temps, segons
l'execució. Amb un dataset d'aquesta mida el temps és irrellevant: 3.2 mil·lisegons contra
2.7 no justifica res, i els vostres números seran diferents dels nostres perquè depenen de
la màquina. La precisió, en canvi, és determinista i us ha de sortir exactament igual.
**El PCA, aquí, no s'ha de vendre com una optimització de velocitat.**

El que sí que val la pena retenir:

- La reducció **costa** precisió. Poca, però costa. Qui digui que el PCA és gratis
  s'equivoca.
- El guany real apareix quan $d$ és gran de veritat (milers de columnes: text, imatges) o
  quan el model que ve després escala malament amb la dimensió.
- I el guany segur, sempre: **ara podeu dibuixar les dades**, cosa que amb 30 columnes no
  podíeu.
"""))

# ---------------------------------------------------------------- 9
A(md(r"""
## 9. On el PCA falla

El PCA és una **projecció lineal**: multiplica les dades per una matriu. Aquesta és tota la
seva potència i tot el seu límit. Si l'estructura que voleu veure no és visible des de cap
direcció recta, el PCA no la trobarà, i no hi ha cap paràmetre que ho arregli.

L'exemple canònic: dos anells concèntrics. `make_circles` els genera.
"""))

A(code("""
from sklearn.datasets import make_circles

X_cer, y_cer = make_circles(n_samples=400, factor=0.3, noise=0.05, random_state=42)

plt.figure(figsize=(6, 6))
for classe, color, nom in zip([0, 1], ["tab:blue", "tab:orange"],
                              ["anell exterior", "anell interior"]):
    m = y_cer == classe
    plt.scatter(X_cer[m, 0], X_cer[m, 1], s=20, color=color, label=nom, alpha=0.8)
plt.gca().set_aspect("equal")
plt.xlabel("primera coordenada")
plt.ylabel("segona coordenada")
plt.title("Dos anells concèntrics: les dades originals")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""))

A(code("""
pca_cer = PCA(n_components=2).fit(X_cer)
Z_cer = pca_cer.transform(X_cer)

print("Variància explicada:", pca_cer.explained_variance_ratio_)

# Projectem sobre la primera component i mirem si els dos anells queden separats
z1 = Z_cer[:, :1]
print(f"\\nRang de la 1a component, anell exterior: "
      f"[{z1[y_cer==0].min():.3f}, {z1[y_cer==0].max():.3f}]")
print(f"Rang de la 1a component, anell interior: "
      f"[{z1[y_cer==1].min():.3f}, {z1[y_cer==1].max():.3f}]")

acc_lineal = LogisticRegression().fit(z1, y_cer).score(z1, y_cer)
print(f"\\nPrecisió d'una logística sobre la 1a component: {acc_lineal:.4f}")
"""))

A(md(r"""
Les dues components expliquen **50.42 %** i **49.58 %**: el núvol és igual de gran en totes
direccions, i el PCA no té cap direcció preferida a la qual agafar-se. Els rangs de la
primera component se **solapen del tot** per als dos anells, i un classificador lineal a
sobre encerta el **50.00 %**, que és el que encertaria llançant una moneda.

No és un PCA mal configurat. **Cap projecció lineal pot separar dos anells concèntrics**:
qualsevol recta que passi pel centre travessa els dos anells.

### Què s'ha de fer

Canviar d'eina, no de paràmetres. El que aquestes dades demanen és una tècnica **no
lineal**:

- **`KernelPCA`**: aplica el truc del kernel que ja vau veure a l'SVM. Calcula el PCA en un
  espai de dimensió molt més alta, definit implícitament pel kernel, sense construir-lo. Amb
  kernel RBF, dos punts del mateix anell tenen una similitud alta i dos d'anells diferents
  una similitud baixa, i aquesta informació sí que és projectable.
- **`TSNE`** i **`UMAP`**: tècniques de visualització que intenten conservar les distàncies
  locals. Funcionen molt bé per mirar dades, però deformen les distàncies globals i no donen
  cap transformació aplicable a dades noves. No les fem servir aquí: amb 400 punts `TSNE`
  triga uns 3 segons, i el resultat no afegeix res al que ja mostra `KernelPCA`.

Fem-ho amb `KernelPCA` i kernel RBF, `gamma=4`.
"""))

A(code("""
from sklearn.decomposition import KernelPCA

Z_ker = KernelPCA(n_components=2, kernel="rbf", gamma=4.0).fit_transform(X_cer)

k1 = Z_ker[:, :1]
print(f"Rang de la 1a component, anell exterior: "
      f"[{k1[y_cer==0].min():.4f}, {k1[y_cer==0].max():.4f}]")
print(f"Rang de la 1a component, anell interior: "
      f"[{k1[y_cer==1].min():.4f}, {k1[y_cer==1].max():.4f}]")

acc_kernel = LogisticRegression().fit(k1, y_cer).score(k1, y_cer)
print(f"\\nPrecisió d'una logística sobre la 1a component del KernelPCA: {acc_kernel:.4f}")
"""))

A(code("""
fig, axs = plt.subplots(1, 2, figsize=(12, 5))
for ax, Z, titol in [(axs[0], Z_cer, "PCA lineal: els anells segueixen encaixats"),
                     (axs[1], Z_ker, "KernelPCA (RBF): separats per la 1a component")]:
    for classe, color, nom in zip([0, 1], ["tab:blue", "tab:orange"],
                                  ["anell exterior", "anell interior"]):
        m = y_cer == classe
        ax.scatter(Z[m, 0], Z[m, 1], s=20, color=color, label=nom, alpha=0.8)
    ax.set_xlabel("1a component")
    ax.set_ylabel("2a component")
    ax.set_title(titol)
    ax.legend()
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""))

A(md(r"""
Amb el kernel RBF, la primera component separa els anells **del tot**: l'anell exterior cau
a l'interval $[-0.4044, -0.3371]$ i l'interior a $[0.1469, 0.5497]$, sense cap solapament, i
una logística sobre aquest únic número encerta el **100 %**. S'ha passat del 50 % al 100 %
canviant d'eina, no ajustant-la.

El preu: **`KernelPCA` no dóna components interpretables**. Al PCA lineal, cada component és
una combinació de les columnes originals i es pot llegir («aquesta component és sobretot la
mida del tumor»). Al kernel no hi ha cap combinació de columnes: la transformació viu en un
espai que no s'arriba a construir. Es guanya capacitat de separar i es perd capacitat
d'explicar.
"""))

# ---------------------------------------------------------------- 10
A(md(r"""
## 10. Nota imprescindible: el PCA exigeix escalar

Això no és un consell de bones pràctiques; és una condició de funcionament, i s'ha de veure
trencada un cop per no oblidar-ho mai.

El PCA busca direccions de **màxima variància**. La variància té unitats: es mesura en el
quadrat de les unitats de la columna. Si una columna està en centenars i una altra en
decimals, la primera tindrà una variància milers de vegades més gran, i el PCA li donarà
tota l'atenció, **no perquè contingui més informació sinó perquè està mesurada en una unitat
més gran**.

El dataset **Wine** ho ensenya en un pas: 178 vins, 13 columnes químiques amb unitats
completament diferents.
"""))

A(code("""
from sklearn.datasets import load_wine

wine = load_wine()
X_wine = wine.data
y_wine = wine.target

variancies_wine = X_wine.var(axis=0)
ordre_w = np.argsort(variancies_wine)[::-1]

print("Variància de cada columna, de major a menor:")
for i in ordre_w:
    print(f"  {wine.feature_names[i]:<32} {variancies_wine[i]:>12.4f}")
"""))

A(md(r"""
`proline` té una variància de **98609.60** i `nonflavanoid_phenols` de **0.0154**: una
proporció de **6 milions a 1**. La traça de la matriu de covariància (la variància total) la
marca pràcticament sencera `proline`. Feu el PCA així i ja sabeu quin serà el resultat.
"""))

A(code("""
# Cas A: sense escalar
pca_A = PCA(n_components=2).fit(X_wine)
Z_A = pca_A.transform(X_wine)

print("SENSE escalar")
print("  variància explicada:", pca_A.explained_variance_ratio_)
i_dom = int(np.argmax(np.abs(pca_A.components_[0])))
print(f"  la 1a component és sobretot '{wine.feature_names[i_dom]}', "
      f"amb càrrega {pca_A.components_[0][i_dom]:.4f}")
print("  càrregues de la 1a component:", np.round(pca_A.components_[0], 4))

# Cas B: amb escalar
X_wine_esc = StandardScaler().fit_transform(X_wine)
pca_B = PCA(n_components=2).fit(X_wine_esc)
Z_B = pca_B.transform(X_wine_esc)

print("\\nAMB StandardScaler")
print("  variància explicada:", pca_B.explained_variance_ratio_)
print(f"  acumulada amb 2 components: {100*pca_B.explained_variance_ratio_.sum():.2f} %")
print("  càrregues de la 1a component:", np.round(pca_B.components_[0], 4))
"""))

A(code("""
fig, axs = plt.subplots(1, 2, figsize=(12, 5))
for ax, Z, titol in [(axs[0], Z_A, "Sense escalar: la 1a component és 'proline'"),
                     (axs[1], Z_B, "Amb StandardScaler: les 3 varietats se separen")]:
    for classe, color in zip(range(3), ["tab:blue", "tab:orange", "tab:green"]):
        m = y_wine == classe
        ax.scatter(Z[m, 0], Z[m, 1], s=25, color=color, alpha=0.8,
                   label=wine.target_names[classe])
    ax.set_xlabel("1a component")
    ax.set_ylabel("2a component")
    ax.set_title(titol)
    ax.legend()
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""))

A(md(r"""
El desastre, en números:

| | 1a component | 2a component | Les dues |
|---|---|---|---|
| Sense escalar | **99.81 %** | 0.17 % | 99.98 % |
| Amb `StandardScaler` | 36.20 % | 19.21 % | 55.41 % |

Sense escalar, el 99.81 % de «variància explicada» sona magnífic i no val res: la càrrega de
`proline` a la primera component és **0.9998**, i la de totes les altres 12 columnes és
pràcticament zero. El PCA no ha reduït res; ha triat una columna i ha ignorat el dataset. Al
gràfic de l'esquerra, l'eix horitzontal **és** `proline` en unitats disfressades, i les tres
varietats queden barrejades.

Amb escalat, els números són més modestos (55.41 % amb dues components) i el resultat és
molt millor: les tres varietats es distingeixen. **Un percentatge de variància explicada alt
no és senyal de res si les columnes no estan escalades.**

Quan no cal escalar: quan totes les columnes ja estan a la mateixa unitat i la diferència de
variància entre elles és informació real. Per exemple, els píxels d'una imatge en escala de
grisos, tots de 0 a 255. En qualsevol altre cas, escaleu.
"""))

# ---------------------------------------------------------------- exercicis
A(md(r"""
## 11. Exercicis

Quatre exercicis. No fan servir res que no surti en aquest quadern, i cada enunciat porta el
número que us ha de sortir per saber si ho heu fet bé.
"""))

A(md(r"""
### Exercici 1 - PCA a mà sobre els dígits

Carregueu `load_digits()`: 1797 imatges de 8x8 píxels, aplanades en **64 columnes**, amb
valors de 0 a 16. Apliqueu-hi la funció `pca_a_ma` amb `k=2` i dibuixeu el resultat pintant
les 10 xifres amb colors diferents (useu `plt.scatter(..., c=y, cmap="tab10")` i
`plt.colorbar()`).

Responeu també: quina fracció de variància conserven les dues primeres components?

**Com saps que ho has fet bé**: la primera component ha d'explicar al voltant del **14.9 %**
i la segona al voltant del **13.6 %**, un **28.5 %** entre les dues. Al gràfic han de quedar
grups reconeixibles (el 0 i el 6, ben separats) però amb molt de solapament: amb el 28 % de
la variància no es poden fer miracles.

**Nota**: els píxels ja estan tots a la mateixa unitat (0-16), així que aquí **no** cal
`StandardScaler`.
"""))

A(code("""
from sklearn.datasets import load_digits

# digits = load_digits()
# X_dig, y_dig = digits.data, digits.target
#
# 1. aplica pca_a_ma amb k=2
# 2. dibuixa les dues components amb un color per xifra
# 3. imprimeix la variància explicada de les dues primeres components
"""))

A(md(r"""
### Exercici 2 - Reconstruir les dades i mesurar què s'ha perdut

Projectar és multiplicar per $V_k$; **reconstruir** és tornar enrere. Com que les columnes de
$V$ són ortonormals, la inversa de la projecció és la transposada:

$$\hat{X} = Z V_k^\top + \bar{x}$$

Amb $k$ menor que el nombre de columnes, $\hat{X}$ no serà igual a $X$: el que s'ha perdut
són les components que heu llençat. Mesureu-ho amb l'error quadràtic mitjà arrel:

$$\mathrm{RMSE} = \sqrt{\frac{1}{n \cdot d}\sum_{i,j}(X_{ij} - \hat{X}_{ij})^2}$$

Feu-ho sobre `load_digits()` per a $k = 2$, $10$ i $30$, i imprimiu els tres errors al
costat de la variància acumulada corresponent.

**Com saps que ho has fet bé**: amb $k=2$ l'RMSE ha de ser al voltant de **3.66**; amb
$k=10$, de **2.22**; amb $k=30$, de **0.88**. La variància acumulada corresponent és 28.5 %,
73.8 % i 95.9 %. Comproveu que l'error baixa quan la variància acumulada puja, i que amb
$k = 64$ (totes les components) l'error és pràcticament zero ($10^{-14}$).
"""))

A(code("""
# Recorda que pca_a_ma retorna (Z, veps_k, vaps_tots, mitjana)
#
# for k in [2, 10, 30]:
#     Z, Vk, vaps, mitjana = pca_a_ma(X_dig, k)
#     X_reconstruit = ...          # Z @ Vk.T + mitjana
#     rmse = ...                   # arrel de la mitjana dels quadrats de la diferència
#     acumulat = ...               # suma dels k primers vaps dividida per la suma de tots
#     print(...)
"""))

A(md(r"""
### Exercici 3 - Comprovar l'ortogonalitat de tots els vectors propis alhora

A la secció 4 hem comprovat amb un producte escalar que dos vectors propis eren ortogonals.
Amb 64 vectors propis això són $\binom{64}{2} = 2016$ productes escalars, i no cal cap
bucle: si totes les columnes de $V$ són ortogonals entre elles i de norma 1, aleshores

$$V^\top V = I$$

Calculeu la matriu completa de vectors propis dels dígits (els 64, no només 2) i comproveu
aquesta igualtat amb **un sol producte de matrius**. Mesureu la desviació màxima respecte de
la identitat amb `np.abs(V.T @ V - np.eye(64)).max()`.

**Com saps que ho has fet bé**: la desviació màxima ha de ser de l'ordre de **$10^{-15}$**,
no zero exacte. Expliqueu en una línia per què no és zero exacte.

Comproveu també que $V V^\top = I$ i penseu per què això també ha de ser cert quan $V$ és
quadrada (i per què **no** ho seria si us quedéssiu només amb $k$ columnes).
"""))

A(code("""
# Pista: per obtenir els 64 vectors propis, crida pca_a_ma amb k = X_dig.shape[1]
#
# _, V_tots, _, _ = pca_a_ma(X_dig, k=64)
# comprova V.T @ V == I i V @ V.T == I, i imprimeix la desviació màxima
"""))

A(md(r"""
### Exercici 4 - Del 95 % al 99 %

A la secció 8 heu vist que el dataset de càncer necessita 10 components per al 95 %.
Calculeu quantes en fan falta per al **99 %**, i quantes per al 90 %. Feu una taula amb els
tres llindars (90, 95, 99) i el nombre de components de cadascun.

Després entreneu la regressió logística amb els tres talls i afegiu la precisió al test a la
taula (feu servir el mateix `train_test_split` de la secció 8).

**Com saps que ho has fet bé**: per al 99 % en fan falta **17** components, i per al 90 %,
**7**. Fixeu-vos en el que això vol dir: passar del 95 % al 99 % de variància costa **7
components més**, gairebé el doble, i després compareu-ho amb el que guanyeu en precisió.
Escriviu una frase dient quin dels tres talls triaríeu i per què.
"""))

A(code("""
# for llindar in [0.90, 0.95, 0.99]:
#     k = int(np.argmax(acumulada >= llindar) + 1)
#     entrena amb k components i guarda la precisió
#     print(llindar, k, precisió)
"""))

# ---------------------------------------------------------------- resum
A(md(r"""
## 12. Resum

Què s'ha demostrat en aquest quadern, amb números:

- **En dimensió alta les distàncies deixen de distingir.** La ràtio $d_{\min}/d_{\max}$
  passa de 0.0017 en dimensió 2 a 0.8020 en dimensió 500, i l'esfera inscrita ocupa
  $10^{-28}$ del cub en dimensió 50. Els models basats en distàncies perden el sentit abans
  de deixar de funcionar.
- **La matriu de covariància és un sol producte de matrius**: $C = \frac{1}{n}X_c^\top X_c$
  coincideix amb `np.cov(ddof=0)` fins a $4\cdot10^{-16}$, és simètrica exactament, i la
  seva traça és la variància total.
- **El denominador importa, i les funcions no es posen d'acord**: `np.var` fa servir
  `ddof=0` i `np.cov` fa servir `ddof=1`. A Iris la diferència és del 0.7 %; amb poques
  mostres, molt més.
- **La variància de les dades projectades sobre un vector unitari $v$ és $v^\top C v$**,
  derivat en dos passos aprofitant que les dades estan centrades.
- **La direcció de màxima variància és el primer vector propi de $C$.** La força bruta sobre
  1800 angles dóna 22.8 graus amb variància 3.636830; `eigh` dóna 22.8126 graus amb valor
  propi 3.636830. Els dos camins arriben al mateix número, i el segon no ha provat cap angle.
- **`eigh` i no `eig`**, perquè $C$ és simètrica: valors propis reals i vectors propis
  ortogonals garantits, i això explica per què la direcció de variància mínima cau a 90 graus
  de la màxima.
- **El PCA complet són cinc passos i vint línies**, i coincideix amb scikit-learn fins a
  $2\cdot10^{-14}$ **en valor absolut**. Amb signe, la diferència és de 7.59, perquè
  $Av=\lambda v$ implica $A(-v)=\lambda(-v)$ i el signe no està definit. No és un error.
- **El PCA no mira les etiquetes.** A Iris, dues components conserven el 97.77 % de la
  variància i les tres espècies surten separades igualment. És el primer resultat no
  supervisat del curs.
- **Reduir costa precisió, i el temps no és l'argument.** Al càncer de mama, 10 de 30
  components conserven el 95.16 % de la variància i la precisió baixa de 0.9825 a 0.9708.
- **El PCA és lineal, i això és un límit dur.** Amb dos anells concèntrics la variància es
  reparteix 50/50 i un classificador sobre la primera component encerta el 50.00 %.
  `KernelPCA` amb RBF puja al 100 %: és un canvi d'eina, no d'ajust, i es paga perdent la
  interpretabilitat de les components.
- **Sense escalar, el PCA mesura unitats en lloc d'informació.** A Wine, la primera component
  sense escalar explica el 99.81 % i **és** `proline` amb càrrega 0.9998; amb
  `StandardScaler`, dues components expliquen el 55.41 % i les tres varietats se separen.

### Què hem deixat fora

- La **demostració** que el màxim de $v^\top C v$ amb $\|v\|=1$ s'assoleix al vector propi
  dominant. Es fa amb multiplicadors de Lagrange i pertoca a un curs de càlcul.
- El **teorema espectral**, que garanteix que una matriu simètrica té valors propis reals i
  vectors propis ortogonals. L'hem fet servir i comprovat numèricament, no demostrat.
- La **descomposició en valors singulars** (SVD), que és el camí pel qual scikit-learn calcula
  el PCA de veritat, i que evita construir $C$ explícitament. Dóna el mateix resultat i és
  numèricament més estable.
- Com escollir el kernel i la `gamma` del `KernelPCA`. Nosaltres hem posat `gamma=4` perquè
  funciona en aquest exemple.
"""))

info = escriu(cells, "Machine Learning/03_matematiques/MA_06_pca_vectors_propis.ipynb",
              titol_colab="MA_06_pca_vectors_propis.ipynb")
print(info)
