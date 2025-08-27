function checkDelete(e, item, toDelete) {
    itemName = item.dataset.name;
    confirmation = confirm(`Are you sure you want to delete the ${toDelete} ${itemName}?`)

    if (confirmation) {
        console.log("fine");
    } else {
        e.preventDefault();
    }
}