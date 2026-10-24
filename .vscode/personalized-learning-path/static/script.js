const targetSelect = document.getElementById("target");
const generateButton = document.getElementById("generate");
const completedList = document.getElementById("completed-list");
const errorBox = document.getElementById("error");
const pathContainer = document.getElementById("path");

function getCompletedTopics() {
  return [...completedList.querySelectorAll('input[type="checkbox"]:checked')]
    .map(input => input.value);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}

function renderPath(data) {
  document.getElementById("remaining").textContent = data.remaining_count;
  document.getElementById("hours").textContent = `${data.estimated_hours} h`;
  document.getElementById("critical").textContent = `${data.critical_path_hours} h`;
  document.getElementById("path-title").textContent = `Path to ${data.target}`;
  document.getElementById("topic-count").textContent =
    `${data.required_count} required · ${data.completed_count} already completed`;

  if (!data.path.length) {
    pathContainer.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">✓</div>
        <h3>You're all caught up!</h3>
        <p>All topics in the prerequisite path for ${escapeHtml(data.target)} are marked completed.</p>
      </div>`;
    return;
  }

  pathContainer.innerHTML = data.path.map(topic => `
    <article class="path-item">
      <div class="step">${topic.step}</div>
      <div>
        <h3>${escapeHtml(topic.name)}</h3>
        <p>${escapeHtml(topic.description)}</p>
        <span class="tag">${escapeHtml(topic.difficulty)}</span>
        ${topic.prerequisites.length
          ? `<span class="tag">Needs: ${topic.prerequisites.map(escapeHtml).join(", ")}</span>`
          : `<span class="tag">Starting topic</span>`}
      </div>
      <div class="meta"><strong>${topic.hours} hour${topic.hours === 1 ? "" : "s"}</strong></div>
    </article>`).join("");
}

async function generatePath() {
  errorBox.textContent = "";
  generateButton.disabled = true;
  generateButton.textContent = "Generating…";
  try {
    const response = await fetch("/api/path", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        target: targetSelect.value,
        completed: getCompletedTopics()
      })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not generate a path.");
    renderPath(data);
  } catch (error) {
    errorBox.textContent = error.message;
  } finally {
    generateButton.disabled = false;
    generateButton.textContent = "Generate my learning path";
  }
}

generateButton.addEventListener("click", generatePath);
generatePath();
