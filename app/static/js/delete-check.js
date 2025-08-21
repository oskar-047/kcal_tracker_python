document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".btn-delete").forEach(btn => {
        btn.addEventListener("click", e => {
            foodName = btn.dataset.name;
            confirmation = confirm(`Are you sure you want to delete the food ${foodName}?`)

            if(confirmation){
                console.log("fine");
            } else{
                e.preventDefault();
            }
        })
    })
})