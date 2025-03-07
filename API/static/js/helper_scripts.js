document.addEventListener("DOMContentLoaded", function() {
    const pinDisplay = document.getElementById("pinDisplay");
    let pinCode_length = 0;

    function updatePinDisplay(pinCodeL) {
        pinCode_length = pinCodeL;
        pinDisplay.textContent = '*'.repeat(pinCode_length);
    }

    window.updatePinDisplay = updatePinDisplay;
    
});