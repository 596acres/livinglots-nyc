define(
    [
        'django',
        'leaflet',
        'map.styles',

        'leaflet.bing',
        'leaflet.dataoptions',
        'leaflet.handlebars',
        'leaflet.hash',
        'leaflet.lotlayer',
        'leaflet.lotmarker',
        'leaflet.usermarker'
    ], function (Django, L, mapstyles) {

        L.LotMap = L.Map.extend({

            boundariesLayer: null,
            centroidsLayer: null,
            polygonsLayer: null,
            lotLayerTransitionPoint: 15,
            previousZoom: null,
            userLayer: null,
            userLocationZoom: 16,

            lotLayerOptions: {
                onEachFeature: function (feature, layer) {
                    layer.on({
                        'click': function (layer) {
                            var latlng = layer.latlng,
                                x = this._map.latLngToContainerPoint(latlng).x,
                                y = this._map.latLngToContainerPoint(latlng).y - 100,
                                point = this._map.containerPointToLatLng([x, y]);
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
                    if (feature.properties.has_organizers) {
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
                    style.fillColor = mapstyles[feature.properties.layer];
                    if (!style.fillColor) {
                        style.fillColor = '#000000';
                    }
                    return style;
                },
                popupOptions: {
                    autoPan: false,
                    maxWidth: 250,
                    minWidth: 250,
                    offset: [0, 0]
                },
                handlebarsTemplateSelector: '#popup-template',
                getTemplateContext: function (layer) {
                    if (!layer.feature) {
                        throw 'noFeatureForContext';
                    }
                    return {
                        detailUrl: Django.url('lots:lot_detail', {
                            pk: layer.feature.id
                        }),
                        feature: layer.feature
                    };
                }
            },

            initialize: function (id, options) {
                L.Map.prototype.initialize.call(this, id, options);
                this.addBaseLayer();
                var hash = new L.Hash(this);

                this.boundariesLayer = L.geoJson(null, {
                    color: '#58595b',
                    fill: false
                }).addTo(this);

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
            },

            addBaseLayer: function () {
                var cloudmade = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                    key: this.options.apikey,
                    styleId: this.options.styleid
                }).addTo(this);

                var bing = new L.BingLayer('Ajio1n0EgmAAvT3zLndCpHrYR_LHJDgfDU6B0tV_1RClr7OFLzy4RnkLXlSdkJ_x');

                L.control.layers({
                    streets: cloudmade,
                    satellite: bing
                }).addTo(this);
            },

            addLotsLayer: function (params) {
                this.addCentroidsLayer(params);
                this.addPolygonsLayer(params);
                if (this.getZoom() <= this.lotLayerTransitionPoint) {
                    this.addLayer(this.centroidsLayer);
                    this.removeLayer(this.polygonsLayer);
                }
                else {
                    this.removeLayer(this.centroidsLayer);
                    this.addLayer(this.polygonsLayer);
                }
            },

            addCentroidsLayer: function (params) {
                if (this.centroidsLayer) {
                    this.removeLayer(this.centroidsLayer);
                }
                var url = this.options.lotCentroidsUrl + '?' + $.param(params);

                var options = {
                    serverZooms: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    unique: function (feature) {
                        return feature.id;
                    }
                };

                this.centroidsLayer = L.lotLayer(url, options, this.lotLayerOptions);
            },

            addPolygonsLayer: function (params) {
                if (this.polygonsLayer) {
                    this.removeLayer(this.polygonsLayer);
                }
                var url = this.options.lotPolygonsUrl + '?' + $.param(params);

                var options = {
                    serverZooms: [16],
                    unique: function (feature) {
                        return feature.id;
                    }
                };

                var layerOptions = L.extend({}, this.lotLayerOptions);
                this.polygonsLayer = L.lotLayer(url, options, layerOptions);
            },

            updateDisplayedLots: function (params) {
                this.removeLayer(this.centroidsLayer);
                this.removeLayer(this.polygonsLayer);
                this.addLotsLayer(params);
            },

            addUserLayer: function (latlng) {
                this.userLayer = L.userMarker(latlng, {
                    smallIcon: true,
                }).addTo(this);
                this.setView(latlng, this.userLocationZoom);
            },

            removeUserLayer: function () {
                if (this.userLayer) {
                    this.removeLayer(this.userLayer);
                }
            },

            removeBoundaries: function (data, options) {
                this.boundariesLayer.clearLayers();
            },

            updateBoundaries: function (data, options) {
                this.boundariesLayer.clearLayers();
                this.boundariesLayer.addData(data);
                if (options.zoomToBounds) {
                    this.fitBounds(this.boundariesLayer.getBounds());
                }
            }

        });

        L.lotMap = function (id, options) {
            return new L.LotMap(id, options);
        };

    }
);
