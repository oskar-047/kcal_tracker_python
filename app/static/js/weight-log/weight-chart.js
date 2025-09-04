const mainCanvas = document.getElementById("weight-chart").querySelector("canvas");
const daysSelect = document.getElementById("days-select");
const daysInput = document.getElementById("days-input");
const chartSelect = document.getElementById("chart-select");
const showKcalCheck = document.getElementById("weight-chart-show-kcal");
let chart;

daysSelect.addEventListener("change", e => {
    daysInput.value = e.target.value;
    updateChart();
});

chartSelect.addEventListener("change", updateChart);

daysInput.addEventListener("input", updateChart);

showKcalCheck.addEventListener("change", updateChart);

async function updateChart() {

    if (!chart) {
        return
    }

    let days = daysInput.value;
    if(days > 150000){
        days = 150000;
    }
    let chartName = chartSelect.value;
    let showKcal = showKcalCheck.checked;

    let weight_show_kcal = showKcal
    let foods_selected_foods = [1]
    let goals_show_macros = [false, false, false]

    if (!days) {
        days = 0;
    }

    const response = await fetch(`/statistics/show-chart`, {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
            days: days,
            chart_name: chartName,
            time_grouping: "weekly",
            weight_show_kcal: weight_show_kcal,
            foods_selected_foods: foods_selected_foods,
            goals_show_macros: goals_show_macros
        })
    });

    const { chartType, data, options } = await response.json();

    chart.type = chartType;
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