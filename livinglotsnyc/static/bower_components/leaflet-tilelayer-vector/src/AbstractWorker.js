
(function () {

    function defineAbstractWorker(L) {
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
    }

    if (typeof define === 'function' && define.amd) {
        // Try to add to Leaflet using AMD
        define(['leaflet'], function (L) {
            defineAbstractWorker(L);
        });
    }
    else {
        // Else use the global L
        defineAbstractWorker(L);
    }

})();
