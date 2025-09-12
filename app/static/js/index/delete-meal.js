const mealsContainer = document.getElementById("day-list-cont");

if(mealsContainer){
    mealsContainer.addEventListener("click", async (e) => {
        if(e.target.closest(".bin-btn")){
            const conf = confirm("You sure you want to delete this meal track???");
            if(!conf){ return }

            const item = e.target.closest(".bin-btn");
            const mealId = item.dataset.id;

            fetch(`/meals/live-delete-meal?meal_id=${Number(mealId)}`,
                {
                method: "POST",
                headers: { "Content-type": "application/json" },
            })
            .then(data => data.json())
            .then(data => {
                if(data.status == "ok"){
                    console.log("OKAY");
                    document.getElementById(`meal-item-${mealId}`).remove();
                } else{
                    console.log("NOT OKAY");
                    return;
                }
            })         

        }
    })
}