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

function getResultsTree(results) {

    /**
     * @type {Map<string, Array<string>}
     */
    const videos = new Map();

    for (const result of results) {
        if (result['kind'] === 'video') {
            const id = result['id'];
            videos.set(id, []);
        } else if (result['kind'] === 'comment') {
            const video_id = result['videoId'];
            if (!videos.has(video_id)) {
                videos.set(video_id, []);
            }
            videos.get(video_id).push(result['id']);
        }
    }

    return videos;
}

searchButton.addEventListener("click", e => {
    const xhttp = new XMLHttpRequest();

    xhttp.onload = async function () {
        let results = JSON.parse(xhttp.responseText);
        console.log(results.length);
        const resultsTree = getResultsTree(results);
        console.log(resultsTree);
        parseResults(resultsTree);
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


/**
 * @param {String} HTML representing a single element
 * @return {Element}
 */
function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}

/**
 * 
 * @param {Map<string, string[]>} resultsTree 
 * @param {Map<string, Object} videos
 */
async function parseResults(resultsTree) {
    
    function videoHtml(params) {
        return `
        <div>
            <h4>${params.title}</h4>
            <div>${params.description}</div>
            <div>${params.likes}</div>
        </div>
        `
    }

    function commentHtml(params) {
        return `
        <div>
            <h5>${params.author}</h5>
            <div>${params.text}</div>
            <div>${params.likes}</div>
        </div>
        `
    }

    for (const videoId of resultsTree.keys()) {
        const commentsIds = resultsTree.get(videoId);
        const video = JSON.parse(await loadVideo(videoId));

        const foundComments = new Map();
        divResponse.appendChild(htmlToElement(videoHtml(video.video)));
    }
}