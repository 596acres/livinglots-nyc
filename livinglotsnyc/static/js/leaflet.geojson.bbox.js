define(
    [
       'leaflet',

       'TileLayer.GeoJSON',
    ], function (L) {

        L.TileLayer.Vector.include({

            getTileUrl: function (coords) {
                var x = coords.x,
                    y = coords.y,
                    z = this._getZoomForUrl(),
                    bounds = this.getTileBBox(x, y, z);
                if (this._url.indexOf('?') < 0) {
                    this._url += '?';
                }
                return this._url + '&bbox=' + bounds.toBBoxString();
            },

            getTileBBox: function (x, y, z) {
                var west = this.getTileLng(x, z),
                    north = this.getTileLat(y, z),
                    east = this.getTileLng(x + 1, z),
                    south = this.getTileLat(y + 1, z),
                    bounds = L.latLngBounds([[south, west], [north, east]]);
                return bounds;
            },

            getTileLng: function (x, z) {
                return (x / Math.pow(2, z) * 360 - 180);
            },

            getTileLat: function (y, z) {
                var n = Math.PI - 2 * Math.PI * y / Math.pow(2, z);
                return (180 / Math.PI * Math.atan(0.5 * (Math.exp(n) - Math.exp(-n))));
            }

        });

    }
);
