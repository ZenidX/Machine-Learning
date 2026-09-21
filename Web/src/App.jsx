import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Programa from './pages/Programa'
import Python from './pages/Python'
import MachineLearning from './pages/MachineLearning'
import DeepRL from './pages/DeepRL'
import Recursos from './pages/Recursos'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/programa" element={<Programa />} />
        <Route path="/python" element={<Python />} />
        <Route path="/machine-learning" element={<MachineLearning />} />
        <Route path="/deep-rl" element={<DeepRL />} />
        <Route path="/recursos" element={<Recursos />} />
      </Routes>
    </Layout>
  )
}

export default App
