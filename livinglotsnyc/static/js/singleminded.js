//
// A very simple AJAX requests queue of length 1.
//
// For requests that will be made repeatedly and that only the most recent 
// should be adhered to.
//
define([], function() {
    var thoughts = {};

    function forget(name) {
        var request = thoughts[name];

        // If request exists and does not have a DONE state, abort it
        if (request && request.readyState != 4) {
            request.abort();
        }

        thoughts[name] = null;
    }

    function remember(params) {
        var name = params.name,
            jqxhr = params.jqxhr;

        forget(name);

        jqxhr.done(function() {
            // Don't bother remembering requests we've finished
            forget(name);
        });
        thoughts[name] = jqxhr;
    }

    return {
        forget: forget,
        remember: remember
    }

});
