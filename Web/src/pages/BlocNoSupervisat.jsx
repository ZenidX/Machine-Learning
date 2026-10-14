import { Link } from "react-router-dom";
import { Layers, BookOpen, Eye, Mountain, ClipboardCheck, AlertTriangle, Wrench, Info } from "lucide-react";
import {
  CapcaleraBloc,
  PassosBloc,
  Pas,
  Seccio,
  QuadernCard,
  AbansDeComencar,
  Reptes,
  QuanCridar,
  ProvaBloc,
  ActivitatsBloc,
  SeguentBloc,
  Chivato,
} from "../components/Bloc";
import { chivatos } from "../data/chivatos";

const C = "teal";

export default function BlocNoSupervisat() {
  return (
    <div className="space-y-8">
      <CapcaleraBloc num={3} icona={Layers} color={C}>
        La diferència entre un dataset de joguina i un de real: nuls, columnes de text, duplicats, i
        com muntar-ho tot sense enganyar-te. I el no supervisat: PCA i k-means. Acaba amb la prova
        pràctica 3, el 21 de desembre.
      </CapcaleraBloc>

      <PassosBloc color={C} />

      <Seccio titol="Què canvia en aquest bloc" icona={Layers} color={C}>
        <div className="space-y-4 text-gray-700">
          <p>
            Fins ara tots els conjunts de dades venien nets, de <code className="text-sm bg-gray-100 px-1 rounded">sklearn.datasets</code>.
            Cap dada real ve així.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
            <div className="bg-gray-50 rounded-lg p-3"><strong>Valors que falten:</strong> esborrar files, esborrar columnes o imputar. Cada opció té un cost, i es mesura.</div>
            <div className="bg-gray-50 rounded-lg p-3"><strong>Columnes de text:</strong> OneHotEncoder, i per què no es codifiquen com a números ordenats.</div>
            <div className="bg-gray-50 rounded-lg p-3"><strong>Escalat:</strong> totes les columnes numèriques a una escala comparable.</div>
            <div className="bg-gray-50 rounded-lg p-3"><strong>Pipelines:</strong> encadenar tots els passos en un sol objecte de scikit-learn, perquè no es puguin fer en l'ordre equivocat.</div>
          </div>
          <div className="flex items-start gap-3 bg-rose-50 border border-rose-200 rounded-lg p-4">
            <AlertTriangle className="w-5 h-5 text-rose-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-rose-900">
              <strong>La idea que t'has d'endur: la fuita d'informació.</strong> Escalar o imputar
              abans de partir el conjunt fa que el test hagi influït en l'entrenament. El número puja i
              és mentida. Un Pipeline ho evita per construcció, no per disciplina. És la mateixa trampa
              que la columna d'identificadors de MA_04, per una altra porta.
            </p>
          </div>
          <p className="text-sm">
            I després, el <strong>no supervisat</strong>: models que no miren la y. El PCA redueix
            dimensions sense haver vist les etiquetes, i tot i així les espècies d'Iris surten
            separades. El k-means busca grups que ningú no li ha dit que hi són.
          </p>
        </div>
      </Seccio>

      <AbansDeComencar />

      {/* ---------- 1 · Aprèn ---------- */}
      <Pas id="apren" num={1} titol="Aprèn" color={C} subtitol="El tancament de l'SVM, les eines per a dades brutes, el PCA i el k-means." />
      <Seccio icona={BookOpen} color={C}>
        <div className="space-y-4">
          <QuadernCard codi="MA_05" color="violet" etiqueta="tanca l'SVM del bloc 2">
            <p className="text-sm text-gray-700 mt-2">
              <strong>L'únic punt del curs que no es deriva fins al final:</strong> el problema dual de
              l'SVM no hi cap en el temps que tenim. El quadern en presenta el resultat, diu clarament que
              no s'ha derivat i el verifica numèricament amb un model entrenat: els punts amb coeficient
              diferent de zero són exactament els vectors de suport. Tota la resta de matemàtiques del curs
              la pots comprovar tu des de zero.
            </p>
            <Chivato f={chivatos.MA_05} />
          </QuadernCard>
          <QuadernCard codi="EX_00" color="indigo" etiqueta="les eines de les dades brutes">
            <p className="text-sm text-gray-700 mt-2">
              SimpleImputer, OneHotEncoder, drop_duplicates, Pipeline i ColumnTransformer: els exemples
              les fan servir totes, i aquí tens què fa cadascuna i el seu parany. Els quaderns de pipelines del
              curs passat són al Moodle.
            </p>
            <Chivato f={chivatos.EX_00_brutes} />
          </QuadernCard>
          <QuadernCard codi="MA_06" color="violet" etiqueta="la porta al no supervisat">
            <Chivato f={chivatos.MA_06} />
          </QuadernCard>
          <QuadernCard codi="ML_06" color={C}>
            <Chivato f={chivatos.ML_06} />
          </QuadernCard>
        </div>
        <div className="mt-4 flex items-start gap-3 bg-gray-50 border border-gray-200 rounded-lg p-4">
          <Info className="w-5 h-5 text-gray-500 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-gray-700">
            Dos avisos del PCA: <strong>cal escalar abans</strong>, perquè mesura variància (amb Wine
            sense escalar és un desastre), i els vectors propis poden sortir amb el signe girat, que no
            és un error. On falla: dos anells concèntrics. Cap projecció lineal els separa, i es canvia
            d'eina, no de paràmetres.
          </p>
        </div>
      </Seccio>

      {/* ---------- 2 · Exemples ---------- */}
      <Pas id="exemples" num={2} titol="Exemples" color={C} subtitol="Exemples resolts: per veure com es fa. L'EX_05 és el més proper a la Pp3." />
      <Seccio icona={Eye} color={C}>
        <div className="space-y-4">
          <QuadernCard codi="EX_05" color={C} etiqueta="exemple resolt">
            <Chivato f={chivatos.EX_05} />
          </QuadernCard>
          <QuadernCard codi="EX_03" color={C} etiqueta="exemple resolt">
            <Chivato f={chivatos.EX_03} />
          </QuadernCard>
          <QuadernCard codi="EX_06" color={C} etiqueta="exemple resolt">
            <Chivato f={chivatos.EX_06} />
          </QuadernCard>
          <p className="text-sm text-gray-700">
            Si una eina no la coneixes, és a la{" "}
            <Link to="/recursos" className="text-teal-700 font-medium hover:text-teal-900 inline-flex items-center gap-1">
              <Wrench className="w-3.5 h-3.5" /> caixa d'eines
            </Link>
            .
          </p>
        </div>
      </Seccio>

      {/* ---------- 3 · Reptes ---------- */}
      <Pas id="reptes" num={3} titol="Reptes" color={C} subtitol="Dades brutes de veritat, i grups que ningú no t'ha dit que hi són." />
      <Seccio icona={Mountain} color={C}>
        <div className="space-y-4">
          <Reptes bloc={3} color={C} />
          <QuanCridar color={C} />
        </div>
      </Seccio>

      {/* ---------- 4 · Prova ---------- */}
      <Pas id="prova" num={4} titol="Prova" color={C} subtitol="A la Pp3 no es mesura la precisió: es mesura si el número que dones és honest." />
      <Seccio icona={ClipboardCheck} color={C}>
        <ProvaBloc bloc={3} color={C} />
        <div className="mt-4">
          <ActivitatsBloc bloc={3} />
        </div>
      </Seccio>

      <SeguentBloc actual={3} />
    </div>
  );
}
