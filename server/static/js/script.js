const searchButton = document.getElementById("button-search");
const inputQuery = document.getElementById("input-query");
const divResponse = document.getElementById("div-response");

inputQuery.value = localStorage.getItem("query");

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

    localStorage.setItem("query", inputQuery.value);
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
            <h5>${params.title}</h5>
            <div>${params.description}</div>
            <div><img src="static/media/hand-thumbs-up-fill.svg"><span>${params.likes}</span></div>
        </div>
        `
    }

    function commentHtml(params) {
        return `
        <div class="ms-5">
            <h6>${params.author}</h6>
            <div>${params.text}</div>
            <div><img src="static/media/hand-thumbs-up-fill.svg"><span>${params.likes}</span></div>
        </div>
        `
    }

    divResponse.innerHTML = "";
    for (const videoId of resultsTree.keys()) {
        const commentsIds = resultsTree.get(videoId);
        const video = JSON.parse(await loadVideo(videoId));

        const foundComments = new Map();
        divResponse.appendChild(htmlToElement(videoHtml(video.video)));
        for (const commentId of commentsIds) {
            const comment = video.comments.find(el => el['topLevelComment']['id'] === commentId);
            divResponse.appendChild(htmlToElement(commentHtml(comment['topLevelComment'])));
        }
    }
}