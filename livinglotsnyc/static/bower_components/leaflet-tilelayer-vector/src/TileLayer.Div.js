L.TileLayer.Div = L.TileLayer.extend({

    initialize: function (options) {
        L.TileLayer.prototype.initialize.call(this, null, options);
    },

    _createTile: function () {
        var tile = L.DomUtil.create('div', 'leaflet-tile leaflet-tile-loaded');
        var tileSize = this._getTileSize();
        tile.style.width = tileSize + 'px';
        tile.style.height = tileSize + 'px';
        tile.onselectstart = tile.onmousemove = L.Util.falseFn;
        return tile;        
    },

    _loadTile: function (tile, tilePoint) {
        tile._layer = this;
        tile._tilePoint = tilePoint;
        this._adjustTilePoint(tilePoint);
        
        this.drawTile(tile, tilePoint);
        
        this._tileLoaded();
    },
    
    drawTile: function (tile, tilePoint) {
        // override with rendering code
    }
});
