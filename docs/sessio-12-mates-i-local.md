# S12 · dilluns 2 de novembre · Treballar en local i les mates de base

Guió privat (no es publica). Substitueix la S12 prevista al guió del bloc 2 («Entrenament i
test»), que passa a una sessió posterior. Motiu: dimarts passat (Pe1 + Pp1) Colab es va penjar a
diversos alumnes, i l'alumnat no ha tingut mai una explicació de la matemàtica bàsica abans dels
models.

## Primera part, 40 min · Python i Jupyter en local

Guia a la web: **/installacio** («Treballar en local», al menú). Que la segueixin sols; tu passes
per les taules.

| Min | Què |
|---|---|
| 0-5 | Per què: el dimarts Colab va caure. En local no depens de Google. |
| 5-35 | Guia, passos 1-4. Els que acabin primer ajuden el del costat. |
| 35-40 | Pas 5: tothom obre `MA_01_algebra_lineal.ipynb` i executa la primera cel·la. |

**Errors previsibles:**
- `python` no es reconeix → no van marcar «Add python.exe to PATH». Que facin servir `py` o
  reinstal·lin marcant-ho.
- Ordinadors del centre sense permisos → l'instal·lador de python.org, amb «Install Now», va per
  usuari i no en demana. Si el proxy bloqueja `pip`, aquest grup segueix amb Colab avui.
- macOS → `python3` a tot arreu.
- Algú sense portàtil → Colab, com fins ara. El quadern és el mateix.

## Segona part, 75 min · De la notació a l'àlgebra lineal

A la pissarra, i cada idea tancada amb la línia de NumPy que la calcula (la teoria aterra al codi).
El quadern de referència és `MA_01`: les seccions entre parèntesis són on ho trobaran després.

| Min | Concepte | A la pissarra | La línia de codi |
|---|---|---|---|
| 15 | **La notació de les dades** | Un dataset és una taula $X$ de $n$ files (mostres) per $d$ columnes (característiques). $x_i$ és la fila $i$; $x_{ij}$, la cel·la. $\sum_{i=1}^{n}$ vol dir «suma-ho per a totes les files». La mitjana: $\bar{x} = \frac{1}{n}\sum x_i$. | `X.shape`, `X[i]`, `X[i, j]`, `X.sum(axis=0) / len(X)` contra `X.mean(axis=0)` |
| 15 | **Vector** (secció 1) | Una flor d'Iris és un punt de 4 dimensions i també una fletxa. Suma de vectors i producte per un escalar, dibuixats en 2D. | `a + b`, `3 * a` |
| 15 | **Norma i distància** (seccions 2-3) | Pitàgores en 2D → en $d$ dimensions: $\lVert x \rVert = \sqrt{\sum x_j^2}$. La distància entre dues flors és la norma de la resta. | `np.sqrt((x**2).sum())` contra `np.linalg.norm(x)`; `np.linalg.norm(a - b)` |
| 15 | **Producte escalar** (seccions 4-5) | $a \cdot b = \sum a_j b_j = \lVert a \rVert \lVert b \rVert \cos\theta$. Si és 0, són perpendiculars. Projectar és «quant d'$a$ va en la direcció de $b$». | `(a * b).sum()` contra `a @ b`; el cosinus |
| 15 | **Matriu = taula i transformació** (seccions 6-7) | Multiplicar una matriu per un vector és fer un producte escalar per fila. Una rotació de 2D com a exemple. I el punt d'arribada: **un model lineal entrenat és un vector de pesos $w$**, i predir tot el dataset és $Xw + b$. | `X @ w + b`, i comparar-ho amb un bucle de Python |

**La frase per tancar:** «A partir d'ara, cada model que veurem és alguna d'aquestes cinc coses:
distàncies (k veïns), productes escalars (regressió, SVM) o matrius (xarxes)».

## Per a casa

`MA_01_algebra_lineal.ipynb`, ja en local, amb els exercicis 1-4. És la comprovació que la
instal·lació funciona i la base de la S13 (k veïns), que fa servir la distància d'avui.

## Què canvia a la programació

La S12 prevista («Entrenament i test», amb `ML_00_demo_iris`) queda pendent. La manera menys
costosa d'encabir-la és començar la S13 amb els 25 minuts de «per què es parteix el conjunt» i
deixar per a casa la comparació dels cinc models.
