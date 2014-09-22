//
// lotdetailpage.js
//
// Scripts that only run on the lot detail page.
//

var Handlebars = require('handlebars');
var L = require('leaflet');

var mapstyles = require('./map.styles');
var StreetView = require('./streetview');

require('leaflet.dataoptions');


function addBaseLayer(map) {
    var streets = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);
}

function addLotsLayer(map) {
    var url = map.options.lotsurl + '?' + 
        $.param({ lot_center: map.options.lotPk });
    $.getJSON(url, function (data) {
        var lotsLayer = L.geoJson(data, {
            style: function (feature) {
                var style = {
                    color: mapstyles[feature.properties.layer],
                    fillColor: mapstyles[feature.properties.layer],
                    fillOpacity: 0.5,
                    opacity: 0.5,
                    weight: 1
                };
                if (feature.properties.pk === map.options.lotPk) {
                    style.color = '#000';
                    style.opacity = 1;
                }
                return style;
            }
        });
        lotsLayer.addTo(map);
    });
}

if ($('.lot-detail-page').length > 0) {
    $(document).ready(function () {
        var map = L.map('lot-detail-map');
        addBaseLayer(map);
        addLotsLayer(map);
        StreetView.load_streetview(
            $('.lot-detail-header-image').data('lon'),
            $('.lot-detail-header-image').data('lat'),
            $('.lot-detail-header-image'),
            $('.lot-detail-header-streetview-error')
        );
    });
}
