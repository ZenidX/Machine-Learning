import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Programa from './pages/Programa'
import Avaluacio from './pages/Avaluacio'
import Python from './pages/Python'
import Fonaments from './pages/Fonaments'
import MachineLearning from './pages/MachineLearning'
import Matematiques from './pages/Matematiques'
import Practica from './pages/Practica'
import DeepRL from './pages/DeepRL'
import Recursos from './pages/Recursos'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/programa" element={<Programa />} />
        <Route path="/avaluacio" element={<Avaluacio />} />
        <Route path="/python" element={<Python />} />
        <Route path="/fonaments" element={<Fonaments />} />
        <Route path="/machine-learning" element={<MachineLearning />} />
        <Route path="/matematiques" element={<Matematiques />} />
        <Route path="/practica" element={<Practica />} />
        <Route path="/deep-rl" element={<DeepRL />} />
        <Route path="/recursos" element={<Recursos />} />
      </Routes>
    </Layout>
  )
}

export default App
