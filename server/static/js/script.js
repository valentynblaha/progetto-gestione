const searchButton = document.getElementById("button-search");
const inputQuery = document.getElementById("input-query");
const divResponse = document.getElementById("div-response");

searchButton.addEventListener("click", e => {
    // Create an XMLHttpRequest object
    const xhttp = new XMLHttpRequest();

    // Define a callback function
    xhttp.onload = function () {
        let ids = JSON.parse(xhttp.responseText)
        let responseText = "";
        for (const id of ids) {
            responseText += `<p>${id}</p>`;
        }
        divResponse.innerHTML = responseText;
    };

    // Send a request
    console.log(inputQuery.value)
    xhttp.open("GET", `search?q=${inputQuery.value}`, true);
    xhttp.send();
});
