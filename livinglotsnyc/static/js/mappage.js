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
var oasis = require('./oasis');
var filters = require('./filters');

require('./leaflet.lotmap');
require('bootstrap_button');
require('bootstrap_tooltip');
require('jquery-infinite-scroll');
require('leaflet-loading');
require('./handlebars.helpers');
require('./map.search.js');
require('./overlaymenu');


function updateLotCount(map) {
    var url = Django.url('lots:lot_count') + '?' + map.getParamsQueryString({ bbox: true });
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
    var url = Django.url('lots:lot_ownership_overview');
    $.getJSON(url + '?' + map.getParamsQueryString({ bbox: true }), function (data) {
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
    var params = map.buildLotFilterParams();
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

    // If boundaries were set via query string trigger change here. Can't do 
    // until the map exists, but we actually do want to set most the other 
    // filters before the map exists.
    $('.filter-boundaries').each(function () {
        if ($(this).val()) {
            $(this).trigger('change');
        }
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
        $('.filter-owner-public').val(params.public_owners);
    }
    if (params.private_owners) {
        $('.filter-owner-private').val(params.private_owners);
    }

    // Set boundaries filters
    if (params.boundary) {
        var split = params.boundary.split('::'),
            layer = split[0].replace(/\+/g, ' '),
            id = split[1];
        $('.filter-boundaries[data-layer="' + layer + '"]').val(id);
    }
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

        var mapOptions = {
            filterParams: filters.filtersToParams(null, {}),
            onMouseOverFeature: function (feature) {},
            onMouseOutFeature: function (feature) {}
        };

        // Get the current center/zoom first rather than wait for map to load
        // and L.hash to set them. This is slightly smoother
        var hash = window.location.hash;
        if (hash && hash !== '') {
            hash = hash.slice(1).split('/');
            mapOptions.center = hash.slice(1);
            mapOptions.zoom = hash[0];
        }

        var map = L.lotMap('map', mapOptions);

        initializeBoundaries(map);

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
                var oasisUrl = oasis.vacantLotsUrl(result.latitude, result.longitude);
                map.addUserLayer([result.latitude, result.longitude], {
                    popupContent: '<p>This is the point we found when we searched.</p><p>Not seeing a vacant lot here that you expected? Check <a href="' + oasisUrl + '" target="_blank">OASIS in this area</a>.</p>'
                });
            });

        $('.filter').change(function () {
            var params = map.buildLotFilterParams();
            map.updateFilters(params);
            updateLotCount(map);
        });

        // When the select for an owner is changed, check that owner type
        $('.filter-owner select').change(function () {
            $(this).parents('.filter-owner').find('.filter-owner-type')
                .prop('checked', true)
                .trigger('change');
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
                map.addLotsLayer(map.buildLotFilterParams());
                map.updateDisplayedLots();
            }
        });

        $('.export').click(function (e) {
            var url = $(this).data('baseurl') + map.getParamsQueryString({ bbox: true });
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
    }
});
