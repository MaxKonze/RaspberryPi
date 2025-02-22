document.addEventListener("DOMContentLoaded", function() {
    const lockButton = document.getElementById("lockButton");
    const unlockButton = document.getElementById("unlockButton");
    const statusButton = document.getElementById("statusButton");
    const statusMessage = document.getElementById("statusMessage");

    console.log("DOM fully loaded and parsed");

    lockButton.addEventListener("click", async function() {
        const response = await fetch("/lock");
        const data = await response.json();
        updateStatus();
    });

    unlockButton.addEventListener("click", async function() {
        const response = await fetch("/unlock", {
            method: "POST"
        });
        const data = await response.json();
        updateStatus();
    });


    async function updateStatus() {
        const response = await fetch("/status", {
            method: "POST"
        });
        const data = await response.json();
        statusMessage.textContent = data.locked ? "Die Tür ist verriegelt." : "Die Tür ist entriegelt.";

        if (data.locked) {
            window.location.reload();
        }
    }
    updateStatus();
});