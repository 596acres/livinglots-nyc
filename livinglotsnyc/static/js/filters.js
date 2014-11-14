var _ = require('underscore');


module.exports = {
    lotShouldAppear: function (lot, filters) {
        var ownershipLayers = ['public', 'private_opt_in'],
            peopleInvolvedLayers = ['in_use', 'in_use_started_here', 'organizing'],
            lotLayers = lot.feature.properties.layers.split(','),
            lotLayersOwnership = _.intersection(lotLayers, ownershipLayers),
            lotLayersNotOwnership = _.difference(lotLayers, ownershipLayers);

        // Gutterspace, no matter owner
        if (_.contains(_.intersection(lotLayersNotOwnership, filters.layers), 'gutterspace')) {
            return true;
        }

        // Ownership layers
        if (_.isEmpty(_.intersection(lotLayersOwnership, filters.owner_types))) {
            return false;
        }

        // Individual owners
        if (filters.public_owners && _.contains(lotLayersOwnership, 'public') &&
                !_.contains(filters.public_owners, lot.feature.properties.owner)) {
            return false;
        }
        if (filters.private_owners && 
                _.contains(lotLayersOwnership, 'private_opt_in') &&
                !_.contains(filters.private_owners, lot.feature.properties.owner)) {
            return false;
        }

        // No people involved (just vacant): no_people selected, lot has no
        // people-involving layers associated with it
        if (_.contains(filters.layers, 'no_people') &&
            _.isEmpty(_.intersection(peopleInvolvedLayers, lotLayersNotOwnership)) &&
            !_.contains(lotLayers, 'gutterspace')) {
            return true;
        }

        // Other layers
        if (_.isEmpty(_.intersection(lotLayersNotOwnership, filters.layers))) {
            return false;
        }

        return true;
    },

    paramsToFilters: function (params) {
        var filters = _.extend({}, params);
        filters.layers = filters.layers.split(',');
        filters.owner_types = filters.owner_types.split(',');
        if (filters.public_owners) {
            filters.public_owners = _.map(filters.public_owners.split(','), function (ownerPk) {
                return parseInt(ownerPk);
            });
        }
        if (filters.private_owners) {
            filters.private_owners = _.map(filters.private_owners.split(','), function (ownerPk) {
                return parseInt(ownerPk);
            });
        }
        return filters;
    }
};
