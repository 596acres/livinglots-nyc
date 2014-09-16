//
// main.js
//
// Scripts that should run on every page.
//

define(
    [
        'jquery',

        'bootstrap'
    ], function ($) {

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
            require(['jquery'], function () {
                // Slide up those sections not initially expanded
                $('.collapsible-section:not(.is-expanded) .collapsible-section-text').slideUp();

                // Prepare headers for clicking
                $('.collapsible-section-header').click(function () {
                    var $section = $(this).parent(),
                        $sectionText = $section.find('.collapsible-section-text');
                    $section.toggleClass('is-expanded');
                    $sectionText.slideToggle();
                });
            });

            /*
             * Fancy the fancyboxes
             */
            require(['jquery', 'fancybox'], function () {
                $('.fancybox').fancybox();
            });

        });


        /*
         * Page-specific modules
         */

        if ($('.map-page').length !== 0) {
            require(['mappage']);
        }

        if ($('.lot-detail-page').length !== 0) {
            require(['lotdetailpage']);
        }

});
