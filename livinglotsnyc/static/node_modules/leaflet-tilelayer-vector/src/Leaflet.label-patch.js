
// patch Leaflet.label plugin to avoid null error on viewreset when label has
// already been removed (v0.5.1), also see comment in L.TileLayer.Vector.onAdd
if (L.Label) {
    var orig = L.Label.prototype._updatePosition;
    L.Label.prototype._updatePosition = function() {
        if (this._map) {
            orig.apply(this, arguments);
        }
    };
}