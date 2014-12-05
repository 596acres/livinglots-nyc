//
// mappage.js
//
// Scripts that only run on the map page.
//

var _ = require('underscore');
var Handlebars = require('handlebars');
var L = require('leaflet');
var Spinner = require('spin.js');
var singleminded = require('./singleminded');
var initWelcome = require('./welcome').init;

require('bootstrap_button');
require('bootstrap_tooltip');
require('jquery.infinitescroll');
require('leaflet.loading');
require('livinglots-map/src/livinglots.addlot');
require('livinglots-map/src/livinglots.mail');
require('./handlebars.helpers');
require('./leaflet.lotmap');
require('./map.search.js');
require('./overlaymenu');


function buildLotFilterParams(map, options) {
    var layers = _.map($('.filter-layer:checked'), function (layer) {
        return $(layer).attr('name'); 
    });
    var ownerTypes = _.map($('.filter-owner-type:checked'), function (ownerType) {
        return $(ownerType).attr('name'); 
    });
    var publicOwnerPks = [$('.filter-owner-public').val()];
    var privateOwnerPks = [$('.filter-owner-private').val()];

    var params = {
        layers: layers.join(','),
        owner_types: ownerTypes.join(','),
        parents_only: true,
        private_owners: privateOwnerPks.join(','),
        public_owners: publicOwnerPks.join(',')
    };

    // Add boundary, if any
    $.each($('.filter-boundaries'), function () {
        if ($(this).val() !== '') {
            params.boundary = $(this).data('layer') + '::' + $(this).val(); 
        }
    });

    // Add BBOX if requested
    if (options && options.bbox) {
        params.bbox = map.getBounds().toBBoxString();
    }

    return params;
}

function updateLotCount(map) {
    var url = Django.url('lots:lot_count') + '?' +
        $.param(buildLotFilterParams(map, { bbox: true }));
    singleminded.remember({
        name: 'updateLotCount',
        jqxhr: $.getJSON(url, function (data) {
            _.each(data, function (value, key) {
                $('#' + key).text(value);
            });
        })
    });
}

function updateOwnershipOverview(map) {
    var url = Django.url('lots:lot_ownership_overview'),
        params = buildLotFilterParams(map, { bbox: true });
    $.getJSON(url + '?' + $.param(params), function (data) {
        var template = Handlebars.compile($('#details-template').html());
        var content = template({
            lottypes: data.owners
        });
        $('.details-overview').html(content);
        $('.details-area-compare-tooltip').tooltip();
        $('.details-show-owners :input').change(function () {
            var $list = $('.details-owner-list-' + $(this).data('type')),
                $otherButton = $('.details-show-organizing-' + $(this).data('type'));
            if ($(this).is(':checked')) {
                $list.slideDown();

                // Slide up other one
                if ($otherButton.is('.active')) {
                    $('.details-show-organizing-' + $(this).data('type')).button('toggle');
                }
            }
            else {
                $list.slideUp();
            }
        });
        $('.details-show-organizing :input').change(function () {
            var $list = $('.details-organizing-' + $(this).data('type')),
                $otherButton = $('.details-show-owners-' + $(this).data('type'));
            if ($(this).is(':checked')) {
                $list.slideDown();

                // Slide up other one
                if ($otherButton.is('.active')) {
                    $('.details-show-owners-' + $(this).data('type')).button('toggle');
                }
            }
            else {
                $list.slideUp();
            }
        });
    });
}

function updateDetailsLink(map) {
    var params = buildLotFilterParams(map);
    delete params.parents_only;

    var l = window.location,
        query = '?' + $.param(params),
        url = l.protocol + '//' + l.host + l.pathname + query + l.hash;
    $('a.details-link').attr('href', url);
}

function initializeBoundaries(map) {
    // Check for city council / community board layers, console a warning
    var url = window.location.protocol + '//' + window.location.host +
        Django.url('inplace:layer_upload');
    if ($('.filter-city-council-districts').length === 0) {
        console.warn('No city council districts! Add some here: ' + url);
    }
    if ($('.filter-community-districts').length === 0) {
        console.warn('No community districts! Add some here: ' + url);
    }

    $('.filter-boundaries').change(function () {
        // Clear other boundary filters
        $('.filter-boundaries').not('#' + $(this).attr('id')).val('');

        addBoundary(map, $(this).data('layer'), $(this).val());
    });
}

function addBoundary(map, layer, pk) {
    if (!pk || pk === '') {
        map.removeBoundaries();
    }
    var url = Django.url('inplace:boundary_detail', { pk: pk });
    $.getJSON(url, function (data) {
        map.updateBoundaries(data, { zoomToBounds: true });
    });
}

function deparam() {
    var vars = {},
        param,
        params = window.location.search.slice(1).split('&');
    for(var i = 0; i < params.length; i++) {
        param = params[i].split('=');
        vars[param[0]] = decodeURIComponent(param[1]);
    }
    return vars;
}

function setFiltersUIFromQueryParams(params) {
    // Clear checkbox filters
    $('.filter[type=checkbox]').prop('checked', false);

    // Set layers filters
    var layers = params.layers.split(',');
    _.each(layers, function (layer) {
        $('.filter-layer[name=' + layer +']').prop('checked', true);
    });

    // Set owner types
    if (params.owner_types) {
        _.each(params.owner_types.split(','), function (owner_type) {
            $('.filter-owner-type[name=' + owner_type +']').prop('checked', true);
        });
    }

    // Set owners filters
    if (params.public_owners) {
        var publicOwners = params.public_owners.split(',');
        _.each(publicOwners, function (pk) {
            $('.filter-owner-public[data-owner-pk=' + pk +']').prop('checked', true);
        });
    }
    if (params.privateOwners) {
        var privateOwners = params.private_owners.split(',');
        _.each(privateOwners, function (pk) {
            $('.filter-owner-private[data-owner-pk=' + pk +']').prop('checked', true);
        });
    }

    // Set boundaries filters
}

function prepareOverlayMenus(map) {
    $('.overlay-download-button').overlaymenu({
        menu: '.overlaymenu-download'
    });

    $('.overlay-admin-button').overlaymenu({
        menu: '.overlaymenu-admin'
    });

    $('.overlay-details-button')
        .overlaymenu({
            menu: '.overlaymenu-details'
        })
        .on('overlaymenuopen', function () {
            var spinner = new Spinner({
                left: '50%',
                top: '50%'
            }).spin($('.details-overview')[0]);
            updateDetailsLink(map);
            updateOwnershipOverview(map);
        });

    $('.overlay-news-button')
        .overlaymenu({
            menu: '.overlaymenu-news'
        })
        .on('overlaymenuopen', function () {
            var spinner = new Spinner().spin($('.activity-stream')[0]);

            var url = Django.url('activity_list');
            $('.activity-stream').load(url, function () {
                $('.action-list').infinitescroll({
                    loading: {
                        finishedMsg: 'No more activities to load.'
                    },
                    behavior: 'local',
                    binder: $('.overlaymenu-news .overlaymenu-menu-content'),
                    itemSelector: 'li.action',
                    navSelector: '.activity-stream-nav',
                    nextSelector: '.activity-stream-nav a:first'
                });
            });
        });

    $('.overlay-filter-button').overlaymenu({
        menu: '.overlaymenu-filter'
    });


}

$(document).ready(function () {
    if ($('.map-page').length > 0) {
        var params;
        if (window.location.search.length) {
            setFiltersUIFromQueryParams(deparam());
        }

        var map = L.lotMap('map', {
            filterParams: buildLotFilterParams(null),

            onMouseOverFeature: function (feature) {
            },

            onMouseOutFeature: function (feature) {
            }

        });

        map.addLotsLayer();

        prepareOverlayMenus(map);

        $('.details-print').click(function () {
            // TODO This is not a good solution since the map size changes
            // on print. Look into taking screenshots like:
            //   https://github.com/tegansnyder/Leaflet-Save-Map-to-PNG
            //   http://html2canvas.hertzen.com
            window.print();
        });

        $('form.map-search-form').mapsearch()
            .on('searchstart', function (e) {
                map.removeUserLayer();
            })
            .on('searchresultfound', function (e, result) {
                map.addUserLayer([result.latitude, result.longitude]);
            });

        $('.filter').change(function () {
            var params = buildLotFilterParams(map);
            map.updateFilters(params);
            updateLotCount(map);
        });

        updateLotCount(map);
        map.on({
            'moveend': function () {
                updateLotCount(map);
            },
            'zoomend': function () {
                updateLotCount(map);
            },
            'lotlayertransition': function (e) {
                map.addLotsLayer(buildLotFilterParams(map));
            }
        });

        $('.export').click(function (e) {
            var url = $(this).data('baseurl') + 
                $.param(buildLotFilterParams(map, { bbox: true }));
            window.location.href = url;
            e.preventDefault();
        });

        initWelcome();

        $('.admin-button-add-lot').click(function () {
            map.enterLotAddMode();
        });

        $('.admin-button-email').click(function () {
            map.enterMailMode();
        });

        initializeBoundaries(map);
    }
});
