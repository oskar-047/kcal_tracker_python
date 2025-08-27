let popup, foodIdInput, invisibleBg, quantityInput

document.addEventListener("DOMContentLoaded", () => {
    popup = document.getElementById("track-meal-dialog");
    foodIdInput = document.getElementById("food_id");
    quantityInput = document.getElementById("quantity");
    invisibleBg = document.getElementById("invisible-bg");

    document.querySelectorAll(".btn-track").forEach(btn => {
        btn.addEventListener("click", (e) => {
            foodIdInput.value = e.target.dataset.foodId;

            
            popup.style.display = "block";
            invisibleBg.style.display = "block";
            
            quantityInput.focus();
        })
    });
})


function occultTrackDialog(){
    popup.style.display = "none";
    invisibleBg.style.display = "none";
}