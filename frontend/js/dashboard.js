if (!getToken()) location.href = "login.html";
const user = getUser();
if (user) document.getElementById("welcome").textContent = `Welcome, ${user.name}`;

// Tab switching
document.querySelectorAll(".sidebar .menu a[data-tab]").forEach(a => {
  a.addEventListener("click", (e) => {
    e.preventDefault();
    document.querySelectorAll(".sidebar .menu a").forEach(x => x.classList.remove("active"));
    a.classList.add("active");
    const tab = a.dataset.tab;
    ["overview","heart","diabetes","obesity","history"].forEach(t =>
      document.getElementById("tab-"+t).hidden = t !== tab);
    if (["heart","diabetes","obesity"].includes(tab)) renderForm(tab);
    if (tab === "history") loadHistory();
  });
});

document.getElementById("heartSubmit").onclick    = () => submitPrediction("heart");
document.getElementById("diabetesSubmit").onclick = () => submitPrediction("diabetes");
document.getElementById("obesitySubmit").onclick  = () => submitPrediction("obesity");

// Charts + stats
let pie, bar;
async function loadOverview() {
  const r = await authFetch("/reports");
  const j = await r.json();
  const setStat = (k, id, barId) => {
    const v = j[k]?.avg_probability;
    document.getElementById(id).textContent = v ? (v*100).toFixed(1)+"%" : "—";
    document.getElementById(barId).style.width = v ? (v*100).toFixed(1)+"%" : "0%";
  };
  setStat("heart","heartAvg","heartBar");
  setStat("diabetes","diabetesAvg","diabetesBar");
  setStat("obesity","obesityAvg","obesityBar");

  const labels = ["Heart","Diabetes","Obesity"];
  const counts = [j.heart?.count||0, j.diabetes?.count||0, j.obesity?.count||0];
  const probs  = [j.heart?.avg_probability||0, j.diabetes?.avg_probability||0, j.obesity?.avg_probability||0];
  pie?.destroy(); bar?.destroy();
  pie = new Chart(document.getElementById("pieChart"), {
    type: "doughnut",
    data: { labels, datasets:[{ data: probs.map(p=> (p*100).toFixed(1)),
      backgroundColor:["#f87171","#fbbf24","#34d399"] }]},
    options:{ plugins:{ legend:{ labels:{ color:"#e6ecf5"} } } }
  });
  bar = new Chart(document.getElementById("barChart"), {
    type: "bar",
    data: { labels, datasets:[{ label:"Predictions", data: counts,
      backgroundColor:"#38bdf8" }]},
    options:{ plugins:{ legend:{ labels:{color:"#e6ecf5"}}},
      scales:{ x:{ticks:{color:"#8a98b3"}}, y:{ticks:{color:"#8a98b3"}}}}
  });
}

async function loadHistory() {
  const r = await authFetch("/history");
  const j = await r.json();
  const list = document.getElementById("historyList");
  if (!j.items.length) { list.innerHTML = "<p style='color:var(--muted)'>No predictions yet.</p>"; return; }
  list.innerHTML = `<table style="width:100%;border-collapse:collapse">
    <thead><tr style="text-align:left;color:var(--muted);font-size:13px">
      <th>Date</th><th>Type</th><th>Model</th><th>Probability</th><th>Risk</th></tr></thead>
    <tbody>${j.items.map(it => `<tr style="border-top:1px solid rgba(255,255,255,.06)">
      <td>${new Date(it.created_at).toLocaleString()}</td>
      <td>${it.kind}</td>
      <td>${it.result.model}</td>
      <td>${it.result.probability ? (it.result.probability*100).toFixed(1)+"%" : "—"}</td>
      <td><span class="risk-tag ${it.result.risk_level}">${it.result.risk_level}</span></td>
    </tr>`).join("")}</tbody></table>`;
}

document.getElementById("downloadBtn").onclick = async () => {
  const r = await authFetch("/history");
  const j = await r.json();
  const blob = new Blob([JSON.stringify(j, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a"); a.href = url; a.download = "health_report.json"; a.click();
  URL.revokeObjectURL(url);
};

// BMI calculator
document.getElementById("bmiBtn").onclick = () => {
  const w = parseFloat(document.getElementById("bmiW").value);
  const h = parseFloat(document.getElementById("bmiH").value)/100;
  if (!w || !h) return;
  const bmi = (w/(h*h));
  document.getElementById("bmiVal").textContent = bmi.toFixed(1);
  const cat = bmi < 18.5 ? "Underweight" : bmi < 25 ? "Normal" : bmi < 30 ? "Overweight" : "Obese";
  document.getElementById("bmiCat").textContent = cat;
};

loadOverview();
