(function () {

    function defineTileQueue(L) {
        L.TileQueue = function(callback) {
            this.callback = callback;
        };

        L.TileQueue.prototype = {

            _queue: [],
            _queueTimeout: null,
            
            add: function(aTile) {
                this._queue.push(aTile);
                if (!this._queueTimeout) {
                    this._queueTimeout = setTimeout(L.bind(function(){
                        var time, timeout, start = +new Date, tile;

                        // handle empty elements, see remove
                        do { 
                            tile = this._queue.shift();
                        }
                        while (!tile && this._queue.length > 0);

                        if (tile) {
                            //console.log('adding ' + tile.key + ' ...');

                            this.callback(tile);

                            // pause a percentage of adding time to keep UI responsive
                            time = +new Date - start;
                            timeout = Math.floor(time * 0.3);
                            //console.log('added  ' + tile.key + ' (' + time + 'ms > ' + timeout + 'ms)');
                            this._queueTimeout = setTimeout(L.bind(arguments.callee, this), timeout);
                        } else {
                            this._queueTimeout = null;
                        }
                    }, this), 0);
                }
            },

            remove: function(tile) {
                var key = tile.key, 
                    val;
                for (var i = 0, len = this._queue.length; i < len; i++) {
                    val = this._queue[i];
                    if (val && val.key === key) {
                        //console.log('##### delete ' + key);
                        // set entry to undefined only for better performance (?) - 
                        // queue consumer needs to handle empty entries!
                        delete this._queue[i];
                    }
                }
            },

            clear: function() {
                if (this._queueTimeout) {
                    clearTimeout(this._queueTimeout);
                    this._queueTimeout = null;
                }
                this._queue = [];
            }
        };
    }

    if (typeof define === 'function' && define.amd) {
        // Try to add to Leaflet using AMD
        define(['leaflet'], function (L) {
            defineTileQueue(L);
        });
    }
    else {
        // Else use the global L
        defineTileQueue(L);
    }

})();
