const searchedFoodsEl = document.getElementById("searched-foods");
const selectedFoodsEl = document.getElementById("selected-foods");
const searchBar = document.getElementById("search-bar");
let canCall = true;

// Detect input change
searchBar.addEventListener("input", () => {

    if (canCall) {
        canCall = false;
        setTimeout(() => {
            searchFoods(searchBar.value);
            canCall = true;
        }, 1);
    } else {
        console.log("WAIT");
    }
})

// Detect when clickin the X to delete a food of the food list
selectedFoodsEl.addEventListener("click", (e) => {
    const item = e.target.closest(".delete-food-button");

    if (item) {
        const foodIdToDelete = Number(item.parentElement.dataset.foodId);
        item.parentElement.remove();

        window.SelectedFoods.removeFood(foodIdToDelete);

        updateCharts();

        console.log(window.SelectedFoods.getSelectedFoods());
    }
})

// Detect when clicking the select
searchedFoodsEl.addEventListener("click", (e) => {
    const item = e.target.closest(".select-food-button");

    if (item) {
        foodId = Number(item.dataset.foodId);
        foodName = item.dataset.foodName;
        // console.log(foodId);

        if (!window.SelectedFoods.getSelectedFoods().includes(Number(foodId))) {
            const selectedFoodItem = document.createElement("div");
            selectedFoodItem.classList.add("selected-food-item")
            selectedFoodItem.dataset.foodId = foodId;

            const title = document.createElement("h3");
            title.textContent = foodName;

            const deleteImg = document.createElement("div");
            deleteImg.classList.add("delete-food-button");
            deleteImg.textContent = "X";

            selectedFoodItem.appendChild(title);
            selectedFoodItem.appendChild(deleteImg);

            selectedFoodsEl.appendChild(selectedFoodItem);
            // selectedFoods.push(foodId);
            window.SelectedFoods.addSelectedFood(foodId)

            updateCharts();

            console.log(window.SelectedFoods.getSelectedFoods());
        } else{
            alert("Food already selected");
        }

    }
})


async function searchFoods(query) {
    response = await fetch(`/fuzzy/food-search?q=${query}&max=5`);
    foodData = await response.json();

    // Reset searched-foods items
    searchedFoodsEl.innerHTML = "";

    // Create fragment
    const fragment = document.createDocumentFragment();

    // Iterate over food data
    if (foodData) {
        for (let i = 0; i < foodData.length; i++) {
            const searchItem = document.createElement("div");
            searchItem.classList.add("search-item");

            const searchItemTitle = document.createElement("h3");
            searchItemTitle.textContent = foodData[i].name;

            const searchItemSelectButton = document.createElement("div");
            searchItemSelectButton.classList.add("select-food-button");
            searchItemSelectButton.textContent = "SELECT";
            searchItemSelectButton.dataset.foodId = foodData[i].food_id;
            searchItemSelectButton.dataset.foodName = foodData[i].name;

            searchItem.appendChild(searchItemTitle);
            searchItem.appendChild(searchItemSelectButton);
            fragment.appendChild(searchItem);
        }
    }

    searchedFoodsEl.appendChild(fragment);

}


