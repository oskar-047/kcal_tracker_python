const kcalChartCont = document.getElementById("donut-chart-kcal").querySelector("canvas");
const proteinChartCont = document.getElementById("donut-chart-protein").querySelector("canvas");
const carbsChartCont = document.getElementById("donut-chart-carbs").querySelector("canvas");
const fatsChartCont = document.getElementById("donut-chart-fats").querySelector("canvas");

// today data
const t_data = window.today;

// console.log(t_data);

kcalColor = {
  "text": ["#ffffff", "#cccccc"],
  "main_donut": ["#3B82F6", "#D0D4DA"],   // azul kcal
  "outer_ring": ["#EF4444", "#00000000"]  // extra en rojo
}

proteinColor = {
  "text": ["#ffffff", "#cccccc"],
  "main_donut": ["#22C55E", "#D0D4DA"],   // verde proteína
  "outer_ring": ["#EF4444", "#00000000"]
}

carbsColor = {
  "text": ["#ffffff", "#cccccc"],
  "main_donut": ["#F59E0B", "#D0D4DA"],   // amarillo carbohidratos
  "outer_ring": ["#EF4444", "#00000000"]
}

fatsColor = {
  "text": ["#ffffff", "#cccccc"],
  "main_donut": ["#A855F7", "#D0D4DA"],   // púrpura grasas
  "outer_ring": ["#EF4444", "#00000000"]
}


const optionsKcal = build_donut(t_data["kcal"], kcalColor, "kcal");
const optionsProtein = build_donut(t_data["protein"], proteinColor, "protein");
const optionsCarbs = build_donut(t_data["carbs"], carbsColor, "carbs");
const optionsFats = build_donut(t_data["fats"], fatsColor, "fats");

const kcalChart = new Chart(kcalChartCont, optionsKcal);
const proteinChart = new Chart(proteinChartCont, optionsProtein);
const carbsChart = new Chart(carbsChartCont, optionsCarbs);
const fatsChart = new Chart(fatsChartCont, optionsFats);

function build_donut(data, colorData, valueName) {
    const text = {
        id: valueName + "Text",
        beforeDraw(chart, args, options) {

            // SAME AS:
            // const ctx = chart.ctx;
            // const width = chart.chartArea.width;
            // const height = chart.chartArea.height;
            const { ctx, chartArea: { width, height } } = chart;

            // ctx.save() and restore() is for using custom parameters for text without breaking the actual graph
            ctx.save();

            const textUp = `${Math.round((data["value"] + data["e_value"]) * 10) / 10}`;
            const textDown = `/${Math.round(data["objective"] * 10) / 10}`;

            // Font size relative to chart size
            const fontSize = Math.min(width, height) / 7;
            
            const lineHeight = fontSize * 1.3
            
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            
            
            ctx.fillStyle = colorData["text"][0];
            ctx.font = `bold ${fontSize}px sans-serif`;
            ctx.fillText(textUp, width / 2, height / 2 - fontSize/2);

            ctx.fillStyle = colorData["text"][1];
            ctx.font = `${fontSize}px sans-serif`;
            ctx.fillText(textDown, width / 2, height / 2 + fontSize/2);

            ctx.restore();

        }
    };

    const chartData = {
        labels: [`Today ${valueName}`, `Remaining ${valueName}`],
        datasets: [
            // Main donut
            {
                data: [data["value"], data["r_value"]],
                backgroundColor: colorData["main_donut"],
                borderWidth: 0,
                radius: "85%"
            },

            // Outer ring
            {
                data: [data["e_value"], data["e_r_value"]],
                backgroundColor: colorData["outer_ring"],
                borderWidth: 0,
                radius: "100%",
                cutout: "85%",
                label: `Extra ${valueName}`
            }
        ]
    }
    const options = {
        type: "doughnut",
        data: chartData,
        options: {
            // cutout: "60%",
            // responsive: true,
            // maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                // tooltip: { enabled: true }
            }
        },
        plugins: [text]
    }

    return options
}