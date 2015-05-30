function start() {
    function sleep(milliSeconds) {
        var startTime = new Date().getTime();
        while(new Date().getTime() < startTime + milliSeconds);
    }
    console.log("Request handle 'start' was called.");
    sleep(10000);
    return "hello start";
}

function upload() {
    console.log("Request handle 'upload' was called.");
    return "hello upload.";
}

exports.start = start;
exports.upload = upload;
