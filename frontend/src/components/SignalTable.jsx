import API from '../api'


function SignalTable({ signals }) {
    const removeSignal = async (id) => {
        try {
            await API.delete(`/api/signals/${id}`)
            window.location.reload()
        } catch (e) {
            console.log(e)
        }
    }

    return (
        <table>
            <thead>
                <tr>
                    <th>Symbol</th>
                    <th>Direction</th>
                    <th>Entry</th>
                    <th>Target</th>
                    <th>Stop Loss</th>
                    <th>Current</th>
                    <th>Status</th>
                    <th>ROI %</th>
                    <th>Expiry Left</th>
                    <th></th>
                </tr>
            </thead>

            <tbody>
                {signals.map((item) => (
                    <tr key={item.id}>
                        <td>{item.symbol}</td>
                        <td>{item.direction}</td>
                        <td>{item.entry_price}</td>
                        <td>{item.target_price}</td>
                        <td>{item.stop_loss}</td>
                        <td>{item.current_price || '-'}</td>
                        <td>{item.status}</td>
                        <td>{item.roi || 0}%</td>
                        <td>{item.time_remaining}</td>
                        <td>
                            <button onClick={() => removeSignal(item.id)}>
                                Delete
                            </button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    )
}


export default SignalTable