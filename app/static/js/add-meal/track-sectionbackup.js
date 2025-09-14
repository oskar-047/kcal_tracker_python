const cont = document.getElementById("results-section");
let canClose = true;

cont.addEventListener("click", (e) => {
  // if (e.target.closest(".food-cont-card")) {
  //   // When a food item is clicked
  //   const food = e.target.closest(".food-cont"); // gets the food item
  //   const card = e.target.closest(".food-cont-card");

  // const its_selected = getComputedStyle(food.querySelector(".food-track")).display === "flex";

  //   // Display none on all items track section
  //   food.parentElement.querySelectorAll(".food-track").forEach((el) => {
  //     if (getComputedStyle(el).display === "flex" && canClose) {
  //       console.log("STARTS CLOSING");
  //       el.classList.remove("food-track-anim");
  //       // el.classList.add("disappear-anim");
  //       // canClose = false;
  //       el.addEventListener("transitionend", () => {
  //         el.style.display = "none";
  //         console.log("closed");
  //       }, {"once": true})
  //       // setTimeout(() => {
  //       //   el.style.display = "none";
  //       //   canClose = true;
  //       // }, 1000);
  //     }
  //   });

  //   // Show track section of current clicked element
  //   if (!its_selected) {
  //     const trackSect = food.querySelector(".food-track");
  //     trackSect.style.display = "flex";
  //     void trackSect.offsetHeight; // Because display flex and the anim are on same "frame" and with void it enforces to recalculate the height again
  //     trackSect.classList.add("food-track-anim");
  //     // trackSect.classList.remove("disappear-anim");
  //   }
  // }




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
        // Helper function
        showPopup(`The food ${foodName} was tracked with ${q}g.`);
      } else{
        showPopup("The food failed to track");
        // alert("NOT OKAY");
      }
    })
  }
})
