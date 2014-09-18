L.TileLayer.Vector.Debug = L.TileLayer.Vector.extend({
    
    _requestCount: 0,

    onAdd: function (map) {
        this.on('tilerequest', this._onTileRequest, this);
        this.on('tileresponse', this._onTileResponse, this);
        this.on('tilerequestabort', this._onTileRequestAbort, this);
        this.on('tileload', this._onTileLoad, this);
        this.on('tileunload', this._onTileUnload, this);
        map.on('moveend', this._onMoveend, this);
        L.TileLayer.Vector.prototype.onAdd.apply(this, arguments);
    },

    onRemove: function (map) {
        L.TileLayer.Vector.prototype.onRemove.apply(this, arguments);
        this.off('tilerequest', this._onTileRequest, this);
        this.off('tileresponse', this._onTileResponse, this);
        this.off('tilerequestabort', this._onTileRequestAbort, this);
        this.off('tileload', this._onTileLoad, this);
        this.off('tileunload', this._onTileUnload, this);
        map.off('moveend', this._onMoveend, this);
    },

    _onTileRequest: function(evt) {
        var tile = evt.tile;
        this._requestCount++;
        console.log('request-start: ' + tile.key + ' - ' + this._requestCount);
    },

    _onTileResponse: function(evt) {
        var tile = evt.tile;
        this._requestCount--;
        console.log('request-end  : ' + tile.key + ' - ' + this._requestCount);
    },

    _onTileRequestAbort: function(evt) {
        var tile = evt.tile;
        this._requestCount--;
        console.log('request-abort: ' + tile.key + ' - ' + this._requestCount);
    },

    _onTileLoad: function(evt) {
        var tile = evt.tile,
            layer = tile.layer,
            tileSize = this.options.tileSize,
            kx = +tile.key.split(':')[0],
            ky = +tile.key.split(':')[1],
            tilePoint = new L.Point(kx, ky),
            x, y, z, 
            nwPoint = tilePoint.multiplyBy(tileSize),
            sePoint = nwPoint.add(new L.Point(tileSize, tileSize)),
            nw = this._map.unproject(nwPoint),
            se = this._map.unproject(sePoint),
            latLngBounds = L.latLngBounds(nw, se),
            tilePos = this._getTilePos(tilePoint),
            lBounds, textEle, textNode, text;
            
        console.log('loaded       : ' + tile.key);

        this._adjustTilePoint(tilePoint);
        x = tilePoint.x;
        y = tilePoint.y;
        z = tilePoint.z;
                
        lBounds = L.rectangle(latLngBounds, {
                weight: 1,
                //stroke: false,
                //dashArray: '8, 8',
                color: 'red',
                opacity: 0.5,
                fill: false,
                //fillOpacity: 0.5,
                clickable: false
        });
        layer.addLayer(lBounds);
        //lBounds._path.setAttribute('shape-rendering', 'crispEdges');
        //lBounds._path.setAttribute('stroke-linejoin', 'miter');
        //lBounds._path.setAttribute('stroke-linecap', 'square');

        textEle = lBounds._createElement('text');
        textEle.setAttribute('x', tilePos.x);
        textEle.setAttribute('y', tilePos.y);
        textEle.setAttribute('dx', '0.5em');
        textEle.setAttribute('dy', '1.5em');
        textEle.setAttribute('style', 'fill: red; font-family: "Lucida Console", Monaco, monospace;');

        text = z + '/' + x + '/' + y + '  ' + '(zoom ' + layer._map.getZoom() + ', key ' + tile.key + ')';
        textNode = document.createTextNode(text);
        textEle.appendChild(textNode);

        lBounds._container.appendChild(textEle);
    },
    
    _onTileUnload: function(evt) {
        console.log('unload       : ' + evt.tile.key);
    },
    
    _onMoveend: function(evt) {
        console.log('--- update ---');
    }
});