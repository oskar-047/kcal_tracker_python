const mainCanvas = document.getElementById("weight-chart").querySelector("canvas");
const proteinCanvas = document.getElementById("protein-chart").querySelector("canvas");
const carbsCanvas = document.getElementById("carbs-chart").querySelector("canvas");
const fatsCanvas = document.getElementById("fats-chart").querySelector("canvas");
const daysSelect = document.getElementById("days-select");
const daysInput = document.getElementById("days-input");
const chartSelect = document.getElementById("chart-select");
const timeGroupingSelect = document.getElementById("time-grouping-select");
const showKcalCheck = document.getElementById("weight-chart-show-kcal");
const modeSelect = document.getElementById("display-mode");
const foodChartSelCont = document.getElementById("foods-chart-selecter");

// INIT CHARTS
let mainChart = initChart(mainCanvas);
let proteinChart = initChart(proteinCanvas);
let carbsChart = initChart(carbsCanvas);
let fatsChart = initChart(fatsCanvas);

// Containers
const foodItems = [foodChartSelCont, proteinCanvas, carbsCanvas, fatsCanvas];
const chartItems = [mainChart, proteinChart, carbsChart, fatsChart];



daysSelect.addEventListener("change", e => {
    daysInput.value = e.target.value;
    updateCharts();
});

chartSelect.addEventListener("change", updateCharts);
timeGroupingSelect.addEventListener("change", updateCharts);
modeSelect.addEventListener("change", updateCharts);


daysInput.addEventListener("input", updateCharts);

showKcalCheck.addEventListener("change", updateCharts);


async function updateCharts(){
    if(chartSelect.value == "weight"){

        foodItems.forEach(i => {
            i.style.display = "none";
        })

        await updateChart(mainChart);
    } else if(chartSelect.value == "foods"){
        foodItems.forEach(i => {
            i.style.display = "grid";
        })
        await updateChart(mainChart);
        await updateChart(proteinChart, "protein");
        await updateChart(carbsChart, "carbs");
        await updateChart(fatsChart, "fats");

    }
}

async function updateChart(chart, displayMode = "default") {

    if (!chart) {
        return
    }

    const selectedFoods = window.SelectedFoods.getSelectedFoods();
    // Checks it is a correct int array or simply an array
    const safeSelectedFoods = Array.isArray(selectedFoods)
        ? selectedFoods.map(Number).filter(Number.isInteger)
        : [];

    let days = daysInput.value;
    if (days > 15000) {
        days = 15000;
    }

    if (!days) {
        days = 0;
    }
    let timeGrouping = timeGroupingSelect.value;

    console.log(days + "" + timeGrouping);

    const labelsResponse = await fetch('/statistics/update-labels', {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
            days: days,
            time_grouping: timeGrouping
        })
    });

    window.labels = await labelsResponse.json();
    chart.data.labels = window.labels;

    let chartName = chartSelect.value;

    let finalDisplayMode;
    if(displayMode === "default"){
        finalDisplayMode = modeSelect.value;
    } else{
        finalDisplayMode = displayMode
    }

    let weightShowKcal = showKcalCheck.checked;
    let goalsShowMacros = [false, false, false]



    const dataResponse = await fetch(`/statistics/show-chart`, {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
            chart_name: chartName,
            weight_show_kcal: weightShowKcal,
            foods_selected_foods: safeSelectedFoods,
            foods_display_mode: finalDisplayMode,
            goals_show_macros: goalsShowMacros
        })
    });

    const { data, options } = await dataResponse.json();

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

updateCharts(mainChart);