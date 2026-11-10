const API = "/api/tasks/";
const form = document.getElementById("task-form");
const list = document.getElementById("task-list");
const empty = document.getElementById("empty");
const errorBox = document.getElementById("error");
let tasks = [];
let filter = "all";

async function request(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

function showError(err) {
  errorBox.hidden = !err;
  if (!err) return;
  errorBox.textContent = err.details
    ? err.details.map((d) => d.msg).join("; ")
    : err.error || "Erro inesperado";
}

function render() {
  const visible = tasks.filter((t) =>
    filter === "all" ? true : filter === "done" ? t.completed : !t.completed
  );
  list.replaceChildren(...visible.map(renderTask));
  empty.hidden = visible.length > 0;
}

function renderTask(task) {
  const li = document.createElement("li");
  li.className = task.completed ? "done" : "";

  const check = document.createElement("input");
  check.type = "checkbox";
  check.checked = task.completed;
  check.addEventListener("change", () => update(task.id, { completed: check.checked }));

  const body = document.createElement("div");
  body.className = "body";
  const title = document.createElement("div");
  title.className = "title";
  title.textContent = task.title;
  body.append(title);
  if (task.description) {
    const desc = document.createElement("div");
    desc.className = "desc";
    desc.textContent = task.description;
    body.append(desc);
  }

  const actions = document.createElement("div");
  actions.className = "actions";
  const edit = document.createElement("button");
  edit.textContent = "Editar";
  edit.addEventListener("click", () => editTask(task));
  const del = document.createElement("button");
  del.className = "delete";
  del.textContent = "Excluir";
  del.addEventListener("click", () => remove(task.id));
  actions.append(edit, del);

  li.append(check, body, actions);
  return li;
}

async function load() {
  tasks = await request(API);
  render();
}

async function update(id, changes) {
  try {
    const updated = await request(`${API}${id}`, { method: "PATCH", body: JSON.stringify(changes) });
    tasks = tasks.map((t) => (t.id === id ? updated : t));
    showError(null);
  } catch (err) {
    showError(err);
  }
  render();
}

function editTask(task) {
  const title = prompt("Título:", task.title);
  if (title === null) return;
  const description = prompt("Descrição:", task.description || "");
  if (description === null) return;
  update(task.id, { title, description: description || null });
}

async function remove(id) {
  if (!confirm("Excluir esta tarefa?")) return;
  await request(`${API}${id}`, { method: "DELETE" });
  tasks = tasks.filter((t) => t.id !== id);
  render();
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const body = {
    title: form.title.value.trim(),
    description: form.description.value.trim() || null,
  };
  try {
    const created = await request(API, { method: "POST", body: JSON.stringify(body) });
    tasks.unshift(created);
    form.reset();
    showError(null);
    render();
  } catch (err) {
    showError(err);
  }
});

document.getElementById("filters").addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-filter]");
  if (!btn) return;
  filter = btn.dataset.filter;
  document.querySelectorAll("#filters button").forEach((b) => b.classList.toggle("active", b === btn));
  render();
});

load();
