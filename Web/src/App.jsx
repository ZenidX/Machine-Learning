import { useEffect } from 'react'
import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Calendari from './pages/Calendari'
import BlocDades from './pages/BlocDades'
import BlocSupervisat from './pages/BlocSupervisat'
import BlocNoSupervisat from './pages/BlocNoSupervisat'
import BlocXarxesRL from './pages/BlocXarxesRL'
import Recursos from './pages/Recursos'
import Pp1 from './pages/Pp1'

// Rutes antigues: redirigeixen a la pàgina nova perquè els enllaços que ja circulen no es trenquin.
const REDIRECCIONS = {
  '/programa': '/calendari',
  '/avaluacio': '/calendari',
  '/python': '/dades',
  '/fonaments': '/dades',
  '/machine-learning': '/supervisat',
  '/practica': '/supervisat',
  '/matematiques': '/supervisat',
  '/deep-rl': '/xarxes-i-rl',
}

function ScrollAmunt() {
  const { pathname } = useLocation()
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])
  return null
}

function App() {
  return (
    <Layout>
      <ScrollAmunt />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/calendari" element={<Calendari />} />
        <Route path="/dades" element={<BlocDades />} />
        <Route path="/supervisat" element={<BlocSupervisat />} />
        <Route path="/no-supervisat" element={<BlocNoSupervisat />} />
        <Route path="/xarxes-i-rl" element={<BlocXarxesRL />} />
        <Route path="/recursos" element={<Recursos />} />
        <Route path="/pp1" element={<Pp1 />} />
        {Object.entries(REDIRECCIONS).map(([de, a]) => (
          <Route key={de} path={de} element={<Navigate to={a} replace />} />
        ))}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  )
}

export default App
