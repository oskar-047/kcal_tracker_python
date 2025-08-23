document.addEventListener("DOMContentLoaded", () => {
    const popup = document.getElementById("track-meal-dialog");
    const foodIdInput = document.getElementById("food_id");

    document.querySelectorAll(".btn-track").forEach(btn => {
        btn.addEventListener("click", (e) => {
            foodIdInput.value = e.target.dataset.foodId;

            popup.style.display = "block";
        })
    });
})