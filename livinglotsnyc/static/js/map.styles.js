//
// Lot map styles by layer for maps
//
var _ = require('underscore');

var fillColors = {
    default: '#000000',
    in_use: '#FD39FE',
    private: '#4292F1',
    public: '#66A954',
    gutterspace: '#FE3627'
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
        if (_.contains(layers, 'gutterspace')) {
            return fillColors.gutterspace;
        }
        return fillColors.default;
    }
};
