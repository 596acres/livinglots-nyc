//
// mappage.js
//
// Scripts that only run on the map page.
//

var _ = require('underscore');
var Handlebars = require('handlebars');
var L = require('leaflet');
var Spinner = require('spinjs');
var singleminded = require('./singleminded');
var initWelcome = require('./welcome').init;

require('jquery.infinitescroll');
require('leaflet.loading');
require('./leaflet.lotmap');
require('./map.search.js');
require('./overlaymenu');


function buildLotFilterParams(map, options) {
    var layers = _.map($('.filter-layer:checked'), function (layer) {
        return $(layer).attr('name'); 
    });
    var publicOwnerPks = [$('.filter-owner-public').val()];
    var params = {
        layers: layers.join(','),
        parents_only: true,
        projects: $('.filter-projects').val(),
        public_owners: publicOwnerPks.join(',')
    };

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

function setFilters(params) {
    // Clear checkbox filters
    $('.filter[type=checkbox]').prop('checked', false);

    // Set layers filters
    var layers = params.layers.split(',');
    _.each(layers, function (layer) {
        $('.filter-layer[name=' + layer +']').prop('checked', true);
    });

    // Set owners filters
    var publicOwners = params.public_owners.split(',');
    _.each(publicOwners, function (pk) {
        $('.filter-owner-public[data-owner-pk=' + pk +']').prop('checked', true);
    });

    // Set boundaries filters

    var projects = params.projects;
    if (projects !== '') {
        $('.filter-projects').val(projects);
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
            var spinner = new Spinner({
                left: '0px',
                top: '0px'
            }).spin($('.activity-stream')[0]);

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
            params = deparam();
            setFilters(params);
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
    }
});
