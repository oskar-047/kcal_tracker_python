document.querySelectorAll(".day-item").forEach(item => {
    item.addEventListener("click", async e => {
        const response = await fetch(`/meals/mark-as-eaten?meal_id=${item.dataset.id}`);
        if (response.ok){
            const data = await response.text();
            item.style.backgroundColor = data;
        }
    })
})