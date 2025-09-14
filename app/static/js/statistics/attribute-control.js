const cont = document.getElementById("attribute-select-cont");

cont.addEventListener("click", e => {
    const i = e.target.closest('.attribute');

    // const is_selected = i.classList.contains("attribute-selected");
    if(i){
        // Check if selected attribute clicked
        if(i.classList.contains("attribute-selected")){
            i.classList.remove("attribute-selected");
            cont.dataset.selected = "none";
            updateCharts();
            return;
        }

        // If not deselect all and select the new one
        cont.querySelectorAll('.attribute').forEach(item => {
            item.classList.remove("attribute-selected");
        })
        i.classList.add("attribute-selected");
        cont.dataset.selected = i.dataset.name;

        updateCharts();
    }
});