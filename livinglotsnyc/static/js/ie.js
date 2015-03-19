/**
 * detect IE
 * returns version of IE or false, if browser is not Internet Explorer
 *
 * Taken from this SO answer:
 *  http://stackoverflow.com/questions/19999388/jquery-check-if-user-is-using-ie/21712356#21712356
 */
function detectIE() {
    var ua = window.navigator.userAgent;

    var msie = ua.indexOf('MSIE ');
    if (msie > 0) {
        // IE 10 or older => return version number
        return parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10);
    }

    var trident = ua.indexOf('Trident/');
    if (trident > 0) {
        // IE 11 => return version number
        var rv = ua.indexOf('rv:');
        return parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10);
    }

    var edge = ua.indexOf('Edge/');
    if (edge > 0) {
       // IE 12 => return version number
       return parseInt(ua.substring(edge + 5, ua.indexOf('.', edge)), 10);
    }

    // other browser
    return false;
}

module.exports = {

    detect: detectIE,

    log: function (msg) {
        if (detectIE()) {
            console.log(msg);
        }
    }

};
