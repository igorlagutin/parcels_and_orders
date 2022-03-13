var refreshUrl = window.location.protocol + "//"  + window.location.host + document.getElementById('refreshUrl').textContent;
var npStatus = document.getElementById('npStatus')
var refreshIcon = document.getElementById('refreshIcon')


refreshIcon.addEventListener("click", () => {
    refreshIcon.classList.add("spin");
    RequestApi(refreshUrl, "POST").then((response) =>{
        npStatus.innerHTML =  response.delivery_status + "</br>"  + response.delivery_destination;
    }).then(npStatus.innerHTML =  "Произошла ошибка, попробуйте позже");
    setTimeout(() => {  refreshIcon.classList.remove("spin"); }, 1000);


 }, false);


