document.addEventListener("DOMContentLoaded", function() {
    const ws = new WebSocket("ws://localhost:8000/ws");
    let pinCode_length = 0;

    ws.onopen = () => {
        console.log("Verbunden mit WebSocket-Server");
    };

    ws.onmessage = (event) => {
        const message = event.data;
        console.log(`Nachricht vom Server: ${message}`);
        if (message === "lock" || message === "unlock") {
            window.location.reload();
        }
        if (message === "false")
            window.shakePinDisplay()

        if (message.slice(0,3) === "key") {
            console.log("Key received");
            pinCode_length = message.slice(3,4);

            window.updatePinDisplay(pinCode_length);
        }

    };

    ws.onclose = () => {
        console.log("Verbindung zum WebSocket-Server getrennt");
    };

});