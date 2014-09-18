(function () {

    function defineOverzoom(L) {
        L.TileLayer.Overzoom = {
            
            overzoomOptions: {
                // List of available server zoom levels in ascending order. Empty means all  
                // client zooms are available (default). Allows to only request tiles at certain
                // zooms and resizes tiles on the other zooms.
                serverZooms: [],
                // workaround: wrapping loads tiles multiple times when zoom < serverZooms[0]
                noWrap: true
            },

            // override _getTileSize to add serverZooms (when maxNativeZoom is not defined)
            _getTileSize: function() {
                var map = this._map,
                    options = this.options,
                    zoom = map.getZoom() + options.zoomOffset,
                    zoomN = options.maxNativeZoom || this._getServerZoom(zoom);

                // increase tile size when overscaling
                //return zoomN && zoom > zoomN ?
                var tileSize = zoomN && zoom !== zoomN ?
                    Math.round(map.getZoomScale(zoom) / map.getZoomScale(zoomN) * options.tileSize) :
                    options.tileSize;

                //console.log('tileSize = ' + tileSize + ', zoomOffset = ' + this.options.zoomOffset + ', serverZoom = ' + zoomN + ', zoom = ' + zoom);
                return tileSize;
            },

            _getZoomForUrl: function () {
                var zoom = L.TileLayer.prototype._getZoomForUrl.call(this);
                var result = this._getServerZoom(zoom);
                //console.log('zoomForUrl = ' + result);
                return result;
            },

            // Returns the appropriate server zoom to request tiles for the current zoom level.
            // Next lower or equal server zoom to current zoom, or minimum server zoom if no lower 
            // (should be restricted by setting minZoom to avoid loading too many tiles).
            _getServerZoom: function(zoom) {
                var serverZooms = this.options.serverZooms || [],
                    result = zoom;
                // expects serverZooms to be sorted ascending
                for (var i = 0, len = serverZooms.length; i < len; i++) {
                    if (serverZooms[i] <= zoom) {
                        result = serverZooms[i];
                    } else {
                        if (i === 0) {
                            // zoom < smallest serverZoom
                            result = serverZooms[0];
                        }
                        break;
                    }
                }
                return result;
            },

            _shouldRemoveLayersAtZoom: function(zoom) {
                if (this.options.serverZooms) {
                    if (this._map.getZoom() in this.options.serverZooms) {
                        return true;
                    }
                    else {
                        return false;
                    }
                }
                return true;
            },

            // Only keep the tiles that are going to be useful on the map's current zoom
            _retainTiles: function() {
                var tiles = L.extend({}, this._tiles),
                    zoom = this._getServerZoom(this._map.getZoom());

                for (var key in tiles) {
                    // Do not retain tiles that won't be used at this zoom
                    if (tiles[key].urlZoom !== zoom) {
                        delete tiles[key];
                    }

                    // Do not retain tiles that don't have a layer. They might
                    // have been interrupted from loading that layer because the
                    // user zoomed in or out very quickly, for example.
                    if (!tiles[key] || !tiles[key].layer) {
                        delete tiles[key];
                    }
                }
                return tiles;
            }
        };

        if (typeof L.TileLayer.Vector !== 'undefined') {
            L.TileLayer.Vector.include(L.TileLayer.Overzoom);
            L.TileLayer.Vector.mergeOptions(L.TileLayer.Overzoom.overzoomOptions);
        }

        if (typeof L.TileLayer.Div !== 'undefined') {
            L.TileLayer.Div.include(L.TileLayer.Overzoom);
            L.TileLayer.Div.mergeOptions(L.TileLayer.Overzoom.overzoomOptions);
        }
    }

    if (typeof define === 'function' && define.amd) {
        // Try to add to Leaflet using AMD
        define(['leaflet', 'TileLayer.GeoJSON'], function (L) {
            defineOverzoom(L);
        });
    }
    else {
        // Else use the global L
        defineOverzoom(L);
    }

})();
