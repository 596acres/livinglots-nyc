define(['leaflet', 'leaflet.lotpath'], function (L) {
    L.LotPolygon = L.Polygon.extend({

        _pickOpacity: function (zoom) {
            if (zoom >= 18) {
                return 0.65;
            }
            if (zoom >= 17) {
                return 0.85;
            }
            return 1;
        },

        _updatePath: function () {
            // Update opacity
            this.options.fillOpacity = this._pickOpacity(this._map.getZoom());
            this._updateStyle();

            this.updateActionPathScale();
            L.Polygon.prototype._updatePath.call(this);
        }

    });

    L.LotPolygon.include(L.LotPathMixin);

    L.LotPolygon.addInitHook(function () {
        this.on({
            'add': function () {
                this.initActionPath();
            }
        });
    });

    L.lotPolygon = function (latlngs, options) {
        return new L.LotPolygon(latlngs, options);
    };

});
