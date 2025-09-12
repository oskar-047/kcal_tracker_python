const body = document.body;

function showPopup(text){
    const cont = document.createElement("div");
    cont.classList.add("popup-cont");
    const time = 3.4;

    cont.textContent = text;

    body.append(cont);

    setTimeout(() => {
        cont.remove();
    }, time*1000);
}