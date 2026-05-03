const generateTab = document.getElementById("tab-generate");
const historyTab = document.getElementById("tab-history");
const generateView = document.getElementById("generate-view");
const historyView = document.getElementById("history-view");
const urlInput = document.getElementById("wiki-url");
const generateBtn = document.getElementById("generate-btn");
const statusEl = document.getElementById("status");
const quizOutput = document.getElementById("quiz-output");
const historyBody = document.getElementById("history-body");
const modal = document.getElementById("modal");
const modalInner = document.getElementById("modal-content-inner");
const closeModal = document.getElementById("close-modal");

function setActiveTab(isGenerate) {
  generateTab.classList.toggle("active", isGenerate);
  historyTab.classList.toggle("active", !isGenerate);
  generateView.classList.toggle("active", isGenerate);
  historyView.classList.toggle("active", !isGenerate);
}

function quizHTML(data) {
  const entities = data.key_entities || {};
  return `
    <div class="card">
      <h2>${data.title}</h2>
      <p><b>URL:</b> <a href="${data.url}" target="_blank">${data.url}</a></p>
      <p>${data.summary}</p>
      <p><b>Sections:</b> ${(data.sections || []).join(", ")}</p>
      <p><b>People:</b> ${(entities.people || []).join(", ")}</p>
      <p><b>Organizations:</b> ${(entities.organizations || []).join(", ")}</p>
      <p><b>Locations:</b> ${(entities.locations || []).join(", ")}</p>
      <p><b>Related Topics:</b> ${(data.related_topics || []).join(", ")}</p>
    </div>
    ${(data.quiz || [])
      .map(
        (q, idx) => `
      <div class="card">
        <h3>Q${idx + 1}. ${q.question}</h3>
        <ul>${q.options.map((o) => `<li>${o}</li>`).join("")}</ul>
        <p><b>Answer:</b> ${q.answer}</p>
        <p><b>Difficulty:</b> ${q.difficulty}</p>
        <p><b>Explanation:</b> ${q.explanation}</p>
      </div>
    `
      )
      .join("")}
  `;
}

async function generateQuiz() {
  const url = urlInput.value.trim();
  if (!url) {
    statusEl.textContent = "Enter a Wikipedia URL.";
    return;
  }

  statusEl.textContent = "Generating quiz...";
  quizOutput.innerHTML = "";

  try {
    const response = await fetch("/api/quizzes/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Failed to generate quiz.");
    }
    quizOutput.innerHTML = quizHTML(data);
    statusEl.textContent = "Quiz ready.";
    await loadHistory();
  } catch (err) {
    statusEl.textContent = err.message;
  }
}

async function loadHistory() {
  const response = await fetch("/api/quizzes");
  const rows = await response.json();
  historyBody.innerHTML = rows
    .map(
      (r) => `
    <tr>
      <td>${r.id}</td>
      <td>${r.title}</td>
      <td><a href="${r.url}" target="_blank">link</a></td>
      <td>${new Date(r.created_at).toLocaleString()}</td>
      <td><button class="detail-btn" data-id="${r.id}">Details</button></td>
    </tr>
  `
    )
    .join("");
}

historyBody.addEventListener("click", async (event) => {
  const button = event.target.closest(".detail-btn");
  if (!button) return;
  const id = button.getAttribute("data-id");
  const response = await fetch(`/api/quizzes/${id}`);
  const data = await response.json();
  modalInner.innerHTML = quizHTML(data);
  modal.classList.remove("hidden");
});

closeModal.addEventListener("click", () => modal.classList.add("hidden"));
generateBtn.addEventListener("click", generateQuiz);
generateTab.addEventListener("click", () => setActiveTab(true));
historyTab.addEventListener("click", async () => {
  setActiveTab(false);
  await loadHistory();
});
