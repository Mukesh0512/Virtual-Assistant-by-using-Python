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
      // If the reply contains a known phrase, trigger opening in new tab
  if (data.reply.includes("Opening YouTube")) {
    window.open("https://youtube.com", "_blank");
  } else if (data.reply.includes("Opening Google")) {
    window.open("https://google.com", "_blank");
  } else if (data.reply.includes("Opening Facebook")) {
    window.open("https://facebook.com", "_blank");
  } else if (data.reply.includes("Opening LinkedIn")) {
    window.open("https://linkedin.com", "_blank");
  }
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
