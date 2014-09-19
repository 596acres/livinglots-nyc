var L = require('leaflet');

require('TileLayer.GeoJSON');

L.TileLayer.Vector.include({

    getTileUrl: function (coords) {
        var x = coords.x,
            y = coords.y,
            z = this._getZoomForUrl();
        return this._url + z + '/' + x + '/' + y + '.geojson';
    }

});
