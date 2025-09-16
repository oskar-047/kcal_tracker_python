fetch("/food/get-pined")
.then(data => data.json())
.then(data => {
    if(!data){
        console.log("no default food");
        return;
    }
    selectFood(data["food_id"], data["name"], "true");
})