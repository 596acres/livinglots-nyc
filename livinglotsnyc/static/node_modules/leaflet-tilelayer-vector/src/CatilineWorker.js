var catiline = require('catiline');
var L = require('leaflet');

L.CatilineWorker = L.AbstractWorker.extend({

    statics: {
        // number of web workers, not using web workers when falsy
        NUM_WORKERS: 2
    },

    initialize: function (workerFunc) {
        this.workerFunc = workerFunc;
    },

    onAdd: function (map) {
        this._workers = L.CatilineWorker.createWorkers(this.workerFunc);
    },

    onRemove: function (map) {
        if (this._workers) {
            // TODO do not close when other layers are still using the static instance
            //this._workers.close();
        }
    },

    process: function(tile, callback) {
        if (this._workers){ 
            tile._worker = this._workers.data(tile.datum).then(function(parsed) {
                if (tile._worker) {
                    tile._worker = null;
                    tile.parsed = parsed;
                    tile.datum = null;
                    callback(tile);
                } else {
                    // tile has been unloaded, don't continue with adding
                    //console.log('worker aborted ' + tile.key);
                }
            });
        } else {
            callback(tile);
        }
    },
    
    abort: function(tile) {
        if (tile._worker) {
            // TODO abort worker, would need to recreate after close
            //tile._worker.close();
            tile._worker = null;
        }
    }
});

L.catilineWorker = function (workerFunc) {
    return new L.CatilineWorker(workerFunc);
};

L.extend(L.CatilineWorker, {
    createWorkers: function(workerFunc) {
        if ( L.CatilineWorker.NUM_WORKERS && typeof Worker === "function" && typeof catiline === "function"
                && !("workers" in L.CatilineWorker)) {
            L.CatilineWorker.workers = catiline({
                //data : L.TileLayer.Vector.parseData
                data : workerFunc
            }, L.CatilineWorker.NUM_WORKERS);
        }
        return L.CatilineWorker.workers;
    }
});
