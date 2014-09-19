//
// Welcome header
//

function initClose() {
    $('.map-welcome-close-button').click(function (e) {
        $('.map-welcome').addClass('closed');
        $('.map-welcome h1').animate({ 'font-size': '28px' });
        $('.map-welcome-body').slideUp();
        e.preventDefault();
        return false;
    });
}

function initOpen() {
    $('.map-welcome-open-button').click(function (e) {
        $('.map-welcome').removeClass('closed');
        $('.map-welcome h1').animate({ 'font-size': '56px' });
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
