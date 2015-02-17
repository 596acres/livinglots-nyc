var L = require('leaflet');

L.AbstractWorker = L.Class.extend({
    initialize: function () {
    },

    onAdd: function (map) {
    },

    onRemove: function (map) {
    },

    process: function(tile, callback) {
        callback(tile);
    },
    
    abort: function(tile) {
    },
    
    clear: function() {
    }
});

// dummy worker (= no worker) when used directly
L.noWorker = function () {
    return new L.AbstractWorker();
};
