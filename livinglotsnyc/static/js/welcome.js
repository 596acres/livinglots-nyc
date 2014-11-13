//
// Welcome header
//

function initClose() {
    $('.map-welcome-close-button').click(function (e) {
        $('.map-welcome').addClass('closed');
        $('.map-welcome-body').slideUp();
        e.preventDefault();
        return false;
    });
}

function initOpen() {
    $('.map-welcome-open-button').click(function (e) {
        $('.map-welcome').removeClass('closed');
        $('.map-welcome-body').slideDown();
        e.preventDefault();
        return false;
    });
}

module.exports = {
    init: function () {
        initClose();
        initOpen();
    }
};
