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

async function showResults(results) {
    page = []
    for (const result of results) {
        if (result['kind'] === 'video') {
            page.push(await JSON.parse(loadVideo(result['id'])));
        }
    }
}

searchButton.addEventListener("click", e => {
    const xhttp = new XMLHttpRequest();

    xhttp.onload = async function () {
        let results = JSON.parse(xhttp.responseText);
        showResults(results)
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
