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
        else if (filters.projects === 'started_here') {
            if (_.contains(lotLayers, 'in_use') && !_.contains(lotLayers, 'in_use_started_here')) {
                return false;
            }
        }

        // Owners
        if (filters.public_owners &&
            !_.contains(filters.public_owners, lot.feature.properties.owner)) {
            return false;
        }

        return true;
    },

    paramsToFilters: function (params) {
        var filters = _.extend({}, params);
        filters.layers = filters.layers.split(',');
        if (filters.public_owners) {
            filters.public_owners = _.map(filters.public_owners.split(','), function (ownerPk) {
                return parseInt(ownerPk);
            });
        }
        return filters;
    }
};
