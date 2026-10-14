// Els reptes: quaderns amb dades reals que no s'han vist mai, per fer sols.
// Viuen a "Machine Learning/04_reptes/<fitxer>" i la web en construeix l'enllaç de Colab.
//
// Camps:
//   codi       "RE_101"
//   bloc       pàgina de la web on surt: 1 Dades · 2 Supervisat ·
//              3 Dades brutes i no supervisat · 4 Xarxes i RL
//              (al catàleg de datasets, els RE_3xx i els RE_4xx van tots dos al bloc 3 de la web)
//   titol      el títol del repte
//   enunciat   dues o tres frases que expliquen el dataset i què s'hi ha de respondre
//   dataset    el nom del conjunt de dades
//   font       URL de la font original de les dades
//   llicencia  "CC BY 4.0", "Llicència oberta d'ús d'informació – Catalunya"...
//   dificultat 1, 2 o 3 (la mateixa escala que docs/cataleg-datasets-reptes.md)
//   fitxer     "RE_101_accidents_bcn.ipynb"
//   resolt     opcional: ruta del quadern resolt dins del repositori; si hi és, surt a Recursos
//              ("Machine Learning/04_reptes/resolts/RE_101_accidents_bcn_resolt.ipynb")
//
// Exemple:
//   {
//     codi: "RE_101",
//     bloc: 1,
//     titol: "On i quan hi ha accidents a Barcelona",
//     enunciat: "Els 7.536 accidents que va gestionar la Guàrdia Urbana el 2024, amb districte, hora i víctimes. Ets analista de mobilitat: on i quan cal actuar primer?",
//     dataset: "Accidents gestionats per la Guàrdia Urbana (2024)",
//     font: "https://opendata-ajuntament.barcelona.cat/data/ca/dataset/accidents-gu-bcn",
//     llicencia: "CC BY 4.0",
//     dificultat: 1,
//     fitxer: "RE_101_accidents_bcn.ipynb",
//     resolt: "Machine Learning/04_reptes/resolts/RE_101_accidents_bcn_resolt.ipynb",
//   },

export const reptes = [
  {
    "codi": "RE_101",
    "bloc": 1,
    "titol": "On i quan hi ha accidents a Barcelona",
    "enunciat": "En quins districtes, a quines hores i quins dies hi ha més accidents, i on fan més mal?",
    "dataset": "Accidents de la Guàrdia Urbana a Barcelona (2024)",
    "font": "https://opendata-ajuntament.barcelona.cat/data/ca/dataset/accidents-gu-bcn",
    "llicencia": "CC BY 4.0",
    "dificultat": 1,
    "fitxer": "RE_101_accidents_bcn.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_101_accidents_bcn_resolt.ipynb"
  },
  {
    "codi": "RE_102",
    "bloc": 1,
    "titol": "Quina música fa ballar",
    "enunciat": "Quin gènere fa més ballar i quin té més energia per entrenar? I, donada una cançó que t'agrada, quines cinc del catàleg s'hi assemblen més?",
    "dataset": "30.000 cançons de Spotify (TidyTuesday)",
    "font": "https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-01-21",
    "llicencia": "Dades de Spotify, ús educatiu",
    "dificultat": 1,
    "fitxer": "RE_102_spotify.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_102_spotify_resolt.ipynb"
  },
  {
    "codi": "RE_103",
    "bloc": 1,
    "titol": "Com de greu va ser la sequera",
    "enunciat": "Com de greu va ser la sequera comparada amb les anteriors, i com estan avui les reserves? A quin moment del passat s'assemblen més?",
    "dataset": "Aigua als embassaments de les conques internes (ACA)",
    "font": "https://analisi.transparenciacatalunya.cat/d/gn9e-3qhr",
    "llicencia": "Llicència oberta d'ús d'informació – Catalunya",
    "dificultat": 2,
    "fitxer": "RE_103_embassaments.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_103_embassaments_resolt.ipynb"
  },
  {
    "codi": "RE_104",
    "bloc": 1,
    "titol": "Quant costa llogar un pis",
    "enunciat": "Quant ha pujat el lloguer a Barcelona, Sant Cugat del Vallès i Terrassa en deu anys? On és més car llogar avui? I quants contractes se signen cada any?",
    "dataset": "Preu mitjà del lloguer per municipi",
    "font": "https://analisi.transparenciacatalunya.cat/d/qww9-bvhh",
    "llicencia": "Llicència oberta d'ús d'informació – Catalunya",
    "dificultat": 2,
    "fitxer": "RE_104_lloguer.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_104_lloguer_resolt.ipynb"
  },
  {
    "codi": "RE_105",
    "bloc": 1,
    "titol": "Els estius de Barcelona, cada cop més calorosos?",
    "enunciat": "Des del 2016, els estius a Barcelona són cada cop més calorosos? Quins han estat els dies més extrems, i quin any ha estat el més estrany?",
    "dataset": "Meteo diària de l'Observatori Fabra (XEMA)",
    "font": "https://analisi.transparenciacatalunya.cat/d/7bvh-jvq2",
    "llicencia": "Llicència oberta d'ús d'informació – Catalunya",
    "dificultat": 3,
    "fitxer": "RE_105_meteo_fabra.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_105_meteo_fabra_resolt.ipynb"
  },
  {
    "codi": "RE_106",
    "bloc": 1,
    "titol": "Quan i on es respira pitjor a Barcelona",
    "enunciat": "A quines hores i a quines estacions l'aire és pitjor? Els caps de setmana es respira millor? Quines estacions es comporten igual i quines no?",
    "dataset": "Qualitat de l'aire a Barcelona (2024, horària)",
    "font": "https://analisi.transparenciacatalunya.cat/d/tasf-thgu",
    "llicencia": "Llicència oberta d'ús d'informació – Catalunya",
    "dificultat": 3,
    "fitxer": "RE_106_aire_bcn.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_106_aire_bcn_resolt.ipynb"
  },
  {
    "codi": "RE_201",
    "bloc": 2,
    "titol": "Bolets: comestible o verinós?",
    "enunciat": "Es pot decidir amb un model? Amb quin, i com de gran ha de ser? Què ha après el model (ha de ser una cosa que una persona pugui seguir)? I què passa quan s'equivoca, si aquí no tots els errors costen el mateix?",
    "dataset": "Mushroom (UCI · OpenML 24)",
    "font": "https://www.openml.org/d/24",
    "llicencia": "CC BY 4.0",
    "dificultat": 1,
    "fitxer": "RE_201_bolets.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_201_bolets_resolt.ipynb"
  },
  {
    "codi": "RE_202",
    "bloc": 2,
    "titol": "Qui acabarà comprant?",
    "enunciat": "Amb una regressió logística, quines variables pesen a favor i en contra de la compra, quant, i com arriba el model a la probabilitat d'una sessió concreta?",
    "dataset": "Online Shoppers Purchasing Intention (OpenML 46947)",
    "font": "https://www.openml.org/d/46947",
    "llicencia": "CC BY 4.0",
    "dificultat": 2,
    "fitxer": "RE_202_compres_en_linia.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_202_compres_en_linia_resolt.ipynb"
  },
  {
    "codi": "RE_203",
    "bloc": 2,
    "titol": "A qui truquem?",
    "enunciat": "Un model pot triar a qui trucar millor que l'atzar? Amb quina mesura s'ha de jutjar, i on poses el llindar per decidir si truques o no?",
    "dataset": "Bank Marketing (OpenML 46910)",
    "font": "https://www.openml.org/d/46910",
    "llicencia": "CC BY 4.0",
    "dificultat": 3,
    "fitxer": "RE_203_campanya_banc.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_203_campanya_banc_resolt.ipynb"
  },
  {
    "codi": "RE_204",
    "bloc": 2,
    "titol": "Formigó: memoritzar no és aprendre",
    "enunciat": "Quin error real pots prometre al laboratori, i com saps que no t'estàs enganyant?",
    "dataset": "Concrete Compressive Strength (OpenML 44959)",
    "font": "https://www.openml.org/d/44959",
    "llicencia": "CC BY 4.0",
    "dificultat": 2,
    "fitxer": "RE_204_formigo.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_204_formigo_resolt.ipynb"
  },
  {
    "codi": "RE_205",
    "bloc": 2,
    "titol": "Quantes bicis caldran a les 8?",
    "enunciat": "Quin model preveu millor els lloguers per hora, i com l'has d'avaluar perquè l'error que prometis sigui el que hi haurà l'any que ve?",
    "dataset": "Bike Sharing (OpenML 42712)",
    "font": "https://www.openml.org/d/42712",
    "llicencia": "CC BY 4.0",
    "dificultat": 2,
    "fitxer": "RE_205_bicis.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_205_bicis_resolt.ipynb"
  },
  {
    "codi": "RE_206",
    "bloc": 2,
    "titol": "És just el model?",
    "enunciat": "El model encerta i s'equivoca igual per a dones i homes, i per als diferents grups? I si traiem sex i race de les dades, el problema desapareix?",
    "dataset": "Adult / Census Income (OpenML 1590)",
    "font": "https://www.openml.org/d/1590",
    "llicencia": "CC BY 4.0",
    "dificultat": 3,
    "fitxer": "RE_206_equitat_adult.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_206_equitat_adult_resolt.ipynb"
  },
  {
    "codi": "RE_301",
    "bloc": 3,
    "titol": "Quant val aquest cotxe?",
    "enunciat": "Amb quin error, en dòlars, es pot estimar el preu d'un cotxe a partir de la seva fitxa? I aquest número, és un número en què es pugui confiar?",
    "dataset": "Automobile / imports-85 (UCI)",
    "font": "https://archive.ics.uci.edu/dataset/10/automobile",
    "llicencia": "CC BY 4.0",
    "dificultat": 2,
    "fitxer": "RE_301_cotxes_preu.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_301_cotxes_preu_resolt.ipynb"
  },
  {
    "codi": "RE_302",
    "bloc": 3,
    "titol": "El 2024 va ser pitjor?",
    "enunciat": "Comparat amb el 2023, el 2024 els accidents van ser més greus? La regidora vol el nombre de morts i de ferits greus per cada 1.000 accidents, per a tota la ciutat i per districte.",
    "dataset": "Accidents de la Guàrdia Urbana a Barcelona (2023 i 2024)",
    "font": "https://opendata-ajuntament.barcelona.cat/data/ca/dataset/accidents-gu-bcn",
    "llicencia": "CC BY 4.0",
    "dificultat": 2,
    "fitxer": "RE_302_accidents_dos_anys.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_302_accidents_dos_anys_resolt.ipynb"
  },
  {
    "codi": "RE_303",
    "bloc": 3,
    "titol": "Es cancel·larà aquesta reserva?",
    "enunciat": "Quin encert (accuracy) es pot prometre a la direcció, amb un model que funcioni el dia que entra la reserva? Han de poder-se'l creure, perquè hi posaran clients al carrer si s'equivoca.",
    "dataset": "Hotel booking demand (TidyTuesday)",
    "font": "https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-02-11",
    "llicencia": "CC BY 4.0",
    "dificultat": 2,
    "fitxer": "RE_303_hotels_cancellacions.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_303_hotels_cancellacions_resolt.ipynb"
  },
  {
    "codi": "RE_304",
    "bloc": 3,
    "titol": "Quina lletra traurà el meu pis?",
    "enunciat": "Quin F1 macro es pot prometre, honestament, amb només aquestes dades? I on s'equivoca?",
    "dataset": "Certificats d'eficiència energètica d'edificis (ICAEN)",
    "font": "https://analisi.transparenciacatalunya.cat/d/j6ii-t3w2",
    "llicencia": "Llicència oberta d'ús d'informació – Catalunya",
    "dificultat": 3,
    "fitxer": "RE_304_certificats_energetics.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_304_certificats_energetics_resolt.ipynb"
  },
  {
    "codi": "RE_401",
    "bloc": 3,
    "titol": "Quins tipus de clients tenim?",
    "enunciat": "Quants grups de clients hi ha, i com els descriuries amb paraules? Han de ser grups que màrqueting pugui fer servir.",
    "dataset": "Wholesale customers (UCI)",
    "font": "https://archive.ics.uci.edu/dataset/292/wholesale+customers",
    "llicencia": "CC BY 4.0",
    "dificultat": 1,
    "fitxer": "RE_401_clients_majorista.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_401_clients_majorista_resolt.ipynb"
  },
  {
    "codi": "RE_402",
    "bloc": 3,
    "titol": "Quants estils hi ha en un número?",
    "enunciat": "Quanta informació diferent hi ha de debò en aquestes 12 columnes? I els grups que surten d'agrupar-les, s'assemblen als gèneres musicals?",
    "dataset": "30.000 cançons de Spotify (TidyTuesday)",
    "font": "https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-01-21",
    "llicencia": "Dades de Spotify, ús educatiu",
    "dificultat": 2,
    "fitxer": "RE_402_spotify_estils.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_402_spotify_estils_resolt.ipynb"
  },
  {
    "codi": "RE_403",
    "bloc": 3,
    "titol": "Quins tipus de municipis té Catalunya?",
    "enunciat": "Quins tipus de municipis hi ha a Catalunya, què els distingeix, i on cau el teu?",
    "dataset": "Indicadors territorials dels municipis de Catalunya",
    "font": "https://analisi.transparenciacatalunya.cat/d/8aaj-ypcb",
    "llicencia": "Domini públic",
    "dificultat": 3,
    "fitxer": "RE_403_municipis_catalunya.ipynb",
    "resolt": "Machine Learning/04_reptes/resolts/RE_403_municipis_catalunya_resolt.ipynb"
  }
];
