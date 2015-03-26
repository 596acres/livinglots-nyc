//
// maplinks.js
//
// A handy way to create links to a filtered view of the map. The filters
// should be in data- attributes such that they will work in 
// filters.toParams().
//
var filters = require('./filters');


function mapLink(linkFilters) {
    return '/?' + $.param(filters.toParams(linkFilters));
}


function init () {
    $('.map-link').each(function () {
        $(this).attr('href', mapLink($(this).data()));
    });
}

$(document).ready(init);

module.exports = {
    init: init
};
