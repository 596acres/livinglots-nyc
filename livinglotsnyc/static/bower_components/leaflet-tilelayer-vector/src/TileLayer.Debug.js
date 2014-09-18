/*
 * Debug layer for L.TileLayer.Vector
 */
L.TileLayer.Debug = L.TileLayer.Div.extend({
    initialize: function (vectorLayer) {
        L.TileLayer.Div.prototype.initialize.call(this, vectorLayer.options);

        this.vectorLayer = vectorLayer;
    },

    onAdd: function (map) {
        map.on('viewreset', this._updateZoom, this);
        this.vectorLayer.on('tileload', this._onTileLoad, this);
        this.vectorLayer.on('tileerror', this._onTileLoad, this);
        L.TileLayer.Div.prototype.onAdd.apply(this, arguments);
    },

    onRemove: function (map) {
        L.TileLayer.Div.prototype.onRemove.apply(this, arguments);
        this.vectorLayer.off('tileload', this._onTileLoad, this);
        this.vectorLayer.off('tileerror', this._onTileLoad, this);
        map.off('viewreset', this._updateZoom, this);
    },

    drawTile: function (tile, tilePoint) {
        tile.style.backgroundColor = 'rgba(128, 128, 128, 0.3)';
        tile.style.border = '1px solid rgba(128, 128, 128, 0.8)';
    },

    _updateZoom: function() {
        if (this.options.tileSize != this.vectorLayer.options.tileSize) {
            this.options.tileSize = this.vectorLayer.options.tileSize;
            this.options.zoomOffset = this.vectorLayer.options.zoomOffset;
        }
    },

    _onTileLoad: function(evt) {
        var key = evt.tile.key,
            tile = this._tiles[key];
        if (tile) {
            
        }
    }
});

