const searchBar = document.getElementById("search-query");
const resultsSection = document.getElementById("results-section");

searchBar.addEventListener("input", e => {
  search();
})

function createResults(foods) {
  // console.log(foods);

  // split cuts the string on "T" and returns an array with 2 values, before and after the cut
  t_dt = new Date().toISOString().split("T")[0];

  resultsSection.innerHTML = "";

  if (foods && foods.length > 0) {
    foods.forEach(food => {
      let favorite = food.favorite == 1 ? "favorite" : "";
      const block = `
      <div class="food-cont">
        <div class="food-cont-card">
          <h2 class="food-title">${food.name}</h2>
          <h3 class="food-kcal">${window.t("add-meal.table.kcal")}: ${food.kcal}</h3>
          <div class="food-macros">
            <p class="food-macros">${window.t("add-meal.table.protein")}: ${food.protein}</p>
            <p class="food-macros">${window.t("add-meal.table.carbs")}: ${food.carbs}</p>
            <p class="food-macros">${window.t("add-meal.table.fats")}: ${food.fats}</p>
          </div>
          <div data-food-id="${food.id}" class="star ${favorite}" title="favorite"></div>
        </div>

        <div class="food-track">
          <input class="gen-input q-input" type="number" step="0" value="0" placeholder="${window.t("add-meal.input.quantity")}">
          <input class="gen-input dt-input" type="date" value="${t_dt}">
          <button data-food-name="${food.name}" data-food-id="${food.id}" type="submit" class="track-btn btn">${window.t("add-meal.action.track")}</button>
        </div>
      </div>
    `;
      resultsSection.insertAdjacentHTML("beforeend", block);
    });
  } else {
    resultsSection.innerHTML = `<p class="empty">${window.t("add-meal.results.empty")}</p>`;
  }
}


function search() {
  query = searchBar.value;
  // encodeURIComponent converts the string to a safe url string
  fetch(`/meals/track/search?query=${encodeURIComponent(query)}`, {})
    .then(data => data.json())
    .then(data => createResults(data));
}

search();