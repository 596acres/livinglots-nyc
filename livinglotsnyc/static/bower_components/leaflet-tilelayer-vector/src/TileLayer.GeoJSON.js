// Load data tiles using the JQuery ajax function

(function () {

    function defineTileLayerGeoJSON(L) {

        L.TileLayer.Ajax = L.TileLayer.extend({
            options: {
                // use L.tileCacheNone to turn caching off
                tileCacheFactory: L.tileCache
            },

            _tileCache: null,

            initialize: function (url, options) {
                L.TileLayer.prototype.initialize.call(this, url, options);
                
                this._tileCache = this.options.tileCacheFactory();
            },

            onAdd: function (map) {
                L.TileLayer.prototype.onAdd.call(this, map);
                this.on('tileunload', this._unloadTile);
            },

            onRemove: function (map) {
                L.TileLayer.prototype.onRemove.call(this, map);
                this.off('tileunload', this._unloadTile);
            },

            _addTile: function(tilePoint, container) {
                var cached = null;
                var key = tilePoint.x + ':' + tilePoint.y;
                var urlZoom = this._getZoomForUrl();
                var tile = cached = this._tileCache.get(key, urlZoom);
                if (!tile) {
                    tile = { key: key, urlZoom: urlZoom, datum: null, loading: true };
                } else {
                    tile.loading = true;
                }

                this._tiles[key] = tile;
                this.fire('tileloadstart', {tile: tile});

                if (cached) {
                    this._addTileData(tile);
                } else {
                    this._loadTile(tile, tilePoint);
                }
            },

            _addTileData: function(tile) {
                // override in subclass
            },

            // XMLHttpRequest handler; closure over the XHR object, the layer, and the tile
            _xhrHandler: function (req, layer, tile) {
                return function() {
                    if (req.readyState != 4) {
                        return;
                    }
                    var s = req.status;

                    // Fire dataload for Leaflet.loading
                    layer._map.fire('dataload');

                    if ((s >= 200 && s < 300) || s == 304) {
                        // check if request is about to be aborted, avoid rare error when aborted while parsing
                        if (tile._request) {
                            tile._request = null;
                            layer.fire('tileresponse', {tile: tile, request: req});
                            tile.datum = req.responseText;
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
                this._adjustTilePoint(tilePoint);
                var layer = this;

                // File dataloading for Leaflet.loading
                layer._map.fire('dataloading');

                var req = new XMLHttpRequest();
                tile._request = req;
                req.onreadystatechange = this._xhrHandler(req, layer, tile);
                this.fire('tilerequest', {tile: tile, request: req});
                req.open('GET', this.getTileUrl(tilePoint), true);
                req.send();
            },

            _unloadTile: function(evt) {
                var tile = evt.tile,
                    req = tile._request;
                if (req) {
                    tile._request = null;
                    req.abort();
                    this.fire('tilerequestabort', {tile: tile, request: req});
                }
            }
        });


        L.TileLayer.Vector = L.TileLayer.Ajax.extend({
            options: {
                // factory function to create the vector tile layers (defaults to L.GeoJSON)
                layerFactory: L.geoJson,
                // factory function to create a web worker for parsing/preparing tile data
                workerFactory: L.communistWorker
                //workerFactory: L.noWorker
            },

            initialize: function (url, options, vectorOptions) {
                L.TileLayer.Ajax.prototype.initialize.call(this, url, options);
                this.vectorOptions = vectorOptions || {};
                this._worker = this.options.workerFactory(L.TileLayer.Vector.parseData);
                this._addQueue = new L.TileQueue(L.bind(this._addTileDataInternal, this));
            },

            onAdd: function (map) {
                this._map = map;
                
                L.TileLayer.Ajax.prototype.onAdd.call(this, map);

                // root vector layer, contains tile vector layers as children 
                this.vectorLayer = this._createVectorLayer(); 
                map.addLayer(this.vectorLayer);

                this._worker.onAdd(map);
                this._tileCache.onAdd(map);
            },

            onRemove: function (map) {
                // unload tiles (L.TileLayer only calls _reset in onAdd)
                this._reset();
                map.removeLayer(this.vectorLayer);

                L.TileLayer.Ajax.prototype.onRemove.call(this, map);

                this._worker.onRemove(map);
                this._tileCache.onRemove(map);

                this.vectorLayer = null;
                this._map = null;
            },

            _createVectorLayer: function() {
                return this.options.layerFactory(null, this.vectorOptions);
            },

            _createTileLayer: function() {
                return this._createVectorLayer();
            },

            _addTileData: function(tile) {
                if (!tile.parsed) {
                    this._worker.process(tile, L.bind(function(tile) {
                        this._addQueue.add(tile);
                    },this));
                } else {
                    // from cache
                    this._addQueue.add(tile);
                }
            },

            _addTileDataInternal: function(tile) {
                var tileLayer = this._createTileLayer();
                if (!tile.parsed) {
                    // when no worker for parsing
                    tile.parsed = L.TileLayer.Vector.parseData(tile.datum);
                    tile.datum = null;
                }
                tileLayer.addData(tile.parsed);
                tile.layer = tileLayer;
                this.vectorLayer.addLayer(tileLayer);

                tile.loading = false;
                this.fire('tileload', {tile: tile});
                this._tileLoaded();
            },

            _unloadTile: function(evt) {
                L.TileLayer.Ajax.prototype._unloadTile.apply(this, arguments);

                var tile = evt.tile,
                    tileLayer = tile.layer;
                if (tile.loading) {
                    this._addQueue.remove(tile);
                    // not from cache or not loaded and parsed yet
                    if (!tile.parsed) {
                        this._worker.abort(tile);
                    }
                    this.fire('tileabort', {tile: tile});
                    this._tileLoaded();
                }
                if (tileLayer && this.vectorLayer.hasLayer(tileLayer)) {
                    if (this._shouldRemoveLayersAtZoom(this._map.getZoom())) {
                        this.vectorLayer.removeLayer(tileLayer);
                    }
                }

                if (tile.parsed) {
                    this._tileCache.put(tile);
                }
            },

            _shouldRemoveLayersAtZoom: function(zoom) {
                return true;
            },

            _retainTiles: function() {
                return {};
            },

            _reset: function(e) {
                var tilesToRetain = this._retainTiles();

                L.TileLayer.Ajax.prototype._reset.apply(this, arguments);

                // Restore useful tiles
                L.extend(this._tiles, tilesToRetain);

                this._addQueue.clear();
                this._worker.clear();
            }
        });


        L.extend(L.TileLayer.Vector, {
            parseData: function(data) {
                return JSON.parse(data);
            }
        });
    }

    if (typeof define === 'function' && define.amd) {
        // Try to add to Leaflet using AMD
        define(['leaflet', 'CommunistWorker', 'TileCache', 'TileQueue'], function (L) {
            defineTileLayerGeoJSON(L);
        });
    }
    else {
        // Else use the global L
        defineTileLayerGeoJSON(L);
    }

})();
