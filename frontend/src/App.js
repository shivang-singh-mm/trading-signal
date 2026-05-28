import { useEffect, useState } from 'react'
import API from './api'
import SignalForm from './components/SignalForm'
import SignalTable from './components/SignalTable'


function App() {
  const [signals, setSignals] = useState([])

  const loadSignals = async () => {
    try {
      const res = await API.get('/api/signals')
      setSignals(res.data)
    } catch (e) {
      console.log(e)
    }
  }

  useEffect(() => {
    loadSignals()

    const timer = setInterval(() => {
      loadSignals()
    }, 15000)

    return () => clearInterval(timer)
  }, [])

  return (
    <div className="container">
      <h2>Trading Signal Tracker</h2>

      <SignalForm reload={loadSignals} />

      <SignalTable signals={signals} />
    </div>
  )
}


export default App