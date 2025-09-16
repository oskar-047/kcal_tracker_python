document.addEventListener("click", item => {
    let star = item.target.closest(".star")
    if(star){
        let id = star.dataset.foodId;
        fetch("/food/toggle-favorite", {
            method: "PUT",
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify({
                f_id: id
            })
        })
        .then(d => d.json())
        .then(d => {
            console.log(d);
            if(d){
                star.classList.add("favorite");
            } else{
                star.classList.remove("favorite");
            }
            search();
        })

    }
})