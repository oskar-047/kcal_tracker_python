const proteinPercent = document.getElementById("protein_percent");
const carbsPercent = document.getElementById("carbs_percent");
const fatsPercent = document.getElementById("fats_percent");

const form = document.getElementById("user-data-form");

form.addEventListener("submit", (e) => {

    const p = parseFloat(proteinPercent.value);
    const c = parseFloat(carbsPercent.value);
    const f = parseFloat(fatsPercent.value);

    let total = p + c + f;

    if(total != 100){
        let ok = window.confirm(`Macros add to ${total}%. Continue anyway?`);

        if(!ok){
            e.preventDefault();
        }
    }
})