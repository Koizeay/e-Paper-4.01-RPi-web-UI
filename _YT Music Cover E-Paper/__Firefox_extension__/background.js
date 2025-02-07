// background.js
let lastVideoId = null;
let isEnabled = true;

browser.browserAction.onClicked.addListener(() => {
    isEnabled = !isEnabled;
    browser.browserAction.setIcon({
        path: isEnabled ? "icon-on.png" : "icon-off.png"
    });
});

function getVideoIdFromUrl(url) {
    const match = url.match(/[?&]v=([a-zA-Z0-9_-]{11})/);
    return match ? match[1] : null;
}

async function checkVideoId(tabId, url) {
    if (!isEnabled) return;
    const videoId = getVideoIdFromUrl(url);
    if (videoId && videoId !== lastVideoId) {
        lastVideoId = videoId;
        fetch(`http://127.0.0.1:5000?id=${videoId}`).catch(err => console.error("Fetch error:", err));
    }
}

browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (tab.url && (tab.url.includes("youtube.com/watch") || tab.url.includes("music.youtube.com/watch"))) {
        checkVideoId(tabId, tab.url);
    }
});
