var _ = require('underscore');
var filters = require('./filters');
var Handlebars = require('handlebars');
var L = require('leaflet');
var mapstyles = require('./map.styles');
var Spinner = require('spin.js');

require('leaflet.bing');
require('leaflet.dataoptions');
require('leaflet.hash');
require('leaflet.usermarker');
require('livinglots-map/src/livinglots.boundaries');

require('./leaflet.lotlayer');
require('./leaflet.lotmarker');


L.LotMap = L.Map.extend({
    centroidsLayer: null,
    currentFilters: {},
    polygonsLayer: null,
    lotLayerTransitionPoint: 15,
    previousZoom: null,
    userLayer: null,
    userLocationZoom: 16,

    filters: null,

    compiledPopupTemplate: null,

    getPopupTemplate: function () {
        if (this.compiledPopupTemplate) {
            return this.compiledPopupTemplate;
        }
        var source = $("#popup-template").html();
        this.compiledPopupTemplate = Handlebars.compile(source);
        return this.compiledPopupTemplate;
    },

    lotLayerOptions: {
        onEachFeature: function (feature, layer) {
            layer.on({
                'click': function (event) {
                    // Trigger a click on the body to close all overlaymenus
                    $('body').trigger('click');

                    var latlng = event.latlng,
                        x = this._map.latLngToContainerPoint(latlng).x,
                        y = this._map.latLngToContainerPoint(latlng).y - 100,
                        point = this._map.containerPointToLatLng([x, y]),
                        template = this._map.getPopupTemplate();
                    this.bindPopup('<div id="popup"></div>').openPopup();
                    var spinner = new Spinner().spin($('#popup')[0]);
                    $.getJSON(Django.url('lots:lot_detail_json', { pk: this.feature.properties.id }), function (data) {
                        spinner.stop();
                        $('#popup').append(template(data));
                    });
                    return this._map.setView(point, this._map._zoom);
                },
                'mouseover': function (event) {
                    this._map.options.onMouseOverFeature(event.target.feature);
                },
                'mouseout': function (event) {
                    this._map.options.onMouseOutFeature(event.target.feature);
                }
            });
        },
        pointToLayer: function (feature, latlng) {
            var options = {};
            var layers = feature.properties.layers.split(',');
            if (_.contains(layers, 'organizing') || _.contains(layers, 'in_use_started_here')) {
                options.hasOrganizers = true;
            }
            return L.lotMarker(latlng, options);
        },
        style: function (feature) {
            var style = {
                fillColor: '#000000',
                fillOpacity: 1,
                stroke: 0
            };
            style.fillColor = mapstyles.getLayerColor(feature.properties.layers.split(','));
            return style;
        },
        popupOptions: {
            autoPan: false,
            maxWidth: 250,
            minWidth: 250,
            offset: [0, 0]
        }
    },

    initialize: function (id, options) {
        L.Map.prototype.initialize.call(this, id, options);
        this.addBaseLayer();
        var hash = new L.Hash(this);

        if (options.filterParams) {
            this.currentFilters = filters.paramsToFilters(options.filterParams);
        }

        // When new lots are added ensure they should be displayed
        var map = this;
        this.on('layeradd', function (event) {
            // Dig through the layers of layers
            event.layer.on('layeradd', function (event) {
                event.layer.eachLayer(function (lot) {
                    if (!lot.feature || !lot.feature.properties.layers) return;
                    if (filters.lotShouldAppear(lot, map.currentFilters, map.boundariesLayer)) {
                        lot.show();
                    }
                    else {
                        lot.hide();
                    }
                });
            });
        });

        this.on('zoomend', function () {
            var currentZoom = this.getZoom();
            if (this.previousZoom) {
                // Switch to centroids
                if (currentZoom <= this.lotLayerTransitionPoint && 
                    this.previousZoom > this.lotLayerTransitionPoint) {
                    this.fire('lotlayertransition', { details: false });
                }
                // Switch to polygons
                else if (currentZoom > this.lotLayerTransitionPoint &&
                         this.previousZoom <= this.lotLayerTransitionPoint) {
                    this.fire('lotlayertransition', { details: true });
                }
            }
            else {
                // Start with centroids
                if (currentZoom <= this.lotLayerTransitionPoint) {
                    this.fire('lotlayertransition', { details: false });
                }
                // Start with polygons
                else if (currentZoom > this.lotLayerTransitionPoint) {
                    this.fire('lotlayertransition', { details: true });
                }
            }
            this.previousZoom = currentZoom;
        });

        this.on('boundarieschange', function () {
            this.updateDisplayedLots();
        });
    },

    addBaseLayer: function () {
        var streets = L.tileLayer('http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png', {
            attribution: 'Map tiles by <a href="http://stamen.com/">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'
        }).addTo(this);
        var bing = new L.BingLayer('Ajio1n0EgmAAvT3zLndCpHrYR_LHJDgfDU6B0tV_1RClr7OFLzy4RnkLXlSdkJ_x');

        L.control.layers({
            streets: streets,
            satellite: bing
        }).addTo(this);
    },

    addLotsLayer: function () {
        this.addCentroidsLayer();
        this.addPolygonsLayer();
        if (this.getZoom() <= this.lotLayerTransitionPoint) {
            this.addLayer(this.centroidsLayer);
            this.removeLayer(this.polygonsLayer);
        }
        else {
            this.removeLayer(this.centroidsLayer);
            this.addLayer(this.polygonsLayer);
        }
    },

    addCentroidsLayer: function () {
        if (this.centroidsLayer) {
            this.removeLayer(this.centroidsLayer);
        }
        var url = this.options.lotCentroidsUrl;

        var options = {
            serverZooms: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            unique: function (feature) {
                return feature.id;
            }
        };

        this.centroidsLayer = L.lotLayer(url, options, this.lotLayerOptions);
    },

    addPolygonsLayer: function () {
        if (this.polygonsLayer) {
            this.removeLayer(this.polygonsLayer);
        }
        var url = this.options.lotPolygonsUrl;

        var options = {
            maxZoom: 19,
            serverZooms: [16],
            unique: function (feature) {
                return feature.id;
            }
        };

        var layerOptions = L.extend({}, this.lotLayerOptions);
        this.polygonsLayer = L.lotLayer(url, options, layerOptions);
    },

    updateFilters: function (params) {
        this.currentFilters = filters.paramsToFilters(params);
        this.updateDisplayedLots();
        this.fire('filterschanged', this.currentFilters);
    },

    updateDisplayedLots: function () {
        var map = this;
        function updateDisplayedLotsForLayer(layer) {
            if (layer && layer.vectorLayer) {
                // Lots are nested in tiles so we need to do two layers of 
                // eachLayer to get to them all
                layer.vectorLayer.eachLayer(function (tileLayer) {
                    tileLayer.eachLayer(function (lot) {
                        if (filters.lotShouldAppear(lot, map.currentFilters, map.boundariesLayer)) {
                            lot.show();
                        }
                        else {
                            lot.hide();
                        }
                    });
                });
            }
        }

        updateDisplayedLotsForLayer(this.centroidsLayer);
        updateDisplayedLotsForLayer(this.polygonsLayer);
    },

    addUserLayer: function (latlng, opts) {
        opts = opts || {};
        this.userLayer = L.userMarker(latlng, {
            smallIcon: true,
        }).addTo(this);
        if (opts.popupContent) {
            this.userLayer.bindPopup(opts.popupContent).openPopup();
        }
        this.setView(latlng, this.userLocationZoom);
    },

    removeUserLayer: function () {
        if (this.userLayer) {
            this.removeLayer(this.userLayer);
        }
    }
});

L.lotMap = function (id, options) {
    return new L.LotMap(id, options);
};
