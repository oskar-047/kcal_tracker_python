const foodChartSelectCont = document.getElementById("foods-chart-selecter");

foodChartSelectCont.addEventListener("click", i => {
    let item = i.target.closest('.pin-wrapper');
    if(!item){ return }
    let overlay = item.querySelector("div");
    // alert(item);
    if (overlay) {
        // if(overlay.classList.contains("pinned")){
        //     overlay.classList.remove("pinned");
        //     return;
        // }

        let foodId = item.parentElement.dataset.foodId;
        console.log(foodId);

        i.target.closest("#selected-foods").querySelectorAll(".pin-overlay").forEach(i => {
            i.classList.remove("pinned");
        })

        fetch("/food/pin-food", {
            method: "POST",
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify({
                food_id: foodId
            })
        })
        .then(data => data.json())
        .then(data => {
            if(data["status"] == "ok"){
                pinItem(overlay, foodId);
            } else{
                console.log("error");
            }
        })

    }
})

function pinItem(item, foodId){
    // Pins the item
    item.classList.add("pinned");
    
    // Check if pinned food is actually on searched foods
    document.getElementById("searched-foods").querySelectorAll(".search-item").forEach(i => {
        // Make pinned dataset false if it have
        i.dataset.pinned = "false";

        // If actual item its same foodId as the new pinned element, change its pinned dataset to true
        if(i.dataset.foodId == foodId){
            i.dataset.pinned = "true";
        }
    })
}