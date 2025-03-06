document.addEventListener("DOMContentLoaded", function() {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onopen = () => {
        console.log("Verbunden mit WebSocket-Server");
    };

    ws.onmessage = (event) => {
        const message = event.data;
        console.log(`Nachricht vom Server: ${message}`);
        if (message === "lock" || message === "unlock") {
            window.location.reload();
        }
        if (message === "key") {
            console.log("Key received");
        }

    };

    ws.onclose = () => {
        console.log("Verbindung zum WebSocket-Server getrennt");
    };

});