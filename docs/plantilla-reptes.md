# Plantilla dels reptes

Els reptes són el format central de pràctica del curs a partir del 14-oct-2026. L'alumnat els fa
**sol**, sense que el professor porti la classe. En Xavi hi és com a expert, quan cal el seu
criteri.

**Per què.** Els quaderns de teoria (FO_xx, ML_xx) eren «executar el que ja hi ha escrit i
avançar». Ara s'aprèn enfrontant-se a **dades reals que no s'han vist mai**. Que alguna cosa surti
malament forma part de l'aprenentatge.

**Format (decisió del 14-oct-2026).** El repte de l'alumne és **només les dades i un enunciat que
les explica**. Sense bastida: ni caixa d'eines, ni nivells, ni cel·les per tasca, ni pistes
plegades, ni comprovacions. Decidir els passos és part del repte. La versió resolta és **pública**.

Els datasets surten de [`cataleg-datasets-reptes.md`](cataleg-datasets-reptes.md).

## On van

- L'enunciat, a `Machine Learning/04_reptes/RE_<bloc><nn>_<nom>.ipynb`. Per exemple,
  `RE_101_accidents_bcn.ipynb` és el bloc 1, repte 01.
- La versió resolta, **pública**, a `Machine Learning/04_reptes/resolts/RE_<...>_resolt.ipynb`. S'enllaça
  des de la pàgina de Recursos.
- El solucionari de treball, a `Machine Learning/04_reptes/solucions/RE_<...>_solucions.ipynb`, amb els
  seus generadors. Aquesta carpeta és al `.gitignore`: hi pot haver notes per al professor.
- Els generadors: `_eines/gen_reptes_enunciat.py` (enunciats; les cel·les de càrrega a
  `_eines/reptes_carrega.py`) i `_eines/gen_reptes_resolts.py` (resolts, a partir de `solucions/`).

## Estructura de l'enunciat (en català)

1. **Títol i encàrrec.** Un cas creïble amb un rol: «Ets analista de...». Una pregunta principal
   amb sentit, en dues o tres frases. Res de teoria.
2. **Les dades.**
   - La font, la llicència, si és una còpia congelada, i què és cada fila (i quantes n'hi ha).
   - El **diccionari de columnes**: una taula amb les columnes que importen, què volen dir, en quines
     unitats i quins codis tenen. Si són moltes, agrupades per prefix.
   - **Com s'han recollit**, i què cal tenir present de la font (qui omple les dades, què no hi és,
     què pot canviar d'un any a l'altre).
   - Regla: el diccionari explica **el que diu la font**. Mai **el que s'hi troba** (un error, una
     columna intercanviada, un nul disfressat): això és la troballa.
3. **Què has d'investigar.** La pregunta de l'encàrrec, desplegada en prosa: què s'ha de respondre,
   amb quins números o gràfics, i la part on **la teoria aterra al codi** (calcular una cosa a mà i
   comprovar-la contra la llibreria). Després, dues o tres **preguntes obertes**.
4. **Pistes per pensar** (opcionals). Pistes que orienten el raonament sense donar el resultat. Per
   exemple: «hi ha una columna que fa que el model sembli perfecte: si et passa, pregunta't per què»,
   o «un buit pot voler dir zero o no se sap». **Mai** un número que sigui la troballa, ni el nom de
   la columna culpable, ni els passos.
5. **Exemples per inspirar-te.** Els quaderns resolts del curs (EX_01-EX_06) i de teoria (FO, ML, MA)
   on es fan servir les eines que caldran, amb la secció. Només l'enllaç: no se'n repeteix el
   contingut.
6. **Lliurament.** El quadern executat, sense errors, amb l'anàlisi (codi i text que justifica cada
   decisió) i una **conclusió** de tres a cinc frases, escrita per ells, que respongui l'encàrrec amb
   números. I, en dues o tres línies, **quan cridar en Xavi**: dubtes de **criteri**, no de sintaxi
   («esborro o imputo?», «aquest resultat té sentit?», «les dades m'estan enganyant?»).
7. **La cel·la de càrrega**, que ha d'anar a la primera, i **una cel·la de codi buida**. La resta del
   quadern és seu.

## Estructura del resolt

Es genera a partir del solucionari amb `gen_reptes_resolts.py`, que:

- posa el títol, un bàner de «repte resolt» i l'enllaç a l'enunciat;
- deixa cada tasca amb el seu enunciat, el codi executat i el comentari del resultat;
- treu les pistes, les comprovacions, la caixa d'eines, el lliurament i les tasques «la teva pregunta»;
- canvia la veu de professor per la d'un quadern resolt, i afegeix una **conclusió** si no n'hi havia;
- s'atura si hi troba qualsevol rastre privat (proves, notes privades, datasets reservats).

Tot el que és només per al professor (com puntuar, què reservar per a una prova) va a
`solucions/` o a `cataleg-datasets-notes-privades.md`, mai al resolt.

## Criteris de qualitat

- Ha de funcionar a Colab sense instal·lar res, i la cel·la de càrrega ha d'anar a la primera.
- Si el dataset és viu (Socrata, XEMA, embassaments...), es **congela una còpia** a
  `Machine Learning/04_reptes/dades/`, si la llicència ho permet, i es carrega des del raw de GitHub
  (`https://raw.githubusercontent.com/ZenidX/Machine-Learning/main/Machine%20Learning/04_reptes/dades/<fitxer>`).
  Ha de pesar menys de 10 MB; si cal, se'n fa una mostra.
- Durada: entre una i dues sessions de 2 h per repte.
- L'enunciat i el resolt s'executen sencers amb `_eines/executa_nb.py`, amb el Python de
  `../CEIABD-IA/.venv/Scripts/python.exe`, des de `Machine Learning/04_reptes/`.
- Cada número del resolt surt d'una execució real.
- Sense dades personals: es treuen les columnes que identifiquin persones o adreces exactes.
- Els datasets reservats per a les proves no surten ni als reptes, ni al catàleg públic, ni als
  resolts.
