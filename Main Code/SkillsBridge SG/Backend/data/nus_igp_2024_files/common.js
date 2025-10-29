//search function
function tryParseJson(data) {
    try {
        return JSON.parse(data);
    } catch (e) {
        return null;
    }
}

function escapeHTML(html) {
    return $('<div>').text(html).html();
}

function redirectTo(url, target) {
    var isUrlValid = validateBeforeRedirect(url)
    if (isUrlValid) {
        window.open(url, target || '_self');
    }
}

function validateBeforeRedirect(url) {
    var endpoint = $('body')?.data('application-path');
    var orginUrl = endpoint == "/" ? window.location.origin : $('body')?.data('application-path');
    var inputUrl = url.startsWith("/") ? window.location.origin : url;
    var isUrlValid = true;

    //var isUrlExistedInAllowList = Boolean(new URL(orginUrl).host === new URL(inputUrl).host);

    //isUrlValid = Boolean(isUrlExistedInAllowList);

    return isUrlValid;
}

function getSessionStorage(name) {
    if (typeof (Storage) === 'undefined') return;
    return sessionStorage[name];
}

function setSessionStorage(name, value) {
    if (typeof (Storage) === 'undefined') return;
    return sessionStorage.setItem(name, value);
}

function removeSessionStorage(name) {
    if (typeof (Storage) === 'undefined') return;
    return sessionStorage.removeItem(name);
}

function entries(obj) {
    var keys = Object.keys(obj);
    var result = [];
    for (var i = 0; i < keys.length; i++) {
        result.push([keys[i], obj[keys[i]]]);
    }
    return result;
}

function callApi(url) {
    var throwException = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;
    return $.get(url).catch(function (e) {
        if (throwException) return Promise.reject(e);
        else return Promise.resolve();
    });
}

function removeLastSlash(url) {
    if (url !== null && url.endsWith("/")) {
        url = url.substring(0, url.length - 1);
    }

    return url;
}