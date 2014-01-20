function route(handle, pathname) {
    console.log("route a request for %s", pathname);
    if(typeof handle[pathname] === 'function'){
        return handle[pathname]();
    }
    else{
        console.log("no request handler found for %s", pathname);
        return "404 not found.";
    }
}

exports.route = route;
