// let createFoodForm = document.getElementById("create-food-form")

// createFoodForm.addEventListener("submit", async (e) => {

//     e.preventDefault();

//     const data = {
//         "name": createFoodForm.name.value,
//         "kcal": createFoodForm.kcal.value,
//         "protein": createFoodForm.protein.value,
//         "carbs": createFoodForm.carbs.value,
//         "fats": createFoodForm.fats.value,
//     };

//     const response = await fetch("/actions/create-food", {
//         method: "POST",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify(data)
//     });

//     if (response.ok) {
//         const html = await response.text();

//         document.open();
//         document.write(html);
//         document.close();
//     }

// })