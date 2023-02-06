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
    const videos = new Map();
    const page = new Map();
    for (const result of results) {
        if (result['kind'] === 'video') {
            const id = result['id']
            const video = JSON.parse(await loadVideo(id))
            videos.set(id, video);
            page.set(id, {title: video['title'], comments: new Map()})
        } else if (result['kind'] === 'comment') {
            if (page.has(result['videoId'])) {
                page.get(result['videoId']).comments.set(result['id'], result['id'])
            }
            // TODO: if page doesn't have video id
        }
    }
    return page;
}

searchButton.addEventListener("click", e => {
    const xhttp = new XMLHttpRequest();

    xhttp.onload = async function () {
        let results = JSON.parse(xhttp.responseText);
        console.log(results.length);
        console.log(await showResults(results));
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
