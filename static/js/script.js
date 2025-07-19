const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
  const recognition = new SpeechRecognition();
  recognition.lang = 'en-US';

  document.getElementById("start-btn").addEventListener("click", () => {
    recognition.start();
  });

  recognition.onresult = (event) => {
    const userSpeech = event.results[0][0].transcript;
    document.getElementById("user-text").innerText = "You said: " + userSpeech;

    fetch("/process", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: userSpeech })
    })
    .then(res => res.json())
    .then(data => {
      speak(data.reply);
    });
  };

  recognition.onerror = (event) => {
    alert("🎤 Microphone error: " + event.error);
  };

} else {
  alert("Speech Recognition not supported in this browser.");
}

function speak(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'en-US';
  speechSynthesis.speak(utterance);
}
