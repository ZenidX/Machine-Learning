# Treballar en local: Python i Jupyter al teu ordinador

Colab va bé fins que Google es penja. Amb Python i Jupyter instal·lats al teu ordinador, els quaderns
s'obren igual i no depens de ningú. Calen uns 20 minuts i 1 GB de disc.

Si en algun pas et surt un error, **copia el missatge sencer** i crida en Xavi. No t'inventis la
solució.

## 1. Instal·la Python 3.12

Descarrega'l de [python.org/downloads](https://www.python.org/downloads/). No facis servir el de la
Microsoft Store.

- **Windows:** a la primera pantalla de l'instal·lador, marca **«Add python.exe to PATH»** i després
  «Install Now». No calen permisos d'administrador.
- **macOS:** l'instal·lador `.pkg` de la mateixa pàgina. A tota aquesta guia, on posa `python`
  escriu `python3`.
- **Linux:** normalment ja el tens. Si no, `sudo apt install python3 python3-venv`.

Obre un terminal nou (a Windows, *PowerShell* o *Símbol del sistema*) i comprova-ho:

```bash
python --version
```

Ha de dir `Python 3.12.x` o superior. Si diu que no troba `python`, a Windows prova `py --version`
i, a partir d'aquí, escriu `py` on posa `python`.

## 2. Descarrega el material del curs

Dues maneres, tria'n una:

- **Sense git:** ves a [github.com/ZenidX/Machine-Learning](https://github.com/ZenidX/Machine-Learning),
  botó verd **Code → Download ZIP**, i descomprimeix-lo a una carpeta teva, per exemple
  `Documents\ML`.
- **Amb git:** `git clone https://github.com/ZenidX/Machine-Learning.git`

A partir d'ara, «la carpeta del curs» és la que conté el fitxer `requirements.txt`.

## 3. Crea l'entorn i instal·la les llibreries

Al terminal, entra a la carpeta del curs (`cd` i la ruta) i executa, d'una en una:

**Windows**

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

**macOS i Linux**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

La segona ordre tarda uns minuts. L'entorn `.venv` és una còpia de Python només per a aquest curs:
el que hi instal·lis no toca res més de l'ordinador. No cal «activar-lo»: cridem directament el seu
Python.

## 4. Obre Jupyter

**Windows**

```bash
.venv\Scripts\python -m jupyter lab
```

**macOS i Linux**

```bash
.venv/bin/python -m jupyter lab
```

S'obrirà el navegador amb Jupyter. **No tanquis el terminal**: és el que fa funcionar Jupyter. Per
aturar-lo, `Ctrl+C` al terminal.

Cada dia que vulguis treballar, només cal repetir aquest pas 4 des de la carpeta del curs.

## 5. Comprova que tot funciona

Obre `Machine Learning/03_matematiques/MA_01_algebra_lineal.ipynb` i executa la primera cel·la. Si
no hi ha cap error, ja ho tens.

També pots crear un quadern nou i executar això:

```python
import numpy, pandas, matplotlib, sklearn
print(numpy.__version__, pandas.__version__, sklearn.__version__)
```

Si imprimeix tres números de versió, l'entorn està complet.

## Coses que convé saber

- **Els quaderns que modifiquis són teus.** Si tornes a descarregar el ZIP, sobreescriuràs els
  canvis. Desa la teva feina amb un altre nom o en una carpeta a part (per exemple `treball/`).
- **Si vas instal·lar l'entorn abans del 3 de novembre**, et falta `ipywidgets` (els controls lliscants dels quaderns): torna a executar l'ordre del pas 3 amb `-r requirements.txt` després de descarregar el material nou.
- **Material nou:** amb git, `git pull`; sense git, torna a descarregar el ZIP en una carpeta nova.
- **Les dades** es carreguen des de GitHub, així que cal connexió a internet, però no cal Google.
- **VS Code:** si ja el fas servir, instal·la l'extensió *Jupyter*, obre la carpeta del curs i, en
  obrir un quadern, tria el nucli `.venv` (a dalt a la dreta). Les ordres dels passos 1 a 3 són les
  mateixes.
- **Lliuraments:** el fitxer `.ipynb` que lliures al Moodle és el mateix, el facis a Colab o en local.
