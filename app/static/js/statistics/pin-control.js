const foodChartSelectCont = document.getElementById("foods-chart-selecter");

foodChartSelectCont.addEventListener("click", i => {
    let item = i.target.closest('.pin-wrapper');
    // alert(item);
    if (item) {
        item.querySelector("div").classList.toggle("pinned");
    }
})