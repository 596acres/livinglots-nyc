// XHR for binary data (responseType arraybuffer)
// TODO add as option to L.TileLayer.Ajax? 
L.TileLayer.Ajax.include({
    // XMLHttpRequest handler; closure over the XHR object, the layer, and the tile
    _xhrHandler: function (req, layer, tile) {
        return function() {
            if (req.readyState != 4) {
                return;
            }
            var s = req.status;
            // status 0 + response check for file:// URLs
            if (((s >= 200 && s < 300) || s == 304) || (s == 0 && req.response)) {
                // check if request is about to be aborted, avoid rare error when aborted while parsing
                if (tile._request) {
                    tile._request = null;
                    layer.fire('tileresponse', {tile: tile, request: req});
                    tile.datum = req.response;
                    layer._addTileData(tile);
                }
            } else {
                tile.loading = false;
                tile._request = null;
                layer.fire('tileerror', {tile: tile, request: req});
                layer._tileLoaded();                
            }
        }
    },
    // Load the requested tile via AJAX
    _loadTile: function (tile, tilePoint) {
        var layer = this;
        var req = new XMLHttpRequest();
        tile._request = req;
        req.onreadystatechange = this._xhrHandler(req, layer, tile);
        this.fire('tilerequest', {tile: tile, request: req});
        req.open('GET', this.getTileUrl(tilePoint), true);
        req.responseType = 'arraybuffer';
        req.send();
    }
});

L.extend(L.TileLayer.Vector, {
    parseData: function(data) {
        //return layer.buildFeatures(data);
        return data;
    }
});
    