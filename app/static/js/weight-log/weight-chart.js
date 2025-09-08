const mainCanvas = document.getElementById("weight-chart").querySelector("canvas");
const daysSelect = document.getElementById("days-select");
const daysInput = document.getElementById("days-input");
const chartSelect = document.getElementById("chart-select");
const timeGroupingSelect = document.getElementById("time-grouping-select");
const showKcalCheck = document.getElementById("weight-chart-show-kcal");
let chart;

daysSelect.addEventListener("change", e => {
    daysInput.value = e.target.value;
    updateChart();
});

chartSelect.addEventListener("change", updateChart);
timeGroupingSelect.addEventListener("change", updateChart);

daysInput.addEventListener("input", updateChart);

showKcalCheck.addEventListener("change", updateChart);

async function updateChart() {

    if (!chart) {
        return
    }

    let days = daysInput.value;
    if(days > 15000){
        days = 15000;
    }

    if (!days) {
        days = 0;
    }
    let timeGrouping = timeGroupingSelect.value;

    console.log(days + "" + timeGrouping);

    const labelsResponse = await fetch('/statistics/update-labels', {
        method:"POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
            days: days,
            time_grouping: timeGrouping
        })
    });

    window.labels = await labelsResponse.json();
    chart.data.labels = window.labels;

    let chartName = chartSelect.value;

    let weightShowKcal = showKcalCheck.checked;
    let foodsSelectedFoods = [1]
    let goalsShowMacros = [false, false, false]

    

    const dataResponse = await fetch(`/statistics/show-chart`, {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
            chart_name: chartName,
            weight_show_kcal: weightShowKcal,
            foods_selected_foods: foodsSelectedFoods,
            goals_show_macros: goalsShowMacros
        })
    });

    const { data, options } = await dataResponse.json();

    chart.options = options;
    chart.data = data;
    chart.update();


}

chart = new Chart(mainCanvas, {
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

updateChart(7, "weight");