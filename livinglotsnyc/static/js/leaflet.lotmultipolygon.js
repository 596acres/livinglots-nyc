define(['leaflet', 'leaflet.lotpolygon'], function (L) {
    L.LotMultiPolygon = L.FeatureGroup.extend({

        initialize: function (latlngs, options) {
            this._layers = {};
            this._options = options;
            this.setLatLngs(latlngs);
        },

        setLatLngs: function (latlngs) {
            var i = 0,
                len = latlngs.length;

            this.eachLayer(function (layer) {
                if (i < len) {
                    layer.setLatLngs(latlngs[i++]);
                } else {
                    this.removeLayer(layer);
                }
            }, this);

            while (i < len) {
                this.addLayer(new L.LotPolygon(latlngs[i++], this._options));
            }

            return this;
        },

        getLatLngs: function () {
            var latlngs = [];

            this.eachLayer(function (layer) {
                latlngs.push(layer.getLatLngs());
            });

            return latlngs;
        }
    });
});
