//
// Welcome header
//

module.exports = {
    init: function () {
        $('.map-welcome-toggle').click(function (e) {
            $('.map-welcome').toggleClass('closed');
            $('.map-welcome-body').slideToggle();
            e.preventDefault();
            return false;
        });
    }
};
