document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent form from submitting normally
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const msgsElement = document.getElementById('msgs');
    
    msgsElement.innerHTML = ''; // Clear previous messages
    console.log('Sending data');

    try {
        const response = await fetch('/ajaxkeyvalue', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data.status === 'ok') {
            window.location.href = 'profile';
        } else {
            msgsElement.innerHTML = `<p style="color:red;">Error: ${data.error || 'Unknown error'}</p>`;
        }
    } catch (error) {
        console.error('Error:', error);
        msgsElement.innerHTML = `<p style="color:red;">Network Error</p>`;
    }
});
