const searchButton = document.getElementById("button-search");
const inputQuery = document.getElementById("input-query");
const divResponse = document.getElementById("div-response");

function parseVideoToHtml(video) {
    video_obj = JSON.parse(video);
    return video_obj["video"]["title"];
}

function loadVideo(id) {
    return new Promise(function (resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open("GET", `static/data/${id}.json`);
        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve(xhr.responseText);
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText,
                });
            }
        };
        xhr.onerror = function () {
            reject({
                status: this.status,
                statusText: xhr.statusText,
            });
        };
        xhr.send();
    });
}

searchButton.addEventListener("click", e => {
    const xhttp = new XMLHttpRequest();

    xhttp.onload = async function () {
        let ids = JSON.parse(xhttp.responseText);
        let responseText = "";
        for (const id of ids) {
            responseText += `<p>${parseVideoToHtml(await loadVideo(id))}</p>`;
        }
        divResponse.innerHTML = responseText;
    };

    console.log(inputQuery.value);
    xhttp.open("GET", `search?q=${inputQuery.value}`, true);
    xhttp.send();
});

inputQuery.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        searchButton.click();
    }
});
