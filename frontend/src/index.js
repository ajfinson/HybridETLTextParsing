// Main frontend entry point
const API_URL = 'http://localhost:8000';

// Sample data to send
const sampleData = [
    { key: "id", value: "1" },
    { key: "name", value: "John Doe" },
    { key: "email", value: "john@example.com" }
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
        const color = result.status === 'success' ? 'green' : 'red';
        document.getElementById('response').innerHTML = `<p style="color: ${color};">Status: ${result.status}</p>`;
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
                <button onclick="sendData()" style="padding: 10px 20px; font-size: 16px; cursor: pointer;">Send Data to API</button>
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
