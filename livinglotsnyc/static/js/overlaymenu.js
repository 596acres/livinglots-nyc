//
// overlaymenu.js
//
// Overlay / dropdown menus, like modals but less intrusive
//

var _ = require('underscore');


function show(button, menu) {
    var offset = button.offset(),
        outerWidth = button.outerWidth(),
        outerHeight = button.outerHeight(),
        menuWidth = menu.outerWidth();

    button.trigger('overlaymenuopen');

    menu
        .show()
        .offset({
            left: offset.left + outerWidth - menuWidth,
            top: offset.top + outerHeight + 13
        });

    // If user hits <Esc>, hide menu
    $('body')
        .on('keyup.overlaymenu', function (event) {
            if (event.which === 27) {
                hide(button, menu);
            }
        });
}

function hide(button, menu) {
    button.trigger('overlaymenuclose');
    menu.hide();

    // Remove event handler that will hide menus
    $('body').off('keyup.overlaymenu');
}

function isVisible(menu) {
    return menu.is(':visible');
}

function isInMenu(target, menu) {
    return (target[0] === menu[0] ||
            _.find(target.parents(), function (ele) { return ele === menu[0]; }));
}

$.fn.overlaymenu = function (options) {
    var button = this,
        menu = $(options.menu);

    $('*').click(function (e) {
        var target = $(e.target);

        // If user not clicking in menu, consider hiding or showing it
        if (!isInMenu(target, menu)) {
            if (target[0] === button[0]) {
                // If button clicked, show or hide the menu appropriately
                if (isVisible(menu)) {
                    hide(button, menu);
                }
                else {
                    show(button, menu);
                }
                return false;
            }
            else {
                // Something else was clicked--hide the menu
                if (isVisible(menu)) {
                    hide(button, menu);
                }
            }
        }
    });
    return this;
};
