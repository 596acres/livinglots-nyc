var L = require('leaflet');

require('leaflet-tilelayer-vector');

L.TileLayer.Vector.include({

    getTileUrl: function (coords) {
        var x = coords.x,
            y = coords.y,
            z = this._getZoomForUrl(),
            url = L.Util.template(this._url, { s: this._getSubdomain(coords) });
        return url + z + '/' + x + '/' + y + '.geojson';
    }

});
