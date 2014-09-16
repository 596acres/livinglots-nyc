define(['leaflet', 'leaflet.lotpath'], function (L) {
    L.LotMarker = L.CircleMarker.extend({

        onZoomEnd: function () {
            if (this._map && this.feature.properties.has_organizers) {
                this.bringToFront();
            }
        },

        _pickRadius: function (zoom) {
            var radius = 4;   
            if (zoom >= 13) {
                radius = 6;
            }
            if (zoom >= 14) {
                radius = 9;
            }
            if (zoom >= 15) {
                radius = 12;
            }
            if (zoom >= 16) {
                radius = 15;
            }
            return radius;
        },

        _updatePath: function () {
            var zoom = this._map.getZoom();

            // Update the circle's radius according to the map's zoom level
            this.options.radius = this._radius = this._pickRadius(zoom);

            this.updateActionPathScale();
            L.CircleMarker.prototype._updatePath.call(this);
        }

    });

    L.LotMarker.include(L.LotPathMixin);

    L.LotMarker.addInitHook(function () {
        this.on({
            'add': function () {
                this.initActionPath();

                if (this.feature && this.feature.properties.has_organizers) {
                    var layer = this;
                    this._map.on('zoomend', this.onZoomEnd, layer);
                }
            },
            'remove': function () {
                if (this.feature && this.feature.properties.has_organizers) {
                    var layer = this;
                    this._map.off('zoomend', this.onZoomEnd, layer);
                }
            }
        });
    });

    L.lotMarker = function (latlng, options) {
        return new L.LotMarker(latlng, options);
    };

});
