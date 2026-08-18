const form = document.getElementById('predict-form');
const result = document.getElementById('result');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form));
  const payload = { ...data, age: Number(data.age), balance: Number(data.balance), campaign: Number(data.campaign) };
  result.hidden = false;
  result.textContent = 'Consultando modelo...';
  try {
    const response = await fetch('/predict', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) });
    const body = await response.json();
    if (!response.ok) throw new Error(body.detail || 'Solicitud inválida');
    result.innerHTML = `<strong>Probabilidad estimada de contratación: ${(body.probability * 100).toFixed(0)}%</strong><br><span>Clase del modelo: ${body.classification}</span><small> Predicción: ${body.prediction}</small>`;
  } catch (error) { result.textContent = `Error: ${error.message}`; }
});
