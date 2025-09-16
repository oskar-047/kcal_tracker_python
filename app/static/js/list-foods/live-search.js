const searchBar = document.getElementById("search-query");
const listed = document.getElementById("listed-items");

function renderFoods(foods){
  listed.innerHTML = "";
  if (foods && foods.length){
    foods.forEach(food => {
      let favorite = food.favorite == 1 ? "favorite" : "";
      const block = `
        <div class="food-cont-card">
          <h2 class="food-title">${food.name}</h2>
          <h3 class="food-kcal">${window.t("add-meal.table.kcal")}: ${food.kcal}</h3>
          <div class="food-macros">
            <p>${window.t("add-meal.table.protein")}: ${food.protein}</p>
            <p>${window.t("add-meal.table.carbs")}: ${food.carbs}</p>
            <p>${window.t("add-meal.table.fats")}: ${food.fats}</p>
          </div>

          <!-- FAVORITE -->
          <div data-food-id="${food.id}" class="star ${favorite}" title="favorite"></div>

          <!-- EDIT -->
          <form method="get" action="/food/edit-food">
            <input type="hidden" name="food_id" value="${food.id}">
            <button type="submit" class="edit" title="edit"></button>
          </form>

          <!-- DELETE -->
          <form method="post" action="/food/delete-food">
            <input type="hidden" name="food_id" value="${food.id}">
            <button type="submit" class="bin" title="delete"
              data-name="${food.name}" onclick="checkDelete(event, this, 'food')"></button>
          </form>
          <input class="color" data-food-id="${food.id}" value="${food.color}" type="color">
        </div>`;
      listed.insertAdjacentHTML("beforeend", block);
    });
  } else {
    listed.innerHTML = `<p class="empty">${window.t("add-meal.results.empty")}</p>`;
  }
}

searchBar.addEventListener("input", () => {
  search();
});

function search(){
  const query = searchBar.value;
  fetch(`/meals/track/search?query=${encodeURIComponent(query)}`)
    .then(r => r.json())
    .then(renderFoods)
    .catch(() => { listed.innerHTML = `<p class="empty">${window.t("add-meal.results.empty")}</p>`; });
}

search();