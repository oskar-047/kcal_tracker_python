const mainCanvas = document.getElementById("weight-chart").querySelector("canvas");
const proteinCanvas = document.getElementById("protein-chart").querySelector("canvas");
const carbsCanvas = document.getElementById("carbs-chart").querySelector("canvas");
const fatsCanvas = document.getElementById("fats-chart").querySelector("canvas");
const daysInput = document.getElementById("custom-days");
const chartSelect = document.getElementById("chart-select");
const timeGroupingSelect = document.getElementById("time-grouping-select");
// const modeSelect = document.getElementById("display-mode");
const foodChartSelCont = document.getElementById("foods-chart-selecter");
const attributeCont = document.getElementById("attribute-select-cont");

let canUpdateCharts = true;

// INIT CHARTS
let mainChart = initChart(mainCanvas);
let proteinChart = initChart(proteinCanvas);
let carbsChart = initChart(carbsCanvas);
let fatsChart = initChart(fatsCanvas);

// Containers
const foodItems = [foodChartSelCont, proteinCanvas, carbsCanvas, fatsCanvas];
const chartItems = [mainChart, proteinChart, carbsChart, fatsChart];



document.getElementById('range-menu').addEventListener("click", e => {
    if(e.target.closest(".dt-select")){
        let days = e.target.closest(".dt-select").dataset.days;
        daysInput.value = days;
        updateCharts(days);
    }
})

chartSelect.addEventListener("change", () => updateCharts());
timeGroupingSelect.addEventListener("change", () => updateCharts());
// modeSelect.addEventListener("change", () => updateCharts());


daysInput.addEventListener("input", () => updateCharts());


async function updateCharts(days = undefined){
    // console.log(canUpdateCharts);
    if(canUpdateCharts){
        canUpdateCharts = false;
        setTimeout(() => {
            canUpdateCharts = true;
        }, 500);
    } else{
        return
    }

    updateUI();

    if(chartSelect.value == "weight"){

        await updateChart(mainChart, "default", days);

    } else if(chartSelect.value == "foods"){

        await updateChart(mainChart, "default", days);
        await updateChart(proteinChart, "protein", days);
        await updateChart(carbsChart, "carbs", days);
        await updateChart(fatsChart, "fats", days);

    }
}

async function updateChart(chart, displayMode = "default", days = undefined) {

    if (!chart) {
        return
    }

    // const start = performance.now(); // === TESTING

    const selectedFoods = window.SelectedFoods.getSelectedFoods();
    // Checks it is a correct int array or simply an array
    const safeSelectedFoods = Array.isArray(selectedFoods)
        ? selectedFoods.map(Number).filter(Number.isInteger)
        : [];

    // DAYS LOGIC
    let fixedDays = 0;
    // console.log(daysInput.value);

    if(days === undefined){
        fixedDays = daysInput.value;
        // console.log("ASAAA");
    } else{
        fixedDays = days;
    }
    if (fixedDays > 10000) {
        fixedDays = 10000;
    }

    fixedDays = Number(fixedDays);

    let timeGrouping = timeGroupingSelect.value;

    // console.log(fixedDays + "" + timeGrouping);

    const labelsResponse = await fetch('/statistics/update-labels', {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
            days: fixedDays,
            time_grouping: timeGrouping
        })
    });
    
    window.labels = await labelsResponse.json();
    chart.data.labels = window.labels;
    
    
    
    let chartName = chartSelect.value;

    // let finalDisplayMode;
    // if(displayMode === "default"){
        // finalDisplayMode = modeSelect.value;
    // } else{
        // finalDisplayMode = displayMode
    // }

    // console.log(attributeCont.dataset.selected);
    let attribute = attributeCont.dataset.selected;

    
    const dataResponse = await fetch(`/statistics/show-chart`, {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
            chart_name: chartName,
            // weight_show_kcal: weightShowKcal,
            foods_selected_foods: safeSelectedFoods,
            attribute: attribute
            // foods_display_mode: finalDisplayMode,
            // goals_show_macros: goalsShowMacros
        })
    });
    
    const { data, options } = await dataResponse.json();
    
    // Round numbers
    options.scales.y1.ticks.callback = v => Number(v).toFixed(1);
    // options.scales.x.ticks.callback = v => Number(v).toFixed(1);
    if(options?.scales?.y2?.ticks){
        options.scales.y2.ticks.callback = v => Number(v).toFixed(1)
    }
    // console.log(chart.options);
    // const end = performance.now(); // === TESTING
    // console.log("Duration:", end - start, "ms"); // === TESTING
    
    chart.options = options;
    chart.data = data;
    
    chart.update();
    
    

}

function initChart(canvas) {
    return new Chart(canvas, {
        type: "line",
        data: {
            labels: [],
            datasets: []
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function updateUI(){
    document.querySelectorAll(".chart-unique").forEach(item => {
        item.classList.add("hidden");
    })
    if(chartSelect.value == "weight"){
        document.querySelectorAll(".chart-weight").forEach(i => {
            i.classList.remove("hidden");
        })
    } else if(chartSelect.value == "foods"){
        document.querySelectorAll(".chart-foods").forEach(i => {
            i.classList.remove("hidden");
        })
    } else if(chartSelect.value == "goals"){
        document.querySelectorAll(".chart-goals").forEach(i => {
            i.classList.remove("hidden");
        })
    }
}

updateCharts();