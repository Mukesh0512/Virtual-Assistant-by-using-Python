const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

let pendingAction = null;

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

      // Set up pending action instead of immediately opening
      if (data.reply.includes("Opening YouTube")) {
        pendingAction = () => window.open("https://youtube.com", "_blank");
      } else if (data.reply.includes("Opening Google")) {
        pendingAction = () => window.open("https://google.com", "_blank");
      } else if (data.reply.includes("Opening Facebook")) {
        pendingAction = () => window.open("https://facebook.com", "_blank");
      } else if (data.reply.includes("Opening LinkedIn")) {
        pendingAction = () => window.open("https://linkedin.com", "_blank");
      } else {
        pendingAction = null;
      }
    });
  };

  recognition.onend = () => {
    // 🔥 Now it's allowed since it's in user gesture scope
    if (pendingAction) {
      pendingAction();
      pendingAction = null;
    }
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
