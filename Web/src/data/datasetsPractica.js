// Datasets per practicar el bloc 1 pel teu compte: cap no surt als reptes, als exemples ni al catàleg.
// Tots es carreguen a Colab amb una sola línia, sense claus ni comptes. Verificats el 21-oct-2026.
//
// Camps:
//   id          identificador curt (ancora de la pàgina)
//   nom         nom del dataset
//   origen      qui el publica
//   font        URL de la pàgina de la font
//   llicencia   llicència de reutilització
//   mida        files × columnes, tal com surt amb df.shape el dia de la verificació
//   carrega     la línia de pd.read_csv
//   context     de què va, en dues frases
//   columnes    les columnes que fan servir les preguntes: [nom, què és]
//   preguntes   el que s'ha de respondre

const TT = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/";

export const datasetsPractica = [
  {
    id: "aigua",
    nom: "Preu de l'aigua per municipi",
    origen: "Agència Catalana de l'Aigua · Dades Obertes de la Generalitat",
    font: "https://analisi.transparenciacatalunya.cat/d/6st4-ptsi",
    llicencia: "Llicència oberta d'ús d'informació – Catalunya",
    mida: "8.524 × 12",
    carrega: 'df = pd.read_csv("https://analisi.transparenciacatalunya.cat/resource/6st4-ptsi.csv?$limit=20000")',
    context:
      "El preu del metre cúbic d'aigua de cada municipi de Catalunya, any per any des del 2017, partit en el que cobra qui subministra, el cànon de l'ACA i el clavegueram.",
    columnes: [
      ["any", "any de la tarifa"],
      ["municipi, comarca", "on"],
      ["subministrament, canon_aigua, clavegueram", "les tres parts del preu, en €/m³"],
      ["preu_aigua", "el preu total, en €/m³"],
      ["gestio_subministrament", "Directa (l'ajuntament), Indirecta (una empresa) o No presta"],
      ["tarifes_socials", "si el municipi té tarifa social"],
    ],
    preguntes: [
      "Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?",
      "Quina comarca té el preu mitjà de l'aigua més alt l'any més recent? I el més baix?",
      "Compara el preu mitjà segons el tipus de gestió del subministrament.",
      "Fes un gràfic de l'evolució del preu mitjà per any.",
      "Amb NumPy, calcula la distància euclidiana entre les tres parts del preu de dos municipis que triïs.",
    ],
  },
  {
    id: "matriculacions",
    nom: "Matriculacions de vehicles electrificats i híbrids",
    origen: "Institut Català d'Energia · Dades Obertes de la Generalitat",
    font: "https://analisi.transparenciacatalunya.cat/d/eds6-562k",
    llicencia: "Llicència oberta d'ús d'informació – Catalunya",
    mida: "338.568 × 15",
    carrega: 'df = pd.read_csv("https://analisi.transparenciacatalunya.cat/resource/eds6-562k.csv?$limit=500000", low_memory=False)',
    context:
      "Els vehicles elèctrics i híbrids matriculats cada mes a Catalunya des del 2017, per municipi, tipus de vehicle i tecnologia. Les dades són vives: cada mes hi ha més files.",
    columnes: [
      ["any, mes", "quan es va matricular"],
      ["comarca, municipi", "on"],
      ["tipus_vehicle, descripci", "turisme, moto, furgoneta..."],
      ["tecnologia", "elèctric, endollable, híbrid lleuger..."],
      ["marca, model", "el vehicle"],
      ["uts", "unitats: quants vehicles representa la fila"],
    ],
    preguntes: [
      "Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?",
      "Quants vehicles es van matricular cada any? I de cada tecnologia?",
      "Quines són les cinc comarques i les cinc marques amb més matriculacions?",
      "Fes un gràfic de les matriculacions per mes al llarg dels anys.",
      "Amb NumPy, construeix el vector de matriculacions per mes de dos anys i calcula la norma de la seva diferència.",
    ],
  },
  {
    id: "netflix",
    nom: "El catàleg de Netflix",
    origen: "TidyTuesday 2021-04-20 (dades de Kaggle)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2021/2021-04-20",
    llicencia: "CC0 el repositori; ús educatiu de les dades",
    mida: "7.787 × 12",
    carrega: `df = pd.read_csv("${TT}2021/2021-04-20/netflix_titles.csv")`,
    context:
      "Les pel·lícules i sèries que hi havia a Netflix el 2021, amb país, any d'estrena, data en què es van afegir, classificació per edats i durada.",
    columnes: [
      ["type", "Movie o TV Show"],
      ["country", "país o països de producció"],
      ["release_year", "any d'estrena"],
      ["date_added", "quan es va afegir a Netflix"],
      ["rating", "classificació per edats"],
      ["duration", "durada: minuts o temporades"],
    ],
    preguntes: [
      "Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?",
      "Quantes pel·lícules i quantes sèries hi ha?",
      "Quins països tenen més títols? Quina és la classificació per edats més freqüent?",
      "Fes un gràfic dels títols afegits a Netflix per any.",
      "Calcula la durada mitjana de les pel·lícules per classificació per edats.",
    ],
  },
  {
    id: "xocolata",
    nom: "Valoracions de xocolata",
    origen: "TidyTuesday 2022-01-18 (Flavors of Cacao)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2022/2022-01-18",
    llicencia: "CC0 el repositori; ús educatiu de les dades",
    mida: "2.530 × 10",
    carrega: `df = pd.read_csv("${TT}2022/2022-01-18/chocolate.csv")`,
    context:
      "Més de 2.500 rajoles de xocolata negra valorades per un expert de l'1 al 4, amb el fabricant, l'origen del cacau i el percentatge de cacau.",
    columnes: [
      ["company_manufacturer, company_location", "qui la fa i on"],
      ["country_of_bean_origin", "d'on ve el cacau"],
      ["review_date", "any de la valoració"],
      ["cocoa_percent", "percentatge de cacau"],
      ["ingredients", "nombre i llista d'ingredients, en codi"],
      ["rating", "nota, de 1 a 4"],
    ],
    preguntes: [
      "Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?",
      "Quins països d'origen del cacau tenen la nota mitjana més alta? Quantes rajoles té cadascun?",
      "Hi ha relació entre el percentatge de cacau i la nota?",
      "Fes un histograma de les notes.",
      "Amb NumPy, calcula la mitjana i la desviació estàndard de la nota i compara-les amb les de Pandas.",
    ],
  },
  {
    id: "jocs-taula",
    nom: "Jocs de taula de BoardGameGeek",
    origen: "TidyTuesday 2022-01-25 (BoardGameGeek)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2022/2022-01-25",
    llicencia: "CC0 el repositori; ús educatiu de les dades",
    mida: "21.831 × 10",
    carrega: `df = pd.read_csv("${TT}2022/2022-01-25/ratings.csv")`,
    context:
      "Més de 21.000 jocs de taula amb la nota mitjana dels usuaris de BoardGameGeek, quanta gent els ha valorat i la posició al rànquing.",
    columnes: [
      ["name, year", "el joc i l'any de publicació"],
      ["average", "nota mitjana dels usuaris"],
      ["bayes_average", "nota corregida pel nombre de vots (la que fa servir el rànquing)"],
      ["users_rated", "quanta gent l'ha valorat"],
      ["rank", "posició al rànquing"],
    ],
    preguntes: [
      "Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?",
      "Quin rang d'anys de publicació cobreix?",
      "Calcula la nota mitjana i el nombre de jocs per dècada de publicació.",
      "Fes un gràfic de dispersió entre el nombre de valoracions i la nota mitjana.",
      "Compara els deu primers jocs ordenats per average i per bayes_average.",
    ],
  },
  {
    id: "big-mac",
    nom: "L'índex Big Mac",
    origen: "TidyTuesday 2020-12-22 (The Economist)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-12-22",
    llicencia: "CC0 el repositori; dades de The Economist",
    mida: "1.386 × 19",
    carrega: `df = pd.read_csv("${TT}2020/2020-12-22/big-mac.csv")`,
    context:
      "El preu d'un Big Mac a 57 països del 2000 al 2020, en moneda local i en dòlars. The Economist el fa servir per veure si una moneda està sobrevalorada o infravalorada.",
    columnes: [
      ["date", "data de la mesura"],
      ["name, iso_a3, currency_code", "país i moneda"],
      ["local_price", "preu en moneda local"],
      ["dollar_ex", "canvi: unitats de moneda local per dòlar"],
      ["dollar_price", "preu en dòlars"],
      ["usd_raw", "quant està sobrevalorada (+) o infravalorada (−) la moneda contra el dòlar"],
    ],
    preguntes: [
      "Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?",
      "Quantes mesures hi ha per país?",
      "On era més car i on era més barat el Big Mac en dòlars a la data més recent?",
      "Fes un gràfic de l'evolució del preu en dòlars de quatre països que triïs.",
      "Amb NumPy, comprova si dollar_price és igual a local_price / dollar_ex i dona la diferència màxima.",
    ],
  },
  {
    id: "himalaia",
    nom: "Expedicions a l'Himàlaia",
    origen: "TidyTuesday 2020-09-22 (The Himalayan Database)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-09-22",
    llicencia: "CC0 el repositori; dades de The Himalayan Database",
    mida: "10.364 × 16",
    carrega: `df = pd.read_csv("${TT}2020/2020-09-22/expeditions.csv")`,
    context:
      "Més de 10.000 expedicions als cims de l'Himàlaia del Nepal entre el 1905 i el 2019: quin cim, quina temporada, quanta gent hi anava, quina alçada van assolir i per què es van acabar.",
    columnes: [
      ["peak_name, year, season", "cim, any i temporada"],
      ["termination_reason", "com va acabar: èxit, mal temps, accident..."],
      ["highpoint_metres", "alçada màxima assolida"],
      ["members, hired_staff", "membres de l'expedició i personal contractat (xerpes)"],
      ["member_deaths, hired_staff_deaths", "morts"],
      ["oxygen_used", "si van fer servir oxigen"],
    ],
    preguntes: [
      "Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?",
      "Quins cims tenen més expedicions? Quina és la temporada més habitual?",
      "Calcula la proporció d'expedicions que arriben al cim, per temporada.",
      "Fes un gràfic del nombre d'expedicions per any.",
      "Compara l'alçada màxima assolida per les expedicions amb oxigen i sense.",
    ],
  },
  {
    id: "pinguins",
    nom: "Pingüins de l'Antàrtida",
    origen: "TidyTuesday 2020-07-28 (Palmer Station LTER)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-07-28",
    llicencia: "CC0",
    mida: "344 × 8",
    carrega: `df = pd.read_csv("${TT}2020/2020-07-28/penguins.csv")`,
    context:
      "344 pingüins de tres espècies de tres illes de l'arxipèlag Palmer, amb les mesures del bec, l'aleta i el pes.",
    columnes: [
      ["species, island, sex", "espècie, illa i sexe"],
      ["bill_length_mm, bill_depth_mm", "llargada i gruix del bec"],
      ["flipper_length_mm", "llargada de l'aleta"],
      ["body_mass_g", "pes"],
      ["year", "any de la mesura"],
    ],
    preguntes: [
      "Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?",
      "Quants pingüins hi ha de cada espècie a cada illa?",
      "Calcula la mitjana de cada mesura per espècie.",
      "Fes un gràfic de dispersió de la llargada contra el gruix del bec, amb un color per espècie.",
      "Amb NumPy, calcula la distància entre els pingüins mitjans de cada parell d'espècies. Quines dues són les més properes?",
    ],
  },
  {
    id: "ramen",
    nom: "Valoracions de ramen instantani",
    origen: "TidyTuesday 2019-06-04 (The Ramen Rater)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-06-04",
    llicencia: "CC0 el repositori; ús educatiu de les dades",
    mida: "3.180 × 6",
    carrega: `df = pd.read_csv("${TT}2019/2019-06-04/ramen_ratings.csv")`,
    context:
      "Més de 3.000 ramen instantanis valorats amb estrelles de 0 a 5, amb la marca, el país i el format (got, paquet, safata...).",
    columnes: [
      ["brand, variety", "marca i producte"],
      ["style", "format: Pack, Cup, Bowl, Tray..."],
      ["country", "país"],
      ["stars", "valoració, de 0 a 5"],
    ],
    preguntes: [
      "Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?",
      "Quins països i quines marques tenen més productes valorats?",
      "Quin format i quin país tenen la valoració mitjana més alta?",
      "Fes un histograma de les estrelles.",
      "Amb NumPy, compta quants productes tenen una nota a més de dues desviacions estàndard de la mitjana.",
    ],
  },
  {
    id: "nobel",
    nom: "Premis Nobel, 1901-2016",
    origen: "TidyTuesday 2019-05-14 (Fundació Nobel)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-05-14",
    llicencia: "CC0 el repositori; dades de la Fundació Nobel",
    mida: "969 × 18",
    carrega: `df = pd.read_csv("${TT}2019/2019-05-14/nobel_winners.csv")`,
    context:
      "Tots els premis Nobel fins al 2016: categoria, any, quina part del premi es van endur, i on i quan va néixer cada guardonat.",
    columnes: [
      ["prize_year, category", "any i categoria"],
      ["laureate_type", "Individual o Organization"],
      ["prize_share", "part del premi: 1/1, 1/2, 1/3, 1/4"],
      ["full_name, gender", "guardonat i gènere"],
      ["birth_date, birth_country", "naixement"],
      ["organization_name", "universitat o institució on treballava"],
    ],
    preguntes: [
      "Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?",
      "Quants premis hi ha per categoria? Quants guardonats són organitzacions?",
      "Calcula la proporció de dones per categoria i per dècada.",
      "Calcula l'edat de cada guardonat l'any del premi i fes-ne un histograma per categoria.",
      "Quines organitzacions acumulen més guardonats?",
    ],
  },
  {
    id: "olimpics",
    nom: "120 anys de Jocs Olímpics",
    origen: "TidyTuesday 2021-07-27 (Sports Reference)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2021/2021-07-27",
    llicencia: "CC0 el repositori; ús educatiu de les dades",
    mida: "271.116 × 15",
    carrega: `df = pd.read_csv("${TT}2021/2021-07-27/olympics.csv")`,
    context:
      "Els esportistes que han participat als Jocs Olímpics, d'Atenes 1896 a Rio 2016, amb l'edat, l'alçada, el pes, l'equip, l'esport, la prova i la medalla.",
    columnes: [
      ["id, name, sex, age, height, weight", "l'esportista"],
      ["team, noc", "equip i codi del comitè olímpic"],
      ["year, season, city", "els Jocs"],
      ["sport, event", "esport i prova"],
      ["medal", "Gold, Silver, Bronze o res"],
    ],
    preguntes: [
      "Quantes files i columnes té el conjunt? Quines columnes tenen valors que falten?",
      "Quants esportistes diferents hi ha?",
      "Quins països tenen més medalles d'or?",
      "Fes un gràfic de la proporció de dones participants per any, separant Jocs d'estiu i d'hivern.",
      "Calcula l'alçada i el pes mitjans per esport. En quins esports són més alts els esportistes?",
    ],
  },
];
