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
//   repte       on és la feina d'aquest dataset, dit en paraules
//   carrega     la línia de pd.read_csv
//   context     de què va, en dues frases
//   columnes    les columnes que fan servir les preguntes: [nom, què és]
//   preguntes   per començar; el resultat el trobes tu
//   paranys     coses tècniques que et faran perdre temps si no les saps

const TT = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/";

export const datasetsPractica = [
  {
    id: "aigua",
    nom: "Preu de l'aigua per municipi",
    origen: "Agència Catalana de l'Aigua · Dades Obertes de la Generalitat",
    font: "https://analisi.transparenciacatalunya.cat/d/6st4-ptsi",
    llicencia: "Llicència oberta d'ús d'informació – Catalunya",
    mida: "8.524 × 12",
    repte:
      "No hi ha res a netejar: el difícil és fer bones preguntes. Què vol dir comparar comarques que tenen un nombre molt diferent de municipis?",
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
      "Quantes files té cada any? Quadra amb el nombre de municipis de Catalunya?",
      "Quina comarca té l'aigua més cara de mitjana l'últim any? I la més barata?",
      "La gestió directa surt més barata o més cara que la indirecta?",
      "Fes un gràfic de l'evolució del preu mitjà per any.",
      "NumPy: posa les tres parts del preu de dos municipis en dos vectors i calcula'n la distància. Quina part pesa més?",
    ],
    paranys: [
      "Sense el $limit de la URL només en baixes 1.000 files.",
      "codi_municipi perd el zero de l'esquerra: 08001 es llegeix com 8001.",
    ],
  },
  {
    id: "matriculacions",
    nom: "Matriculacions de vehicles electrificats i híbrids",
    origen: "Institut Català d'Energia · Dades Obertes de la Generalitat",
    font: "https://analisi.transparenciacatalunya.cat/d/eds6-562k",
    llicencia: "Llicència oberta d'ús d'informació – Catalunya",
    mida: "338.568 × 15",
    repte:
      "Abans de comptar res has de saber què representa una fila, perquè no sempre és un vehicle. I els buits no sempre es diuen NaN.",
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
      "Quantes matriculacions hi ha cada any? I quantes de cada tecnologia?",
      "Quines cinc comarques en matriculen més? I quines marques?",
      "Fes un gràfic de les matriculacions per mes al llarg dels anys. Es veu cap estacionalitat?",
      "NumPy: fes el vector de matriculacions per mes (12 valors) de dos anys i calcula'n la norma de la diferència.",
    ],
    paranys: [
      "Hi ha una columna que es diu any, i df.any és un mètode de Pandas. Fes servir df[\"any\"].",
      "Mira quins valors fan servir per dir «no ho sabem». No tots els buits són NaN.",
      "Sense el $limit de la URL només en baixes 1.000 files.",
    ],
  },
  {
    id: "netflix",
    nom: "El catàleg de Netflix",
    origen: "TidyTuesday 2021-04-20 (dades de Kaggle)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2021/2021-04-20",
    llicencia: "CC0 el repositori; ús educatiu de les dades",
    mida: "7.787 × 12",
    repte:
      "Columnes que barregen coses diferents: una durada que de vegades són minuts i de vegades temporades, i països en plural dins d'una sola cel·la.",
    carrega: `df = pd.read_csv("${TT}2021/2021-04-20/netflix_titles.csv")`,
    context:
      "Les pel·lícules i sèries que hi havia a Netflix el 2021, amb país, any d'estrena, data en què es van afegir, classificació per edats i durada.",
    columnes: [
      ["type", "Movie o TV Show"],
      ["country", "país o països de producció"],
      ["release_year", "any d'estrena"],
      ["date_added", "quan es va afegir a Netflix (text)"],
      ["rating", "classificació per edats"],
      ["duration", "durada: minuts o temporades"],
    ],
    preguntes: [
      "Quina proporció són pel·lícules i quina sèries? Quines columnes tenen més buits?",
      "Quins països tenen més títols? I de quina classificació per edats n'hi ha més?",
      "Fes un gràfic dels títols afegits per any. Quan va créixer més el catàleg?",
      "Converteix la durada de les pel·lícules en un número i compara la mitjana per classificació.",
    ],
    paranys: [
      "duration barreja «93 min» i «4 Seasons» a la mateixa columna.",
      "Alguns valors de date_added comencen amb un espai.",
      "country pot portar diversos països separats per comes.",
    ],
  },
  {
    id: "xocolata",
    nom: "Valoracions de xocolata",
    origen: "TidyTuesday 2022-01-18 (Flavors of Cacao)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2022/2022-01-18",
    llicencia: "CC0 el repositori; ús educatiu de les dades",
    mida: "2.530 × 10",
    repte:
      "Un número disfressat de text, i mitjanes fetes amb grups de mides molt diferents.",
    carrega: `df = pd.read_csv("${TT}2022/2022-01-18/chocolate.csv")`,
    context:
      "Més de 2.500 rajoles de xocolata negra valorades per un expert de l'1 al 4, amb el fabricant, l'origen del cacau i el percentatge de cacau.",
    columnes: [
      ["company_manufacturer, company_location", "qui la fa i on"],
      ["country_of_bean_origin", "d'on ve el cacau"],
      ["review_date", "any de la valoració"],
      ["cocoa_percent", "percentatge de cacau (text)"],
      ["ingredients", "nombre i llista d'ingredients, en codi"],
      ["rating", "nota, de 1 a 4"],
    ],
    preguntes: [
      "Quins països d'origen del cacau tenen millor nota mitjana? Compta també quantes rajoles té cadascun.",
      "Les rajoles amb més cacau tenen millor nota?",
      "Fes un histograma de les notes.",
      "NumPy: calcula a mà la mitjana i la desviació de rating i compara-les amb .mean() i .std().",
    ],
    paranys: [
      "cocoa_percent és text amb el signe %: primer s'ha de convertir en número.",
      "Una mitjana feta amb tres rajoles no val el mateix que una feta amb tres-centes.",
    ],
  },
  {
    id: "jocs-taula",
    nom: "Jocs de taula de BoardGameGeek",
    origen: "TidyTuesday 2022-01-25 (BoardGameGeek)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2022/2022-01-25",
    llicencia: "CC0 el repositori; ús educatiu de les dades",
    mida: "21.831 × 10",
    repte:
      "Dues notes que semblen la mateixa i no ho són, i anys que no poden ser.",
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
      "Quin rang d'anys cobreix? Té sentit tot el que hi surt?",
      "Nota mitjana i nombre de jocs per dècada de publicació.",
      "Fes un gràfic de dispersió entre users_rated i average.",
      "Per què average i bayes_average no ordenen igual els jocs? Busca'n un exemple.",
    ],
    paranys: [
      "Mira els valors mínim i màxim de year abans de fer cap grup per dècades.",
      "users_rated està molt concentrat en pocs jocs: prova l'escala logarítmica al gràfic.",
    ],
  },
  {
    id: "big-mac",
    nom: "L'índex Big Mac",
    origen: "TidyTuesday 2020-12-22 (The Economist)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-12-22",
    llicencia: "CC0 el repositori; dades de The Economist",
    mida: "1.386 × 19",
    repte:
      "Cada país paga en la seva moneda: comparar sense convertir no té sentit. I hi ha columnes que només existeixen a partir d'una data.",
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
      "Quantes mesures hi ha per país? Tots els països hi són tots els anys?",
      "On és més car i on és més barat en dòlars la data més recent?",
      "Fes un gràfic de l'evolució de dollar_price per a quatre països que triïs.",
      "NumPy: comprova que dollar_price és local_price / dollar_ex. Diferència màxima?",
    ],
    paranys: [
      "No compareu local_price entre països: cada un està en la seva moneda.",
      "Les columnes *_adjusted només tenen valor a partir d'una data.",
    ],
  },
  {
    id: "himalaia",
    nom: "Expedicions a l'Himàlaia",
    origen: "TidyTuesday 2020-09-22 (The Himalayan Database)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-09-22",
    llicencia: "CC0 el repositori; dades de The Himalayan Database",
    mida: "10.364 × 16",
    repte:
      "Has de decidir tu què és un èxit: la columna que ho explica no respon amb un sí o un no.",
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
      "Quins cims tenen més expedicions? Quina temporada és la més habitual?",
      "Quina proporció d'expedicions arriba al cim, per temporada? Fes-la amb termination_reason.",
      "Fes un gràfic de les expedicions per any.",
      "Les expedicions amb oxigen arriben més amunt? Compara highpoint_metres en els dos grups.",
    ],
    paranys: [
      "Les dates (basecamp_date...) arriben com a text: converteix-les amb pd.to_datetime si les vols fer servir.",
      "termination_reason té més de dos valors: decideix tu quins compten com a èxit.",
    ],
  },
  {
    id: "pinguins",
    nom: "Pingüins de l'Antàrtida",
    origen: "TidyTuesday 2020-07-28 (Palmer Station LTER)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-07-28",
    llicencia: "CC0",
    mida: "344 × 8",
    repte:
      "Dades petites i netes: la feina és interpretar. Quina mesura distingeix les espècies, i per què la distància depèn de les unitats?",
    carrega: `df = pd.read_csv("${TT}2020/2020-07-28/penguins.csv")`,
    context:
      "344 pingüins de tres espècies de tres illes de l'arxipèlag Palmer, amb les mesures del bec, l'aleta i el pes. És petit i net: bo per començar.",
    columnes: [
      ["species, island, sex", "espècie, illa i sexe"],
      ["bill_length_mm, bill_depth_mm", "llargada i gruix del bec"],
      ["flipper_length_mm", "llargada de l'aleta"],
      ["body_mass_g", "pes"],
      ["year", "any de la mesura"],
    ],
    preguntes: [
      "Quants n'hi ha de cada espècie a cada illa?",
      "Mitjana de cada mesura per espècie. Quina mesura separa millor les espècies?",
      "Fes un gràfic de dispersió del bec (llargada contra gruix), un color per espècie.",
      "NumPy: el pingüí mitjà de cada espècie és un vector de 4 mesures. Quines dues espècies estan més a prop?",
    ],
    paranys: [
      "Hi ha uns quants nuls: decideix què en fas abans de calcular les mitjanes.",
      "Les mesures estan en unitats diferents (mm i g), i això afecta la distància.",
    ],
  },
  {
    id: "ramen",
    nom: "Valoracions de ramen instantani",
    origen: "TidyTuesday 2019-06-04 (The Ramen Rater)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-06-04",
    llicencia: "CC0 el repositori; ús educatiu de les dades",
    mida: "3.180 × 6",
    repte:
      "Grups minúsculs que encapçalen rànquings: quan et pots creure una mitjana?",
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
      "Quins països i quines marques tenen més productes valorats?",
      "Quin format té millor valoració mitjana? I quin país, comptant només els que tenen prou productes?",
      "Fes un histograma de les estrelles.",
      "NumPy: quants ramen tenen una nota a més de dues desviacions de la mitjana? Fes-ho amb una màscara.",
    ],
    paranys: [
      "Alguns formats tenen molt pocs productes: compta abans de comparar mitjanes.",
    ],
  },
  {
    id: "nobel",
    nom: "Premis Nobel, 1901-2016",
    origen: "TidyTuesday 2019-05-14 (Fundació Nobel)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-05-14",
    llicencia: "CC0 el repositori; dades de la Fundació Nobel",
    mida: "969 × 18",
    repte:
      "Persones i organitzacions barrejades, gent que surt més d'un cop i dates en text: calcular una edat té feina.",
    carrega: `df = pd.read_csv("${TT}2019/2019-05-14/nobel_winners.csv")`,
    context:
      "Tots els premis Nobel fins al 2016: categoria, any, quina part del premi es van endur, i on i quan va néixer cada guardonat.",
    columnes: [
      ["prize_year, category", "any i categoria"],
      ["laureate_type", "Individual o Organization"],
      ["prize_share", "part del premi: 1/1, 1/2, 1/3, 1/4 (text)"],
      ["full_name, gender", "guardonat i gènere"],
      ["birth_date, birth_country", "naixement"],
      ["organization_name", "universitat o institució on treballava"],
    ],
    preguntes: [
      "Quants premis hi ha per categoria? I quants guardonats són organitzacions?",
      "Proporció de dones per categoria i per dècada.",
      "Calcula l'edat de cada guardonat l'any del premi i fes-ne un histograma per categoria.",
      "Quines organitzacions acumulen més guardonats?",
    ],
    paranys: [
      "Abans de comptar persones, mira si n'hi ha de repetides.",
      "birth_date és text: converteix-la amb pd.to_datetime abans de calcular edats.",
    ],
  },
  {
    id: "olimpics",
    nom: "120 anys de Jocs Olímpics",
    origen: "TidyTuesday 2021-07-27 (Sports Reference)",
    font: "https://github.com/rfordatascience/tidytuesday/tree/master/data/2021/2021-07-27",
    llicencia: "CC0 el repositori; ús educatiu de les dades",
    mida: "271.116 × 15",
    repte:
      "Entendre què és una fila: és una participació en una prova, no un esportista ni una medalla. Si t'equivoques aquí, tot el que ve després surt malament.",
    carrega: `df = pd.read_csv("${TT}2021/2021-07-27/olympics.csv")`,
    context:
      "Cada participació d'un esportista en una prova olímpica, d'Atenes 1896 a Rio 2016, amb l'edat, l'alçada, el pes, l'equip i la medalla si en va guanyar.",
    columnes: [
      ["id, name, sex, age, height, weight", "l'esportista"],
      ["team, noc", "equip i codi del comitè olímpic"],
      ["year, season, city", "els Jocs"],
      ["sport, event", "esport i prova"],
      ["medal", "Gold, Silver, Bronze o res"],
    ],
    preguntes: [
      "Què és exactament una fila? Quants esportistes diferents hi ha?",
      "Quins països tenen més medalles d'or? Pensa bé què compta com una medalla.",
      "Fes un gràfic de la proporció de dones participants per any, separant estiu i hivern.",
      "Alçada i pes mitjans per esport: en quins esports els esportistes són més alts?",
    ],
    paranys: [
      "Un NaN a medal no és un valor que falta: vol dir que no va guanyar medalla.",
      "Ocupa uns 170 MB a memòria: a Colab va bé, en un ordinador justet pot anar lent.",
    ],
  },
];
