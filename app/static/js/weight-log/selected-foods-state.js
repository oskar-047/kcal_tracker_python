const selectedFoods = [];

window.SelectedFoods = {
    getSelectedFoods: () => [...selectedFoods],
    addSelectedFood: (n) => {
        const id = Number(n);
        if(!Number.isInteger(id)){ return }
        selectedFoods.push(id);
    },
    removeFood: (n) => {
        const id = Number(n);
        if(!Number.isInteger(id)){ return }
        for (let i = selectedFoods.length - 1; i >= 0; i--) {
            if (selectedFoods[i] === id) {
                selectedFoods.splice(i, 1);
            }
        }
    }
};