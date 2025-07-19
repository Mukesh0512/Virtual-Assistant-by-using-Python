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

      // Auto-link + click method (avoids popup block)
      const link = document.getElementById("fake-link");
      if (data.reply.includes("Opening YouTube")) {
        link.href = "https://youtube.com";
        link.click();
      } else if (data.reply.includes("Opening Google")) {
        link.href = "https://google.com";
        link.click();
      } else if (data.reply.includes("Opening Facebook")) {
        link.href = "https://facebook.com";
        link.click();
      } else if (data.reply.includes("Opening LinkedIn")) {
        link.href = "https://linkedin.com";
        link.click();
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
