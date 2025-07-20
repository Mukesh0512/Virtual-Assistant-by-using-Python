const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const bgMusic = document.getElementById("bg-music");
const startupSound = document.getElementById("startup-sound");
const shutdownSound = document.getElementById("shutdown-sound");
const errorSound = document.getElementById("error-sound");

const historyList = document.getElementById("command-history");
const startBtn = document.getElementById("start-btn");

let isMusicPlaying = false;

function playStartup() {
  startupSound.play();
}

function playShutdown() {
  shutdownSound.play();
}

function playError() {
  errorSound.play();
}

function typeWriterEffect(text, elementId) {
  let i = 0;
  const speed = 40;
  const target = document.getElementById(elementId);
  target.innerText = "";

  const typing = setInterval(() => {
    target.innerText += text.charAt(i);
    i++;
    if (i >= text.length) clearInterval(typing);
  }, speed);
}

function addToHistory(command, response) {
  const li = document.createElement("li");
  li.textContent = `🗣️ ${command} → 💬 ${response}`;
  li.onclick = () => {
    document.getElementById("user-text").innerText = "You said: " + command;
    typeWriterEffect(response, "response-text");
    speak(response);
  };
  historyList.prepend(li);
}

function speak(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'en-US';
  speechSynthesis.speak(utterance);
}

if (SpeechRecognition) {
  const recognition = new SpeechRecognition();
  recognition.lang = 'en-US';

  startBtn.addEventListener("click", () => {
    if (!isMusicPlaying) {
      bgMusic.volume = 0.3;
      bgMusic.loop = true;
      bgMusic.play();
      isMusicPlaying = true;
    }
    recognition.start();
  });

  recognition.onresult = (event) => {
    const userSpeech = event.results[0][0].transcript.toLowerCase();
    document.getElementById("user-text").innerText = "You said: " + userSpeech;

    fetch("/process", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userSpeech })
    })
    .then(res => res.json())
    .then(data => {
      const reply = data.reply;
      const sound = data.playSound;

      typeWriterEffect(reply, "response-text");
      speak(reply);
      addToHistory(userSpeech, reply);

      if (sound === "shutdown") {
        playShutdown();
      } else if (sound === "startup") {
        playStartup();
      } else if (sound === "error") {
        playError();
      }

      // Auto redirect
      const link = document.getElementById("fake-link");
      if (reply.includes("Opening YouTube")) {
        link.href = "https://youtube.com";
        link.click();
      } else if (reply.includes("Opening Google")) {
        link.href = "https://google.com";
        link.click();
      } else if (reply.includes("Opening Facebook")) {
        link.href = "https://facebook.com";
        link.click();
      } else if (reply.includes("Opening LinkedIn")) {
        link.href = "https://linkedin.com";
        link.click();
      }
    })
    .catch(err => {
      console.error(err);
      typeWriterEffect("⚠️ Error occurred!", "response-text");
      playError();
    });
  };

  recognition.onerror = (event) => {
    alert("🎤 Microphone error: " + event.error);
    playError();
  };
} else {
  alert("Speech Recognition not supported in this browser.");
  playError();
}

