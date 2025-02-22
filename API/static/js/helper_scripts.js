document.addEventListener("DOMContentLoaded", function() {
    const unlockButton = document.getElementById("unlockButton");

    unlockButton.addEventListener("click", function() {
        fetch("/unlock", {
            method: "POST"
        });

        window.location.reload();
    });
} );
