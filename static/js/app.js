const chatWindow = document.getElementById("chat-window");
const input = document.getElementById("message");
const sendBtn = document.getElementById("send");
const loader = document.getElementById("loader");
const sessionId = crypto.randomUUID();

const typeText = async (el, text) => {
  el.textContent = "";
  for (const ch of text) {
    el.textContent += ch;
    await new Promise((r) => setTimeout(r, 10));
  }
};

const addMessage = async (text, cls, typing = false) => {
  const div = document.createElement("div");
  div.className = `msg ${cls}`;
  chatWindow.appendChild(div);
  if (typing) await typeText(div, text); else div.textContent = text;
  chatWindow.scrollTop = chatWindow.scrollHeight;
};

const sendMessage = async () => {
  const message = input.value.trim();
  if (!message) return;
  input.value = "";
  await addMessage(message, "user");
  loader.classList.remove("hidden");
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message })
    });
    const data = await res.json();
    const recommendations = (data.recommendations || []).map((r, i) => `${i+1}. ${r.name} (confidence ${r.confidence})`).join("\n");
    const text = `${data.reply}${recommendations ? "\n" + recommendations : ""}`;
    await addMessage(text, "bot", true);
  } catch {
    await addMessage("Something went wrong. Please try again.", "bot", true);
  } finally {
    loader.classList.add("hidden");
  }
};

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => e.key === "Enter" && sendMessage());
addMessage("Hi! Tell me the role, seniority, and skills you are hiring for.", "bot", true);
