function estimateKcal() {
  const byId = (id) => document.getElementById(id);

  const weight = Number(byId("weight")?.value) || 70;     // default 70kg
  const height = Number(byId("height")?.value) || 170;    // default 170cm
  const age    = Number(byId("age")?.value)    || 30;     // default 30y
  const male   = (byId("is_male")?.value || "1") === "1"; // default male
  const act    = Number(byId("activity_level")?.value) || 1.55; // default moderate
  const obj    = Number(byId("objective")?.value) || 0;

  const bmr = 10 * weight + 6.25 * height - 5 * age + (male ? 5 : -161);
  const tdee = bmr * act;
  const target = Math.round((tdee + obj) / 10) * 10;

  const out = byId("kcal_target");
  if (out) out.value = Math.min(Math.max(target, 800), 6000);
}

document.getElementById("auto_kcal_btn")
  .addEventListener("click", estimateKcal);