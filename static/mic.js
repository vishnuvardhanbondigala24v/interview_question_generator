<<<<<<< HEAD
function startDictation(targetId) {
    if (!('webkitSpeechRecognition' in window)) {
        alert('Speech recognition only works in Chrome.');
        return;
    }
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function(event) {
        document.getElementById(targetId).value = event.results[0][0].transcript;
    };
}
=======
function startDictation(targetId) {
    if (!('webkitSpeechRecognition' in window)) {
        alert('Speech recognition only works in Chrome.');
        return;
    }
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function(event) {
        document.getElementById(targetId).value = event.results[0][0].transcript;
    };
}
>>>>>>> 2f06ed24ae254f36f58dd8d183fcca7d75ca7d18
