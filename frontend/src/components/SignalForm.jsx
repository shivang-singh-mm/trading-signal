import { useState } from 'react'
import API from '../api'


function SignalForm({ reload }) {
    const [form, setForm] = useState({
        symbol: '',
        direction: 'BUY',
        entry_price: '',
        stop_loss: '',
        target_price: '',
        entry_time: '',
        expiry_time: ''
    })

    const [error, setError] = useState('')

    const changeValue = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    const submitData = async (e) => {
        e.preventDefault()

        setError('')

        try {
            await API.post('/api/signals', form)

            setForm({
                symbol: '',
                direction: 'BUY',
                entry_price: '',
                stop_loss: '',
                target_price: '',
                entry_time: '',
                expiry_time: ''
            })

            reload()
        } catch (e) {
            setError(e.response?.data?.message || 'Something went wrong')
        }
    }

    return (
        <form onSubmit={submitData} className="formBox">
            <input
                type="text"
                name="symbol"
                placeholder="BTCUSDT"
                value={form.symbol}
                onChange={changeValue}
                required
            />

            <select
                name="direction"
                value={form.direction}
                onChange={changeValue}
            >
                <option value="BUY">BUY</option>
                <option value="SELL">SELL</option>
            </select>

            <input
                type="number"
                step="0.01"
                name="entry_price"
                placeholder="Entry Price"
                value={form.entry_price}
                onChange={changeValue}
                required
            />

            <input
                type="number"
                step="0.01"
                name="stop_loss"
                placeholder="Stop Loss"
                value={form.stop_loss}
                onChange={changeValue}
                required
            />

            <input
                type="number"
                step="0.01"
                name="target_price"
                placeholder="Target Price"
                value={form.target_price}
                onChange={changeValue}
                required
            />

            <input
                type="datetime-local"
                name="entry_time"
                value={form.entry_time}
                onChange={changeValue}
                required
            />

            <input
                type="datetime-local"
                name="expiry_time"
                value={form.expiry_time}
                onChange={changeValue}
                required
            />

            <button>Create Signal</button>

            {error && <p className="error">{error}</p>}
        </form>
    )
}


export default SignalForm