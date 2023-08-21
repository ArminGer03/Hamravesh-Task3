document.querySelector('form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const start = document.getElementById('start').value;
    const end = document.getElementById('end').value;
    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `start=${start}&end=${end}`
    });
    const result = await response.text();
    document.getElementById('result').textContent = `Random Number: ${result}`;
});

