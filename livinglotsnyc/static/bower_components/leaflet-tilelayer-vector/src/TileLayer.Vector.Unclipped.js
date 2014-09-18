/*
 * Tile layer for unclipped vector tiles where features spanning multiple tiles are contained with
 * their full geometry in each tile (as opposed to clipping geometries at tile boundary).
 * 
 * This layer loads such duplicated features only once by using a 'unique' function given in the options
 * to identify identical features and to keep track of the tiles that are referencing the same feature.
 * 
 * Uses a filter to remove duplicates, so a vector layer set with options.layerFactory must support 
 * feature filtering like in L.GeoJSON.
 */
L.TileLayer.Vector.Unclipped = L.TileLayer.Vector.extend({
    // hash: unique featureKey -> number of tiles referencing the feature
    featureRefCounts: {},
    // hash: unique featureKey -> feature layer
    commonFeatures: {},

    initialize: function (url, options, vectorOptions) {
        L.TileLayer.Vector.prototype.initialize.apply(this, arguments);

        if (!options || !options.unique) {
            console.warn('"unique" function missing in options, deduplicating disabled');
        }
    },

    _createTileLayer: function() {
        var tileLayer = L.TileLayer.Vector.prototype._createTileLayer.apply(this, arguments);
        if (this.options.unique) {
            if (tileLayer.options.filter) {
                tileLayer.options.filter = this._andFilter(tileLayer.options.filter, L.bind(this._filterDuplicates, tileLayer));
            } else {
                tileLayer.options.filter = L.bind(this._filterDuplicates, tileLayer);
            }
            tileLayer._tilingLayer = this;
            // common features this tile is referencing (array of unique feature keys)
            tileLayer._featureRefs = [];
        }
        return tileLayer;
    },

    // filter out duplicate features that are contained in multiple tiles
    // (true keeps, false discards feature)
    _filterDuplicates: function(feature) {
        var featureKey = this._tilingLayer.options.unique(feature);
        var refs = this._tilingLayer.featureRefCounts[featureKey];

        if (refs && refs > 0) {
            refs++;
            this._featureRefs.push(featureKey);
        } else {
            refs = 1;
        }
        this._tilingLayer.featureRefCounts[featureKey] = refs;

        return refs <= 1;
    },
    
    _andFilter: function(filterA, filterB) {
        return function(feature) {
            return filterA(feature) && filterB(feature);
        };
    },
    
    _unloadTile: function(evt) {
        var tileLayer = evt.tile.layer;
        if (tileLayer) {
            if (this.options.unique) {
                this._clearFeatureLayers(tileLayer);
                this._clearCommonFeatureLayers(tileLayer);
            }
        }        
        L.TileLayer.Vector.prototype._unloadTile.apply(this, arguments);
    },
    
    // Remove feature layers from the given tile layer and
    // decrease reference counter for all features of the tile. 
    _clearFeatureLayers: function(tileLayer) {
        tileLayer.eachLayer(function (layer) {
            if (layer.feature) {
                var featureKey = this.options.unique(layer.feature);
                var refs = this._decreaseFeatureRefCount(featureKey);
                if (refs > 0) {
                    // referenced by other tiles, keep feature (move to root vector layer)
                    this.vectorLayer.addLayer(layer);
                    this.commonFeatures[featureKey] = layer;

                    // from removeLayer: remove layer from tileLayer but not from map (not sure if necessary)
                    var id = L.stamp(layer);
                    delete tileLayer._layers[id];
                } else {
                    tileLayer.removeLayer(layer);
                }
            }
        }, this);
    },

    // Remove common features that are only referenced by the given tile
    _clearCommonFeatureLayers: function(tileLayer) {
        var featureRefs = tileLayer._featureRefs;
        for (i = 0, len = featureRefs.length; i < len; i++) {
            var featureKey = featureRefs[i];
            var refs = this._decreaseFeatureRefCount(featureKey);
            if (refs <= 0) {
                var layer = this.commonFeatures[featureKey];
                if (layer) {
                    this.vectorLayer.removeLayer(layer);
                }
            }
        }
    },

    _decreaseFeatureRefCount: function(featureKey) {
        var refs = --this.featureRefCounts[featureKey];
        if (refs <= 0) {
            delete this.featureRefCounts[featureKey];
        }
        return refs;
    }
});
