// === JS ===
const searchedFoodsEl = document.getElementById("searched-foods");
const selectedFoodsEl = document.getElementById("selected-foods");
const searchBar = document.getElementById("search-bar");
let canCall = true;

// Input debounce-lite
searchBar.addEventListener("input", () => {
  if (canCall) {
    canCall = false;
    setTimeout(() => {
      searchFoods(searchBar.value);
    }, 1);
  }
});

// Delete from selected
selectedFoodsEl.addEventListener("click", (e) => {
  const item = e.target.closest(".delete-food-button");
  if (item) {
    const foodIdToDelete = Number(item.parentElement.dataset.foodId);
    item.parentElement.remove();
    window.SelectedFoods.removeFood(foodIdToDelete);
    updateCharts();
  }
});

// Select from search by clicking the whole item
searchedFoodsEl.addEventListener("click", (e) => {
  // ignore clicks on pin
  if (e.target.closest(".pin-wrapper")) return;

  const item = e.target.closest(".search-item");
  if (item) {
    const foodId = Number(item.dataset.foodId);
    const foodName = item.dataset.foodName;
    const isPinned = item.dataset.pinned === "true";

    // If the clicked food is not already selected
    selectFood(foodId, foodName, isPinned);
  }
});

function selectFood(foodId, foodName, isPinned){
  if (!window.SelectedFoods.getSelectedFoods().includes(foodId)) {
      const selectedFoodItem = document.createElement("div");
      selectedFoodItem.classList.add("selected-food-item");
      selectedFoodItem.dataset.foodId = foodId;

      selectedFoodItem.innerHTML = `
        <h3></h3>
        <div class="pin-wrapper">
          <img src="/static/img/pin.svg" class="pin-food-icon">
          <div class="pin-overlay"></div>
        </div>
        <div class="delete-food-button">X</div>
      `;

      selectedFoodItem.querySelector("h3").textContent = foodName;
      const overlayEl = selectedFoodItem.querySelector(".pin-overlay");
      if (isPinned) overlayEl.classList.add("pinned");

      selectedFoodsEl.appendChild(selectedFoodItem);
      window.SelectedFoods.addSelectedFood(foodId);
      updateCharts();
    } else {
      alert("Food already selected");
    }
}


// ========= SEARCH FOOD LOGIC =========
async function searchFoods(query) {
  const response = await fetch(`/fuzzy/food-search?q=${encodeURIComponent(query)}&max=5`);
  const foodData = await response.json();

  searchedFoodsEl.innerHTML = "";
  const fragment = document.createDocumentFragment();

  if (foodData) {
    for (let i = 0; i < foodData.length; i++) {
      const d = foodData[i];
      const searchItem = document.createElement("div");
      searchItem.classList.add("search-item");
      searchItem.dataset.foodId = d.id;
      searchItem.dataset.foodName = d.name;
      searchItem.dataset.pinned = d.is_default === true ? "true" : "false";

      // searchItem.innerHTML = `
      //   <h3></h3>
      //   <div class="pin-wrapper">
      //     <img src="/static/img/pin.svg" class="pin-food-icon">
      //     <div class="pin-overlay${d.is_default ? " pinned" : ""}"></div>
      //   </div>
      // `;
      searchItem.innerHTML = `
        <h3></h3>
      `;

      searchItem.querySelector("h3").textContent = d.name;
      fragment.appendChild(searchItem);
    }
  }

  searchedFoodsEl.appendChild(fragment);
  canCall = true;
}
