//
// main.js
//
// Scripts that should run on every page.
//

require('fancybox');


/*
 * Global form-related scripts
 */
$(document).ready(function () {
    /*
     * Disable submit buttons on forms once they have been submitted once.
     */
    $('form').submit(function () {
        $(this).find('input[type="submit"]').attr('disabled', 'disabled');
    });

    /*
     * Collapse the collapsible sections
     */
    // Slide up those sections not initially expanded
    $('.collapsible-section:not(.is-expanded) .collapsible-section-text').slideUp();

    // Prepare headers for clicking
    $('.collapsible-section-header').click(function () {
        var $section = $(this).parent(),
            $sectionText = $section.find('.collapsible-section-text');
        $section.toggleClass('is-expanded');
        $sectionText.slideToggle();
    });

    /*
     * Fancy the fancyboxes
     */
    $('.fancybox').fancybox({
        beforeShow: function () {
            var $link = this.element,
                $img = $link.find('img'),
                alt = $img.attr('alt'),
                addedBy = $link.data('added-by'),
                description = $link.data('description');

            this.inner.find('img').attr('alt', alt);
            this.title = alt + ' by ' + addedBy + '<p>' + description + '</p>';
        }
    });

});


/*
 * Page-specific modules
 */
require('./mappage.js');
require('./lotdetailpage.js');
