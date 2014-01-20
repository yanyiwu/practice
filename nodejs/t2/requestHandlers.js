function start() {
    console.log("Request handle 'start' was called.");
    return "hello start";
}

function upload() {
    console.log("Request handle 'upload' was called.");
    return "hello upload.";
}

exports.start = start;
exports.upload = upload;
