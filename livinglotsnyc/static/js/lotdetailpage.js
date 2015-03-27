//
// lotdetailpage.js
//
// Scripts that only run on the lot detail page.
//

var Handlebars = require('handlebars');
var L = require('leaflet');

require('leaflet-dataoptions');

require('./leaflet.lotlayer');
require('./leaflet.lotmarker');
var mapstyles = require('./map.styles');
var StreetView = require('./streetview');
require('./overlaymenu');


var vectorLayerOptions = {
    serverZooms: [16],
    unique: function (feature) {
        return feature.id;
    }
};

function getLotLayerOptions(lotPk) {
    return {
        pointToLayer: function (feature, latlng) {
            var options = {};
            if (feature.properties.has_organizers) {
                options.hasOrganizers = true;
            }
            return L.lotMarker(latlng, options);
        },
        style: function (feature) {
            var style = {
                fillOpacity: 0.2,
                stroke: false
            };
            style.fillColor = mapstyles.getLayerColor(feature.properties.layers.split(','));

            // Style this lot distinctly
            if (feature.properties.id === lotPk) {
                style.fillOpacity = 1;
            }
            return style;
        }
    };
}

function addBaseLayer(map) {
    var streets = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);
}

function addLotsLayer(map) {
    var url = map.options.lotsurl,
        lotLayerOptions = getLotLayerOptions(map.options.lotPk);
    var lotsLayer = L.lotLayer(url, vectorLayerOptions, lotLayerOptions).addTo(map);
}

function initFacebookLink($link) {
    var url = 'http://www.facebook.com/sharer/sharer.php?' + $.param({
        u: window.location.href
    });
    $link.attr('href', url);
}

function initTwitterLink($link) {
    var url = 'http://twitter.com/intent/tweet?' + $.param({
        related: '596acres',
        text: $link.data('tweet'),
        url: window.location.href
    });
    $link.attr('href', url);
}

$(document).ready(function () {
    if ($('.lot-detail-page').length > 0) {
        var map = L.map('lot-detail-map', {
            doubleClickZoom: false,
            dragging: false,
            scrollWheelZoom: false,
            touchZoom: false
        });

        var bbox = map.options.bbox;
        if (bbox) {
            map.fitBounds([
                [bbox[1], bbox[0]],   
                [bbox[3], bbox[2]]   
            ], { padding: [20, 20], maxZoom: 18 });
        }

        addBaseLayer(map);
        addLotsLayer(map);
        StreetView.load_streetview(
            $('.lot-detail-header-image').data('lon'),
            $('.lot-detail-header-image').data('lat'),
            $('.lot-detail-header-image'),
            $('.lot-detail-header-streetview-error')
        );

        $('.referral-message').slideDown();
        $('.referral-message-close').click(function () {
            $('.referral-message').slideUp();
            return false;
        });
    }

    $('.overlay-nearby-button').overlaymenu({
        menu: '.overlaymenu-nearby'
    });

    $('.btn-add-to-group').click(function () {
        if (!confirm("Group these two lots? This will move notes, organizers, and other content to the group and is very difficult to undo.")) {
            return false;
        }
        var url = Django.url('lots:add_to_group', { pk: $(this).data('lot') });
        $.post(url, { lot_to_add: $(this).data('lot-to-add') }, function (data) {
            window.location = Django.url('lots:lot_detail', { pk: data.group });
        });
        return false;
    });

    $('.btn-remove-from-group').click(function () {
        if (!confirm("Remove this lot from the group?")) {
            return false;
        }
        var url = Django.url('lots:remove_from_group', { pk: $(this).data('lot') });
        $.post(url, {}, function (data) {
            window.location = Django.url('lots:lot_detail', { pk: data.former_group });
        });
        return false;
    });

    $('.btn-show-private-organizers').click(function () {
        $('.organizer-list-private').slideToggle();
        return false;
    });

    initFacebookLink($('.share-facebook'));
    initTwitterLink($('.share-twitter'));
});
