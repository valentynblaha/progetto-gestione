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
    // TODO: refactoring. This sucks
    /**
     * @type {Map<string, Map<string, string[]>>}
     */
    const videos = new Map();
    /**
     * @type {Map<string, Array<number>}
     */
    const sentiments = new Map();

    function getSentiment(result) {
        return [result['negative'], result['neutral'], result['positive']];
    }

    for (const result of results) {
        sentiments.set(result['id'], getSentiment(result))
        if (result['kind'] === 'video') {
            const id = result['id'];
            videos.set(id, new Map());
        } else if (result['kind'] === 'comment') {
            const video_id = result['videoId'];
            const topLevelId = commentReplyId(result['id']);
            if (!videos.has(video_id)) {
                videos.set(video_id, new Map());
            }
            if (topLevelId) {
                if (!videos.get(video_id).get(topLevelId)) {
                    videos.get(video_id).set(topLevelId, []);
                }
                videos.get(video_id).get(topLevelId).push(result['id']);
            } else {
                videos.get(video_id).set(result['id'], [])
            }
        }
    }

    return {tree: videos, sentiments: sentiments};
}

// TODO: solve last of the benchmark query issue

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
 * Returns the id of a topLevelComment given the id of the reply
 * @param {string} id Id of the reply comment
 * @returns Id of topLevelComment or empty string if id is already a topLevelComment
 */
function commentReplyId(id) {
    return id.substring(0, id.indexOf('.'));
}


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
 * @param {{tree: Map<string, Map<string, string[]>>, 
 *  sentiments: Map<string, number[]>}} resultsTree 
 * @param {Map<string, Object} videos
 */
async function parseResults(resultsTree) {
    const TEXT_MAX_LENGTH = 500;

    function showMoreLessHtml(text) {
        if (text.length > TEXT_MAX_LENGTH) {
            return text.slice(0, TEXT_MAX_LENGTH) + 
                `<span class="dots">...</span><span class="more">` +
                text.slice(TEXT_MAX_LENGTH, text.length) +
                `</span>`;
        }
        // TODO: show more show less button
        return text;
    }

    function sentimentsHtml(params) {
        if (Array.isArray(params.sentiments) && params.sentiments.length > 0) {
            let [negative, neutral] = params.sentiments;
            return `
                <div class="mb-1 d-flex sentiment-bar">
                    <div class="h-100 negative-bar" style="width: ${negative * 100}%"></div>
                    <div class="h-100 neutral-bar" style="width: ${neutral * 100}%"></div>
                </div>
            `;
        }
        return '';
    }

    function likesHtml(params) {
        return `
            <div class="px-3 py-2 d-inline-flex rounded-pill c-light-gray">
                <img src="static/media/hand-thumbs-up-fill.svg" class="me-1">
                <span>${params.likes}</span>
            </div>
        `;
    }

    function videoHtml(params) {
        return `
        <div class="mt-4 mb-1">
            <h5><b>${params.title}</b></h5>
            <div>${showMoreLessHtml(params.description)}</div>
            ${sentimentsHtml(params)}
            <div>${likesHtml(params)}</div>
        </div>
        `;
    }

    function commentHtml(params) {
        return `
        <div class="ms-5 mt-3">
            <h6><b>${params.author}</b></h6>
            <div>${params.text}</div>
            ${sentimentsHtml(params)}
            <div>${likesHtml(params)}</div>
        </div>
        `;
    }

    function replyHtml(params) {
        return `
        <div class="ms-5">${commentHtml(params)}</div>
        `;
    }

    divResponse.innerHTML = "";
    for (const videoId of resultsTree.tree.keys()) {
        const tlComments = resultsTree.tree.get(videoId);
        const video = JSON.parse(await loadVideo(videoId));

        divResponse.appendChild(htmlToElement(videoHtml(
            {...video.video, sentiments: resultsTree.sentiments.get(videoId) || []}
            )));
        for (const tlCommentId of tlComments.keys()) {
            const tlComment = video.comments.find(el => el['topLevelComment']['id'] === tlCommentId);
            divResponse.appendChild(htmlToElement(commentHtml(
                {...tlComment['topLevelComment'], sentiments: resultsTree.sentiments.get(tlCommentId) || []}
                )));
            const repliesIds = tlComments.get(tlCommentId);
            if (repliesIds) {
                for (const replyId of repliesIds) {
                    const reply = tlComment['replies'].find(el => el['id'] === replyId);
                    divResponse.appendChild(htmlToElement(replyHtml(
                        {...reply, sentiments: resultsTree.sentiments.get(replyId) || []}
                        )));
                }
            }
        }
    }
}