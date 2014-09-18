/*
 * Loading progress info layer for L.TileLayer.Vector
 */
L.TileLayer.Progress = L.TileLayer.Div.extend({
    _adding: false,

    /* key hash of vector tiles currently loading {String: true} */
    _loadingTiles: {},
    
    initialize: function (vectorLayer) {
        L.TileLayer.Div.prototype.initialize.call(this, vectorLayer.options);

        this.vectorLayer = vectorLayer;
    },

    onAdd: function (map) {
        this._adding = true;
        map.on('layerremove', this._onVecRemove, this);
        this.vectorLayer.on('tileloadstart', this._onTileLoading, this);
        this.vectorLayer.on('tileload', this._onTileLoad, this);
        this.vectorLayer.on('tileerror', this._onTileError, this);
        this.vectorLayer.on('tileunload', this._onTileLoad, this);
        L.TileLayer.Div.prototype.onAdd.apply(this, arguments);
        this._adding = false;
    },

    onRemove: function (map) {
        L.TileLayer.Div.prototype.onRemove.apply(this, arguments);
        this._loadingTiles = {};
        this.vectorLayer.off('tileloadstart', this._onTileLoading, this);
        this.vectorLayer.off('tileload', this._onTileLoad, this);
        this.vectorLayer.off('tileerror', this._onTileError, this);
        this.vectorLayer.off('tileunload', this._onTileLoad, this);
    },

    drawTile: function (tile, tilePoint) {
        var vecTile, 
            loading, 
            key = tilePoint.x + ':' + tilePoint.y;

        tile.style.backgroundColor = 'rgba(128, 128, 128, 0.3)';
        tile.style.border = '1px solid rgba(128, 128, 128, 0.8)';
        tile.style.boxSizing = 'border-box';

        if (!this._loadingTiles[key]) {
            this._hide(tile);
        }

        // check for already loading tiles, because initial tileloadstart
        // events might have been missed when layer is added
        if (this._adding) {
            vecTile = this.vectorLayer._tiles[key];
            loading = vecTile && vecTile.loading;
            if (loading) {
                this._show(tile);
            }
        }
    },

    _onVecRemove: function(evt) {
        if (evt.layer === this.vectorLayer) {
            this._hideAll();
        }
    },

    _hideAll: function() {
        for (var key in this._tiles) {
            var tile = this._tiles[key];
            this._hide(tile);
        }
    },

    _onTileLoading: function(evt) {
        var key = evt.tile.key,
            tile = this._tiles[key];
        if (tile) {
            this._show(tile);
        } else {
            this._loadingTiles[key] = true;
        }
    },

    _onTileLoad: function(evt) {
        var key = evt.tile.key,
            tile = this._tiles[key];
        this._hide(tile);
        delete this._loadingTiles[key];
    },

    _onTileError: function(evt) {
        var key = evt.tile.key,
            tile = this._tiles[key];
        if (tile) {
            tile.style.backgroundColor = 'rgba(128, 128, 128, 0.7)';
            tile.style.border = 'none';
        }
        delete this._loadingTiles[key];
    },
    
    _show: function(tile) {
        if (tile) {
            tile.classList.add('leaflet-tile-loaded');
        }
    },
    
    _hide: function(tile) {
        if (tile) {
            tile.classList.remove('leaflet-tile-loaded');
        }
    }
});

