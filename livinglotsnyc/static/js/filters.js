var _ = require('underscore');


module.exports = {
    lotShouldAppear: function (lot, filters) {
        // Layers
        var lotLayers = lot.feature.properties.layers.split(',');
        if (_.isEmpty(_.intersection(lotLayers, filters.layers))) {
            return false;
        }

        // Projects
        if (filters.projects === 'exclude' && _.contains(lotLayers, 'in_use')) {
            return false;
        }
        else if (filters.projects === 'only' && !_.contains(lotLayers, 'in_use')) {
            return false;
        }

        return true;
    },

    paramsToFilters: function (params) {
        var filters = _.extend({}, params);
        filters.layers = filters.layers.split(',');
        return filters;
    }
};
