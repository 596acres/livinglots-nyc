var L = require('leaflet');

require('leaflet-tilelayer-vector');

L.TileLayer.Vector.include({

    getTileUrl: function (coords) {
        var x = coords.x,
            y = coords.y,
            z = this._getZoomForUrl();
        return this._url + z + '/' + x + '/' + y + '.geojson';
    }

});
