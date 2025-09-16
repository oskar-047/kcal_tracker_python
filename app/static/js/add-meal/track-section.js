const cont = document.getElementById("results-section");
let canClose = true;

cont.addEventListener("click", (e) => {

    if (e.target.closest(".food-cont-card")) {
        // Check if the clicked element is the favorite div
        if(e.target.closest(".star")){return}

        foodTrack = e.target.closest(".food-cont").querySelector(".food-track"); 
        if(foodTrack.classList.contains("food-track-anim")){
            foodTrack.classList.remove("food-track-anim");
            return
        }
        // If some track section is displayed it will remove the class to occult them
        cont.querySelectorAll(".food-track").forEach(item => {
            if(item.classList.contains("food-track-anim")){
                item.classList.remove("food-track-anim");
            }
        });

        foodTrack.classList.toggle("food-track-anim");
    }


    // Track food
    if (e.target.closest(".track-btn")) {
        const item = e.target.closest(".track-btn");

        const foodId = item.dataset.foodId;
        const foodName = item.dataset.foodName;

        const q = item.parentElement.querySelector(".q-input").value;
        const date = item.parentElement.querySelector(".dt-input").value;

        fetch("/meals/track/track-meal", {
            method: "POST",
            headers: { "Content-type": "application/json" },
            body: JSON.stringify({
                food_id: foodId,
                quantity: q,
                dt: date
            })
        })
            .then(data => data.json())
            .then(status => {
                if (status["status"] == "ok") {
                    // Helper function
                    showPopup(`The food ${foodName} was tracked with ${q}g.`);
                } else {
                    showPopup("The food failed to track");
                    // alert("NOT OKAY");
                }
            })
    }
})
