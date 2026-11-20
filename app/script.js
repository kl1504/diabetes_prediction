const API_URL = "http://127.0.0.1:5000/predict";

const FIELDS = [
  "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
  "Insulin", "BMI", "DiabetesPedigreeFunction", "Age",
];

const EXAMPLE = {
  Pregnancies: 2, Glucose: 150, BloodPressure: 70, SkinThickness: 30,
  Insulin: 100, BMI: 33.6, DiabetesPedigreeFunction: 0.5, Age: 45,
};

const $ = (id) => document.getElementById(id);
const STATES = ["state-empty", "state-loading", "state-result", "state-error"];

function showState(name) {
  STATES.forEach((s) => $(s).classList.toggle("hidden", s !== name));
}

function markInvalid(input, invalid) {
  input.classList.toggle("border-warn", invalid);
  input.classList.toggle("focus:ring-warn/30", invalid);
  input.setAttribute("aria-invalid", invalid ? "true" : "false");
}

// Exemple de valeurs
$("fill-example").addEventListener("click", () => {
  FIELDS.forEach((f) => {
    $(f).value = EXAMPLE[f];
    markInvalid($(f), false);
  });
});

// Réinitialisation
$("reset").addEventListener("click", () => {
  FIELDS.forEach((f) => markInvalid($(f), false));
  $("result-marker").style.left = "0%";
  showState("state-empty");
});

// Envoi du formulaire
$("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  // Validation simple : champs vides
  const data = {};
  let firstInvalid = null;
  FIELDS.forEach((f) => {
    const input = $(f);
    const value = parseFloat(input.value);
    const invalid = Number.isNaN(value) || value < 0;
    markInvalid(input, invalid);
    if (invalid && !firstInvalid) firstInvalid = input;
    data[f] = value;
  });

  if (firstInvalid) {
    $("error-message").textContent =
      "Un ou plusieurs champs sont vides ou négatifs. Corrigez les champs en rouge.";
    showState("state-error");
    firstInvalid.focus();
    return;
  }

  const button = $("submit");
  button.disabled = true;
  showState("state-loading");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Erreur " + response.status);
    const result = await response.json();
    displayResult(result);
  } catch (err) {
    $("error-message").textContent =
      "L'API ne répond pas. Vérifiez que « python app.py » est lancé, puis réessayez.";
    showState("state-error");
  } finally {
    button.disabled = false;
  }
});

function displayResult({ prediction, probability, result }) {
  const percent = Math.round(probability * 100);
  const high = prediction === 1;

  $("result-label").textContent = result;
  $("result-label").className =
    "font-display text-2xl font-bold leading-snug " + (high ? "text-warn" : "text-ok");

  $("result-percent").textContent = percent + " %";
  $("result-advice").textContent = high
    ? "Vos valeurs ressemblent à celles de patientes diagnostiquées. Un contrôle chez un médecin permettrait de le confirmer ou non."
    : "Vos valeurs ressemblent plutôt à celles de patientes non diabétiques. Gardez des contrôles réguliers.";

  showState("state-result");

  // Anime le curseur depuis 0 jusqu'à la valeur
  const marker = $("result-marker");
  marker.style.left = "0%";
  requestAnimationFrame(() => requestAnimationFrame(() => {
    marker.style.left = Math.min(Math.max(percent, 2), 98) + "%";
  }));
}
