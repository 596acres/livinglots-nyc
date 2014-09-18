/**
 * Simple tile cache to keep tiles while zooming with overzoom
 */

(function () {

    function defineTileCache(L) {
        L.TileCache = function() {
        };

        L.TileCache.prototype = {
            // cache key: tile (String: Object)
            _cache: {},

            // flag to determine switch between tile unloading (put) and loading (get) phase
            _unloading: false,

            // flag to only cache tiles when zooming, not when moving
            _zooming: false,

            onAdd: function(map) {
                this._map = map;
                
                map.on('zoomstart', this._onZoomStart, this);
                map.on('zoomend', this._onZoomEnd, this);
            },

            onRemove: function(map) {
                this._map = null;

                map.off('zoomstart', this._onZoomStart, this);
                map.off('zoomend', this._onZoomEnd, this);
            },

            _onZoomStart: function(evt) {
                this._zooming = true;
            },

            _onZoomEnd: function(evt) {
                this._zooming = false;
            },

            get: function(key, urlZoom) {
                var ckey = this._getCacheKey(key, urlZoom);
                var tile = this._cache[ckey];
                this._unloading = false;
                //console.log('cache ' + (tile ? 'hit ' : 'miss') + ': ' + ckey);
                return tile;
            },
            
            put: function(tile) {
                if (!this._zooming) return;

                if (!this._unloading) {
                    // clear old entries before adding newly removed tiles after zoom or move
                    this.clear();
                    this._unloading = true;
                }

                var ckey = this._getCacheKeyFromTile(tile);
                if (!(ckey in this._cache)) {
                    // vector layer is recreated because of feature filter
                    delete tile.layer;
                    this._cache[ckey] = tile;
                    //console.log('cache put : ' + ckey + ' (' + Object.keys(this._cache).length + ')');
                }
            },
            
            clear: function() {
                //console.log('cache clear');
                this._cache = {};
            },

            _getCacheKeyFromTile: function(tile) {
                return this._getCacheKey(tile.key, tile.urlZoom);
            },

            _getCacheKey: function(key, urlZoom) {
                return urlZoom + ':' + key
            }
        };

        L.tileCache = function() {
            return new L.TileCache();
        };

        // dummy impl. to turn caching off
        L.tileCacheNone = function() {
            return {
                onAdd: function(map) {},
                onRemove: function(map) {},
                get: function(key, urlZoom) {},
                put: function(tile) {},
                clear: function() {}
            };
        };
    }

    if (typeof define === 'function' && define.amd) {
        // Try to add to Leaflet using AMD
        define(['leaflet'], function (L) {
            defineTileCache(L);
        });
    }
    else {
        // Else use the global L
        defineTileCache(L);
    }

})();
