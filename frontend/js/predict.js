// Field definitions for the three prediction forms.
const FIELDS = {
  heart: [
    ["age","Age",29,77,54],["sex","Sex (0=F,1=M)",0,1,1],
    ["cp","Chest pain type (0-3)",0,3,1],["trestbps","Resting BP",90,200,130],
    ["chol","Cholesterol",120,570,240],["fbs","Fasting sugar >120 (0/1)",0,1,0],
    ["restecg","Rest ECG (0-2)",0,2,1],["thalach","Max heart rate",70,210,150],
    ["exang","Exercise angina (0/1)",0,1,0],["oldpeak","ST depression",0,7,1],
    ["slope","ST slope (0-2)",0,2,1],["ca","Major vessels (0-4)",0,4,0],
    ["thal","Thalassemia (0-3)",0,3,2],
  ],
  diabetes: [
    ["Pregnancies","Pregnancies",0,17,1],["Glucose","Glucose",0,200,120],
    ["BloodPressure","Blood pressure",0,140,70],["SkinThickness","Skin thickness",0,99,20],
    ["Insulin","Insulin",0,900,80],["BMI","BMI",0,70,28],
    ["DiabetesPedigreeFunction","Pedigree fn",0,3,0.5],["Age","Age",10,100,33],
  ],
  obesity: [
    ["Gender","Gender (0=F,1=M)",0,1,1],["Age","Age",10,80,25],
    ["Height","Height (m)",1.0,2.2,1.7],["Weight","Weight (kg)",30,200,70],
    ["family_history_with_overweight","Family overweight (0/1)",0,1,1],
    ["FAVC","High calorie food (0/1)",0,1,1],["FCVC","Veg freq (1-3)",1,3,2],
    ["NCP","# main meals (1-4)",1,4,3],["CAEC","Snack freq (0-3)",0,3,2],
    ["SMOKE","Smoke (0/1)",0,1,0],["CH2O","Water L/day (1-3)",1,3,2],
    ["SCC","Calorie monitor (0/1)",0,1,0],["FAF","Physical activity (0-3)",0,3,1],
    ["TUE","Tech use hrs (0-2)",0,2,1],["CALC","Alcohol freq (0-3)",0,3,1],
    ["MTRANS","Transport (0-4)",0,4,2],
  ],
};

function renderForm(kind) {
  const form = document.getElementById(kind + "Form");
  if (!form || form.dataset.rendered) return;
  form.dataset.rendered = "1";
  for (const [name, label, min, max, def] of FIELDS[kind]) {
    form.insertAdjacentHTML("beforeend", `
      <div><label style="display:block;color:var(--muted);font-size:12px;margin-bottom:4px">${label}</label>
        <input name="${name}" type="number" step="any" min="${min}" max="${max}" value="${def}" required
          style="width:100%;padding:10px;border-radius:8px;background:var(--surface-2);border:1px solid rgba(255,255,255,.08);color:var(--text)"/>
      </div>`);
  }
}

async function submitPrediction(kind) {
  renderForm(kind);
  const form = document.getElementById(kind + "Form");
  const payload = {};
  new FormData(form).forEach((v,k)=> payload[k] = parseFloat(v));
  const btn = document.getElementById(kind + "Submit");
  btn.innerHTML = '<span class="loading"></span> Predicting…';
  try {
    const r = await authFetch(`/predict/${kind}`, { method: "POST", body: JSON.stringify(payload) });
    const j = await r.json();
    if (!r.ok) throw new Error(j.error || "Prediction failed");
    showResultModal(kind, j);
  } catch (e) { alert(e.message); }
  btn.innerHTML = "Predict";
}

function showResultModal(kind, j) {
  document.getElementById("rmTitle").textContent = `${kind.toUpperCase()} — ${j.model}`;
  const pct = j.probability ? (j.probability*100).toFixed(1) : "—";
  document.getElementById("rmText").innerHTML =
    `Prediction: <b>${j.prediction}</b> · Probability: <b>${pct}%</b> · ` +
    `<span class="risk-tag ${j.risk_level}">${j.risk_level.toUpperCase()} RISK</span>`;
  document.getElementById("rmRecs").innerHTML =
    "<ul>" + j.recommendations.map(r=>`<li>${r}</li>`).join("") + "</ul>";
  document.getElementById("resultModal").classList.add("open");
}
document.getElementById("rmClose")?.addEventListener("click", () =>
  document.getElementById("resultModal").classList.remove("open"));
