document.addEventListener("change", e => {
  if (e.target.matches("input[type=color]")) {
    const foodId = e.target.dataset.foodId;
    const value = e.target.value;
    console.log("Food id: ", foodId, "Color:", value);

    fetch(`/food/edit-color?color=${encodeURIComponent(value)}&food_id=${encodeURIComponent(foodId)}`)
    .then(data => data.json())
    .then(data => {
        if(data["status"] == "ok"){
            // alert("OK");
        } else{
            // alert("ERROR");
        }
    })
  }
});