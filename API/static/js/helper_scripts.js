document.addEventListener("DOMContentLoaded", function() {
    const pinDisplay = document.getElementById("pinDisplay");
    let pinCode_length = 0;

    function updatePinDisplay(pinCodeL) {
        pinCode_length = pinCodeL;
        pinDisplay.textContent = '*'.repeat(pinCode_length);
    }

    function shakePinDisplay() {
        pinDisplay.textContent = '*'.repeat(4);
        pinDisplay.classList.add("shake");
        setTimeout(() => {
            pinDisplay.classList.remove("shake");
        }, 1000);
    }

    window.updatePinDisplay = updatePinDisplay;
    window.shakePinDisplay = shakePinDisplay;
    
});