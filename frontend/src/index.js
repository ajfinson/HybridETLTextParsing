// Main frontend entry point
const API_URL = 'http://localhost:8000';

// Sample data with mix of valid and invalid events
const sampleData = [
    { "event_id": "e1", "user_id": "u1", "source": "web", "lang": "en", "ts": "2026-02-10T08:30:12+00:00", "ref": "Genesis 1:1-3" },
    { "event_id": "e2", "user_id": "u2", "source": "mobile", "lang": "he", "ref": "Exodus 3:14" },
    { "event_id": "e3", "source": "web", "lang": "en", "ref": "John 1:1" },  // Missing user_id
    { "event_id": "e4", "user_id": "u4", "source": "web" },  // Missing ref
    { "event_id": "e5", "user_id": "u5", "source": "partner", "lang": "en", "ref": "Matthew 5:1-12" }
];

const sendData = async () => {
    try {
        const response = await fetch(`${API_URL}/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(sampleData)
        });
        const result = await response.json();
        
        let html = '<h2>Processing Results</h2>';
        
        // Stats
        html += '<div style="background: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 20px;">';
        html += '<h3>Statistics</h3>';
        html += `<p>Total Input: ${result.stats.total_in}</p>`;
        html += `<p>Total Normalized: ${result.stats.total_out}</p>`;
        html += `<p>Total Quarantined: ${result.stats.total_quarantined}</p>`;
        if (Object.keys(result.stats.errors_by_type).length > 0) {
            html += '<p>Errors: ' + JSON.stringify(result.stats.errors_by_type) + '</p>';
        }
        html += '</div>';
        
        // Normalized events
        if (result.normalized.length > 0) {
            html += '<div style="background: #e8f5e9; padding: 10px; border-radius: 5px; margin-bottom: 20px;">';
            html += '<h3>Normalized Events (' + result.normalized.length + ')</h3>';
            html += '<pre style="background: white; padding: 10px; overflow-x: auto;">' + JSON.stringify(result.normalized, null, 2) + '</pre>';
            html += '</div>';
        }
        
        // Quarantined events
        if (result.quarantined.length > 0) {
            html += '<div style="background: #ffebee; padding: 10px; border-radius: 5px;">';
            html += '<h3>Quarantined Events (' + result.quarantined.length + ')</h3>';
            html += '<pre style="background: white; padding: 10px; overflow-x: auto;">' + JSON.stringify(result.quarantined, null, 2) + '</pre>';
            html += '</div>';
        }
        
        document.getElementById('response').innerHTML = html;
    } catch (error) {
        document.getElementById('response').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
};

document.addEventListener('DOMContentLoaded', async () => {
    const root = document.getElementById('root');
    
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        
        root.innerHTML = `
            <header>
                <h1>HybridETL Text Parsing</h1>
            </header>
            <main>
                <p>API Status: ${data.status}</p>
                <button onclick="sendData()" style="padding: 10px 20px; font-size: 16px; cursor: pointer; background: #007bff; color: white; border: none; border-radius: 5px;">Send Data to API</button>
                <div id="response" style="margin-top: 20px;"></div>
            </main>
        `;
    } catch (error) {
        root.innerHTML = `
            <header>
                <h1>HybridETL Text Parsing</h1>
            </header>
            <main>
                <p style="color: red;">Error connecting to API: ${error.message}</p>
            </main>
        `;
    }
});
