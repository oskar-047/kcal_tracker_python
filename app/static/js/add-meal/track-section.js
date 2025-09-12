const cont = document.getElementById("results-section");

cont.addEventListener("click", (e) => {
    // Show track section
    if(e.target.closest(".food-cont-card")){ // When a food item is clicked
        const food = e.target.closest(".food-cont"); // gets the food item
        const card = e.target.closest(".food-cont-card");

        const its_selected = getComputedStyle(food.querySelector(".food-track")).display == "flex" ? true : false

        // Display none on all items track section
        food.parentElement.querySelectorAll(".food-track").forEach(e => {
            if(getComputedStyle(e).display == "flex"){
                console.log("WORKS");
                e.classList.remove("appear-anim");
                e.classList.add("disappear-anim");
                setTimeout(() => {
                    e.style.display = "none";
                }, 700);
            }
        });
        // Show track section of current clicked element
        if(!its_selected){
            const trackSect = food.querySelector(".food-track")
            trackSect.style.display = "flex";
            trackSect.classList.add("appear-anim");
            trackSect.classList.remove("disappear-anim");
        }
    }

    // Track food
    if(e.target.closest(".track-btn")){
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
            if(status["status"] == "ok"){
                // alert("OK");
                // Helper function
                showPopup(`The food ${foodName} was tracked with ${q}g.`);
            } else{
                showPopup("The food failed to track");
                // alert("NOT OKAY");
            }
        })
    }
})

// let popup, foodIdInput, invisibleBg, quantityInput

// document.addEventListener("DOMContentLoaded", () => {
//     popup = document.getElementById("track-meal-dialog");
//     foodIdInput = document.getElementById("food_id");
//     quantityInput = document.getElementById("quantity");
//     invisibleBg = document.getElementById("invisible-bg");

//     document.querySelectorAll(".btn-track").forEach(btn => {
//         btn.addEventListener("click", (e) => {
//             foodIdInput.value = e.target.dataset.foodId;

            
//             popup.style.display = "block";
//             invisibleBg.style.display = "block";
            
//             quantityInput.focus();
//         })
//     });
// })


// function occultTrackDialog(){
//     popup.style.display = "none";
//     invisibleBg.style.display = "none";
// }