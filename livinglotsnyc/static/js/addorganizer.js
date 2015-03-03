//
// addorganizer.js
//
// Scripts that only run when adding an organizer.
//

function showOrHideFacebookPage() {
    // Only show facebook page input if organizer is a cbo
    var type = $(':input[name=type] option:selected').text(),
        $facebookPage = $(':input[name=facebook_page]').parents('.form-group');

    if (type === 'community based organization') {
        $facebookPage.show();
    }
    else {
        $facebookPage.hide();
    }
}

$(document).ready(function () {
    if ($('.add-organizer-page').length > 0) {
        showOrHideFacebookPage();

        // When the type changes, show or hide facebook_page accordingly
        $(':input[name=type]').change(showOrHideFacebookPage);
    }
});
