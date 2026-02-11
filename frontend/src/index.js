// Main frontend entry point
const API_URL = 'http://localhost:8000';

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
