//
// Lot map styles by layer for maps
//
var _ = require('underscore');

var fillColors = {
    default: '#000000',
    in_use: '#97b03d',
    private: '#ea292e',
    public: '#812683'
};

module.exports = {
    fillColors: fillColors,

    getLayerColor: function (layers) {
        if (_.contains(layers, 'in_use')) {
            return fillColors.in_use;
        }
        if (_.contains(layers, 'public')) {
            return fillColors.public;
        }
        if (_.contains(layers, 'private')) {
            return fillColors.private;
        }
        return fillColors.default;
    }
};
